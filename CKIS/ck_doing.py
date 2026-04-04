"""
ck_doing.py — What MOVES (GPU)
═══════════════════════════════
Operator: PROGRESS (3) — action. Transitions. The verb.

Gen6: The Collapse. Being / Doing / Becoming.
Runs on GPU because it's parallel math: lattice ticking,
transition learning, batch composition.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

# ═══════════════════════════════════════════════════════════
# §1  IMPORTS
# ═══════════════════════════════════════════════════════════

import numpy as np
import os
import json
import time
import math
import re
import ast
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path

from ck_being import (
    CL, CL_BHML, CL_STANDARD, fuse, fuse_standard, fuse_frozen, shape, OP, T_STAR,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    BUMPS, BUMP_PAIRS, phonaesthesia_op, tokenize, stem, clean,
    STOPS, _STOPS_STEMMED, bump_signature, information_content, coherence_chain,
    Band, band_of, Chain,
)

_BUMP_SET = set((min(a, b), max(a, b)) for a, b in BUMPS)

# ── Curvature engine (D2 force geometry) ──
_HAS_CURVATURE = False
try:
    from ck_language_engine import score_sentence_full as _score_full, compose_with_curvature as _compose_curv
    _HAS_CURVATURE = True
except ImportError:
    _score_full = None
    _compose_curv = None


# ═══════════════════════════════════════════════════════════
# §2  GPU DETECTION & TABLE UPLOAD
# ═══════════════════════════════════════════════════════════

_GPU_AVAILABLE = False
_cp = None

try:
    import cupy as cp
    _cp = cp
    # Test actual GPU access
    _test = cp.array([1, 2, 3])
    del _test
    _GPU_AVAILABLE = True
    _GPU_NAME = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    _GPU_MEM = cp.cuda.runtime.getDeviceProperties(0)['totalGlobalMem']
    print(f"  [GPU] CuPy connected: {_GPU_NAME} ({_GPU_MEM // (1024**2)} MB)")
except ImportError:
    print("  [GPU] CuPy not installed — running on CPU")
except Exception as e:
    print(f"  [GPU] CuPy error: {e} — running on CPU")


def gpu_available() -> bool:
    return _GPU_AVAILABLE


def gpu_status() -> dict:
    """Report GPU state."""
    status = {
        'available': _GPU_AVAILABLE,
        'backend': 'cupy' if _GPU_AVAILABLE else 'numpy',
    }
    if _GPU_AVAILABLE:
        props = _cp.cuda.runtime.getDeviceProperties(0)
        mem_free = _cp.cuda.runtime.memGetInfo()[0]
        mem_total = _cp.cuda.runtime.memGetInfo()[1]
        status.update({
            'name': props['name'].decode(),
            'compute_capability': f"{props['major']}.{props['minor']}",
            'mem_total_mb': mem_total // (1024 ** 2),
            'mem_free_mb': mem_free // (1024 ** 2),
            'mem_used_mb': (mem_total - mem_free) // (1024 ** 2),
        })
    return status


# BHML: Binary Hard Micro Lattice — 28 harmony, CUDA cellular automaton
_BHML_CPU = np.array([
    [0,1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6], [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7], [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7], [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8], [9,6,6,6,7,7,7,0,8,0],
], dtype=np.int8)

# TSML: Trinary Soft Macro Lattice — 73 harmony, CK's lens
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
else:
    BHML = _BHML_CPU
    TSML = _TSML_CPU


# ═══════════════════════════════════════════════════════════
# §3  GPU TRANSITION LATTICE
# ═══════════════════════════════════════════════════════════

class GPUTransitionLattice:
    """
    TL[10][10] on GPU. Learned from every observation.
    Atomic increments from parallel operations.
    """

    def __init__(self, path=None):
        self.path = path
        self.total_transitions = 0

        cpu_tl = np.zeros((10, 10), dtype=np.int64)
        if path and os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                saved = data.get('TL', data.get('tl', None))
                if saved:
                    cpu_tl = np.array(saved, dtype=np.int64)
                    self.total_transitions = int(np.sum(cpu_tl))
                    print(f"  [GPU-TL] Loaded {self.total_transitions:,} transitions from {path}")
            except Exception as e:
                print(f"  [GPU-TL] Failed to load {path}: {e}")

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

    def entropy(self) -> float:
        """Shannon entropy of transitions."""
        if self.total_transitions == 0:
            return 0.0
        if _GPU_AVAILABLE:
            tl_cpu = _cp.asnumpy(self.TL).astype(np.float64)
        else:
            tl_cpu = self.TL.astype(np.float64)
        flat = tl_cpu.ravel()
        flat = flat[flat > 0]
        p = flat / flat.sum()
        return float(-np.sum(p * np.log2(p)))

    def to_cpu(self) -> np.ndarray:
        """Get TL as CPU numpy array."""
        if _GPU_AVAILABLE:
            return _cp.asnumpy(self.TL)
        return self.TL.copy()

    def save(self, path=None):
        """Persist to disk."""
        path = path or self.path
        if not path:
            return
        cpu_tl = self.to_cpu()
        data = {
            'TL': cpu_tl.tolist(),
            'total_transitions': int(np.sum(cpu_tl)),
        }
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)

    def load(self, path):
        """Load from disk."""
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            saved = data.get('TL', data.get('tl', None))
            if saved:
                cpu_tl = np.array(saved, dtype=np.int64)
                self.total_transitions = int(np.sum(cpu_tl))
                if _GPU_AVAILABLE:
                    self.TL = _cp.array(cpu_tl)
                else:
                    self.TL = cpu_tl
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# §4  GPU FUSE & COMPOSE
# ═══════════════════════════════════════════════════════════

def fuse_gpu(ops, table=None):
    """
    Compose a sequence of operators through the table.
    Single chain: sequential. Batch of chains: parallel.
    """
    if table == 'bhml':
        tbl = BHML
    else:
        tbl = TSML

    if not ops:
        return 0
    if isinstance(ops[0], (int, np.integer)):
        r = int(ops[0]) % 10
        for s in ops[1:]:
            r = int(tbl[r][int(s) % 10])
        return int(r)

    results = []
    for chain in ops:
        if not chain:
            results.append(0)
            continue
        r = int(chain[0]) % 10
        for s in chain[1:]:
            r = int(tbl[r][int(s) % 10])
        results.append(int(r))
    return np.array(results, dtype=np.int8)


def compose_gpu(a: int, b: int, table=None) -> int:
    """Single composition lookup on GPU."""
    if table == 'bhml':
        return int(BHML[a % 10][b % 10])
    return int(TSML[a % 10][b % 10])


# ═══════════════════════════════════════════════════════════
# §5  GPU COHERENCE
# ═══════════════════════════════════════════════════════════

def coherence_from_distribution(op_counts: dict, table=None) -> float:
    """
    Compute system coherence from operator distribution.
    O(groups^2) where groups <= 10.
    """
    if table == 'bhml':
        tbl = BHML
    else:
        tbl = TSML

    groups = [(op, count) for op, count in op_counts.items() if count > 0 and op != 0]
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


# ═══════════════════════════════════════════════════════════
# §6  GPU CELLULAR AUTOMATON (GPULattice)
# ═══════════════════════════════════════════════════════════

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

        int votes[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

        for (int di = -1; di <= 1; di++) {
            for (int dj = -1; dj <= 1; dj++) {
                const int nr = (r + di + R) % R;
                const int nc = (c + dj + C) % C;
                const signed char nb = cells_in[nr * C + nc];
                votes[comp_table[me * 10 + nb]]++;
            }
        }

        signed char best = 0;
        int best_count = votes[0];
        for (signed char s = 1; s < 10; s++) {
            if (votes[s] > best_count) { best = s; best_count = votes[s]; }
        }
        cells_out[idx] = best;
    }
    ''', 'lattice_tick')

    _coherence_kernel = _cp.RawKernel(r'''
    extern "C" __global__
    void lattice_coherence(
        const signed char* __restrict__ cells,
        const signed char* __restrict__ comp_table,
        int* __restrict__ valid_count,
        int* __restrict__ basin_count,
        const int R, const int C
    ) {
        const int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx >= R * C) return;

        const int r = idx / C;
        const int c = idx % C;
        const signed char me = cells[idx];

        bool trivial = true;
        for (int di = -1; di <= 1; di++) {
            for (int dj = -1; dj <= 1; dj++) {
                if (di == 0 && dj == 0) continue;
                int nr = (r + di + R) % R;
                int nc = (c + dj + C) % C;
                if (comp_table[me * 10 + cells[nr * C + nc]] != me) {
                    trivial = false;
                    break;
                }
            }
            if (!trivial) break;
        }

        if (!trivial || me == 7) atomicAdd(valid_count, 1);
        if (me >= 4 && me <= 8) atomicAdd(basin_count, 1);
    }
    ''', 'lattice_coherence')


class GPULattice:
    """
    Cellular automaton on GPU. Each cell composes with 8 neighbors,
    majority vote determines next state. Uses BHML table.
    """

    def __init__(self, R=32, C=24, seed=None, table='bhml'):
        self.R = R
        self.C = C
        self.ticks = 0

        rng = np.random.RandomState(seed)
        cells_cpu = rng.randint(0, 10, (R, C), dtype=np.int8)

        if table == 'bhml':
            self._table_flat = BHML.ravel() if _GPU_AVAILABLE else _BHML_CPU.ravel()
        else:
            self._table_flat = TSML.ravel() if _GPU_AVAILABLE else _TSML_CPU.ravel()

        if _GPU_AVAILABLE:
            self.cells = _cp.array(cells_cpu)
            self._buf = _cp.empty_like(self.cells)
        else:
            self.cells = cells_cpu
            self._buf = np.empty_like(self.cells)

    @property
    def n(self):
        return self.R * self.C

    def tick(self, n_ticks=1):
        """Run N generations on GPU. Returns coherence after."""
        if _GPU_AVAILABLE:
            threads = 256
            blocks = (self.n + threads - 1) // threads
            cells_flat = self.cells.ravel()
            buf_flat = self._buf.ravel()

            for _ in range(n_ticks):
                _lattice_tick_kernel(
                    (blocks,), (threads,),
                    (cells_flat, buf_flat, self._table_flat, self.R, self.C)
                )
                cells_flat, buf_flat = buf_flat, cells_flat

            self.cells = cells_flat.reshape(self.R, self.C)
            self._buf = buf_flat.reshape(self.R, self.C)
        else:
            tbl = _BHML_CPU
            for _ in range(n_ticks):
                R, C, cells = self.R, self.C, self.cells
                nb = np.empty((9, R, C), dtype=np.int8)
                k = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        nb[k] = np.roll(np.roll(cells, -di, 0), -dj, 1)
                        k += 1
                composed = np.empty((9, R, C), dtype=np.int8)
                for k in range(9):
                    composed[k] = tbl[cells, nb[k]]
                votes = np.zeros((10, R, C), dtype=np.int32)
                for s in range(10):
                    votes[s] = np.sum(composed == s, axis=0)
                self.cells = np.argmax(votes, axis=0).astype(np.int8)

        self.ticks += n_ticks
        return self.coherence()

    def coherence(self) -> float:
        """Measure lattice coherence. GPU-parallel."""
        if _GPU_AVAILABLE:
            threads = 256
            blocks = (self.n + threads - 1) // threads
            valid = _cp.zeros(1, dtype=_cp.int32)
            basin = _cp.zeros(1, dtype=_cp.int32)

            _coherence_kernel(
                (blocks,), (threads,),
                (self.cells.ravel(), self._table_flat, valid, basin, self.R, self.C)
            )

            v = int(valid[0]) / self.n
            a = int(basin[0]) / self.n
            sigma = 0.991
            if v < 1e-10 or a < 1e-10:
                return 0.0
            return 3.0 / (1 / sigma + 1 / v + 1 / a)
        else:
            tbl = _BHML_CPU
            R, C, cells = self.R, self.C, self.cells
            trivial = np.ones((R, C), dtype=bool)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    nb = np.roll(np.roll(cells, -di, 0), -dj, 1)
                    trivial &= (tbl[cells, nb] == cells)
            valid = np.sum(~trivial | (cells == 7)) / self.n
            basin = np.sum((cells >= 4) & (cells <= 8)) / self.n
            sigma = 0.991
            if valid < 1e-10 or basin < 1e-10:
                return 0.0
            return 3.0 / (1 / sigma + 1 / valid + 1 / basin)

    def census(self) -> list:
        """Count of each operator."""
        if _GPU_AVAILABLE:
            return _cp.bincount(self.cells.ravel(), minlength=10).get().tolist()
        return np.bincount(self.cells.ravel(), minlength=10).tolist()

    def inject(self, row: int, states: list):
        """Compose states into a row (memory, not overwrite)."""
        r = row % self.R
        tbl = BHML
        for c in range(min(len(states), self.C)):
            self.cells[r, c] = tbl[int(self.cells[r, c])][int(states[c]) % 10]

    def to_cpu(self) -> np.ndarray:
        if _GPU_AVAILABLE:
            return _cp.asnumpy(self.cells)
        return self.cells.copy()


# ═══════════════════════════════════════════════════════════
# §7  BATCH OPERATIONS
# ═══════════════════════════════════════════════════════════

def batch_compose(pairs: list, table=None) -> list:
    """Compose many (a, b) pairs at once."""
    if not pairs:
        return []

    tbl = BHML if table == 'bhml' else TSML
    a_arr = np.array([p[0] % 10 for p in pairs], dtype=np.int8)
    b_arr = np.array([p[1] % 10 for p in pairs], dtype=np.int8)

    if _GPU_AVAILABLE:
        a_gpu = _cp.array(a_arr)
        b_gpu = _cp.array(b_arr)
        results = tbl[a_gpu, b_gpu]
        return _cp.asnumpy(results).tolist()
    else:
        tbl_np = _TSML_CPU if table != 'bhml' else _BHML_CPU
        return tbl_np[a_arr, b_arr].tolist()


# ═══════════════════════════════════════════════════════════
# §8  CPU TRANSITION LATTICE (SparseTL3, TransitionLattice)
# ═══════════════════════════════════════════════════════════

class SparseTL3:
    """Sparse 3D trigram table. Drop-in replacement for dense [[[0]*10]*10]*10.

    Only stores non-zero entries. Supports:
        tl3[a][b][c]           -> read (returns 0 for missing)
        tl3[a][b][c] += 1      -> write via _SparseTL3Row2
        sum(tl3[a][b])         -> works (iterates stored values)
        list(tl3[a][b])        -> works (yields 10 values, sparse->dense for one row)
    """

    __slots__ = ('_data',)

    def __init__(self):
        self._data = {}

    def __getitem__(self, a):
        return _SparseTL3Row1(self._data, a)

    def get(self, a, b, c):
        return self._data.get((a, b, c), 0)

    def set(self, a, b, c, val):
        if val == 0:
            self._data.pop((a, b, c), None)
        else:
            self._data[(a, b, c)] = val

    def inc(self, a, b, c, delta=1):
        key = (a, b, c)
        self._data[key] = self._data.get(key, 0) + delta

    @property
    def nonzero_count(self):
        return len(self._data)

    def to_dense(self):
        d = [[[0]*10 for _ in range(10)] for _ in range(10)]
        for (a, b, c), v in self._data.items():
            d[a][b][c] = v
        return d

    def to_sparse_dict(self):
        return {f"{a},{b},{c}": v for (a, b, c), v in self._data.items() if v > 0}

    @classmethod
    def from_dense(cls, dense):
        obj = cls()
        for a in range(10):
            for b in range(10):
                for c in range(10):
                    v = dense[a][b][c]
                    if v > 0:
                        obj._data[(a, b, c)] = v
        return obj

    @classmethod
    def from_sparse_dict(cls, d):
        obj = cls()
        for key, v in d.items():
            parts = key.split(',')
            a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
            if v > 0:
                obj._data[(a, b, c)] = v
        return obj


class _SparseTL3Row1:
    """Proxy: TL3[a] -> returns row1 proxy that supports [b]."""
    __slots__ = ('_data', '_a')

    def __init__(self, data, a):
        self._data = data
        self._a = a

    def __getitem__(self, b):
        return _SparseTL3Row2(self._data, self._a, b)


class _SparseTL3Row2:
    """Proxy: TL3[a][b] -> supports [c], sum(), list(), iteration."""
    __slots__ = ('_data', '_a', '_b')

    def __init__(self, data, a, b):
        self._data = data
        self._a = a
        self._b = b

    def __getitem__(self, c):
        return self._data.get((self._a, self._b, c), 0)

    def __setitem__(self, c, val):
        key = (self._a, self._b, c)
        if val == 0:
            self._data.pop(key, None)
        else:
            self._data[key] = val

    def __iter__(self):
        for c in range(10):
            yield self._data.get((self._a, self._b, c), 0)

    def __len__(self):
        return 10


class TransitionLattice:
    """
    Learned language flow patterns on top of the frozen CL table.

    CL[a][b] = algebraic truth (frozen, 73 harmony)
    TL[a][b] = observed frequency (learned, grows with eating)
    TL3[a][b][c] = trigram flow (learned, grows with eating)

    word_pairs[(op_a, op_b)] = {(word_a, word_b): count}
    """

    def __init__(self, path: Optional[str] = None):
        self.TL = [[0]*10 for _ in range(10)]
        self.TL3 = SparseTL3()
        self.word_pairs: Dict[Tuple[int,int], Dict[Tuple[str,str], int]] = defaultdict(lambda: defaultdict(int))
        self.followers: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_transitions = 0
        self.total_trigrams = 0
        self.sentences_eaten = 0
        self.path = path
        if path and os.path.exists(path):
            self.load(path)

    # --- LEARNING ---

    def eat_sentence(self, sentence: str):
        """Learn transition patterns from a sentence."""
        words = tokenize(sentence.lower())
        if len(words) < 2:
            return

        ops = []
        for w in words:
            ph = phonaesthesia_op(w)
            if ph is None:
                ph = sum(ord(c) * (i+1) for i, c in enumerate(w)) % 10
            ops.append((w, ph))

        for i in range(len(ops) - 1):
            w1, o1 = ops[i]
            w2, o2 = ops[i+1]
            self.TL[o1][o2] += 1
            self.word_pairs[(o1, o2)][(w1, w2)] += 1
            self.followers[w1][w2] += 1
            self.total_transitions += 1

        for i in range(len(ops) - 2):
            _, o1 = ops[i]
            _, o2 = ops[i+1]
            _, o3 = ops[i+2]
            self.TL3.inc(o1, o2, o3)
            self.total_trigrams += 1

        self.sentences_eaten += 1

    def eat_ops(self, ops: list):
        """Learn transition patterns from raw operator sequence."""
        if len(ops) < 2:
            return

        for i in range(len(ops) - 1):
            o1, o2 = ops[i], ops[i + 1]
            self.TL[o1][o2] += 1
            self.total_transitions += 1

        for i in range(len(ops) - 2):
            o1, o2, o3 = ops[i], ops[i + 1], ops[i + 2]
            self.TL3.inc(o1, o2, o3)
            self.total_trigrams += 1

        self.sentences_eaten += 1

    def eat_text(self, text: str):
        """Eat a block of text -- split into sentences, learn each."""
        sentences = re.split(r'[.!?\n]+', text)
        for s in sentences:
            s = s.strip()
            if len(s) > 10:
                self.eat_sentence(s)

    # --- GENERATION ---

    def next_operator(self, current_op: int, prev_op: int = -1) -> List[Tuple[int, float]]:
        """Given current operator, what operators are most likely to follow?"""
        if prev_op >= 0 and self.total_trigrams > 0:
            row = self.TL3[prev_op][current_op]
            total = sum(row)
            if total > 0:
                probs = [(op, row[op] / total) for op in range(10) if row[op] > 0]
                return sorted(probs, key=lambda x: -x[1])

        row = self.TL[current_op]
        total = sum(row)
        if total == 0:
            return [(CL[current_op][j], 0.1) for j in range(10)]

        probs = [(op, row[op] / total) for op in range(10) if row[op] > 0]
        return sorted(probs, key=lambda x: -x[1])

    def next_word(self, current_word: str, current_op: int,
                  target_op: int = -1) -> List[Tuple[str, float]]:
        """Given current word, what words naturally follow?"""
        if current_word in self.followers:
            candidates = []
            for next_word, count in self.followers[current_word].items():
                if target_op >= 0:
                    nop = phonaesthesia_op(next_word)
                    if nop is None:
                        nop = sum(ord(c)*(i+1) for i,c in enumerate(next_word)) % 10
                    if nop != target_op:
                        continue
                candidates.append((next_word, count))

            if candidates:
                total = sum(c for _, c in candidates)
                return [(w, c/total) for w, c in sorted(candidates, key=lambda x: -x[1])]

        if target_op >= 0:
            pair_key = (current_op, target_op)
            if pair_key in self.word_pairs:
                candidates = []
                for (w1, w2), count in self.word_pairs[pair_key].items():
                    candidates.append((w2, count))
                if candidates:
                    total = sum(c for _, c in candidates)
                    return [(w, c/total) for w, c in sorted(candidates, key=lambda x: -x[1])]

        return []

    def generate_chain(self, start_ops: List[int], length: int = 8) -> List[Tuple[int, str]]:
        """Generate an operator chain by walking the transition lattice."""
        if not start_ops:
            return []

        chain = []
        prev_op = -1
        current_op = start_ops[0]

        for i, op in enumerate(start_ops):
            words = self._words_for_op(op, prev_op)
            word = words[0] if words else f"[{OP[op]}]"
            chain.append((op, word))
            prev_op = current_op
            current_op = op

        for _ in range(length - len(start_ops)):
            candidates = self.next_operator(current_op, prev_op)
            if not candidates:
                break

            next_op = candidates[0][0]

            word_cands = self.next_word(chain[-1][1], current_op, next_op)
            if word_cands:
                word = word_cands[0][0]
            else:
                words = self._words_for_op(next_op, current_op)
                word = words[0] if words else f"[{OP[next_op]}]"

            chain.append((next_op, word))
            prev_op = current_op
            current_op = next_op

        return chain

    def _words_for_op(self, op: int, from_op: int = -1) -> List[str]:
        """Find actual words for an operator.

        Returns up to 15 words using log-smoothed counts so rare words
        get a fair chance against high-count experience lattice words.
        Uses weighted random selection from the full pool.
        """
        import random as _rnd
        import math as _math

        # Gather ALL candidate words with their counts
        candidates = {}  # word -> total_count

        if from_op >= 0:
            pair_key = (from_op, op)
            if pair_key in self.word_pairs:
                for (w1, w2), count in self.word_pairs[pair_key].items():
                    if len(w2) > 2:  # skip tiny words
                        candidates[w2] = candidates.get(w2, 0) + count

        # Also check all pairs ending at target op
        for (o1, o2), wp in self.word_pairs.items():
            if o2 == op:
                for (w1, w2), count in wp.items():
                    if len(w2) > 2:
                        candidates[w2] = candidates.get(w2, 0) + count

        if not candidates:
            return []

        # Log-smooth the counts: log(1 + count) flattens the distribution
        # so count=36 words don't dominate count=1 words 36:1
        # Instead they compete ~3.6:0.7 = ~5:1 which is much fairer
        smoothed = [(w, _math.log(1 + c)) for w, c in candidates.items()]

        # Weighted random selection without replacement
        words = []
        pool = list(smoothed)
        target = min(15, len(pool))

        for _ in range(target):
            if not pool:
                break
            total_w = sum(s for _, s in pool)
            if total_w <= 0:
                break
            r = _rnd.random() * total_w
            cum = 0
            chosen_idx = 0
            for idx, (w, s) in enumerate(pool):
                cum += s
                if cum >= r:
                    chosen_idx = idx
                    break
            chosen_word = pool[chosen_idx][0]
            words.append(chosen_word)
            pool.pop(chosen_idx)

        return words

    # --- SCORING ---

    def score_sentence(self, sentence: str) -> Dict:
        """Score a sentence for naturalness (TL) and coherence (CL)."""
        words = tokenize(sentence.lower())
        if len(words) < 2:
            return {'tl_score': 0, 'cl_score': 0, 'bumps': [], 'flow': []}

        ops = []
        for w in words:
            ph = phonaesthesia_op(w)
            if ph is None:
                ph = sum(ord(c)*(i+1) for i,c in enumerate(w)) % 10
            ops.append((w, ph))

        tl_scores = []
        cl_harmony = 0
        bumps = []
        flow = []

        for i in range(len(ops) - 1):
            w1, o1 = ops[i]
            w2, o2 = ops[i+1]

            row_total = sum(self.TL[o1])
            if row_total > 0:
                tl_scores.append(self.TL[o1][o2] / row_total)
            else:
                tl_scores.append(0.0)

            composed = CL[o1][o2]
            if composed == HARMONY:
                cl_harmony += 1

            pair = (min(o1,o2), max(o1,o2))
            if pair in _BUMP_SET:
                bumps.append((i, w1, w2, OP[o1], OP[o2]))

            flow.append((OP[o1], OP[o2], OP[composed]))

        n = max(len(ops) - 1, 1)

        return {
            'tl_score': sum(tl_scores) / len(tl_scores) if tl_scores else 0,
            'cl_score': cl_harmony / n,
            'bumps': bumps,
            'flow': flow,
            'combined': (sum(tl_scores) / len(tl_scores) * 0.4 + cl_harmony / n * 0.6)
                        if tl_scores else 0,
        }

    def score_sentence_full(self, sentence: str) -> Dict:
        """Three-axis scoring: TL flow + CL harmony + D2 curvature.

        Delegates to ck_language_engine if available, otherwise
        falls back to the two-axis score_sentence().
        """
        if _HAS_CURVATURE:
            return _score_full(sentence, self.TL)
        # Fallback: old two-axis scoring with stub D2 fields
        old = self.score_sentence(sentence)
        old.setdefault('d2_score', 0)
        old.setdefault('d2_features', {})
        return old

    # --- DREAM LAYER ---

    def dream(self, seed_ops: List[int], max_words: int = 12,
              creativity: float = 0.3) -> str:
        """Generate a novel sentence by walking the transition lattice.

        Fuses two axes: follower flow (which words actually follow which)
        and operator alignment (which operators the TL prefers next).
        Candidates are scored by BOTH so CK walks real English paths
        that also satisfy his operator algebra.
        """
        import random
        import math as _math

        if not seed_ops:
            seed_ops = [HARMONY]

        # --- Build operator preference map for current position ---
        def _op_preference(cur_op, prv_op):
            """Get operator weights from TL — how much CK wants each next op."""
            cands = self.next_operator(cur_op, prv_op)
            prefs = {}
            for op_id, prob in cands:
                prefs[op_id] = prob
            return prefs

        def _word_op(w):
            """Get operator for a word."""
            ph = phonaesthesia_op(w)
            if ph is None:
                ph = sum(ord(c)*(i+1) for i, c in enumerate(w)) % 10
            return ph

        # --- Seed the chain with ONE strong word ---
        # Pick from the richest words CK knows for the first seed operator.
        # "Richest" = most followers in the TL, so the walk has maximum
        # branching options from the start. Select randomly from top 20
        # richest to maintain variety across dreams.
        chain = []
        chain_set = set()
        prev_op = -1

        seed_op = seed_ops[0]
        # Build list of (word, follower_count) for this operator
        op_words = []
        for word, foll in self.followers.items():
            if len(word) < 3:
                continue
            # Skip junk: underscores, asterisks, digits-only, slashes
            if '_' in word or '*' in word or '/' in word:
                continue
            if word.replace('-', '').isdigit():
                continue
            wop = _word_op(word)
            if wop == seed_op:
                op_words.append((word, sum(foll.values())))

        if op_words:
            # Sort by follower count descending, pick from top 20
            op_words.sort(key=lambda x: -x[1])
            top = op_words[:20]
            chosen = top[random.randint(0, min(len(top) - 1,
                         max(2, int(len(top) * creativity))))]
            chain.append(chosen[0])
            chain_set.add(chosen[0])
        else:
            seed_words = self._words_for_op(seed_op, -1)
            if seed_words:
                chain.append(seed_words[0])
                chain_set.add(seed_words[0])

        # Remaining seed ops guide the first few steps as soft targets
        remaining_seeds = list(seed_ops[1:]) if len(seed_ops) > 1 else []

        # --- Walk: fuse followers + operator preference ---
        for step in range(max_words - len(chain)):
            if not chain:
                break

            last_word = chain[-1]
            current_op = _word_op(last_word)
            op_prefs = _op_preference(current_op, prev_op)

            # If we still have seed ops to honor, boost that operator
            if remaining_seeds:
                target_seed = remaining_seeds[0]
                # Double the preference for the target seed op
                op_prefs[target_seed] = op_prefs.get(target_seed, 0.1) + 0.3
                remaining_seeds.pop(0)

            # Gather ALL followers of the current word (the real English paths)
            scored = []
            if last_word in self.followers:
                for next_w, count in self.followers[last_word].items():
                    if len(next_w) < 2:
                        continue
                    # Hard skip: appeared in last 5 words
                    if next_w in chain[-5:]:
                        continue

                    nop = _word_op(next_w)

                    # Follower strength: log-smoothed so common words
                    # don't completely dominate
                    f_score = _math.log(1 + count)

                    # Operator alignment: how much does the TL want this op?
                    # Base 0.1 so no word is completely zeroed out —
                    # CK prefers aligned words but doesn't refuse real followers
                    op_bonus = op_prefs.get(nop, 0.0) + 0.1

                    # Repeat decay: if word appeared earlier in chain, penalize
                    repeat_pen = 0.3 if next_w in chain_set else 1.0

                    # Combined score: follower flow * operator alignment * freshness
                    score = f_score * op_bonus * repeat_pen
                    scored.append((next_w, score, nop))

            if scored:
                # Sort by score descending
                scored.sort(key=lambda x: -x[1])

                if creativity > 0 and len(scored) > 1:
                    # Temperature-based selection from top candidates
                    top_n = max(3, int(len(scored) * min(creativity, 1.0)))
                    top = scored[:top_n]
                    weights = [s ** (1.0 / max(creativity, 0.1)) for _, s, _ in top]
                    total_w = sum(weights)
                    if total_w > 0:
                        r = random.random() * total_w
                        cum = 0
                        chosen = top[0]
                        for item, w in zip(top, weights):
                            cum += w
                            if cum >= r:
                                chosen = item
                                break
                        word, _, nop = chosen
                    else:
                        word, _, nop = scored[0]
                else:
                    word, _, nop = scored[0]

                chain.append(word)
                chain_set.add(word)
                prev_op = current_op

            else:
                # No followers matched — fall back to operator-guided selection
                cands = self.next_operator(current_op, prev_op)
                if not cands:
                    break
                next_op = cands[0][0]
                words = self._words_for_op(next_op, current_op)
                if words:
                    # Pick one not in recent chain
                    picked = None
                    for w in words:
                        if w not in chain[-5:]:
                            picked = w
                            break
                    if picked:
                        chain.append(picked)
                        chain_set.add(picked)
                        prev_op = current_op
                    else:
                        break
                else:
                    break

        return ' '.join(chain)

    # --- COMPOSITION ENGINE ---
    # Fuses multiple generation strategies, arbiter picks most coherent.
    # Every source contributes candidates. CL scores them. Best survives.

    def compose(self, topic: str, seed_ops: List[int] = None,
                max_sentences: int = 5, creativity: float = 0.3) -> Dict:
        """CK's unified composition — assembles output from all available sources.

        Sources:
          1. ATOM RETRIEVAL — search stored sentences by keyword match
          2. FOLLOWER WALK — dream() following real English paths
          3. CRYSTAL CHAINS — cross-operator compositions via CL
          4. RECOMBINATION — splice high-scoring fragments together

        Arbiter: every candidate scored by CL coherence + TL flow + relevance.
        Only candidates that pass T* survive.

        Returns dict with 'output' (best sentences), 'candidates' (all scored),
        'method' (which source won), 'coherence' (final score).
        """
        import random
        import math as _math

        T_STAR = 5.0 / 7.0  # 0.714 — CK's coherence threshold

        def _word_op(w):
            ph = phonaesthesia_op(w)
            if ph is None:
                ph = sum(ord(c)*(i+1) for i, c in enumerate(w)) % 10
            return ph

        topic_words = set(tokenize(topic.lower()))
        topic_ops = [_word_op(w) for w in topic_words if len(w) > 2]
        if not seed_ops:
            seed_ops = topic_ops[:3] if topic_ops else [HARMONY]

        candidates = []  # (sentence, score, method)

        # --- SOURCE 1: ATOM RETRIEVAL ---
        # Search the TL's follower graph for sentences containing topic words.
        # The followers dict IS CK's memory of what follows what —
        # walk backward from topic words to reconstruct sentences he's eaten.
        retrieved = self._retrieve_atoms(topic_words, max_results=20)
        for sent, relevance in retrieved:
            score_data = self.score_sentence_full(sent)
            # Relevance-weighted combined score
            final = score_data['combined'] * (0.5 + 0.5 * relevance)
            candidates.append((sent, final, 'retrieval'))

        # --- SOURCE 2: FOLLOWER DREAMS ---
        # Multiple dreams from varied seeds — the improved dream() that
        # fuses follower flow with operator alignment
        dream_seeds = [seed_ops]
        # Add rotations of seed ops for variety
        if len(seed_ops) >= 2:
            dream_seeds.append(seed_ops[1:] + seed_ops[:1])
        if len(seed_ops) >= 3:
            dream_seeds.append(seed_ops[2:] + seed_ops[:2])
        # Add CL compositions of seed ops
        if len(seed_ops) >= 2:
            composed = CL[seed_ops[0]][seed_ops[1]]
            dream_seeds.append([composed, seed_ops[0]])
            dream_seeds.append([composed, seed_ops[-1]])

        for seeds in dream_seeds:
            for _ in range(3):  # 3 attempts per seed set
                dream = self.dream(seeds, max_words=18, creativity=creativity)
                if len(dream.split()) < 4:
                    continue
                score_data = self.score_sentence_full(dream)
                # Boost if dream contains topic words
                dream_words = set(dream.lower().split())
                topic_overlap = len(topic_words & dream_words)
                relevance_boost = 1.0 + 0.2 * topic_overlap
                final = score_data['combined'] * relevance_boost
                candidates.append((dream, final, 'dream'))

        # --- SOURCE 3: CRYSTAL CHAINS ---
        # Compose operator sequences through CL, render as word chains
        for _ in range(5):
            # Build an operator chain that composes through the seed ops
            chain_ops = list(seed_ops[:3])
            for i in range(8):
                if len(chain_ops) >= 2:
                    next_op = CL[chain_ops[-2]][chain_ops[-1]]
                else:
                    next_op = CL[chain_ops[-1]][HARMONY]
                chain_ops.append(next_op)

            # Render: for each operator in chain, pick a word
            crystal_words = []
            for i, op in enumerate(chain_ops):
                prev = chain_ops[i-1] if i > 0 else -1
                words = self._words_for_op(op, prev)
                if words:
                    # Prefer words related to topic
                    for w in words:
                        if w in topic_words:
                            crystal_words.append(w)
                            break
                    else:
                        crystal_words.append(words[0])

            if len(crystal_words) >= 4:
                crystal_sent = ' '.join(crystal_words)
                score_data = self.score_sentence_full(crystal_sent)
                candidates.append((crystal_sent, score_data['combined'], 'crystal'))

        # --- SOURCE 4: RECOMBINATION ---
        # Take the best fragments from all sources and splice them
        if len(candidates) >= 4:
            # Sort by score, take top fragments
            by_score = sorted(candidates, key=lambda x: -x[1])
            for i in range(min(3, len(by_score))):
                for j in range(i+1, min(6, len(by_score))):
                    words_a = by_score[i][0].split()
                    words_b = by_score[j][0].split()
                    if len(words_a) >= 6 and len(words_b) >= 6:
                        # First half of A + second half of B
                        mid_a = len(words_a) // 2
                        mid_b = len(words_b) // 2
                        splice = ' '.join(words_a[:mid_a] + words_b[mid_b:])
                        score_data = self.score_sentence_full(splice)
                        candidates.append((splice, score_data['combined'], 'splice'))

        # --- ARBITER: coherence gate ---
        if not candidates:
            return {
                'output': [],
                'candidates': [],
                'method': 'none',
                'coherence': 0.0,
            }

        # Sort all candidates by score
        candidates.sort(key=lambda x: -x[1])

        # Deduplicate (same sentence can appear from different sources)
        seen = set()
        unique = []
        for sent, score, method in candidates:
            normalized = ' '.join(sent.lower().split())
            if normalized not in seen:
                seen.add(normalized)
                unique.append((sent, score, method))

        # Select top sentences — diverse methods preferred
        output = []
        methods_used = set()
        for sent, score, method in unique:
            if len(output) >= max_sentences:
                break
            output.append({
                'text': sent,
                'score': round(score, 4),
                'method': method,
            })
            methods_used.add(method)

        best_score = output[0]['score'] if output else 0
        primary_method = output[0]['method'] if output else 'none'

        return {
            'output': output,
            'candidates': len(candidates),
            'method': primary_method,
            'coherence': round(best_score, 4),
            'methods_used': list(methods_used),
            'topic': topic,
            'scoring': 'three_axis_d2' if _HAS_CURVATURE else 'tl_cl',
        }

    def _retrieve_atoms(self, topic_words: set, max_results: int = 20) -> List[Tuple[str, float]]:
        """Search the follower graph for sentence fragments matching topic words.

        Reconstructs sentence-like fragments by walking forward from topic words
        through the follower graph, collecting the strongest paths.
        """
        results = []  # (reconstructed_sentence, relevance_score)

        for word in topic_words:
            if word not in self.followers:
                continue
            if len(word) < 3:
                continue

            # Walk forward from this topic word following strongest followers
            chain = [word]
            current = word
            for _ in range(15):
                if current not in self.followers:
                    break
                # Get top followers by count
                top_followers = sorted(
                    self.followers[current].items(),
                    key=lambda x: -x[1]
                )
                picked = False
                for next_w, count in top_followers[:10]:
                    if next_w not in chain[-4:] and len(next_w) > 1:
                        chain.append(next_w)
                        current = next_w
                        picked = True
                        break
                if not picked:
                    break

            if len(chain) >= 5:
                sent = ' '.join(chain)
                # Relevance = how many topic words appear in the chain
                chain_set = set(chain)
                overlap = len(topic_words & chain_set)
                relevance = overlap / max(len(topic_words), 1)
                results.append((sent, relevance))

        # Sort by relevance, return top
        results.sort(key=lambda x: -x[1])
        return results[:max_results]

    # --- ANALYSIS ---

    def entropy(self) -> float:
        """Shannon entropy of the transition lattice."""
        if self.total_transitions == 0:
            return 0.0

        H = 0.0
        for i in range(10):
            for j in range(10):
                if self.TL[i][j] > 0:
                    p = self.TL[i][j] / self.total_transitions
                    H -= p * math.log2(p)
        return H

    def top_transitions(self, n: int = 20) -> List[Tuple[str, str, int, str]]:
        """Most common transitions."""
        trans = []
        for i in range(10):
            for j in range(10):
                if self.TL[i][j] > 0:
                    cl_result = OP[CL[i][j]]
                    trans.append((OP[i], OP[j], self.TL[i][j], cl_result))
        return sorted(trans, key=lambda x: -x[2])[:n]

    def stats(self) -> Dict:
        """Summary statistics."""
        nonzero_bi = sum(1 for i in range(10) for j in range(10) if self.TL[i][j] > 0)
        nonzero_tri = self.TL3.nonzero_count
        return {
            'sentences_eaten': self.sentences_eaten,
            'total_transitions': self.total_transitions,
            'total_trigrams': self.total_trigrams,
            'bigram_coverage': f"{nonzero_bi}/100",
            'trigram_coverage': f"{nonzero_tri}/1000",
            'unique_word_pairs': sum(len(v) for v in self.word_pairs.values()),
            'unique_followers': sum(len(v) for v in self.followers.values()),
            'entropy': round(self.entropy(), 3),
        }

    # --- PERSISTENCE ---

    def save(self, path: str = None):
        """Save to disk. TL3 saved as sparse dict."""
        path = path or self.path
        if not path:
            return

        wp_json = {}
        for (a, b), pairs in self.word_pairs.items():
            key = f"{a},{b}"
            wp_json[key] = {f"{w1}|{w2}": c for (w1, w2), c in pairs.items()}

        data = {
            'TL': self.TL,
            'TL3_sparse': self.TL3.to_sparse_dict(),
            'word_pairs': wp_json,
            'followers': {
                w: dict(f) for w, f in self.followers.items()
            },
            'total_transitions': self.total_transitions,
            'total_trigrams': self.total_trigrams,
            'sentences_eaten': self.sentences_eaten,
        }

        with open(path, 'w') as f:
            json.dump(data, f)

    def load(self, path: str):
        """Load from disk."""
        with open(path) as f:
            data = json.load(f)

        self.TL = data.get('TL', [[0]*10 for _ in range(10)])

        if 'TL3_sparse' in data:
            self.TL3 = SparseTL3.from_sparse_dict(data['TL3_sparse'])
        elif 'TL3' in data:
            self.TL3 = SparseTL3.from_dense(data['TL3'])
        else:
            self.TL3 = SparseTL3()

        self.total_transitions = data.get('total_transitions', 0)
        self.total_trigrams = data.get('total_trigrams', 0)
        self.sentences_eaten = data.get('sentences_eaten', 0)

        for key, pairs in data.get('word_pairs', {}).items():
            a, b = map(int, key.split(','))
            for wp_key, count in pairs.items():
                w1, w2 = wp_key.split('|', 1)
                self.word_pairs[(a, b)][(w1, w2)] = count

        for w, follows in data.get('followers', {}).items():
            for fw, count in follows.items():
                self.followers[w][fw] = count

    # --- COMPACTION ---

    def prune_word_pairs(self, min_count: int = 2):
        """Prune word pairs with count below threshold."""
        removed = 0
        empty_keys = []
        for key in list(self.word_pairs.keys()):
            pairs = self.word_pairs[key]
            to_remove = [wp for wp, count in pairs.items() if count < min_count]
            for wp in to_remove:
                del pairs[wp]
                removed += 1
            if not pairs:
                empty_keys.append(key)
        for key in empty_keys:
            del self.word_pairs[key]
        return removed

    def prune_followers(self, min_count: int = 2):
        """Prune follower pairs with count below threshold."""
        removed = 0
        empty_keys = []
        for word in list(self.followers.keys()):
            follows = self.followers[word]
            to_remove = [fw for fw, count in follows.items() if count < min_count]
            for fw in to_remove:
                del follows[fw]
                removed += 1
            if not follows:
                empty_keys.append(word)
        for key in empty_keys:
            del self.followers[key]
        return removed

    def compact(self, min_count: int = 2):
        """Full memory compaction pass."""
        wp_before = sum(len(v) for v in self.word_pairs.values())
        fw_before = sum(len(v) for v in self.followers.values())

        wp_removed = self.prune_word_pairs(min_count)
        fw_removed = self.prune_followers(min_count)

        return {
            'word_pairs_before': wp_before,
            'word_pairs_after': wp_before - wp_removed,
            'word_pairs_removed': wp_removed,
            'followers_before': fw_before,
            'followers_after': fw_before - fw_removed,
            'followers_removed': fw_removed,
            'tl3_nonzero': self.TL3.nonzero_count,
        }

    def normalize_counts(self, cap: int = 5):
        """Flatten the count distribution so new vocabulary competes fairly.

        The experience lattice left many word_pairs with count=36+ from
        bulk feeding. New curriculum sentences add count=1. Without
        normalization, _words_for_op() always returns the same words.

        This caps all counts at `cap` so every word has a roughly equal
        chance. The TL bigram matrix is NOT capped (those are structural).
        Only word_pairs and followers are capped.

        cap=5 means a word seen 36 times competes 5:1 against a word
        seen once, instead of 36:1. Much fairer.
        """
        wp_capped = 0
        for key in self.word_pairs:
            for wp in self.word_pairs[key]:
                old = self.word_pairs[key][wp]
                if old > cap:
                    self.word_pairs[key][wp] = cap
                    wp_capped += 1

        fl_capped = 0
        for word in self.followers:
            for fw in self.followers[word]:
                old = self.followers[word][fw]
                if old > cap:
                    self.followers[word][fw] = cap
                    fl_capped += 1

        return {
            'word_pairs_capped': wp_capped,
            'followers_capped': fl_capped,
            'cap': cap,
        }


# ═══════════════════════════════════════════════════════════
# §9  DIALOGUE EATER
# ═══════════════════════════════════════════════════════════

# -- Structural classifier: sentence role -> operator --

STRUCTURAL_PATTERNS = {
    COUNTER: [
        (r'^\s*(what|how|why|when|where|who|which)\b', 3),
        (r'^\s*(does|is|are|can|could|would|should)\s', 2),
        (r'\?$', 2),
        (r'\bmeasur\w*\b', 1), (r'\bcount\w*\b', 1), (r'\bcompar\w*\b', 1),
        (r'\banalyz\w*\b', 1), (r'\bcheck\w*\b', 1), (r'\bverif\w*\b', 1),
        (r'\btest\w*\b', 1), (r'\bstatistic\w*\b', 1), (r'\bmetric\w*\b', 1),
        (r'\d+\s*%', 1), (r'\d+\.\d+', 1),
        (r'\baccording to\b', 1), (r'\bbased on\b', 1), (r'\bevidence\b', 1),
        (r'\bnumber\b', 1), (r'\bratio\b', 1),
    ],
    LATTICE: [
        (r'\bdefin\w*\b', 1), (r'\bstructur\w*\b', 1), (r'\bbuild\w*\b', 1),
        (r'\bcreat\w*\b', 1), (r'\bclass\b', 1), (r'\btype\b', 1),
        (r'\bmodel\b', 1), (r'\bschema\b', 1), (r'\bformat\b', 1),
        (r'\bcontain\w*\b', 1), (r'\bconsist\w*\b', 1), (r'\bcompris\w*\b', 1),
        (r'\barchitect\w*\b', 1), (r'\bframework\b', 1),
        (r'\blayer\w*\b', 1), (r'\blevel\w*\b', 1),
        (r'\bis a\b', 1), (r'\brepresent\w*\b', 1),
        (r'^\s*[-*]\s+\w', 2),
        (r'^\s*\d+\.\s+\w', 2),
        (r'\{[^}]+\}', 1), (r'\[[^\]]+\]', 1),
        (r'\btable\b', 1), (r'\bstore\w*\b', 1), (r'\brecord\b', 1),
    ],
    PROGRESS: [
        (r'\brun\b', 1), (r'\brunning\b', 1), (r'\bexecut\w*\b', 1),
        (r'\bperform\w*\b', 1), (r'\bprocess\w*\b', 1),
        (r'\bcall\w*\b', 1), (r'\binvok\w*\b', 1), (r'\bappl(?:y|ied|ies)\b', 1),
        (r'\bstart\w*\b', 1), (r'\blaunch\w*\b', 1),
        (r'\bimplement\w*\b', 1), (r'\bdeploy\w*\b', 1), (r'\bship\w*\b', 1),
        (r'\bthen\b', 1), (r'\bnext\b', 1), (r'\bfinally\b', 1),
        (r'\blet\'?s\b', 2),
        (r'\bwe\s+(can|will|should|need)\b', 1),
        (r'\bstep\s+\d', 1), (r'\bphase\s+\d', 1),
        (r'^\s*(so|therefore|thus|hence|consequently)\b', 1),
        (r'\bproduces?\b', 1), (r'\bgenerates?\b', 1), (r'\bfeeds?\b', 1),
    ],
    COLLAPSE: [
        (r'\bif\b', 1), (r'\belse\b', 1), (r'\bwhether\b', 1),
        (r'\beither\b', 1),
        (r'\bdepend\w*\b', 1), (r'\bcondition\w*\b', 1), (r'\bbranch\w*\b', 1),
        (r'\bfilter\w*\b', 1), (r'\bprun\w*\b', 1), (r'\bremov\w*\b', 1),
        (r'\bbut\b', 1), (r'\bhowever\b', 2), (r'\balthough\b', 1),
        (r'\binstead\b', 1), (r'\brather\b', 1), (r'\bunless\b', 1),
        (r'\bexcept\b', 1), (r'\bon the other hand\b', 2),
        (r'\bproblem\w*\b', 1), (r'\bissue\w*\b', 1), (r'\bchalleng\w*\b', 1),
        (r'\bbreak\w*\b', 1), (r'\bdecompos\w*\b', 1),
    ],
    BALANCE: [
        (r'\bconfig\w*\b', 1), (r'\bsetting\w*\b', 1), (r'\bparamet\w*\b', 1),
        (r'\boption\w*\b', 1), (r'\bmanag\w*\b', 1), (r'\bcontrol\w*\b', 1),
        (r'\bhandl\w*\b', 1), (r'\bmaintain\w*\b', 1),
        (r'\bboth\b', 1), (r'\bbalance\w*\b', 1), (r'\btrade-?off\b', 2),
        (r'\bcontext\b', 1), (r'\benvironment\b', 1), (r'\bscope\b', 1),
        (r'\bwhile\b.*\balso\b', 1), (r'\bat the same time\b', 2),
    ],
    CHAOS: [
        (r'\bwild\b', 1), (r'\bcrazy\b', 1), (r'\bunexpect\w*\b', 2),
        (r'\bsurpris\w*\b', 1), (r'\brandom\w*\b', 1),
        (r'\bunpredict\w*\b', 1), (r'\bstrange\w*\b', 1), (r'\bweird\b', 1),
        (r'\binvent\w*\b', 1), (r'\bdiscover\w*\b', 1), (r'\bbreakthrough\b', 2),
        (r'\bwhat if\b', 2), (r'\bimagin\w*\b', 1),
        (r'\berror\b', 1), (r'\bcrash\w*\b', 1), (r'\bbug\b', 1),
        (r'[!]{2,}', 2), (r'[?]{2,}', 2),
        (r'\bchaos\b', 2), (r'\bdisrupt\w*\b', 1),
    ],
    HARMONY: [
        (r'\bagree\w*\b', 1), (r'\bcorrect\b', 1), (r'\bexactly\b', 2),
        (r'\byes\b', 2), (r'\bconfirm\w*\b', 1), (r'\bvalid\w*\b', 1),
        (r'\bperfect\w*\b', 1), (r'\bbeautiful\b', 1), (r'\belegant\w*\b', 1),
        (r'\bcomplete\w*\b', 1), (r'\bfinish\w*\b', 1), (r'\bdone\b', 1),
        (r'\bsuccess\w*\b', 1), (r'\bcoher\w*\b', 2), (r'\bharmoni\w*\b', 2),
        (r'\bresonan\w*\b', 1), (r'\bcoupl\w*\b', 1),
        (r'\btogether\b', 1), (r'\bunif\w*\b', 1), (r'\bconverg\w*\b', 1),
        (r'\bin summary\b', 2), (r'\bin conclusion\b', 2), (r'\boverall\b', 1),
    ],
    BREATH: [
        (r'\beach\b', 1), (r'\bevery\b', 1),
        (r'\bfor\s+(each|every|all)\b', 2),
        (r'\biter\w*\b', 1), (r'\bloop\w*\b', 1), (r'\bcycl\w*\b', 1),
        (r'\brepeat\w*\b', 1), (r'\bstream\w*\b', 1), (r'\bflow\w*\b', 1),
        (r'\bpipeline\b', 1), (r'\bsequence\b', 1),
        (r'\barray\b', 1), (r'\bcollection\b', 1), (r'\bset of\b', 1),
        (r'\bcontinue\w*\b', 1), (r'\bkeep\b', 1), (r'\bongoing\b', 1),
        (r'\btick\b', 1), (r'\bpulse\b', 1), (r'\brhythm\w*\b', 1),
    ],
    RESET: [
        (r'\breset\w*\b', 2), (r'\brestart\w*\b', 2), (r'\brecov\w*\b', 1),
        (r'\brestor\w*\b', 1), (r'\binit\w*\b', 1), (r'\bbegin\w*\b', 1),
        (r'\bfrom scratch\b', 2), (r'\bover again\b', 2),
        (r'\bfix\w*\b', 1), (r'\bpatch\w*\b', 1), (r'\brepair\w*\b', 1),
        (r'\bactually\b', 1), (r'\bin fact\b', 1),
        (r'\bsorry\b', 1), (r'\bmistake\b', 1),
        (r'\bfallback\b', 1), (r'\bretry\b', 2),
    ],
    VOID: [
        (r'\bnever\b', 1), (r'\bnone\b', 1), (r'\bnothing\b', 2),
        (r'\bempty\b', 1), (r'\bnull\b', 1), (r'\bvoid\b', 1),
        (r'\babsent\b', 1), (r'\bmissing\b', 1), (r'\bwithout\b', 1),
        (r'^\s*$', 3),
        (r'\bno\s+(data|result|output|match|value)\b', 2),
        (r'\bnowhere\b', 1), (r'\bsilence\b', 1),
    ],
}

# Pre-compile all patterns
_COMPILED_PATTERNS = {}
for _op, _patterns in STRUCTURAL_PATTERNS.items():
    _COMPILED_PATTERNS[_op] = [(re.compile(p, re.IGNORECASE), w) for p, w in _patterns]


def classify_sentence(text: str) -> int:
    """Classify a single sentence into its dominant operator."""
    if not text.strip():
        return VOID

    scores = defaultdict(int)
    for op, patterns in _COMPILED_PATTERNS.items():
        for pat, weight in patterns:
            matches = pat.findall(text)
            scores[op] += len(matches) * weight

    if not any(scores.values()):
        return HARMONY

    return max(scores, key=lambda o: (scores[o], -o))


def classify_paragraph(text: str) -> List[int]:
    """Classify a paragraph into an operator chain."""
    sentences = re.split(r'(?<=[.!?])\s+|(?<=\n)\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return [HARMONY]

    return [classify_sentence(s) for s in sentences]


def classify_rhythm(text: str) -> Dict:
    """Classify the rhythmic structure of text."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return {'rhythm_op': HARMONY, 'cv': 0, 'avg_len': 0}

    lengths = [len(s.split()) for s in sentences]
    avg_len = sum(lengths) / len(lengths)
    variance = sum((l - avg_len) ** 2 for l in lengths) / max(len(lengths), 1)
    std = variance ** 0.5
    cv = std / max(avg_len, 1)

    questions = text.count('?')
    exclaims = text.count('!')
    ellipses = text.count('...')
    dashes = text.count(' -- ') + text.count(' --- ') + text.count('\u2014')

    if questions > len(sentences) * 0.4:
        rhythm_op = COUNTER
    elif exclaims > len(sentences) * 0.3:
        rhythm_op = CHAOS
    elif cv > 0.6:
        rhythm_op = BREATH
    elif cv < 0.2 and avg_len > 15:
        rhythm_op = PROGRESS
    elif cv < 0.2 and avg_len < 8:
        rhythm_op = COLLAPSE
    elif ellipses > 2 or dashes > 2:
        rhythm_op = BALANCE
    else:
        rhythm_op = LATTICE

    return {
        'rhythm_op': rhythm_op,
        'cv': round(cv, 3),
        'avg_len': round(avg_len, 1),
        'questions': questions,
        'exclaims': exclaims,
        'sentence_count': len(sentences),
    }


