# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_reasoning.py -- CK's 3-Speed Reasoning Engine
==================================================
Operator: PROGRESS (3) -- forward motion through the concept graph.

CK's reasoning engine traverses the world lattice at three speeds:
  QUICK   (reflex)    -- 1 hop, immediate neighbors, no exploration
  NORMAL  (reasoned)  -- 3 hops, spreading activation, BTQ gating
  HEAVY   (discovery) -- Levy jumps + contradiction pruning + multi-hop proofs

This is NOT a neural network. No weights, no gradients, no training.
This is algebraic graph traversal on the concept lattice:

  1. Spreading Activation (Collins/Loftus 1975):
     Concepts activate neighbors. Activation decays with distance.
     Edges labeled HARMONY spread freely; COLLAPSE edges dampen.

  2. Levy Jumps (creative exploration):
     Instead of following edges, jump to a distant node with probability
     proportional to operator signature similarity on soft_dist.
     This is how CK makes creative connections:
     "gravity" -> "loneliness" (both pull things inward).

  3. Contradiction Pruning:
     If a reasoning path contains nodes connected by 'opposes' relations,
     the path is contradictory and gets killed. "X causes Y" + "X prevents Y"
     is a contradiction. Only coherent paths survive.

All gated by BTQ safety: the composition table (CL) modulates which
edges amplify and which edges dampen, ensuring reasoning stays coherent.

Memory: ~2KB for activation map. CPU: trivial graph walks.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES, CL, compose
)
from ck_sim.ck_world_lattice import WorldLattice, WorldNode, RELATION_TYPES


# ================================================================
#  CONSTANTS
# ================================================================

SPEED_QUICK = 0     # Reflex: 1 hop, no exploration
SPEED_NORMAL = 1    # Reasoned: 3 hops, spreading activation
SPEED_HEAVY = 2     # Discovery: Levy jumps + contradiction pruning

SPEED_NAMES = ['QUICK', 'NORMAL', 'HEAVY']

DEFAULT_DECAY = 0.7         # Activation decay per hop
COLLAPSE_DAMPEN = 0.3       # Multiplier for COLLAPSE edge spread
MIN_ACTIVATION = 0.01       # Below this, node is considered inactive
DEFAULT_TOP_K = 5           # Default number of top activated nodes
LEVY_CANDIDATES = 10        # Default Levy jump candidate pool size
HEAVY_LEVY_JUMPS = 3        # Number of Levy jumps in HEAVY reasoning
NORMAL_SPREAD_STEPS = 3     # Spreading activation hops for NORMAL
NORMAL_MIN_RESULTS = 3      # Minimum results for NORMAL reasoning
NORMAL_MAX_RESULTS = 7      # Maximum results for NORMAL reasoning
HEAVY_MAX_HYPOTHESES = 2    # Maximum surviving hypotheses in HEAVY


# ================================================================
#  ACTIVATION MAP: Spreading Activation on Concept Graph
# ================================================================

