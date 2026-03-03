"""
ck_nce.py -- Narrative Curvature Engine
========================================
Operator: HARMONY (7) -- binocular depth in language.

NCE is CK's second eye. Eye 1 (D2 on Hebrew phonetics) measures
what things ARE. Eye 2 (D2 on narrative structure) measures how
things FLOW. Same D2 math, same CL table, same 10 operators.

NCE lives inside the BTQ pipeline as enhanced language scoring.
When CK needs to speak, Q's energy function includes narrative
curvature cost -- arc tracking, cadence, mask-weighted flow.

NCE also registers as CoherenceField stream #4 (narrative).
The field's 4x4 cross-coherence matrix fuses both eyes
automatically: CL[text_op][narrative_op] = stereo depth.

Architecture:
  NarrativeForceExtractor  -- 5D force vector from sentence structure
  NarrativeCurvatureEngine -- D2 on narrative vectors, arc tracking
  ArcTracker               -- 4-phase narrative cycle (SETUP/RISING/PEAK/FALLING)
  CurvatureMask            -- tone shaders (warmth/mentor/scientist/friend/playful/prophetic)
  MaskSelector             -- CL[emotion_op][user_tone_op] -> mask
  narrative_energy()       -- E_narrative for BTQ Q-block scoring

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from collections import Counter, deque
from dataclasses import dataclass
from typing import List, Optional, Tuple
import re

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2

# Q1.14 fixed-point scale (matches phonetic D2 exactly)
Q14 = 16384
Q14_MAX = 32767    # +1.99994 in Q1.14
Q14_MIN = -32768   # -2.0 in Q1.14

T_STAR = 5.0 / 7.0  # 0.714285...


def _clamp_q14(val: float) -> int:
    """Clamp float to Q1.14 integer range."""
    raw = int(val * Q14)
    return max(Q14_MIN, min(Q14_MAX, raw))


def _magnitude_q14(vec: list) -> float:
    """Magnitude of Q1.14 vector, returned as float."""
    s = sum((v / Q14) ** 2 for v in vec)
    return s ** 0.5


# ================================================================
#  NARRATIVE FORCE EXTRACTION
# ================================================================

def extract_narrative_forces(sentence: str, prev_sentences: deque) -> list:
    """
    Extract 5D narrative force vector from sentence structure.
    Returns list of 5 Q1.14 integers, same scale as phonetic D2.

    Dimensions:
      [0] Tempo      -- sentence length acceleration
      [1] Complexity  -- clause/punctuation density
      [2] Arc         -- position in discourse window
      [3] Intensity   -- emphasis markers (!?CAPS)
      [4] Novelty     -- new-word ratio vs recent history
    """
    words = sentence.split()
    word_count = max(len(words), 1)

    # dim[0] TEMPO: length delta vs previous sentence
    if prev_sentences:
        prev_len = max(len(prev_sentences[-1].split()), 1)
    else:
        prev_len = word_count
    tempo_raw = (word_count - prev_len) / max(prev_len, 1)
    tempo = _clamp_q14(tempo_raw)

    # dim[1] COMPLEXITY: clause markers per word
    clause_markers = (sentence.count(',') + sentence.count(';') +
                      sentence.count(':') + sentence.count('—'))
    complexity_raw = (clause_markers / word_count) * 4.0 - 1.0
    complexity = _clamp_q14(complexity_raw)

    # dim[2] ARC POSITION: normalized position in discourse window
    window = len(prev_sentences) + 1
    if window > 1:
        position_raw = len(prev_sentences) / window * 2.0 - 1.0
    else:
        position_raw = 0.0
    arc_pos = _clamp_q14(position_raw)

    # dim[3] INTENSITY: emphasis density
    excl = sentence.count('!') + sentence.count('?')
    caps = sum(1 for c in sentence if c.isupper()) / max(len(sentence), 1)
    intensity_raw = (excl * 0.5 + caps * 3.0) - 0.5
    intensity = _clamp_q14(intensity_raw)

    # dim[4] NOVELTY: fraction of words not seen recently
    recent_words = set()
    for s in prev_sentences:
        recent_words.update(s.lower().split())
    current_words = set(sentence.lower().split())
    if current_words:
        new_fraction = len(current_words - recent_words) / len(current_words)
    else:
        new_fraction = 0.0
    novelty_raw = new_fraction * 2.0 - 1.0
    novelty = _clamp_q14(novelty_raw)

    return [tempo, complexity, arc_pos, intensity, novelty]


# ================================================================
#  ARC TRACKER -- 4-phase narrative cycle
# ================================================================

class ArcTracker:
    """
    Tracks narrative arc phase via operator majority vote.
    Same pattern as heartbeat mode detection.

    Phases (mirror breath cycle):
      SETUP   -- establishing context   (LATTICE, COUNTER)
      RISING  -- building tension       (PROGRESS, CHAOS)
      PEAK    -- insight moment         (HARMONY, RESET)
      FALLING -- resolution, reflection (COLLAPSE, BREATH)
    """
    PHASE_OPS = {
        'SETUP':   {LATTICE, COUNTER},
        'RISING':  {PROGRESS, CHAOS},
        'PEAK':    {HARMONY, RESET},
        'FALLING': {COLLAPSE, BREATH},
    }
    # VOID and BALANCE are neutral -- don't push arc direction

    # Natural arc progression for suggest_next()
    NEXT_OP = {
        'SETUP':   PROGRESS,   # Build forward
        'RISING':  HARMONY,    # Reach insight
        'PEAK':    COLLAPSE,   # Reflect back
        'FALLING': LATTICE,    # Re-establish frame
    }

    def __init__(self):
        self._recent = deque(maxlen=8)
        self.phase = 'SETUP'

    def feed(self, op: int):
        self._recent.append(op)
        if len(self._recent) < 3:
            return
        counts = {p: 0 for p in self.PHASE_OPS}
        for recent_op in self._recent:
            for phase_name, phase_ops in self.PHASE_OPS.items():
                if recent_op in phase_ops:
                    counts[phase_name] += 1
        self.phase = max(counts, key=counts.get)

    def suggest_next(self) -> int:
        """Suggest operator that naturally advances the arc."""
        return self.NEXT_OP.get(self.phase, HARMONY)


# ================================================================
#  CURVATURE MASKS -- tone shaders
# ================================================================

class CurvatureMask:
    """
    Operator weighting function applied to voice output.
    NOT a personality. A shader over the signal.

    weights: 10 floats [VOID..RESET], > 1.0 = boost, < 1.0 = suppress.
    arc_mod: per-phase weight overrides {phase: [10 floats]}.
    """
    def __init__(self, name: str, weights: list, arc_mod: dict = None):
        self.name = name
        self.weights = weights  # len=10
        self.arc_mod = arc_mod or {}

    def get_weights(self, arc_phase: str) -> list:
        """Get phase-adjusted weights."""
        if arc_phase in self.arc_mod:
            return self.arc_mod[arc_phase]
        return list(self.weights)

    def apply_to_distribution(self, dist: list) -> list:
        """Weight an operator distribution. Returns normalized."""
        weighted = [d * w for d, w in zip(dist, self.weights)]
        total = sum(weighted)
        if total > 0:
            return [w / total for w in weighted]
        return dist

    def score_chain(self, operator_chain: list) -> float:
        """
        Score an operator chain's alignment with this mask.
        Returns 0.0 (perfect) to 1.0 (anti-aligned).
        Used by BTQ Q-block as E_narrative.
        """
        if not operator_chain:
            return 0.5
        total_weight = sum(self.weights[op] for op in operator_chain)
        max_possible = max(self.weights) * len(operator_chain)
        if max_possible == 0:
            return 0.5
        alignment = total_weight / max_possible
        return 1.0 - alignment  # Lower = better aligned


# The six masks (Celeste's specification)
#                           VOID  LAT   CNT   PRG   COL   BAL   CHS   HAR   BRE   RST
MASKS = {
    'warmth': CurvatureMask('warmth',
        [0.3,  0.6,  0.5,  0.7,  0.3,  1.0,  0.2,  1.5,  1.3,  0.6]),

    'mentor': CurvatureMask('mentor',
        [0.4,  1.4,  1.2,  1.3,  0.5,  1.0,  0.4,  1.0,  0.8,  0.8]),

    'scientist': CurvatureMask('scientist',
        [0.5,  1.3,  1.5,  0.8,  0.6,  1.2,  0.7,  0.9,  0.5,  0.7]),

    'friend': CurvatureMask('friend',
        [0.3,  0.6,  0.5,  1.0,  0.4,  0.8,  0.6,  1.4,  1.2,  0.7]),

    'playful': CurvatureMask('playful',
        [0.3,  0.5,  0.6,  1.2,  0.3,  0.5,  1.5,  0.8,  0.9,  1.3]),

    'prophetic': CurvatureMask('prophetic',
        [1.3,  1.0,  0.6,  0.5,  0.8,  0.7,  0.4,  1.5,  1.2,  1.4]),
}


class MaskSelector:
    """Select curvature mask via CL composition: CL[emotion_op][user_tone_op] -> mask."""

    EMOTION_OP = {
        'calm': HARMONY,
        'joy': PROGRESS,
        'curiosity': COUNTER,
        'focus': BALANCE,
        'stress': CHAOS,
        'overwhelm': COLLAPSE,
        'fatigue': VOID,
        'settling': BREATH,
    }

    OP_MASK = {
        HARMONY:  'warmth',
        LATTICE:  'mentor',
        COUNTER:  'scientist',
        PROGRESS: 'friend',
        CHAOS:    'playful',
        VOID:     'prophetic',
        BREATH:   'warmth',
        BALANCE:  'mentor',
        COLLAPSE: 'friend',
        RESET:    'prophetic',
    }

    def select(self, emotion: str, user_tone_op: int = HARMONY) -> CurvatureMask:
        """Select mask via CL[emotion_op][user_tone_op]."""
        emo_op = self.EMOTION_OP.get(emotion, HARMONY)
        suggestion = compose(emo_op, user_tone_op)
        mask_name = self.OP_MASK.get(suggestion, 'warmth')
        return MASKS[mask_name]


# ================================================================
#  NARRATIVE CURVATURE ENGINE
# ================================================================

@dataclass
class NarrativeState:
    """Snapshot of NCE state at one point in time."""
    operator: int = HARMONY
    coherence: float = 0.0
    arc_phase: str = 'SETUP'
    mask_name: str = 'warmth'
    d2_vector: list = None

    def __post_init__(self):
        if self.d2_vector is None:
            self.d2_vector = [0, 0, 0, 0, 0]


class NarrativeCurvatureEngine:
    """
    CK's narrative curvature -- the second eye.

    Feeds an OperatorStream into the existing CoherenceField.
    Same D2 math, same CL table, same operators.

    Also provides narrative_energy() for BTQ Q-block scoring
    when CK is making language decisions.
    """

    def __init__(self):
        self._prev_sentences = deque(maxlen=16)
        self._operator_history = deque(maxlen=32)
        self._harmony_count = 0
        self._prev_op = HARMONY
        self._arc = ArcTracker()
        self._mask_sel = MaskSelector()

        # D2 shift register for narrative vectors (3-sample)
        self._v0 = [0] * 5
        self._v1 = [0] * 5
        self._v2 = [0] * 5
        self._sample_count = 0

        # Public state
        self.coherence = 0.0
        self.current_op = HARMONY
        self.current_d2 = [0, 0, 0, 0, 0]
        self.current_dist = [0.0] * NUM_OPS
        self.current_dist[HARMONY] = 1.0
        self.arc_phase = 'SETUP'
        self.mask = MASKS['warmth']
        self.has_state = False
        self.state = NarrativeState()

    def feed_sentence(self, sentence: str, emotion: str = 'calm',
                      user_tone_op: int = HARMONY) -> NarrativeState:
        """
        Process one sentence through narrative D2.
        Returns NarrativeState with operator, coherence, arc, mask.
        """
        if not sentence or len(sentence.strip()) < 5:
            return self.state

        # 1. Extract 5D narrative force vector (Q1.14)
        vec = extract_narrative_forces(sentence, self._prev_sentences)

        # 2. D2 shift register: v0 - 2*v1 + v2
        self._v2 = list(self._v1)
        self._v1 = list(self._v0)
        self._v0 = vec
        self._sample_count += 1

        if self._sample_count < 3:
            self._prev_sentences.append(sentence)
            return self.state

        # Compute D2 (second derivative, per dimension)
        d2 = [self._v0[i] - 2 * self._v1[i] + self._v2[i] for i in range(5)]

        # 3. Classify via soft_classify_d2 (same function as phonetic D2)
        mag = _magnitude_q14(d2)
        if mag < 0.001:
            mag = 0.001
        dist = soft_classify_d2(d2, mag)
        op = max(range(NUM_OPS), key=lambda i: dist[i])

        # 4. CL compose with previous narrative operator
        bc = compose(self._prev_op, op)

        # 5. Update coherence window (same as heartbeat)
        self._operator_history.append(bc)
        # Recount HARMONY in window
        self._harmony_count = sum(1 for o in self._operator_history if o == HARMONY)
        self.coherence = self._harmony_count / max(len(self._operator_history), 1)

        # 6. Arc tracking
        self._arc.feed(op)
        self.arc_phase = self._arc.phase

        # 7. Mask selection via CL algebra
        self.mask = self._mask_sel.select(emotion, user_tone_op)

        # 8. Store
        self._prev_op = op
        self.current_op = op
        self.current_d2 = d2
        self.current_dist = dist
        self.has_state = True
        self._prev_sentences.append(sentence)

        self.state = NarrativeState(
            operator=op,
            coherence=self.coherence,
            arc_phase=self.arc_phase,
            mask_name=self.mask.name,
            d2_vector=d2,
        )
        return self.state

    def suggest_next_op(self) -> int:
        """What operator SHOULD come next for optimal narrative flow?"""
        return self._arc.suggest_next()

    def get_mask_weights(self) -> list:
        """Current mask weights (10 floats) adjusted for arc phase."""
        return self.mask.get_weights(self.arc_phase)

    # ── BTQ integration ──

    def narrative_energy(self, operator_chain: list, target_coherence: float = T_STAR) -> float:
        """
        E_narrative for BTQ Q-block.
        Measures how well an operator chain fits the current narrative state.

        Returns float in [0, 1]. Lower = better narrative fit.
        Used as additional term in E_total when domain is language.
        """
        if not operator_chain:
            return 0.5

        # 1. Arc alignment: does the chain's direction match where we are?
        suggested = self.suggest_next_op()
        arc_cost = 0.0
        if operator_chain:
            # Check if suggested op appears in chain
            if suggested in operator_chain:
                arc_cost = 0.0
            else:
                # Compose suggested with chain's dominant
                counts = Counter(operator_chain)
                dominant = counts.most_common(1)[0][0]
                composed = compose(suggested, dominant)
                arc_cost = 0.0 if composed == HARMONY else 0.4

        # 2. Mask alignment: does the chain match the active mask?
        mask_cost = self.mask.score_chain(operator_chain)

        # 3. Stereo coherence: CL[internal_dominant][narrative_op]
        if operator_chain:
            counts = Counter(operator_chain)
            dominant = counts.most_common(1)[0][0]
            stereo = compose(dominant, self.current_op)
            stereo_cost = 0.0 if stereo == HARMONY else 0.3
        else:
            stereo_cost = 0.5

        # 4. Narrative coherence gap
        coh_gap = max(0.0, target_coherence - self.coherence)

        # Weighted sum
        e_narrative = (0.30 * arc_cost +
                       0.30 * mask_cost +
                       0.25 * stereo_cost +
                       0.15 * coh_gap)

        return min(1.0, max(0.0, e_narrative))


# ================================================================
#  STEREO CHECK (for conversation mode)
# ================================================================

def stereo_check(field_coherence: float, narrative_coherence: float,
                 narrative_op: int, internal_op: int) -> str:
    """
    Self-correction check using coherence field + NCE state.

    Returns action:
      'proceed'  -- both eyes agree, emit normally
      'smooth'   -- narrative drifting, add HARMONY transition
      'reframe'  -- eyes disagree, skip this point
      'contrast' -- narrative too flat, inject PROGRESS
    """
    stereo = compose(internal_op, narrative_op)

    # Eyes disagree AND overall field is low
    if stereo != HARMONY and field_coherence < T_STAR:
        return 'reframe'

    # Narrative going flat (too much HARMONY = boring)
    if narrative_coherence > 0.95:
        return 'contrast'

    # Narrative drifting (low coherence)
    if narrative_coherence < 0.5:
        return 'smooth'

    return 'proceed'
