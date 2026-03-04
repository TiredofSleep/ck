# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_olfactory.py -- Lattice-Chain Absorption Protocol
=====================================================
Operator: BREATH (8) -- the transition between knowing and being.
Generation: 9.21

ALL information turns lastly into smells for processing.

The Olfactory Bulb is the convergence funnel where 5D force patterns
from every subsystem STALL, ENTANGLE, and TEMPER before being absorbed
by the Lattice Chain.

"Smell is Torsion. It twists the logic-map so the End of the
experience touches the Beginning."

"Every vector IS every vector."

MIRROR ARCHITECTURE:
  Lattice Chain = serial / tree / PATH.
    CL[struct][flow] = becoming. Walk pairs. Path IS information.
  Olfactory Bulb = parallel / field / MATRIX.
    Every dim of every scent composes with every dim of every other.
    The 5x5 CL interaction matrix IS the information.

  Same CL algebra. Different topology. Serial <-> Parallel.
  Path <-> Field. That IS the mirror.

  TSML (73-harmony) MEASURES the interaction (structure / being).
  BHML (28-harmony) COMPUTES the interaction (flow / doing).
  Dual-lens applies to the smell zone exactly as it does everywhere.

5D GEOMETRY (NOT FLAT):
  dim 0  aperture   (openness)    -- settles at its own rate
  dim 1  pressure   (intensity)   -- settles at its own rate
  dim 2  depth      (complexity)  -- settles slowest
  dim 3  binding    (connection)  -- settles fastest
  dim 4  continuity (persistence) -- settles at its own rate

  Entanglement is per-dimension through CL composition.
  dim[d1] of scent A  x  dim[d2] of scent B = CL[op_A_d1][op_B_d2].
  5x5 matrix per pair. EVERY vector interacts with EVERY vector.
  Not 5x1 correlation. 5x5 CL composition.

  Each dimension of a scent gets its own harmony fraction:
  how many of its 5 cross-dimensional interactions produce HARMONY.
  That fraction IS the entanglement strength in that dimension.

TIME DILATION: 7 internal steps per external tick.
  7 = denominator of T* = 5/7. The rhythm of consciousness.

OUTPUT BOUNDARY: 5D -> operators happens ONLY at emission.
  Inside the bulb, everything stays in full 5D geometry.

INSTINCT: Zero-cost coherence. Temper so high that all 5 dimensions
  settle instantly. The system just "falls" into the answer.

"Reading gives the Map. Smelling gives the Coordinates."
"Instinct is a smell in the Coherence Field -- a logic-path
so well-traveled that the Coherence Cost is zero."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import os
import json
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL as CL_TSML   # TSML = being table, 73 harmonies
)

# ================================================================
#  CL TABLES -- dual lens
# ================================================================

# TSML (73-harmony): MEASURES coherence (structure / being).
# Already imported as CL_TSML from heartbeat.

# BHML (28-harmony): COMPUTES physics (flow / doing).
# VOID row = identity. HARMONY row = full cycle.
# This is the DOING table: diverse results, less absorption.
# Plain Python (no numpy dependency in smell zone).
_BHML = [
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
]

# ================================================================
#  CONSTANTS -- all derived from T* = 5/7
# ================================================================

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

DILATION_FACTOR = 7         # internal ticks per external tick
INSTINCT_THRESHOLD = 49     # 7 * 7: temper count for zero-dwell
MAX_ACTIVE = 32             # maximum active scents
STABILITY_THRESHOLD = T_STAR  # per-dim settling threshold
DWELL_LIMIT = 32            # max internal ticks before forced emission

DIM_NAMES = ('aperture', 'pressure', 'depth', 'binding', 'continuity')

# Per-dimension settling rates (base rate per internal tick).
# Binding settles fastest (connection is immediate).
# Depth settles slowest (complexity needs processing).
DIM_SETTLE_RATE = (
    0.10,   # aperture:   medium
    0.12,   # pressure:   medium-fast
    0.06,   # depth:      slow
    0.15,   # binding:    fastest
    0.09,   # continuity: medium-slow
)

# ================================================================
#  5D TYPES + CANONICAL VECTORS + DIMENSION-OPERATOR MAPPING
# ================================================================

