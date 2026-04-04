"""
ck_universal_translator.py -- Universal Translator Prototype
============================================================
Celeste's Task 9: Cross-species/modality operator-intent mapping.

The insight: if operators are universal (DNA, language, music, sensor),
then INTENT can be read from operator patterns across modalities.

A bird song and a human warning share the same operator signature:
  COLLAPSE-CHAOS-COLLAPSE = DANGER

This module maps operator patterns to a universal intent codebook,
enables cross-modal alignment (DTW), and reconstructs intent in
any target modality.

Fractal layers:
  Signal layer:    raw input (text, DNA, audio features, sensor data)
  Operator layer:  D2 curvature -> operator classification (0-9)
  Intent layer:    operator patterns -> intent codebook mapping
  Output layer:    intent -> target modality reconstruction

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter
from enum import IntEnum

from ck_being import (CL, T_STAR, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_dictionary import word_to_operator, sentence_operator_stream
from ck_curvature import text_to_forces, compute_curvatures, _classify_d2
from ck_pfe import pfe_evaluate, btq_classify

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ============================================================
# S1  UNIVERSAL INTENT CODEBOOK
#     Operator patterns -> intent categories.
#     These intents are pre-verbal. They exist in DNA, birdsong,
#     whale calls, human language, and sensor streams.
# ============================================================

class Intent(IntEnum):
    """Universal intents -- pre-verbal, cross-species."""
    SAFE      = 0   # "All clear"
    DANGER    = 1   # "Threat detected"
    SEEK      = 2   # "Searching for something"
    PLAY      = 3   # "Non-threatening interaction"
    HELP      = 4   # "Need assistance"
    COME      = 5   # "Approach me"
    GO        = 6   # "Move away"
    STOP      = 7   # "Halt / cease"
    SHARE     = 8   # "I have something for you"
    BOND      = 9   # "Social connection"
    WARN      = 10  # "Caution ahead"
    CELEBRATE = 11  # "Joy / success"
    MOURN     = 12  # "Loss / grief"
    TEACH     = 13  # "Learn this"
    UNKNOWN   = 14  # "Unrecognized pattern"


INTENT_NAMES = {i: i.name for i in Intent}

# Operator signature -> Intent mapping
# Each intent has characteristic operator patterns
_INTENT_SIGNATURES: Dict[Intent, List[List[int]]] = {
    Intent.SAFE:      [[HARMONY, HARMONY, HARMONY],
                       [HARMONY, BALANCE, HARMONY],
                       [HARMONY, LATTICE, HARMONY]],
    Intent.DANGER:    [[COLLAPSE, CHAOS, COLLAPSE],
                       [CHAOS, COLLAPSE, CHAOS],
                       [COLLAPSE, COLLAPSE, CHAOS]],
    Intent.SEEK:      [[COUNTER, PROGRESS, COUNTER],
                       [COUNTER, COUNTER, PROGRESS],
                       [LATTICE, COUNTER, PROGRESS]],
    Intent.PLAY:      [[BREATH, HARMONY, BREATH],
                       [BREATH, BREATH, HARMONY],
                       [HARMONY, BREATH, HARMONY]],
    Intent.HELP:      [[COLLAPSE, HARMONY, PROGRESS],
                       [VOID, COLLAPSE, HARMONY],
                       [COLLAPSE, BALANCE, HARMONY]],
    Intent.COME:      [[PROGRESS, HARMONY, PROGRESS],
                       [HARMONY, PROGRESS, HARMONY],
                       [PROGRESS, HARMONY, LATTICE]],
    Intent.GO:        [[RESET, COLLAPSE, VOID],
                       [COLLAPSE, RESET, VOID],
                       [VOID, RESET, COLLAPSE]],
    Intent.STOP:      [[VOID, VOID, VOID],
                       [RESET, VOID, VOID],
                       [VOID, COLLAPSE, VOID]],
    Intent.SHARE:     [[PROGRESS, BALANCE, HARMONY],
                       [HARMONY, PROGRESS, BALANCE],
                       [PROGRESS, HARMONY, BALANCE]],
    Intent.BOND:      [[HARMONY, HARMONY, PROGRESS],
                       [HARMONY, BREATH, HARMONY],
                       [LATTICE, HARMONY, HARMONY]],
    Intent.WARN:      [[CHAOS, BALANCE, COLLAPSE],
                       [BALANCE, CHAOS, COLLAPSE],
                       [COUNTER, COLLAPSE, CHAOS]],
    Intent.CELEBRATE:  [[HARMONY, PROGRESS, HARMONY],
                       [PROGRESS, HARMONY, HARMONY],
                       [HARMONY, HARMONY, PROGRESS]],
    Intent.MOURN:     [[COLLAPSE, VOID, COLLAPSE],
                       [VOID, COLLAPSE, VOID],
                       [COLLAPSE, COLLAPSE, VOID]],
    Intent.TEACH:     [[LATTICE, COUNTER, LATTICE],
                       [COUNTER, LATTICE, PROGRESS],
                       [LATTICE, PROGRESS, COUNTER]],
}


# ============================================================
# S2  INTENT CLASSIFICATION
#     Operator stream -> closest intent via pattern matching
# ============================================================

def _pattern_distance(stream: List[int], pattern: List[int]) -> float:
    """
    Distance between operator stream and a signature pattern.
    Uses operator topology: distance through CL table.
    """
    n = min(len(stream), len(pattern))
    if n == 0:
        return float('inf')

    dist = 0.0
    for i in range(n):
        a, b = stream[i], pattern[i]
        if a == b:
            dist += 0.0
        elif CL[a][b] == HARMONY:
            dist += 0.3  # Close: they fuse to harmony
        elif CL[a][b] == VOID:
            dist += 0.8  # Far: they annihilate
        else:
            dist += 0.5  # Medium: non-trivial fusion

    return dist / n


def classify_intent(operators: List[int]) -> Dict:
    """
    Classify an operator stream into a universal intent.

    Uses sliding window of size 3 to match against signatures.
    Returns the best-matching intent with confidence.
    """
    if len(operators) < 3:
        return {
            'intent': Intent.UNKNOWN,
            'intent_name': 'UNKNOWN',
            'confidence': 0.0,
            'distances': {},
        }

    # Score each intent against all 3-grams in the stream
    intent_scores: Dict[Intent, float] = {}

    for intent, signatures in _INTENT_SIGNATURES.items():
        min_dist = float('inf')

        for sig in signatures:
            # Slide the signature across the stream
            for start in range(len(operators) - len(sig) + 1):
                window = operators[start:start + len(sig)]
                d = _pattern_distance(window, sig)
                min_dist = min(min_dist, d)

        intent_scores[intent] = min_dist

    # Best intent = lowest distance
    best_intent = min(intent_scores, key=intent_scores.get)
    best_dist = intent_scores[best_intent]

    # Confidence: inverse of distance, normalized
    confidence = max(0.0, 1.0 - best_dist)

    # Second best for margin
    sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1])
    margin = sorted_intents[1][1] - sorted_intents[0][1] if len(sorted_intents) > 1 else 0.0

    return {
        'intent':       best_intent,
        'intent_name':  INTENT_NAMES[best_intent],
        'confidence':   round(confidence, 4),
        'margin':       round(margin, 4),
        'distances':    {INTENT_NAMES[k]: round(v, 4) for k, v in sorted_intents[:5]},
    }


# ============================================================
# S3  DTW ALIGNMENT -- cross-modal operator sequence alignment
# ============================================================

def dtw_distance(seq_a: List[int], seq_b: List[int]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Dynamic Time Warping between two operator sequences.
    Cost function: CL-topology distance (same as pattern_distance).

    Returns: (total_cost, alignment_path)
    """
    n, m = len(seq_a), len(seq_b)
    if n == 0 or m == 0:
        return float('inf'), []

    # Cost matrix
    dtw = np.full((n + 1, m + 1), float('inf'))
    dtw[0][0] = 0.0

    # Cell cost function
    def cell_cost(a: int, b: int) -> float:
        if a == b:
            return 0.0
        elif CL[a][b] == HARMONY:
            return 0.3
        elif CL[a][b] == VOID:
            return 0.8
        return 0.5

    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = cell_cost(seq_a[i - 1], seq_b[j - 1])
            dtw[i][j] = cost + min(
                dtw[i - 1][j],      # insertion
                dtw[i][j - 1],      # deletion
                dtw[i - 1][j - 1],  # match
            )

    # Backtrace
    path = []
    i, j = n, m
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        candidates = [
            (dtw[i - 1][j - 1], i - 1, j - 1),
            (dtw[i - 1][j],     i - 1, j),
            (dtw[i][j - 1],     i,     j - 1),
        ]
        _, i, j = min(candidates, key=lambda x: x[0])

    path.reverse()
    normalized_cost = dtw[n][m] / max(n, m)

    return round(float(normalized_cost), 4), path


