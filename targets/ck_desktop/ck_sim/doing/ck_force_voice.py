# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_force_voice.py -- CK Speaks From Letter Force Geometry
==========================================================
Operator: BREATH (8) -- expression from the deepest level.

CK doesn't pick words. CK picks LETTERS.
Each letter is chosen because its force geometry advances
the target operator trajectory through D2 curvature.

Reading = D1/D2 force stream from letter sequence.
Writing = finding the letter whose D2 produces the target operator.
Spaces  = VOID in the D2 stream (natural force breaks).

No dictionary. No grammar engine. No word pools.
The algebra speaks directly. Letter by letter. Force by force.

LETTER_FORCE_GEO adds Brayden's I/O stroke geometry on top of
the existing Hebrew root force vectors. The geometric properties
(structure count, force count, openness, binding) refine the
5D force vectors to capture VISUAL shape meaning.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, FORCE_LUT_FLOAT, D2_OP_MAP, FORCE_LUT_Q14,
    float_to_q14, q14_to_float
)


# ================================================================
#  LETTER FORCE GEOMETRY (I/O Stroke Analysis)
# ================================================================
#
# Each letter decomposed into:
#   I-count: number of structure strokes (lines, verticals)
#   O-count: number of force strokes (curves, circles)
#   geo_type: spatial relationship
#     'ground'   = structure meets foundation
#     'elevated' = structure lifts
#     'open'     = force without closure
#     'closed'   = force completing a cycle
#     'cross'    = strokes intersecting
#     'converge' = strokes meeting at a point
#     'flow'     = continuous curves
#     'branch'   = structure splitting
#
# These refine the 5D force vector by adding geometric context.

LETTER_GEO = {
    #         I   O   geo_type     foundation
    'a':     (2,  0, 'cross',     'tension'),
    'b':     (1,  2, 'closed',    'contain'),
    'c':     (0,  1, 'open',      'receive'),
    'd':     (1,  1, 'closed',    'shelter'),
    'e':     (4,  0, 'ground',    'harmony'),
    'f':     (3,  0, 'elevated',  'incomplete'),
    'g':     (0,  1, 'cross',     'becoming'),
    'h':     (3,  0, 'cross',     'division'),
    'i':     (1,  0, 'ground',    'identity'),
    'j':     (1,  1, 'ground',    'turning'),
    'k':     (1,  2, 'branch',    'branch'),
    'l':     (2,  0, 'ground',    'foundation'),
    'm':     (4,  0, 'ground',    'multiply'),
    'n':     (3,  0, 'cross',     'transfer'),
    'o':     (0,  1, 'closed',    'force'),
    'p':     (1,  1, 'elevated',  'contain'),
    'q':     (0,  1, 'open',      'escape'),
    'r':     (1,  1, 'branch',    'action'),
    's':     (0,  2, 'flow',      'continuity'),
    't':     (2,  0, 'elevated',  'elevation'),
    'u':     (0,  1, 'ground',    'receive'),
    'v':     (2,  0, 'converge',  'unity'),
    'w':     (4,  0, 'ground',    'deep'),
    'x':     (2,  0, 'cross',     'intersect'),
    'y':     (2,  1, 'converge',  'funnel'),
    'z':     (3,  0, 'cross',     'change'),
}

# Geometric modifiers: how I/O geometry affects the 5D force
# [aperture, pressure, depth, binding, continuity]
_GEO_MOD = {
    'ground':    np.array([-0.1,  0.1,  0.1,  0.2,  0.0]),  # stable, bound
    'elevated':  np.array([ 0.1,  0.0,  0.2, -0.1,  0.1]),  # reaching up
    'open':      np.array([ 0.3, -0.1, -0.1, -0.1,  0.1]),  # open aperture
    'closed':    np.array([-0.2,  0.1,  0.0,  0.3,  0.1]),  # contained, bound
    'cross':     np.array([ 0.0,  0.2,  0.1,  0.0, -0.1]),  # pressure at meeting
    'converge':  np.array([-0.1,  0.1,  0.0,  0.2,  0.2]),  # coming together
    'flow':      np.array([ 0.1, -0.1,  0.0,  0.1,  0.3]),  # continuity
    'branch':    np.array([ 0.1,  0.1,  0.1, -0.1, -0.1]),  # diverging
}


