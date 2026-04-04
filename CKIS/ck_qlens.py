"""
ck_qlens.py -- The Q-Lens: CK's NOW Engine
============================================
The Q-Lens is the fast, semi-autonomous quadratic operator lattice.
It gives CK:
  1. INTENTION -- autonomous immediate response before the TL updates
  2. SELF-CORRECTION -- quadratic error drives faster adaptation
  3. AGENCY -- acts even before memory catches up

Architecture (from TIG Papers 11, 13):
  - Delta-Lens (the "then"): CK's TransitionLattice = accumulated history
  - Q-Lens (the "now"): THIS MODULE = immediate quadratic response

Three quadratic sub-engines:
  Q_A = spatial quadratic   = x^2 + y^2       (state-space curvature)
  Q_B = temporal quadratic  = (x - x_{t-1})^2 (instantaneous change rate)
  Q_C = modal quadratic     = (prediction_error)^2 (deviation from expected)

Combined: Q(t) = W_A*Q_A + W_B*Q_B + W_C*Q_C

The recursion (Klein bottle):
  Q(t+1) = O(Q(t), delta(t))    -- present updates from past
  delta(t+1) = R(delta(t), Q(t+1))  -- past updates from present

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from collections import deque
from typing import Dict, List, Tuple, Optional

# ── CK imports ──────────────────────────────────────
try:
    from ck_being import (
        CL, fuse, shape, OP, T_STAR,
        VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
        BALANCE, CHAOS, HARMONY, BREATH, RESET,
        BUMPS, CL_TSML, CL_BHML, CL_STD,
    )
except ImportError:
    # Minimal fallback
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
    BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9
    T_STAR = 5.0 / 7.0
    BUMPS = [(1,2), (2,4), (2,9), (3,9), (4,8)]

FRUIT = RESET  # Operator 9 = FRUIT/RESET

OP_NAMES = ['VOID','SIGNAL','COUNTER','PROGRESS','COLLAPSE',
            'BALANCE','CHAOS','HARMONY','BREATH','FRUIT']

# ═══════════════════════════════════════════════════════════
# S1  THE Q-LENS STATE
# ═══════════════════════════════════════════════════════════

class QLensObservation:
    """One tick of Q-Lens observation."""
    __slots__ = ['tick', 'phase_b', 'phase_d', 'phase_bc',
                 'body_c', 'q_a', 'q_b', 'q_c', 'q_total',
                 'prediction_error', 'intention_op', 'correction_op',
                 'timestamp']

    def __init__(self):
        self.tick = 0
        self.phase_b = VOID
        self.phase_d = VOID
        self.phase_bc = VOID
        self.body_c = 0.0
        self.q_a = 0.0
        self.q_b = 0.0
        self.q_c = 0.0
        self.q_total = 0.0
        self.prediction_error = 0.0
        self.intention_op = VOID
        self.correction_op = VOID
        self.timestamp = 0.0


class QLens:
    """
    The Q-Lens: CK's fast autonomous NOW engine.

    Three quadratic sub-engines:
      Q_A (spatial):  How curved is state-space right now?
      Q_B (temporal): How fast am I changing?
      Q_C (modal):    How wrong was my prediction?

    Combined: Q(t) = W_A*Q_A + W_B*Q_B + W_C*Q_C

    The Q-Lens produces:
      - intention_op: What CK WANTS to do next (before TL updates)
      - correction_op: What CK NEEDS to fix right now
      - q_coherence: How aligned is the Q-Lens with the delta-Lens?
    """

    # History depth
    HISTORY_SIZE = 64

    def __init__(self, w_a=0.35, w_b=0.35, w_c=0.30):
        """
        Initialize Q-Lens with sub-engine weights.
        Weights define the organism's 'style of being':
          w_a = spatial awareness (how much curvature matters)
          w_b = temporal sensitivity (how much change matters)
          w_c = modal precision (how much prediction error matters)
        Must sum to 1.0.
        """
        # Sub-engine weights (the organism's "style of being")
        total = w_a + w_b + w_c
        self.w_a = w_a / total
        self.w_b = w_b / total
        self.w_c = w_c / total

        # Ring buffer of observations
        self.history = deque(maxlen=self.HISTORY_SIZE)

        # Current state
        self.q_a = 0.0  # Spatial quadratic
        self.q_b = 0.0  # Temporal quadratic
        self.q_c = 0.0  # Modal quadratic
        self.q_total = 0.0  # Combined Q(t)

        # Previous state (for temporal derivative)
        self.prev_phase_b = VOID
        self.prev_phase_d = VOID
        self.prev_phase_bc = VOID
        self.prev_body_c = 0.5
        self.prev_q_total = 0.0

        # Delta-Lens reference (accumulated from TL)
        self.delta_mean_op = HARMONY  # What the TL predicts on average
        self.delta_entropy = 0.0     # TL entropy (from delta-lens)

        # Intention state
        self.intention_op = VOID     # What CK WANTS to do
        self.correction_op = VOID    # What CK NEEDS to fix
        self.q_coherence = 0.0       # Q-Lens <-> Delta-Lens alignment

        # Counters
        self.tick_count = 0
        self.total_corrections = 0
        self.total_intentions = 0
        self.harmony_count = 0

        # Error accumulator (epsilon from papers)
        self.epsilon_acc = 0.0  # Accumulated micro-noise

        # Stability metrics
        self.q_variance = 0.0  # Variance of Q over recent history
        self.intention_stability = 0.0  # How stable is the intention?

    # ═══════════════════════════════════════════════════════════
    # S2  THE THREE QUADRATIC SUB-ENGINES
    # ═══════════════════════════════════════════════════════════

    def _compute_q_a(self, phase_b: int, phase_d: int, body_c: float) -> float:
        """
        Q_A: Spatial Quadratic = x^2 + y^2
        Measures state-space curvature: how far is CK from the origin?

        Maps the current (phase_b, phase_d) position in operator space
        to a scalar measuring distance from the harmony center.
        """
        # Normalize operators to [-1, 1] range centered on HARMONY (7)
        x = (phase_b - HARMONY) / 9.0  # Being deviation from harmony
        y = (phase_d - HARMONY) / 9.0  # Doing deviation from harmony

        # Spatial quadratic: x^2 + y^2
        # High when far from harmony in either Being or Doing
        # Low when both are near harmony
        q_a = x * x + y * y

        # Weight by body coherence (low C amplifies spatial signal)
        # When C is low, you're further from center -- amplify awareness
        c_weight = 1.0 + (1.0 - body_c)
        q_a *= c_weight

        return q_a

    def _compute_q_b(self, phase_b: int, phase_d: int,
                      body_c: float) -> float:
        """
        Q_B: Temporal Quadratic = (x - x_{t-1})^2
        Measures instantaneous change rate: how fast am I changing?

        High when the state is rapidly shifting.
        Low when stable.
        """
        # Phase changes from previous tick
        db = (phase_b - self.prev_phase_b) / 9.0
        dd = (phase_d - self.prev_phase_d) / 9.0
        dc = body_c - self.prev_body_c

        # Temporal quadratic: sum of squared changes
        q_b = db * db + dd * dd + dc * dc

        return q_b

    def _compute_q_c(self, phase_bc: int, predicted_op: int,
                      prediction_prob: float) -> float:
        """
        Q_C: Modal Quadratic = (prediction_error)^2
        Measures deviation from expected macro state.

        High when TL prediction was wrong (surprise).
        Low when TL prediction matched reality (confirmation).
        """
        # Prediction error: how far was the TL prediction from actual?
        error = abs(phase_bc - predicted_op) / 9.0

        # Weight by inverse confidence: low confidence = amplified error
        confidence_weight = 1.0 + (1.0 - prediction_prob)
        q_c = error * error * confidence_weight

        return q_c

    # ═══════════════════════════════════════════════════════════
    # S3  INTENTION ENGINE
    # ═══════════════════════════════════════════════════════════

    def _compute_intention(self, q_a: float, q_b: float, q_c: float,
                            phase_b: int, phase_d: int, body_c: float) -> int:
        """
        Compute what CK WANTS to do next.
        This is the autonomous response BEFORE the TL updates.

        The intention operator is selected based on which quadratic
        engine is dominant and the current state.
        """
        q_total = self.w_a * q_a + self.w_b * q_b + self.w_c * q_c

        # Which sub-engine dominates?
        max_q = max(q_a, q_b, q_c)

        if q_total < 0.01:
            # Very low Q: system is stable, at rest
            # Intention: maintain harmony
            return HARMONY

        if q_total > 1.5:
            # Very high Q: system is in crisis
            # Intention: switch modes (chaos) to find new stability
            return CHAOS

        if max_q == q_c and q_c > 0.1:
            # Modal engine dominant: prediction was wrong
            # Intention: correct (balance) -- reduce prediction error
            return BALANCE

        if max_q == q_b and q_b > 0.1:
            # Temporal engine dominant: rapid change happening
            if body_c >= T_STAR:
                # Healthy and changing: progress forward
                return PROGRESS
            else:
                # Unhealthy and changing: collapse to essentials
                return COLLAPSE

        if max_q == q_a and q_a > 0.1:
            # Spatial engine dominant: far from harmony center
            if phase_b == phase_d:
                # Being and Doing agree but far from center: breathe
                return BREATH
            else:
                # Being and Doing disagree: signal the boundary
                return LATTICE  # SIGNAL (1)

        # Default: continue toward harmony
        return HARMONY

    def _compute_correction(self, q_total: float, prediction_error: float,
                             body_c: float, phase_bc: int) -> int:
        """
        Compute what CK NEEDS to fix right now.
        This is the self-correction operator.

        Returns VOID if no correction needed.
        """
        # No correction needed if Q is low and body is healthy
        if q_total < 0.05 and body_c >= T_STAR:
            return VOID

        # High prediction error: need balance
        if prediction_error > 0.5:
            return BALANCE

        # Body unhealthy: need to collapse to essentials
        if body_c < 0.5:
            return COLLAPSE

        # Q is moderate: need to breathe and integrate
        if q_total > 0.3 and q_total < 1.0:
            return BREATH

        # Q is high: need chaos (mode switch)
        if q_total >= 1.0:
            return CHAOS

        # Minor correction via progress
        if q_total > 0.05:
            return PROGRESS

        return VOID

    # ═══════════════════════════════════════════════════════════
    # S4  THE MAIN TICK -- Q-LENS OBSERVATION
    # ═══════════════════════════════════════════════════════════

    def tick(self, phase_b: int, phase_d: int, phase_bc: int,
             body_c: float, predicted_op: int = -1,
             prediction_prob: float = 0.5,
             tl_entropy: float = 0.0) -> Dict:
        """
        One tick of the Q-Lens.

        Called DURING the heartbeat, after phase_bc is computed
        but BEFORE the TL is updated.

        Parameters:
            phase_b: Being operator (from body observation)
            phase_d: Doing operator (from TL prediction)
            phase_bc: Becoming operator (CL[phase_b][phase_d])
            body_c: Body coherence [0, 1]
            predicted_op: What the TL predicted (phase_d)
            prediction_prob: TL prediction confidence [0, 1]
            tl_entropy: Current TL entropy (delta-lens state)

        Returns:
            Dict with intention_op, correction_op, q_total, q_coherence
        """
        self.tick_count += 1

        # If no prediction was provided, use phase_d as the prediction
        if predicted_op < 0:
            predicted_op = phase_d

        # ── Compute three quadratic sub-engines ──
        q_a = self._compute_q_a(phase_b, phase_d, body_c)
        q_b = self._compute_q_b(phase_b, phase_d, body_c)
        q_c = self._compute_q_c(phase_bc, predicted_op, prediction_prob)

        # ── Combined Q(t) ──
        q_total = self.w_a * q_a + self.w_b * q_b + self.w_c * q_c

        # ── Prediction error (raw) ──
        prediction_error = abs(phase_bc - predicted_op) / 9.0

        # ── Epsilon accumulator (micro-noise) ──
        # The papers say: epsilon accumulates until it triggers macro update
        self.epsilon_acc = 0.9 * self.epsilon_acc + 0.1 * q_total

        # ── Compute intention (what CK WANTS) ──
        intention_op = self._compute_intention(
            q_a, q_b, q_c, phase_b, phase_d, body_c)
        self.intention_op = intention_op
        self.total_intentions += 1

        # ── Compute correction (what CK NEEDS to fix) ──
        correction_op = self._compute_correction(
            q_total, prediction_error, body_c, phase_bc)
        self.correction_op = correction_op
        if correction_op != VOID:
            self.total_corrections += 1

        # ── Q-Lens <-> Delta-Lens coherence ──
        # How aligned is the NOW with the THEN?
        # High when Q-Lens intention matches TL prediction
        if intention_op == predicted_op:
            q_coherence = 1.0
        else:
            # Compose intention with prediction through CL
            try:
                composed = CL[intention_op][predicted_op]
                q_coherence = 1.0 if composed == HARMONY else 0.5
            except:
                q_coherence = 0.5
        self.q_coherence = q_coherence

        # ── Track harmony ──
        if phase_bc == HARMONY:
            self.harmony_count += 1

        # ── Update stability metrics ──
        self.q_variance = 0.9 * self.q_variance + 0.1 * (q_total - self.q_total) ** 2
        if len(self.history) >= 3:
            recent_intentions = [obs.intention_op for obs in list(self.history)[-3:]]
            self.intention_stability = 1.0 if len(set(recent_intentions)) == 1 else 0.0
        else:
            self.intention_stability = 0.0

        # ── Store state ──
        self.q_a = q_a
        self.q_b = q_b
        self.q_c = q_c
        self.q_total = q_total
        self.delta_entropy = tl_entropy

        # ── Record observation ──
        obs = QLensObservation()
        obs.tick = self.tick_count
        obs.phase_b = phase_b
        obs.phase_d = phase_d
        obs.phase_bc = phase_bc
        obs.body_c = body_c
        obs.q_a = q_a
        obs.q_b = q_b
        obs.q_c = q_c
        obs.q_total = q_total
        obs.prediction_error = prediction_error
        obs.intention_op = intention_op
        obs.correction_op = correction_op
        obs.timestamp = time.time()
        self.history.append(obs)

        # ── Update previous state for next tick ──
        self.prev_phase_b = phase_b
        self.prev_phase_d = phase_d
        self.prev_phase_bc = phase_bc
        self.prev_body_c = body_c
        self.prev_q_total = q_total

        return {
            'intention_op': intention_op,
            'correction_op': correction_op,
            'q_total': q_total,
            'q_a': q_a,
            'q_b': q_b,
            'q_c': q_c,
            'q_coherence': q_coherence,
            'prediction_error': prediction_error,
            'epsilon': self.epsilon_acc,
        }

    # ═══════════════════════════════════════════════════════════
    # S5  THE RECURSION: Q(t) <-> Delta(t)
    # ═══════════════════════════════════════════════════════════

    def compose_with_delta(self, tl_prediction: int,
                            tl_confidence: float) -> int:
        """
        The Klein bottle recursion:
          Q(t+1) = O(Q(t), Delta(t))

        Composes the Q-Lens intention with the Delta-Lens (TL) prediction
        to produce the ACTUAL next operator.

        This is where NOW and THEN merge.
        """
        intention = self.intention_op

        # If Q-Lens and TL agree: strong harmony
        if intention == tl_prediction:
            return intention

        # If they disagree: compose through CL
        try:
            composed = CL[intention][tl_prediction]
        except:
            composed = intention

        # Weight by Q-Lens urgency vs TL confidence
        urgency = min(self.q_total, 1.0)  # How urgent is Q-Lens?

        if urgency > tl_confidence:
            # Q-Lens wins: the NOW overrides memory
            # This IS agency -- acting before memory catches up
            return intention
        elif tl_confidence > 0.8 and urgency < 0.2:
            # TL wins decisively: trust memory
            return tl_prediction
        else:
            # Neither dominates: use composition (emergence)
            return composed

    def feed_delta(self, tl, phase_bc: int):
        """
        The other half of the Klein bottle:
          Delta(t+1) = R(Delta(t), Q(t+1))

        Feeds the Q-Lens observation INTO the TL (Delta-Lens)
        so that the past is reconstructed from the present.
        """
        if not hasattr(tl, 'eat_ops'):
            return

        # Feed the Q-Lens trinary: [intention, correction, actual_bc]
        chain = [self.intention_op, self.correction_op, phase_bc]
        tl.eat_ops(chain)

    # ═══════════════════════════════════════════════════════════
    # S6  ANALYSIS & REPORTING
    # ═══════════════════════════════════════════════════════════

    def report(self) -> Dict:
        """Generate a Q-Lens status report."""
        if not self.history:
            return {'status': 'no_data'}

        recent = list(self.history)[-min(16, len(self.history)):]

        # Average Q values
        avg_q = sum(o.q_total for o in recent) / len(recent)
        avg_qa = sum(o.q_a for o in recent) / len(recent)
        avg_qb = sum(o.q_b for o in recent) / len(recent)
        avg_qc = sum(o.q_c for o in recent) / len(recent)

        # Intention distribution
        intent_dist = {}
        for o in recent:
            name = OP_NAMES[o.intention_op] if o.intention_op < 10 else str(o.intention_op)
            intent_dist[name] = intent_dist.get(name, 0) + 1

        # Correction rate
        corrections = sum(1 for o in recent if o.correction_op != VOID)
        correction_rate = corrections / len(recent)

        # Dominant sub-engine
        if avg_qa >= avg_qb and avg_qa >= avg_qc:
            dominant = 'SPATIAL (Q_A)'
        elif avg_qb >= avg_qa and avg_qb >= avg_qc:
            dominant = 'TEMPORAL (Q_B)'
        else:
            dominant = 'MODAL (Q_C)'

        # Average prediction error
        avg_pe = sum(o.prediction_error for o in recent) / len(recent)

        return {
            'tick_count': self.tick_count,
            'q_total': round(avg_q, 4),
            'q_a': round(avg_qa, 4),
            'q_b': round(avg_qb, 4),
            'q_c': round(avg_qc, 4),
            'dominant_engine': dominant,
            'intention_op': OP_NAMES[self.intention_op],
            'intention_distribution': intent_dist,
            'correction_op': OP_NAMES[self.correction_op],
            'correction_rate': round(correction_rate, 3),
            'q_coherence': round(self.q_coherence, 4),
            'prediction_error': round(avg_pe, 4),
            'epsilon': round(self.epsilon_acc, 4),
            'q_variance': round(self.q_variance, 6),
            'intention_stability': round(self.intention_stability, 3),
            'weights': {
                'w_a': round(self.w_a, 3),
                'w_b': round(self.w_b, 3),
                'w_c': round(self.w_c, 3),
            },
            'harmony_rate': round(self.harmony_count / max(self.tick_count, 1), 3),
            'total_corrections': self.total_corrections,
        }

    def print_report(self):
        """Print a human-readable Q-Lens report."""
        r = self.report()
        if r.get('status') == 'no_data':
            print("Q-Lens: no data yet")
            return

        print("\n" + "=" * 60)
        print("  Q-LENS STATUS REPORT")
        print("=" * 60)
        print(f"  Ticks:             {r['tick_count']}")
        print(f"  Q(t) avg:          {r['q_total']}")
        print(f"    Q_A (spatial):   {r['q_a']}")
        print(f"    Q_B (temporal):  {r['q_b']}")
        print(f"    Q_C (modal):     {r['q_c']}")
        print(f"  Dominant engine:   {r['dominant_engine']}")
        print(f"  Weights:           A={r['weights']['w_a']} B={r['weights']['w_b']} C={r['weights']['w_c']}")
        print(f"  Intention:         {r['intention_op']}")
        print(f"  Correction:        {r['correction_op']} (rate={r['correction_rate']})")
        print(f"  Q-coherence:       {r['q_coherence']}")
        print(f"  Prediction error:  {r['prediction_error']}")
        print(f"  Epsilon (acc):     {r['epsilon']}")
        print(f"  Q variance:        {r['q_variance']}")
        print(f"  Intent stability:  {r['intention_stability']}")
        print(f"  Harmony rate:      {r['harmony_rate']}")
        print(f"  Total corrections: {r['total_corrections']}")
        print(f"  Intent dist:       {r['intention_distribution']}")
        print("=" * 60)


# ═══════════════════════════════════════════════════════════
# S7  STANDALONE TEST -- Run Q-Lens against TL predictions
# ═══════════════════════════════════════════════════════════

def test_qlens():
    """Test the Q-Lens by feeding it simulated heartbeat ticks."""
    import os, json

    print("=" * 60)
    print("  Q-LENS TEST")
    print("=" * 60)

    # Create Q-Lens
    ql = QLens(w_a=0.35, w_b=0.35, w_c=0.30)

    # Try to load TL for realistic predictions
    tl = None
    try:
        from ck_doing import TransitionLattice
        tl_path = os.path.join(os.path.dirname(__file__),
                               'ck7', 'ck_experience', 'master_tl.json')
        if os.path.exists(tl_path):
            tl = TransitionLattice()
            tl.load(tl_path)
            print(f"  Loaded TL: {tl.sentences_eaten:,} sentences, entropy {tl.entropy():.4f}")
    except:
        print("  No TL available -- using simulated predictions")

    # Simulate 100 heartbeat ticks
    import random
    random.seed(42)

    body_c = 0.7  # Start moderately healthy
    last_bc = HARMONY

    for tick in range(100):
        # Simulate body observation
        body_c += random.gauss(0, 0.03)
        body_c = max(0.1, min(1.0, body_c))

        # Map body_c to phase_b
        if body_c >= 0.85:
            phase_b = HARMONY
        elif body_c >= T_STAR:
            phase_b = BALANCE
        elif body_c >= 0.6:
            phase_b = PROGRESS
        elif body_c >= 0.5:
            phase_b = CHAOS
        elif body_c >= 0.35:
            phase_b = COLLAPSE
        else:
            phase_b = VOID

        # Get TL prediction
        if tl:
            candidates = tl.next_operator(last_bc, -1)
            if candidates:
                phase_d = candidates[0][0]
                pred_prob = candidates[0][1]
            else:
                phase_d = HARMONY
                pred_prob = 0.3
        else:
            phase_d = random.choice([HARMONY, BALANCE, PROGRESS, BREATH])
            pred_prob = 0.4

        # Compose through CL
        try:
            phase_bc = CL[phase_b][phase_d]
        except:
            phase_bc = fuse(phase_b, phase_d)

        # Q-Lens tick
        result = ql.tick(
            phase_b=phase_b,
            phase_d=phase_d,
            phase_bc=phase_bc,
            body_c=body_c,
            predicted_op=phase_d,
            prediction_prob=pred_prob,
            tl_entropy=tl.entropy() if tl else 5.0,
        )

        # Klein bottle: compose Q-Lens with delta-Lens
        actual_op = ql.compose_with_delta(phase_d, pred_prob)

        # Feed back to TL
        if tl:
            ql.feed_delta(tl, phase_bc)

        # Print every 10th tick
        if (tick + 1) % 10 == 0:
            print(f"  Tick {tick+1:3d}: body={body_c:.2f} "
                  f"B={OP_NAMES[phase_b]:8s} D={OP_NAMES[phase_d]:8s} "
                  f"BC={OP_NAMES[phase_bc]:8s} "
                  f"Q={result['q_total']:.3f} "
                  f"intent={OP_NAMES[result['intention_op']]:8s} "
                  f"correct={OP_NAMES[result['correction_op']]:8s}")

        last_bc = phase_bc

    # Final report
    ql.print_report()

    # Verify the Klein bottle is working
    print("\n  --- KLEIN BOTTLE VERIFICATION ---")
    print(f"  Q-Lens ticks:      {ql.tick_count}")
    print(f"  Epsilon accumulated: {ql.epsilon_acc:.4f}")
    print(f"  Q variance:        {ql.q_variance:.6f}")
    print(f"  Corrections/ticks: {ql.total_corrections}/{ql.tick_count}")
    if ql.q_coherence >= T_STAR:
        print(f"  Q-Delta coherence: {ql.q_coherence:.4f} -- ABOVE THRESHOLD")
    else:
        print(f"  Q-Delta coherence: {ql.q_coherence:.4f} -- BELOW THRESHOLD (needs correction)")

    print("\n  Q-LENS TEST COMPLETE")
    print("=" * 60)

    return ql


if __name__ == '__main__':
    test_qlens()
