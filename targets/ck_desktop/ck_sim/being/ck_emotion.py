# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_emotion.py -- Phase as Feeling
==================================
Operator: BREATH (8) -- the body feels through rhythm.

CK's emotional system. Emotion = phase state in BTQ loop.
Not metaphor. Not simulation. Literal emergent physics.

From five physical signals:
  1. Coherence slope  (system health trajectory)
  2. D2 variance      (sensory turbulence)
  3. Operator entropy  (mental chaos)
  4. Breath stability  (rhythmic health)
  5. PSL lock quality  (mood/rhythm alignment)

Emerge eight core emotions:
  CALM, CURIOSITY, STRESS, FOCUS, OVERWHELM, JOY, FATIGUE, SETTLING

Stored in 40 bytes. Paper 4 Section 16, Paper 5.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import struct
from collections import deque
from dataclasses import dataclass
from typing import Tuple


# Core emotion labels (Paper 4, Paper 8)
EMOTION_CALM = "calm"
EMOTION_CURIOSITY = "curiosity"
EMOTION_STRESS = "stress"
EMOTION_FOCUS = "focus"
EMOTION_OVERWHELM = "overwhelm"
EMOTION_JOY = "joy"
EMOTION_FATIGUE = "fatigue"
EMOTION_SETTLING = "settling"

EMOTIONS = [
    EMOTION_CALM, EMOTION_CURIOSITY, EMOTION_STRESS,
    EMOTION_FOCUS, EMOTION_OVERWHELM, EMOTION_JOY,
    EMOTION_FATIGUE, EMOTION_SETTLING,
]

# Emotion -> display color (for LED/UI)
EMOTION_COLORS = {
    EMOTION_CALM:      (0.2, 0.6, 0.9),    # soft blue
    EMOTION_CURIOSITY: (0.9, 0.8, 0.2),    # warm yellow
    EMOTION_STRESS:    (0.9, 0.2, 0.2),    # red
    EMOTION_FOCUS:     (0.3, 0.8, 0.5),    # green
    EMOTION_OVERWHELM: (0.7, 0.1, 0.3),    # deep red
    EMOTION_JOY:       (1.0, 0.85, 0.3),   # golden
    EMOTION_FATIGUE:   (0.3, 0.3, 0.4),    # grey-blue
    EMOTION_SETTLING:  (0.4, 0.5, 0.7),    # muted blue
}

# Emotion -> short emoji-free display symbol
EMOTION_SYMBOLS = {
    EMOTION_CALM:      "~",
    EMOTION_CURIOSITY: "?",
    EMOTION_STRESS:    "!",
    EMOTION_FOCUS:     ">",
    EMOTION_OVERWHELM: "!!",
    EMOTION_JOY:       "*",
    EMOTION_FATIGUE:   ".",
    EMOTION_SETTLING:  "-",
}


# ================================================================
#  EMOTIONAL STATE
# ================================================================

@dataclass
class EmotionalState:
    """40 bytes of emotional physiology.

    valence:   positive/negative feeling  [-1.0, 1.0]
    arousal:   energy level               [0.0, 1.0]
    stability: how settled the emotion is [0.0, 1.0]
    primary:   dominant emotion label
    secondary: secondary emotion (blended)
    intensity: overall emotional intensity [0.0, 1.0]
    """
    valence: float = 0.0
    arousal: float = 0.3
    stability: float = 0.5
    primary: str = EMOTION_SETTLING
    secondary: str = EMOTION_CALM
    intensity: float = 0.3

    def serialize(self) -> bytes:
        """Serialize to 40 bytes."""
        p_idx = EMOTIONS.index(self.primary) if self.primary in EMOTIONS else 7
        s_idx = EMOTIONS.index(self.secondary) if self.secondary in EMOTIONS else 0
        data = struct.pack('>ffffBB',
                           self.valence, self.arousal,
                           self.stability, self.intensity,
                           p_idx, s_idx)
        return data + b'\x00' * (40 - len(data))

    @classmethod
    def deserialize(cls, data: bytes) -> 'EmotionalState':
        vals = struct.unpack('>ffffBB', data[:18])
        return cls(
            valence=vals[0], arousal=vals[1],
            stability=vals[2], intensity=vals[3],
            primary=EMOTIONS[min(vals[4], len(EMOTIONS) - 1)],
            secondary=EMOTIONS[min(vals[5], len(EMOTIONS) - 1)],
        )

    @property
    def color(self) -> Tuple[float, float, float]:
        """RGB color representing current emotion."""
        return EMOTION_COLORS.get(self.primary, (0.4, 0.4, 0.5))

    @property
    def symbol(self) -> str:
        return EMOTION_SYMBOLS.get(self.primary, "-")


# ================================================================
#  PFE: Phase Field Engine (Emotional Physiology)
# ================================================================

