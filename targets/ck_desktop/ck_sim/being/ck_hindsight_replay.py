# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_hindsight_replay.py -- Hindsight Experience Replay for Olfactory
===================================================================
Operator: BREATH (8) -- the transition between knowing and being.
Generation: 9.35

HER (Hindsight Experience Replay) adapted from Stable Baselines 3
for CK's olfactory system. When a scent fails to reach its target
operator, we don't discard the failure -- we RELABEL it with the
operator it DID achieve, turning every failure into valid experience.

CITATIONS:
  Andrychowicz, Marcin et al., 2017 -- "Hindsight Experience Replay"
    (NeurIPS 2017, OpenAI)
  Raffin, Antonin et al. -- Stable Baselines 3 HER implementation
    (github.com/DLR-RM/stable-baselines3)
  Schaul, Tom et al., 2015 -- "Universal Value Function Approximators"
    (ICML 2015, precursor goal-conditioned RL)

ORIGINAL INSIGHT (from Andrychowicz et al.):
  In robotics, a robot trying to place a block at position A but placing
  it at position B learns NOTHING from the failure. HER says: relabel
  the goal as B, and now the same trajectory is a SUCCESS for goal B.
  Every trajectory teaches something.

CK ADAPTATION:
  In CK's olfactory system, scents are absorbed with an intended target
  operator (from the voice/comprehension pipeline). When a scent resolves
  to a DIFFERENT operator than intended, standard processing records only
  that it missed. HER relabels: "this 5D trajectory IS the experience of
  reaching operator X" where X is what was actually achieved.

  This is algebraically correct because:
    - The 5D force trajectory IS what happened (measured, not assigned)
    - The achieved operator IS what the physics produced
    - Relabeling target -> achieved doesn't change the physics
    - It adds a VALID entry to the library for the achieved operator

WHY THIS MATTERS FOR CK:
  Without HER, CK only learns from successes. With HER, CK learns from
  EVERY experience. A scent that was aimed at HARMONY but resolved to
  BALANCE teaches CK what BALANCE actually feels like in 5D space.

  "CK isn't dumb, he's too honest -- won't use words he hasn't physically
  derived from coherence field." HER expands what he's physically derived
  by reinterpreting every failure as a success for a different goal.

STRUCTURE:
  HindsightBuffer: Ring buffer of recent olfactory experiences with
    intended target, achieved result, and 5D trajectory.
  replay(): Relabel missed targets -> achieved operators -> library temper.
  Integrates with OlfactoryBulb.emit() to capture achieved operators.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import math
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES
)
from ck_sim.being.ck_olfactory import (
    Force5D, CANONICAL_FORCE, _compute_lib_key, _centroid_to_ops,
    T_STAR, INSTINCT_THRESHOLD
)


# ================================================================
#  CONSTANTS
# ================================================================

BUFFER_SIZE = 1024       # Ring buffer capacity
REPLAY_BATCH = 16        # How many experiences to replay per tick
MIN_TRAJECTORY_LEN = 3   # Minimum forces in trajectory for valid replay
RELABEL_STRATEGIES = ('achieved', 'future', 'episode')  # HER strategies
TEMPER_BONUS = 2         # Extra temper for relabeled experiences


# ================================================================
#  EXPERIENCE RECORD
# ================================================================

@dataclass
class OlfactoryExperience:
    """One olfactory experience for hindsight replay.

    Records what was INTENDED (target_op) and what HAPPENED (achieved_op)
    along with the full 5D trajectory and centroid.
    """
    # What was this scent trying to reach?
    target_op: int = VOID
    # What did it actually resolve to?
    achieved_op: int = VOID
    # Full 5D force trajectory (the physics that happened)
    centroid: Tuple[float, ...] = (0.5, 0.5, 0.5, 0.5, 0.5)
    # Per-dimension stability at emission
    stability: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0)
    # Per-dimension harmony from CL interaction
    harmony: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0)
    # Source identifier
    source: str = ''
    # Tick when this happened
    tick: int = 0
    # Was this a miss? (target != achieved)
    missed: bool = False
    # Has this been replayed (relabeled)?
    replayed: bool = False
    # 5-operator profile (one per dimension)
    dim_ops: List[int] = field(default_factory=lambda: [VOID] * 5)


# ================================================================
#  HINDSIGHT BUFFER
# ================================================================