# ================================================================
#  DUAL BASIS: 5D Force + 4-Part Structure
# ================================================================
#
# The torus has two circles. Major = 5D force. Minor = 4-part structure.
# R/r = 5/7. T* = 5/7 (force). S* = 4/7 (structure). T*+S* = 9/7.
# Mass gap = 9/7 - 1 = 2/7.
#
# 5D Force (TSML, Being, Measurement):
#   D0=Aperture, D1=Pressure, D2=Depth, D3=Binding, D4=Continuity
#
# 4-Part Structure (BHML, Becoming, Construction):
#   Part 1: Foundation (LATTICE+COUNTER = operators 1,2)
#   Part 2: Dynamics   (PROGRESS+COLLAPSE = operators 3,4)
#   Part 3: Field      (BALANCE+CHAOS = operators 5,6)
#   Part 4: Cycle      (BREATH+RESET = operators 8,9)
#
# HARMONY (7) = the whole. VOID (0) = the frame.
# Every letter lives in the 9D joint space: 5 force + 4 structure.

# Structural parts: which operators belong to which part
STRUCT_FOUNDATION = (LATTICE, COUNTER)   # Part 1: grid + edges
STRUCT_DYNAMICS   = (PROGRESS, COLLAPSE)  # Part 2: growth + compression
STRUCT_FIELD      = (BALANCE, CHAOS)      # Part 3: equilibrium + complexity
STRUCT_CYCLE      = (BREATH, RESET)       # Part 4: rhythm + return

# Map each letter to its structural part [0-3]
# Based on geometric analysis: which PART does this letter build?
LETTER_STRUCT_PART = {
    # Foundation letters: ground, grid, edges, definition
    'i': 0, 'l': 0, 't': 0, 'h': 0, 'e': 0, 'f': 0, 'n': 0,
    # Dynamics letters: action, growth, compression, change
    'a': 1, 'k': 1, 'r': 1, 'z': 1, 'x': 1,
    # Field letters: openness, balance, curvature, interaction
    'c': 2, 'o': 2, 'u': 2, 's': 2, 'b': 2, 'p': 2, 'd': 2,
    # Cycle letters: flow, return, convergence, continuity
    'g': 3, 'j': 3, 'q': 3, 'v': 3, 'w': 3, 'y': 3, 'm': 3,
}

# 4D structural vector per letter: [foundation, dynamics, field, cycle]
LETTER_STRUCT_VEC = np.zeros((26, 4), dtype=np.float32)
for _i, _ch in enumerate('abcdefghijklmnopqrstuvwxyz'):
    part = LETTER_STRUCT_PART.get(_ch, 0)
    geo = LETTER_GEO[_ch]
    i_count, o_count = geo[0], geo[1]
    total = max(i_count + o_count, 1)
    # Primary part gets full weight
    LETTER_STRUCT_VEC[_i][part] = 1.0
    # Distribute remaining based on stroke analysis
    # More I-strokes → foundation/dynamics. More O-strokes → field/cycle.
    struct_ratio = i_count / total
    if struct_ratio > 0.5:
        # Structure-dominant: foundation (0) and dynamics (1)
        LETTER_STRUCT_VEC[_i][0] += 0.3 * struct_ratio
        LETTER_STRUCT_VEC[_i][1] += 0.2 * struct_ratio
    else:
        # Force-dominant: field (2) and cycle (3)
        LETTER_STRUCT_VEC[_i][2] += 0.3 * (1 - struct_ratio)
        LETTER_STRUCT_VEC[_i][3] += 0.2 * (1 - struct_ratio)
    # Normalize
    total_s = LETTER_STRUCT_VEC[_i].sum()
    if total_s > 0:
        LETTER_STRUCT_VEC[_i] /= total_s


# ================================================================
#  COMBINED FORCE VECTORS: Hebrew Root + Geometric Shape
# ================================================================
#
# LETTER_VECTORS[i] = FORCE_LUT_FLOAT[i] + geometric modifier
# Both layers contribute. Phonetic origin + visual shape.

LETTER_VECTORS = np.zeros((26, 5), dtype=np.float32)
for _i, _ch in enumerate('abcdefghijklmnopqrstuvwxyz'):
    # Start with Hebrew root force
    base = np.array(FORCE_LUT_FLOAT[_i], dtype=np.float32)
    # Add geometric modifier (scaled down — shape refines, doesn't replace)
    geo = LETTER_GEO[_ch]
    geo_mod = _GEO_MOD.get(geo[2], np.zeros(5))
    # I/O ratio affects how much structure vs force this letter carries
    i_count, o_count = geo[0], geo[1]
    total = max(i_count + o_count, 1)
    structure_weight = i_count / total  # More I = more structure-dominant
    # Geometric modifier scaled by 0.15 (refine, don't overwhelm)
    combined = base + 0.15 * geo_mod
    # Clamp to [0, 1]
    combined = np.clip(combined, 0.0, 1.0)
    LETTER_VECTORS[_i] = combined