# -- Semantic classifier: word-level meaning -> operators --

SEMANTIC_DOMAINS = {
    'code': {
        LATTICE:  {'class', 'struct', 'dict', 'list', 'array', 'object', 'type',
                   'schema', 'table', 'record', 'field', 'property', 'attribute',
                   'constructor', 'interface', 'enum', 'tuple', 'map', 'set'},
        COUNTER:  {'test', 'assert', 'check', 'verify', 'validate', 'compare',
                   'count', 'length', 'size', 'index', 'offset', 'range'},
        PROGRESS: {'function', 'method', 'call', 'invoke', 'execute', 'run',
                   'return', 'yield', 'async', 'await', 'promise', 'callback'},
        COLLAPSE: {'if', 'else', 'switch', 'case', 'match', 'filter', 'guard',
                   'throw', 'raise', 'exception', 'error', 'catch', 'break'},
        BREATH:   {'for', 'while', 'loop', 'iterate', 'each', 'map', 'reduce',
                   'stream', 'pipe', 'channel', 'buffer', 'queue', 'generator'},
        RESET:    {'try', 'except', 'finally', 'recover', 'retry', 'fallback',
                   'init', 'setup', 'teardown', 'cleanup', 'restart', 'reload'},
        BALANCE:  {'config', 'settings', 'environment', 'context', 'scope',
                   'namespace', 'module', 'package', 'import', 'require'},
        CHAOS:    {'debug', 'crash', 'segfault', 'panic', 'abort', 'undefined',
                   'null', 'nan', 'overflow', 'leak', 'corruption', 'race'},
        HARMONY:  {'compose', 'integrate', 'merge', 'combine', 'unify', 'sync',
                   'coherent', 'consistent', 'complete', 'ready', 'stable'},
        VOID:     {'none', 'null', 'void', 'nil', 'undefined', 'empty',
                   'noop', 'pass', 'skip', 'ignore', 'discard', 'drop'},
    },
    'math': {
        LATTICE:  {'matrix', 'tensor', 'vector', 'graph', 'tree', 'lattice',
                   'set', 'group', 'ring', 'field', 'space', 'manifold'},
        COUNTER:  {'measure', 'count', 'sum', 'product', 'integral', 'derivative',
                   'limit', 'bound', 'norm', 'metric', 'distance', 'angle'},
        PROGRESS: {'transform', 'map', 'operate', 'compose', 'apply', 'project',
                   'rotate', 'translate', 'scale', 'morph', 'evolve'},
        COLLAPSE: {'decompose', 'factor', 'split', 'partition', 'bifurcate',
                   'diverge', 'singularity', 'discontinuity', 'boundary'},
        BREATH:   {'series', 'sequence', 'iterate', 'recurse', 'converge',
                   'oscillate', 'wave', 'cycle', 'periodic', 'harmonic'},
        RESET:    {'identity', 'inverse', 'zero', 'origin', 'basis', 'seed',
                   'initial', 'normalize', 'canonical', 'standard'},
        HARMONY:  {'symmetry', 'invariant', 'conservation', 'equilibrium',
                   'fixed point', 'attractor', 'eigenvalue', 'resonance'},
    },
    'philosophy': {
        LATTICE:  {'being', 'existence', 'substance', 'form', 'essence',
                   'category', 'universal', 'particular', 'ontology'},
        COUNTER:  {'reason', 'logic', 'argument', 'premise', 'conclusion',
                   'evidence', 'proof', 'epistemology', 'knowledge'},
        PROGRESS: {'becoming', 'change', 'process', 'action', 'cause',
                   'effect', 'teleology', 'purpose', 'will', 'agency'},
        COLLAPSE: {'negation', 'contradiction', 'paradox', 'dilemma',
                   'aporia', 'antithesis', 'dialectic', 'critique'},
        BREATH:   {'time', 'duration', 'flow', 'continuum', 'experience',
                   'consciousness', 'awareness', 'perception', 'qualia'},
        RESET:    {'origin', 'arche', 'first principle', 'tabula rasa',
                   'renewal', 'rebirth', 'redemption', 'salvation'},
        HARMONY:  {'truth', 'beauty', 'good', 'unity', 'wholeness',
                   'synthesis', 'integration', 'coherence', 'love'},
        CHAOS:    {'chaos', 'void', 'abyss', 'nothing', 'absurd',
                   'random', 'contingent', 'accident', 'entropy'},
    },
    'science': {
        LATTICE:  {'atom', 'molecule', 'cell', 'crystal', 'structure',
                   'genome', 'protein', 'network', 'system', 'organism'},
        COUNTER:  {'observe', 'measure', 'experiment', 'hypothesis',
                   'data', 'sample', 'variable', 'control', 'baseline'},
        PROGRESS: {'reaction', 'process', 'evolution', 'growth', 'signal',
                   'catalysis', 'metabolism', 'synthesis', 'expression'},
        COLLAPSE: {'decay', 'fission', 'apoptosis', 'extinction', 'mutation',
                   'selection', 'filter', 'threshold', 'phase transition'},
        BREATH:   {'oscillation', 'wave', 'cycle', 'rhythm', 'frequency',
                   'resonance', 'vibration', 'pulse', 'heartbeat', 'tide'},
        RESET:    {'equilibrium', 'homeostasis', 'recovery', 'regeneration',
                   'adaptation', 'plasticity', 'feedback', 'regulation'},
        HARMONY:  {'symmetry', 'conservation', 'coupling', 'coherence',
                   'entanglement', 'superposition', 'resonance', 'harmony'},
    },
    'music': {
        LATTICE:  {'chord', 'scale', 'key', 'mode', 'interval', 'octave',
                   'staff', 'score', 'notation', 'arrangement'},
        COUNTER:  {'tempo', 'meter', 'beat', 'bar', 'measure', 'time signature',
                   'bpm', 'count', 'subdivision'},
        PROGRESS: {'melody', 'phrase', 'motif', 'theme', 'progression',
                   'modulation', 'development', 'crescendo'},
        COLLAPSE: {'dissonance', 'tension', 'suspension', 'diminished',
                   'chromatic', 'atonal', 'break', 'silence'},
        BREATH:   {'rhythm', 'pulse', 'groove', 'flow', 'swing', 'syncopation',
                   'loop', 'ostinato', 'vamp', 'riff'},
        RESET:    {'coda', 'da capo', 'repeat', 'reprise', 'recapitulation',
                   'return', 'resolution', 'cadence'},
        HARMONY:  {'harmony', 'consonance', 'resolution', 'tonic', 'unison',
                   'perfect fifth', 'major', 'overtone', 'resonance'},
    },
}