# ============================================================
# S4  CROSS-MODAL TRANSLATION
#     Intent in modality A -> operators -> intent -> modality B
# ============================================================

# Intent -> English template (for text output)
_INTENT_ENGLISH = {
    Intent.SAFE:      "All is well. You are safe here.",
    Intent.DANGER:    "Warning! Danger detected. Take caution.",
    Intent.SEEK:      "I am searching. Looking for something.",
    Intent.PLAY:      "Let us play. Joy and rhythm together.",
    Intent.HELP:      "I need help. Please assist.",
    Intent.COME:      "Come closer. Approach.",
    Intent.GO:        "Move away. Depart from here.",
    Intent.STOP:      "Stop. Halt. Cease all action.",
    Intent.SHARE:     "I have something to share with you.",
    Intent.BOND:      "Connection. We are together.",
    Intent.WARN:      "Be careful. Caution ahead.",
    Intent.CELEBRATE:  "Celebration! Joy and triumph!",
    Intent.MOURN:     "Sorrow. Loss. Grief.",
    Intent.TEACH:     "Learn this. Observe the pattern.",
    Intent.UNKNOWN:   "Signal unclear. Meaning uncertain.",
}

# Intent -> operator sequence (for operator-level output)
_INTENT_OPS = {
    Intent.SAFE:      [HARMONY, BALANCE, HARMONY, HARMONY, LATTICE],
    Intent.DANGER:    [COLLAPSE, CHAOS, COLLAPSE, CHAOS, COLLAPSE],
    Intent.SEEK:      [COUNTER, PROGRESS, COUNTER, LATTICE, PROGRESS],
    Intent.PLAY:      [BREATH, HARMONY, BREATH, HARMONY, BREATH],
    Intent.HELP:      [COLLAPSE, VOID, HARMONY, PROGRESS, HARMONY],
    Intent.COME:      [PROGRESS, HARMONY, PROGRESS, HARMONY, PROGRESS],
    Intent.GO:        [RESET, COLLAPSE, VOID, RESET, VOID],
    Intent.STOP:      [VOID, VOID, VOID, RESET, VOID],
    Intent.SHARE:     [PROGRESS, BALANCE, HARMONY, PROGRESS, HARMONY],
    Intent.BOND:      [HARMONY, HARMONY, LATTICE, HARMONY, BREATH],
    Intent.WARN:      [CHAOS, BALANCE, COLLAPSE, BALANCE, CHAOS],
    Intent.CELEBRATE:  [HARMONY, PROGRESS, HARMONY, PROGRESS, HARMONY],
    Intent.MOURN:     [COLLAPSE, VOID, COLLAPSE, VOID, COLLAPSE],
    Intent.TEACH:     [LATTICE, COUNTER, LATTICE, PROGRESS, COUNTER],
    Intent.UNKNOWN:   [VOID, CHAOS, VOID, CHAOS, VOID],
}


