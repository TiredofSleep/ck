# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_beam_voice.py -- Viterbi Beam Search Language Reconstructor (Gen9)
=====================================================================
Operator: HARMONY (7) -- the voice composes from the orbit.

CK can hear (text -> operators). Now he speaks (operators -> text).

The inverse problem: given an operator stream, reconstruct natural
language that produces that stream. This is not lookup. It's composition.
Multiple valid sentences can produce the same operator stream.

Two scores multiply. Meaning x grammar. CL x English.
Neither dominates. Both vote.

  ALGEBRA SCORE: BHML composition of prev_op with candidate_op.
    Does this word ADVANCE the target trajectory?
    The CL table picks which words carry information.

  BIGRAM SCORE: English word-pair frequency.
    Does this word SOUND RIGHT after the previous word?
    Grammar picks which combinations are speakable.

  final_score = algebra_score * bigram_score

Pipeline:
  operator stream -> ALL candidate words (no length filtering)
  -> algebra scoring (BHML trajectory match)
  -> bigram scoring (English grammar)
  -> multiply scores -> Viterbi beam search -> best sentence

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter

# ================================================================
#  IMPORTS FROM GEN9 CORE
# ================================================================

from ck_sim.being.ck_sim_heartbeat import (
    CL, compose, NUM_OPS, OP_NAMES,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)
from ck_sim.being.ck_sim_d2 import (
    FORCE_LUT_FLOAT, D2Pipeline, soft_classify_d2,
)
from ck_sim.doing.ck_voice_lattice import SEMANTIC_LATTICE, FOUNDATIONAL_WORDS
from ck_sim.doing.ck_fractal_scorer import (
    score_word_candidate as _fractal_score_word,
    observe_text, learn_grammar, learned_bigram_score,
    fractal_score as _multi_level_score,
    find_gravity_anchors, build_response_trajectory,
    score_letters as _score_letters,
)

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

# ================================================================
#  BHML -- The Becoming table (full rank, deterministic)
#  Imported as plain list-of-lists so no numpy dependency at module level.
#  BHML[a][b] = what a BECOMES when composed with b.
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


def bhml_compose(a: int, b: int) -> int:
    """BHML composition. What a BECOMES when meeting b."""
    if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
        return BHML[a][b]
    return VOID


# ================================================================
#  ENGLISH BIGRAM TABLE -- grammar without rules
#  Top ~200 word pairs by frequency in English.
#  Score = log-frequency, normalized to [0.1, 1.0].
#  Missing pairs get 0.1 (rare but possible).
#  The bigram table handles grammar. The CL table handles meaning.
# ================================================================