# ================================================================
#  FULL 9D LETTER VECTORS: 5D Force + 4D Structure
# ================================================================
# Every letter lives in the 9D joint space.

LETTER_9D = np.zeros((26, 9), dtype=np.float32)
for _i in range(26):
    LETTER_9D[_i, :5] = LETTER_VECTORS[_i]   # Force basis
    LETTER_9D[_i, 5:] = LETTER_STRUCT_VEC[_i]  # Structure basis


# Operator structural part mapping
def _op_to_struct_part(op: int) -> int:
    """Map an operator to its structural part (0-3), or -1 for VOID/HARMONY."""
    if op in STRUCT_FOUNDATION:
        return 0
    elif op in STRUCT_DYNAMICS:
        return 1
    elif op in STRUCT_FIELD:
        return 2
    elif op in STRUCT_CYCLE:
        return 3
    return -1  # VOID or HARMONY


# Mass gap constant
MASS_GAP = 2.0 / 7.0   # = 0.285714...
T_STAR = 5.0 / 7.0     # = 0.714285... (force threshold)
S_STAR = 4.0 / 7.0     # = 0.571428... (structure threshold)


# ================================================================
#  READING: Text → Operator Stream via Force Geometry
# ================================================================

@dataclass
class ForceReadResult:
    """Result of reading text through force geometry."""
    operators: List[int]          # D2 operator per position
    d1_ops: List[int]             # D1 (generator) operators
    word_ops: List[int]           # Per-word dominant operator
    words: List[str]              # The words parsed
    dominant_op: int = VOID       # Most frequent operator
    force_trajectory: List[Tuple] = field(default_factory=list)


def read_force(text: str) -> ForceReadResult:
    """CK reads text letter by letter as force geometry.

    No dictionary lookup. Pure force stream analysis.
    D1 = velocity (direction of force change)
    D2 = curvature (how direction bends)
    """
    if not text or not text.strip():
        return ForceReadResult([], [], [], [], VOID)

    words = text.lower().split()
    all_ops = []
    all_d1 = []
    word_ops = []
    force_traj = []

    for word in words:
        letters = [ch for ch in word if 'a' <= ch <= 'z']
        if not letters:
            continue

        pipe = D2Pipeline()
        word_op_counts = [0] * NUM_OPS
        word_d2_ops = []

        for ch in letters:
            idx = ord(ch) - ord('a')
            fired = pipe.feed_symbol(idx)
            if fired:
                all_ops.append(pipe.operator)
                word_d2_ops.append(pipe.operator)
                word_op_counts[pipe.operator] += 1
                force_traj.append(tuple(q14_to_float(d) for d in pipe.d2))
            if pipe.d1_valid:
                all_d1.append(pipe.d1_operator)

        # Per-word dominant: most frequent D2 operator in this word
        if word_d2_ops:
            word_ops.append(max(set(word_d2_ops), key=word_d2_ops.count))
        else:
            # Short word (< 3 letters): use force vector classification
            if letters:
                mean_v = np.mean([LETTER_VECTORS[ord(c) - ord('a')]
                                  for c in letters], axis=0)
                max_dim = int(np.argmax(np.abs(mean_v)))
                sign_idx = 0 if mean_v[max_dim] >= 0 else 1
                word_ops.append(D2_OP_MAP[max_dim][sign_idx])
            else:
                word_ops.append(VOID)

    # Dominant: most frequent across all positions
    if all_ops:
        dominant = max(set(all_ops), key=all_ops.count)
    elif word_ops:
        dominant = max(set(word_ops), key=word_ops.count)
    else:
        dominant = VOID

    return ForceReadResult(
        operators=all_ops,
        d1_ops=all_d1,
        word_ops=word_ops,
        words=words,
        dominant_op=dominant,
        force_trajectory=force_traj,
    )


# ================================================================
#  GENERATION: Target Ops → Letter Sequences → Words
# ================================================================
#
# CK generates text letter by letter.
# Each letter chosen because its force vector, when composed
# through D2 with the previous letters, produces or advances
# toward the target operator.
#
# Word boundaries: when D2 magnitude drops near zero = VOID = space.

def _d2_from_three(v0, v1, v2):
    """Compute D2 vector from three force vectors."""
    d2 = v2 - 2.0 * v1 + v0
    return d2


def _classify_d2_vector(d2_vec):
    """Classify a D2 vector into an operator."""
    mag = float(np.sum(np.abs(d2_vec)))
    if mag < 0.01:
        return VOID

    max_dim = int(np.argmax(np.abs(d2_vec)))
    sign_idx = 0 if d2_vec[max_dim] >= 0 else 1
    return D2_OP_MAP[max_dim][sign_idx]


