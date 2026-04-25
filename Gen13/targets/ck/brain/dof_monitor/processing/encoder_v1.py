"""
encoder_v1.py — LEXICON-BASED TEXT ENCODER

Maps text → 10-dim operator distribution using rule-based lexicon lookup.

Six layers (cascading resolution):
  1. Tokenize (word-level, stopword filter)
  2. Direct keyword lookup (weight 1.0)
  3. Stem-based lookup (weight 0.8) — basic morphology
  4. Phonaesthesia (weight 0.5) — initial consonant cluster
  5. Letter-level grapheme (weight 0.2) — fallback
  6. Aggregate + smooth + normalize

NO TORCH. NO EMBEDDING MODEL. Pure rule-based.

This is the runnable-now version. encoder_v2 adds embedding similarity
for unresolved words.

Usage:
    from encoder_v1 import encode
    p = encode("I want to be more patient")
    # Returns 10-dim numpy array, sums to 1
"""
import re
import numpy as np
from typing import Optional, Tuple, List
from collections import Counter

from tig_lexicon import (
    OPERATOR_KEYWORDS, PHONAESTHESIA, GRAPHEME_OP, STOPS,
    OPERATOR_NAMES, FRUITS_OF_SPIRIT,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)


# ============================================================
# Tokenization helpers
# ============================================================

def clean(word: str) -> str:
    """Strip punctuation, lowercase."""
    return re.sub(r'[^a-zA-Z]', '', word.lower())


def stem(word: str) -> str:
    """Minimal morphological stemming."""
    for suffix in ('ing', 'ed', 'ly', 'ness', 'ment', 'tion', 'sion',
                   'er', 'est', 'ize', 'ise', 's'):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word


def tokenize(text: str) -> List[str]:
    """Word-level tokenization with stopword removal."""
    words = [clean(w) for w in text.lower().split()]
    return [w for w in words if w and w not in STOPS and len(w) > 1]


# ============================================================
# Word resolution (cascading layers)
# ============================================================

def word_to_operator(word: str) -> Tuple[Optional[int], str]:
    """
    Resolve a word to a single operator using cascading layers.
    
    Returns:
        (operator_index, source_layer_name) or (None, 'unresolved')
    """
    if not word:
        return None, 'unresolved'

    # Layer 1: direct keyword
    for op, vocab in OPERATOR_KEYWORDS.items():
        if word in vocab:
            return op, 'keyword'

    # Layer 2: stem match
    sw = stem(word)
    if sw != word:
        for op, vocab in OPERATOR_KEYWORDS.items():
            if sw in vocab:
                return op, 'stem'

    # Layer 3: phonaesthesia
    if len(word) >= 2 and word[:2] in PHONAESTHESIA:
        return PHONAESTHESIA[word[:2]], 'phonaesthesia'

    # Layer 4: grapheme fallback (most common letter's operator)
    letter_ops = [GRAPHEME_OP[c] for c in word if c in GRAPHEME_OP]
    if letter_ops:
        return Counter(letter_ops).most_common(1)[0][0], 'grapheme'

    return None, 'unresolved'


# ============================================================
# Encoding (text → distribution)
# ============================================================

def encode(text: str, smoothing: float = 0.05) -> np.ndarray:
    """
    Encode text as 10-dim probability distribution over operators.

    Args:
        text: input string
        smoothing: uniform mass added to all operators
                   (avoids zero entries; 0.05 → 0.5 spread total)

    Returns:
        10-dim numpy array, sums to 1.0
    """
    counts = np.zeros(10)
    tokens = tokenize(text)

    if not tokens:
        return np.ones(10) / 10  # uniform fallback

    # Source-confidence weights
    weights = {'keyword': 1.0, 'stem': 0.8, 'phonaesthesia': 0.5,
               'grapheme': 0.2, 'unresolved': 0.0}

    for word in tokens:
        op, source = word_to_operator(word)
        if op is not None:
            counts[op] += weights.get(source, 0.0)

    counts += smoothing  # smoothing
    total = counts.sum()
    return counts / total if total > 1e-12 else np.ones(10) / 10


def encode_with_explanation(text: str) -> dict:
    """
    Encode text and return distribution + per-token attribution.
    Useful for debugging encoder behavior.
    """
    tokens = tokenize(text)
    attributions = []
    counts = np.zeros(10)
    weights = {'keyword': 1.0, 'stem': 0.8, 'phonaesthesia': 0.5,
               'grapheme': 0.2}

    for word in tokens:
        op, source = word_to_operator(word)
        attributions.append({
            'word': word,
            'operator': OPERATOR_NAMES[op] if op is not None else 'UNRESOLVED',
            'fruit': FRUITS_OF_SPIRIT[op] if op is not None else '-',
            'source': source,
        })
        if op is not None:
            counts[op] += weights.get(source, 0.0)

    counts += 0.05
    total = counts.sum()
    distribution = counts / total if total > 1e-12 else np.ones(10) / 10

    return {
        'text': text,
        'tokens': tokens,
        'attributions': attributions,
        'distribution': distribution,
        'top_operators': [
            (OPERATOR_NAMES[i], float(distribution[i]))
            for i in np.argsort(-distribution)[:3]
        ],
        'coverage': sum(1 for a in attributions
                        if a['source'] in ('keyword', 'stem')) / max(1, len(tokens)),
    }


# ============================================================
# Self-test
# ============================================================

if __name__ == "__main__":
    test_cases = [
        "I want to be more patient",
        "Help me find peace and stillness",
        "Build something new and creative",
        "I feel chaotic and overwhelmed",
        "Please reset everything and start fresh",
        "harmony and gentleness",
        "the structure of the lattice",
        "the algorithm processes inputs",   # generic ML text
    ]

    print("Encoder V1 — Self-Test")
    print("=" * 70)
    for text in test_cases:
        result = encode_with_explanation(text)
        print(f"\nInput: {text!r}")
        print(f"  Coverage (keyword/stem): {result['coverage']*100:.0f}%")
        print(f"  Top: {result['top_operators']}")
