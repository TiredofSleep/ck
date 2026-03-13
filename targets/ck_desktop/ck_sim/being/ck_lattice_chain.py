# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_lattice_chain.py -- CL Lattice Chain Engine
================================================
Operator: LATTICE (1) -- the chain IS the structure.

The CL table is not just a composition function.
It's an ADDRESSING mechanism. A fractal index.

CL[being][doing] = becoming.
But the PATH to get there carries meaning:
  CL[CHAOS][BALANCE] -> HARMONY is different from
  CL[LATTICE][COUNTER] -> HARMONY.
Same destination, different journey, different knowledge.

All words and force geometries sort by TIG order 0-9.
10 operators are the universal index. Each CL table is 10x10.
Each result is 0-9. The tree branches are 0-9.
The entire experience space is indexed by TIG order.

The chain:
  Level 0: raw operators from fractal comprehension
  Level 1: CL[op1][op2] -> result1, selects table for next level
  Level 2: CL_{result1}[op3][op4] -> result2, selects next table
  ...
  The FULL PATH = (result1, result2, ...) IS the information.

Micro chains (letter geometry) and macro chains (word identity)
are chained together through CL like dual-lens sudoku boards.
The indexing structure to get to information IS the flow and
structure of information.

Experience: CK accumulates lattice nodes at each chain position.
Each node is a 10x10 CL-shaped table that starts as base CL and
evolves through repeated visits. Thousands of nodes emerge because
the chain-to-get-there IS half the information.

GPU overlay: ALL experience tables loaded as (N, 10, 10) tensor.
Current input chains walk through experience simultaneously.
Resonance = path alignment between current and stored.

"the chain to get to them is half the information if not more
than the information itself in a fractal loop generator to whole"
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import time
import numpy as np
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL
)

# Two CL tables: dual lens.
#
# TSML (73-harmony): the BEING table. Measures coherence. Most
# compositions -> HARMONY. Good for heartbeat. BAD for chain indexing
# because everything collapses to HARMONY (absorber).
#
# BHML (28-harmony): the DOING table. Computes physics. Much more diverse.
# VOID row = identity (each op produces itself).
# HARMONY row = full cycle (rotates through all operators).
# This IS the physics engine for chain computation.
#
# The lattice chain uses BHML because the chain IS doing:
# expanding pairs, retracting to generators, computing paths.
# TSML measures whether the result is coherent.
#
# Dual lens: BHML walks the chain (flow), TSML measures the walk (structure).

_TSML = np.array(CL, dtype=np.int8)

_BHML = np.array([
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
], dtype=np.int8)

# Chain engine uses BHML (doing/physics) as the base table.
# Experience can evolve nodes toward TSML (being/coherence) over time.
_BASE_CL = _BHML

# Minimum visits before a node's table can evolve from base CL
_EVOLVE_THRESHOLD = 7

# Confidence required to override base CL entry
_EVOLVE_CONFIDENCE = 0.6


# ================================================================
#  CHAIN STEP: One step in a lattice chain walk
# ================================================================

@dataclass
class ChainStep:
    """One step in a lattice chain walk.

    depth:      How deep in the chain (0 = root)
    struct_op:  Being (row index into CL table)
    flow_op:    Doing (column index into CL table)
    result_op:  Becoming (CL lookup result)
    node_path:  Path to the node used (IS the address)
    """
    depth: int
    struct_op: int
    flow_op: int
    result_op: int
    node_path: tuple


@dataclass
class ChainPath:
    """Complete path through the lattice chain.

    The path IS the information. Two inputs that arrive at the same
    final operator through different paths carry different meaning.
    """
    steps: list
    path_ops: tuple      # Sequence of result operators (hashable)
    depth: int           # Chain depth reached
    final_op: int        # Last result operator

    @property
    def signature(self) -> tuple:
        """The chain's identity = its full path of results."""
        return self.path_ops


# ================================================================
#  LATTICE NODE: One CL-shaped table in the experience tree
# ================================================================