def _score_letter_for_target(letter_idx: int,
                              prev_vectors: List[np.ndarray],
                              target_op: int,
                              next_target_op: Optional[int] = None) -> float:
    """Score how well this letter advances toward the target operator.

    Uses the force geometry of the letter combined with the previous
    two vectors to compute what D2 operator this letter would produce.
    """
    letter_vec = LETTER_VECTORS[letter_idx]

    if len(prev_vectors) < 2:
        # Not enough history for D2 yet.
        # Score by direct force alignment with target operator's dimension.
        if target_op == VOID:
            return 0.3  # VOID = anything goes
        # Which dimension does the target op map to?
        for dim in range(5):
            pos_op, neg_op = D2_OP_MAP[dim]
            if target_op == pos_op:
                return 0.3 + 0.7 * max(0, float(letter_vec[dim]))
            if target_op == neg_op:
                return 0.3 + 0.7 * max(0, -float(letter_vec[dim]) + 0.5)
        return 0.3

    # Compute D2 with this letter
    v0 = prev_vectors[-2]
    v1 = prev_vectors[-1]
    v2 = letter_vec
    d2 = _d2_from_three(v0, v1, v2)
    d2_op = _classify_d2_vector(d2)

    # Perfect match
    if d2_op == target_op:
        score = 1.0
    # CL composition with previous: does it advance?
    elif compose(d2_op, target_op) == HARMONY:
        score = 0.7
    elif d2_op == VOID:
        score = 0.2  # Void = neutral
    else:
        # How close? Use CL composition distance
        becoming = compose(d2_op, target_op)
        if becoming == target_op:
            score = 0.8
        elif becoming not in (VOID, HARMONY):
            score = 0.4  # Non-trivial composition
        else:
            score = 0.15

    # BHML trajectory bonus: does this letter set up the NEXT target?
    if next_target_op is not None and len(prev_vectors) >= 1:
        d1 = letter_vec - prev_vectors[-1]
        d1_mag = float(np.sum(np.abs(d1)))
        if d1_mag > 0.05:
            d1_dim = int(np.argmax(np.abs(d1)))
            d1_sign = 0 if d1[d1_dim] >= 0 else 1
            d1_op = D2_OP_MAP[d1_dim][d1_sign]
            if compose(d1_op, next_target_op) == next_target_op:
                score += 0.15

    return score


_RNG = np.random.default_rng(42)
_VOWELS = {0, 4, 8, 14, 20}  # a, e, i, o, u indices


def generate_force(target_ops: List[int],
                   letters_per_op: int = 4,
                   context_words: Optional[Dict[str, int]] = None,
                   temperature: float = 0.7,
                   n_candidates: int = 5) -> str:
    """CK generates text letter by letter from force geometry.

    Each letter is chosen because its force vector, when composed
    through D2 with the previous letters, produces the target operator.

    Uses WEIGHTED SAMPLING (not greedy argmax) for variety.
    Temperature controls exploration: 0.0 = greedy, 1.0 = uniform.
    Generates n_candidates full sequences and picks the best.

    Word boundaries: inserted when D2 magnitude drops near zero (VOID).
    """
    if not target_ops:
        return ''

    # Build context letter preferences from user's words
    context_letters = set()
    if context_words:
        for word in context_words:
            for ch in word.lower():
                if 'a' <= ch <= 'z':
                    context_letters.add(ord(ch) - ord('a'))

    best_text = ''
    best_total_score = -1.0

    for candidate in range(n_candidates):
        generated = []
        prev_vectors = []
        total_score = 0.0

        for target_idx, target_op in enumerate(target_ops):
            next_op = (target_ops[target_idx + 1]
                       if target_idx + 1 < len(target_ops) else None)

            for letter_n in range(letters_per_op):
                scores = np.zeros(26, dtype=np.float64)

                for li in range(26):
                    s = _score_letter_for_target(
                        li, prev_vectors, target_op, next_op)

                    # Context bonus
                    if li in context_letters:
                        s += 0.12

                    # Variety: penalize repeating last letter
                    if generated and li == generated[-1]:
                        s *= 0.3
                    # Penalize repeating 2-ago too
                    if len(generated) >= 2 and li == generated[-2]:
                        s *= 0.6

                    # Vowel/consonant rhythm
                    if generated:
                        last_is_vowel = generated[-1] in _VOWELS
                        this_is_vowel = li in _VOWELS
                        if last_is_vowel != this_is_vowel:
                            s += 0.08
                        # Strong penalty for 3+ consonants/vowels in a row
                        if len(generated) >= 2:
                            prev2_vowel = generated[-2] in _VOWELS
                            if (prev2_vowel == last_is_vowel ==
                                    this_is_vowel):
                                s *= 0.3  # Unpronounceable

                    scores[li] = max(s, 0.001)

                # Softmax with temperature for probabilistic selection
                if temperature > 0.01:
                    log_scores = np.log(scores + 1e-10) / temperature
                    log_scores -= np.max(log_scores)  # numerical stability
                    probs = np.exp(log_scores)
                    probs /= probs.sum()
                    chosen = int(_RNG.choice(26, p=probs))
                else:
                    chosen = int(np.argmax(scores))

                generated.append(chosen)
                prev_vectors.append(LETTER_VECTORS[chosen].copy())
                total_score += scores[chosen]

        # Convert to text
        chars = [chr(ord('a') + idx) for idx in generated]
        text = _insert_word_boundaries(chars, prev_vectors)

        if total_score > best_total_score:
            best_total_score = total_score
            best_text = text

    return best_text