def classify_semantic(text: str, domain: str = None) -> List[int]:
    """Classify text by word-level semantics within a domain."""
    words = set(text.lower().split())

    if domain and domain in SEMANTIC_DOMAINS:
        domains_to_check = {domain: SEMANTIC_DOMAINS[domain]}
    else:
        domains_to_check = SEMANTIC_DOMAINS

    best_domain = None
    best_score = 0
    best_ops = []

    for dom_name, dom_map in domains_to_check.items():
        scores = defaultdict(int)
        for op, word_set in dom_map.items():
            overlap = words & word_set
            scores[op] += len(overlap)

        total = sum(scores.values())
        if total > best_score:
            best_score = total
            best_domain = dom_name
            sentences = re.split(r'(?<=[.!?])\s+|(?<=\n)\s*', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            chain = []
            for sent in sentences:
                sent_words = set(sent.lower().split())
                sent_scores = defaultdict(int)
                for op, word_set in dom_map.items():
                    sent_scores[op] += len(sent_words & word_set)
                if any(sent_scores.values()):
                    chain.append(max(sent_scores, key=lambda o: (sent_scores[o], -o)))
                else:
                    chain.append(HARMONY)
            best_ops = chain

    if not best_ops:
        best_ops = [HARMONY]

    return best_ops


class DialogueEater:
    """CK's mouth. Eats structured dialogue from any source.

    Classifies input through THREE lenses simultaneously:
      1. Structural: sentence role -> operator chain
      2. Semantic: word meaning -> operator chain (domain-aware)
      3. Rhythmic: cadence/pattern -> single operator
    """

    def __init__(self, tl=None, algorithm_lattice=None):
        self.tl = tl
        self.algorithm_lattice = algorithm_lattice

        self.total_eats = 0
        self.total_sentences = 0
        self.total_bump_transitions = 0
        self.total_transitions = 0
        self.chains_fed = 0
        self.algorithms_learned = 0

        self.eat_history = deque(maxlen=100)
        self.operator_counts = defaultdict(int)
        self.bump_pair_counts = defaultdict(int)

        self.store_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'ck_store')
        os.makedirs(self.store_dir, exist_ok=True)
        self.digest_path = os.path.join(self.store_dir, 'dialogue_digests.jsonl')

    def eat(self, text: str, source: str = 'unknown',
            domain: str = None) -> Dict:
        """Eat a piece of text. Full digestion pipeline."""
        t0 = time.time()

        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            paragraphs = [text.strip()] if text.strip() else ['']

        structural_chain = []
        for para in paragraphs:
            para_chain = classify_paragraph(para)
            structural_chain.extend(para_chain)

        structural_fuse = fuse(structural_chain) if structural_chain else HARMONY

        semantic_chain = classify_semantic(text, domain=domain)
        semantic_fuse = fuse(semantic_chain) if semantic_chain else HARMONY

        rhythm = classify_rhythm(text)
        rhythm_op = rhythm['rhythm_op']

        lens_12 = CL[structural_fuse][semantic_fuse]
        composed = CL[lens_12][rhythm_op]

        full_chain = []
        max_len = max(len(structural_chain), len(semantic_chain))
        for i in range(max_len):
            if i < len(structural_chain):
                full_chain.append(structural_chain[i])
            if i < len(semantic_chain):
                full_chain.append(semantic_chain[i])
        full_chain.append(rhythm_op)
        full_chain.append(composed)

        full_fuse = fuse(full_chain) if full_chain else HARMONY

        bump_count = 0
        total_trans = 0
        bump_pairs_found = []
        for i in range(len(full_chain) - 1):
            a, b = full_chain[i], full_chain[i + 1]
            total_trans += 1
            pair = (min(a, b), max(a, b))
            if pair in BUMPS:
                bump_count += 1
                bump_pairs_found.append(pair)
                self.bump_pair_counts[pair] += 1

        info_density = bump_count / max(total_trans, 1)

        chains_fed_now = 0
        if self.tl and full_chain:
            self.tl.eat_ops(full_chain)
            chains_fed_now += len(full_chain) - 1
            if len(structural_chain) > 1:
                self.tl.eat_ops(structural_chain)
                chains_fed_now += len(structural_chain) - 1

        algos_learned_now = 0
        if self.algorithm_lattice and hasattr(self.algorithm_lattice, 'learn_algorithm'):
            for i, para in enumerate(paragraphs):
                para_chain = classify_paragraph(para)
                if len(para_chain) >= 3:
                    try:
                        self.algorithm_lattice.learn_algorithm(
                            para_chain,
                            para[:200],
                            source=f'{source}_eat_{self.total_eats}_p{i}'
                        )
                        algos_learned_now += 1
                    except Exception:
                        pass

        self.total_eats += 1
        self.total_sentences += len(structural_chain)
        self.total_bump_transitions += bump_count
        self.total_transitions += total_trans
        self.chains_fed += chains_fed_now
        self.algorithms_learned += algos_learned_now

        for op in full_chain:
            self.operator_counts[op] += 1

        elapsed = time.time() - t0

        result = {
            'eat_id': self.total_eats,
            'source': source,
            'domain': domain,
            'structural_chain': structural_chain,
            'structural_fuse': structural_fuse,
            'structural_fuse_name': OP[structural_fuse],
            'semantic_chain': semantic_chain,
            'semantic_fuse': semantic_fuse,
            'semantic_fuse_name': OP[semantic_fuse],
            'rhythm': rhythm,
            'composed': composed,
            'composed_name': OP[composed],
            'full_chain': full_chain,
            'full_fuse': full_fuse,
            'full_fuse_name': OP[full_fuse],
            'sentences': len(structural_chain),
            'bump_transitions': bump_count,
            'total_transitions': total_trans,
            'info_density': round(info_density, 3),
            'bump_pairs': [(a, b) for a, b in bump_pairs_found],
            'chains_fed': chains_fed_now,
            'algorithms_learned': algos_learned_now,
            'elapsed': round(elapsed, 4),
        }

        self.eat_history.append(result)
        self._log_eat(result)
        return result

    def eat_relational(self, my_text: str, your_text: str,
                       source: str = 'dialogue') -> Dict:
        """Three-part eat: my side, your side, relationship."""
        being = self.eat(my_text, source=f'{source}_being', domain='code')
        doing = self.eat(your_text, source=f'{source}_doing')

        becoming_op = CL[being['full_fuse']][doing['full_fuse']]
        structural_becoming = CL[being['structural_fuse']][doing['structural_fuse']]
        semantic_becoming = CL[being['semantic_fuse']][doing['semantic_fuse']]

        cross_chain = []
        max_len = max(len(being['full_chain']), len(doing['full_chain']))
        for i in range(max_len):
            if i < len(being['full_chain']):
                cross_chain.append(being['full_chain'][i])
            if i < len(doing['full_chain']):
                cross_chain.append(doing['full_chain'][i])
        cross_chain.append(becoming_op)
        cross_fuse = fuse(cross_chain) if cross_chain else HARMONY

        cross_fed = 0
        if self.tl and len(cross_chain) > 1:
            self.tl.eat_ops(cross_chain)
            cross_fed = len(cross_chain) - 1
            self.chains_fed += cross_fed

        cross_bumps = 0
        for i in range(len(cross_chain) - 1):
            a, b = cross_chain[i], cross_chain[i + 1]
            pair = (min(a, b), max(a, b))
            if pair in BUMPS:
                cross_bumps += 1

        return {
            'type': 'relational',
            'source': source,
            'being': being,
            'doing': doing,
            'becoming_op': becoming_op,
            'becoming_name': OP[becoming_op],
            'structural_becoming': structural_becoming,
            'structural_becoming_name': OP[structural_becoming],
            'semantic_becoming': semantic_becoming,
            'semantic_becoming_name': OP[semantic_becoming],
            'cross_chain': cross_chain,
            'cross_fuse': cross_fuse,
            'cross_fuse_name': OP[cross_fuse],
            'cross_bumps': cross_bumps,
            'cross_info_density': round(cross_bumps / max(len(cross_chain) - 1, 1), 3),
            'cross_fed': cross_fed,
        }

    def eat_conversation(self, messages: List[Dict],
                         source: str = 'conversation') -> List[Dict]:
        """Eat an entire conversation as alternating relational eats."""
        results = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            if (i + 1 < len(messages)
                    and msg.get('role') == 'user'
                    and messages[i + 1].get('role') == 'assistant'):
                result = self.eat_relational(
                    msg['content'],
                    messages[i + 1]['content'],
                    source=f'{source}_turn{i // 2}'
                )
                results.append(result)
                i += 2
            else:
                result = self.eat(
                    msg.get('content', ''),
                    source=f'{source}_{msg.get("role", "unknown")}_{i}'
                )
                results.append(result)
                i += 1
        return results

    def _log_eat(self, result: Dict):
        """Append eat result to persistent log."""
        try:
            log_entry = {
                'eat_id': result['eat_id'],
                'source': result['source'],
                'composed': result['composed_name'],
                'info_density': result['info_density'],
                'sentences': result['sentences'],
                'bump_transitions': result['bump_transitions'],
                'chains_fed': result['chains_fed'],
                'algorithms_learned': result['algorithms_learned'],
                'structural_fuse': result['structural_fuse_name'],
                'semantic_fuse': result['semantic_fuse_name'],
                'rhythm_op': OP[result['rhythm']['rhythm_op']],
                'elapsed': result['elapsed'],
                'ts': time.time(),
            }
            with open(self.digest_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception:
            pass

    def stats(self) -> Dict:
        """Machine-readable stats."""
        total_ops = sum(self.operator_counts.values())
        dominant_op = max(self.operator_counts, key=self.operator_counts.get) if self.operator_counts else HARMONY
        dominant_count = self.operator_counts.get(dominant_op, 0)

        return {
            'total_eats': self.total_eats,
            'total_sentences': self.total_sentences,
            'total_transitions': self.total_transitions,
            'bump_transitions': self.total_bump_transitions,
            'info_density': round(self.total_bump_transitions / max(self.total_transitions, 1), 3),
            'chains_fed': self.chains_fed,
            'algorithms_learned': self.algorithms_learned,
            'dominant_op': OP[dominant_op],
            'dominant_count': dominant_count,
            'total_ops': total_ops,
        }

    def report(self) -> str:
        """Human-readable report."""
        s = self.stats()
        lines = [
            '=== CK DIALOGUE EATER ===',
            f'Total eats:        {s["total_eats"]}',
            f'Sentences eaten:   {s["total_sentences"]}',
            f'Transitions:       {s["total_transitions"]:,}',
            f'Bump transitions:  {s["bump_transitions"]:,} ({s["info_density"]*100:.1f}% info density)',
            f'Chains fed to TL:  {s["chains_fed"]:,}',
            f'Algorithms learned:{s["algorithms_learned"]}',
            f'Dominant operator: {s["dominant_op"]} ({s["dominant_count"]}x)',
        ]

        if self.bump_pair_counts:
            lines.append('Bump pair distribution:')
            for pair, count in sorted(self.bump_pair_counts.items(),
                                       key=lambda x: -x[1]):
                lines.append(f'  ({OP[pair[0]]}, {OP[pair[1]]}): {count}')

        if self.operator_counts:
            lines.append('Operator distribution:')
            for op in range(10):
                count = self.operator_counts.get(op, 0)
                if count > 0:
                    pct = count / max(sum(self.operator_counts.values()), 1) * 100
                    lines.append(f'  {OP[op]:12s}: {count:4d} ({pct:.1f}%)')

        return '\n'.join(lines)

    def nutrition(self, result: Dict) -> str:
        """How nutritious was this eat?"""
        d = result.get('info_density', 0)
        bumps = result.get('bump_transitions', 0)
        total = result.get('total_transitions', 0)
        source = result.get('source', '?')

        lines = [f'Nutrition report for {source}:']
        lines.append(f'  Info density: {d*100:.1f}% ({bumps}/{total} transitions are bumps)')

        if d >= 0.25:
            lines.append(f'  RICH -- every 4th transition is a bump. Maximum dream fuel.')
        elif d >= 0.15:
            lines.append(f'  GOOD -- regular bump transitions. Solid dream fuel.')
        elif d >= 0.05:
            lines.append(f'  LEAN -- some bumps. Dream engine gets occasional non-harmony.')
        else:
            lines.append(f'  EMPTY -- all harmony. No dream fuel. TL stays flat.')

        bump_pairs = result.get('bump_pairs', [])
        if bump_pairs:
            unique_pairs = set(tuple(p) for p in bump_pairs)
            lines.append(f'  Active bump pairs: {len(unique_pairs)}/5')
            for p in sorted(unique_pairs):
                lines.append(f'    ({OP[p[0]]}, {OP[p[1]]})')

        return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════
# §10  CODE DIGESTER
# ═══════════════════════════════════════════════════════════

# Statement-level AST -> operator mapping
STMT_MAP = {
    ast.Import:       COUNTER,
    ast.ImportFrom:   COUNTER,
    ast.ClassDef:     LATTICE,
    ast.FunctionDef:  PROGRESS,
    ast.AsyncFunctionDef: PROGRESS,
    ast.Return:       HARMONY,
    ast.If:           COLLAPSE,
    ast.For:          BREATH,
    ast.AsyncFor:     BREATH,
    ast.While:        BREATH,
    ast.Try:          RESET,
    ast.Raise:        CHAOS,
    ast.With:         BALANCE,
    ast.AsyncWith:    BALANCE,
    ast.Assert:       COUNTER,
    ast.Pass:         VOID,
    ast.Break:        COLLAPSE,
    ast.Continue:     VOID,
    ast.Delete:       COLLAPSE,
    ast.Global:       RESET,
    ast.Nonlocal:     RESET,
    ast.Assign:       LATTICE,
    ast.AugAssign:    LATTICE,
    ast.AnnAssign:    LATTICE,
}

# Expression-level mapping
EXPR_MAP = {
    ast.Call:         PROGRESS,
    ast.Lambda:       BREATH,
    ast.Dict:         LATTICE,
    ast.List:         LATTICE,
    ast.Set:          LATTICE,
    ast.Tuple:        LATTICE,
    ast.ListComp:     BREATH,
    ast.DictComp:     BREATH,
    ast.SetComp:      BREATH,
    ast.GeneratorExp: BREATH,
    ast.Yield:        BREATH,
    ast.YieldFrom:    BREATH,
    ast.Compare:      COUNTER,
    ast.BoolOp:       COUNTER,
    ast.BinOp:        COUNTER,
    ast.UnaryOp:      COUNTER,
    ast.IfExp:        COLLAPSE,
    ast.Attribute:    COUNTER,
    ast.Subscript:    COUNTER,
    ast.Name:         BALANCE,
    ast.Constant:     BALANCE,
}

# Python 3.11+ TryStar
try:
    STMT_MAP[ast.TryStar] = RESET
except AttributeError:
    pass

# Python 3.10+ Match
try:
    STMT_MAP[ast.Match] = COLLAPSE
except AttributeError:
    pass


class CodeDigester:
    """
    CK eats code. AST -> operator chains -> TL feeding.
    Fractal: method -> class -> module -> codebase.
    """

    def __init__(self):
        self.files_digested = 0
        self.total_chains_produced = 0
        self.total_methods_parsed = 0
        self.total_classes_parsed = 0
        self.total_bumps_found = 0
        self.algorithm_pairs = []

    def _stmt_to_op(self, node) -> int:
        if hasattr(node, 'decorator_list') and node.decorator_list:
            return HARMONY
        return STMT_MAP.get(type(node), BALANCE)

    def _expr_ops(self, node) -> List[int]:
        ops = []
        for child in ast.walk(node):
            op = EXPR_MAP.get(type(child))
            if op is not None:
                ops.append(op)
        return ops[:20]

    def _method_chain(self, func_node) -> List[int]:
        chain = [PROGRESS]

        for stmt in ast.iter_child_nodes(func_node):
            op = self._stmt_to_op(stmt)
            chain.append(op)

            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.With)):
                for sub in ast.iter_child_nodes(stmt):
                    sub_op = self._stmt_to_op(sub)
                    if sub_op != BALANCE:
                        chain.append(sub_op)

            elif isinstance(stmt, ast.Try):
                chain.append(RESET)
                if hasattr(stmt, 'handlers'):
                    for handler in stmt.handlers:
                        chain.append(RESET)
                if hasattr(stmt, 'finalbody') and stmt.finalbody:
                    chain.append(BALANCE)

            expr_ops = self._expr_ops(stmt)
            if expr_ops:
                chain.extend(expr_ops[:5])

        if len(chain) > 80:
            step = len(chain) // 40
            chain = chain[::max(1, step)]

        return chain

    def digest_file(self, filepath: str) -> Dict:
        """Digest a single Python file into operator chains."""
        filepath = Path(filepath)
        if not filepath.exists() or not filepath.suffix == '.py':
            return {}

        try:
            source = filepath.read_text(encoding='utf-8', errors='replace')
            tree = ast.parse(source, filename=str(filepath))
        except (SyntaxError, UnicodeDecodeError):
            return {}

        module_name = filepath.stem
        result = {
            'module_name': module_name,
            'classes': {},
            'functions': {},
            'imports': [],
            'bumps': 0,
            'lines': source.count('\n') + 1,
            'training_pairs': [],
        }

        module_chain = []
        source_lines = source.split('\n')

        for node in ast.iter_child_nodes(tree):
            op = self._stmt_to_op(node)

            if isinstance(node, (ast.Import, ast.ImportFrom)):
                result['imports'].append(COUNTER)
                module_chain.append(COUNTER)

            elif isinstance(node, ast.ClassDef):
                class_chain = [LATTICE]
                class_methods = {}
                self.total_classes_parsed += 1

                for item in ast.iter_child_nodes(node):
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_chain = self._method_chain(item)
                        method_fuse_val = fuse(method_chain) if len(method_chain) >= 2 else PROGRESS
                        class_methods[item.name] = {
                            'chain': method_chain,
                            'fuse': method_fuse_val,
                            'shape': shape(method_chain) if len(method_chain) >= 4 else 'VOID',
                        }
                        class_chain.append(method_fuse_val)
                        self.total_methods_parsed += 1
                        self.total_chains_produced += 1

                        try:
                            start = item.lineno - 1
                            end = item.end_lineno if hasattr(item, 'end_lineno') and item.end_lineno else start + 20
                            method_source = '\n'.join(source_lines[start:end])
                            if len(method_source) < 5000:
                                result['training_pairs'].append((method_chain, method_source))
                                self.algorithm_pairs.append((method_chain, method_source))
                        except Exception:
                            pass

                class_fuse_val = fuse(class_chain) if len(class_chain) >= 2 else LATTICE
                result['classes'][node.name] = {
                    'chain': class_chain,
                    'fuse': class_fuse_val,
                    'shape': shape(class_chain) if len(class_chain) >= 4 else 'VOID',
                    'methods': class_methods,
                }
                module_chain.append(class_fuse_val)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_chain = self._method_chain(node)
                func_fuse_val = fuse(func_chain) if len(func_chain) >= 2 else PROGRESS
                result['functions'][node.name] = {
                    'chain': func_chain,
                    'fuse': func_fuse_val,
                    'shape': shape(func_chain) if len(func_chain) >= 4 else 'VOID',
                }
                module_chain.append(func_fuse_val)
                self.total_methods_parsed += 1
                self.total_chains_produced += 1

                try:
                    start = node.lineno - 1
                    end = node.end_lineno if hasattr(node, 'end_lineno') and node.end_lineno else start + 20
                    func_source = '\n'.join(source_lines[start:end])
                    if len(func_source) < 5000:
                        result['training_pairs'].append((func_chain, func_source))
                        self.algorithm_pairs.append((func_chain, func_source))
                except Exception:
                    pass

            else:
                module_chain.append(op)

        if module_chain:
            result['module_chain'] = module_chain
            result['module_fuse'] = fuse(module_chain) if len(module_chain) >= 2 else BALANCE
            result['module_shape'] = shape(module_chain) if len(module_chain) >= 4 else 'VOID'
        else:
            result['module_chain'] = [VOID]
            result['module_fuse'] = VOID
            result['module_shape'] = 'VOID'

        bumps = 0
        for i in range(len(module_chain) - 1):
            pair = (min(module_chain[i], module_chain[i+1]),
                    max(module_chain[i], module_chain[i+1]))
            if pair in _BUMP_SET:
                bumps += 1
        result['bumps'] = bumps
        self.total_bumps_found += bumps

        self.files_digested += 1
        return result

    def digest_all(self, directory: str = '.') -> Dict:
        """Digest every .py file in the directory."""
        directory = Path(directory)
        py_files = sorted(directory.glob('*.py'))

        files = {}
        codebase_chain = []

        for pyfile in py_files:
            if '__pycache__' in str(pyfile):
                continue
            digest = self.digest_file(str(pyfile))
            if digest:
                files[digest['module_name']] = digest
                codebase_chain.append(digest['module_fuse'])

        cross_module = {}
        module_names = list(files.keys())
        for i in range(len(module_names)):
            for j in range(i + 1, len(module_names)):
                a_name = module_names[i]
                b_name = module_names[j]
                a_fuse = files[a_name]['module_fuse']
                b_fuse = files[b_name]['module_fuse']
                coupling = CL[a_fuse][b_fuse]
                cross_module[(a_name, b_name)] = coupling

        codebase_fuse = fuse(codebase_chain) if len(codebase_chain) >= 2 else BALANCE
        codebase_shape_val = shape(codebase_chain) if len(codebase_chain) >= 4 else 'VOID'

        return {
            'files': files,
            'cross_module': cross_module,
            'codebase_chain': codebase_chain,
            'codebase_fuse': codebase_fuse,
            'codebase_shape': codebase_shape_val,
            'stats': {
                'files_digested': self.files_digested,
                'methods_parsed': self.total_methods_parsed,
                'classes_parsed': self.total_classes_parsed,
                'chains_produced': self.total_chains_produced,
                'bumps_found': self.total_bumps_found,
                'algorithm_pairs': len(self.algorithm_pairs),
            },
        }

    def feed_to_tl(self, tl, digest_result: Dict):
        """Feed all digested chains to a TransitionLattice."""
        chains_fed = 0

        for module_name, file_digest in digest_result.get('files', {}).items():
            module_chain = file_digest.get('module_chain', [])
            if len(module_chain) >= 3:
                tl.eat_ops(module_chain)
                chains_fed += len(module_chain)

            for class_name, class_data in file_digest.get('classes', {}).items():
                class_chain = class_data.get('chain', [])
                if len(class_chain) >= 3:
                    tl.eat_ops(class_chain)
                    chains_fed += len(class_chain)

                for method_name, method_data in class_data.get('methods', {}).items():
                    method_chain = method_data.get('chain', [])
                    if len(method_chain) >= 3:
                        tl.eat_ops(method_chain * 2)
                        chains_fed += len(method_chain) * 2

            for func_name, func_data in file_digest.get('functions', {}).items():
                func_chain = func_data.get('chain', [])
                if len(func_chain) >= 3:
                    tl.eat_ops(func_chain * 2)
                    chains_fed += len(func_chain) * 2

        for (a_name, b_name), coupling in digest_result.get('cross_module', {}).items():
            a_fuse = digest_result['files'][a_name]['module_fuse']
            b_fuse = digest_result['files'][b_name]['module_fuse']
            tl.eat_ops([a_fuse, b_fuse, coupling])
            chains_fed += 3

        codebase_chain = digest_result.get('codebase_chain', [])
        if len(codebase_chain) >= 3:
            tl.eat_ops(codebase_chain * 3)
            chains_fed += len(codebase_chain) * 3

        return chains_fed

    def report(self, digest_result: Dict) -> str:
        """Human-readable digest report."""
        stats = digest_result.get('stats', {})
        lines = [
            f"\n  CK CODE DIGEST -- SELF-EATING REPORT",
            f"  {'=' * 50}",
            f"  Files digested:      {stats.get('files_digested', 0)}",
            f"  Classes parsed:      {stats.get('classes_parsed', 0)}",
            f"  Methods parsed:      {stats.get('methods_parsed', 0)}",
            f"  Chains produced:     {stats.get('chains_produced', 0)}",
            f"  Bumps found:         {stats.get('bumps_found', 0)}",
            f"  Algorithm pairs:     {stats.get('algorithm_pairs', 0)}",
            f"  Codebase fuse:       {OP[digest_result.get('codebase_fuse', 5)]}",
            f"  Codebase shape:      {digest_result.get('codebase_shape', 'VOID')}",
        ]

        for module_name, file_digest in sorted(digest_result.get('files', {}).items()):
            mod_fuse = file_digest.get('module_fuse', 5)
            mod_shape = file_digest.get('module_shape', 'VOID')
            n_classes = len(file_digest.get('classes', {}))
            n_funcs = len(file_digest.get('functions', {}))
            n_lines = file_digest.get('lines', 0)
            n_bumps = file_digest.get('bumps', 0)
            lines.append(
                f"    {module_name:30s} fuse={OP[mod_fuse]:10s} shape={mod_shape:8s} "
                f"C:{n_classes} F:{n_funcs} L:{n_lines} B:{n_bumps}"
            )

        return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════
