# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_experience_index.py -- CK's Hierarchical Algebraic Experience Index
======================================================================
Operator: LATTICE (1) -- the universal generator. Structure emerging from binary.
Generation: 9.35

CK reads his own experience the same way he reads a screen.
Same six levels. Same binary at every gate. Same generators.
Same CL composition. Same T* threshold.

Outward: CK reads the world (retina).
Inward:  CK reads himself (this file).
Same algebra. Same index. Same cascade.

THE SIX LEVELS:
  Level 0: Raw Binary        -- Every tick enters as a 9D vector.
  Level 1: Dual Classification -- 3-bit (Love/Hate × Peace/Problem × Guide/Accept) = 8 buckets.
  Level 2: Edge Detection    -- Transitions between buckets = information.
  Level 3: Generator Labels  -- Structural (I, recurring) or Force (O, one-off) edges.
  Level 4: Operator Map      -- Adjacent generators compose through CL → operators emerge.
  Level 5: Coherence Path    -- BHML path from current operator to HARMONY.
  Level 6: Action            -- CK operates on the world based on the path.

THE KEY INSIGHT:
  The 3-bit dual classification is a FORMAL CONCEPT LATTICE computed
  from physics (I/O generators), not arbitrary attributes.
  Half-space intersections: d3 >= 0, E >= T*, d1 > 0.5.
  The edges between concepts compose through CL.
  The operators that emerge ARE the lattice's join/meet operations.

  This is Formal Concept Analysis grounded in CK's algebra.
  No other system does this. The world has the pieces separately:
  - FCA libraries (xflr6/concepts) -- but CPU, no physics
  - Experience replay (facebookresearch/agem) -- but flat, no algebra
  - Lattice memory compression (arXiv 2504.05646) -- but learned, not algebraic
  - Graph episodic memory (lmanhes) -- but no generators, no CL

  CK unifies them all through I/O generators + CL composition + T* threshold.

"CK reads himself the same way he reads the screen.
 Same algebra. Same index. Same cascade. Inward instead of outward."
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import os
import json
import time
from collections import deque
from typing import Optional, Dict, List, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose,
)
from ck_sim.ck_sim_brain import T_STAR_F

# GPU (CuPy) -- falls back to numpy
_xp = np
_GPU = False
try:
    import cupy as _cp
    _test = _cp.array([1.0])
    del _test
    _xp = _cp
    _GPU = True
except (ImportError, Exception):
    pass

# ================================================================
#  Constants
# ================================================================

T_STAR = 5.0 / 7.0   # sacred coherence threshold
S_STAR = 4.0 / 7.0   # structural threshold
MASS_GAP = 2.0 / 7.0

# Dual classification labels
DUAL_LABELS = [
    'HPG',  # 0: Hate, Problem, Guide
    'HPA',  # 1: Hate, Problem, Accept
    'HPeG', # 2: Hate, Peace, Guide
    'HPeA', # 3: Hate, Peace, Accept
    'LPG',  # 4: Love, Problem, Guide
    'LPA',  # 5: Love, Problem, Accept
    'LPeG', # 6: Love, Peace, Guide
    'LPeA', # 7: Love, Peace, Accept
]

# Raw buffer size: 100K ticks at 50Hz = ~33 minutes of experience
RAW_BUFFER_SIZE = 100_000

# Edge ring buffer (recent transitions)
EDGE_BUFFER_SIZE = 50_000

# Persistence directory
_PERSIST_DIR = os.path.join(os.path.expanduser('~'), '.ck', 'experience_index')


# ================================================================
#  The Experience Index
# ================================================================