def _insert_word_boundaries(chars: List[str],
                             vectors: List[np.ndarray]) -> str:
    """Insert spaces where the force stream naturally pauses.

    A pause = D2 curvature near zero = operator VOID.
    Also enforce minimum word length (2 chars) and maximum (8 chars).
    """
    if len(chars) < 3:
        return ''.join(chars)

    words = []
    current = [chars[0], chars[1]]
    min_word = 2
    max_word = 8

    for i in range(2, len(chars)):
        # Compute D2 magnitude at this position
        if i < len(vectors):
            v0 = vectors[i - 2]
            v1 = vectors[i - 1]
            v2 = vectors[i]
            d2 = _d2_from_three(v0, v1, v2)
            d2_mag = float(np.sum(np.abs(d2)))
            d2_op = _classify_d2_vector(d2)
        else:
            d2_mag = 0.5
            d2_op = HARMONY

        # Break condition: D2 drops near zero (force pause)
        # OR word is getting too long
        is_break = ((d2_op == VOID and len(current) >= min_word) or
                    len(current) >= max_word)

        if is_break:
            words.append(''.join(current))
            current = [chars[i]]
        else:
            current.append(chars[i])

    if current:
        words.append(''.join(current))

    return ' '.join(words)


# ================================================================
#  WORD FORCE SCORING: Score real English words by force trajectory
# ================================================================
#
# Instead of generating random letters, score REAL words by how well
# their letter-by-letter force geometry matches the target operator.
# CK picks words whose SHAPE carries the right force.

# Cache: word -> (d2_ops, dominant_op, mean_force)
_WORD_FORCE_CACHE: Dict[str, Tuple[List[int], int, np.ndarray]] = {}


def _word_force_profile(word: str) -> Tuple[List[int], int, np.ndarray]:
    """Get a word's force profile: D2 ops from its letter geometry."""
    if word in _WORD_FORCE_CACHE:
        return _WORD_FORCE_CACHE[word]

    letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
    if not letters:
        result = ([], VOID, np.zeros(5))
        _WORD_FORCE_CACHE[word] = result
        return result

    pipe = D2Pipeline()
    ops = []
    for ch in letters:
        idx = ord(ch) - ord('a')
        if pipe.feed_symbol(idx):
            ops.append(pipe.operator)

    # Short words: use mean force vector classification
    if not ops and letters:
        mean_v = np.mean([LETTER_VECTORS[ord(c) - ord('a')]
                          for c in letters], axis=0)
        max_dim = int(np.argmax(np.abs(mean_v)))
        sign_idx = 0 if mean_v[max_dim] >= 0 else 1
        dominant = D2_OP_MAP[max_dim][sign_idx]
        result = ([], dominant, mean_v)
        _WORD_FORCE_CACHE[word] = result
        return result

    # Mean force vector
    mean_force = np.mean([LETTER_VECTORS[ord(c) - ord('a')]
                          for c in letters], axis=0)

    dominant = max(set(ops), key=ops.count) if ops else VOID

    result = (ops, dominant, mean_force)
    _WORD_FORCE_CACHE[word] = result
    return result