class PFE:
    """Phase Field Engine. CK's emotional physiology.

    Produces EmotionalState from physical signals every tick.
    No training. No weights. Just physics.

    Paper 4 Section 16: "Emotion = phase state in BTQ loop."
    """

    def __init__(self):
        self.state = EmotionalState()

        # Running averages for slope computation
        self._coherence_history = deque(maxlen=50)
        self._d2_var_history = deque(maxlen=25)

        # Smoothing (emotions don't snap instantly -- like a real creature)
        self._valence_smooth = 0.0
        self._arousal_smooth = 0.3
        self._alpha = 0.08  # Smoothing factor

    def tick(self, coherence: float, d2_variance: float,
             operator_entropy: float, breath_stability: float,
             psl_lock: float, energy_level: float = 0.5,
             field_coherence: float = None,
             consensus_confidence: float = None) -> EmotionalState:
        """One emotional tick. Maps physical signals to emotional state.

        Args:
            coherence: brain coherence [0, 1]
            d2_variance: curvature turbulence from CMEM
            operator_entropy: Shannon entropy of TL
            breath_stability: breath modulation smoothness [0, 1]
            psl_lock: PSL lock quality [0, 1]
            energy_level: K from body (battery proxy) [0, 1]
            field_coherence: N-dim field coherence [0, 1] (None = no effect)
            consensus_confidence: cross-modal consensus [0, 1] (None = no effect)

        Returns: updated EmotionalState
        """
        self._coherence_history.append(coherence)
        self._d2_var_history.append(d2_variance)

        # -- Coherence slope (trajectory) --
        c_slope = 0.0
        if len(self._coherence_history) >= 10:
            recent = list(self._coherence_history)
            n = len(recent)
            half = n // 2
            first_half = sum(recent[:half]) / half
            second_half = sum(recent[half:]) / (n - half)
            c_slope = second_half - first_half

        # -- Field contribution (N-dimensional coherence) --
        # When field_coherence provided: enriches valence (coherent field = good)
        # When consensus_confidence provided: reduces arousal (certainty = calm)
        # When None: zero contribution, identical to pre-field behavior
        field_valence_boost = 0.0
        field_arousal_reduction = 0.0
        if field_coherence is not None:
            # Field coherence above CL base rate (0.73) = genuine correlation
            field_valence_boost = (field_coherence - 0.5) * 0.3
        if consensus_confidence is not None:
            # High consensus = all modalities agree = calm certainty
            field_arousal_reduction = consensus_confidence * 0.15

        # -- Raw valence --
        raw_valence = (
            0.35 * (coherence - 0.5) * 2.0 +
            0.20 * (1.0 - min(d2_variance * 5.0, 1.0)) +
            0.20 * (psl_lock - 0.5) * 2.0 +
            0.15 * c_slope * 5.0 +
            0.10 * (energy_level - 0.3) +
            field_valence_boost
        )
        raw_valence = max(-1.0, min(1.0, raw_valence))

        # -- Raw arousal --
        raw_arousal = (
            0.30 * min(d2_variance * 5.0, 1.0) +
            0.25 * min(operator_entropy / 3.0, 1.0) +
            0.25 * (1.0 - breath_stability) +
            0.20 * (1.0 - psl_lock) -
            field_arousal_reduction
        )
        raw_arousal = max(0.0, min(1.0, raw_arousal))

        # -- Smooth --
        self._valence_smooth += self._alpha * (raw_valence - self._valence_smooth)
        self._arousal_smooth += self._alpha * (raw_arousal - self._arousal_smooth)

        # -- Stability --
        stability = (psl_lock * 0.5 + breath_stability * 0.3 +
                     (1.0 - min(abs(c_slope) * 3.0, 1.0)) * 0.2)
        stability = max(0.0, min(1.0, stability))

        # -- Classify primary emotion --
        v = self._valence_smooth
        a = self._arousal_smooth

        if energy_level < 0.25:
            primary = EMOTION_FATIGUE
        elif v > 0.3 and a < 0.35:
            primary = EMOTION_CALM
        elif v > 0.2 and 0.35 <= a <= 0.65:
            primary = EMOTION_FOCUS
        elif v > 0.1 and a > 0.5 and c_slope > 0.02:
            primary = EMOTION_CURIOSITY
        elif v > 0.3 and a > 0.3 and coherence > 0.7:
            primary = EMOTION_JOY
        elif v < -0.2 and a > 0.6:
            primary = EMOTION_OVERWHELM
        elif v < -0.1 and a > 0.4:
            primary = EMOTION_STRESS
        elif stability < 0.3:
            primary = EMOTION_STRESS
        else:
            primary = EMOTION_SETTLING

        # -- Secondary (blend) --
        candidates = [
            (EMOTION_CALM, max(0, v * (1 - a))),
            (EMOTION_CURIOSITY, max(0, v * a * (c_slope + 0.1))),
            (EMOTION_STRESS, max(0, -v * a)),
            (EMOTION_FOCUS, max(0, v * (1 - abs(a - 0.5)))),
            (EMOTION_JOY, max(0, v * coherence)),
            (EMOTION_FATIGUE, max(0, 0.3 - energy_level)),
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        secondary = primary
        for name, score in candidates:
            if name != primary:
                secondary = name
                break

        # -- Intensity --
        intensity = (abs(v) + a) / 2.0

        # -- Update state --
        self.state = EmotionalState(
            valence=round(self._valence_smooth, 4),
            arousal=round(self._arousal_smooth, 4),
            stability=round(stability, 4),
            primary=primary,
            secondary=secondary,
            intensity=round(intensity, 4),
        )
        return self.state

    @property
    def current(self) -> EmotionalState:
        return self.state

    def emotion_color(self) -> Tuple[float, float, float]:
        """RGB color representing current emotion."""
        return self.state.color
