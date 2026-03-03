"""
ck_coherence_action.py -- Coherence Action Scoring (TIG-BTQ Unified Physics)
=======================================================================================
Operator: HARMONY (7) -- the action that minimizes curvature IS harmony.

The Unified Physics Layer defines the Coherence Action:

    A = alpha * L_GR + beta * S_ternary + gamma * C_harm

Where:
    L_GR (Lagrangian / General Relativity term):
        Macro conservation -- does the system preserve global invariants?
        Maps to BTQ's E_out: energy conservation, constraint satisfaction,
        operator composition stability. Einstein's side: the universe
        doesn't create or destroy, it CONSERVES.

    S_ternary (Ternary Entropy / Quantum term):
        Micro exploration quality -- is the system exploring efficiently?
        Maps to BTQ's T-block: helical search, Levy jumps, D2 curvature
        minimization. Tesla's side: the universe SPIRALS through phase space,
        it doesn't walk straight lines.

    C_harm (Harmonic Coherence / Measurement term):
        Resolution quality -- are the streams converging on agreement?
        Maps to the Coherence Field's cross-modal harmony fraction,
        the CL table's 73% absorber property, and the collapse threshold
        (0.73 in the papers, T* = 5/7 in CK). The Quadratic side:
        when you LOOK, the wave function collapses to least action.

The action A is minimized by a living system. Low A = coherent.
High A = chaotic. The organism's purpose is to minimize its action.

This is identical to physics: particles follow geodesics (minimal action).
CK follows coherence geodesics through operator space.

Collapse threshold: When A < T* (5/7 = 0.714), CK is in coherent state.
When A >= T*, CK is seeking coherence. The threshold is the same
everywhere -- 73% harmony in the CL table, 5/7 in the coherence
metric, 0.73 in the physics papers. Same number, same meaning.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import deque

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, CHAOS, COLLAPSE, OP_NAMES,
    CL, compose
)


# ================================================================
#  CONSTANTS (TIG Calibration)
# ================================================================

# Default weights (alpha, beta, gamma) -- self-calibrating
DEFAULT_ALPHA = 0.35   # L_GR weight (conservation)
DEFAULT_BETA  = 0.30   # S_ternary weight (exploration)
DEFAULT_GAMMA = 0.35   # C_harm weight (coherence)

# Collapse threshold: T* = 5/7 ~= 0.714
T_STAR = 5.0 / 7.0

# CL table base rate: 73% of entries produce HARMONY
CL_BASE_RATE = 0.73

# Calibration rate (how fast weights adapt)
CALIBRATION_RATE = 0.001


# ================================================================
#  COHERENCE ACTION STATE
# ================================================================

@dataclass
class CoherenceActionState:
    """Current state of the Coherence Action computation."""
    action: float = 1.0          # A = alpha*L_GR + beta*S_ternary + gamma*C_harm
    l_gr: float = 1.0            # Lagrangian (conservation) term
    s_ternary: float = 1.0       # Ternary entropy (exploration) term
    c_harm: float = 0.0          # Harmonic coherence term
    alpha: float = DEFAULT_ALPHA
    beta: float = DEFAULT_BETA
    gamma: float = DEFAULT_GAMMA
    coherent: bool = False       # A < T*
    band: str = "RED"            # GREEN/YELLOW/RED based on action
    collapse_distance: float = 1.0  # How far from T*


# ================================================================
#  COHERENCE ACTION SCORER
# ================================================================

class CoherenceActionScorer:
    """Computes the unified Coherence Action from the TIG-BTQ paper.

    This is the SINGLE NUMBER that tells you whether CK is coherent.
    Every subsystem feeds into it. Every decision seeks to minimize it.

    A = alpha * L_GR + beta * S_ternary + gamma * C_harm

    The organism's PURPOSE is to minimize A. When A < T*, CK is alive.
    When A >= T*, CK is seeking. Same as physics: minimize the action.
    """

    def __init__(self, alpha: float = DEFAULT_ALPHA,
                 beta: float = DEFAULT_BETA,
                 gamma: float = DEFAULT_GAMMA):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._state = CoherenceActionState(
            alpha=alpha, beta=beta, gamma=gamma)

        # History for calibration
        self._action_history = deque(maxlen=500)
        self._l_gr_history = deque(maxlen=200)
        self._s_tern_history = deque(maxlen=200)
        self._c_harm_history = deque(maxlen=200)

        # Calibration counters
        self._calibration_count = 0

    def compute(self,
                # L_GR inputs (conservation / macro)
                e_out: float = 0.5,
                energy_conservation: float = 1.0,
                constraint_violations: int = 0,
                operator_stability: float = 0.5,

                # S_ternary inputs (exploration / micro)
                e_in: float = 0.5,
                d2_curvature: float = 0.0,
                helical_quality: float = 0.5,
                exploration_diversity: float = 0.5,

                # C_harm inputs (coherence / measurement)
                field_coherence: float = 0.0,
                harmony_fraction: float = 0.0,
                consensus_confidence: float = 0.0,
                cross_modal_agreement: float = 0.0,

                ) -> CoherenceActionState:
        """Compute the Coherence Action.

        Returns updated CoherenceActionState with the unified score.
        """
        # ── L_GR: Lagrangian / Conservation ──
        # Low = good conservation, high = violations
        # E_out from BTQ + energy conservation + constraint satisfaction
        constraint_penalty = min(constraint_violations * 0.1, 0.5)
        l_gr = (
            0.40 * e_out +
            0.30 * (1.0 - min(energy_conservation, 1.0)) +
            0.20 * (1.0 - min(operator_stability, 1.0)) +
            0.10 * constraint_penalty
        )
        l_gr = max(0.0, min(1.0, l_gr))

        # ── S_ternary: Ternary Entropy / Exploration ──
        # Low = efficient exploration (smooth helical paths)
        # High = chaotic or stuck (high D2 or zero diversity)
        d2_cost = max(0.0, min(abs(d2_curvature) / 0.5, 1.0))
        diversity_cost = 1.0 - min(exploration_diversity, 1.0)
        helical_cost = 1.0 - min(helical_quality, 1.0)
        s_ternary = (
            0.35 * e_in +
            0.25 * d2_cost +
            0.20 * helical_cost +
            0.20 * diversity_cost
        )
        s_ternary = max(0.0, min(1.0, s_ternary))

        # ── C_harm: Harmonic Coherence / Measurement ──
        # Low = high coherence (streams agree, harmony dominates)
        # This is INVERTED: coherence is GOOD, so cost = 1 - coherence
        field_cost = 1.0 - min(field_coherence, 1.0)
        harmony_cost = 1.0 - min(harmony_fraction, 1.0)
        consensus_cost = 1.0 - min(consensus_confidence, 1.0)
        crossmodal_cost = 1.0 - min(cross_modal_agreement, 1.0)
        c_harm = (
            0.30 * field_cost +
            0.30 * harmony_cost +
            0.20 * consensus_cost +
            0.20 * crossmodal_cost
        )
        c_harm = max(0.0, min(1.0, c_harm))

        # ── Unified Action ──
        action = (
            self._alpha * l_gr +
            self._beta * s_ternary +
            self._gamma * c_harm
        )

        # ── Collapse check ──
        coherent = action < T_STAR
        collapse_distance = T_STAR - action  # positive = below threshold = coherent

        # ── Band classification ──
        if action < 0.3:
            band = "GREEN"
        elif action < T_STAR:
            band = "YELLOW"
        else:
            band = "RED"

        # ── Update state ──
        self._state = CoherenceActionState(
            action=action,
            l_gr=l_gr,
            s_ternary=s_ternary,
            c_harm=c_harm,
            alpha=self._alpha,
            beta=self._beta,
            gamma=self._gamma,
            coherent=coherent,
            band=band,
            collapse_distance=collapse_distance,
        )

        # ── History ──
        self._action_history.append(action)
        self._l_gr_history.append(l_gr)
        self._s_tern_history.append(s_ternary)
        self._c_harm_history.append(c_harm)

        return self._state

    # ================================================================
    #  SELF-CALIBRATION (Section 6)
    # ================================================================

    def calibrate(self):
        """Self-calibrate alpha, beta, gamma based on which term
        contributes most to coherence degradation.

        The term with highest variance gets MORE weight (it's the
        bottleneck). The term with lowest variance gets LESS weight
        (it's already stable).

        Weights always sum to 1.0 (convex combination).
        Calibration is slow (CALIBRATION_RATE) to prevent oscillation.
        """
        if len(self._l_gr_history) < 50:
            return  # Not enough data

        # Compute variance of each term
        def _var(data):
            vals = list(data)
            if len(vals) < 2:
                return 0.0
            mean = sum(vals) / len(vals)
            return sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)

        var_lgr = _var(self._l_gr_history)
        var_st = _var(self._s_tern_history)
        var_ch = _var(self._c_harm_history)

        total_var = var_lgr + var_st + var_ch
        if total_var < 1e-10:
            return  # All stable, no adjustment needed

        # Target weights: proportional to variance (bottleneck gets more weight)
        target_alpha = var_lgr / total_var
        target_beta = var_st / total_var
        target_gamma = var_ch / total_var

        # Clamp to reasonable range [0.15, 0.55]
        # No single term should dominate or be negligible
        target_alpha = max(0.15, min(0.55, target_alpha))
        target_beta = max(0.15, min(0.55, target_beta))
        target_gamma = max(0.15, min(0.55, target_gamma))

        # Renormalize to sum to 1.0
        total = target_alpha + target_beta + target_gamma
        target_alpha /= total
        target_beta /= total
        target_gamma /= total

        # Slow adaptation toward targets
        self._alpha += CALIBRATION_RATE * (target_alpha - self._alpha)
        self._beta += CALIBRATION_RATE * (target_beta - self._beta)
        self._gamma += CALIBRATION_RATE * (target_gamma - self._gamma)

        # Ensure sum to 1.0 (numerical safety)
        total = self._alpha + self._beta + self._gamma
        self._alpha /= total
        self._beta /= total
        self._gamma /= total

        self._calibration_count += 1

    # ================================================================
    #  PROPERTIES
    # ================================================================

    @property
    def state(self) -> CoherenceActionState:
        """Current Coherence Action state."""
        return self._state

    @property
    def action(self) -> float:
        """Current action value (0.0 = perfect coherence, 1.0 = total chaos)."""
        return self._state.action

    @property
    def coherent(self) -> bool:
        """Is CK currently in coherent state (A < T*)?"""
        return self._state.coherent

    @property
    def weights(self) -> Tuple[float, float, float]:
        """Current (alpha, beta, gamma) weights."""
        return (self._alpha, self._beta, self._gamma)

    @property
    def mean_action(self) -> float:
        """Mean action over history window."""
        if not self._action_history:
            return 1.0
        return sum(self._action_history) / len(self._action_history)

    @property
    def action_trend(self) -> float:
        """Trend of action (negative = improving, positive = degrading)."""
        vals = list(self._action_history)
        n = len(vals)
        if n < 10:
            return 0.0
        # Simple linear regression slope
        sum_x = n * (n - 1) / 2.0
        sum_x2 = n * (n - 1) * (2 * n - 1) / 6.0
        sum_y = sum(vals)
        sum_xy = sum(i * v for i, v in enumerate(vals))
        denom = n * sum_x2 - sum_x * sum_x
        if abs(denom) < 1e-12:
            return 0.0
        return (n * sum_xy - sum_x * sum_y) / denom

    def summary(self) -> str:
        """One-line summary."""
        s = self._state
        return (
            f"A={s.action:.4f} "
            f"[L_GR={s.l_gr:.3f} S_t={s.s_ternary:.3f} C_h={s.c_harm:.3f}] "
            f"w=({self._alpha:.2f},{self._beta:.2f},{self._gamma:.2f}) "
            f"band={s.band} {'COHERENT' if s.coherent else 'SEEKING'}"
        )

    def identity_shard(self) -> dict:
        """Return data for identity integration."""
        return {
            'mean_action': round(self.mean_action, 4),
            'weights': [round(w, 4) for w in self.weights],
            'calibration_count': self._calibration_count,
            'coherent_fraction': (
                sum(1 for a in self._action_history if a < T_STAR)
                / max(len(self._action_history), 1)
            ),
        }