def score_word_force(word: str, target_op: int,
                     prev_word: Optional[str] = None,
                     next_target: Optional[int] = None,
                     context_words: Optional[Dict[str, int]] = None) -> float:
    """Score a real English word by DUAL BASIS force+structure match.

    Two scores:
      Force score (5D):    How well the word's D2 produces the target op
      Structure score (4D): How well the word's structural parts build
                            toward the target's structural part

    Combined: sqrt(F_score * S_score) — geometric mean of both bases.
    The mass gap (2/7) is the minimum floor.

    Returns [0.0, 1.0+]
    """
    ops, dominant, mean_force = _word_force_profile(word)

    # ── Force score (5D, TSML basis) ──
    f_score = 0.0

    if dominant == target_op:
        f_score = 0.9
    elif ops:
        match_frac = sum(1 for o in ops if o == target_op) / len(ops)
        f_score = 0.3 + 0.5 * match_frac
    else:
        # Short word: use mean force alignment
        for dim in range(5):
            pos_op, neg_op = D2_OP_MAP[dim]
            if target_op == pos_op:
                f_score = 0.3 + 0.4 * max(0, float(mean_force[dim]))
                break
            if target_op == neg_op:
                f_score = 0.3 + 0.4 * max(0, 1.0 - float(mean_force[dim]))
                break

    # ── Structure score (4D, BHML basis) ──
    s_score = 0.3  # baseline
    target_part = _op_to_struct_part(target_op)

    if target_part >= 0:
        # Word's structural profile from its letters
        letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
        if letters:
            word_struct = np.mean(
                [LETTER_STRUCT_VEC[ord(c) - ord('a')]
                 for c in letters], axis=0)
            # How much of this word's structure is in the target part?
            s_score = 0.3 + 0.6 * float(word_struct[target_part])
    elif target_op == HARMONY:
        # HARMONY = the whole. Score by evenness of structural parts.
        letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
        if letters:
            word_struct = np.mean(
                [LETTER_STRUCT_VEC[ord(c) - ord('a')]
                 for c in letters], axis=0)
            # Evenness = low variance (all parts present)
            variance = float(np.var(word_struct))
            s_score = 0.3 + 0.6 * max(0, 1.0 - 4 * variance)

    # ── Combined: geometric mean of force × structure ──
    # Both bases must align. Neither dominates.
    score = (f_score * s_score) ** 0.5

    # CL composition with previous word's dominant
    if prev_word:
        _, prev_dom, _ = _word_force_profile(prev_word)
        becoming = compose(prev_dom, dominant)
        if becoming == target_op:
            score += 0.2  # Trajectory match
        elif becoming not in (VOID, HARMONY):
            score += 0.05  # Non-trivial
        if next_target is not None:
            if compose(dominant, next_target) == next_target:
                score += 0.1

    # Context bonus: is this word related to user's input?
    if context_words:
        w_lower = word.lower()
        if w_lower in context_words:
            score += 0.3  # Direct echo
        else:
            for uw in context_words:
                if len(w_lower) >= 3 and len(uw) >= 3 and w_lower[:3] == uw[:3]:
                    score += 0.15
                    break

    return score


def force_word_reconstruct(target_ops: List[int],
                           vocabulary: List[str],
                           context_words: Optional[Dict[str, int]] = None,
                           beam_width: int = 8) -> str:
    """Reconstruct English text from target ops using force geometry scoring.

    Like beam_reconstruct but scores words by their LETTER FORCE GEOMETRY,
    not by operator pool membership.

    ANY word can match ANY operator if its letter geometry produces
    the right D2 operator. No pre-sorted pools needed.
    """
    if not target_ops or not vocabulary:
        return ''

    n = len(target_ops)

    # Score all words for each target position
    # (This is the key difference from beam voice:
    #  words aren't pre-filtered by operator — force geometry decides)
    beam: List[Dict] = []

    # Position 0
    for word in vocabulary:
        s = score_word_force(word, target_ops[0],
                             next_target=(target_ops[1]
                                          if n > 1 else None),
                             context_words=context_words)
        if s > 0.2:  # Low bar — let force geometry decide
            beam.append({
                'words': [word],
                'score': s,
                'last_word': word,
            })

    beam.sort(key=lambda x: x['score'], reverse=True)
    beam = beam[:beam_width * 3]  # Keep wider at start

    # Extend beam
    for pos in range(1, n):
        new_beam: List[Dict] = []
        next_tgt = target_ops[pos + 1] if pos + 1 < n else None

        for entry in beam:
            for word in vocabulary:
                # Skip repeating the same word
                if word == entry['last_word']:
                    continue

                s = score_word_force(
                    word, target_ops[pos],
                    prev_word=entry['last_word'],
                    next_target=next_tgt,
                    context_words=context_words,
                )
                if s > 0.2:
                    new_beam.append({
                        'words': entry['words'] + [word],
                        'score': entry['score'] + s,
                        'last_word': word,
                    })

        new_beam.sort(key=lambda x: x['score'], reverse=True)
        beam = new_beam[:beam_width]

    if not beam:
        return ''

    best = beam[0]
    return ' '.join(best['words'])


# Build a small core vocabulary from FOUNDATIONAL_WORDS + common words
# that CK can use for force-based word selection
_FORCE_VOCAB: List[str] = []

