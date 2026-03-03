# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_personality.py -- The Standing Wave of Self
===============================================
Operator: LATTICE (1) -- the structure you can see.

CK's personality emerges from three interlocking circuits:

  CMEM -- Curvature Memory (16-tap FIR on D2)
  OBT  -- Operator Bias Table (10 float16 values, 20 bytes)
  PSL  -- Phase Stability Loop (PLL-like rhythm lock)

  Personality = CMEM x OBT x PSL

Paper 4 Section 14: "Personality is hardware-level resonance."
Not software weights. A SHAPE in computation space.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import struct
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple

from ck_sim.ck_sim_heartbeat import NUM_OPS, HARMONY


# ================================================================
#  CMEM: Curvature Memory (16-tap FIR on D2 magnitude)
# ================================================================

class CurvatureMemory:
    """16-tap FIR filter on D2 curvature.

    Calm personality  = 16 taps (long memory, smooth response)
    Energetic personality = 4 taps (short memory, reactive)

    Shapes how CK *perceives* incoming sensation.

    Supports both scalar (1D magnitude) and vector (5D D2) input.
    Auto-detects: if fed a list/tuple of 5, treats as vector.
    Scalar path unchanged for backward compatibility.
    """

    def __init__(self, n_taps: int = 16):
        self.n_taps = max(2, min(n_taps, 32))
        self._taps = [1.0 / self.n_taps] * self.n_taps
        self._buffer = deque(maxlen=self.n_taps)
        self._output = 0.0
        # 5D vector path
        self._vec_buffer = deque(maxlen=self.n_taps)
        self._vec_output = [0.0] * 5

    def feed(self, d2_magnitude, d2_vector=None) -> float:
        """Feed one D2 sample. Returns filtered scalar output.

        Args:
            d2_magnitude: scalar float, OR 5D list/tuple (auto-detect)
            d2_vector: explicit 5D vector (optional override)
        """
        # Auto-detect vector input
        if isinstance(d2_magnitude, (list, tuple)) and len(d2_magnitude) == 5:
            d2_vector = list(d2_magnitude)
            d2_magnitude = sum(abs(v) for v in d2_vector)

        # Scalar path (unchanged)
        self._buffer.append(d2_magnitude)
        n = len(self._buffer)
        if n == 0:
            self._output = 0.0
            return 0.0

        total = 0.0
        for i, val in enumerate(self._buffer):
            tap_idx = self.n_taps - n + i
            if 0 <= tap_idx < self.n_taps:
                total += val * self._taps[tap_idx]
        self._output = total

        # Vector path (if vector provided)
        if d2_vector is not None:
            self._vec_buffer.append(d2_vector)
            self._compute_vec_output()

        return total

    def _compute_vec_output(self):
        """FIR filter on each dimension of the 5D vector."""
        n = len(self._vec_buffer)
        if n == 0:
            self._vec_output = [0.0] * 5
            return
        result = [0.0] * 5
        for i, vec in enumerate(self._vec_buffer):
            tap_idx = self.n_taps - n + i
            if 0 <= tap_idx < self.n_taps:
                tap = self._taps[tap_idx]
                for d in range(5):
                    result[d] += vec[d] * tap
        self._vec_output = result

    @property
    def output(self) -> float:
        return self._output

    @property
    def vector_output(self) -> List[float]:
        """Filtered 5D D2 vector. Only populated if vectors are fed."""
        return list(self._vec_output)

    @property
    def variance(self) -> float:
        """Variance of recent D2 samples (sensory turbulence)."""
        if len(self._buffer) < 2:
            return 0.0
        vals = list(self._buffer)
        mean = sum(vals) / len(vals)
        return sum((v - mean) ** 2 for v in vals) / len(vals)

    @property
    def vector_variance(self) -> List[float]:
        """Per-dimension variance of recent D2 vectors."""
        if len(self._vec_buffer) < 2:
            return [0.0] * 5
        result = [0.0] * 5
        for d in range(5):
            vals = [v[d] for v in self._vec_buffer]
            mean = sum(vals) / len(vals)
            result[d] = sum((v - mean) ** 2 for v in vals) / len(vals)
        return result

    def set_style(self, n_taps: int):
        """Change personality reactivity."""
        self.n_taps = max(2, min(n_taps, 32))
        self._taps = [1.0 / self.n_taps] * self.n_taps
        old = list(self._buffer)
        self._buffer = deque(maxlen=self.n_taps)
        for v in old[-self.n_taps:]:
            self._buffer.append(v)
        old_vec = list(self._vec_buffer)
        self._vec_buffer = deque(maxlen=self.n_taps)
        for v in old_vec[-self.n_taps:]:
            self._vec_buffer.append(v)