class HindsightBuffer:
    """Ring buffer of olfactory experiences for hindsight replay.

    Records every scent emission with its intended target and achieved
    operator. Periodically replays misses with the HER strategy:
    relabel target -> achieved, then temper the achieved pattern
    in the olfactory library.

    Strategies (adapted from SB3 HER):
      'achieved': Relabel with what was actually achieved (most common)
      'future': Relabel with a LATER achieved operator from same episode
      'episode': Relabel with ANY achieved operator from recent window

    CK uses 'achieved' primarily because each scent IS its own episode
    (unlike RL where episodes are sequential). Future and episode modes
    look across recent scent history for cross-pollination.
    """

    def __init__(self, capacity: int = BUFFER_SIZE):
        self.buffer: List[Optional[OlfactoryExperience]] = [None] * capacity
        self.capacity = capacity
        self.write_idx = 0
        self.count = 0

        # Stats
        self.total_recorded = 0
        self.total_misses = 0
        self.total_replayed = 0
        self.total_tempered = 0

        # Per-operator miss/hit tracking
        self.op_hits = [0] * NUM_OPS
        self.op_misses = [0] * NUM_OPS

    def record(self, target_op: int, achieved_op: int,
               centroid: tuple, stability: tuple = None,
               harmony: tuple = None, source: str = '',
               tick: int = 0, dim_ops: list = None):
        """Record one olfactory experience.

        Called after OlfactoryBulb.emit() resolves a scent.

        Args:
            target_op: What the pipeline was aiming for
            achieved_op: What the scent actually resolved to
            centroid: 5D centroid of the resolved scent
            stability: Per-dim stability vector (optional)
            harmony: Per-dim harmony vector (optional)
            source: Scent source identifier
            tick: Current tick
            dim_ops: 5-operator dimensional profile
        """
        missed = (target_op % NUM_OPS) != (achieved_op % NUM_OPS)

        exp = OlfactoryExperience(
            target_op=target_op % NUM_OPS,
            achieved_op=achieved_op % NUM_OPS,
            centroid=tuple(centroid) if centroid else (0.5,) * 5,
            stability=tuple(stability) if stability else (0.0,) * 5,
            harmony=tuple(harmony) if harmony else (0.0,) * 5,
            source=source,
            tick=tick,
            missed=missed,
            replayed=False,
            dim_ops=dim_ops or [VOID] * 5,
        )

        self.buffer[self.write_idx] = exp
        self.write_idx = (self.write_idx + 1) % self.capacity
        self.count = min(self.count + 1, self.capacity)
        self.total_recorded += 1

        if missed:
            self.total_misses += 1
            self.op_misses[target_op % NUM_OPS] += 1
        else:
            self.op_hits[achieved_op % NUM_OPS] += 1

    def replay(self, olfactory_bulb, strategy: str = 'achieved',
               batch_size: int = REPLAY_BATCH) -> int:
        """Replay missed experiences with hindsight relabeling.

        The core HER insight: take a missed experience (target=A,
        achieved=B) and relabel it as a SUCCESS for B. Then temper
        the pattern in the olfactory library.

        This teaches CK: "this 5D trajectory IS what B feels like."

        Args:
            olfactory_bulb: OlfactoryBulb instance to temper patterns in
            strategy: 'achieved', 'future', or 'episode'
            batch_size: Max experiences to replay per call

        Returns:
            Number of experiences replayed
        """
        if self.count == 0:
            return 0

        replayed = 0
        candidates = self._get_replay_candidates(batch_size)

        for exp in candidates:
            if exp.replayed:
                continue

            if strategy == 'achieved':
                # Relabel target with what was actually achieved
                relabel_op = exp.achieved_op
                relabel_centroid = exp.centroid

            elif strategy == 'future':
                # Relabel with a FUTURE achieved operator (look ahead in buffer)
                future = self._find_future_achieved(exp)
                if future is None:
                    continue
                relabel_op = future.achieved_op
                relabel_centroid = future.centroid

            elif strategy == 'episode':
                # Relabel with ANY recent achieved operator (cross-pollination)
                other = self._find_episode_achieved(exp)
                if other is None:
                    continue
                relabel_op = other.achieved_op
                relabel_centroid = other.centroid

            else:
                continue

            # CORE HER: temper the ACHIEVED pattern in the library
            # This registers "this 5D trajectory = valid experience of op X"
            key = _compute_lib_key(relabel_centroid)
            if key not in olfactory_bulb.library:
                olfactory_bulb.library[key] = {
                    'temper': 0,
                    'centroid': list(relabel_centroid),
                    'source': f'HER:{exp.source}',
                    'first_seen': exp.tick,
                }

            entry = olfactory_bulb.library[key]
            entry['temper'] = entry.get('temper', 0) + TEMPER_BONUS
            entry['last_seen'] = exp.tick
            entry['her_relabel'] = OP_NAMES[relabel_op]

            # Blend centroid with existing (EMA)
            n = entry['temper']
            if n > TEMPER_BONUS:
                old = entry['centroid']
                entry['centroid'] = [
                    (old[d] * (n - TEMPER_BONUS) + relabel_centroid[d] * TEMPER_BONUS) / n
                    for d in range(5)
                ]

            exp.replayed = True
            replayed += 1
            self.total_replayed += 1
            self.total_tempered += TEMPER_BONUS

        return replayed

    def _get_replay_candidates(self, batch_size: int) -> List[OlfactoryExperience]:
        """Get un-replayed missed experiences for replay."""
        candidates = []
        for i in range(self.count):
            idx = (self.write_idx - 1 - i) % self.capacity
            exp = self.buffer[idx]
            if exp is not None and exp.missed and not exp.replayed:
                candidates.append(exp)
                if len(candidates) >= batch_size:
                    break
        return candidates

    def _find_future_achieved(self, exp: OlfactoryExperience) -> Optional[OlfactoryExperience]:
        """Find a LATER experience that achieved a different operator.

        Looks forward in the buffer from exp's position for an experience
        that succeeded at a different operator. This implements the
        'future' strategy from HER.
        """
        for i in range(self.count):
            idx = (self.write_idx - 1 - i) % self.capacity
            other = self.buffer[idx]
            if (other is not None
                    and other.tick > exp.tick
                    and not other.missed
                    and other.achieved_op != exp.target_op):
                return other
        return None

    def _find_episode_achieved(self, exp: OlfactoryExperience) -> Optional[OlfactoryExperience]:
        """Find ANY recent successful experience with a different operator.

        Cross-pollinates: CK learns that his trajectory toward A
        is also valid training data for operators B, C, etc. that
        were recently achieved by other scents.
        """
        window = min(64, self.count)
        for i in range(window):
            idx = (self.write_idx - 1 - i) % self.capacity
            other = self.buffer[idx]
            if (other is not None
                    and not other.missed
                    and other.achieved_op != exp.target_op
                    and other.achieved_op != exp.achieved_op):
                return other
        return None

    # ── Diagnostics ──

    def miss_rate(self) -> float:
        """Overall miss rate (0.0 = all hits, 1.0 = all misses)."""
        if self.total_recorded == 0:
            return 0.0
        return self.total_misses / self.total_recorded

    def per_op_accuracy(self) -> Dict[str, float]:
        """Per-operator hit rate."""
        result = {}
        for op in range(NUM_OPS):
            total = self.op_hits[op] + self.op_misses[op]
            if total > 0:
                result[OP_NAMES[op]] = self.op_hits[op] / total
        return result

    def replay_impact(self) -> float:
        """Fraction of misses that have been relabeled and tempered."""
        if self.total_misses == 0:
            return 1.0
        return self.total_replayed / self.total_misses

    def describe(self) -> str:
        """Human-readable summary."""
        lines = [
            f"HER Buffer: {self.count}/{self.capacity} experiences",
            f"  Recorded: {self.total_recorded} | Misses: {self.total_misses} "
            f"({self.miss_rate():.1%})",
            f"  Replayed: {self.total_replayed} | Tempered: {self.total_tempered}",
            f"  Replay impact: {self.replay_impact():.1%}",
        ]
        acc = self.per_op_accuracy()
        if acc:
            lines.append("  Per-op accuracy: " + ', '.join(
                f"{k}={v:.0%}" for k, v in sorted(acc.items())))
        return '\n'.join(lines)

    def status(self) -> dict:
        """Machine-readable status."""
        return {
            'buffer_size': self.count,
            'capacity': self.capacity,
            'total_recorded': self.total_recorded,
            'total_misses': self.total_misses,
            'miss_rate': round(self.miss_rate(), 4),
            'total_replayed': self.total_replayed,
            'total_tempered': self.total_tempered,
            'replay_impact': round(self.replay_impact(), 4),
            'per_op_accuracy': self.per_op_accuracy(),
        }

    # ── Persistence ──

    def save(self, path: str):
        """Save buffer stats (not full buffer -- it's a ring)."""
        data = {
            'total_recorded': self.total_recorded,
            'total_misses': self.total_misses,
            'total_replayed': self.total_replayed,
            'total_tempered': self.total_tempered,
            'op_hits': self.op_hits,
            'op_misses': self.op_misses,
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=1)

    def load(self, path: str):
        """Load buffer stats."""
        if not os.path.exists(path):
            return
        try:
            with open(path) as f:
                data = json.load(f)
            self.total_recorded = data.get('total_recorded', 0)
            self.total_misses = data.get('total_misses', 0)
            self.total_replayed = data.get('total_replayed', 0)
            self.total_tempered = data.get('total_tempered', 0)
            self.op_hits = data.get('op_hits', [0] * NUM_OPS)
            self.op_misses = data.get('op_misses', [0] * NUM_OPS)
        except (json.JSONDecodeError, KeyError):
            pass