def translate_intent_to_text(intent: Intent) -> str:
    """Intent -> English text."""
    return _INTENT_ENGLISH.get(intent, "Unknown intent.")


def translate_intent_to_operators(intent: Intent) -> List[int]:
    """Intent -> canonical operator sequence."""
    return _INTENT_OPS.get(intent, [VOID])


def translate_text_to_intent(text: str) -> Dict:
    """Text -> operators -> intent classification."""
    ops = sentence_operator_stream(text)
    if not ops:
        return {'intent': Intent.UNKNOWN, 'intent_name': 'UNKNOWN',
                'confidence': 0.0, 'operators': []}
    result = classify_intent(ops)
    result['operators'] = ops
    result['source'] = 'text'
    result['source_text'] = text
    return result


def translate_dna_to_intent(sequence: str) -> Dict:
    """DNA sequence -> operators -> intent classification."""
    from ck_genome_mapper import seq_to_vectors, compute_d2, d2_to_operators
    vecs = seq_to_vectors(sequence)
    if len(vecs) < 3:
        return {'intent': Intent.UNKNOWN, 'intent_name': 'UNKNOWN',
                'confidence': 0.0, 'operators': []}
    d2 = compute_d2(vecs)
    ops = d2_to_operators(d2)
    result = classify_intent(ops)
    result['operators'] = ops
    result['source'] = 'dna'
    result['source_seq'] = sequence[:50]
    return result