_BIGRAM_RAW = {
    # Determiner + noun patterns
    ('the', 'form'): 0.9, ('the', 'void'): 0.8, ('the', 'one'): 0.9,
    ('the', 'way'): 0.9, ('the', 'end'): 0.9, ('the', 'sea'): 0.8,
    ('the', 'key'): 0.8, ('the', 'law'): 0.8, ('the', 'man'): 0.9,
    ('the', 'sun'): 0.8, ('the', 'day'): 0.9, ('the', 'old'): 0.8,
    ('the', 'new'): 0.9, ('the', 'temple'): 0.8, ('the', 'pattern'): 0.8,
    ('the', 'silence'): 0.8, ('the', 'whole'): 0.8, ('the', 'soul'): 0.8,
    ('the', 'truth'): 0.8, ('the', 'space'): 0.8, ('the', 'god'): 0.7,
    ('the', 'air'): 0.8, ('the', 'body'): 0.8, ('the', 'mind'): 0.8,
    ('the', 'earth'): 0.8, ('the', 'king'): 0.8, ('the', 'son'): 0.8,
    ('a', 'form'): 0.8, ('a', 'man'): 0.8, ('a', 'new'): 0.8,
    ('a', 'way'): 0.8, ('a', 'key'): 0.7, ('a', 'soul'): 0.7,
    ('a', 'whole'): 0.7, ('a', 'gap'): 0.7, ('a', 'pattern'): 0.7,

    # Subject + verb patterns
    ('i', 'am'): 1.0, ('i', 'see'): 0.9, ('i', 'can'): 0.9,
    ('i', 'do'): 0.8, ('i', 'try'): 0.8, ('i', 'ask'): 0.7,
    ('i', 'run'): 0.7, ('i', 'get'): 0.8, ('i', 'say'): 0.8,
    ('i', 'set'): 0.7, ('i', 'put'): 0.7, ('i', 'let'): 0.7,
    ('i', 'fly'): 0.7, ('i', 'act'): 0.7,
    ('we', 'are'): 0.9, ('we', 'see'): 0.8, ('we', 'can'): 0.8,
    ('we', 'do'): 0.7, ('we', 'all'): 0.7, ('we', 'may'): 0.7,
    ('he', 'is'): 0.9, ('he', 'was'): 0.9, ('he', 'did'): 0.8,
    ('he', 'can'): 0.8, ('he', 'has'): 0.8, ('he', 'may'): 0.7,
    ('she', 'is'): 0.9, ('she', 'was'): 0.9, ('she', 'has'): 0.8,
    ('it', 'is'): 1.0, ('it', 'was'): 0.9, ('it', 'can'): 0.8,
    ('it', 'has'): 0.7, ('it', 'may'): 0.7,
    ('who', 'is'): 0.8, ('who', 'was'): 0.8, ('who', 'can'): 0.7,
    ('you', 'are'): 0.9, ('you', 'can'): 0.9, ('you', 'see'): 0.8,
    ('you', 'may'): 0.7, ('you', 'do'): 0.7,

    # Verb + object / complement patterns
    ('is', 'the'): 0.9, ('is', 'a'): 0.9, ('is', 'not'): 0.9,
    ('is', 'in'): 0.8, ('is', 'it'): 0.7, ('is', 'no'): 0.7,
    ('is', 'one'): 0.7, ('is', 'all'): 0.7, ('is', 'now'): 0.7,
    ('was', 'the'): 0.8, ('was', 'a'): 0.8, ('was', 'not'): 0.8,
    ('was', 'in'): 0.7, ('was', 'no'): 0.6,
    ('am', 'the'): 0.7, ('am', 'a'): 0.7, ('am', 'not'): 0.7,
    ('am', 'in'): 0.7, ('am', 'here'): 0.8,
    ('are', 'the'): 0.8, ('are', 'not'): 0.8, ('are', 'in'): 0.7,
    ('are', 'all'): 0.7, ('are', 'one'): 0.6,
    ('can', 'see'): 0.8, ('can', 'be'): 0.8, ('can', 'not'): 0.7,
    ('can', 'you'): 0.7, ('can', 'do'): 0.6,
    ('do', 'not'): 0.9, ('do', 'you'): 0.7, ('do', 'we'): 0.6,
    ('see', 'the'): 0.8, ('see', 'a'): 0.7, ('see', 'it'): 0.7,
    ('see', 'how'): 0.7, ('see', 'you'): 0.6,
    ('has', 'the'): 0.7, ('has', 'a'): 0.7, ('has', 'no'): 0.7,
    ('has', 'its'): 0.6, ('has', 'not'): 0.7,
    ('get', 'the'): 0.7, ('get', 'a'): 0.6, ('get', 'to'): 0.7,
    ('let', 'the'): 0.7, ('let', 'it'): 0.8, ('let', 'us'): 0.8,
    ('let', 'me'): 0.8, ('let', 'go'): 0.7,

    # Preposition patterns
    ('in', 'the'): 1.0, ('in', 'a'): 0.8, ('in', 'its'): 0.7,
    ('in', 'all'): 0.7, ('in', 'one'): 0.6,
    ('of', 'the'): 1.0, ('of', 'a'): 0.8, ('of', 'all'): 0.7,
    ('of', 'its'): 0.7, ('of', 'one'): 0.6, ('of', 'god'): 0.7,
    ('to', 'the'): 0.9, ('to', 'a'): 0.8, ('to', 'be'): 0.9,
    ('to', 'see'): 0.8, ('to', 'do'): 0.7, ('to', 'go'): 0.7,
    ('to', 'get'): 0.7, ('to', 'it'): 0.6, ('to', 'its'): 0.6,
    ('on', 'the'): 0.9, ('on', 'a'): 0.7, ('on', 'its'): 0.6,
    ('at', 'the'): 0.8, ('at', 'a'): 0.6, ('at', 'its'): 0.5,
    ('by', 'the'): 0.8, ('by', 'a'): 0.7, ('by', 'its'): 0.6,
    ('for', 'the'): 0.9, ('for', 'a'): 0.8, ('for', 'all'): 0.7,
    ('for', 'its'): 0.6, ('for', 'you'): 0.6,
    ('from', 'the'): 0.8, ('from', 'a'): 0.7, ('from', 'its'): 0.6,
    ('with', 'the'): 0.8, ('with', 'a'): 0.7, ('with', 'its'): 0.6,
    ('into', 'the'): 0.8, ('into', 'a'): 0.7,

    # Conjunction patterns
    ('and', 'the'): 0.9, ('and', 'a'): 0.8, ('and', 'it'): 0.7,
    ('and', 'i'): 0.7, ('and', 'we'): 0.7, ('and', 'all'): 0.6,
    ('and', 'so'): 0.7, ('and', 'yet'): 0.7, ('and', 'now'): 0.7,
    ('but', 'the'): 0.8, ('but', 'a'): 0.7, ('but', 'it'): 0.8,
    ('but', 'i'): 0.8, ('but', 'not'): 0.8, ('but', 'we'): 0.7,
    ('or', 'a'): 0.7, ('or', 'the'): 0.7, ('or', 'it'): 0.6,
    ('so', 'the'): 0.7, ('so', 'it'): 0.7, ('so', 'i'): 0.7,
    ('so', 'we'): 0.6, ('so', 'be'): 0.6,
    ('yet', 'the'): 0.7, ('yet', 'it'): 0.7, ('yet', 'i'): 0.7,
    ('now', 'the'): 0.7, ('now', 'it'): 0.7, ('now', 'i'): 0.7,
    ('now', 'we'): 0.6, ('now', 'is'): 0.7,
    ('not', 'the'): 0.8, ('not', 'a'): 0.7, ('not', 'in'): 0.7,
    ('not', 'by'): 0.6, ('not', 'one'): 0.6, ('not', 'all'): 0.6,
    ('not', 'yet'): 0.7, ('not', 'be'): 0.6, ('not', 'see'): 0.6,

    # Adjective + noun patterns
    ('new', 'form'): 0.7, ('new', 'way'): 0.7, ('new', 'day'): 0.7,
    ('old', 'form'): 0.6, ('old', 'way'): 0.6, ('old', 'law'): 0.6,
    ('all', 'the'): 0.8, ('all', 'is'): 0.7, ('all', 'of'): 0.7,
    ('all', 'one'): 0.6,
    ('no', 'one'): 0.8, ('no', 'way'): 0.7, ('no', 'form'): 0.6,
    ('no', 'end'): 0.6,

    # Content word transitions (physics vocabulary)
    ('form', 'and'): 0.7, ('form', 'is'): 0.7, ('form', 'of'): 0.7,
    ('form', 'in'): 0.6, ('void', 'is'): 0.6, ('void', 'and'): 0.6,
    ('silence', 'is'): 0.7, ('silence', 'and'): 0.6,
    ('temple', 'of'): 0.7, ('temple', 'and'): 0.6, ('temple', 'is'): 0.6,
    ('pattern', 'of'): 0.7, ('pattern', 'is'): 0.6, ('pattern', 'in'): 0.6,
    ('soul', 'of'): 0.7, ('soul', 'is'): 0.6, ('soul', 'and'): 0.6,
    ('god', 'is'): 0.8, ('god', 'of'): 0.7, ('god', 'and'): 0.6,
    ('truth', 'is'): 0.8, ('truth', 'of'): 0.7, ('truth', 'and'): 0.6,
    ('one', 'is'): 0.7, ('one', 'who'): 0.7, ('one', 'can'): 0.6,
    ('one', 'and'): 0.6,
    ('way', 'of'): 0.7, ('way', 'to'): 0.8, ('way', 'is'): 0.6,
    ('way', 'the'): 0.6,
    ('eye', 'of'): 0.7, ('eye', 'is'): 0.6, ('eye', 'can'): 0.6,
    ('sea', 'of'): 0.7, ('sea', 'and'): 0.6, ('sea', 'is'): 0.6,
    ('end', 'of'): 0.8, ('end', 'is'): 0.7, ('end', 'and'): 0.6,
    ('sun', 'is'): 0.7, ('sun', 'and'): 0.6, ('sun', 'of'): 0.6,
    ('air', 'is'): 0.7, ('air', 'and'): 0.6, ('air', 'of'): 0.6,
    ('war', 'is'): 0.7, ('war', 'and'): 0.6, ('war', 'of'): 0.6,
    ('boy', 'is'): 0.6, ('boy', 'who'): 0.6,
    ('ice', 'and'): 0.6, ('ice', 'is'): 0.6,
    ('joy', 'of'): 0.7, ('joy', 'is'): 0.7, ('joy', 'and'): 0.6,
}

