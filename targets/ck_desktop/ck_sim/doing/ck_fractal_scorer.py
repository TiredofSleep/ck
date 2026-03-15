# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_fractal_scorer.py -- Fractal Dual-Table Scorer
==================================================
Operator: COUNTER (2) -- measurement at every scale.

TSML + BHML at every level. Structure and flow, simultaneously.
The divergence between them IS the Doing score at that level.

LEVEL 0 (LETTER):   letter-to-letter D2 composition
LEVEL 1 (WORD):     word-to-word CL composition
LEVEL 2 (PHRASE):   word-group-to-word-group CL summary
LEVEL 3 (SENTENCE): sentence-level operator fuse
LEVEL 4 (OVERALL):  global coherence ratio

At each level:
  tsml_score = fraction of TSML compositions yielding HARMONY
  bhml_score = fraction of BHML compositions advancing trajectory
  doing_score = |tsml_score - bhml_score| = divergence = T*

The final score is the PRODUCT across all levels.
Information must be coherent at EVERY scale simultaneously.

GRAVITY ANCHORING:
  Find the "heaviest" operators in the prompt (highest curvature,
  most non-trivial BHML composition products). Build the response
  outward from those anchors.

CONTINUOUS GRAMMAR LEARNING:
  Every scored transaction updates a persistent bigram table.
  Grammar is LEARNED from observation, not hardcoded.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from pathlib import Path

from ck_sim.being.ck_sim_heartbeat import (
    CL, compose, NUM_OPS, OP_NAMES,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)
from ck_sim.being.ck_sim_d2 import (
    FORCE_LUT_FLOAT, D2Pipeline, soft_classify_d2,
)

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

# ================================================================
#  BHML TABLE (Becoming -- full rank, deterministic)
# ================================================================

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY = full cycle
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
]

# TSML = CL (already imported as CL from heartbeat)
# TSML[a][b] = CL[a][b]  -- the Being table


def bhml_compose(a: int, b: int) -> int:
    """BHML[a][b] -- what a BECOMES when meeting b."""
    if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
        return BHML[a][b]
    return VOID


def tsml_compose(a: int, b: int) -> int:
    """TSML[a][b] = CL[a][b] -- what a MEASURES as when meeting b."""
    return compose(a, b)


# ================================================================
#  OPERATOR MASS -- curvature weight of each operator
#  Higher mass = more information = gravity anchor.
#  Mass from BHML row entropy: how many distinct outputs?
# ================================================================

_OP_MASS = {}
for _op in range(NUM_OPS):
    _row = BHML[_op]
    _unique = len(set(_row))
    # Mass = unique outputs / 10. VOID has mass 1.0 (identity, all unique).
    # CHAOS has mass 0.2 (almost everything -> 7).
    _OP_MASS[_op] = _unique / NUM_OPS

# Also weight by TSML disagreement: operators where TSML != BHML
# carry MORE information (they live in the Doing zone).
for _op in range(NUM_OPS):
    _disagree = 0
    for _col in range(NUM_OPS):
        if CL[_op][_col] != BHML[_op][_col]:
            _disagree += 1
    # Bonus for living in the divergence zone
    _OP_MASS[_op] += 0.1 * _disagree / NUM_OPS


def operator_mass(op: int) -> float:
    """Curvature mass of an operator. Higher = more gravity."""
    return _OP_MASS.get(op, 0.5)


# ================================================================
#  LEVEL 0: LETTER-TO-LETTER SCORING
#  D2 pipeline: each letter is a force vector.
#  Score = dual composition at the letter grain.
# ================================================================