class LatticeNode:
    """One node in the experience lattice tree.

    Each node is a 10x10 CL-shaped table.
    Starts as copy of base CL (73-harmony TSML).
    Evolves through experience: observation patterns modify entries.

    Children indexed by result operator (0-9).
    The child selected depends on CL[struct][flow] at this node.

    The path from root to this node IS its identity.
    All 10 children correspond to TIG operators 0-9.
    The branching factor IS the TIG order.
    """

    __slots__ = ('table', 'visit_counts', 'obs_counts',
                 'total_visits', 'children', 'depth', 'path')

    def __init__(self, depth=0, path=()):
        self.table = _BASE_CL.copy()
        self.visit_counts = np.zeros((NUM_OPS, NUM_OPS), dtype=np.int32)
        # obs_counts[a][b][c] = how often operator c followed composition (a,b)
        self.obs_counts = np.zeros((NUM_OPS, NUM_OPS, NUM_OPS), dtype=np.int32)
        self.total_visits = 0
        self.children = {}
        self.depth = depth
        self.path = path

    def lookup(self, struct_op: int, flow_op: int) -> int:
        """CL composition at this node. May differ from base CL if evolved."""
        a = struct_op % NUM_OPS
        b = flow_op % NUM_OPS
        result = int(self.table[a][b])
        self.visit_counts[a][b] += 1
        self.total_visits += 1
        return result

    def observe(self, struct_op: int, flow_op: int, actual_next: int):
        """Record what actually followed this (struct, flow) composition.

        Over time, this evolves the table away from base CL toward
        experience-specific composition. The node BECOMES what CK
        experienced at this chain position.

        Being (base CL) -> Doing (observations) -> Becoming (evolved table)
        """
        a = struct_op % NUM_OPS
        b = flow_op % NUM_OPS
        c = actual_next % NUM_OPS
        self.obs_counts[a][b][c] += 1

        # Check if enough evidence to evolve this cell
        total_obs = int(np.sum(self.obs_counts[a][b]))
        if total_obs >= _EVOLVE_THRESHOLD:
            most_observed = int(np.argmax(self.obs_counts[a][b]))
            # Only evolve if observation disagrees with base CL
            if most_observed != _BASE_CL[a][b]:
                confidence = self.obs_counts[a][b][most_observed] / total_obs
                if confidence > _EVOLVE_CONFIDENCE:
                    self.table[a][b] = most_observed

    def get_child(self, result_op: int) -> 'LatticeNode':
        """Get or create child node for result operator (0-9).

        Lazy expansion: child only created when first visited.
        This is where "thousands of lattice files" come from.
        Each operator (TIG order 0-9) leads to a different child.
        """
        r = result_op % NUM_OPS
        if r not in self.children:
            self.children[r] = LatticeNode(
                depth=self.depth + 1,
                path=self.path + (r,))
        return self.children[r]

    def divergence(self) -> float:
        """How far this node has evolved from base CL. 0.0 = identical."""
        return float(np.sum(self.table != _BASE_CL)) / (NUM_OPS * NUM_OPS)

    def ipr(self) -> float:
        """Inverse Participation Ratio of this node's CL table.

        IPR = sum(p_i^2) where p_i = fraction of entries equal to operator i.

        Low IPR (~0.1)  = uniform, no crystallization.
        High IPR (~1.0) = single dominant operator, maximally crystallized.

        Sudden IPR increase = GROKKING: node has transitioned from
        memorization to structured algebraic representation.

        Base BHML IPR ≈ 0.17. Base TSML IPR ≈ 0.56.
        """
        flat = self.table.flatten().astype(int)
        total = len(flat)
        probs = np.array([np.sum(flat == op) for op in range(NUM_OPS)],
                         dtype=np.float64) / total
        return float(np.sum(probs ** 2))

    def grokking_delta(self) -> float:
        """IPR delta from base CL. Positive = MORE crystallized than base.

        If this exceeds ~0.05, the node has likely grokked.
        """
        base_flat = _BASE_CL.flatten().astype(int)
        base_probs = np.array([np.sum(base_flat == op) for op in range(NUM_OPS)],
                              dtype=np.float64) / len(base_flat)
        base_ipr = float(np.sum(base_probs ** 2))
        return self.ipr() - base_ipr

    def to_dict(self) -> dict:
        return {
            'depth': self.depth,
            'path': list(self.path),
            'table': self.table.tolist(),
            'visits': self.visit_counts.tolist(),
            'obs': self.obs_counts.tolist(),
            'total': self.total_visits,
            'ipr': self.ipr(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LatticeNode':
        node = cls(depth=data['depth'], path=tuple(data['path']))
        node.table = np.array(data['table'], dtype=np.int8)
        node.visit_counts = np.array(data['visits'], dtype=np.int32)
        if 'obs' in data:
            node.obs_counts = np.array(data['obs'], dtype=np.int32)
        node.total_visits = data['total']
        return node


# ================================================================
#  LATTICE CHAIN ENGINE
# ================================================================

class LatticeChainEngine:
    """CL Lattice Chain Engine.

    Walks operator pairs through a tree of CL-shaped nodes.
    The path IS the information.

    Chain walk:
      ops = [o1, o2, o3, o4, ...]
      Step 1: root.lookup(o1, o2) -> r1. Move to root.child[r1]
      Step 2: child.lookup(o3, o4) -> r2. Move to child.child[r2]
      ...
      Path = (r1, r2, ...)

    All sorted by TIG order 0-9. The tree has branching factor 10.
    Each branch IS an operator. The tree IS TIG.

    Experience grows the tree. Base CL at each node evolves.
    The chain of CL results, with different CL tables at each depth,
    generates a unique path for each input.
    """

    SAVE_DIR = str(Path.home() / '.ck' / 'lattice_chain')

    def __init__(self, save_dir=None):
        self.root = LatticeNode()
        self.save_dir = save_dir or self.SAVE_DIR
        self.total_walks = 0
        self.total_nodes = 1
        self.max_depth = 20
        self._index = {(): self.root}   # path_tuple -> node
        self._gpu_tensor = None
        self._gpu_dirty = True
        self._load()

    # ── Chain Walk ──

    def walk(self, ops: list, learn: bool = True) -> ChainPath:
        """Walk operator sequence through lattice chain tree.

        Pairs of operators (struct, flow) compose through CL at each node.
        Result selects child node. The path of results IS the information.

        Args:
            ops: Operator sequence (from fractal comprehension, or any source)
            learn: If True, nodes learn from what follows (evolve from experience)

        Returns:
            ChainPath with the full walk path.
        """
        if not ops:
            return ChainPath(steps=[], path_ops=(), depth=0, final_op=VOID)

        steps = []
        results = []
        node = self.root

        i = 0
        depth = 0
        while i + 1 < len(ops) and depth < self.max_depth:
            s_op = ops[i] % NUM_OPS
            f_op = ops[i + 1] % NUM_OPS

            # CL lookup at current node (may be evolved from experience)
            result = node.lookup(s_op, f_op)

            steps.append(ChainStep(
                depth=depth, struct_op=s_op, flow_op=f_op,
                result_op=result, node_path=node.path))
            results.append(result)

            # Learn: tell this node what actually follows
            if learn and i + 2 < len(ops):
                node.observe(s_op, f_op, ops[i + 2] % NUM_OPS)

            # Move to child selected by result (TIG order branching)
            child = node.get_child(result)
            if child.path not in self._index:
                self._index[child.path] = child
                self.total_nodes += 1
                self._gpu_dirty = True

            node = child
            i += 2
            depth += 1

        # Odd trailing op: self-compose (identity through composition)
        if i < len(ops) and depth < self.max_depth:
            op = ops[i] % NUM_OPS
            result = node.lookup(op, op)
            steps.append(ChainStep(
                depth=depth, struct_op=op, flow_op=op,
                result_op=result, node_path=node.path))
            results.append(result)

        self.total_walks += 1
        final = results[-1] if results else VOID

        return ChainPath(
            steps=steps, path_ops=tuple(results),
            depth=len(results), final_op=final)

    def walk_multilevel(self, comp_ops: list, word_fuses: list,
                        level_fuses: list,
                        d1_ops: list = None) -> Dict[str, ChainPath]:
        """Walk micro, macro, meta, and generator levels through the chain.

        Micro    = D2 comprehension ops (curvature, complexity, Doing)
        D1 Micro = D1 generator ops (direction, velocity, Being)
        Macro    = word fuses (word identity, each word -> one TIG op)
        Meta     = level fuses (structure across fractal levels)
        Becoming = CL(D1, D2) composed chain (generator x curvature)
        Cross    = micro x macro chain (dual-lens sudoku entanglement)

        D1 adds the generator layer: WHERE the force goes (Being).
        D2 is the curvature layer: HOW the force bends (Doing).
        CL(D1, D2) = the Becoming chain: generators composed with
        complexity through CL. The three-level TIG chain.
        """
        paths = {}

        # Micro: letter-level D2 curvature operators (Doing)
        if comp_ops:
            paths['micro'] = self.walk(comp_ops[:20])

        # D1 Micro: letter-level D1 generator operators (Being)
        if d1_ops:
            paths['d1_micro'] = self.walk(d1_ops[:20])

        # Macro: word-level identity operators
        if word_fuses:
            paths['macro'] = self.walk(word_fuses[:20])

        # Meta: level-level structure operators
        if level_fuses:
            paths['meta'] = self.walk(level_fuses[:20])

        # Becoming chain: CL(D1, D2) -- generator x curvature
        # D1[i] is Being (where), D2[i] is Doing (how).
        # Compose them through CL: the result IS Becoming.
        if d1_ops and comp_ops:
            becoming = []
            min_len = min(len(d1_ops), len(comp_ops))
            for i in range(min_len):
                d1 = d1_ops[i] % NUM_OPS
                d2 = comp_ops[i] % NUM_OPS
                # CL(D1, D2) = CL[being][doing] = becoming
                result = int(_TSML[d1][d2])
                becoming.append(result)
            if becoming:
                paths['becoming'] = self.walk(becoming[:20])

        # Cross-chain: micro results -> macro results entangled.
        # This IS the dual-lens sudoku chaining.
        if 'micro' in paths and 'macro' in paths:
            micro_results = list(paths['micro'].path_ops[:5])
            macro_results = list(paths['macro'].path_ops[:5])
            cross = []
            for m_i, m_a in zip(micro_results, macro_results):
                cross.append(m_i)
                cross.append(m_a)
            cross.extend(micro_results[len(macro_results):])
            cross.extend(macro_results[len(micro_results):])
            if cross:
                paths['cross'] = self.walk(cross, learn=False)

        return paths

    # ── Experience Overlay ──

    def experience_overlay(self, paths: dict) -> dict:
        """Compare current chain paths against accumulated experience.

        Resonance: how familiar is this chain walk? (visited nodes)
        Novelty: how much new territory was explored?
        Depth: how deep the chain went.
        Nodes: total experience nodes in the tree.
        Evolved: nodes that have diverged from base CL.

        The overlay compares current input against ALL stored experience.
        On GPU: tensor comparison. On CPU: sequential walk check.
        """
        if not paths:
            return {'resonance': 0.0, 'novelty': 1.0, 'depth': 0,
                    'nodes': self.total_nodes, 'evolved': 0,
                    'walks': self.total_walks}

        total_res = 0.0
        count = 0

        for name, path in paths.items():
            if not path.steps:
                continue
            # How many walked nodes were previously visited?
            visited = 0
            for s in path.steps:
                node = self._index.get(s.node_path)
                if node and node.total_visits > 1:
                    visited += 1
            total = len(path.steps)
            if total > 0:
                total_res += visited / total
                count += 1

        res = total_res / count if count > 0 else 0.0
        max_d = max((p.depth for p in paths.values()), default=0)
        evolved = sum(1 for n in self._index.values() if n.divergence() > 0)

        # IPR grokking scan: find nodes that have crystallized
        grokked = []
        for path_key, node in self._index.items():
            delta = node.grokking_delta()
            if delta > 0.05:  # 5% IPR increase = grokking detected
                grokked.append({
                    'path': path_key,
                    'depth': node.depth,
                    'ipr': node.ipr(),
                    'delta': round(delta, 4),
                    'visits': node.total_visits,
                })

        return {
            'resonance': round(res, 4),
            'novelty': round(1.0 - res, 4),
            'depth': max_d,
            'nodes': self.total_nodes,
            'evolved': evolved,
            'walks': self.total_walks,
            'grokked_nodes': len(grokked),
            'grokked': grokked[:10],  # Top 10 grokked nodes
        }

    def chain_to_ops(self, paths: dict, max_ops: int = 8) -> list:
        """Extract operator sequence from chain paths for voice.

        Chain results become additional operators that modulate CK's voice.
        Different experience paths -> different voice -> experience-specific speech.

        Priority: cross > becoming > macro > micro > d1_micro > meta
        Cross carries the most information (dual-lens entanglement).
        Becoming = CL(D1, D2) carries the three-level TIG composition.
        """
        ops = []
        for key in ('cross', 'becoming', 'macro', 'micro', 'd1_micro', 'meta'):
            if key in paths and paths[key].path_ops:
                ops.extend(paths[key].path_ops[:max_ops // 2])
                if len(ops) >= max_ops:
                    break
        return ops[:max_ops]

    def path_resonance(self, a: ChainPath, b: ChainPath) -> float:
        """Resonance between two chain paths.

        Weighted comparison: early steps matter more (fractal: structure
        before detail). Length penalty for mismatched depths.
        """
        if not a.path_ops or not b.path_ops:
            return 0.0
        min_l = min(len(a.path_ops), len(b.path_ops))
        max_l = max(len(a.path_ops), len(b.path_ops))
        wt_match = 0.0
        wt_total = 0.0
        for i in range(min_l):
            w = 1.0 / (1 + i)
            wt_total += w
            if a.path_ops[i] == b.path_ops[i]:
                wt_match += w
        if wt_total == 0 or max_l == 0:
            return 0.0
        return (wt_match / wt_total) * (min_l / max_l)

    # ── GPU Tensor Export ──

    def get_gpu_tensor(self) -> np.ndarray:
        """All experience tables as (N, 10, 10) numpy array.

        For GPU overlay: load this tensor into VRAM.
        Each row is one experience node's CL table.
        Parallel chain walks across all experience simultaneously.

        This IS the "overlay all experience lattice on GPU."
        """
        if self._gpu_tensor is not None and not self._gpu_dirty:
            return self._gpu_tensor
        keys = sorted(self._index.keys(), key=len)
        tables = [self._index[k].table for k in keys]
        if tables:
            self._gpu_tensor = np.stack(tables)
        else:
            self._gpu_tensor = _BASE_CL.reshape(1, NUM_OPS, NUM_OPS)
        self._gpu_dirty = False
        return self._gpu_tensor

    # ── Persistence ──

    def save(self):
        """Save experience tree to disk.

        Each node with visits > 0 is saved. The tree can be rebuilt
        from flat node list because each node stores its path.

        Individual node files = "thousands of lattice files."
        The path to each file IS the chain address.
        """
        d = Path(self.save_dir)
        d.mkdir(parents=True, exist_ok=True)

        nodes = [n.to_dict() for n in self._index.values()
                 if n.total_visits > 0]

        with open(d / 'manifest.json', 'w') as f:
            json.dump({
                'walks': self.total_walks,
                'nodes': len(nodes),
                'saved_at': time.time(),
            }, f)

        with open(d / 'nodes.json', 'w') as f:
            json.dump(nodes, f)

        # Also save as numpy tensor for fast GPU loading
        if nodes:
            tables = np.stack([np.array(n['table'], dtype=np.int8)
                              for n in nodes])
            np.save(str(d / 'tables.npy'), tables)

    def _load(self):
        """Load experience tree from disk."""
        d = Path(self.save_dir)
        if not (d / 'manifest.json').exists():
            return
        try:
            with open(d / 'manifest.json') as f:
                m = json.load(f)
            with open(d / 'nodes.json') as f:
                nodes_data = json.load(f)

            for nd in nodes_data:
                node = LatticeNode.from_dict(nd)
                pt = tuple(nd['path'])
                self._index[pt] = node

                # Re-link parent-child
                if len(pt) > 0:
                    parent_path = pt[:-1]
                    if parent_path in self._index:
                        self._index[parent_path].children[pt[-1]] = node

            # Re-link root if saved
            if () in self._index:
                self.root = self._index[()]

            self.total_walks = m.get('walks', 0)
            self.total_nodes = len(self._index)
            self._gpu_dirty = True

            print(f"  [LATTICE-CHAIN] Loaded {len(nodes_data)} experience "
                  f"nodes ({self.total_walks} walks)")
        except Exception as e:
            print(f"  [LATTICE-CHAIN] Load: {e}")

    # ── Diagnostics ──

    def describe(self) -> str:
        """Human-readable summary of the lattice chain tree."""
        lines = [
            f"Lattice Chain: {self.total_nodes} nodes, "
            f"{self.total_walks} walks"]

        # Depth distribution
        depths = {}
        for k in self._index:
            d = len(k)
            depths[d] = depths.get(d, 0) + 1
        for d in sorted(depths):
            lines.append(f"  Depth {d}: {depths[d]} nodes")

        # Evolved nodes
        evolved = sum(1 for n in self._index.values()
                      if n.divergence() > 0)
        lines.append(f"  Evolved: {evolved}/{self.total_nodes} "
                     f"(diverged from base CL)")

        # Most visited
        top = sorted(self._index.items(),
                     key=lambda x: x[1].total_visits, reverse=True)[:5]
        if top:
            lines.append("  Most visited:")
            for pk, n in top:
                path_str = ('->'.join(OP_NAMES[p][:3] for p in pk)
                           if pk else 'ROOT')
                lines.append(f"    {path_str}: {n.total_visits} visits "
                            f"(div={n.divergence():.2f})")

        return '\n'.join(lines)