# Build fast lookup (default 0.1 for unknown pairs)
_BIGRAM_DEFAULT = 0.1


def _bigram_score(word_a: str, word_b: str) -> float:
    """English bigram frequency score for a word pair.

    Returns [0.1, 1.0]. Higher = more natural English pairing.
    """
    return _BIGRAM_RAW.get((word_a.lower(), word_b.lower()), _BIGRAM_DEFAULT)


# ================================================================
#  S1  WORD -> 5D FORCE VECTOR (from letter forces)
# ================================================================

_FORCE_CACHE: Dict[str, np.ndarray] = {}


def _word_force(word: str) -> np.ndarray:
    """Mean 5D force vector for a word from its letters. Cached."""
    if word in _FORCE_CACHE:
        return _FORCE_CACHE[word]
    letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
    if not letters:
        v = np.zeros(5, dtype=np.float32)
    else:
        force_sum = np.zeros(5, dtype=np.float32)
        for ch in letters:
            idx = ord(ch) - ord('a')
            for d in range(5):
                force_sum[d] += FORCE_LUT_FLOAT[idx][d]
        v = (force_sum / len(letters)).astype(np.float32)
    _FORCE_CACHE[word] = v
    return v


def _word_to_operator(word: str) -> int:
    """Classify a word into its dominant operator via D2 pipeline.

    Runs the word through D2Pipeline letter by letter,
    returns the hard-classified operator from the final D2 vector.
    If the word is too short for D2 (< 3 letters), fall back to
    soft classification of the mean force vector.
    """
    letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
    if not letters:
        return VOID

    pipe = D2Pipeline()
    last_op = VOID
    for ch in letters:
        idx = ord(ch) - ord('a')
        fired = pipe.feed_symbol(idx)
        if fired:
            last_op = pipe.operator

    # If D2 never fired (word < 3 letters), use soft classify on mean force
    if last_op == VOID and len(letters) >= 1:
        mean_f = _word_force(word)
        dist = soft_classify_d2(tuple(mean_f))
        if dist is not None:
            last_op = int(np.argmax(dist))

    return last_op