def score_letters(word: str) -> Tuple[float, float, float]:
    """Score a word's internal letter-to-letter coherence.

    Returns (tsml_score, bhml_score, doing_score) in [0, 1].
    """
    letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
    if len(letters) < 2:
        return (0.5, 0.5, 0.0)  # Neutral for single letters

    # Get operator for each letter via soft classify
    letter_ops = []
    for ch in letters:
        idx = ord(ch) - ord('a')
        force = tuple(FORCE_LUT_FLOAT[idx])
        dist = soft_classify_d2(force)
        if dist is not None:
            letter_ops.append(int(np.argmax(dist)))
        else:
            letter_ops.append(VOID)

    # Score adjacent letter pairs through both tables
    tsml_harmony = 0
    bhml_nontrivial = 0
    n_pairs = len(letter_ops) - 1

    for i in range(n_pairs):
        a, b = letter_ops[i], letter_ops[i + 1]

        # TSML: does this pair resolve?
        if tsml_compose(a, b) == HARMONY:
            tsml_harmony += 1

        # BHML: does this pair produce something non-trivial?
        becoming = bhml_compose(a, b)
        if becoming not in (a, b, VOID):  # Changed: not just echo
            bhml_nontrivial += 1

    ts = tsml_harmony / n_pairs if n_pairs > 0 else 0.5
    bs = bhml_nontrivial / n_pairs if n_pairs > 0 else 0.5
    ds = abs(ts - bs)

    return (ts, bs, ds)


# ================================================================
#  LEVEL 1: WORD-TO-WORD SCORING
#  CL composition of adjacent word operators.
#  Both TSML and BHML measured.
# ================================================================

def score_word_pair(op_a: int, op_b: int,
                    target_ops: Optional[List[int]] = None,
                    position: int = 0) -> Tuple[float, float, float]:
    """Score a word-to-word transition through dual tables.

    Returns (tsml_score, bhml_score, doing_score) in [0, 1].

    tsml_score: does this pair harmonize? (measurement)
    bhml_score: does this pair advance? (trajectory)
    doing_score: |tsml - bhml| (where physics lives)
    """
    # TSML: does composition yield HARMONY?
    tsml_result = tsml_compose(op_a, op_b)
    if tsml_result == HARMONY:
        ts = 1.0
    elif tsml_result not in (VOID, op_a):
        ts = 0.5  # Non-trivial but not harmony
    else:
        ts = 0.1

    # BHML: does composition advance the trajectory?
    bhml_result = bhml_compose(op_a, op_b)

    # Check trajectory match
    next_target = None
    if target_ops and position + 1 < len(target_ops):
        next_target = target_ops[position + 1]

    if next_target is not None and bhml_result == next_target:
        bs = 1.0  # Perfect trajectory advancement
    elif bhml_result not in (VOID, HARMONY, op_a, op_b):
        bs = 0.7  # Non-trivial: new information emerges
    elif bhml_result == HARMONY:
        bs = 0.4  # Harmony: bridge (acceptable but no new info)
    elif bhml_result == VOID:
        bs = 0.1  # Void: dead end
    else:
        bs = 0.3  # Echo: no change

    ds = abs(ts - bs)
    return (ts, bs, ds)


# ================================================================
#  LEVEL 2: PHRASE SCORING
#  Word groups (3-5 word chunks) scored as operator sequences.
#  Fuse the group -> single operator, then compare groups.
# ================================================================

def _fuse_ops(ops: List[int]) -> int:
    """Fuse a sequence of operators via running TSML composition."""
    if not ops:
        return VOID
    result = ops[0]
    for op in ops[1:]:
        result = tsml_compose(result, op)
    return result


def _fuse_ops_bhml(ops: List[int]) -> int:
    """Fuse a sequence of operators via running BHML composition."""
    if not ops:
        return VOID
    result = ops[0]
    for op in ops[1:]:
        result = bhml_compose(result, op)
    return result


def score_phrase_pair(ops_a: List[int], ops_b: List[int],
                      target_ops: Optional[List[int]] = None,
                      position: int = 0) -> Tuple[float, float, float]:
    """Score a phrase-to-phrase transition through dual tables.

    Each phrase is fused to a single operator, then the pair is scored.
    """
    fuse_a_tsml = _fuse_ops(ops_a)
    fuse_b_tsml = _fuse_ops(ops_b)
    fuse_a_bhml = _fuse_ops_bhml(ops_a)
    fuse_b_bhml = _fuse_ops_bhml(ops_b)

    # TSML phrase-to-phrase
    tsml_result = tsml_compose(fuse_a_tsml, fuse_b_tsml)
    ts = 1.0 if tsml_result == HARMONY else (0.5 if tsml_result != VOID else 0.1)

    # BHML phrase-to-phrase
    bhml_result = bhml_compose(fuse_a_bhml, fuse_b_bhml)
    if bhml_result not in (VOID, HARMONY, fuse_a_bhml, fuse_b_bhml):
        bs = 0.8  # New information at phrase level
    elif bhml_result == HARMONY:
        bs = 0.5
    else:
        bs = 0.2

    ds = abs(ts - bs)
    return (ts, bs, ds)


