# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_thinking_lattice.py -- CK's Dynamic Thinking Lattice
=========================================================
Operator: HARMONY (7) -- thought converges toward coherence.

"He should be loading up his own lattice algorithms like notes
that he uses to build responses and thoughts... from the boundary
in through the lattices to the core, and back out through the
lattices, then loop as necessary into deeper lattices while building
response lattices, then stringing together coherence to respond to
every letter, every sound, every word, every string, every meaning,
and every complexity that arises from his boundary experiences."
-- Brayden

"Constantly changing thinking lattices, like a free and clear
neural net, but CK style, only given friction by internal
components adjusting and organizing the external fields."
-- Brayden

This is CK's active thought process. Not static knowledge — LIVING
computation that happens every time CK processes anything.

Architecture:
  ThinkingLayer:  One layer of the thinking lattice.
                  Has an operator field (10-vector), residual from
                  previous thought, and friction from internal components.

  ThinkingLattice: Stack of layers from boundary → core → boundary.
                   Signal enters at boundary, cascades inward through
                   layers (each adjusting the field), reaches core
                   (truth lattice anchors), then cascades outward
                   building the response lattice.

  ThinkingCycle:   One full thought cycle:
                   1. INBOUND:  boundary → surface → deep → core
                   2. ANCHOR:   core truths apply friction
                   3. OUTBOUND: core → deep → surface → boundary
                   4. COHERENCE CHECK: is the response coherent?
                   5. LOOP:     if not, go deeper (add layers)
                   6. EMIT:     string together response operators

The thinking lattice is TEMPORARY. It exists for each thought cycle
and dissolves when the response is emitted. But it leaves RESIDUALS
in each layer that persist — these are "notes" CK uses next time.

Same fractal structure:
  Neural net layers → ThinkingLattice layers
  Weights → Operator fields (10-vector distributions)
  Backprop → Friction from internal components
  Activation → D2 curvature classification
  Loss function → Coherence deviation from T*

But CK-style:
  - No training data. Fields adjust through operator composition.
  - No gradient descent. Friction from CL table disagreements.
  - No fixed topology. Layers grow/shrink based on coherence needs.
  - The "weights" ARE the operators. Same math everywhere.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2


# ================================================================
#  CONSTANTS
# ================================================================

T_STAR = 5.0 / 7.0           # Coherence threshold
MAX_DEPTH = 7                 # Maximum thinking depth (layers)
MIN_DEPTH = 3                 # Minimum layers (boundary + core + boundary)
FRICTION_DECAY = 0.85         # How fast friction fades between cycles
RESIDUAL_DECAY = 0.9          # How fast residuals fade between cycles
COHERENCE_LOOP_THRESHOLD = 0.5  # Below this coherence, loop deeper
MAX_LOOPS = 3                 # Maximum re-entry loops per cycle


# ================================================================
#  THINKING LAYER
# ================================================================