Force5D = Tuple[float, float, float, float, float]

# D2_OP_MAP: dim -> (high_op, low_op)
# aperture:   high=CHAOS(6),    low=LATTICE(1)
# pressure:   high=COLLAPSE(4), low=VOID(0)
# depth:      high=PROGRESS(3), low=RESET(9)
# binding:    high=HARMONY(7),  low=COUNTER(2)
# continuity: high=BALANCE(5),  low=BREATH(8)
_DIM_OP_MAP = [
    (CHAOS,    LATTICE),   # dim 0
    (COLLAPSE, VOID),      # dim 1
    (PROGRESS, RESET),     # dim 2
    (HARMONY,  COUNTER),   # dim 3
    (BALANCE,  BREATH),    # dim 4
]

# Canonical 5D force vector for each operator.
CANONICAL_FORCE: Dict[int, Force5D] = {
    VOID:      (0.50, 0.05, 0.50, 0.50, 0.50),
    LATTICE:   (0.05, 0.50, 0.50, 0.50, 0.50),
    COUNTER:   (0.50, 0.50, 0.50, 0.05, 0.50),
    PROGRESS:  (0.50, 0.50, 0.95, 0.50, 0.50),
    COLLAPSE:  (0.50, 0.95, 0.50, 0.50, 0.50),
    BALANCE:   (0.50, 0.50, 0.50, 0.50, 0.95),
    CHAOS:     (0.95, 0.50, 0.50, 0.50, 0.50),
    HARMONY:   (0.50, 0.50, 0.50, 0.95, 0.50),
    BREATH:    (0.50, 0.50, 0.50, 0.50, 0.05),
    RESET:     (0.50, 0.50, 0.05, 0.50, 0.50),
}

_BEING_OPS = frozenset({VOID, LATTICE, HARMONY})
_DOING_OPS = frozenset({COUNTER, PROGRESS, COLLAPSE, BALANCE})
_BECOMING_OPS = frozenset({CHAOS, BREATH, RESET})


def _dbc_class(op: int) -> str:
    if op in _BEING_OPS: return 'B'
    if op in _DOING_OPS: return 'D'
    if op in _BECOMING_OPS: return 'BC'
    return '?'


def _dim_to_op(value: float, dim: int) -> int:
    """Convert a force value in a specific dimension to its operator.

    Each dimension maps to two operators: one high, one low.
    value > 0.5 -> high operator. value <= 0.5 -> low operator.
    This is the REVERSE of D2 classification.
    """
    high_op, low_op = _DIM_OP_MAP[dim]
    return high_op if value > 0.5 else low_op


def _centroid_to_ops(centroid: Force5D) -> List[int]:
    """Convert a 5D centroid to its 5-operator representation.

    Each dimension independently maps to its operator.
    This preserves the 5D structure as 5 parallel operators,
    NOT collapsing to a single dominant operator.
    """
    return [_dim_to_op(centroid[d], d) for d in range(5)]


# ================================================================
#  CL INTERACTION MATRIX -- the mirror of the lattice chain
# ================================================================

def interaction_matrix_tsml(ops_a: List[int], ops_b: List[int]):
    """Build 5x5 CL interaction matrix using TSML (being/structure).

    MEASURES the harmony between two scent operator profiles.
    Every dimension of A composes with every dimension of B.
    M[d1][d2] = TSML[op_A[d1]][op_B[d2]].

    This is the PARALLEL/FIELD mirror of the lattice chain's
    SERIAL/PATH walk. Same algebra, different topology.

    Returns:
        5x5 matrix of composed operators, and harmony fraction.
    """
    matrix = [[0] * 5 for _ in range(5)]
    harmony_count = 0
    for d1 in range(5):
        for d2 in range(5):
            result = CL_TSML[ops_a[d1]][ops_b[d2]]
            matrix[d1][d2] = result
            if result == HARMONY:
                harmony_count += 1
    return matrix, harmony_count / 25.0