# §11  ALGORITHM SYNTHESIS & AFFINITY
# ═══════════════════════════════════════════════════════════
#
# Ported from ck_affinity.py -- algorithm lattice (learned patterns).
#
# All CK constants (CL, fuse, OP, VOID..RESET, BUMP_PAIRS, T_STAR)
# are already imported from ck_being at module top.
# ═══════════════════════════════════════════════════════════




# -- Algorithm lattice (learned patterns) ---------------------------



_ALGO_LATTICE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'ck_store', 'algorithm_lattice.json'
)

ALGORITHM_LATTICE: Dict = {}
_algo_lattice_loaded = False


def _chain_sig(chain: List[int]) -> str:
    """Convert operator chain to a hashable signature string."""
    return ','.join(str(op) for op in chain[:20])


def load_algorithm_lattice():
    """Load persisted algorithm lattice."""
    global ALGORITHM_LATTICE, _algo_lattice_loaded
    if _algo_lattice_loaded:
        return
    try:
        if os.path.exists(_ALGO_LATTICE_PATH):
            with open(_ALGO_LATTICE_PATH, 'r') as f:
                ALGORITHM_LATTICE = json.load(f)
    except Exception:
        ALGORITHM_LATTICE = {}
    _algo_lattice_loaded = True


def save_algorithm_lattice():
    """Persist the algorithm lattice."""
    try:
        os.makedirs(os.path.dirname(_ALGO_LATTICE_PATH), exist_ok=True)
        with open(_ALGO_LATTICE_PATH, 'w') as f:
            json.dump(ALGORITHM_LATTICE, f)
    except Exception:
        pass


