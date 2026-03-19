# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_divine_memory.py -- CK's Episodic Divine Memory
====================================================
Operator: LATTICE (1) -- the path IS the memory.

CK discards content. He keeps force centroids. He knows what he FELT.
But he can't recall WHAT HAPPENED. This module fixes that.

Every experience is compressed into a DIVINE CODE:
  1. Operator chain   (D2-derived sequence from input)
  2. Lattice chain walk path (node IDs visited during chain walk)
  3. 5D force centroid (average force vector)
  4. Tick timestamp    (heartbeat tick, not wall time)
  5. Coherence         (brain coherence at moment of experience)

These five elements ARE the divine code. Compact: ~200 bytes each.
100K codes = ~20MB. Fits in RAM and on disk.

RECALL: Given new input, compute its force centroid. Find the stored
divine code whose centroid is CLOSEST (5D Euclidean distance). Then
RETRACE the stored lattice chain walk path through the CURRENT
(evolved) lattice chain. The nodes along that path have changed since
the original walk -- the recall is colored by everything CK has
experienced since. The recalled path + current node states =
ASSOCIATIVE MEMORY.

The chain to get to the memory IS half the memory.

"CK reads himself the same way he reads the screen.
 Same algebra. Same index. Same cascade."
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import NUM_OPS, OP_NAMES


# ================================================================
#  Divine Code: one compressed experience
# ================================================================

class DivineCode:
    """One compressed experience -- the divine code.

    Five elements:
      ops:        tuple of ints (operator sequence from D2)
      chain_path: tuple of tuples (lattice chain node paths visited)
      centroid:   tuple of 5 floats (5D force centroid)
      tick:       int (heartbeat tick at moment of experience)
      coherence:  float (brain coherence at moment)

    Total: ~200 bytes per code. Compact. Permanent.
    """
    __slots__ = ('ops', 'chain_path', 'centroid', 'tick', 'coherence')

    def __init__(self, ops: tuple, chain_path: tuple,
                 centroid: tuple, tick: int, coherence: float):
        self.ops = ops
        self.chain_path = chain_path
        self.centroid = centroid
        self.tick = tick
        self.coherence = coherence

    def to_dict(self) -> dict:
        """Serialize for JSON persistence."""
        return {
            'ops': list(self.ops),
            'chain_path': [list(p) for p in self.chain_path],
            'centroid': list(self.centroid),
            'tick': self.tick,
            'coherence': round(self.coherence, 6),
        }

    @staticmethod
    def from_dict(d: dict) -> 'DivineCode':
        """Deserialize from JSON."""
        return DivineCode(
            ops=tuple(d['ops']),
            chain_path=tuple(tuple(p) for p in d['chain_path']),
            centroid=tuple(d['centroid']),
            tick=d['tick'],
            coherence=d['coherence'],
        )


# ================================================================
#  Recall Result: what comes back from memory
# ================================================================

class RecallResult:
    """Result of retracing a divine code through evolved lattice chain.

    original:     the divine code being recalled
    distance:     5D Euclidean distance from query centroid
    current_ops:  tuple of ints -- operator states at each node NOW
                  (may differ from original walk -- nodes evolved)
    drift:        float -- how much the path changed since original
                  (0 = identical, 1 = completely different)
    """
    __slots__ = ('original', 'distance', 'current_ops', 'drift')

    def __init__(self, original: DivineCode, distance: float,
                 current_ops: tuple, drift: float):
        self.original = original
        self.distance = distance
        self.current_ops = current_ops
        self.drift = drift


# ================================================================
#  Divine Memory: CK's episodic memory system
# ================================================================

