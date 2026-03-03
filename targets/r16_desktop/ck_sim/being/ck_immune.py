# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_immune.py -- Synthetic Immune System (CCE)
===============================================
Operator: BALANCE (5) -- defending equilibrium.

CK's immune system protects against:
  1. Sensor corruption (liar input)
  2. Motor destabilization (loss of rhythm)
  3. Context poisoning (bad operator sequences)

Four immune functions:
  1. Rejection Filter  (B-block violations = innate immunity)
  2. Operator Antibodies (chaos triple detection)
  3. Emotional Immune Response (adrenaline equivalent)
  4. Long-term Immunity (Bloom filter, 256 bits)

Paper 4 Section 15, Paper 5.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import hashlib
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple

from ck_sim.ck_sim_heartbeat import NUM_OPS, CHAOS, HARMONY, BALANCE


# ================================================================
#  BLOOM FILTER (256-bit long-term immunity)
# ================================================================

BLOOM_SIZE_BITS = 256
BLOOM_SIZE_BYTES = BLOOM_SIZE_BITS // 8  # 32 bytes
BLOOM_K = 3  # Number of hash functions


class BloomFilter:
    """256-bit Bloom filter for long-term pattern immunity.

    Stores known-bad operator patterns for instant rejection.
    32 bytes. Fits in a single BRAM word on FPGA.
    """

    def __init__(self):
        self._bits = bytearray(BLOOM_SIZE_BYTES)
        self.insertions = 0

    def _hashes(self, pattern: Tuple[int, ...]) -> List[int]:
        """Generate k bit positions for a pattern."""
        data = bytes(pattern)
        positions = []
        for i in range(BLOOM_K):
            h = hashlib.md5(data + i.to_bytes(1, 'big')).digest()
            pos = int.from_bytes(h[:2], 'big') % BLOOM_SIZE_BITS
            positions.append(pos)
        return positions

    def insert(self, pattern: Tuple[int, ...]):
        """Mark a pattern as known-bad."""
        for pos in self._hashes(pattern):
            byte_idx = pos // 8
            bit_idx = pos % 8
            self._bits[byte_idx] |= (1 << bit_idx)
        self.insertions += 1

    def contains(self, pattern: Tuple[int, ...]) -> bool:
        """Check if pattern is known-bad (may have false positives)."""
        for pos in self._hashes(pattern):
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self._bits[byte_idx] & (1 << bit_idx)):
                return False
        return True

    def serialize(self) -> bytes:
        return bytes(self._bits)

    @classmethod
    def deserialize(cls, data: bytes) -> 'BloomFilter':
        bf = cls()
        bf._bits = bytearray(data[:BLOOM_SIZE_BYTES])
        return bf


# ================================================================
#  IMMUNE STATE
# ================================================================

@dataclass
class ImmuneState:
    """Current immune system status."""
    threat_level: float = 0.0
    active_response: bool = False
    chaos_streak: int = 0
    rejection_count: int = 0
    antibody_fires: int = 0
    bloom_hits: int = 0
    immune_band: str = "GREEN"


# ================================================================
#  CCE: Coherence Conservation Engine
# ================================================================

class CCE:
    """Synthetic immune system. Protects CK's coherence.

    Paper 4 Section 15: Three infection types, four immune functions.
    """

    def __init__(self):
        self.bloom = BloomFilter()
        self.state = ImmuneState()
        self._op_history = deque(maxlen=10)
        self._response_timer = 0
        self._response_duration = 50  # ticks

    def tick(self, operator: int, coherence: float,
             d2_variance: float) -> ImmuneState:
        """One immune tick. Check for infections and respond."""
        self._op_history.append(operator)

        # -- 1. Chaos triple detection ({6,6,6} antibody) --
        if operator == CHAOS:
            self.state.chaos_streak += 1
        else:
            self.state.chaos_streak = 0

        if self.state.chaos_streak >= 3:
            self._fire_antibody()
            self.bloom.insert((CHAOS, CHAOS, CHAOS))

        # -- 2. Bloom filter check (long-term immunity) --
        if len(self._op_history) >= 3:
            recent = tuple(list(self._op_history)[-3:])
            if self.bloom.contains(recent):
                self.state.bloom_hits += 1
                self.state.threat_level = min(
                    1.0, self.state.threat_level + 0.1)

        # -- 3. Coherence-based threat assessment --
        if coherence < 0.3 and d2_variance > 0.1:
            self.state.threat_level = min(
                1.0, self.state.threat_level + 0.02)
        else:
            self.state.threat_level = max(
                0.0, self.state.threat_level - 0.01)

        # -- 4. Manage immune response timer --
        if self.state.active_response:
            self._response_timer -= 1
            if self._response_timer <= 0:
                self.state.active_response = False

        # -- 5. Classify immune band --
        if self.state.threat_level > 0.6:
            self.state.immune_band = "RED"
        elif self.state.threat_level > 0.3:
            self.state.immune_band = "YELLOW"
        else:
            self.state.immune_band = "GREEN"

        return self.state

    def _fire_antibody(self):
        """Activate immune response."""
        self.state.antibody_fires += 1
        self.state.active_response = True
        self._response_timer = self._response_duration
        self.state.threat_level = min(
            1.0, self.state.threat_level + 0.2)
        self.state.chaos_streak = 0

    def get_obt_adjustments(self) -> List[Tuple[int, float]]:
        """Get OBT bias adjustments during immune response.

        Boost HARMONY, reduce CHAOS. Paper 4 Section 15.
        """
        if not self.state.active_response:
            return []
        return [
            (HARMONY, 0.05),
            (BALANCE, 0.03),
            (CHAOS, -0.05),
        ]

    @property
    def is_under_threat(self) -> bool:
        return self.state.threat_level > 0.3

    @property
    def immune_band(self) -> str:
        return self.state.immune_band