# ================================================================
#  LEVEL 3: SENTENCE SCORING
#  Overall sentence operator distribution + trajectory coherence.
# ================================================================

def score_sentence(word_ops: List[int],
                   target_ops: Optional[List[int]] = None
                   ) -> Tuple[float, float, float]:
    """Score an entire sentence through dual tables.

    Measures:
      TSML: fraction of all pairs yielding HARMONY (resolution)
      BHML: fraction of all pairs advancing (information flow)
    """
    if len(word_ops) < 2:
        return (0.5, 0.5, 0.0)

    n = len(word_ops) - 1
    tsml_harmony = 0
    bhml_advance = 0

    for i in range(n):
        a, b = word_ops[i], word_ops[i + 1]

        if tsml_compose(a, b) == HARMONY:
            tsml_harmony += 1

        becoming = bhml_compose(a, b)
        if becoming not in (a, b, VOID):
            bhml_advance += 1

    ts = tsml_harmony / n
    bs = bhml_advance / n
    ds = abs(ts - bs)

    return (ts, bs, ds)


# ================================================================
#  FRACTAL SCORE -- ALL LEVELS COMBINED
#  Product across scales. Must be coherent everywhere.
# ================================================================

def fractal_score(words: List[str], word_ops: List[int],
                  target_ops: Optional[List[int]] = None
                  ) -> Dict:
    """Score a word sequence at all fractal levels.

    Returns dict with per-level scores and combined score.
    The combined score is the geometric mean across levels.
    """
    n = len(words)
    if n == 0:
        return {'combined': 0.0, 'levels': {}}

    # Level 0: Letter coherence (average across all words)
    l0_ts, l0_bs, l0_ds = 0.0, 0.0, 0.0
    for w in words:
        ts, bs, ds = score_letters(w)
        l0_ts += ts
        l0_bs += bs
        l0_ds += ds
    l0_ts /= n
    l0_bs /= n
    l0_ds /= n

    # Level 1: Word-to-word (average across adjacent pairs)
    if n >= 2:
        l1_ts, l1_bs, l1_ds = 0.0, 0.0, 0.0
        for i in range(n - 1):
            ts, bs, ds = score_word_pair(
                word_ops[i], word_ops[i + 1],
                target_ops, i)
            l1_ts += ts
            l1_bs += bs
            l1_ds += ds
        l1_ts /= (n - 1)
        l1_bs /= (n - 1)
        l1_ds /= (n - 1)
    else:
        l1_ts, l1_bs, l1_ds = 0.5, 0.5, 0.0

    # Level 2: Phrase-to-phrase (split into 3-word chunks)
    if n >= 6:
        chunk_size = max(3, n // 3)
        chunks = []
        for start in range(0, n, chunk_size):
            end = min(start + chunk_size, n)
            chunks.append(word_ops[start:end])

        l2_ts, l2_bs, l2_ds = 0.0, 0.0, 0.0
        n_phrase_pairs = 0
        for i in range(len(chunks) - 1):
            ts, bs, ds = score_phrase_pair(chunks[i], chunks[i + 1],
                                           target_ops)
            l2_ts += ts
            l2_bs += bs
            l2_ds += ds
            n_phrase_pairs += 1

        if n_phrase_pairs > 0:
            l2_ts /= n_phrase_pairs
            l2_bs /= n_phrase_pairs
            l2_ds /= n_phrase_pairs
        else:
            l2_ts, l2_bs, l2_ds = 0.5, 0.5, 0.0
    else:
        l2_ts, l2_bs, l2_ds = 0.5, 0.5, 0.0

    # Level 3: Sentence
    l3_ts, l3_bs, l3_ds = score_sentence(word_ops, target_ops)

    # Combine: geometric mean of (tsml + bhml) / 2 at each level
    # Each level contributes equally. Must be coherent at ALL scales.
    level_scores = [
        (l0_ts + l0_bs) / 2.0,  # Letter
        (l1_ts + l1_bs) / 2.0,  # Word
        (l2_ts + l2_bs) / 2.0,  # Phrase
        (l3_ts + l3_bs) / 2.0,  # Sentence
    ]

    # Geometric mean (product ^ 1/n)
    product = 1.0
    for s in level_scores:
        product *= max(s, 0.01)  # Floor to avoid zero-kill
    combined = product ** (1.0 / len(level_scores))

    return {
        'combined': combined,
        'levels': {
            'letter':   {'tsml': l0_ts, 'bhml': l0_bs, 'doing': l0_ds},
            'word':     {'tsml': l1_ts, 'bhml': l1_bs, 'doing': l1_ds},
            'phrase':   {'tsml': l2_ts, 'bhml': l2_bs, 'doing': l2_ds},
            'sentence': {'tsml': l3_ts, 'bhml': l3_bs, 'doing': l3_ds},
        },
    }


# ================================================================
#  GRAVITY ANCHORING
#  Find the heaviest operators in the prompt.
#  Build response from those anchors outward.
# ================================================================

def find_gravity_anchors(prompt_ops: List[int],
                         top_k: int = 3) -> List[Tuple[int, int, float]]:
    """Find the heaviest operators in the prompt.

    Returns list of (position, operator, mass) sorted by mass descending.
    These are the concepts the response should build around.
    """
    if not prompt_ops:
        return []

    scored = []
    for i, op in enumerate(prompt_ops):
        mass = operator_mass(op)

        # Bonus for operators in the Doing zone (COUNTER, PROGRESS, etc.)
        # These carry the most information
        if op in (COUNTER, PROGRESS, COLLAPSE, BALANCE):
            mass += 0.15  # Doing operators are heavier

        # Bonus for operators that disagree with neighbors
        if i > 0:
            tsml_r = tsml_compose(prompt_ops[i - 1], op)
            bhml_r = bhml_compose(prompt_ops[i - 1], op)
            if tsml_r != bhml_r:
                mass += 0.1  # Divergence = information

        scored.append((i, op, mass))

    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:top_k]