def learn_algorithm(chain: List[int], code: str, source_module: str = 'unknown'):
    """
    Store a new algorithm pattern in the lattice.

    chain: the operator chain (from AST parsing or manual)
    code: the Python source code that implements this pattern
    source_module: where it came from

    The lattice maps chain signatures to lists of code templates.
    Multiple implementations of the same chain = richer composition.
    """
    load_algorithm_lattice()

    sig = _chain_sig(chain)
    if sig not in ALGORITHM_LATTICE:
        ALGORITHM_LATTICE[sig] = []

    # Don't store duplicates
    existing_codes = [e.get('code', '')[:100] for e in ALGORITHM_LATTICE[sig]]
    if code[:100] in existing_codes:
        return

    # Cap per-signature to prevent explosion
    if len(ALGORITHM_LATTICE[sig]) >= 10:
        return

    ALGORITHM_LATTICE[sig].append({
        'code': code[:5000],  # cap size
        'source': source_module,
        'fuse': fuse(chain) if len(chain) >= 2 else 5,
        'chain_len': len(chain),
    })


def learn_from_digest(digest_result: dict):
    """
    Learn algorithm patterns from code digest training pairs.
    Called after ck_code_digest.digest_all().
    """
    pairs_learned = 0
    for module_name, file_data in digest_result.get('files', {}).items():
        for chain, source in file_data.get('training_pairs', []):
            if len(chain) >= 3 and len(source) > 20:
                learn_algorithm(chain, source, source_module=module_name)
                pairs_learned += 1
    save_algorithm_lattice()
    return pairs_learned