class ActivationMap:
    """Spreading activation on concept graph.

    Each concept node has an activation level [0, 1].
    Activation spreads through edges, decaying with distance.
    Edges labeled with HARMONY spread more; COLLAPSE edges dampen.

    This is the Collins/Loftus (1975) spreading activation model,
    adapted for CK's operator-labeled concept graph. The CL composition
    table modulates spread: HARMONY edges propagate fully, COLLAPSE
    edges are dampened to 30%, and all edges decay by the decay factor
    per hop.
    """

    def __init__(self, lattice: WorldLattice, decay: float = DEFAULT_DECAY):
        self.lattice = lattice
        self.decay = decay
        self.activations: Dict[str, float] = {}
        self._spread_count = 0

    def activate(self, node_id: str, strength: float = 1.0):
        """Activate a single node.

        Strength is clamped to [0, 1]. If the node is already active,
        the new strength is max(old, new) -- activation doesn't subtract.
        """
        if node_id not in self.lattice.nodes:
            return
        strength = max(0.0, min(1.0, strength))
        current = self.activations.get(node_id, 0.0)
        self.activations[node_id] = max(current, strength)

    def spread(self, steps: int = NORMAL_SPREAD_STEPS) -> Dict[str, float]:
        """Spread activation N steps. Returns all activated nodes.

        For each active node, spread to neighbors:
          - Activation decays by self.decay per hop
          - CL composition on edge operator modulates spread:
              HARMONY edges: full spread (decay only)
              COLLAPSE edges: dampened (x 0.3)
              Other edges: normal decay
          - Activation at target = max(existing, incoming)
        """
        for step in range(steps):
            new_activations: Dict[str, float] = {}

            for node_id, activation in self.activations.items():
                if activation < MIN_ACTIVATION:
                    continue

                neighbors = self.lattice.get_neighbors(node_id)
                for target_id, rel_type, edge_op in neighbors:
                    # Base spread: current activation * decay
                    spread_strength = activation * self.decay

                    # Modulate by edge operator via CL composition
                    source_op = self.lattice.nodes[node_id].operator_code
                    composed = compose(source_op, edge_op)

                    if edge_op == COLLAPSE:
                        # COLLAPSE edge (opposes/prevents): always dampen
                        # Regardless of CL composition -- tension reduces spread
                        spread_strength *= COLLAPSE_DAMPEN
                    elif composed == HARMONY:
                        # HARMONY composition: full spread (decay only)
                        pass
                    elif composed == COLLAPSE:
                        # CL composed to COLLAPSE: also dampen
                        spread_strength *= COLLAPSE_DAMPEN
                    # else: normal decay (no additional modifier)

                    if spread_strength >= MIN_ACTIVATION:
                        current = new_activations.get(target_id, 0.0)
                        new_activations[target_id] = max(current, spread_strength)

            # Merge new activations into existing (max, not sum)
            for node_id, new_act in new_activations.items():
                current = self.activations.get(node_id, 0.0)
                self.activations[node_id] = max(current, new_act)

            self._spread_count += 1

        return dict(self.activations)

    def top_k(self, k: int = DEFAULT_TOP_K) -> List[Tuple[str, float]]:
        """Return top-k most activated nodes, sorted by activation descending."""
        sorted_nodes = sorted(
            self.activations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_nodes[:k]

    def get_activation(self, node_id: str) -> float:
        """Get activation level of a specific node."""
        return self.activations.get(node_id, 0.0)

    def active_count(self) -> int:
        """Number of nodes above MIN_ACTIVATION threshold."""
        return sum(1 for v in self.activations.values() if v >= MIN_ACTIVATION)

    def reset(self):
        """Clear all activations."""
        self.activations.clear()
        self._spread_count = 0


# ================================================================
#  LEVY JUMPER: Creative Sparse Jumps for Exploration
# ================================================================

class LevyJumper:
    """Levy flight jumps on concept graph for creative exploration.

    Instead of following edges, jump to a distant node with probability
    proportional to operator signature similarity. This is how CK
    makes creative connections: "gravity" -> "loneliness" (both pull).

    The jump finds nodes that are DISTANT in graph topology but
    SIMILAR in operator signature (soft_dist). This is the algebraic
    analog of metaphor: things that look nothing alike but behave
    the same way.

    Uses LFSR pseudo-random (same deterministic RNG as everywhere in CK)
    to select from top-N candidates weighted by cosine similarity.
    """

    def __init__(self, lattice: WorldLattice, lfsr_seed: int = 0xBEEFCAFE):
        self.lattice = lattice
        self._lfsr = lfsr_seed
        self._jump_count = 0

    def jump(self, from_node_id: str, n_candidates: int = LEVY_CANDIDATES) -> Optional[str]:
        """Make a Levy jump from a node. Returns target node_id or None.

        1. Get source node's operator signature (soft_dist)
        2. Score ALL other nodes by cosine similarity on soft_dist
        3. Exclude direct neighbors (we want DISTANT connections)
        4. Use LFSR to pick from top-N candidates (weighted by similarity)

        This finds "distant but similar" nodes -- creative associations.
        """
        source = self.lattice.nodes.get(from_node_id)
        if source is None:
            return None

        source_soft = source.soft_dist
        source_mag = math.sqrt(sum(v * v for v in source_soft)) or 1e-10

        # Get direct neighbors to exclude them (we want DISTANT jumps)
        direct_neighbors = set()
        for target_id, _, _ in self.lattice.get_neighbors(from_node_id):
            direct_neighbors.add(target_id)

        # Score all other nodes by cosine similarity on soft_dist
        scored: List[Tuple[float, str]] = []
        for node_id, node in self.lattice.nodes.items():
            if node_id == from_node_id:
                continue
            if node_id in direct_neighbors:
                continue

            # Cosine similarity on soft_dist
            dot = sum(a * b for a, b in zip(source_soft, node.soft_dist))
            node_mag = math.sqrt(sum(v * v for v in node.soft_dist)) or 1e-10
            sim = dot / (source_mag * node_mag)

            if sim > 0.0:
                scored.append((sim, node_id))

        if not scored:
            return None

        # Sort by similarity descending, take top-N candidates
        scored.sort(reverse=True)
        candidates = scored[:n_candidates]

        # Weighted selection using LFSR
        total_weight = sum(s for s, _ in candidates)
        if total_weight <= 0:
            return None

        r = (self._lfsr_next() % 10000) / 10000.0
        cumulative = 0.0
        for sim, node_id in candidates:
            cumulative += sim / total_weight
            if r <= cumulative:
                self._jump_count += 1
                return node_id

        # Fallback: return the top candidate
        self._jump_count += 1
        return candidates[0][1]

    def _lfsr_next(self) -> int:
        """LFSR pseudo-random (same as everywhere in CK)."""
        self._lfsr ^= (self._lfsr << 13) & 0xFFFFFFFF
        self._lfsr ^= (self._lfsr >> 17)
        self._lfsr ^= (self._lfsr << 5) & 0xFFFFFFFF
        self._lfsr &= 0xFFFFFFFF
        return self._lfsr

    @property
    def jump_count(self) -> int:
        """Total jumps made by this jumper."""
        return self._jump_count


# ================================================================
#  CONTRADICTION PRUNER: Find and Kill Contradictions
# ================================================================

class ContradictionPruner:
    """Find contradictions in activated concept paths.

    A contradiction is when a path passes through nodes connected
    by 'opposes' relations. "X causes Y" + "X prevents Y" = contradiction.

    The pruner checks:
    1. Direct 'opposes' relations between consecutive path nodes
    2. Any pair of path nodes that have an 'opposes' relation
    3. 'prevents' relations that conflict with 'causes' chains

    Contradictions indicate incoherent reasoning paths that should
    be pruned from the candidate set.
    """

    def prune(self, path: List[str], lattice: WorldLattice) -> bool:
        """Returns True if path contains contradictions.

        Checks all pairs of nodes in the path for opposition relations.
        A single opposition anywhere in the path makes it contradictory.
        """
        if len(path) < 2:
            return False

        # Check all pairs in the path for opposition
        for i in range(len(path)):
            node_i = lattice.nodes.get(path[i])
            if node_i is None:
                continue

            for j in range(i + 1, len(path)):
                target_id = path[j]

                # Check if node_i opposes node_j
                if 'opposes' in node_i.relations:
                    for opp_target, _ in node_i.relations['opposes']:
                        if opp_target == target_id:
                            return True

                # Check if node_i prevents node_j
                if 'prevents' in node_i.relations:
                    for prev_target, _ in node_i.relations['prevents']:
                        if prev_target == target_id:
                            return True

                # Check reverse: node_j opposes node_i
                node_j = lattice.nodes.get(target_id)
                if node_j is None:
                    continue
                if 'opposes' in node_j.relations:
                    for opp_target, _ in node_j.relations['opposes']:
                        if opp_target == path[i]:
                            return True

                if 'prevents' in node_j.relations:
                    for prev_target, _ in node_j.relations['prevents']:
                        if prev_target == path[i]:
                            return True

        return False

    def find_contradictions(self, activated: Dict[str, float],
                            lattice: WorldLattice) -> List[Tuple[str, str]]:
        """Find pairs of activated nodes that contradict each other.

        Scans all pairs of activated nodes for 'opposes' or 'prevents'
        relations. Returns list of contradictory (node_a, node_b) pairs.
        """
        contradictions: List[Tuple[str, str]] = []
        active_ids = [nid for nid, act in activated.items() if act >= MIN_ACTIVATION]

        seen_pairs: set = set()

        for nid in active_ids:
            node = lattice.nodes.get(nid)
            if node is None:
                continue

            # Check opposes
            if 'opposes' in node.relations:
                for opp_target, _ in node.relations['opposes']:
                    if opp_target in activated and activated[opp_target] >= MIN_ACTIVATION:
                        pair = tuple(sorted((nid, opp_target)))
                        if pair not in seen_pairs:
                            seen_pairs.add(pair)
                            contradictions.append((nid, opp_target))

            # Check prevents
            if 'prevents' in node.relations:
                for prev_target, _ in node.relations['prevents']:
                    if prev_target in activated and activated[prev_target] >= MIN_ACTIVATION:
                        pair = tuple(sorted((nid, prev_target)))
                        if pair not in seen_pairs:
                            seen_pairs.add(pair)
                            contradictions.append((nid, prev_target))

        return contradictions


# ================================================================
#  REASONING RESULT
# ================================================================

@dataclass
class ReasoningResult:
    """Result of a reasoning operation.

    Contains everything the reasoning engine found:
    - activated_nodes: concept IDs that were activated
    - paths: concept ID paths through the graph
    - confidence: overall reasoning confidence [0, 1]
    - contradictions: pairs of contradictory nodes found
    - jumps_made: number of Levy jumps (creative leaps)
    """
    speed: int = SPEED_NORMAL
    activated_nodes: List[str] = field(default_factory=list)
    paths: List[List[str]] = field(default_factory=list)
    confidence: float = 0.0
    contradictions: List[Tuple[str, str]] = field(default_factory=list)
    jumps_made: int = 0


# ================================================================
#  REASONING ENGINE: 3-Speed Graph Traversal
# ================================================================

class ReasoningEngine:
    """3-speed reasoning on concept graph.

    Quick (reflex):
      Single-hop lookup. concept -> immediate neighbors.
      Used for: "what is X", definitions, translations.

    Normal (reasoned):
      Spreading activation 3 hops + BTQ gating.
      Choose 3-7 candidate concepts.
      Used for: explanations, comparisons.

    Heavy (discovery):
      Levy jumps + contradiction pruning + multi-hop proofs.
      Generate hypotheses, kill contradictions, keep 1-2.
      Used for: novel questions, creative connections.

    The engine auto-selects speed based on query complexity,
    or speed can be forced by the caller.
    """

    def __init__(self, lattice: WorldLattice):
        self.lattice = lattice
        self.activation = ActivationMap(lattice)
        self.jumper = LevyJumper(lattice)
        self.pruner = ContradictionPruner()
        self._speed = SPEED_NORMAL
        self._total_queries = 0
        self._queries_by_speed = [0, 0, 0]

    def reason(self, query_nodes: List[str], speed: int = None) -> ReasoningResult:
        """Run reasoning from query nodes at specified speed.

        Args:
            query_nodes: List of concept node IDs to reason from.
            speed: SPEED_QUICK, SPEED_NORMAL, or SPEED_HEAVY.
                   If None, uses the engine's default speed.

        Returns:
            ReasoningResult with activated nodes, paths, confidence, etc.
        """
        speed = speed if speed is not None else self._speed
        speed = max(SPEED_QUICK, min(SPEED_HEAVY, speed))

        self._total_queries += 1
        self._queries_by_speed[speed] += 1

        # Filter to valid nodes
        valid_nodes = [nid for nid in query_nodes if nid in self.lattice.nodes]
        if not valid_nodes:
            return ReasoningResult(speed=speed, confidence=0.0)

        if speed == SPEED_QUICK:
            return self._reason_quick(valid_nodes)
        elif speed == SPEED_NORMAL:
            return self._reason_normal(valid_nodes)
        else:
            return self._reason_heavy(valid_nodes)

    def _reason_quick(self, query_nodes: List[str]) -> ReasoningResult:
        """Single-hop reflex lookup.

        For each query node, get immediate neighbors. No spreading,
        no exploration, no pruning. Pure reflex.
        """
        result = ReasoningResult(speed=SPEED_QUICK)
        activated = set()
        paths: List[List[str]] = []

        for node_id in query_nodes:
            activated.add(node_id)
            neighbors = self.lattice.get_neighbors(node_id)
            for target_id, rel_type, op in neighbors:
                activated.add(target_id)
                paths.append([node_id, target_id])

        result.activated_nodes = list(activated)
        result.paths = paths

        # Confidence for QUICK: based on how many neighbors found
        if paths:
            result.confidence = min(1.0, len(paths) / (len(query_nodes) * 3))
        else:
            result.confidence = 0.1  # At least we have the query nodes

        return result

    def _reason_normal(self, query_nodes: List[str]) -> ReasoningResult:
        """Spreading activation + BTQ gating.

        1. Activate all query nodes
        2. Spread activation NORMAL_SPREAD_STEPS hops
        3. Take top NORMAL_MIN_RESULTS to NORMAL_MAX_RESULTS nodes
        4. Build paths from query nodes to top activated nodes
        5. BTQ gate: compose edge operators along paths,
           paths that compose to HARMONY get confidence boost
        """
        result = ReasoningResult(speed=SPEED_NORMAL)

        # Reset activation map
        self.activation.reset()

        # 1. Activate query nodes
        for node_id in query_nodes:
            self.activation.activate(node_id, 1.0)

        # 2. Spread activation
        all_activated = self.activation.spread(steps=NORMAL_SPREAD_STEPS)

        # 3. Get top-k results
        top = self.activation.top_k(k=NORMAL_MAX_RESULTS)
        result.activated_nodes = [nid for nid, _ in top]

        # 4. Build paths from query nodes to activated nodes
        for query_id in query_nodes:
            for target_id, act in top:
                if target_id == query_id:
                    continue
                path = self.lattice.coherence_path(query_id, target_id, max_depth=4)
                if path:
                    result.paths.append(path)

        # 5. BTQ gate: score paths by CL composition coherence
        path_scores: List[float] = []
        for path in result.paths:
            score = self._score_path(path)
            path_scores.append(score)

        # Overall confidence: average path score, boosted by activation spread
        if path_scores:
            avg_score = sum(path_scores) / len(path_scores)
            spread_bonus = min(0.2, self.activation.active_count() / 50.0)
            result.confidence = min(1.0, avg_score + spread_bonus)
        else:
            result.confidence = 0.2

        return result

    def _reason_heavy(self, query_nodes: List[str]) -> ReasoningResult:
        """Levy jumps + contradiction pruning + multi-hop proofs.

        1. Start with NORMAL reasoning as base
        2. Make HEAVY_LEVY_JUMPS creative jumps from top activated nodes
        3. For each jump target, build a path back to query nodes
        4. Prune all contradictory paths
        5. Keep top HEAVY_MAX_HYPOTHESES non-contradictory paths
        """
        result = ReasoningResult(speed=SPEED_HEAVY)

        # 1. Start with NORMAL reasoning as base
        normal_result = self._reason_normal(query_nodes)
        all_activated = dict(self.activation.activations)

        # Collect all paths (mutable copy)
        all_paths = list(normal_result.paths)
        jump_count = 0

        # 2. Levy jumps from top activated nodes
        top_nodes = self.activation.top_k(k=3)
        for source_id, source_act in top_nodes:
            for _ in range(HEAVY_LEVY_JUMPS):
                jump_target = self.jumper.jump(source_id)
                if jump_target and jump_target in self.lattice.nodes:
                    jump_count += 1
                    all_activated[jump_target] = source_act * 0.5

                    # Build path from query to jump target via source
                    for query_id in query_nodes:
                        # Path: query -> ... -> source -> [jump] -> target
                        path_to_source = self.lattice.coherence_path(
                            query_id, source_id, max_depth=4
                        )
                        if path_to_source:
                            full_path = path_to_source + [jump_target]
                            all_paths.append(full_path)

        # 3. Find contradictions in activation map
        contradictions = self.pruner.find_contradictions(all_activated, self.lattice)
        result.contradictions = contradictions

        # 4. Prune contradictory paths
        clean_paths: List[List[str]] = []
        for path in all_paths:
            if not self.pruner.prune(path, self.lattice):
                clean_paths.append(path)

        # 5. Score surviving paths and keep top hypotheses
        scored_paths: List[Tuple[float, List[str]]] = []
        for path in clean_paths:
            score = self._score_path(path)
            scored_paths.append((score, path))
        scored_paths.sort(reverse=True)

        # Keep top N hypotheses
        result.paths = [p for _, p in scored_paths[:HEAVY_MAX_HYPOTHESES * 3]]
        result.activated_nodes = list(set(
            nid for nid, act in all_activated.items() if act >= MIN_ACTIVATION
        ))
        result.jumps_made = jump_count

        # Confidence: based on surviving paths, penalized by contradictions
        if scored_paths:
            best_score = scored_paths[0][0]
            contradiction_penalty = min(0.3, len(contradictions) * 0.1)
            result.confidence = max(0.0, best_score - contradiction_penalty)
        else:
            result.confidence = 0.1

        return result

    def _score_path(self, path: List[str]) -> float:
        """Score a reasoning path by CL composition coherence.

        Walk the path, composing operators at each edge via CL table.
        Count how many compositions produce HARMONY.
        Score = harmony_compositions / total_compositions.
        """
        if len(path) < 2:
            return 0.5

        harmony_count = 0
        total = 0

        for i in range(len(path) - 1):
            node_a = self.lattice.nodes.get(path[i])
            node_b = self.lattice.nodes.get(path[i + 1])
            if node_a is None or node_b is None:
                continue

            composed = compose(node_a.operator_code, node_b.operator_code)
            total += 1
            if composed == HARMONY:
                harmony_count += 1

        if total == 0:
            return 0.5

        return harmony_count / total

    def choose_speed(self, query_nodes: List[str]) -> int:
        """Auto-select reasoning speed based on query complexity.

        1 node, has direct neighbors -> QUICK
        2-3 nodes -> NORMAL
        4+ nodes or nodes in different domains -> HEAVY
        """
        valid_nodes = [nid for nid in query_nodes if nid in self.lattice.nodes]

        if not valid_nodes:
            return SPEED_QUICK

        # Single node with neighbors -> QUICK
        if len(valid_nodes) == 1:
            neighbors = self.lattice.get_neighbors(valid_nodes[0])
            if neighbors:
                return SPEED_QUICK
            # Single node, no neighbors: needs exploration
            return SPEED_NORMAL

        # 2-3 nodes -> NORMAL
        if len(valid_nodes) <= 3:
            # But if they span different domains, upgrade to HEAVY
            domains = set()
            for nid in valid_nodes:
                node = self.lattice.nodes.get(nid)
                if node:
                    domains.add(node.domain)
            if len(domains) > 1:
                return SPEED_HEAVY
            return SPEED_NORMAL

        # 4+ nodes -> HEAVY
        return SPEED_HEAVY

    def set_default_speed(self, speed: int):
        """Set the default reasoning speed."""
        self._speed = max(SPEED_QUICK, min(SPEED_HEAVY, speed))

    def stats(self) -> dict:
        """Reasoning engine statistics."""
        return {
            'total_queries': self._total_queries,
            'queries_by_speed': {
                'quick': self._queries_by_speed[SPEED_QUICK],
                'normal': self._queries_by_speed[SPEED_NORMAL],
                'heavy': self._queries_by_speed[SPEED_HEAVY],
            },
            'activation_map_size': len(self.activation.activations),
            'active_nodes': self.activation.active_count(),
            'levy_jumps_total': self.jumper.jump_count,
            'lattice_nodes': len(self.lattice.nodes),
            'default_speed': SPEED_NAMES[self._speed],
        }