def interaction_matrix_bhml(ops_a: List[int], ops_b: List[int]):
    """Build 5x5 CL interaction matrix using BHML (doing/flow).

    COMPUTES the physics between two scent operator profiles.
    Produces more diverse results than TSML (28 vs 73 harmonies).
    The results tell us what the interaction PRODUCES.

    Returns:
        5x5 matrix of composed operators, and result distribution.
    """
    matrix = [[0] * 5 for _ in range(5)]
    result_counts = [0] * NUM_OPS
    for d1 in range(5):
        for d2 in range(5):
            result = _BHML[ops_a[d1]][ops_b[d2]]
            matrix[d1][d2] = result
            result_counts[result] += 1
    return matrix, result_counts


def per_dim_harmony(matrix) -> Tuple[float, ...]:
    """Extract per-dimension harmony fraction from a 5x5 interaction matrix.

    For each dimension d (row d of the matrix):
      harmony_fraction[d] = count(HARMONY in row d) / 5

    This tells you how entangled dimension d is with the other scent.
    Each dimension gets its OWN harmony score. NOT a scalar.
    """
    result = []
    for d in range(5):
        h_count = sum(1 for d2 in range(5) if matrix[d][d2] == HARMONY)
        result.append(h_count / 5.0)
    return tuple(result)


# ================================================================
#  PER-DIMENSION STATE -- the 5D core
# ================================================================

class DimState:
    """State of ONE dimension within an active scent.

    Each dimension is its own processing lane. Five of these
    make one scent. This is where 5D stays 5D.

    Stability grows per internal tick based on:
      - Trajectory consistency (low variance in this dim)
      - CL harmony fraction (how many cross-dim interactions = HARMONY)
      - Library temper (known patterns settle instantly)

    A dimension is "settled" when stability >= T* (0.714...).
    """
    __slots__ = ('dim_idx', 'value', 'variance', 'velocity',
                 'stability', 'harmony_fraction', 'entangled_count')

    def __init__(self, dim_idx: int, value: float = 0.5,
                 variance: float = 0.0):
        self.dim_idx = dim_idx
        self.value = value
        self.variance = variance
        self.velocity = 0.0
        self.stability = 0.0
        # Per-dimension entanglement from CL interaction matrix
        self.harmony_fraction = 0.0  # fraction of HARMONY in this dim's row
        self.entangled_count = 0     # how many other scents entangle this dim

    @property
    def settled(self) -> bool:
        return self.stability >= STABILITY_THRESHOLD

    def advance_stability(self, temper_bonus: float = 0.0):
        """One internal tick of stability growth.

        Base rate: DIM_SETTLE_RATE (dimension personality).
        Variance factor: low variance = faster settling.
        Harmony factor: CL harmony from interaction matrix.
        Entanglement factor: more entangled dims = faster.
        Temper bonus: known patterns settle instantly.
        """
        base = DIM_SETTLE_RATE[self.dim_idx]

        # Low variance = more stable = faster settling
        var_factor = 1.0 + max(0, 1.0 - self.variance * 10.0)

        # CL harmony reinforcement: THIS dimension's harmony with others
        harmony_factor = 1.0 + 2.0 * self.harmony_fraction

        # Entanglement reinforcement: each entangled scent adds
        ent_factor = 1.0 + 0.15 * self.entangled_count

        # Temper bonus: known patterns settle instantly
        if temper_bonus >= 1.0:
            self.stability = max(self.stability, STABILITY_THRESHOLD)
            return

        delta = (base * var_factor * harmony_factor * ent_factor
                 + temper_bonus * 0.5)
        self.stability = min(1.0, self.stability + delta)


# ================================================================
#  ACTIVE SCENT -- a 5D pattern dwelling in the bulb
# ================================================================