# ================================================================
#  S2  REVERSE DICTIONARY -- operator -> candidate word list
#      Built from FOUNDATIONAL_WORDS + SEMANTIC_LATTICE.
#      NO LENGTH SORTING. Order doesn't matter -- algebra scores.
# ================================================================

_REVERSE: Dict[int, List[str]] = defaultdict(list)
_WORD_OP: Dict[str, int] = {}

# First: Add foundational words (1-3 letters, D2-classified)
for _wlen, _op_words in FOUNDATIONAL_WORDS.items():
    for _op, _wlist in _op_words.items():
        for _w in _wlist:
            _w = _w.strip().lower()
            if _w and _w not in _WORD_OP:
                _WORD_OP[_w] = _op
                _REVERSE[_op].append(_w)

# Then: Harvest all words from every leaf of the SEMANTIC_LATTICE tree
for _op in range(NUM_OPS):
    if _op not in SEMANTIC_LATTICE:
        continue
    op_dict = SEMANTIC_LATTICE[_op]
    for _lens in ('structure', 'flow'):
        if _lens not in op_dict:
            continue
        for _phase in ('being', 'doing', 'becoming'):
            if _phase not in op_dict[_lens]:
                continue
            for _tier in ('simple', 'mid', 'advanced'):
                if _tier not in op_dict[_lens][_phase]:
                    continue
                for _word in op_dict[_lens][_phase][_tier]:
                    _w = _word.strip().lower()
                    if not _w:
                        continue
                    if _w not in _WORD_OP:
                        _WORD_OP[_w] = _op
                        _REVERSE[_op].append(_w)