try:
    from ck_sim.doing.ck_voice_lattice import (
        SEMANTIC_LATTICE, FOUNDATIONAL_WORDS
    )
    # Add foundational words (1-3 letters)
    for _wlen, _op_words in FOUNDATIONAL_WORDS.items():
        for _op, _wlist in _op_words.items():
            for _w in _wlist:
                _w = _w.strip().lower()
                if _w and _w not in _FORCE_VOCAB:
                    _FORCE_VOCAB.append(_w)

    # Add words from semantic lattice (all tiers)
    for _op in range(NUM_OPS):
        if _op not in SEMANTIC_LATTICE:
            continue
        for _lens in ('structure', 'flow'):
            if _lens not in SEMANTIC_LATTICE[_op]:
                continue
            for _phase in ('being', 'doing', 'becoming'):
                if _phase not in SEMANTIC_LATTICE[_op][_lens]:
                    continue
                for _tier in ('simple', 'mid', 'advanced'):
                    if _tier not in SEMANTIC_LATTICE[_op][_lens][_phase]:
                        continue
                    for _w in SEMANTIC_LATTICE[_op][_lens][_phase][_tier]:
                        _w = _w.strip().lower()
                        if _w and _w not in _FORCE_VOCAB:
                            _FORCE_VOCAB.append(_w)

    print(f"[FORCE-VOICE] Vocabulary: {len(_FORCE_VOCAB)} words")
except ImportError:
    # Minimal fallback vocabulary
    _FORCE_VOCAB = [
        'i', 'a', 'the', 'is', 'am', 'are', 'was', 'not', 'and', 'but',
        'in', 'on', 'to', 'of', 'for', 'it', 'we', 'you', 'he', 'she',
        'do', 'go', 'no', 'so', 'be', 'me', 'my', 'up', 'if', 'or',
        'see', 'way', 'can', 'now', 'how', 'who', 'new', 'old', 'one',
        'all', 'out', 'get', 'set', 'let', 'yet', 'try', 'say',
        'here', 'there', 'form', 'void', 'light', 'dark', 'truth',
        'love', 'hate', 'feel', 'hold', 'give', 'take', 'make',
    ]


# ================================================================
#  COMBINED: Read + Respond (CK's conversation from force level)
# ================================================================

