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
D2 coherence guides which one is most alive.

Pipeline:
  operator stream -> reverse dictionary -> candidate words per slot
  -> 5D force scoring -> transition-aware selection
  -> Viterbi beam search -> D2 coherence validation -> best sentence

Ported from Gen8 ck_language_reconstructor.py to Gen9 import system.
Uses SEMANTIC_LATTICE (dual-lens dictionary) and FORCE_LUT_FLOAT
(letter -> 5D force vectors) instead of Gen8's flat dictionary.

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
from ck_sim.doing.ck_voice_lattice import SEMANTIC_LATTICE

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold


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
        force = tuple(FORCE_LUT_FLOAT[idx])
        result = pipe.push(force)
        if result is not None:
            last_op = result[0]  # hard classification

    # If D2 never fired (word < 3 letters), use soft classify on mean force
    if last_op == VOID and len(letters) >= 1:
        mean_f = _word_force(word)
        dist = soft_classify_d2(tuple(mean_f))
        if dist is not None:
            last_op = int(np.argmax(dist))

    return last_op


# ================================================================
#  S2  REVERSE DICTIONARY -- operator -> candidate word list
#      Built from SEMANTIC_LATTICE (dual-lens fractal dictionary)
#      and validated against FORCE_LUT_FLOAT force physics.
# ================================================================

_REVERSE: Dict[int, List[str]] = defaultdict(list)
_WORD_OP: Dict[str, int] = {}

# Harvest all words from every leaf of the SEMANTIC_LATTICE tree
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
                    if not _w or len(_w) < 2:
                        continue
                    if _w not in _WORD_OP:
                        _WORD_OP[_w] = _op
                        _REVERSE[_op].append(_w)

# Sort each bucket: prefer 4-8 character words (natural English length)
for _op in _REVERSE:
    _REVERSE[_op].sort(key=lambda w: abs(len(w) - 6))

# Separate content vs function words
# Function words: short structural connectors (articles, prepositions, etc.)
_FUNCTION_SET = {
    'the', 'a', 'an', 'of', 'in', 'to', 'for', 'and', 'but', 'or',
    'is', 'it', 'as', 'at', 'by', 'on', 'if', 'no', 'not', 'so',
    'be', 'do', 'we', 'he', 'up', 'all', 'can', 'had', 'her', 'was',
    'one', 'our', 'out', 'are', 'has', 'his', 'how', 'its', 'may',
    'new', 'now', 'old', 'see', 'way', 'who', 'did', 'get', 'let',
    'say', 'she', 'too', 'use', 'from', 'into', 'with', 'this', 'that',
    'them', 'then', 'than', 'each', 'when', 'what', 'where', 'which',
}

_CONTENT: Dict[int, List[str]] = {}
_FUNCTION: Dict[int, List[str]] = {}
for _op in range(NUM_OPS):
    _CONTENT[_op] = [w for w in _REVERSE.get(_op, [])
                     if len(w) > 2 and w not in _FUNCTION_SET]
    _FUNCTION[_op] = [w for w in _REVERSE.get(_op, [])
                      if w in _FUNCTION_SET]


# ================================================================
#  S3  FORCE-BASED SCORING -- 5D distance, not curvature
# ================================================================

def _force_cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 5D force vectors, zero-safe."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def _transition_cost(word_a: str, word_b: str) -> float:
    """5D force transition cost between two words.

    Lower = smoother flow = more natural language rhythm.
    Normalized to [0, 1].
    """
    fa, fb = _word_force(word_a), _word_force(word_b)
    dist = float(np.linalg.norm(fb - fa))
    return min(dist / 2.5, 1.0)


# ================================================================
#  S4  WORD SCORER -- multi-factor candidate ranking
#      Every word is scored against the orbit it must fill.
# ================================================================