# NO SORTING BY LENGTH. The algebra scores. Not the index position.


# ================================================================
#  S3  ALGEBRA SCORING -- BHML trajectory composition
#      The CL table picks meaning. Not length. Not frequency.
# ================================================================

def _algebra_score(word: str, prev_op: Optional[int],
                   target_ops: List[int], position: int) -> float:
    """Score a word by how well it advances the BHML trajectory.

    This is the MEANING score. The CL table decides.

    Returns [0.0, 1.0]:
      1.0 = perfect trajectory match (BHML says this word advances the path)
      0.7 = non-trivial composition (carries information)
      0.4 = harmony (filler -- acceptable bridge)
      0.1 = void/dead end
    """
    word_op = _WORD_OP.get(word)
    if word_op is None:
        word_op = _word_to_operator(word)

    # Must match target operator for this slot
    target_op = target_ops[position] if position < len(target_ops) else None
    if target_op is not None and word_op != target_op:
        return 0.0  # Hard filter: operator must match slot

    if prev_op is None:
        # First word in sentence -- no composition to check
        return 0.6  # Neutral start

    # What does this word BECOME when composed with previous?
    becoming = bhml_compose(prev_op, word_op)

    # Does it match where we're trying to go next?
    next_target = target_ops[position + 1] if position + 1 < len(target_ops) else None
    if next_target is not None and becoming == next_target:
        return 1.0  # Perfect trajectory match

    # Does it produce something non-trivial?
    if becoming not in (VOID, HARMONY):
        return 0.7  # Carries information -- a real operator emerges

    if becoming == HARMONY:
        return 0.4  # Harmony filler -- bridge between real words

    return 0.1  # Void -- dead end


# ================================================================
#  S4  COMBINED SCORER -- algebra x bigram
#      Algebra picks meaning. Bigrams pick grammar.
#      Neither dominates. Both vote.
# ================================================================

def _score_candidate(word: str, target_op: int,
                     prev_word: Optional[str] = None,
                     prev_op: Optional[int] = None,
                     target_ops: Optional[List[int]] = None,
                     position: int = 0) -> float:
    """Score a candidate word: fractal dual-table x grammar.

    Uses the fractal scorer which evaluates at multiple levels:
      Level 0 (letter): word's internal letter-to-letter coherence
      Level 1 (word): TSML+BHML composition with previous word
      Grammar: hardcoded bigram + learned bigram (from observation)

    Returns 0.0 if word doesn't match target operator (hard filter).
    """
    if target_ops is None:
        target_ops = [target_op]

    word_op = _WORD_OP.get(word)
    if word_op is None:
        word_op = _word_to_operator(word)

    # Use fractal scorer: evaluates letter-level + word-level + grammar
    return _fractal_score_word(
        word, word_op,
        prev_word, prev_op,
        target_ops, position,
        hardcoded_bigram_fn=_bigram_score,
    )


# ================================================================
#  S5  BEAM SEARCH DECODER -- Viterbi-style path finding
#      The orbit is given. Find the matter that fits.
#      No length filtering. ALL words compete. Algebra decides.
# ================================================================

def _build_slot_words(operators: List[int],
                      max_candidates: int) -> List[List[str]]:
    """Build candidate word lists per operator slot.

    ALL words for the operator. No length filtering.
    The scoring function decides which ones win.
    """
    slot_words = []
    for op in operators:
        words = list(_REVERSE.get(op, []))

        # Cap total candidates (performance bound, not quality filter)
        words = words[:max_candidates]

        if not words:
            words = [OP_NAMES[op].lower()]  # Absolute fallback

        slot_words.append(words)
    return slot_words


def _d2_coherence_score(text: str) -> float:
    """Score a text string for D2 coherence.

    Runs every letter through a D2 pipeline, counts how many D2
    classifications land on HARMONY (the absorber), and returns
    the ratio. Higher = more coherent physics.
    """
    letters = [ch for ch in text.lower() if 'a' <= ch <= 'z']
    if len(letters) < 3:
        return 0.0

    pipe = D2Pipeline()
    n_fired = 0
    n_harmony = 0
    for ch in letters:
        idx = ord(ch) - ord('a')
        fired = pipe.feed_symbol(idx)
        if fired:
            n_fired += 1
            if pipe.operator == HARMONY:
                n_harmony += 1

    if n_fired == 0:
        return 0.0
    return n_harmony / n_fired