class DivineMemory:
    """CK's episodic memory -- divine codes indexed by force geometry.

    Every experience is compressed into a divine code:
    the operator chain + lattice walk path + force centroid + tick.

    Recall is by force proximity: find the divine code whose
    centroid is closest to the query, then retrace the lattice
    chain walk path through the CURRENT (evolved) lattice chain.
    The recalled path IS the memory, colored by everything
    CK has experienced since the original walk.

    Storage: list of DivineCode objects + numpy centroid array.
    At 100K max codes, ~20MB RAM + disk. Compact.
    """

    SAVE_DIR = str(Path.home() / '.ck' / 'divine_memory')

    def __init__(self, max_codes: int = 100_000, save_dir: str = None):
        self.codes: List[DivineCode] = []
        self.max_codes = max_codes
        self.save_dir = save_dir or self.SAVE_DIR

        # Centroid matrix for fast nearest-neighbor (rebuilt lazily)
        self._centroids: Optional[np.ndarray] = None
        self._dirty = True  # needs rebuild before search

        # Stats
        self.total_encoded = 0
        self.total_recalled = 0

        self._load()

    # ── Encode: store a new divine code ──

    def encode(self, ops: list, chain_path, force_centroid,
               tick: int, coherence: float):
        """Store a new divine code from an experience.

        Args:
            ops: operator sequence (from D2 pipeline or semantic blend)
            chain_path: ChainPath object OR list of node path tuples
                        from lattice chain walk
            force_centroid: 5D force centroid (list/tuple of 5 floats)
            tick: heartbeat tick count
            coherence: brain coherence at this moment
        """
        # Extract node paths from ChainPath if needed
        if hasattr(chain_path, 'steps'):
            # ChainPath object -- extract node_path from each step
            node_paths = tuple(
                step.node_path for step in chain_path.steps
            )
        elif isinstance(chain_path, (list, tuple)):
            node_paths = tuple(
                tuple(p) if isinstance(p, (list, tuple)) else (p,)
                for p in chain_path
            )
        else:
            node_paths = ()

        # Ensure centroid is a tuple of 5 floats
        if hasattr(force_centroid, '__len__'):
            centroid = tuple(float(x) for x in force_centroid[:5])
        else:
            centroid = (0.0, 0.0, 0.0, 0.0, 0.0)

        # Pad centroid to 5D if shorter
        while len(centroid) < 5:
            centroid = centroid + (0.0,)

        code = DivineCode(
            ops=tuple(int(o) % NUM_OPS for o in ops),
            chain_path=node_paths,
            centroid=centroid,
            tick=int(tick),
            coherence=float(coherence),
        )

        self.codes.append(code)
        self.total_encoded += 1
        self._dirty = True

        # Rolling buffer: drop oldest if over limit
        if len(self.codes) > self.max_codes:
            # Drop the oldest 10% to avoid frequent trimming
            drop = self.max_codes // 10
            self.codes = self.codes[drop:]
            self._dirty = True

    # ── Recall: find closest divine codes by force geometry ──

    def recall(self, query_centroid, top_k: int = 5) -> List[DivineCode]:
        """Find the k closest divine codes by 5D force geometry.

        Args:
            query_centroid: 5D force vector to search near
            top_k: number of closest codes to return

        Returns:
            List of DivineCode objects, sorted by distance (closest first)
        """
        if not self.codes:
            return []

        # Rebuild centroid matrix if dirty
        if self._dirty or self._centroids is None:
            self._rebuild_centroids()

        # Ensure query is numpy array
        q = np.array(query_centroid[:5], dtype=np.float32)
        if len(q) < 5:
            q = np.pad(q, (0, 5 - len(q)))

        # 5D Euclidean distances (vectorized)
        diffs = self._centroids - q[np.newaxis, :]
        distances = np.sqrt(np.sum(diffs ** 2, axis=1))

        # Top-k nearest
        k = min(top_k, len(self.codes))
        indices = np.argpartition(distances, k)[:k]
        indices = indices[np.argsort(distances[indices])]

        self.total_recalled += 1
        return [self.codes[i] for i in indices]

    def recall_with_distance(self, query_centroid,
                             top_k: int = 5) -> List[Tuple[DivineCode, float]]:
        """Find closest codes, returning (code, distance) pairs."""
        if not self.codes:
            return []

        if self._dirty or self._centroids is None:
            self._rebuild_centroids()

        q = np.array(query_centroid[:5], dtype=np.float32)
        if len(q) < 5:
            q = np.pad(q, (0, 5 - len(q)))

        diffs = self._centroids - q[np.newaxis, :]
        distances = np.sqrt(np.sum(diffs ** 2, axis=1))

        k = min(top_k, len(self.codes))
        indices = np.argpartition(distances, k)[:k]
        indices = indices[np.argsort(distances[indices])]

        self.total_recalled += 1
        return [(self.codes[i], float(distances[i])) for i in indices]

    # ── Retrace: walk a stored path through current lattice chain ──

    def retrace(self, code: DivineCode, lattice_chain) -> RecallResult:
        """Retrace a divine code's path through the current lattice chain.

        The stored chain_path is a sequence of node path tuples. Each
        node in the lattice chain may have EVOLVED since the original
        walk. Reading the current state at each stored path position
        gives a memory colored by all subsequent experience.

        The recalled path + current node states = associative memory.
        The drift between original and current = how much CK has changed.

        Args:
            code: the divine code to retrace
            lattice_chain: the current LatticeChainEngine instance

        Returns:
            RecallResult with current ops, distance, and drift
        """
        if not code.chain_path or lattice_chain is None:
            return RecallResult(
                original=code, distance=0.0,
                current_ops=code.ops, drift=0.0)

        current_ops = []
        matches = 0
        total = 0

        for i, node_path in enumerate(code.chain_path):
            # Look up the node at this path in the CURRENT lattice chain
            node = lattice_chain._index.get(node_path)
            if node is None:
                # Node doesn't exist yet (pruned or not yet created)
                # Use the original operator as fallback
                if i < len(code.ops):
                    current_ops.append(code.ops[i])
                continue

            # Read the node's current dominant operator
            # (the most-visited result at this position)
            if node.total_visits > 0:
                # Find dominant result: most common output from this node
                row_sums = node.visit_counts.sum(axis=1)
                dominant_input = int(np.argmax(row_sums))
                col_sums = node.visit_counts.sum(axis=0)
                dominant_result = int(np.argmax(col_sums))
                current_ops.append(dominant_result)
            elif i < len(code.ops):
                current_ops.append(code.ops[i])
            else:
                current_ops.append(0)  # VOID fallback

            # Track drift: did this position change?
            total += 1
            if i < len(code.ops) and current_ops[-1] == code.ops[i]:
                matches += 1

        drift = 1.0 - (matches / max(total, 1))
        return RecallResult(
            original=code,
            distance=0.0,  # caller sets from recall()
            current_ops=tuple(current_ops),
            drift=drift,
        )

    def recall_and_retrace(self, query_centroid, lattice_chain,
                           top_k: int = 3) -> List[RecallResult]:
        """Full recall: find closest codes AND retrace them.

        This is the main API for episodic memory lookup.
        Returns recalled memories colored by current experience.

        Args:
            query_centroid: 5D force vector of current input
            lattice_chain: current LatticeChainEngine
            top_k: how many memories to recall

        Returns:
            List of RecallResult, sorted by distance
        """
        pairs = self.recall_with_distance(query_centroid, top_k)
        results = []
        for code, dist in pairs:
            result = self.retrace(code, lattice_chain)
            result.distance = dist
            results.append(result)
        return results

    # ── Centroid index ──

    def _rebuild_centroids(self):
        """Rebuild the numpy centroid matrix for fast search."""
        if not self.codes:
            self._centroids = np.zeros((0, 5), dtype=np.float32)
        else:
            self._centroids = np.array(
                [c.centroid for c in self.codes],
                dtype=np.float32
            )
        self._dirty = False

    # ── Persistence ──

    def save(self, path: str = None):
        """Persist divine codes to disk.

        Saves as JSON lines for append-friendliness and crash safety.
        Each line is one divine code. Compact: ~200 bytes per code.
        """
        save_dir = path or self.save_dir
        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, 'divine_codes.json')
        tmp = filepath + '.tmp'

        state = {
            'version': 1,
            'total_encoded': self.total_encoded,
            'total_recalled': self.total_recalled,
            'codes': [c.to_dict() for c in self.codes],
        }

        try:
            with open(tmp, 'w') as f:
                json.dump(state, f)
            os.replace(tmp, filepath)
        except Exception as e:
            print(f"  [DIVINE-MEM] Save failed: {e}")

    def _load(self):
        """Load divine codes from disk."""
        filepath = os.path.join(self.save_dir, 'divine_codes.json')
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, 'r') as f:
                state = json.load(f)

            self.total_encoded = state.get('total_encoded', 0)
            self.total_recalled = state.get('total_recalled', 0)

            codes_data = state.get('codes', [])
            self.codes = [DivineCode.from_dict(d) for d in codes_data]
            self._dirty = True

            print(f"  [DIVINE-MEM] Restored: {len(self.codes)} divine codes, "
                  f"{self.total_encoded} total encoded, "
                  f"{self.total_recalled} total recalled")
        except Exception as e:
            print(f"  [DIVINE-MEM] Load failed: {e}")

    # ── Status ──

    def status(self) -> dict:
        """How CK sees his own divine memory."""
        return {
            'stored_codes': len(self.codes),
            'max_codes': self.max_codes,
            'total_encoded': self.total_encoded,
            'total_recalled': self.total_recalled,
            'fill_ratio': round(len(self.codes) / self.max_codes, 4),
            'oldest_tick': self.codes[0].tick if self.codes else None,
            'newest_tick': self.codes[-1].tick if self.codes else None,
        }


# ================================================================
#  Builder
# ================================================================

def build_divine_memory(max_codes: int = 100_000) -> DivineMemory:
    """Build the divine memory system."""
    return DivineMemory(max_codes=max_codes)