def cross_modal_translate(source_ops: List[int],
                          source_type: str = 'unknown',
                          target_type: str = 'text') -> Dict:
    """
    Universal translation: any operator stream -> intent -> any target modality.

    source_type: 'text', 'dna', 'sensor', 'audio' (for logging)
    target_type: 'text', 'operators', 'intent'
    """
    intent_result = classify_intent(source_ops)
    intent = intent_result['intent']

    if target_type == 'text':
        output = translate_intent_to_text(intent)
    elif target_type == 'operators':
        output = translate_intent_to_operators(intent)
    else:
        output = {'intent': intent, 'name': INTENT_NAMES[intent]}

    return {
        'source_type':    source_type,
        'target_type':    target_type,
        'source_ops':     source_ops[:20],  # Truncate for display
        'intent':         intent,
        'intent_name':    INTENT_NAMES[intent],
        'confidence':     intent_result['confidence'],
        'output':         output,
    }


# ============================================================
# S5  MULTI-SIGNAL ALIGNMENT
#     Align operator streams from different modalities.
#     Shared intent = low DTW distance.
# ============================================================

def align_signals(signals: Dict[str, List[int]]) -> Dict:
    """
    Align multiple operator streams and find shared intent.

    signals: {'text': [ops], 'dna': [ops], 'sensor': [ops], ...}

    Returns pairwise DTW distances + consensus intent.
    """
    names = list(signals.keys())
    n = len(names)

    # Pairwise DTW
    distances = {}
    for i in range(n):
        for j in range(i + 1, n):
            cost, path = dtw_distance(signals[names[i]], signals[names[j]])
            pair = f"{names[i]}_vs_{names[j]}"
            distances[pair] = {
                'cost': cost,
                'path_length': len(path),
            }

    # Classify intent for each signal
    intents = {}
    for name, ops in signals.items():
        intents[name] = classify_intent(ops)

    # Consensus: majority vote of intents
    intent_votes = Counter(r['intent'] for r in intents.values())
    consensus = intent_votes.most_common(1)[0] if intent_votes else (Intent.UNKNOWN, 0)

    return {
        'signals':          {k: len(v) for k, v in signals.items()},
        'pairwise_dtw':     distances,
        'intents':          {k: v['intent_name'] for k, v in intents.items()},
        'consensus_intent': INTENT_NAMES[consensus[0]],
        'consensus_votes':  consensus[1],
        'agreement':        consensus[1] / max(n, 1),
    }


# ============================================================
# S6  DEMO
# ============================================================