def _context_bonus(word: str, context_words: Dict[str, int],
                    target_op: int) -> float:
    """Score bonus for words topically related to user's input.

    CK should RESPOND to what was said, not ignore it.
    Words from the user's input get a bonus. Words sharing the same
    operator as user words get a smaller bonus.

    Returns [0.0, 0.5] — added to base score, never dominates.
    """
    if not context_words:
        return 0.0

    w_lower = word.lower()

    # Direct echo: user said this word → CK acknowledges it
    if w_lower in context_words:
        return 0.4

    # Same root: shares first 3+ letters with a user word
    for uw in context_words:
        if len(w_lower) >= 3 and len(uw) >= 3:
            if w_lower[:3] == uw[:3]:
                return 0.3

    # Operator affinity: same operator as a user word
    word_op = _WORD_OP.get(w_lower)
    if word_op is None:
        word_op = _word_to_operator(w_lower)
    user_ops = set(context_words.values())
    if word_op in user_ops:
        return 0.15

    return 0.0


def beam_reconstruct(operators: List[int],
                     beam_width: int = 6,
                     max_words_per_slot: int = 30,
                     force_context: Optional[List[np.ndarray]] = None,
                     include_function_words: bool = True,
                     max_word_length: int = 99,
                     context_words: Optional[Dict[str, int]] = None) -> str:
    """Operators -> natural English via Viterbi beam search.

    This is the main entry point the voice loop calls.

    Parameters:
        operators:              target operator sequence (0-9 ints)
        beam_width:             number of paths to keep at each step
        max_words_per_slot:     max candidate words tried per position
        force_context:          (unused, kept for API compat)
        include_function_words: (unused, kept for API compat)
        max_word_length:        (unused, kept for API compat)
        context_words:          {word: operator} from user's input
                                (from fractal comprehension)

    Returns:
        Best reconstruction as a string.
    """
    if not operators:
        return ''

    ctx = context_words or {}
    n = len(operators)

    # Segment long streams into phrase-sized windows
    if n > 8:
        return _reconstruct_long(operators, beam_width, max_words_per_slot)

    slot_words = _build_slot_words(operators, max_words_per_slot)

    # Initialize beam at position 0
    beam: List[Dict] = []

    for w in slot_words[0]:
        s = _score_candidate(w, operators[0],
                             prev_word=None, prev_op=None,
                             target_ops=operators, position=0)
        # Context bonus: prefer words related to user's input
        s += _context_bonus(w, ctx, operators[0])
        if s > 0:
            beam.append({
                'words': [w],
                'score': s,
                'last_word': w,
                'last_op': _WORD_OP.get(w, _word_to_operator(w)),
            })

    beam.sort(key=lambda x: x['score'], reverse=True)
    beam = beam[:beam_width]

    # Extend beam position by position
    for pos in range(1, n):
        new_beam: List[Dict] = []
        for entry in beam:
            for w in slot_words[pos]:
                s = _score_candidate(
                    w, operators[pos],
                    prev_word=entry['last_word'],
                    prev_op=entry['last_op'],
                    target_ops=operators,
                    position=pos,
                )
                # Context bonus: prefer words related to user's input
                s += _context_bonus(w, ctx, operators[pos])
                if s > 0:
                    new_beam.append({
                        'words': entry['words'] + [w],
                        'score': entry['score'] + s,
                        'last_word': w,
                        'last_op': _WORD_OP.get(w, _word_to_operator(w)),
                    })

        new_beam.sort(key=lambda x: x['score'], reverse=True)
        beam = new_beam[:beam_width]

        if not beam:
            # Dead beam -- fall back to greedy single word per slot
            fallback = [
                slot_words[p][0] if slot_words[p]
                else OP_NAMES[operators[p]].lower()
                for p in range(n)
            ]
            beam = [{
                'words': fallback, 'score': 0.1,
                'last_word': fallback[-1],
                'last_op': _WORD_OP.get(fallback[-1], VOID),
            }]
            break

    # Score completed paths with full fractal multi-level scorer
    # TSML+BHML at letter, word, phrase, and sentence levels
    results = []
    for entry in beam:
        text = ' '.join(entry['words'])
        word_ops = [_WORD_OP.get(w, _word_to_operator(w))
                    for w in entry['words']]

        # Multi-level fractal score (letter + word + phrase + sentence)
        fs = _multi_level_score(entry['words'], word_ops, operators)
        fractal_combined = fs['combined']

        # Beam path score (normalized)
        beam_score = entry['score'] / max(len(entry['words']), 1)

        # Context relevance bonus: how many of CK's words relate to input
        ctx_score = 0.0
        if ctx:
            ctx_hits = sum(1 for w in entry['words']
                           if _context_bonus(w, ctx, 0) > 0)
            ctx_score = ctx_hits / max(len(entry['words']), 1)

        # Final: fractal coherence (0.50) + beam path (0.30) + context (0.20)
        final = (0.50 * fractal_combined
                 + 0.30 * beam_score
                 + 0.20 * ctx_score)

        results.append({
            'text': text,
            'beam_score': beam_score,
            'fractal_score': fractal_combined,
            'context_score': ctx_score,
            'final_score': final,
            'words': entry['words'],
            'levels': fs.get('levels', {}),
        })

    results.sort(key=lambda x: x['final_score'], reverse=True)

    if results:
        best = results[0]
        print(f"[BEAM] Best: '{best['text']}' "
              f"fractal={best['fractal_score']:.3f} "
              f"beam={best['beam_score']:.3f} "
              f"ctx={best.get('context_score', 0):.3f}")
        return best['text']
    return ' '.join(OP_NAMES[op].lower() for op in operators)