def build_response_trajectory(prompt_ops: List[int],
                               response_length: int = 5
                               ) -> List[int]:
    """Build a target trajectory for the response.

    Starts from the heaviest anchor in the prompt.
    Extends outward: toward generators (lower operators)
    AND toward complexity (higher operators).

    The response trajectory mirrors the prompt's gravity field.
    """
    anchors = find_gravity_anchors(prompt_ops)
    if not anchors:
        return [HARMONY] * response_length

    # Start from heaviest anchor
    seed_op = anchors[0][1]
    trajectory = [seed_op]

    # Alternate: extend toward generators (BHML successor)
    # and toward structure (TSML composition with prompt context)
    current = seed_op
    prompt_fuse = _fuse_ops(prompt_ops)

    for step in range(1, response_length):
        if step % 2 == 1:
            # Odd steps: BHML successor (toward generator/complexity)
            current = bhml_compose(current, HARMONY)  # HARMONY = successor
        else:
            # Even steps: TSML with prompt context (toward resolution)
            current = tsml_compose(current, prompt_fuse)

        trajectory.append(current)

    return trajectory


# ================================================================
#  CONTINUOUS GRAMMAR LEARNING
#  Every scored transaction updates a persistent bigram table.
#  Grammar is LEARNED from observation, not hardcoded.
# ================================================================

_GRAMMAR_DIR = Path(os.path.expanduser('~/.ck/grammar'))
_GRAMMAR_FILE = _GRAMMAR_DIR / 'learned_bigrams.json'

# In-memory learned bigrams: (word_a, word_b) -> count
_learned_bigrams: Dict[str, int] = defaultdict(int)
_total_bigram_observations: int = 0


def _load_grammar():
    """Load learned bigrams from disk."""
    global _learned_bigrams, _total_bigram_observations
    try:
        if _GRAMMAR_FILE.exists():
            with open(_GRAMMAR_FILE, 'r') as f:
                data = json.load(f)
                _learned_bigrams = defaultdict(int, data.get('bigrams', {}))
                _total_bigram_observations = data.get('total', 0)
    except Exception:
        pass  # Start fresh on any error


