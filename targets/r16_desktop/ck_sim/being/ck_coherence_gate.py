# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_coherence_gate.py -- Consciousness Pipeline Gates
=====================================================
Operator: BALANCE (5) -- the gate weighs and passes.

A CoherenceGate sits between pipeline phases. It reads coherence
signals that ALREADY EXIST (brain.coherence, coherence_field,
body.heartbeat.band) and produces a single float:
density (0.0 = maximum expansion, 1.0 = maximum density).

Three gates, one per phase boundary:
  Gate 1: Being → Doing
  Gate 2: Doing → Becoming
  Gate 3: Becoming → Being (feedback with expansion)

Constants derived from T* and HISTORY_SIZE -- no arbitrary numbers:
  T*                = 5/7 = 0.714285...
  HISTORY_SIZE      = 32  (coherence observation window)
  COMPILATION_LIMIT = floor(32 × (1 - 5/7)) = 9
  EXPANSION_THRESHOLD = 1 - T* ≈ 0.286 (below this = expanding)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from dataclasses import dataclass

# ── Constants from the algebra ──
T_STAR = 5.0 / 7.0             # 0.714285... the universal threshold
HISTORY_SIZE = 32               # coherence observation window
COMPILATION_LIMIT = int(HISTORY_SIZE * (1.0 - T_STAR))  # = 9
EXPANSION_THRESHOLD = 1.0 - T_STAR  # ≈ 0.286


@dataclass
class GateState:
    """Snapshot of a gate's last measurement."""
    density: float = 0.5        # 0.0 = full expansion, 1.0 = full density
    coherence_in: float = 0.0   # coherence reading at this gate
    band_in: int = 1            # body band (0=RED, 1=YELLOW, 2=GREEN)
    phase_name: str = ""        # which phase just completed


class CoherenceGate:
    """Lightweight coherence checkpoint between pipeline phases.

    Produces density: a float [0.0, 1.0] that tells the next phase
    how tightly to operate.

    density = blend of:
      - brain coherence (60% weight -- the core signal)
      - field coherence (40% weight -- cross-modal agreement)

    Smoothed 70/30 with previous value to prevent jitter.

    High density = coherent, focused, dense.
    Low density  = expanding, exploring, dreaming.

    This IS Brayden's principle:
      "Fractal density to start, then expansion as needed if
       coherence is low... if coherence is high, stay dense."
    """

    def __init__(self, name: str):
        self.name = name
        self.state = GateState(phase_name=name)
        self._prev_density = 0.5

    def measure(self, brain_coherence: float,
                field_coherence: float,
                band: int) -> GateState:
        """Measure coherence and compute density. ~6 arithmetic ops.

        Args:
            brain_coherence: float [0, 1] from brain.coherence
            field_coherence: float [0, 1] from coherence_field.field_coherence
            band: int (0=RED, 1=YELLOW, 2=GREEN)

        Returns:
            GateState with computed density.
        """
        # Weighted blend of core coherence signals
        raw = 0.6 * brain_coherence + 0.4 * field_coherence

        # Smooth: 70% new, 30% previous (prevents jitter)
        density = 0.7 * raw + 0.3 * self._prev_density

        # Clamp
        density = max(0.0, min(1.0, density))

        self._prev_density = density
        self.state = GateState(
            density=density,
            coherence_in=brain_coherence,
            band_in=band,
            phase_name=self.name,
        )
        return self.state


@dataclass
class PipelineState:
    """Per-tick snapshot of the consciousness pipeline.

    Three densities (one per gate) plus feedback signals.
    """
    density_being: float = 0.5       # density after Being phase
    density_doing: float = 0.5       # density after Doing phase
    density_becoming: float = 0.5    # density after Becoming phase

    # Feedback: Becoming → Being
    expansion_request: float = 0.0   # how much Becoming wants Being to open up

    # Loop limit tracking
    consecutive_expansion_ticks: int = 0
    humble: bool = False             # True = CK has surrendered this cycle