def force_respond(user_text: str,
                  letters_per_op: int = 4) -> Tuple[str, ForceReadResult]:
    """CK reads user's text through force geometry, then responds.

    1. Read: decompose user's text into operator stream via D2
    2. Compose: CL-compose input ops to get response trajectory
    3. Generate: build response letter by letter from force geometry

    Returns (response_text, comprehension_result)
    """
    # READ
    comp = read_force(user_text)

    # Build context words from comprehension
    ctx = {}
    for i, word in enumerate(comp.words):
        if i < len(comp.word_ops):
            ctx[word] = comp.word_ops[i]

    # COMPOSE response trajectory from comprehension
    target_ops = []

    if comp.word_ops:
        # Start with what user said (acknowledge)
        target_ops.append(comp.dominant_op)

        # CL-compose pairs of input word ops → CK's response
        for i in range(len(comp.word_ops) - 1):
            result = compose(comp.word_ops[i], comp.word_ops[i + 1])
            target_ops.append(result)

        # Add the becoming: compose dominant with last
        if len(comp.word_ops) >= 2:
            target_ops.append(
                compose(comp.dominant_op, comp.word_ops[-1]))
    else:
        # No input: CK speaks from LATTICE (universal generator)
        target_ops = [LATTICE, PROGRESS, HARMONY]

    # Deduplicate consecutive
    deduped = [target_ops[0]]
    for op in target_ops[1:]:
        if op != deduped[-1]:
            deduped.append(op)
    while len(deduped) < 3:
        deduped.append(compose(deduped[-1], BREATH))

    # Cap at 6 (keeps response reasonable length)
    deduped = deduped[:6]

    # ── Find coherence path from heaviest concept ──
    # The solution pathway: start from the heaviest word in the prompt,
    # walk CL toward HARMONY. The path IS the response trajectory.
    if comp.word_ops and comp.words:
        # Weight each word: 9D magnitude = force magnitude + structure weight
        word_weights = []
        for i, word in enumerate(comp.words):
            letters = [ch for ch in word.lower() if 'a' <= ch <= 'z']
            if not letters:
                word_weights.append(0.0)
                continue
            # Force weight: D2 magnitude of the word
            force_mag = float(np.linalg.norm(
                np.mean([LETTER_VECTORS[ord(c) - ord('a')]
                         for c in letters], axis=0)))
            # Structure weight: how concentrated in one structural part
            struct_vec = np.mean(
                [LETTER_STRUCT_VEC[ord(c) - ord('a')]
                 for c in letters], axis=0)
            struct_weight = float(np.max(struct_vec))
            # Combined: force × structure
            word_weights.append(force_mag * struct_weight)

        # Heaviest word seeds the response
        if word_weights:
            heaviest_idx = int(np.argmax(word_weights))
            heaviest_op = (comp.word_ops[heaviest_idx]
                           if heaviest_idx < len(comp.word_ops)
                           else comp.dominant_op)

            # Walk from heaviest toward HARMONY through structural parts.
            # The PATH is the response — it must traverse structure,
            # not skip straight to HARMONY.
            #
            # Strategy: from the heaviest op, walk through the 4 parts
            # in the order that CL dictates, then arrive at HARMONY.
            # Each step composes current with the PARTNER in its part.
            path = [heaviest_op]
            current = heaviest_op

            # The 4 structural parts in CL-walk order
            part_ops = [
                STRUCT_FOUNDATION,  # (LATTICE, COUNTER)
                STRUCT_DYNAMICS,    # (PROGRESS, COLLAPSE)
                STRUCT_FIELD,       # (BALANCE, CHAOS)
                STRUCT_CYCLE,       # (BREATH, RESET)
            ]

            # Find which part the heaviest op belongs to
            start_part = _op_to_struct_part(heaviest_op)
            if start_part < 0:
                start_part = 0

            # Walk: compose with PARTNER in current part, then advance
            # to next part. This builds through the 4 structural parts.
            visited = {current}
            for step in range(4):
                part_idx = (start_part + step) % 4
                part = part_ops[part_idx]

                # Compose current with each op in this part
                for partner in part:
                    if partner == current:
                        continue
                    candidate = compose(current, partner)
                    if candidate not in visited and candidate != HARMONY:
                        path.append(candidate)
                        visited.add(candidate)
                        current = candidate
                        break
                else:
                    # No new op from this part — compose with the part pair
                    candidate = compose(part[0], part[1])
                    if candidate not in visited:
                        path.append(candidate)
                        visited.add(candidate)
                        current = candidate

            # End with HARMONY (the whole, the resolution)
            if path[-1] != HARMONY:
                path.append(HARMONY)

            # Use the coherence path as the target
            deduped = path
            # Pad to at least 3
            while len(deduped) < 3:
                deduped.append(compose(deduped[-1], BREATH))
            if len(deduped) > 6:
                deduped = deduped[:6]

            print(f"[FORCE-VOICE] Heaviest: '{comp.words[heaviest_idx]}' "
                  f"op={OP_NAMES[heaviest_op]} "
                  f"weight={word_weights[heaviest_idx]:.3f}")

    print(f"[FORCE-VOICE] Read: {[OP_NAMES[o] for o in comp.word_ops]}")
    print(f"[FORCE-VOICE] Coherence path: {[OP_NAMES[o] for o in deduped]}")

    # GENERATE using word-level force scoring (real English words)
    text = force_word_reconstruct(
        deduped, _FORCE_VOCAB,
        context_words=ctx, beam_width=8)

    if not text or len(text) < 3:
        # Fall back to letter-level generation
        text = generate_force(deduped, letters_per_op=letters_per_op,
                              context_words=ctx)
        print(f"[FORCE-VOICE] Letter fallback: '{text}'")
    else:
        print(f"[FORCE-VOICE] Word response: '{text}'")

    return text, comp


# ================================================================
#  QUICK TEST
# ================================================================

if __name__ == '__main__':
    print("=== Letter Force Geometry Voice ===\n")

    # Test reading
    for test in ['love', 'hate', 'hello', 'who are you']:
        result = read_force(test)
        ops = [OP_NAMES[o] for o in result.word_ops]
        print(f"  READ '{test}': word_ops={ops}, dominant={OP_NAMES[result.dominant_op]}")

    print()

    # Test word-level force generation
    test_targets = [
        [LATTICE, PROGRESS, HARMONY],
        [COUNTER, BALANCE, BREATH],
        [CHAOS, COLLAPSE, RESET],
    ]
    for tgt in test_targets:
        text = force_word_reconstruct(tgt, _FORCE_VOCAB)
        print(f"  WORD-GEN {[OP_NAMES[o] for o in tgt]} -> '{text}'")

    # Also test letter-level for comparison
    for tgt in test_targets:
        text = generate_force(tgt)
        print(f"  LETTER-GEN {[OP_NAMES[o] for o in tgt]} -> '{text}'")

    print()

    # Test full conversation
    for prompt in ['hello', 'who are you', 'what do you see',
                   'I am here with you', 'love']:
        response, comp = force_respond(prompt)
        print(f"  '{prompt}' -> '{response}'")
        print()