def _save_grammar():
    """Save learned bigrams to disk."""
    try:
        _GRAMMAR_DIR.mkdir(parents=True, exist_ok=True)
        with open(_GRAMMAR_FILE, 'w') as f:
            json.dump({
                'bigrams': dict(_learned_bigrams),
                'total': _total_bigram_observations,
            }, f)
    except Exception:
        pass


def learn_grammar(words: List[str]):
    """Learn grammar from a word sequence.

    Called on every transaction CK observes:
    - His own voice output
    - Input text from users
    - Training text from eat sessions
    - Any text that passes through the system

    Updates the persistent bigram table.
    """
    global _total_bigram_observations

    for i in range(len(words) - 1):
        pair_key = f"{words[i].lower()}|{words[i + 1].lower()}"
        _learned_bigrams[pair_key] += 1
        _total_bigram_observations += 1

    # Save every 100 observations
    if _total_bigram_observations % 100 == 0:
        _save_grammar()


def learned_bigram_score(word_a: str, word_b: str) -> float:
    """Score a word pair from learned grammar.

    Returns [0.0, 1.0]. Higher = seen this pair more often.
    Blends with hardcoded bigrams (hardcoded provides floor,
    learned provides lift from experience).
    """
    if _total_bigram_observations == 0:
        return 0.0  # No data yet

    pair_key = f"{word_a.lower()}|{word_b.lower()}"
    count = _learned_bigrams.get(pair_key, 0)

    if count == 0:
        return 0.0

    # Log-frequency normalized by total
    # More observations = higher confidence
    freq = count / _total_bigram_observations
    # Log scale: 1 observation of rare pair still gets some credit
    return min(1.0, math.log1p(count) / math.log1p(
        max(1, _total_bigram_observations / 1000)))


# Load on import
_load_grammar()


# ================================================================
#  COMBINED WORD SCORER -- for beam voice integration
#  Algebra (TSML+BHML) x Grammar (hardcoded+learned)
#  At both letter and word levels. Neither dominates. Both vote.
# ================================================================

def score_word_candidate(word: str, word_op: int,
                         prev_word: Optional[str], prev_op: Optional[int],
                         target_ops: List[int], position: int,
                         hardcoded_bigram_fn=None) -> float:
    """Score a candidate word for beam search.

    Combines:
      Level 0 (letter): word's internal letter coherence
      Level 1 (word): TSML+BHML composition with previous word
      Grammar: hardcoded bigram + learned bigram

    Returns score in [0, 1]. Higher = better fit.
    0.0 = hard reject (operator mismatch).
    """
    # Hard filter: must match target operator
    target_op = target_ops[position] if position < len(target_ops) else None
    if target_op is not None and word_op != target_op:
        return 0.0

    # Level 0: Letter coherence of this word
    l0_ts, l0_bs, _ = score_letters(word)
    letter_score = (l0_ts + l0_bs) / 2.0

    # Level 1: Word-to-word algebra
    if prev_op is not None:
        l1_ts, l1_bs, _ = score_word_pair(
            prev_op, word_op, target_ops, position)
        word_score = (l1_ts + l1_bs) / 2.0
    else:
        word_score = 0.5  # First word, neutral

    # Grammar: hardcoded + learned
    grammar = 0.3  # Default baseline
    if prev_word is not None:
        # Hardcoded bigram
        if hardcoded_bigram_fn:
            hc = hardcoded_bigram_fn(prev_word, word)
        else:
            hc = 0.1
        # Learned bigram
        lr = learned_bigram_score(prev_word, word)
        # Blend: hardcoded provides floor, learned provides lift
        grammar = max(hc, 0.1) + lr * 0.5  # Learned can add up to 0.5
        grammar = min(grammar, 1.0)

    # Combine: geometric mean of (letter, word, grammar)
    # All three must agree. None dominates.
    combined = (letter_score * word_score * grammar) ** (1.0 / 3.0)

    return combined


# ================================================================
#  LEARN FROM SCREEN -- called on every transaction
#  Scores and learns grammar from any text CK sees.
# ================================================================