# ================================================================
#  S6  SLIDING WINDOW SEGMENTATION -- phrases from streams
#      Natural language has phrase structure. 5-7 word chunks.
# ================================================================

def _segment(operators: List[int],
             window: int = 6,
             overlap: int = 1) -> List[List[int]]:
    """Segment a long operator stream into overlapping windows."""
    if len(operators) <= window:
        return [operators]

    segments = []
    step = max(1, window - overlap)
    for start in range(0, len(operators), step):
        end = min(start + window, len(operators))
        seg = operators[start:end]
        if len(seg) >= 2:
            segments.append(seg)
        if end >= len(operators):
            break
    return segments


def _reconstruct_long(operators: List[int],
                      beam_width: int = 6,
                      max_words_per_slot: int = 30,
                      window: int = 6,
                      overlap: int = 1) -> str:
    """Reconstruct a long operator stream: segment -> reconstruct -> join."""
    segments = _segment(operators, window, overlap)

    phrases: List[str] = []
    for seg in segments:
        text = beam_reconstruct(seg, beam_width, max_words_per_slot)
        phrases.append(text)

    # Join phrases, removing overlap words to avoid repetition
    if not phrases:
        return ''

    full_words = phrases[0].split()
    for phrase in phrases[1:]:
        words = phrase.split()
        skip = min(overlap, len(words) - 1) if words else 0
        full_words.extend(words[skip:])

    return ' '.join(full_words)


# ================================================================
#  S7  QUICK GLOSS -- fast single-word-per-operator translation
#      No beam search. Just: best word per slot by algebra.
# ================================================================

def gloss(operators: List[int]) -> str:
    """Quick operator stream -> English word stream (algebra-scored)."""
    words: List[str] = []
    prev_op = None
    for i, op in enumerate(operators):
        prev_word = words[-1] if words else None
        candidates = _REVERSE.get(op, [])
        if not candidates:
            words.append(OP_NAMES[op].lower())
            prev_op = op
            continue

        # Score each candidate by algebra x bigram
        best_word = candidates[0]
        best_score = -1.0
        for w in candidates[:20]:
            s = _score_candidate(
                w, op,
                prev_word=prev_word, prev_op=prev_op,
                target_ops=operators, position=i,
            )
            if s > best_score:
                best_score = s
                best_word = w

        words.append(best_word)
        prev_op = _WORD_OP.get(best_word, op)
    return ' '.join(words)


# ================================================================
#  S8  DETAILED RECONSTRUCTION (returns full result dict)
# ================================================================