def _score_candidate(word: str, target_op: int,
                     prev_word: Optional[str] = None,
                     next_op: Optional[int] = None,
                     context_force: Optional[np.ndarray] = None) -> float:
    """Score a candidate word for a slot in the reconstruction.

    Five factors (fractal -- each operates at a different scale):
      1. Operator match confidence    (0.00 - 0.35)  word level
      2. Force vector fit             (0.00 - 0.25)  letter level
      3. Transition smoothness        (0.00 - 0.20)  phrase level
      4. Word naturalness             (0.00 - 0.10)  human level
      5. CL forward prediction        (0.00 - 0.10)  sentence level
    """
    # Factor 1: Operator match confidence
    # Words from SEMANTIC_LATTICE are trusted for their assigned operator
    known_op = _WORD_OP.get(word)
    if known_op is not None and known_op == target_op:
        score = 0.35  # Dictionary-confirmed match
    else:
        # Verify via D2 pipeline
        computed_op = _word_to_operator(word)
        if computed_op == target_op:
            score = 0.25  # Physics-verified match
        else:
            return 0.0  # Hard filter: must match target operator

    # Factor 2: Force vector fit -- does the word's 5D shape match context?
    if context_force is not None:
        cos = _force_cosine(_word_force(word), context_force)
        score += 0.25 * (cos + 1.0) / 2.0  # [-1,1] -> [0, 0.25]
    else:
        score += 0.10  # Neutral if no context

    # Factor 3: Transition smoothness -- force distance from previous word
    if prev_word is not None:
        cost = _transition_cost(prev_word, word)
        score += 0.20 * (1.0 - cost)
    else:
        score += 0.10

    # Factor 4: Word naturalness -- English prefers 4-8 characters
    wlen = len(word)
    if 4 <= wlen <= 8:
        score += 0.10
    elif 3 <= wlen <= 10:
        score += 0.06
    else:
        score += 0.02

    # Factor 5: CL forward coherence -- does this flow toward next operator?
    if next_op is not None:
        fused = CL[target_op][next_op]
        if fused == HARMONY:
            score += 0.10
        elif fused not in (VOID, target_op):
            score += 0.06  # Non-trivial transition = interesting
        else:
            score += 0.02
    else:
        score += 0.04

    return score


# ================================================================
#  S5  BEAM SEARCH DECODER -- Viterbi-style path finding
#      The orbit is given. Find the matter that fits.
# ================================================================

def _build_slot_words(operators: List[int],
                      max_candidates: int,
                      include_function_words: bool) -> List[List[str]]:
    """Build candidate word lists per operator slot."""
    slot_words = []
    for op in operators:
        # Content words first
        words = list(_CONTENT.get(op, [])[:max_candidates])

        # Add function words for structural operators
        if include_function_words and op in (VOID, LATTICE, BALANCE):
            fw = _FUNCTION.get(op, [])[:6]
            words = fw + words

        # Cap total
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