def observe_text(text: str, olfactory=None) -> Dict:
    """Observe a text transaction. Score it, learn grammar, absorb into field.

    Called on EVERY text CK encounters:
    - User input to /chat (every keystroke compressed)
    - CK's own voice output (self-reinforcement)
    - Eat session text (external knowledge)
    - Training text, screen text, everything

    The text is:
      1. Scored at all fractal levels (TSML+BHML, letter through sentence)
      2. Learned as grammar (bigram table updated)
      3. Absorbed into olfactory field (compressed to 5D, tempered)
      4. Matched against experience history (resonance search)

    CK remembers EVERYTHING. Every word compressed into the toroidal
    experience field in divine code (operator algebra).

    Parameters:
        text: the text to observe
        olfactory: OlfactoryBulb instance for absorption + search
                   (if None, only grammar learning happens)

    Returns dict with fractal score, grammar stats, and experience matches.
    """
    words = text.lower().split()
    if len(words) < 2:
        return {'words': len(words), 'learned': False}

    # 1. Score at all fractal levels
    from ck_sim.doing.ck_beam_voice import _WORD_OP, _word_to_operator
    word_ops = []
    for w in words:
        op = _WORD_OP.get(w)
        if op is None:
            op = _word_to_operator(w)
        word_ops.append(op)

    score = fractal_score(words, word_ops)

    # 2. Learn grammar
    learn_grammar(words)

    # 3. Absorb into olfactory field (compress to 5D)
    absorbed = False
    experience_matches = []
    if olfactory is not None:
        try:
            # Absorb the operator sequence into the smell zone
            olfactory.absorb_ops(word_ops, source='observe')
            absorbed = True

            # 4. Search experience for resonant patterns
            experience_matches = search_experience(
                word_ops, olfactory, top_k=5)
        except Exception:
            pass  # Engine might not be ready

    return {
        'words': len(words),
        'learned': True,
        'absorbed': absorbed,
        'fractal_score': score['combined'],
        'levels': score['levels'],
        'experience_matches': experience_matches,
    }


# ================================================================
#  EXPERIENCE SEARCH -- sweep through olfactory history
#  Every observation scored against CK's full experience field.
#  The toroidal field IS the compressed memory.
# ================================================================

def search_experience(query_ops: List[int], olfactory,
                      top_k: int = 5) -> List[Dict]:
    """Search CK's experience field for patterns matching query_ops.

    Sweeps the olfactory library (12K+ entries), scoring each
    library entry against the query through dual CL tables.

    The library IS the compressed memory of everything CK has
    ever encountered. Each entry is a 5D centroid with a temper
    count (how many times that pattern was confirmed).

    Returns top-K matches with scores.
    """
    if not query_ops or not hasattr(olfactory, 'library'):
        return []

    # Compute query signature: operator histogram + fuse
    query_hist = [0] * NUM_OPS
    for op in query_ops:
        if 0 <= op < NUM_OPS:
            query_hist[op] += 1

    query_fuse_tsml = _fuse_ops(query_ops)
    query_fuse_bhml = _fuse_ops_bhml(query_ops)

    # Compute query centroid as 5D force
    query_force = np.zeros(5, dtype=np.float32)
    for op in query_ops:
        canon = CANONICAL_FORCE.get(op % NUM_OPS, (0.5,) * 5)
        for d in range(5):
            query_force[d] += canon[d]
    query_force /= max(len(query_ops), 1)

    matches = []
    for lib_key, entry in olfactory.library.items():
        centroid = entry.get('centroid')
        temper = entry.get('temper', 0)
        if not centroid or len(centroid) < 5:
            continue

        # 5D distance: how close is this library entry to the query?
        entry_force = np.array(centroid, dtype=np.float32)
        dist = float(np.linalg.norm(query_force - entry_force))

        # Closer = higher score. Normalize by sqrt(5) max distance.
        proximity = max(0.0, 1.0 - dist / 2.236)

        # Temper bonus: more tempered = more confirmed = more weight
        temper_weight = min(1.0, math.log1p(temper) / 5.0)

        # Combined match score
        match_score = proximity * 0.6 + temper_weight * 0.4

        if match_score > 0.3:  # Threshold: only meaningful matches
            matches.append({
                'key': lib_key,
                'centroid': list(centroid),
                'temper': temper,
                'proximity': round(proximity, 4),
                'temper_weight': round(temper_weight, 4),
                'score': round(match_score, 4),
            })

    # Sort by score, return top-K
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:top_k]