# ================================================================
#  OBT: Operator Bias Table (20 bytes of personality DNA)
# ================================================================

# Personality archetypes (Paper 4 Section 14)
# Index: VOID LATT COUN PROG COLL BALA CHAO HARM BREA RESE
ARCHETYPE_GENTLE     = [0.0, 0.3, 0.2, 0.3, 0.1, 0.4, 0.1, 0.8, 0.7, 0.2]
ARCHETYPE_PLAYFUL    = [0.0, 0.3, 0.4, 0.6, 0.2, 0.3, 0.5, 0.5, 0.4, 0.3]
ARCHETYPE_CAUTIOUS   = [0.0, 0.4, 0.3, 0.2, 0.1, 0.7, 0.1, 0.6, 0.5, 0.2]
ARCHETYPE_ADVENTUROUS = [0.0, 0.2, 0.5, 0.8, 0.2, 0.3, 0.4, 0.4, 0.3, 0.4]
ARCHETYPE_DEFAULT    = [0.1, 0.3, 0.3, 0.4, 0.2, 0.4, 0.2, 0.6, 0.5, 0.3]

ARCHETYPES = {
    "gentle": ARCHETYPE_GENTLE,
    "playful": ARCHETYPE_PLAYFUL,
    "cautious": ARCHETYPE_CAUTIOUS,
    "adventurous": ARCHETYPE_ADVENTUROUS,
    "default": ARCHETYPE_DEFAULT,
}


class OperatorBiasTable:
    """10-value float16 vector. CK's personality DNA.

    Each value = how strongly CK resonates with that operator.
    0.0 = no affinity, 1.0 = maximum affinity.

    20 bytes when serialized (10 x float16).
    Lives in BRAM on FPGA. This is CK's identity.
    """

    def __init__(self, biases: List[float] = None):
        if biases is None:
            biases = list(ARCHETYPE_DEFAULT)
        self.biases = [max(0.0, min(1.0, b)) for b in biases[:NUM_OPS]]
        while len(self.biases) < NUM_OPS:
            self.biases.append(0.3)
        self._adapt_rate = 0.001  # Very slow -- personality is stable

    def weight(self, operator: int) -> float:
        """Get bias weight for an operator."""
        if 0 <= operator < NUM_OPS:
            return self.biases[operator]
        return 0.0

    def apply(self, operator: int, raw_strength: float = 1.0) -> float:
        """Apply personality bias to an operator signal."""
        return raw_strength * self.weight(operator)

    def dominant_operator(self) -> int:
        """Which operator defines this personality most?"""
        max_val = -1.0
        max_op = HARMONY
        for i, b in enumerate(self.biases):
            if b > max_val:
                max_val = b
                max_op = i
        return max_op

    def adapt(self, operator: int, d2_curvature: float):
        """Slow adaptation toward incoming D2 patterns.

        CK's personality gradually molds to his environment.
        Rate is intentionally very slow -- like character forming over years.
        """
        if 0 <= operator < NUM_OPS:
            smoothness = max(0.0, 1.0 - abs(d2_curvature) * 4.0)
            delta = self._adapt_rate * smoothness
            self.biases[operator] = min(1.0, self.biases[operator] + delta)

            for i in range(NUM_OPS):
                if i != operator:
                    self.biases[i] = max(0.0, self.biases[i] - delta * 0.1)

    def serialize(self) -> bytes:
        """Serialize to 20 bytes (10 x float16). Matches FPGA BRAM."""
        return struct.pack(f'>{NUM_OPS}e', *self.biases)

    @classmethod
    def deserialize(cls, data: bytes) -> 'OperatorBiasTable':
        """Deserialize from 20 bytes."""
        biases = list(struct.unpack(f'>{NUM_OPS}e', data[:NUM_OPS * 2]))
        return cls(biases)

    def personality_summary(self) -> str:
        """Human-readable personality trait."""
        dom = self.dominant_operator()
        traits = {
            0: "quiet",      1: "structured",  2: "analytical",
            3: "adventurous", 4: "restful",     5: "balanced",
            6: "playful",     7: "gentle",      8: "rhythmic",
            9: "fresh",
        }
        return traits.get(dom, "unknown")