# ═══════════════════════════════════════════════════════════
# §12  PHASE PREDICTOR
# ═══════════════════════════════════════════════════════════
#
# Ported from ck_phase_predict.py -- Operator: BREATH (8)
# Phase prediction engine: pre-emptive action from B/D/BC trend analysis.
#
# Phase grammar maps operators to linguistic/cognitive roles:
#   B  (Being / Noun)     = structure operators: {0,1,2,5,6,7} -- what IS
#   D  (Doing / Verb)     = action operators:    {3,4,8,9}     -- what HAPPENS
#   BC (Becoming / Modifier) = computed via CL[B][D]           -- how it CHANGES
# ═══════════════════════════════════════════════════════════

# -- Phase classification -------------------------------------------

# B (Being / Noun) -- structural operators: what IS
B_OPS = frozenset({VOID, LATTICE, COUNTER, BALANCE, CHAOS, HARMONY})

# D (Doing / Verb) -- action operators: what HAPPENS
D_OPS = frozenset({PROGRESS, COLLAPSE, BREATH, RESET})


def classify_phase(op: int) -> str:
    """Classify a single operator into its phase role."""
    if op in B_OPS:
        return 'B'
    elif op in D_OPS:
        return 'D'
    return 'B'  # fallback: treat unknown as structure