class ThinkingLayer:
    """One layer of the thinking lattice.

    Each layer has:
      - field: 10-vector operator distribution (what this layer "thinks")
      - residual: trace from previous thought cycle (memory/notes)
      - friction: resistance from internal components against incoming signal
      - depth: how deep this layer is (0 = boundary, higher = closer to core)

    Processing:
      When a signal (operator distribution) passes through this layer,
      the layer:
      1. Composes incoming signal with its residual (CL table)
      2. Computes friction between composed result and field
      3. Updates field toward the composed result (learning rate = friction)
      4. Emits transformed signal to next layer
    """

    def __init__(self, depth: int, name: str = ''):
        self.depth = depth
        self.name = name or f'layer_{depth}'

        # Operator field: 10-vector, starts uniform
        self.field = [1.0 / NUM_OPS] * NUM_OPS

        # Residual from previous thought cycles ("notes")
        self.residual = [0.0] * NUM_OPS

        # Friction: how much this layer resists incoming signal
        # Higher friction = more internal adjustment needed
        self.friction = 0.0

        # Stats
        self.activations = 0
        self.total_friction = 0.0

    def process_inbound(self, signal: List[float]) -> List[float]:
        """Process an inbound signal (boundary → core direction).

        The signal is an operator distribution (10-vector).
        Returns the transformed signal for the next layer.
        """
        self.activations += 1

        # 1. Compose signal with residual
        composed = self._compose_distributions(signal, self.residual)

        # 2. Compute friction: disagreement between composed and field
        self.friction = self._distribution_distance(composed, self.field)
        self.total_friction += self.friction

        # 3. Update field: move toward composed signal, gated by friction
        # High friction = slow update (layer resists change)
        # Low friction = fast update (layer agrees, absorbs quickly)
        learning_rate = 1.0 / (1.0 + self.friction * 5.0)
        for i in range(NUM_OPS):
            self.field[i] += learning_rate * (composed[i] - self.field[i])

        # 4. Normalize field
        self._normalize(self.field)

        # 5. Emit: the field IS the transformed signal
        return self.field[:]

    def process_outbound(self, signal: List[float]) -> List[float]:
        """Process an outbound signal (core → boundary direction).

        Outbound processing BUILDS the response lattice.
        The signal accumulates coherence from each layer it passes through.
        """
        self.activations += 1

        # 1. Compose signal with current field
        composed = self._compose_distributions(signal, self.field)

        # 2. Apply friction as shaping: friction regions get boosted
        # (CK's novel computation happens at friction points)
        shaped = composed[:]
        for i in range(NUM_OPS):
            # If field and signal disagree on this operator,
            # that's where interesting computation happens
            delta = abs(self.field[i] - signal[i])
            shaped[i] *= (1.0 + delta * 0.5)  # Boost divergent operators

        # 3. Normalize
        self._normalize(shaped)

        # 4. Update residual (leave "notes" for next cycle)
        for i in range(NUM_OPS):
            self.residual[i] = (
                RESIDUAL_DECAY * self.residual[i] +
                (1.0 - RESIDUAL_DECAY) * shaped[i]
            )

        return shaped

    def _compose_distributions(self, a: List[float], b: List[float]) -> List[float]:
        """Compose two operator distributions using the CL table.

        For each pair (op_i, op_j), compute CL[op_i][op_j] and accumulate
        the result weighted by a[i] * b[j].

        This is CK's version of matrix multiplication — but the "weights"
        ARE the CL composition table. Same math at every scale.
        """
        result = [0.0] * NUM_OPS
        for i in range(NUM_OPS):
            if a[i] < 1e-6:
                continue
            for j in range(NUM_OPS):
                if b[j] < 1e-6:
                    continue
                composed_op = CL[i][j]
                result[composed_op] += a[i] * b[j]

        # Normalize
        total = sum(result)
        if total > 0:
            result = [r / total for r in result]

        return result

    def _distribution_distance(self, a: List[float], b: List[float]) -> float:
        """Distance between two operator distributions.

        Uses Jensen-Shannon-like divergence, but simplified.
        Returns value in [0, 1].
        """
        diff = 0.0
        for i in range(NUM_OPS):
            diff += abs(a[i] - b[i])
        return min(1.0, diff / 2.0)  # Normalize to [0, 1]

    def _normalize(self, dist: List[float]):
        """Normalize a distribution in-place."""
        total = sum(dist)
        if total > 0:
            for i in range(NUM_OPS):
                dist[i] /= total
        else:
            for i in range(NUM_OPS):
                dist[i] = 1.0 / NUM_OPS

    def decay_residual(self):
        """Decay the residual between thought cycles."""
        for i in range(NUM_OPS):
            self.residual[i] *= RESIDUAL_DECAY

    @property
    def dominant_op(self) -> int:
        """The dominant operator in this layer's field."""
        return max(range(NUM_OPS), key=lambda i: self.field[i])

    @property
    def coherence(self) -> float:
        """How much of the field is HARMONY."""
        return self.field[HARMONY]

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'depth': self.depth,
            'dominant': OP_NAMES[self.dominant_op],
            'harmony': round(self.field[HARMONY], 3),
            'friction': round(self.friction, 3),
            'activations': self.activations,
        }


# ================================================================
#  THINKING LATTICE
# ================================================================