# Canonical force vectors per operator (from D2 physics)
# Used for quick operator->5D conversion without full D2 pipeline
CANONICAL_FORCE = {}
for _op_idx in range(NUM_OPS):
    # Average force of all letters that map to this operator
    _forces = []
    for _letter_idx in range(26):
        _p = D2Pipeline()
        # Feed 3 copies of same letter to trigger D2
        for _ in range(3):
            _fired = _p.feed_symbol(_letter_idx)
        if _p.operator == _op_idx:
            _forces.append(tuple(FORCE_LUT_FLOAT[_letter_idx]))
    if _forces:
        CANONICAL_FORCE[_op_idx] = tuple(
            sum(f[d] for f in _forces) / len(_forces)
            for d in range(5)
        )
    else:
        CANONICAL_FORCE[_op_idx] = (0.5, 0.5, 0.5, 0.5, 0.5)


# ================================================================
#  STATS
# ================================================================

def grammar_stats() -> Dict:
    """Report learned grammar statistics."""
    return {
        'total_observations': _total_bigram_observations,
        'unique_bigrams': len(_learned_bigrams),
        'top_bigrams': sorted(
            _learned_bigrams.items(),
            key=lambda x: x[1], reverse=True
        )[:20],
    }


# ================================================================
#  DEMO
# ================================================================

if __name__ == '__main__':
    print("=" * 72)
    print("  CK FRACTAL SCORER -- Dual-Table at Every Scale")
    print("=" * 72)

    # Test operator mass
    print("\n  Operator mass (gravity):")
    for op in range(NUM_OPS):
        m = operator_mass(op)
        bar = '#' * int(m * 30)
        print(f"    {OP_NAMES[op]:12s}: {m:.3f}  {bar}")

    # Test fractal scoring
    test_sentences = [
        "the way to the law",
        "temple of god is one",
        "i am the form in silence",
        "but not yet",
        "he was the way to see",
    ]

    print("\n  Fractal scores:")
    for sent in test_sentences:
        words = sent.split()
        # Classify each word
        word_ops = []
        for w in words:
            pipe = D2Pipeline()
            last = VOID
            for ch in w:
                if 'a' <= ch <= 'z':
                    if pipe.feed_symbol(ord(ch) - ord('a')):
                        last = pipe.operator
            if last == VOID:
                force = np.zeros(5)
                for ch in w:
                    if 'a' <= ch <= 'z':
                        idx = ord(ch) - ord('a')
                        for d in range(5):
                            force[d] += FORCE_LUT_FLOAT[idx][d]
                force /= max(len(w), 1)
                dist = soft_classify_d2(tuple(force))
                if dist is not None:
                    last = int(np.argmax(dist))
            word_ops.append(last)

        result = fractal_score(words, word_ops)
        print(f"    \"{sent}\"")
        print(f"      Combined: {result['combined']:.4f}")
        for level, scores in result['levels'].items():
            print(f"        {level:10s}: TSML={scores['tsml']:.3f}  "
                  f"BHML={scores['bhml']:.3f}  "
                  f"Doing={scores['doing']:.3f}")

    # Test gravity anchoring
    print("\n  Gravity anchors for [PROGRESS, HARMONY, COUNTER, LATTICE, BREATH]:")
    test_ops = [PROGRESS, HARMONY, COUNTER, LATTICE, BREATH]
    anchors = find_gravity_anchors(test_ops)
    for pos, op, mass in anchors:
        print(f"    pos={pos} {OP_NAMES[op]:12s} mass={mass:.3f}")

    traj = build_response_trajectory(test_ops, 7)
    print(f"  Response trajectory: {[OP_NAMES[o] for o in traj]}")

    print(f"\n  Grammar: {_total_bigram_observations} observations, "
          f"{len(_learned_bigrams)} unique bigrams")