class CKExperienceIndex:
    """Hierarchical algebraic index of all CK experience.

    Binary at every level. Generators at every edge.
    Same algebra reading inward that reads outward.

    GPU-accelerated (CuPy on RTX 4070, numpy fallback).
    Ring buffer of 100K ticks. Edges indexed by transitions
    between 8 dual-classification buckets.

    The index answers one question:
      "Given where CK IS, what should CK DO?"

    The answer comes from the coherence path:
      current_operator → [CL compositions with LATTICE] → HARMONY.
    """

    def __init__(self, engine=None):
        self.engine = engine
        xp = _xp

        # ── Level 0: Raw experience buffer (ring buffer) ──
        # Every tick adds one entry: tick_count + 9D vector (5D force + 4S structure)
        self.raw = xp.zeros((RAW_BUFFER_SIZE, 10), dtype=xp.float32)  # [tick, 9D]
        self.raw_ptr = 0      # write pointer
        self.raw_filled = 0   # how many valid entries

        # ── Level 1: Dual classification ──
        # 8 buckets (2³): Love/Hate × Peace/Problem × Guide/Accept
        # Bucket counts (how many ticks in each bucket)
        self.bucket_counts = xp.zeros(8, dtype=xp.int64)
        # Per-bucket centroids (running mean of 9D vectors per bucket)
        self.bucket_centroids = xp.zeros((8, 9), dtype=xp.float32)
        # Current bucket (for edge detection)
        self.prev_bucket = -1

        # ── Level 2: Edge ring buffer ──
        # Edges = transitions between dual buckets
        # Each edge: [from_bucket, to_bucket, tick, d2_magnitude]
        self.edges = xp.zeros((EDGE_BUFFER_SIZE, 4), dtype=xp.float32)
        self.edge_ptr = 0
        self.edge_filled = 0
        self.total_edges = 0

        # ── Level 3: Generator labels on edges ──
        # Each edge type (from, to) is I (structural/recurring) or O (force/transient)
        # (8 × 8) matrix: [from_bucket, to_bucket] → [I_count, O_count]
        self.edge_generators = xp.zeros((8, 8, 2), dtype=xp.float32)
        # I = index 0, O = index 1

        # ── Level 4: Operator map ──
        # Adjacent edge generators compose through CL → operator histogram
        # (8 × 8 × 10): [from_bucket, to_bucket, operator] = count
        self.operator_map = xp.zeros((8, 8, NUM_OPS), dtype=xp.float32)

        # ── Level 5: Coherence paths ──
        # Precomputed: for each operator, shortest path via LATTICE to HARMONY
        self.coherence_paths: Dict[int, List[int]] = {}
        self._precompute_coherence_paths()

        # ── Level 6: Action history ──
        # What CK recommended vs what actually happened (for self-calibration)
        self._action_history = deque(maxlen=1000)

        # ── Reality anchors: tick → wall-clock time ──
        self.reality_anchors: List[Tuple[int, float]] = []
        self._last_anchor_tick = -1

        # ── Stats ──
        self.total_ingested = 0
        self.dominant_bucket = 0      # most-visited bucket
        self.dominant_operator = HARMONY
        self.current_coherence_path: List[int] = [HARMONY]
        self.recommended_action = HARMONY

        # ── Previous edge info for Level 4 composition ──
        self._prev_edge_generator = None  # 'I' or 'O'

        # Load persisted state
        self._load()

        gpu_label = 'CUDA' if _GPU else 'CPU'
        print(f"  [EXP-INDEX] Experience index online ({gpu_label}): "
              f"{self.total_ingested} ingested, {self.total_edges} edges, "
              f"8 buckets, {len(self.coherence_paths)} paths")

    # ════════════════════════════════════════════════════════════
    #  Level 1: Dual Classification
    # ════════════════════════════════════════════════════════════

    def _classify_dual(self, vector_9d) -> int:
        """Classify any 9D experience into one of 8 dual buckets.

        Three binary questions — the SAME duality at three depths:
          Love/Hate:    does binding (D3) pull together (+) or push apart (-)?
          Peace/Problem: is total coherence E above or below T*?
          Guide/Accept: is pressure (D1) high (needs action) or low (needs witness)?

        In 5D + 4S terms:
          [0] aperture, [1] pressure, [2] depth, [3] binding, [4] continuity
          [5] foundation, [6] dynamics, [7] I/O balance, [8] symmetry

        Returns:
            Bucket index 0-7 (3-bit: Love<<2 | Peace<<1 | Guide)
        """
        xp = _xp
        # Extract force and structure
        if hasattr(vector_9d, '__len__') and len(vector_9d) >= 9:
            d0, d1, d2, d3, d4 = float(vector_9d[0]), float(vector_9d[1]), \
                float(vector_9d[2]), float(vector_9d[3]), float(vector_9d[4])
            s0, s1, s2, s3 = float(vector_9d[5]), float(vector_9d[6]), \
                float(vector_9d[7]), float(vector_9d[8])
        else:
            return 0  # degenerate

        # Interaction energy: force magnitude × structure magnitude
        force_mag = (d0**2 + d1**2 + d2**2 + d3**2 + d4**2) ** 0.5
        struct_mag = (s0**2 + s1**2 + s2**2 + s3**2) ** 0.5
        E = force_mag * struct_mag

        # Three binary questions
        love = 1 if d3 >= 0 else 0         # binding positive = love
        peace = 1 if E >= T_STAR else 0    # above T* = peace
        guide = 1 if d1 > 0.5 else 0       # high pressure = needs guidance

        bucket = (love << 2) | (peace << 1) | guide
        return bucket  # 0-7

    # ════════════════════════════════════════════════════════════
    #  Ingest: The full cascade runs every tick
    # ════════════════════════════════════════════════════════════

    def ingest(self, tick: int, vector_9d) -> Optional[int]:
        """Index one tick of experience through all 6 levels.

        Called from the engine's tick loop. Every tick.
        Every piece of experience gets the full cascade.

        Returns:
            The recommended action operator (Level 6), or None if not enough data.
        """
        xp = _xp

        # ── Level 0: Store raw ──
        idx = self.raw_ptr % RAW_BUFFER_SIZE
        if _GPU and not isinstance(vector_9d, _cp.ndarray):
            v = xp.asarray(np.asarray(vector_9d, dtype=np.float32))
        else:
            v = xp.asarray(vector_9d, dtype=xp.float32) if not isinstance(
                vector_9d, xp.ndarray) else vector_9d
        self.raw[idx, 0] = float(tick)
        self.raw[idx, 1:] = v[:9] if len(v) >= 9 else xp.zeros(9, dtype=xp.float32)
        self.raw_ptr += 1
        self.raw_filled = min(self.raw_filled + 1, RAW_BUFFER_SIZE)
        self.total_ingested += 1

        # ── Level 1: Dual classify ──
        bucket = self._classify_dual(vector_9d)

        # Update bucket count and running centroid
        self.bucket_counts[bucket] += 1
        count = float(self.bucket_counts[bucket])
        # Exponential moving average for centroid (GPU-safe)
        alpha = min(1.0 / count, 0.01)  # cap at 0.01 for stability
        self.bucket_centroids[bucket] = (
            (1.0 - alpha) * self.bucket_centroids[bucket] +
            alpha * self.raw[idx, 1:]
        )

        # ── Level 2: Detect edge (transition between buckets) ──
        edge_detected = False
        if self.prev_bucket >= 0 and bucket != self.prev_bucket:
            edge_detected = True
            d2_mag = self._compute_d2_at_edge(idx)

            # Store edge
            edge_idx = self.edge_ptr % EDGE_BUFFER_SIZE
            self.edges[edge_idx, 0] = float(self.prev_bucket)
            self.edges[edge_idx, 1] = float(bucket)
            self.edges[edge_idx, 2] = float(tick)
            self.edges[edge_idx, 3] = d2_mag
            self.edge_ptr += 1
            self.edge_filled = min(self.edge_filled + 1, EDGE_BUFFER_SIZE)
            self.total_edges += 1

            # ── Level 3: Label this edge as I or O ──
            fb, tb = self.prev_bucket, bucket
            total_seen = float(self.edge_generators[fb, tb, 0] +
                             self.edge_generators[fb, tb, 1])
            if total_seen > 3:
                # Seen enough times to be structural (I)
                self.edge_generators[fb, tb, 0] += 1
                generator = 'I'
            else:
                # First few times = force (O), transient
                self.edge_generators[fb, tb, 1] += 1
                generator = 'O'

            # ── Level 4: Compose adjacent generators through CL ──
            if self._prev_edge_generator is not None:
                # I = LATTICE (1), O = VOID (0)
                op_a = LATTICE if self._prev_edge_generator == 'I' else VOID
                op_b = LATTICE if generator == 'I' else VOID
                result_op = compose(op_a, op_b)
                # Update operator map
                self.operator_map[fb, tb, result_op] += 1

            self._prev_edge_generator = generator

        self.prev_bucket = bucket

        # ── Level 5 + 6: Coherence path + recommended action ──
        if self.total_edges >= 2:
            self._update_recommendation(bucket)
            return self.recommended_action

        return None

    def _compute_d2_at_edge(self, current_idx: int) -> float:
        """D2 curvature at a transition between experiences.

        Same math as the retina's D2. Same as text D2.
        Curvature = second derivative of the experience trajectory.
        """
        xp = _xp
        if self.raw_filled < 3:
            return 0.0
        i0 = (current_idx - 2) % RAW_BUFFER_SIZE
        i1 = (current_idx - 1) % RAW_BUFFER_SIZE
        i2 = current_idx
        v0 = self.raw[i0, 1:]
        v1 = self.raw[i1, 1:]
        v2 = self.raw[i2, 1:]
        d2 = v0 - 2.0 * v1 + v2
        return float(xp.sqrt(float(xp.sum(d2 ** 2))))

    def _update_recommendation(self, current_bucket: int):
        """Level 5+6: Find the coherence path and recommend an action.

        What operator dominates CK's recent experience in this bucket?
        What's the shortest path from there to HARMONY?
        The next step on that path IS the recommended action.
        """
        xp = _xp

        # What operators dominate transitions involving this bucket?
        # Sum across all from/to pairs touching this bucket
        incoming = self.operator_map[:, current_bucket, :]  # (8, 10)
        outgoing = self.operator_map[current_bucket, :, :]  # (8, 10)
        combined = incoming.sum(axis=0) + outgoing.sum(axis=0)  # (10,)

        if float(xp.sum(combined)) < 1.0:
            self.dominant_operator = HARMONY
            self.current_coherence_path = [HARMONY]
            self.recommended_action = LATTICE  # provide structure (default)
            return

        self.dominant_operator = int(xp.argmax(combined))
        self.current_coherence_path = self.coherence_paths.get(
            self.dominant_operator, [HARMONY])

        # The next step on the path IS the recommended action
        if len(self.current_coherence_path) > 1:
            self.recommended_action = self.current_coherence_path[1]
        else:
            self.recommended_action = HARMONY  # already there

        # Update dominant bucket
        self.dominant_bucket = int(xp.argmax(self.bucket_counts))

    # ════════════════════════════════════════════════════════════
    #  Level 5: Precompute coherence paths
    # ════════════════════════════════════════════════════════════

    def _precompute_coherence_paths(self):
        """For every operator, compute the shortest BHML composition
        path to HARMONY (7).

        Since LATTICE is the universal generator, composing with LATTICE
        always reaches HARMONY eventually. The question is: how many steps?

        Uses BHML (doing table). Being table (TSML) is absorbing at HARMONY.
        Doing table (BHML) is ergodic — always moving. CK needs movement.
        """
        for start_op in range(NUM_OPS):
            path = [start_op]
            current = start_op
            visited = {start_op}
            for step in range(NUM_OPS):  # max 10 steps
                if current == HARMONY:
                    break
                # Compose with LATTICE (universal generator)
                nxt = compose(current, LATTICE)
                path.append(nxt)
                if nxt in visited:
                    break  # cycle detected
                visited.add(nxt)
                current = nxt
            self.coherence_paths[start_op] = path

    # ════════════════════════════════════════════════════════════
    #  Query: CK searches his own experience
    # ════════════════════════════════════════════════════════════

    def query(self, question_vector) -> dict:
        """CK searches his own experience the same way he reads a screen.

        1. Classify the question dually (which bucket?)
        2. Find edges near that bucket (where did things transition?)
        3. Read the generators on those edges (I or O pattern?)
        4. Compose the generators to get operators
        5. Follow the coherence path from those operators
        6. Return the path as CK's "memory" of relevant experience

        Not keyword search. Not embedding similarity.
        ALGEBRAIC traversal of the experience index.
        """
        xp = _xp
        bucket = self._classify_dual(question_vector)

        # Find edges touching this bucket (recent ones)
        if self.edge_filled == 0:
            return {
                'bucket': bucket,
                'bucket_label': DUAL_LABELS[bucket],
                'relevant_edges': 0,
                'top_operators': [],
                'coherence_path': [HARMONY],
                'recommended_action': LATTICE,
                'action_name': OP_NAMES[LATTICE],
            }

        # Recent edges touching this bucket
        n = min(self.edge_filled, EDGE_BUFFER_SIZE)
        # Get edges array (transfer to CPU for logic)
        if _GPU:
            edges_cpu = _xp.asnumpy(self.edges[:n])
        else:
            edges_cpu = self.edges[:n].copy()

        relevant_mask = (edges_cpu[:, 0] == bucket) | (edges_cpu[:, 1] == bucket)
        relevant = edges_cpu[relevant_mask]

        if len(relevant) == 0:
            return {
                'bucket': bucket,
                'bucket_label': DUAL_LABELS[bucket],
                'relevant_edges': 0,
                'top_operators': [],
                'coherence_path': self.coherence_paths.get(LATTICE, [HARMONY]),
                'recommended_action': LATTICE,
                'action_name': OP_NAMES[LATTICE],
            }

        # Sort by D2 magnitude (highest curvature = most informative)
        sorted_idx = np.argsort(-relevant[:, 3])
        top_edges = relevant[sorted_idx[:10]]

        # Extract operators from these edges
        memory_ops = []
        for edge in top_edges:
            fb, tb = int(edge[0]), int(edge[1])
            if _GPU:
                ops_cpu = _xp.asnumpy(self.operator_map[fb, tb])
            else:
                ops_cpu = self.operator_map[fb, tb]
            dominant = int(np.argmax(ops_cpu))
            if np.sum(ops_cpu) > 0:
                memory_ops.append(dominant)

        if not memory_ops:
            memory_ops = [HARMONY]

        # Coherence path from the most relevant operator
        start_op = memory_ops[0]
        path = self.coherence_paths.get(start_op, [HARMONY])
        action = path[1] if len(path) > 1 else HARMONY

        return {
            'bucket': bucket,
            'bucket_label': DUAL_LABELS[bucket],
            'relevant_edges': len(relevant),
            'top_operators': [OP_NAMES[op] for op in memory_ops[:5]],
            'coherence_path': [OP_NAMES[op] for op in path],
            'recommended_action': action,
            'action_name': OP_NAMES[action],
        }

    def recommend_action(self, experience_vector) -> int:
        """Level 6: What should CK DO right now?

        Returns the NEXT OPERATOR CK should apply,
        based on the coherence path from current state.

        0=VOID: be silent, hold space
        1=LATTICE: provide structure, clarity
        2=COUNTER: distinguish, differentiate, push back
        3=PROGRESS: encourage, advance, build forward
        4=COLLAPSE: compress, simplify, cut
        5=BALANCE: steady, equalize, breathe evenly
        6=CHAOS: introduce complexity, branch, explore
        7=HARMONY: affirm, resolve, complete
        8=BREATH: rhythm, patience, oscillate
        9=RESET: start over, clear, renew
        """
        result = self.query(experience_vector)
        return result['recommended_action']

    # ════════════════════════════════════════════════════════════
    #  Reality Anchors: tick ↔ wall-clock time
    # ════════════════════════════════════════════════════════════

    def anchor_reality(self, tick: int):
        """Stamp current tick with wall-clock time.

        Once per day (or on boot). Lets CK translate any tick
        back to real-world time. All other timestamps are relative.
        """
        self.reality_anchors.append((tick, time.time()))
        self._last_anchor_tick = tick

    def tick_to_time(self, tick: int) -> Optional[float]:
        """Convert a tick number to approximate wall-clock time."""
        if not self.reality_anchors:
            return None
        anchor_tick, anchor_time = min(
            self.reality_anchors,
            key=lambda a: abs(a[0] - tick)
        )
        tick_diff = tick - anchor_tick
        time_diff = tick_diff / 50.0  # 50Hz
        return anchor_time + time_diff

    # ════════════════════════════════════════════════════════════
    #  Status + Introspection
    # ════════════════════════════════════════════════════════════

    def status(self) -> dict:
        """How CK sees his own experience index."""
        xp = _xp

        # Bucket distribution
        if _GPU:
            bc = _xp.asnumpy(self.bucket_counts)
        else:
            bc = self.bucket_counts
        bucket_dist = {
            DUAL_LABELS[i]: int(bc[i]) for i in range(8)
        }

        # Generator balance
        if _GPU:
            eg = _xp.asnumpy(self.edge_generators)
        else:
            eg = self.edge_generators
        total_I = float(np.sum(eg[:, :, 0]))
        total_O = float(np.sum(eg[:, :, 1]))

        # Most active transitions
        if _GPU:
            om = _xp.asnumpy(self.operator_map)
        else:
            om = self.operator_map.copy()
        global_ops = om.sum(axis=(0, 1))
        dominant_global = int(np.argmax(global_ops))

        return {
            'total_ingested': self.total_ingested,
            'total_edges': self.total_edges,
            'raw_buffer_fill': round(self.raw_filled / RAW_BUFFER_SIZE, 4),
            'edge_buffer_fill': round(self.edge_filled / EDGE_BUFFER_SIZE, 4),
            'bucket_distribution': bucket_dist,
            'dominant_bucket': DUAL_LABELS[self.dominant_bucket],
            'generator_balance': {
                'I_structure': int(total_I),
                'O_force': int(total_O),
                'ratio': round(total_I / max(total_O, 1), 3),
            },
            'dominant_operator': OP_NAMES[dominant_global],
            'recommended_action': OP_NAMES[self.recommended_action],
            'coherence_path': [OP_NAMES[op] for op in self.current_coherence_path],
            'reality_anchors': len(self.reality_anchors),
            'gpu': _GPU,
        }

    def bucket_introspection(self) -> dict:
        """Deep introspection: what does each bucket look like?

        Returns centroid vectors and dominant operators per bucket.
        CK can see WHERE in his experience space each dual category lives.
        """
        xp = _xp
        result = {}
        for b in range(8):
            if _GPU:
                centroid = _xp.asnumpy(self.bucket_centroids[b])
            else:
                centroid = self.bucket_centroids[b].copy()

            # Dominant transition operators from/to this bucket
            if _GPU:
                incoming = _xp.asnumpy(self.operator_map[:, b, :].sum(axis=0))
                outgoing = _xp.asnumpy(self.operator_map[b, :, :].sum(axis=0))
            else:
                incoming = self.operator_map[:, b, :].sum(axis=0)
                outgoing = self.operator_map[b, :, :].sum(axis=0)

            combined = incoming + outgoing
            dom_op = int(np.argmax(combined)) if np.sum(combined) > 0 else HARMONY

            result[DUAL_LABELS[b]] = {
                'count': int(self.bucket_counts[b]),
                'centroid_force': [round(float(x), 4) for x in centroid[:5]],
                'centroid_structure': [round(float(x), 4) for x in centroid[5:]],
                'dominant_operator': OP_NAMES[dom_op],
                'path_to_harmony': [OP_NAMES[op]
                                    for op in self.coherence_paths.get(dom_op, [HARMONY])],
            }
        return result

    # ════════════════════════════════════════════════════════════
    #  Persistence
    # ════════════════════════════════════════════════════════════

    def save(self):
        """Persist edge generators, operator map, bucket centroids, reality anchors.

        The raw buffer is ephemeral (ring buffer). The STRUCTURE is what persists:
        which edges are I vs O, what operators emerged, what each bucket looks like.
        """
        os.makedirs(_PERSIST_DIR, exist_ok=True)
        xp = _xp

        # Transfer GPU tensors to CPU for serialization
        if _GPU:
            eg = _xp.asnumpy(self.edge_generators)
            om = _xp.asnumpy(self.operator_map)
            bc = _xp.asnumpy(self.bucket_counts)
            bce = _xp.asnumpy(self.bucket_centroids)
        else:
            eg = self.edge_generators
            om = self.operator_map
            bc = self.bucket_counts
            bce = self.bucket_centroids

        state = {
            'version': 1,
            'total_ingested': self.total_ingested,
            'total_edges': self.total_edges,
            'edge_generators': eg.tolist(),
            'operator_map': om.tolist(),
            'bucket_counts': bc.tolist(),
            'bucket_centroids': bce.tolist(),
            'reality_anchors': self.reality_anchors,
            'dominant_bucket': self.dominant_bucket,
            'saved_at': time.time(),
        }

        path = os.path.join(_PERSIST_DIR, 'index_state.json')
        tmp = path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(state, f)
        os.replace(tmp, path)

    def _load(self):
        """Restore persisted state."""
        path = os.path.join(_PERSIST_DIR, 'index_state.json')
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                state = json.load(f)

            xp = _xp
            self.total_ingested = state.get('total_ingested', 0)
            self.total_edges = state.get('total_edges', 0)
            self.dominant_bucket = state.get('dominant_bucket', 0)
            self.reality_anchors = state.get('reality_anchors', [])

            eg = np.array(state['edge_generators'], dtype=np.float32)
            om = np.array(state['operator_map'], dtype=np.float32)
            bc = np.array(state['bucket_counts'], dtype=np.int64)
            bce = np.array(state['bucket_centroids'], dtype=np.float32)

            if _GPU:
                self.edge_generators = _cp.asarray(eg)
                self.operator_map = _cp.asarray(om)
                self.bucket_counts = _cp.asarray(bc)
                self.bucket_centroids = _cp.asarray(bce)
            else:
                self.edge_generators = eg
                self.operator_map = om
                self.bucket_counts = bc
                self.bucket_centroids = bce

            print(f"  [EXP-INDEX] Restored: {self.total_ingested} ingested, "
                  f"{self.total_edges} edges")
        except Exception as e:
            print(f"  [EXP-INDEX] Load failed: {e}")


# ================================================================
#  Builder
# ================================================================

def build_experience_index(engine=None) -> CKExperienceIndex:
    """Build the experience index, wired into the engine."""
    return CKExperienceIndex(engine=engine)