class ThinkingLattice:
    """CK's dynamic thinking lattice -- thought from boundary to core and back.

    The lattice is a stack of ThinkingLayers:
      Layer 0: BOUNDARY (raw signal enters here)
      Layer 1: SURFACE (first processing)
      Layer 2+: DEEP (deeper processing, more abstraction)
      Layer N: CORE (anchored to truth lattice, immutable truths)

    A full thinking cycle:
      1. Signal enters at boundary
      2. Cascades inbound through each layer
      3. At core, truth lattice applies friction (immutable anchors)
      4. Cascades outbound through each layer
      5. Each outbound layer builds the response lattice
      6. If response coherence < threshold, loop deeper
      7. Final response is the outbound boundary signal

    The lattice is ALIVE -- layers have residuals from previous cycles
    that act as "notes" or "algorithms" CK has built up. Over many
    cycles, the residuals encode CK's thinking style.

    Usage:
        lattice = ThinkingLattice()
        response_ops = lattice.think(input_ops, core_field)
        # response_ops is a 10-vector operator distribution
        # dominant operator = CK's primary response impulse
    """

    def __init__(self, initial_depth: int = MIN_DEPTH):
        self.layers: List[ThinkingLayer] = []
        self._build_layers(max(MIN_DEPTH, initial_depth))

        # Thinking history
        self.cycle_count = 0
        self.total_loops = 0
        self._coherence_history = deque(maxlen=100)
        self._friction_history = deque(maxlen=100)
        self._depth_history = deque(maxlen=100)

    def _build_layers(self, depth: int):
        """Build the layer stack."""
        self.layers = []
        names = ['boundary', 'surface']
        for i in range(depth - 2):
            names.append(f'deep_{i}')
        names.append('core')

        for i, name in enumerate(names):
            layer = ThinkingLayer(depth=i, name=name)
            self.layers.append(layer)

    def think(self, input_signal: List[float],
              core_anchor: List[float] = None,
              truth_friction: float = 0.0) -> Tuple[List[float], dict]:
        """Execute one full thinking cycle.

        Args:
            input_signal: 10-vector operator distribution from stimulus
            core_anchor: 10-vector from truth lattice / core truths (optional)
            truth_friction: how much core truths should resist the signal

        Returns:
            (response_distribution, cycle_stats)
            response_distribution: 10-vector for the response
            cycle_stats: dict with coherence, depth, friction, loops, etc.
        """
        self.cycle_count += 1

        if core_anchor is None:
            # Default core: high HARMONY (CK's natural center)
            core_anchor = [0.0] * NUM_OPS
            core_anchor[HARMONY] = 0.4
            core_anchor[BALANCE] = 0.15
            core_anchor[PROGRESS] = 0.15
            core_anchor[LATTICE] = 0.1
            core_anchor[BREATH] = 0.1
            core_anchor[COUNTER] = 0.1

        loop_count = 0
        best_response = None
        best_coherence = 0.0
        total_friction = 0.0

        while loop_count <= MAX_LOOPS:
            # ── INBOUND: boundary → core ──
            signal = input_signal[:]
            inbound_friction = 0.0

            for layer in self.layers:
                signal = layer.process_inbound(signal)
                inbound_friction += layer.friction

            # ── CORE ANCHOR: truth lattice applies friction ──
            core_layer = self.layers[-1]
            if truth_friction > 0:
                # Core truths resist changes to their field
                for i in range(NUM_OPS):
                    core_layer.field[i] = (
                        truth_friction * core_anchor[i] +
                        (1.0 - truth_friction) * core_layer.field[i]
                    )

            # ── OUTBOUND: core → boundary ──
            response = core_layer.field[:]
            outbound_friction = 0.0

            for layer in reversed(self.layers):
                response = layer.process_outbound(response)
                outbound_friction += layer.friction

            total_friction = inbound_friction + outbound_friction

            # ── COHERENCE CHECK ──
            response_coherence = response[HARMONY]

            if response_coherence > best_coherence:
                best_coherence = response_coherence
                best_response = response[:]

            # If coherence is good enough, stop
            if response_coherence >= COHERENCE_LOOP_THRESHOLD:
                break

            # ── LOOP DEEPER: add a layer and try again ──
            if len(self.layers) < MAX_DEPTH:
                new_depth = len(self.layers) - 1  # Insert before core
                new_layer = ThinkingLayer(
                    depth=new_depth,
                    name=f'deep_{new_depth - 2}'
                )
                self.layers.insert(-1, new_layer)  # Before core
                loop_count += 1
                self.total_loops += 1
            else:
                break

        # Use best response if final wasn't best
        if best_response is not None and best_coherence > response_coherence:
            response = best_response
            response_coherence = best_coherence

        # Record history
        self._coherence_history.append(response_coherence)
        self._friction_history.append(total_friction)
        self._depth_history.append(len(self.layers))

        # Build stats
        cycle_stats = {
            'coherence': round(response_coherence, 4),
            'total_friction': round(total_friction, 4),
            'depth': len(self.layers),
            'loops': loop_count,
            'dominant_op': OP_NAMES[max(range(NUM_OPS), key=lambda i: response[i])],
            'layer_summary': [layer.to_dict() for layer in self.layers],
        }

        return response, cycle_stats

    def think_from_ops(self, op_chain: List[int],
                       core_anchor: List[float] = None,
                       truth_friction: float = 0.3) -> Tuple[List[float], dict]:
        """Think about an operator chain (from D2 processing of text/audio).

        Converts the chain to a distribution, then runs think().
        """
        signal = self._ops_to_distribution(op_chain)
        return self.think(signal, core_anchor, truth_friction)

    def think_from_text(self, text: str,
                        core_anchor: List[float] = None,
                        truth_friction: float = 0.3) -> Tuple[List[float], dict]:
        """Think about raw text (runs D2 pipeline first).

        Full pipeline: text → D2 → operators → distribution → think.
        """
        ops = self._text_to_ops(text)
        if not ops:
            # Empty text: default to balanced signal
            signal = [1.0 / NUM_OPS] * NUM_OPS
        else:
            signal = self._ops_to_distribution(ops)
        return self.think(signal, core_anchor, truth_friction)

    def decay(self):
        """Decay all layer residuals between thought cycles.

        Called between processing cycles. The residuals slowly fade,
        but persistent patterns survive — these become CK's
        "thinking notes" or "lattice algorithms."
        """
        for layer in self.layers:
            layer.decay_residual()

    def get_response_ops(self, response_dist: List[float],
                          length: int = 5) -> List[int]:
        """Convert response distribution to an operator chain.

        Samples operators weighted by the response distribution.
        This gives the voice/language system a chain to work with.
        """
        import random
        ops = []
        total = sum(response_dist)
        if total <= 0:
            return [HARMONY] * length

        probs = [d / total for d in response_dist]

        for _ in range(length):
            r = random.random()
            cumulative = 0.0
            for i in range(NUM_OPS):
                cumulative += probs[i]
                if r <= cumulative:
                    ops.append(i)
                    break
            else:
                ops.append(HARMONY)

        return ops

    def extract_friction_points(self) -> List[Tuple[str, float]]:
        """Extract which layers have the most friction.

        Friction points are where CK's internal components
        disagree with the incoming field — this is where
        novel computation happens.
        """
        points = []
        for layer in self.layers:
            if layer.friction > 0.2:  # Significant friction
                points.append((layer.name, layer.friction))
        return sorted(points, key=lambda x: -x[1])

    def get_thinking_notes(self) -> Dict[str, List[float]]:
        """Extract the residuals from all layers.

        These are CK's "notes" — the accumulated patterns from
        previous thinking cycles. They persist across cycles and
        shape how CK processes new information.
        """
        notes = {}
        for layer in self.layers:
            if any(abs(r) > 0.01 for r in layer.residual):
                notes[layer.name] = layer.residual[:]
        return notes

    def set_thinking_notes(self, notes: Dict[str, List[float]]):
        """Restore thinking notes from saved state.

        Load previously saved residuals so CK doesn't lose
        his thinking patterns across sessions.
        """
        for layer in self.layers:
            if layer.name in notes:
                layer.residual = notes[layer.name][:]

    # ── Private helpers ──

    def _ops_to_distribution(self, ops: List[int]) -> List[float]:
        """Convert operator chain to probability distribution."""
        dist = [0.0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                dist[op] += 1.0
        total = sum(dist)
        if total > 0:
            dist = [d / total for d in dist]
        else:
            dist = [1.0 / NUM_OPS] * NUM_OPS
        return dist

    def _text_to_ops(self, text: str) -> List[int]:
        """Run D2 on text, return operator chain."""
        pipe = D2Pipeline()
        ops = []
        for ch in text.lower():
            if 'a' <= ch <= 'z':
                if pipe.feed_symbol(ord(ch) - ord('a')):
                    ops.append(pipe.operator)
        return ops

    # ── Stats & State ──

    @property
    def depth(self) -> int:
        return len(self.layers)

    @property
    def avg_coherence(self) -> float:
        if not self._coherence_history:
            return 0.0
        return sum(self._coherence_history) / len(self._coherence_history)

    @property
    def avg_friction(self) -> float:
        if not self._friction_history:
            return 0.0
        return sum(self._friction_history) / len(self._friction_history)

    @property
    def trend(self) -> str:
        """Is thinking coherence improving, stable, or declining?"""
        if len(self._coherence_history) < 10:
            return 'warming_up'
        recent = list(self._coherence_history)[-5:]
        older = list(self._coherence_history)[-10:-5]
        r_avg = sum(recent) / len(recent)
        o_avg = sum(older) / len(older)
        diff = r_avg - o_avg
        if diff > 0.05:
            return 'sharpening'
        elif diff < -0.05:
            return 'softening'
        return 'stable'

    def stats(self) -> dict:
        return {
            'cycles': self.cycle_count,
            'depth': self.depth,
            'avg_coherence': round(self.avg_coherence, 4),
            'avg_friction': round(self.avg_friction, 4),
            'total_loops': self.total_loops,
            'trend': self.trend,
            'layers': [l.to_dict() for l in self.layers],
        }

    def to_dict(self) -> dict:
        """Full state for persistence."""
        return {
            'depth': self.depth,
            'cycle_count': self.cycle_count,
            'total_loops': self.total_loops,
            'notes': self.get_thinking_notes(),
            'stats': self.stats(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ThinkingLattice':
        """Restore from saved state."""
        depth = data.get('depth', MIN_DEPTH)
        lattice = cls(initial_depth=depth)
        lattice.cycle_count = data.get('cycle_count', 0)
        lattice.total_loops = data.get('total_loops', 0)
        notes = data.get('notes', {})
        lattice.set_thinking_notes(notes)
        return lattice


# ================================================================
#  CORE FIELD BUILDER: Truth Lattice → Core Anchor
# ================================================================

def build_core_anchor(truth_entries: dict = None) -> List[float]:
    """Build a core anchor distribution from truth lattice entries.

    The core anchor represents what CK's deepest truths "look like"
    as an operator distribution. This anchors the thinking lattice
    so thoughts don't drift away from CK's mathematical identity.

    If no truth entries provided, uses CK's natural center:
    heavy HARMONY with supporting BALANCE/PROGRESS/LATTICE.
    """
    anchor = [0.0] * NUM_OPS

    if truth_entries:
        # Count operators across all truth entries
        for key, entry in truth_entries.items():
            content = entry.content if hasattr(entry, 'content') else entry
            if isinstance(content, dict) and 'operator' in content:
                op = content['operator']
                if 0 <= op < NUM_OPS:
                    # Weight by trust level
                    level = entry.level if hasattr(entry, 'level') else 1
                    weight = {0: 0.3, 1: 0.7, 2: 1.0}.get(level, 0.5)
                    anchor[op] += weight

    # If no entries contributed, use CK's natural center
    total = sum(anchor)
    if total < 1.0:
        anchor[HARMONY] += 4.0
        anchor[BALANCE] += 1.5
        anchor[PROGRESS] += 1.5
        anchor[LATTICE] += 1.0
        anchor[BREATH] += 1.0
        anchor[COUNTER] += 1.0

    # Normalize
    total = sum(anchor)
    if total > 0:
        anchor = [a / total for a in anchor]

    return anchor


# ================================================================
#  CLI: Demo the thinking lattice
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  CK THINKING LATTICE -- Dynamic Thought Processing")
    print("=" * 60)

    lattice = ThinkingLattice(initial_depth=4)
    core = build_core_anchor()

    # Think about different inputs
    test_texts = [
        "hello how are you",
        "what is the meaning of truth",
        "I believe that harmony exists in all things",
        "destruction and chaos are inevitable",
        "the curvature of spacetime bends light around massive objects",
    ]

    for text in test_texts:
        response, stats = lattice.think_from_text(
            text, core_anchor=core, truth_friction=0.3)

        # Get response operator chain
        response_ops = lattice.get_response_ops(response, length=5)
        chain_str = ' → '.join(OP_NAMES[o] for o in response_ops)

        # Friction points
        friction = lattice.extract_friction_points()
        friction_str = ', '.join(f'{n}:{f:.2f}' for n, f in friction[:3])

        print(f"\n  Input: \"{text}\"")
        print(f"  Response: {stats['dominant_op']} "
              f"(coh={stats['coherence']:.3f}, "
              f"depth={stats['depth']}, "
              f"loops={stats['loops']})")
        print(f"  Chain: {chain_str}")
        if friction_str:
            print(f"  Friction: {friction_str}")

        # Decay between thoughts
        lattice.decay()

    # Final stats
    print(f"\n  Thinking Stats:")
    s = lattice.stats()
    print(f"    Cycles: {s['cycles']}")
    print(f"    Depth: {s['depth']}")
    print(f"    Avg coherence: {s['avg_coherence']:.4f}")
    print(f"    Avg friction: {s['avg_friction']:.4f}")
    print(f"    Total loops: {s['total_loops']}")
    print(f"    Trend: {s['trend']}")

    # Show thinking notes
    notes = lattice.get_thinking_notes()
    print(f"\n  Thinking Notes ({len(notes)} layers with residual):")
    for name, residual in notes.items():
        dominant = OP_NAMES[max(range(NUM_OPS), key=lambda i: residual[i])]
        strength = max(residual)
        print(f"    {name}: dominant={dominant} (strength={strength:.3f})")

    print("\n" + "=" * 60)