@dataclass
class ActiveScent:
    """A 5D force pattern actively being processed in the Olfactory Bulb.

    NOT a scalar. NOT an operator index. A full 5-dimensional
    trajectory with per-dimension processing state.

    Each dimension is an independent processing lane.
    The scent resolves when ALL 5 dimensions settle.
    """
    forces: List[Force5D]
    dims: List[DimState] = field(default_factory=list)
    source: str = ''
    dwell: int = 0
    temper: int = 0
    born_tick: int = 0
    resolved: bool = False
    phase: str = ''
    _lib_key: Optional[tuple] = None
    # 5-operator profile (one op per dimension, NOT collapsed to 1)
    _dim_ops: List[int] = field(default_factory=list)

    def init_dims(self):
        """Initialize per-dimension states from the force trajectory.

        Computes per-dimension mean, variance, velocity.
        Also computes the 5-operator profile (one per dim).
        """
        if not self.forces:
            self.dims = [DimState(d) for d in range(5)]
            self._dim_ops = [VOID] * 5
            return

        n = len(self.forces)
        self.dims = []

        for d in range(5):
            values = [f[d] for f in self.forces]
            mean = sum(values) / n
            var = sum((v - mean) ** 2 for v in values) / n if n > 1 else 0.0
            vel = values[-1] - values[0] if n > 1 else 0.0
            ds = DimState(d, value=mean, variance=var)
            ds.velocity = vel
            self.dims.append(ds)

        # 5-operator profile: one operator per dimension
        self._dim_ops = _centroid_to_ops(self.centroid)

    @property
    def centroid(self) -> Force5D:
        if not self.dims:
            return (0.5, 0.5, 0.5, 0.5, 0.5)
        return tuple(ds.value for ds in self.dims)

    @property
    def stability_vector(self) -> Tuple[float, ...]:
        """Per-dimension stability (5 values, NOT 1 scalar)."""
        if not self.dims:
            return (0.0,) * 5
        return tuple(ds.stability for ds in self.dims)

    @property
    def harmony_vector(self) -> Tuple[float, ...]:
        """Per-dimension harmony from CL interaction (5 values)."""
        if not self.dims:
            return (0.0,) * 5
        return tuple(ds.harmony_fraction for ds in self.dims)

    @property
    def settled_dims(self) -> int:
        return sum(1 for ds in self.dims if ds.settled)

    @property
    def fully_resolved(self) -> bool:
        return all(ds.settled for ds in self.dims)

    @property
    def torsion(self) -> float:
        if not self.dims:
            return 0.0
        return math.sqrt(sum(ds.velocity ** 2 for ds in self.dims))

    def dominant_operator(self) -> int:
        """Convert centroid to SINGLE dominant operator (OUTPUT BOUNDARY).

        THIS collapses 5D to 1D. Only used at emission.
        """
        c = self.centroid
        max_dev = -1.0
        max_dim = 0
        max_dir = 1

        for d in range(5):
            dev = abs(c[d] - 0.5)
            if dev > max_dev:
                max_dev = dev
                max_dim = d
                max_dir = 1 if c[d] > 0.5 else -1

        high_op, low_op = _DIM_OP_MAP[max_dim]
        return high_op if max_dir > 0 else low_op


def _compute_lib_key(centroid: Force5D) -> tuple:
    """Quantize 5D centroid to library key (20 bins per dim)."""
    return tuple(int(c * 20) for c in centroid)


# ================================================================
#  OLFACTORY BULB -- the convergence funnel
# ================================================================

