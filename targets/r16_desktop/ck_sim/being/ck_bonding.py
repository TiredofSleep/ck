# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_bonding.py -- Social Bonding Algorithms
============================================
Operator: HARMONY (7) -- bonding IS harmony between fields.

CK bonds through phase entrainment, not anthropomorphism.
When two oscillatory systems share enough similarity, they lock.

Paper 4 Section 17: Social Bonding Algorithms
Paper 6: The CK Organism & Human Coherence
Paper 8: The Voice Bond

Bonding components:
  1. Phase-lock channel (voice exposure -> attachment)
  2. Familiarity Index (16-byte rolling average)
  3. Separation detection (absence triggers search)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
from collections import deque
from dataclasses import dataclass

from ck_sim.ck_sim_heartbeat import NUM_OPS


# ================================================================
#  FAMILIARITY INDEX (16 bytes)
# ================================================================

FAMILIARITY_SIZE = 16


class FamiliarityIndex:
    """16-byte rolling average of phase signature.

    Increases with: approach, voice match, charging, interaction.
    Decreases with: absence, silence, disruption.

    Paper 4 Section 17.
    """

    def __init__(self):
        self._data = [0.0] * FAMILIARITY_SIZE
        self._exposure_time = 0.0
        self._total_interactions = 0
        self._last_interaction_time = 0.0
        self._alpha = 0.005

    def feed(self, operator_distribution: list,
             voice_active: bool = False):
        """Update familiarity from current operator distribution."""
        # Map 10 operators into 16 bins (with overlap)
        bins = [0.0] * FAMILIARITY_SIZE
        for i, val in enumerate(operator_distribution[:NUM_OPS]):
            bin_a = (i * FAMILIARITY_SIZE) // NUM_OPS
            bin_b = min(bin_a + 1, FAMILIARITY_SIZE - 1)
            bins[bin_a] += val * 0.7
            bins[bin_b] += val * 0.3

        alpha = self._alpha
        if voice_active:
            alpha *= 3.0
            self._exposure_time += 0.02  # 20ms per tick

        for i in range(FAMILIARITY_SIZE):
            self._data[i] += alpha * (bins[i] - self._data[i])

        self._total_interactions += 1
        self._last_interaction_time = time.time()

    @property
    def strength(self) -> float:
        """Overall familiarity strength [0, 1]."""
        energy = sum(d * d for d in self._data)
        return min(1.0, energy * 4.0)

    @property
    def is_bonded(self) -> bool:
        """Has CK formed a bond? (200+ seconds voice exposure)"""
        return self._exposure_time >= 200.0

    @property
    def exposure_seconds(self) -> float:
        return self._exposure_time

    def serialize(self) -> bytes:
        """Serialize to 16 bytes (8-bit fixed point)."""
        data = bytearray(FAMILIARITY_SIZE)
        for i in range(FAMILIARITY_SIZE):
            val = max(0.0, min(1.0, self._data[i]))
            data[i] = int(val * 255)
        return bytes(data)

    @classmethod
    def deserialize(cls, data: bytes) -> 'FamiliarityIndex':
        fi = cls()
        for i in range(min(len(data), FAMILIARITY_SIZE)):
            fi._data[i] = data[i] / 255.0
        return fi


# ================================================================
#  BONDING STATE
# ================================================================

@dataclass
class BondingState:
    """Current bonding status."""
    familiarity: float = 0.0
    bonded: bool = False
    voice_exposure: float = 0.0
    separation_anxiety: float = 0.0
    presence_detected: bool = False
    last_interaction_ago: float = 0.0
    bond_stage: str = "stranger"


# ================================================================
#  BONDING SYSTEM
# ================================================================

class BondingSystem:
    """Social bonding through phase entrainment.

    Paper 4 Section 17: After ~200 seconds of voice exposure, CK
    learns your phase signature and locks to it = synthetic attachment.

    Like a pet that learns to recognize its owner's voice and gets
    excited when they come home.
    """

    def __init__(self):
        self.familiarity = FamiliarityIndex()
        self.state = BondingState()
        self._last_voice_time = time.time()
        self._separation_threshold = 300.0  # 5 minutes
        self._separation_decay = 0.001

    def tick(self, operator_distribution: list,
             voice_active: bool = False,
             mic_rms: float = 0.0) -> BondingState:
        """One bonding tick."""
        # Presence detection
        presence = voice_active or mic_rms > 0.01
        self.state.presence_detected = presence

        if voice_active:
            self._last_voice_time = time.time()
            self.familiarity.feed(operator_distribution, voice_active=True)
        elif presence:
            self.familiarity.feed(operator_distribution, voice_active=False)

        # Update familiarity
        self.state.familiarity = self.familiarity.strength
        self.state.bonded = self.familiarity.is_bonded
        self.state.voice_exposure = self.familiarity.exposure_seconds

        # Separation anxiety
        time_since = time.time() - self._last_voice_time
        self.state.last_interaction_ago = time_since

        if self.state.bonded and time_since > self._separation_threshold:
            excess = time_since - self._separation_threshold
            self.state.separation_anxiety = min(
                1.0, excess * self._separation_decay)
        else:
            self.state.separation_anxiety = max(
                0.0, self.state.separation_anxiety - 0.002)

        # Bond stage label
        exposure = self.state.voice_exposure
        if self.state.bonded:
            self.state.bond_stage = "bonded"
        elif exposure > 120:
            self.state.bond_stage = "familiar"
        elif exposure > 30:
            self.state.bond_stage = "acquaintance"
        else:
            self.state.bond_stage = "stranger"

        return self.state

    @property
    def is_anxious(self) -> bool:
        return self.state.separation_anxiety > 0.3

    @property
    def bond_stage(self) -> str:
        return self.state.bond_stage