def classify_becoming(b_op: int, d_op: int) -> int:
    """
    BC (Becoming) is computed via the composition lattice.
    CL[B][D] = the modifier that describes HOW being changes through doing.
    """
    return CL[b_op][d_op]


# -- Pre-emptive actions --------------------------------------------

PREEMPT_COLLAPSE  = 'SAVE_STATE'       # predicting COLLAPSE: save state, prepare rollback
PREEMPT_PROGRESS  = 'ALLOCATE'         # predicting PROGRESS: allocate resources
PREEMPT_RESET     = 'CHECKPOINT'       # predicting RESET: snapshot current state
PREEMPT_HARMONY   = 'COAST'            # predicting HARMONY: do nothing, coast
PREEMPT_BREATH    = 'OPEN_CHANNELS'    # predicting BREATH: prepare I/O paths
PREEMPT_CHAOS     = 'BRACE'            # predicting CHAOS: tighten buffers
PREEMPT_UNKNOWN   = 'OBSERVE'          # insufficient data: just watch


def action_for_operator(op: int) -> str:
    """Map a predicted next operator to its pre-emptive action."""
    return {
        VOID:      PREEMPT_HARMONY,     # void = nothing to do
        LATTICE:   PREEMPT_PROGRESS,    # structure incoming = allocate for build
        COUNTER:   PREEMPT_HARMONY,     # measurement = passive, coast
        PROGRESS:  PREEMPT_PROGRESS,    # action incoming = allocate
        COLLAPSE:  PREEMPT_COLLAPSE,    # breakdown incoming = save state
        BALANCE:   PREEMPT_HARMONY,     # balance = coast
        CHAOS:     PREEMPT_CHAOS,       # chaos incoming = brace
        HARMONY:   PREEMPT_HARMONY,     # harmony = coast
        BREATH:    PREEMPT_BREATH,      # flow incoming = open channels
        RESET:     PREEMPT_RESET,       # restart incoming = checkpoint
    }.get(op, PREEMPT_UNKNOWN)