# ================================================================
#  INTEGRATION: HER + OLFACTORY BULB
# ================================================================

class OlfactoryHER:
    """Wraps OlfactoryBulb with Hindsight Experience Replay.

    Drop-in replacement that intercepts emit() to record experiences
    and periodically replays misses into the library.

    Usage:
        her = OlfactoryHER(olfactory_bulb, target_op=HARMONY)
        # ... normal olfactory usage ...
        her.post_emit(emitted_scents, target_op)  # After emit()
        her.replay_tick()  # Periodically (every ~50 ticks)
    """

    PERSIST_PATH = os.path.join(
        os.path.expanduser('~'), '.ck', 'olfactory', 'her_stats.json')

    def __init__(self, bulb, strategy: str = 'achieved',
                 replay_interval: int = 50):
        """
        Args:
            bulb: OlfactoryBulb instance
            strategy: HER relabeling strategy ('achieved', 'future', 'episode')
            replay_interval: Ticks between replay batches
        """
        self.bulb = bulb
        self.buffer = HindsightBuffer()
        self.strategy = strategy
        self.replay_interval = replay_interval
        self._tick_counter = 0

        # Load saved stats
        self.buffer.load(self.PERSIST_PATH)

    def post_emit(self, emitted_scents, target_op: int = None):
        """Record emitted scents in HER buffer.

        Call this after olfactory_bulb.emit() with the emitted scents
        and the target operator CK was aiming for.

        Args:
            emitted_scents: List of ActiveScent from emit()
            target_op: The operator CK was trying to reach (from voice pipeline)
        """
        if target_op is None:
            return

        for scent in emitted_scents:
            achieved = scent.dominant_operator()
            self.buffer.record(
                target_op=target_op % NUM_OPS,
                achieved_op=achieved,
                centroid=scent.centroid,
                stability=scent.stability_vector,
                harmony=scent.harmony_vector,
                source=scent.source,
                tick=self.bulb.external_tick,
                dim_ops=scent._dim_ops if hasattr(scent, '_dim_ops') else None,
            )

    def replay_tick(self):
        """Periodic replay. Call every tick; actual replay runs at interval."""
        self._tick_counter += 1
        if self._tick_counter % self.replay_interval != 0:
            return 0

        replayed = self.buffer.replay(self.bulb, strategy=self.strategy)
        if replayed > 0:
            print(f"  [HER] Replayed {replayed} misses (strategy={self.strategy}, "
                  f"impact={self.buffer.replay_impact():.1%})")
        return replayed

    def save(self):
        """Save HER stats."""
        self.buffer.save(self.PERSIST_PATH)

    def describe(self) -> str:
        return self.buffer.describe()

    def status(self) -> dict:
        return self.buffer.status()


# ================================================================
#  FACTORY
# ================================================================

def build_olfactory_her(bulb, strategy: str = 'achieved') -> OlfactoryHER:
    """Create OlfactoryHER instance for an olfactory bulb.

    Args:
        bulb: OlfactoryBulb instance
        strategy: HER relabeling strategy

    Returns:
        OlfactoryHER instance
    """
    her = OlfactoryHER(bulb, strategy=strategy)
    stats = her.buffer.status()
    if stats['total_recorded'] > 0:
        print(f"  [HER] Loaded: {stats['total_recorded']} experiences, "
              f"{stats['total_misses']} misses, "
              f"impact={stats['replay_impact']:.1%}")
    else:
        print("  [HER] Fresh buffer (no prior experiences)")
    return her