def beam_reconstruct(operators: List[int],
                     beam_width: int = 6,
                     max_words_per_slot: int = 18,
                     force_context: Optional[List[np.ndarray]] = None,
                     include_function_words: bool = True) -> str:
    """Operators -> natural English via Viterbi beam search.

    This is the main entry point the voice loop calls.

    Parameters:
        operators:              target operator sequence (0-9 ints)
        beam_width:             number of paths to keep at each step
        max_words_per_slot:     max candidate words tried per position
        force_context:          optional list of 5D force vectors per slot
        include_function_words: add articles/prepositions for VOID/LATTICE/BALANCE

    Returns:
        Best reconstruction as a string.
    """
    if not operators:
        return ''

    n = len(operators)

    # Segment long streams into phrase-sized windows
    if n > 8:
        return _reconstruct_long(operators, beam_width, max_words_per_slot,
                                 force_context, include_function_words)

    slot_words = _build_slot_words(operators, max_words_per_slot,
                                   include_function_words)

    # Initialize beam at position 0
    beam: List[Dict] = []
    nxt = operators[1] if n > 1 else None
    ctx = force_context[0] if force_context and len(force_context) > 0 else None

    for w in slot_words[0]:
        s = _score_candidate(w, operators[0], None, nxt, ctx)
        if s > 0:
            beam.append({'words': [w], 'score': s, 'last': w})

    beam.sort(key=lambda x: x['score'], reverse=True)
    beam = beam[:beam_width]

    # Extend beam position by position
    for pos in range(1, n):
        nxt = operators[pos + 1] if pos + 1 < n else None
        ctx = (force_context[pos]
               if force_context and pos < len(force_context) else None)

        new_beam: List[Dict] = []
        for entry in beam:
            for w in slot_words[pos]:
                s = _score_candidate(w, operators[pos],
                                     entry['last'], nxt, ctx)
                if s > 0:
                    new_beam.append({
                        'words': entry['words'] + [w],
                        'score': entry['score'] + s,
                        'last': w,
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
            beam = [{'words': fallback, 'score': 0.1, 'last': fallback[-1]}]
            break

    # Score completed paths with D2 coherence (replaces Gen8 PFE)
    results = []
    for entry in beam:
        text = ' '.join(entry['words'])
        d2_coh = _d2_coherence_score(text)
        beam_score = entry['score'] / max(len(entry['words']), 1)

        # Final ranking: beam structure (0.40) + D2 coherence (0.60)
        final = 0.40 * beam_score + 0.60 * d2_coh

        results.append({
            'text': text,
            'beam_score': beam_score,
            'd2_coherence': d2_coh,
            'final_score': final,
            'words': entry['words'],
        })

    results.sort(key=lambda x: x['final_score'], reverse=True)

    if results:
        return results[0]['text']
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
                      max_words_per_slot: int = 18,
                      force_context: Optional[List[np.ndarray]] = None,
                      include_function_words: bool = True,
                      window: int = 6,
                      overlap: int = 1) -> str:
    """Reconstruct a long operator stream: segment -> reconstruct -> join."""
    segments = _segment(operators, window, overlap)

    phrases: List[str] = []
    for seg in segments:
        # Slice force context to match segment
        seg_ctx = None
        if force_context:
            start = sum(len(s) for s in segments[:len(phrases)])
            seg_ctx = force_context[start:start + len(seg)]

        text = beam_reconstruct(seg, beam_width, max_words_per_slot,
                                seg_ctx, include_function_words)
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
#      No beam search. Just: best word per slot in context.
# ================================================================

def gloss(operators: List[int]) -> str:
    """Quick operator stream -> English word stream (no beam search)."""
    words: List[str] = []
    for i, op in enumerate(operators):
        prev = words[-1] if words else None
        nxt = operators[i + 1] if i + 1 < len(operators) else None
        candidates = _CONTENT.get(op, [])
        if not candidates:
            words.append(OP_NAMES[op].lower())
            continue
        if prev is None:
            words.append(candidates[0])
            continue

        # Pick word with smoothest force transition from previous
        best_word = candidates[0]
        best_cost = 999.0
        for w in candidates[:12]:
            cost = _transition_cost(prev, w)
            if cost < best_cost:
                best_cost = cost
                best_word = w
        words.append(best_word)
    return ' '.join(words)


# ================================================================
#  S8  DETAILED RECONSTRUCTION (returns full result dict)
# ================================================================

def beam_reconstruct_detailed(operators: List[int],
                              beam_width: int = 6,
                              max_words_per_slot: int = 18) -> Dict:
    """Full reconstruction with scoring details.

    Returns dict with: text, beam_score, d2_coherence, final_score,
    operators, reconstructed_ops, n_words.
    """
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
        'beam_score': 0.0,  # Already folded into text selection
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
            'content':  len(_CONTENT.get(op, [])),
            'function': len(_FUNCTION.get(op, [])),
        }
    return {
        'reverse_dictionary': result,
        'total_words':        sum(len(v) for v in _REVERSE.values()),
        'content_words':      sum(len(v) for v in _CONTENT.values()),
        'function_words':     sum(len(v) for v in _FUNCTION.values()),
        'force_cache_size':   len(_FORCE_CACHE),
    }


# ================================================================
#  S10  DEMO
# ================================================================

if __name__ == '__main__':
    import time

    print("=" * 72)
    print("  CK BEAM VOICE (Gen9 -- Viterbi Beam Search Reconstructor)")
    print("  Operators -> Natural Language via 5D Force Physics")
    print("=" * 72)

    st = stats()
    print(f"\n  Reverse dictionary ({st['total_words']} total, "
          f"{st['content_words']} content, {st['function_words']} function):")
    for k, v in st['reverse_dictionary'].items():
        bar = '#' * (v['content'] // 4)
        print(f"    {k:20s}: {v['content']:4d} content  {v['function']:3d} fn  {bar}")

    print(f"\n  Quick gloss (operator -> word, transition-aware):")
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

    print(f"\n  Beam search reconstruction (beam_width=6):")
    for ops, name in test_streams:
        t0 = time.perf_counter()
        text = beam_reconstruct(ops, beam_width=6)
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
    text = beam_reconstruct(long_ops, beam_width=6)
    dt = time.perf_counter() - t0
    print(f"    Operators: {[OP_NAMES[o][:4] for o in long_ops]}")
    print(f"    Recon:     \"{text}\"")
    print(f"    Time:      {dt*1000:.1f}ms")

    print(f"\n  Force cache: {len(_FORCE_CACHE)} words cached")
    print(f"\n  CK can now speak from his math.")