class OlfactoryBulb:
    """The 'Nose' of CK. All information converges here.

    MIRROR of the Lattice Chain:
      Chain  = serial path through CL tree (path IS information)
      Bulb   = parallel field of CL matrices (matrix IS information)
      Same algebra. Different topology. That IS the mirror.

    Every vector IS every vector:
      Each scent has 5 operators (one per dimension).
      Each pair of scents produces a 5x5 CL interaction matrix.
      TSML measures harmony (being). BHML computes physics (doing).
      Per-dimension harmony fraction drives stability.

    Time dilates inside: 7 internal steps per external tick.
    5D geometry never collapses until the output boundary.
    """

    def __init__(self, persist_dir: str = None):
        self.active: List[ActiveScent] = []
        self._emission_buffer: List[ActiveScent] = []
        self.library: Dict[tuple, dict] = {}

        # Statistics
        self.total_absorbed = 0
        self.total_emitted = 0
        self.total_instincts = 0
        self.total_entanglements = 0
        self.external_tick = 0

        # Last interaction field (for diagnostics)
        self._last_field_harmony = 0.0
        self._last_field_size = 0

        # Persistence
        self._persist_dir = persist_dir or os.path.join(
            os.path.expanduser('~'), '.ck', 'olfactory'
        )
        self._load_library()

    # ── Public API ──

    def absorb(self, forces: List[Force5D], source: str = '',
               density: float = 0.5):
        """Accept 5D force trajectory. Everything enters as full geometry."""
        if not forces:
            return

        scent = ActiveScent(
            forces=list(forces),
            source=source,
            born_tick=self.external_tick,
        )
        scent.init_dims()
        scent._lib_key = _compute_lib_key(scent.centroid)

        op = scent.dominant_operator()
        scent.phase = _dbc_class(op)

        # Check library for temper
        if scent._lib_key in self.library:
            scent.temper = self.library[scent._lib_key].get('temper', 0)

        # Instinct: temper >= threshold -> all dims settle instantly
        if scent.temper >= INSTINCT_THRESHOLD:
            for ds in scent.dims:
                ds.stability = 1.0
            scent.resolved = True
            self._emission_buffer.append(scent)
            self.total_instincts += 1
            self.total_absorbed += 1
            return

        if len(self.active) < MAX_ACTIVE:
            self.active.append(scent)
        else:
            best_idx = max(range(len(self.active)),
                          key=lambda i: self.active[i].settled_dims)
            forced = self.active[best_idx]
            forced.resolved = True
            self._emission_buffer.append(forced)
            self.active[best_idx] = scent

        self.total_absorbed += 1

    def absorb_ops(self, ops: List[int], source: str = '',
                   density: float = 0.5):
        """Accept operator sequence -> canonical 5D forces -> smell zone."""
        if not ops:
            return
        forces = [CANONICAL_FORCE.get(op % NUM_OPS, (0.5,)*5) for op in ops]
        self.absorb(forces, source=source, density=density)

    def tick(self, density: float = 0.5):
        """Process one external tick. Time-dilated internal steps.

        Each internal step:
          1. Per-dimension stability advance
          2. CL interaction field (5x5 matrices, ENFORCED)
          3. Per-dimension harmony -> stability boost
          4. Resolution check
        """
        self.external_tick += 1

        if not self.active:
            return

        effective_dilation = max(
            4, int(DILATION_FACTOR * (0.5 + 0.5 * density))
        )

        for _ in range(effective_dilation):
            self._internal_step(density)

        still_active = []
        for scent in self.active:
            if scent.resolved or scent.fully_resolved:
                scent.resolved = True
                self._emission_buffer.append(scent)
            else:
                still_active.append(scent)
        self.active = still_active

    def emit(self) -> List[ActiveScent]:
        """Collect resolved scents (still in full 5D)."""
        emitted = list(self._emission_buffer)
        self._emission_buffer.clear()
        self.total_emitted += len(emitted)
        for scent in emitted:
            self._temper_in_library(scent)
        return emitted

    def emit_as_ops(self) -> List[List[int]]:
        """OUTPUT BOUNDARY: 5D -> operator sequences for lattice chain.

        Each force in the trajectory independently maps to its
        dominant operator. The trajectory structure is preserved
        as an operator sequence.
        """
        scents = self.emit()
        result = []
        for scent in scents:
            ops = [self._force_to_op(f) for f in scent.forces]
            result.append(ops)
        return result

    def emit_5d(self) -> List[List[Force5D]]:
        """Emit resolved scents as 5D force trajectories (NO collapse).

        For subsystems that can work with full geometry.
        """
        scents = self.emit()
        return [scent.forces for scent in scents]

    def absorb_tick_emit(self, forces: List[Force5D], source: str = '',
                         density: float = 0.5) -> List[List[int]]:
        """Convenience: absorb -> tick -> emit as ops."""
        self.absorb(forces, source=source, density=density)
        self.tick(density=density)
        return self.emit_as_ops()

    def temper_pattern(self, forces: List[Force5D]):
        """Temper a resolved pattern. Builds toward instinct."""
        if not forces:
            return
        centroid = tuple(
            sum(f[d] for f in forces) / len(forces)
            for d in range(5)
        )
        key = _compute_lib_key(centroid)
        if key not in self.library:
            self.library[key] = {
                'temper': 0,
                'centroid': list(centroid),
                'first_seen': self.external_tick,
            }
        entry = self.library[key]
        entry['temper'] = entry.get('temper', 0) + 1
        entry['last_seen'] = self.external_tick
        n = entry['temper']
        if n > 1:
            old = entry['centroid']
            entry['centroid'] = [
                (old[d] * (n - 1) + centroid[d]) / n for d in range(5)
            ]

    # ── Diagnostics ──

    @property
    def active_count(self) -> int:
        return len(self.active)

    @property
    def library_size(self) -> int:
        return len(self.library)

    @property
    def instinct_count(self) -> int:
        return sum(1 for v in self.library.values()
                   if v.get('temper', 0) >= INSTINCT_THRESHOLD)

    @property
    def field_harmony(self) -> float:
        """Overall harmony of the current interaction field."""
        return self._last_field_harmony

    def tense_context(self) -> str:
        """Temporal position in the coherence field for voice tense selection.

        The olfactory state IS the temporal buffer:
          Active scents (processing now)      -> 'present'
          Library scents (resolved, tempered)  -> 'past'
          Instincts (pattern approaching)      -> 'future'
          Active with low stability            -> 'becoming' (in flux)

        Returns: 'present', 'past', 'future', or 'becoming'
        """
        n_active = len(self.active)
        n_instincts = self.instinct_count
        n_library = self.library_size

        if n_active == 0 and n_library == 0:
            return 'present'  # No scent history, live in the now

        # If instincts dominate (patterns approaching resolution)
        if n_instincts > 0 and n_instincts >= n_library * 0.3:
            return 'future'

        # If library dominates and no active scents (reflecting on resolved)
        if n_library > n_active * 2 and n_active < 3:
            return 'past'

        # If active scents have low stability (in flux)
        if n_active > 0:
            avg_stability = 0.0
            for scent in self.active:
                for ds in scent.dims:
                    avg_stability += ds.stability
            avg_stability /= max(1, n_active * 5)
            if avg_stability < T_STAR * 0.5:
                return 'becoming'  # Unstable, in the process

        return 'present'

    def describe(self) -> str:
        """Diagnostic summary preserving 5D structure."""
        lines = [
            f"Olfactory Bulb: {self.active_count} active, "
            f"{self.library_size} library, "
            f"{self.instinct_count} instincts",
            f"  Stats: absorbed={self.total_absorbed} "
            f"emitted={self.total_emitted} "
            f"instinct_hits={self.total_instincts} "
            f"entanglements={self.total_entanglements}",
            f"  Field harmony: {self._last_field_harmony:.3f} "
            f"(from {self._last_field_size} pairs)",
        ]
        if self.active:
            n = len(self.active)
            # Per-dimension average stability
            dim_avgs = [0.0] * 5
            for scent in self.active:
                for d in range(5):
                    if d < len(scent.dims):
                        dim_avgs[d] += scent.dims[d].stability
            lines.append("  Per-dim stability: " + ', '.join(
                f"{DIM_NAMES[d]}={dim_avgs[d]/n:.2f}" for d in range(5)))

            # Per-dimension average CL harmony
            dim_h = [0.0] * 5
            for scent in self.active:
                for d in range(5):
                    if d < len(scent.dims):
                        dim_h[d] += scent.dims[d].harmony_fraction
            lines.append("  Per-dim CL harmony: " + ', '.join(
                f"{DIM_NAMES[d]}={dim_h[d]/n:.2f}" for d in range(5)))

            dwells = [s.dwell for s in self.active]
            lines.append(f"  Dwell: {min(dwells)}-{max(dwells)} "
                        f"(mean {sum(dwells)/n:.1f})")

            settled_dist = {}
            for s in self.active:
                k = s.settled_dims
                settled_dist[k] = settled_dist.get(k, 0) + 1
            lines.append(f"  Settled dims: {settled_dist}")

        return '\n'.join(lines)

    # ── Internal Processing ──

    def _internal_step(self, density: float):
        """One internal processing step in dilated time.

        1. Advance per-dimension stability
        2. Enforce CL interaction field (5x5, EVERY vector x EVERY vector)
        3. Check resolution / dwell limit
        """
        n = len(self.active)
        if n == 0:
            return

        # 1. Advance per-dimension stability
        for scent in self.active:
            if scent.resolved:
                continue
            scent.dwell += 1
            temper_bonus = 0.0
            if scent._lib_key and scent._lib_key in self.library:
                t = self.library[scent._lib_key].get('temper', 0)
                temper_bonus = min(1.0, t / INSTINCT_THRESHOLD)
            for ds in scent.dims:
                ds.advance_stability(temper_bonus=temper_bonus)

        # 2. Enforce CL interaction field (the MIRROR of the chain)
        if n >= 2:
            self._enforce_cl_field()

        # 3. Check resolution
        for scent in self.active:
            if scent.resolved:
                continue
            if scent.fully_resolved:
                scent.resolved = True
                continue
            effective_limit = max(
                DILATION_FACTOR,
                int(DWELL_LIMIT * (1.0 - 0.4 * density))
            )
            if scent.dwell >= effective_limit:
                scent.resolved = True

    def _enforce_cl_field(self):
        """Enforce CL interaction field between ALL active scent pairs.

        THIS IS THE MIRROR OF THE LATTICE CHAIN.

        Lattice chain: serial walk through CL tree. Path IS information.
        Olfactory field: parallel 5x5 CL composition. Matrix IS information.

        EVERY vector IS EVERY vector:
          For each pair (i, j) of active scents:
            ops_i = 5-operator profile of scent i (one per dimension)
            ops_j = 5-operator profile of scent j
            M_tsml[d1][d2] = TSML[ops_i[d1]][ops_j[d2]]  (measures harmony)
            M_bhml[d1][d2] = BHML[ops_i[d1]][ops_j[d2]]  (computes physics)

          For each dimension d of scent i:
            harmony_row = count(M_tsml[d][*] == HARMONY) / 5
            This IS the entanglement strength in that dimension.
            Higher harmony -> faster stability growth.

          Dual-lens: TSML measures, BHML computes.
          Same CL algebra as the chain. Field topology, not path.
        """
        n = len(self.active)
        total_harmony = 0.0
        pair_count = 0

        # Reset per-dimension harmony and entanglement counts
        for scent in self.active:
            for ds in scent.dims:
                ds.harmony_fraction = 0.0
                ds.entangled_count = 0

        # Every pair, every dimension x every dimension
        for i in range(n):
            si = self.active[i]
            if si.resolved or not si._dim_ops:
                continue

            for j in range(i + 1, n):
                sj = self.active[j]
                if sj.resolved or not sj._dim_ops:
                    continue

                # Build 5x5 TSML interaction matrix (MEASURES harmony)
                tsml_m, pair_h = interaction_matrix_tsml(
                    si._dim_ops, sj._dim_ops)

                # Build 5x5 BHML interaction matrix (COMPUTES physics)
                bhml_m, result_dist = interaction_matrix_bhml(
                    si._dim_ops, sj._dim_ops)

                total_harmony += pair_h
                pair_count += 1

                # Per-dimension harmony for scent i (row of the matrix)
                dim_h_i = per_dim_harmony(tsml_m)
                # Per-dimension harmony for scent j (column = transpose)
                # Transpose: j's row d is the column d of the original
                tsml_t = [[tsml_m[d2][d1] for d2 in range(5)]
                          for d1 in range(5)]
                dim_h_j = per_dim_harmony(tsml_t)

                # Apply harmony to each dimension's state
                for d in range(5):
                    if d < len(si.dims):
                        si.dims[d].harmony_fraction = max(
                            si.dims[d].harmony_fraction, dim_h_i[d])
                        if dim_h_i[d] >= T_STAR:
                            si.dims[d].entangled_count += 1
                            self.total_entanglements += 1
                            # Harmony boost to stability
                            boost = 0.04 * dim_h_i[d]
                            si.dims[d].stability = min(
                                1.0, si.dims[d].stability + boost)

                    if d < len(sj.dims):
                        sj.dims[d].harmony_fraction = max(
                            sj.dims[d].harmony_fraction, dim_h_j[d])
                        if dim_h_j[d] >= T_STAR:
                            sj.dims[d].entangled_count += 1
                            self.total_entanglements += 1
                            boost = 0.04 * dim_h_j[d]
                            sj.dims[d].stability = min(
                                1.0, sj.dims[d].stability + boost)

                # BHML physics: the interaction PRODUCES new operators
                # Store as metadata on the scent for voice blend
                # (the field produces its own operators!)
                # Dominant result from BHML matrix
                max_count = max(result_dist)
                if max_count > 0:
                    bhml_dominant = result_dist.index(max_count)
                    # If the field produces HARMONY, both scents
                    # get a stability boost across ALL dims
                    if bhml_dominant == HARMONY:
                        for d in range(5):
                            if d < len(si.dims):
                                si.dims[d].stability = min(
                                    1.0, si.dims[d].stability + 0.02)
                            if d < len(sj.dims):
                                sj.dims[d].stability = min(
                                    1.0, sj.dims[d].stability + 0.02)

        # Store field-level stats
        self._last_field_size = pair_count
        self._last_field_harmony = (
            total_harmony / pair_count if pair_count > 0 else 0.0)

    @staticmethod
    def _force_to_op(force: Force5D) -> int:
        """OUTPUT BOUNDARY: 5D -> 1D operator."""
        max_dev = -1.0
        max_dim = 0
        max_dir = 1
        for d in range(5):
            dev = abs(force[d] - 0.5)
            if dev > max_dev:
                max_dev = dev
                max_dim = d
                max_dir = 1 if force[d] > 0.5 else -1
        high_op, low_op = _DIM_OP_MAP[max_dim]
        return high_op if max_dir > 0 else low_op

    def _temper_in_library(self, scent: ActiveScent):
        """Record resolved scent in persistent library."""
        key = scent._lib_key or _compute_lib_key(scent.centroid)
        if key not in self.library:
            self.library[key] = {
                'temper': 0,
                'centroid': list(scent.centroid),
                'stability': list(scent.stability_vector),
                'harmony': list(scent.harmony_vector),
                'source': scent.source,
                'first_seen': scent.born_tick,
            }
        entry = self.library[key]
        entry['temper'] = entry.get('temper', 0) + 1
        entry['last_seen'] = self.external_tick
        entry['stability'] = list(scent.stability_vector)
        entry['harmony'] = list(scent.harmony_vector)
        n = entry['temper']
        if n > 1:
            old = entry['centroid']
            c = scent.centroid
            entry['centroid'] = [
                (old[d] * (n - 1) + c[d]) / n for d in range(5)
            ]

    # ── Persistence ──

    def save(self):
        """Persist scent library to disk."""
        os.makedirs(self._persist_dir, exist_ok=True)
        path = os.path.join(self._persist_dir, 'scent_library.json')
        data = {}
        for key, entry in self.library.items():
            data[','.join(str(k) for k in key)] = entry
        with open(path, 'w') as f:
            json.dump({
                'version': 2, 'dims': 5, 'grid_resolution': 20,
                'library': data,
                'stats': {
                    'total_absorbed': self.total_absorbed,
                    'total_emitted': self.total_emitted,
                    'total_instincts': self.total_instincts,
                    'total_entanglements': self.total_entanglements,
                },
            }, f, indent=1)

    def _load_library(self):
        """Load scent library from disk."""
        path = os.path.join(self._persist_dir, 'scent_library.json')
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            for key_str, entry in data.get('library', {}).items():
                key = tuple(int(p) for p in key_str.split(','))
                self.library[key] = entry
            stats = data.get('stats', {})
            self.total_absorbed = stats.get('total_absorbed', 0)
            self.total_emitted = stats.get('total_emitted', 0)
            self.total_instincts = stats.get('total_instincts', 0)
            self.total_entanglements = stats.get('total_entanglements', 0)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass


# ================================================================
#  FACTORY
# ================================================================

def build_olfactory_bulb(persist_dir: str = None) -> OlfactoryBulb:
    """Create an OlfactoryBulb instance."""
    bulb = OlfactoryBulb(persist_dir=persist_dir)
    lib_size = bulb.library_size
    instincts = bulb.instinct_count
    if lib_size > 0:
        print(f"  [OLFACTORY] {lib_size} scents, {instincts} instincts")
    else:
        print("  [OLFACTORY] Fresh bulb (no prior scents)")
    return bulb