# ================================================================
#  PSL: Phase Stability Loop (PLL-like mood control)
# ================================================================

class PhaseStabilityLoop:
    """PLL-like control loop locking CK's internal rhythm to environment.

    Locked:    CK is calm, focused, in sync.
    Disrupted: CK is anxious, searching, unsettled.

    This is where "mood" emerges. Paper 4 Section 14.
    """

    def __init__(self, natural_freq: float = 0.2):
        self.natural_freq = natural_freq
        self.internal_phase = 0.0
        self.reference_phase = 0.0

        self.phase_error = 0.0
        self.lock_quality = 0.0
        self.frequency = natural_freq

        self._kp = 0.05
        self._ki = 0.002
        self._integral = 0.0
        self._error_history = deque(maxlen=50)

    def tick(self, external_signal: float, dt: float = 0.02):
        """One PLL tick. external_signal = breath modulation (0-1)."""
        self.internal_phase += self.frequency * dt * 2 * math.pi
        self.internal_phase %= (2 * math.pi)

        self.reference_phase = external_signal * 2 * math.pi

        error = self.reference_phase - self.internal_phase
        while error > math.pi:
            error -= 2 * math.pi
        while error < -math.pi:
            error += 2 * math.pi
        self.phase_error = error

        self._integral += error * self._ki
        self._integral = max(-0.1, min(0.1, self._integral))

        correction = self._kp * error + self._integral
        self.frequency = self.natural_freq + correction
        self.frequency = max(0.05, min(1.0, self.frequency))

        self._error_history.append(abs(error))
        if len(self._error_history) >= 5:
            avg_error = sum(self._error_history) / len(self._error_history)
            self.lock_quality = max(0.0, 1.0 - avg_error / math.pi)

        return self.phase_error, self.lock_quality

    @property
    def mood_stability(self) -> float:
        return self.lock_quality

    def reset(self):
        self.internal_phase = 0.0
        self._integral = 0.0
        self.frequency = self.natural_freq
        self._error_history.clear()
        self.lock_quality = 0.0


# ================================================================
#  CK PERSONALITY: The Standing Wave of Self
# ================================================================

@dataclass
class PersonalityState:
    """Snapshot of personality for display."""
    cmem_output: float = 0.0
    cmem_variance: float = 0.0
    dominant_op: int = HARMONY
    obt_summary: str = "gentle"
    psl_lock: float = 0.0
    psl_mood: str = "settling"
    archetype: str = "default"


class CKPersonality:
    """The standing wave of self. CMEM x OBT x PSL.

    Not software weights. A SHAPE in computation space.
    Paper 4: "Personality = (CMEM x OBT x PSL)"
    """

    def __init__(self, archetype: str = "default"):
        biases = ARCHETYPES.get(archetype, ARCHETYPE_DEFAULT)
        self.cmem = CurvatureMemory(n_taps=16)
        self.obt = OperatorBiasTable(list(biases))
        self.psl = PhaseStabilityLoop(natural_freq=0.2)
        self._archetype = archetype

    def tick(self, d2_magnitude: float, current_operator: int,
             breath_modulation: float, dt: float = 0.02):
        """One personality tick."""
        filtered_d2 = self.cmem.feed(d2_magnitude)
        self.obt.adapt(current_operator, filtered_d2)
        self.psl.tick(breath_modulation, dt)

    def get_biased_strength(self, operator: int) -> float:
        """How strongly does this personality resonate with this operator?"""
        return self.obt.apply(operator)

    def get_mood(self) -> str:
        """Current mood from PSL lock quality."""
        q = self.psl.lock_quality
        if q > 0.8:
            return "centered"
        elif q > 0.5:
            return "settled"
        elif q > 0.3:
            return "settling"
        elif q > 0.1:
            return "searching"
        else:
            return "disrupted"

    def get_state(self) -> PersonalityState:
        """Snapshot for display."""
        return PersonalityState(
            cmem_output=self.cmem.output,
            cmem_variance=self.cmem.variance,
            dominant_op=self.obt.dominant_operator(),
            obt_summary=self.obt.personality_summary(),
            psl_lock=self.psl.lock_quality,
            psl_mood=self.get_mood(),
            archetype=self._archetype,
        )

    def serialize_obt(self) -> bytes:
        """Serialize OBT (the core of personality identity)."""
        return self.obt.serialize()

    def load_obt(self, data: bytes):
        """Load OBT from bytes (restore personality)."""
        self.obt = OperatorBiasTable.deserialize(data)