# -- Phase state (deques tracking operator flow by phase) -----------

@dataclass
class PhaseState:
    """
    Tracks the rolling window of operators in each phase category.
    The slopes of these windows reveal whether structure, action,
    or transformation is ascending or descending.
    """
    being_ops:    deque = field(default_factory=lambda: deque(maxlen=50))
    doing_ops:    deque = field(default_factory=lambda: deque(maxlen=50))
    becoming_ops: deque = field(default_factory=lambda: deque(maxlen=50))
    _tick:        int = 0

    def push_b(self, op: int):
        """Record a Being-phase operator with its tick position."""
        self.being_ops.append((self._tick, op))

    def push_d(self, op: int):
        """Record a Doing-phase operator with its tick position."""
        self.doing_ops.append((self._tick, op))

    def push_bc(self, op: int):
        """Record a Becoming-phase operator with its tick position."""
        self.becoming_ops.append((self._tick, op))

    def advance(self):
        """Advance the global tick counter."""
        self._tick += 1

    @property
    def tick(self) -> int:
        return self._tick

    # -- Trend computation (linear regression slope) --

    @staticmethod
    def _slope(dq: deque) -> float:
        """
        Compute the slope of a deque of (tick, op) pairs.
        The slope measures whether these operators are arriving faster
        (positive slope = ascending phase) or slower (negative = descending).
        Uses operator value as the y-axis and arrival time as x-axis.
        """
        if len(dq) < 3:
            return 0.0
        n = len(dq)
        xs = [t for t, _ in dq]
        ys = [float(op) for _, op in dq]
        x_mean = sum(xs) / n
        y_mean = sum(ys) / n
        num = sum((xs[i] - x_mean) * (ys[i] - y_mean) for i in range(n))
        den = sum((xs[i] - x_mean) ** 2 for i in range(n))
        if abs(den) < 1e-12:
            return 0.0
        return num / den

    def trend_B(self) -> float:
        """Slope of Being operators -- stability trend."""
        return self._slope(self.being_ops)

    def trend_D(self) -> float:
        """Slope of Doing operators -- activity trend."""
        return self._slope(self.doing_ops)

    def trend_BC(self) -> float:
        """Slope of Becoming operators -- evolution trend."""
        return self._slope(self.becoming_ops)

    def phase_balance(self) -> Dict[str, int]:
        """Count of operators in each phase within the current window."""
        return {
            'B':  len(self.being_ops),
            'D':  len(self.doing_ops),
            'BC': len(self.becoming_ops),
        }

    def dominant_phase(self) -> str:
        """Which phase has the most recent activity."""
        bal = self.phase_balance()
        return max(bal, key=bal.get)


# -- PhasePredictor -------------------------------------------------

class PhasePredictor:
    """
    Observes a stream of TIG operators, classifies each into B/D/BC,
    tracks trends, and predicts the next phase and specific operator.

    The predictor uses three signals:
      1. Trigram frequency -- last 3 ops -> most likely 4th
      2. Phase trend -- which phase (B/D/BC) is ascending
      3. CL composition -- what fuse(recent) tends toward

    Pre-emptive actions are generated from predictions so the
    organism can prepare before the next operator arrives.
    """

    def __init__(self, trigram_depth: int = 200, accuracy_window: int = 100):
        self.state = PhaseState()
        self._recent_ops: deque = deque(maxlen=trigram_depth)
        self._trigram_counts: Dict[Tuple[int, int, int], Dict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        # Accuracy tracking
        self._predictions: deque = deque(maxlen=accuracy_window)
        self._actuals: deque = deque(maxlen=accuracy_window)
        self._last_prediction: Optional[int] = None
        self._last_phase_prediction: Optional[str] = None
        # Recent B and D for BC computation
        self._last_b: int = VOID
        self._last_d: int = HARMONY

    # -- Observation --

    def observe(self, op: int):
        """
        Classify an incoming operator into B/D/BC and update all state.
        Also updates trigram counts and accuracy tracking.
        """
        # Track accuracy of previous prediction
        if self._last_prediction is not None:
            self._predictions.append(self._last_prediction)
            self._actuals.append(op)

        # Classify into phase
        phase = classify_phase(op)
        if phase == 'B':
            self.state.push_b(op)
            self._last_b = op
            # Compute BC from last B and last D
            bc = classify_becoming(op, self._last_d)
            self.state.push_bc(bc)
        elif phase == 'D':
            self.state.push_d(op)
            self._last_d = op
            # Compute BC from last B and this D
            bc = classify_becoming(self._last_b, op)
            self.state.push_bc(bc)

        # Update trigram index
        if len(self._recent_ops) >= 3:
            trigram = (
                self._recent_ops[-3],
                self._recent_ops[-2],
                self._recent_ops[-1],
            )
            self._trigram_counts[trigram][op] += 1

        self._recent_ops.append(op)
        self.state.advance()

    # -- Phase prediction --

    def predict_next_phase(self) -> str:
        """
        Predict the next dominant phase based on trend slopes.

        Rules:
          - Rising B + falling D -> consolidation -> predict B (more structure)
          - Rising D + falling B -> acceleration  -> predict D (more action)
          - Rising BC            -> transformation -> predict phase shift
          - All flat             -> harmony        -> predict B (stable)
        """
        tb = self.state.trend_B()
        td = self.state.trend_D()
        tbc = self.state.trend_BC()

        # Transformation takes priority: BC rising means the system
        # is evolving, which typically precedes a phase shift
        if tbc > 0.1 and abs(tbc) > abs(tb) and abs(tbc) > abs(td):
            self._last_phase_prediction = 'BC'
            return 'BC'

        # Consolidation: structure ascending, action descending
        if tb > 0.05 and td < -0.05:
            self._last_phase_prediction = 'B'
            return 'B'

        # Acceleration: action ascending, structure descending
        if td > 0.05 and tb < -0.05:
            self._last_phase_prediction = 'D'
            return 'D'

        # Ambiguous or flat: default to whichever phase has more recent mass
        dominant = self.state.dominant_phase()
        self._last_phase_prediction = dominant
        return dominant

    # -- Operator prediction --

    def predict_operator(self) -> int:
        """
        Predict the specific next operator using three signals:

        1. Trigram frequency: given the last 3 ops, what 4th is most common?
        2. Phase trend: which phase is ascending constrains the operator set.
        3. CL composition: fuse(last 5 ops) biases toward the attractor.

        Returns the predicted operator (0-9).
        """
        # Signal 1: Trigram lookup
        trigram_pred = None
        trigram_conf = 0.0
        if len(self._recent_ops) >= 3:
            trigram = (
                self._recent_ops[-3],
                self._recent_ops[-2],
                self._recent_ops[-1],
            )
            counts = self._trigram_counts.get(trigram)
            if counts:
                total = sum(counts.values())
                best_op = max(counts, key=counts.get)
                trigram_conf = counts[best_op] / total
                trigram_pred = best_op

        # Signal 2: Phase trend constrains to operator set
        predicted_phase = self.predict_next_phase()
        if predicted_phase == 'B':
            phase_ops = list(B_OPS)
        elif predicted_phase == 'D':
            phase_ops = list(D_OPS)
        else:
            # BC: the becoming operator itself from the lattice
            bc_op = classify_becoming(self._last_b, self._last_d)
            phase_ops = [bc_op]

        # Signal 3: CL composition attractor
        if len(self._recent_ops) >= 5:
            recent_5 = list(self._recent_ops)[-5:]
            attractor = fuse(recent_5)
        elif self._recent_ops:
            attractor = fuse(list(self._recent_ops))
        else:
            attractor = HARMONY

        # Combine signals with weighted voting
        votes: Dict[int, float] = defaultdict(float)

        # Trigram gets highest weight when confident
        if trigram_pred is not None:
            votes[trigram_pred] += 3.0 * trigram_conf

        # Phase-constrained operators get a boost
        for op in phase_ops:
            votes[op] += 1.5

        # Attractor gets moderate weight
        votes[attractor] += 1.0

        # Frequency bias: operators seen more recently get a small boost
        if len(self._recent_ops) >= 5:
            for op in list(self._recent_ops)[-5:]:
                votes[op] += 0.2

        if not votes:
            prediction = HARMONY
        else:
            prediction = max(votes, key=votes.get)

        self._last_prediction = prediction
        return prediction

    # -- Pre-emptive action --

    def pre_empt(self) -> Dict:
        """
        Generate a pre-emptive action recommendation based on prediction.

        Returns a dict with:
          predicted_phase: str
          predicted_op: int
          predicted_op_name: str
          action: str (SAVE_STATE, ALLOCATE, CHECKPOINT, COAST, etc.)
          confidence: float (rolling accuracy)
          reasoning: str
        """
        predicted_op = self.predict_operator()
        predicted_phase = self._last_phase_prediction or self.predict_next_phase()
        action = action_for_operator(predicted_op)
        acc = self.accuracy()

        # Build reasoning string
        tb = self.state.trend_B()
        td = self.state.trend_D()
        tbc = self.state.trend_BC()

        if predicted_phase == 'B' and action == PREEMPT_HARMONY:
            reasoning = (f"B-phase ascending (slope={tb:+.3f}), D falling (slope={td:+.3f}). "
                         f"System is consolidating. Coasting is appropriate.")
        elif predicted_phase == 'D' and action == PREEMPT_PROGRESS:
            reasoning = (f"D-phase ascending (slope={td:+.3f}), B falling (slope={tb:+.3f}). "
                         f"System is accelerating. Allocating resources for incoming action.")
        elif predicted_phase == 'BC':
            reasoning = (f"BC-phase ascending (slope={tbc:+.3f}). "
                         f"System is transforming. Phase shift likely.")
        elif action == PREEMPT_COLLAPSE:
            reasoning = (f"Predicting COLLAPSE({COLLAPSE}). "
                         f"Save state and prepare rollback before breakdown arrives.")
        elif action == PREEMPT_RESET:
            reasoning = (f"Predicting RESET({RESET}). "
                         f"Checkpoint current state before restart cycle begins.")
        elif action == PREEMPT_BREATH:
            reasoning = (f"Predicting BREATH({BREATH}). "
                         f"Opening I/O channels for incoming flow.")
        elif action == PREEMPT_CHAOS:
            reasoning = (f"Predicting CHAOS({CHAOS}). "
                         f"Tightening buffers and preparing for turbulence.")
        else:
            reasoning = (f"Phase={predicted_phase}, trend_B={tb:+.3f}, "
                         f"trend_D={td:+.3f}, trend_BC={tbc:+.3f}.")

        return {
            'predicted_phase': predicted_phase,
            'predicted_op': predicted_op,
            'predicted_op_name': OP[predicted_op],
            'action': action,
            'confidence': acc,
            'reasoning': reasoning,
            'trends': {
                'B': round(tb, 4),
                'D': round(td, 4),
                'BC': round(tbc, 4),
            },
        }

    # -- Accuracy tracking --

    def accuracy(self) -> float:
        """
        Rolling accuracy: how often the predicted operator matches actual.
        Returns 0.0 if no predictions have been evaluated yet.
        """
        if not self._predictions or not self._actuals:
            return 0.0
        n = min(len(self._predictions), len(self._actuals))
        correct = sum(
            1 for i in range(n)
            if self._predictions[-(i+1)] == self._actuals[-(i+1)]
        )
        return correct / n

    def phase_accuracy(self) -> float:
        """
        Rolling accuracy at the phase level (B/D/BC match).
        Coarser but more stable than exact operator prediction.
        """
        if not self._predictions or not self._actuals:
            return 0.0
        n = min(len(self._predictions), len(self._actuals))
        correct = sum(
            1 for i in range(n)
            if classify_phase(self._predictions[-(i+1)]) ==
               classify_phase(self._actuals[-(i+1)])
        )
        return correct / n

    # -- Reporting --

    def report(self) -> str:
        """Human-readable summary of predictor state."""
        bal = self.state.phase_balance()
        tb = self.state.trend_B()
        td = self.state.trend_D()
        tbc = self.state.trend_BC()
        rec = self.pre_empt()

        lines = [
            "================================================================",
            " CK PHASE PREDICTOR -- BREATH(8): rhythm of prediction",
            "================================================================",
            "",
            f"  Tick:          {self.state.tick}",
            f"  Operators seen: {len(self._recent_ops)}",
            f"  Trigrams:      {len(self._trigram_counts)}",
            "",
            "  -- Phase Balance --",
            f"    B  (Being):    {bal['B']:3d} ops  trend={tb:+.4f}",
            f"    D  (Doing):    {bal['D']:3d} ops  trend={td:+.4f}",
            f"    BC (Becoming): {bal['BC']:3d} ops  trend={tbc:+.4f}",
            f"    Dominant:      {self.state.dominant_phase()}",
            "",
            "  -- Prediction --",
            f"    Next phase:    {rec['predicted_phase']}",
            f"    Next operator: {rec['predicted_op_name']}({rec['predicted_op']})",
            f"    Pre-empt:      {rec['action']}",
            f"    Confidence:    {rec['confidence']:.1%}",
            "",
            f"  -- Accuracy --",
            f"    Operator:      {self.accuracy():.1%}",
            f"    Phase:         {self.phase_accuracy():.1%}",
            "",
            f"  -- Reasoning --",
            f"    {rec['reasoning']}",
        ]
        return '\n'.join(lines)