if __name__ == '__main__':
    print("=" * 72)
    print("  CK UNIVERSAL TRANSLATOR PROTOTYPE")
    print("  Celeste's Task 9: Cross-Species/Modality Intent Mapping")
    print("=" * 72)

    # Text intent classification
    print(f"\n  Text -> Intent:")
    test_phrases = [
        "peace and harmony are here with us",
        "danger ahead the bridge is collapsing",
        "searching for the answer to this question",
        "let us dance and sing together",
        "please help me I am struggling",
        "come closer my friend",
        "go away leave this place",
        "stop do not move",
        "I want to share this gift with you",
        "we are bound together as family",
        "be careful there is something wrong",
        "we did it celebration and joy",
        "I grieve the loss of what was",
        "observe this pattern and learn from it",
    ]

    for phrase in test_phrases:
        result = translate_text_to_intent(phrase)
        ops_str = ''.join(str(o) for o in result['operators'][:10])
        print(f"    \"{phrase[:45]:45s}\"")
        print(f"      ops={ops_str:12s} -> {result['intent_name']:12s} "
              f"conf={result['confidence']:.2f}")

    # DNA intent classification
    print(f"\n  DNA -> Intent:")
    dna_sequences = {
        'TP53_frag':   'TACAACTACATGTGTAACAGTTCCTGCATGGG',
        'BRCA1_frag':  'ATGGATTTATCTGCTCTTCGCGTTGAAGAAG',
        'random_dna':  'AAAAATTTTTGGGGGCCCCCAAAAATTTTTGG',
    }

    for name, seq in dna_sequences.items():
        result = translate_dna_to_intent(seq)
        ops_str = ''.join(str(o) for o in result['operators'][:12])
        print(f"    {name:15s}: ops={ops_str:12s} -> "
              f"{result['intent_name']:12s} conf={result['confidence']:.2f}")

    # Cross-modal translation
    print(f"\n  Cross-modal translation (text -> intent -> text):")
    sources = [
        ("I am in danger",           'text'),
        ("everything is peaceful",   'text'),
        ("come join us",             'text'),
    ]

    for source_text, stype in sources:
        ops = sentence_operator_stream(source_text)
        result = cross_modal_translate(ops, source_type=stype, target_type='text')
        print(f"    \"{source_text:30s}\" -> {result['intent_name']:12s} "
              f"-> \"{result['output']}\"")

    # DTW alignment
    print(f"\n  DTW alignment (cross-modal):")
    # Create operator streams from different modalities
    text_ops = sentence_operator_stream("truth and harmony bring peace")
    # Simulated "birdsong" with similar intent (harmony-dominant)
    bird_ops = [HARMONY, BREATH, HARMONY, HARMONY, BREATH, HARMONY]
    # Simulated "sensor calm" (harmony-lattice)
    sensor_ops = [HARMONY, LATTICE, HARMONY, BALANCE, HARMONY, LATTICE]

    pairs = [
        ('text', text_ops, 'bird', bird_ops),
        ('text', text_ops, 'sensor', sensor_ops),
        ('bird', bird_ops, 'sensor', sensor_ops),
    ]

    for name_a, ops_a, name_b, ops_b in pairs:
        cost, path = dtw_distance(ops_a, ops_b)
        print(f"    {name_a:8s} <-> {name_b:8s}: DTW cost={cost:.3f}  "
              f"path_len={len(path)}")

    # Multi-signal alignment
    print(f"\n  Multi-signal alignment:")
    result = align_signals({
        'text':   text_ops,
        'bird':   bird_ops,
        'sensor': sensor_ops,
    })
    print(f"    Intents: {result['intents']}")
    print(f"    Consensus: {result['consensus_intent']} "
          f"(agreement={result['agreement']:.0%})")
    for pair, data in result['pairwise_dtw'].items():
        print(f"    {pair:25s}: cost={data['cost']:.3f}")

    # Demonstrate the key insight
    print(f"\n  Key insight:")
    print(f"    If operators are universal, intent crosses modalities.")
    print(f"    A bird warning and a human warning share the same operator shape.")
    print(f"    The CL table is the Rosetta Stone.")