def beam_reconstruct_detailed(operators: List[int],
                              beam_width: int = 6,
                              max_words_per_slot: int = 30) -> Dict:
    """Full reconstruction with scoring details."""
    if not operators:
        return {'text': '', 'beam_score': 0.0, 'd2_coherence': 0.0,
                'final_score': 0.0, 'operators': [], 'n_words': 0}

    text = beam_reconstruct(operators, beam_width, max_words_per_slot)
    words = text.split()
    recon_ops = [_word_to_operator(w) for w in words]
    d2_coh = _d2_coherence_score(text)

    # Operator fidelity: how many slots match?
    if operators and recon_ops:
        matches = sum(1 for a, b in zip(operators, recon_ops) if a == b)
        fidelity = matches / max(len(operators), len(recon_ops))
    else:
        fidelity = 0.0

    return {
        'text': text,
        'beam_score': 0.0,
        'd2_coherence': d2_coh,
        'final_score': d2_coh,
        'operators': operators,
        'reconstructed_ops': recon_ops,
        'operator_fidelity': round(fidelity, 4),
        'n_words': len(words),
    }


# ================================================================
#  S9  STATISTICS & INTROSPECTION
# ================================================================

def stats() -> Dict:
    """Report reverse dictionary composition."""
    result = {}
    for op in range(NUM_OPS):
        name = OP_NAMES[op]
        result[f"{op}_{name}"] = {
            'total':    len(_REVERSE.get(op, [])),
        }
    return {
        'reverse_dictionary': result,
        'total_words':        sum(len(v) for v in _REVERSE.values()),
        'force_cache_size':   len(_FORCE_CACHE),
    }


# ================================================================
#  S10  DEMO
# ================================================================

if __name__ == '__main__':
    import time

    print("=" * 72)
    print("  CK BEAM VOICE (Gen9 -- Algebra x Bigram Reconstructor)")
    print("  Operators -> Natural Language via BHML + English Grammar")
    print("=" * 72)

    st = stats()
    print(f"\n  Reverse dictionary ({st['total_words']} total words):")
    for k, v in st['reverse_dictionary'].items():
        bar = '#' * (v['total'] // 4)
        print(f"    {k:20s}: {v['total']:4d}  {bar}")

    print(f"\n  Quick gloss (operator -> word, algebra-scored):")
    test_streams = [
        ([7, 3, 2, 7, 0],  "HARMONY -> PROGRESS -> COUNTER -> HARMONY -> VOID"),
        ([4, 6, 4, 4, 6],  "COLLAPSE -> CHAOS -> COLLAPSE -> COLLAPSE -> CHAOS"),
        ([8, 8, 8, 7, 8],  "BREATH -> BREATH -> BREATH -> HARMONY -> BREATH"),
        ([9, 3, 3, 7, 3],  "RESET -> PROGRESS -> PROGRESS -> HARMONY -> PROGRESS"),
        ([7, 7, 7, 7, 7],  "HARMONY x5 (the absorber stream)"),
    ]

    for ops, name in test_streams:
        g = gloss(ops)
        print(f"    {name[:48]:48s} -> {g}")

    print(f"\n  Beam search reconstruction (beam_width=8):")
    for ops, name in test_streams:
        t0 = time.perf_counter()
        text = beam_reconstruct(ops, beam_width=8)
        dt = time.perf_counter() - t0
        detail = beam_reconstruct_detailed(ops)
        print(f"    {name[:40]:40s}")
        print(f"      \"{text}\"")
        print(f"      D2={detail['d2_coherence']:.4f}  "
              f"fidelity={detail['operator_fidelity']:.0%}  "
              f"{dt*1000:.1f}ms")

    print(f"\n  Long sequence reconstruction:")
    long_ops = [7, 3, 8, 7, 1, 2, 7, 3, 9, 7, 8, 7, 3, 5, 7]
    t0 = time.perf_counter()
    text = beam_reconstruct(long_ops, beam_width=8)
    dt = time.perf_counter() - t0
    print(f"    Operators: {[OP_NAMES[o][:4] for o in long_ops]}")
    print(f"    Recon:     \"{text}\"")
    print(f"    Time:      {dt*1000:.1f}ms")

    print(f"\n  Force cache: {len(_FORCE_CACHE)} words cached")
    print(f"\n  CK speaks from his algebra now.")
