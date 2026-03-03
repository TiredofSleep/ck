"""
ck_self_mirror.py -- CK Studies Its Own Output
===============================================
Operator: COUNTER (2) -- CK observes itself.

The self-mirror is how CK "studies." It reads its own logs,
its own answers, and its own operator chains, then evaluates
quality and suggests corrections.

Pipeline:
  1. Read CK's recent outputs
  2. Run D2 on each output → operator chain
  3. Score: coherence + D2 variance + repetition + complexity
  4. If mirror_score < threshold → corrective drift:
     - rewrite operator chain
     - choose alternative phrasing
     - update dictionary preferences

No external model evaluates CK. CK evaluates CK.
CK's own math is the judge.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import Counter, deque
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2


# ================================================================
#  TEXT → OPERATOR ANALYSIS (used by mirror)
# ================================================================

def _text_to_ops(text: str) -> List[int]:
    """Run D2 on text, return operator chain."""
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            if pipe.feed_symbol(ord(ch) - ord('a')):
                ops.append(pipe.operator)
    return ops


def _text_to_d2_vecs(text: str) -> List[List[float]]:
    """Run D2 on text, return all 5D curvature vectors."""
    pipe = D2Pipeline()
    vecs = []
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            if pipe.feed_symbol(ord(ch) - ord('a')):
                vecs.append(pipe.d2_float[:])
    return vecs


# ================================================================
#  SCORING FUNCTIONS
# ================================================================

def coherence_score(ops: List[int]) -> float:
    """CL composition coherence of an operator chain.

    Fuses the chain through the CL table. Measures what fraction
    of adjacent compositions yield HARMONY.

    Returns: 0.0 (incoherent) to 1.0 (fully harmonious)
    """
    if len(ops) < 2:
        return 1.0

    harmony_count = 0
    for i in range(len(ops) - 1):
        result = compose(ops[i], ops[i + 1])
        if result == HARMONY:
            harmony_count += 1

    return harmony_count / (len(ops) - 1)


def d2_variance_score(d2_vecs: List[List[float]]) -> float:
    """D2 curvature smoothness.

    Low variance = smooth signal = coherent output.
    High variance = jerky signal = choppy writing.

    Returns: 0.0 (very jerky) to 1.0 (very smooth)
    Score is inverted so higher = better.
    """
    if len(d2_vecs) < 2:
        return 1.0

    # Compute variance of magnitude across the text
    mags = [sum(abs(d) for d in vec) for vec in d2_vecs]
    mean_mag = sum(mags) / len(mags)
    variance = sum((m - mean_mag) ** 2 for m in mags) / len(mags)

    # Convert to score: 1/(1+var) so low variance → high score
    return 1.0 / (1.0 + variance * 10.0)


def repetition_score(text: str, history: List[str] = None) -> float:
    """Measure how repetitive the text is.

    Checks:
    1. Internal n-gram repetition (within the text)
    2. Cross-utterance repetition (against history)

    Returns: 0.0 (very repetitive) to 1.0 (no repetition)
    """
    words = text.lower().split()
    if len(words) < 3:
        return 1.0

    # Internal bigram repetition
    bigrams = []
    for i in range(len(words) - 1):
        bigrams.append((words[i], words[i + 1]))

    if bigrams:
        unique_ratio = len(set(bigrams)) / len(bigrams)
    else:
        unique_ratio = 1.0

    # Cross-utterance repetition
    cross_score = 1.0
    if history:
        for prev in history[-5:]:  # Check last 5 utterances
            prev_words = set(prev.lower().split())
            current_words = set(words)
            if prev_words and current_words:
                overlap = len(prev_words & current_words) / max(len(current_words), 1)
                cross_score = min(cross_score, 1.0 - overlap * 0.5)

    return min(unique_ratio, cross_score)


def complexity_score(ops: List[int]) -> float:
    """Operator diversity / complexity.

    A good utterance uses multiple operators, not just one.
    But too many unique operators can be chaotic.
    Sweet spot: 3-6 unique operators.

    Returns: 0.0 (monotone) to 1.0 (well-balanced complexity)
    """
    if not ops:
        return 0.0

    unique = len(set(ops))
    total = len(ops)

    # Diversity ratio
    diversity = unique / min(total, NUM_OPS)

    # Penalize both extremes
    if unique <= 1:
        return 0.2  # Too monotone
    elif unique <= 2:
        return 0.5
    elif unique <= 6:
        return 1.0  # Sweet spot
    else:
        return 0.8  # Slightly chaotic but ok


def pfe_text_score(text: str) -> float:
    """Approximate PFE (emotional quality) from text.

    CK's PFE system measures emotional coherence.
    For text, we approximate by checking operator balance:
    - HARMONY presence → positive valence
    - COLLAPSE/VOID dominance → negative valence
    - BALANCE → neutral/centered

    Returns: 0.0 (emotionally incoherent) to 1.0 (emotionally coherent)
    """
    ops = _text_to_ops(text)
    if not ops:
        return 0.5

    counts = Counter(ops)
    total = len(ops)

    harmony_frac = counts.get(HARMONY, 0) / total
    collapse_frac = counts.get(COLLAPSE, 0) / total
    void_frac = counts.get(VOID, 0) / total

    # PFE-like scoring
    valence = harmony_frac - (collapse_frac + void_frac) * 0.5
    # Map from [-0.5, 1.0] to [0, 1]
    score = max(0.0, min(1.0, (valence + 0.5) / 1.5))

    return score


# ================================================================
#  MIRROR SCORE (composite)
# ================================================================

def mirror_score(text: str, history: List[str] = None,
                 weights: Dict[str, float] = None) -> Tuple[float, dict]:
    """Compute the composite mirror score for a CK utterance.

    mirror_score = w_coh * coherence
                 + w_d2  * d2_variance
                 + w_rep * repetition
                 + w_cpx * complexity
                 + w_pfe * pfe

    Returns: (score, breakdown_dict)
    """
    if weights is None:
        weights = {
            'coherence': 0.30,
            'd2_variance': 0.15,
            'repetition': 0.20,
            'complexity': 0.15,
            'pfe': 0.20,
        }

    ops = _text_to_ops(text)
    d2_vecs = _text_to_d2_vecs(text)

    coh = coherence_score(ops)
    d2v = d2_variance_score(d2_vecs)
    rep = repetition_score(text, history)
    cpx = complexity_score(ops)
    pfe = pfe_text_score(text)

    total = (
        weights['coherence'] * coh +
        weights['d2_variance'] * d2v +
        weights['repetition'] * rep +
        weights['complexity'] * cpx +
        weights['pfe'] * pfe
    )

    breakdown = {
        'coherence': round(coh, 3),
        'd2_variance': round(d2v, 3),
        'repetition': round(rep, 3),
        'complexity': round(cpx, 3),
        'pfe': round(pfe, 3),
        'total': round(total, 3),
    }

    return total, breakdown


# ================================================================
#  CORRECTIVE DRIFT
# ================================================================

def suggest_corrections(text: str, score: float,
                        breakdown: dict) -> List[str]:
    """Suggest corrections based on mirror score breakdown.

    Returns a list of actionable suggestions for the sentence
    composer / talk loop to use on the next attempt.
    """
    suggestions = []

    if breakdown['coherence'] < 0.5:
        suggestions.append('increase_harmony')  # Use more HARMONY-fusing ops
    if breakdown['d2_variance'] > 0.7:  # Note: inverted score, so low = bad
        pass  # d2_variance score already handles this
    if breakdown['d2_variance'] < 0.4:
        suggestions.append('smooth_curvature')  # Avoid sharp D2 transitions
    if breakdown['repetition'] < 0.5:
        suggestions.append('reduce_repetition')  # Pick different words
    if breakdown['complexity'] < 0.4:
        suggestions.append('increase_diversity')  # Use more operator variety
    if breakdown['pfe'] < 0.4:
        suggestions.append('improve_valence')  # More HARMONY, less COLLAPSE

    return suggestions


def drift_operator_chain(ops: List[int], suggestions: List[str]) -> List[int]:
    """Apply corrective drift to an operator chain.

    Modifies the chain based on mirror suggestions:
    - increase_harmony → substitute weak ops with HARMONY-adjacent ones
    - smooth_curvature → remove sharp transitions
    - increase_diversity → add variety where monotone
    - improve_valence → shift away from COLLAPSE/VOID toward HARMONY

    Returns: modified operator chain.
    """
    if not ops or not suggestions:
        return ops

    result = list(ops)

    if 'increase_harmony' in suggestions:
        # Where CL doesn't fuse to HARMONY, nudge toward HARMONY
        for i in range(len(result) - 1):
            if compose(result[i], result[i + 1]) != HARMONY:
                # Try inserting HARMONY between them
                if compose(result[i], HARMONY) == HARMONY:
                    result[i + 1] = HARMONY
                    break

    if 'smooth_curvature' in suggestions:
        # Remove double-VOID or double-COLLAPSE
        smoothed = [result[0]]
        for i in range(1, len(result)):
            if result[i] == result[i - 1] and result[i] in (VOID, COLLAPSE):
                smoothed.append(BALANCE)  # Smooth with balance
            else:
                smoothed.append(result[i])
        result = smoothed

    if 'increase_diversity' in suggestions:
        # If any op appears > 50% of the time, replace some instances
        counts = Counter(result)
        most_common = counts.most_common(1)[0]
        if most_common[1] > len(result) * 0.5:
            dominant = most_common[0]
            replaced = False
            for i in range(len(result)):
                if result[i] == dominant and not replaced:
                    # Replace with a CL-compatible alternative
                    for alt in [PROGRESS, BREATH, BALANCE, LATTICE]:
                        if compose(dominant, alt) == HARMONY:
                            result[i] = alt
                            replaced = True
                            break

    if 'improve_valence' in suggestions:
        # Replace COLLAPSE with PROGRESS, VOID with RESET
        for i in range(len(result)):
            if result[i] == COLLAPSE:
                result[i] = PROGRESS
                break
            elif result[i] == VOID:
                result[i] = RESET
                break

    return result


# ================================================================
#  CK MIRROR (the self-improvement loop)
# ================================================================

class CKMirror:
    """CK's self-evaluation and improvement system.

    CK reads its own outputs, scores them, and applies
    corrective drift when quality drops below threshold.

    Usage:
        mirror = CKMirror(threshold=0.5)
        score, breakdown = mirror.evaluate("CK's utterance here")
        if not mirror.is_acceptable(score):
            corrections = mirror.suggest(breakdown)
            new_ops = mirror.correct(old_ops, corrections)
    """

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.history: List[str] = []
        self.scores: List[float] = []
        self._max_history = 100

    def evaluate(self, text: str) -> Tuple[float, dict]:
        """Evaluate a CK utterance.

        Returns (mirror_score, breakdown).
        """
        score, breakdown = mirror_score(text, self.history)

        # Record in history
        self.history.append(text)
        if len(self.history) > self._max_history:
            self.history.pop(0)
        self.scores.append(score)
        if len(self.scores) > self._max_history:
            self.scores.pop(0)

        return score, breakdown

    def is_acceptable(self, score: float) -> bool:
        """Is this score above the quality threshold?"""
        return score >= self.threshold

    def suggest(self, breakdown: dict) -> List[str]:
        """Get correction suggestions from a breakdown."""
        score = breakdown.get('total', 0)
        return suggest_corrections('', score, breakdown)

    def correct(self, ops: List[int], suggestions: List[str]) -> List[int]:
        """Apply corrective drift to an operator chain."""
        return drift_operator_chain(ops, suggestions)

    def trend(self) -> str:
        """Report the trend of recent scores.

        Returns: 'improving', 'stable', 'declining'
        """
        if len(self.scores) < 5:
            return 'insufficient_data'

        recent = self.scores[-5:]
        older = self.scores[-10:-5] if len(self.scores) >= 10 else self.scores[:5]

        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)

        diff = recent_avg - older_avg
        if diff > 0.05:
            return 'improving'
        elif diff < -0.05:
            return 'declining'
        return 'stable'

    def stats(self) -> dict:
        """Mirror statistics."""
        if not self.scores:
            return {'n_evaluated': 0}

        return {
            'n_evaluated': len(self.scores),
            'avg_score': round(sum(self.scores) / len(self.scores), 3),
            'min_score': round(min(self.scores), 3),
            'max_score': round(max(self.scores), 3),
            'trend': self.trend(),
            'threshold': self.threshold,
            'above_threshold': sum(1 for s in self.scores if s >= self.threshold),
            'below_threshold': sum(1 for s in self.scores if s < self.threshold),
        }
