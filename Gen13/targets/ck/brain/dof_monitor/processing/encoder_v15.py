"""
encoder_v15.py - canonical TIG corpus encoder (Ask 1)

Replaces encoder_v1's seed lexicon (~250 words) with the canonical
ck_dictionary.json (112,703 words mapped to operators 0..9 by Brayden's
production pipeline).

Strategy: same six-layer cascade as v1, but layer-1 lookup uses the
112k-word lexicon instead of the seed list. Falls back to v1's stem /
phonaesthesia / grapheme layers for unknowns.

Smoothing parameter and tokenization unchanged from v1.

Goal: cluster separation should jump above v1's 2.27 baseline.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# ----- locate ck_dictionary.json (canonical corpus) -----
CANDIDATE_DICT_PATHS = [
    Path("C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen12/targets/website/ck_dictionary.json"),
    Path("C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/targets/ck/web/ck_dictionary.json"),
]
DICT_PATH = next((p for p in CANDIDATE_DICT_PATHS if p.exists()), None)
if DICT_PATH is None:
    raise SystemExit("ck_dictionary.json not found in known locations")

with open(DICT_PATH, "r", encoding="utf-8") as f:
    _RAW = json.load(f)

# Each entry: { word: {'o': operator_int, 'p': pos_char} }
LEXICON: dict[str, int] = {
    word.lower(): int(meta["o"])
    for word, meta in _RAW["flat"].items()
    if isinstance(meta, dict) and "o" in meta and 0 <= int(meta["o"]) <= 9
}

print(f"[encoder_v15] loaded {len(LEXICON)} words from {DICT_PATH.name}", file=sys.stderr)

# ----- v1 fallback layers -----
sys.path.insert(0, str(Path("C:/Users/brayd/OneDrive/Desktop/ck_handoff_20260425_evening_unpack/ck_handoff_full/05_encoder_proposal")))
from tig_lexicon import (
    OPERATOR_KEYWORDS, PHONAESTHESIA, GRAPHEME_OP, STOPS,
    OPERATOR_NAMES, FRUITS_OF_SPIRIT,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)


def clean(word: str) -> str:
    return re.sub(r"[^a-zA-Z]", "", word.lower())


def stem(word: str) -> str:
    for suffix in ("ing", "ed", "ly", "ness", "ment", "tion", "sion",
                   "er", "est", "ize", "ise", "s"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word


def tokenize(text: str) -> List[str]:
    words = [clean(w) for w in text.lower().split()]
    return [w for w in words if w and w not in STOPS and len(w) > 1]


def word_to_operator(word: str) -> Tuple[Optional[int], str]:
    """Resolve via cascading layers, layer-1 = canonical 112k corpus."""
    if not word:
        return None, "unresolved"

    # Layer 1: canonical corpus direct
    if word in LEXICON:
        return LEXICON[word], "corpus"

    # Layer 1.5: seed-keyword (kept for hand-tuned overrides)
    for op, vocab in OPERATOR_KEYWORDS.items():
        if word in vocab:
            return op, "keyword"

    # Layer 2: stem then corpus, then stem then keyword
    sw = stem(word)
    if sw != word:
        if sw in LEXICON:
            return LEXICON[sw], "corpus_stem"
        for op, vocab in OPERATOR_KEYWORDS.items():
            if sw in vocab:
                return op, "stem"

    # Layer 3: phonaesthesia
    if len(word) >= 2 and word[:2] in PHONAESTHESIA:
        return PHONAESTHESIA[word[:2]], "phonaesthesia"

    # Layer 4: grapheme fallback
    letter_ops = [GRAPHEME_OP[c] for c in word if c in GRAPHEME_OP]
    if letter_ops:
        return Counter(letter_ops).most_common(1)[0][0], "grapheme"

    return None, "unresolved"


WEIGHTS = {
    "corpus": 1.0,
    "keyword": 1.0,
    "corpus_stem": 0.85,
    "stem": 0.8,
    "phonaesthesia": 0.5,
    "grapheme": 0.2,
    "unresolved": 0.0,
}


def encode(text: str, smoothing: float = 0.05) -> np.ndarray:
    counts = np.zeros(10)
    tokens = tokenize(text)
    if not tokens:
        return np.ones(10) / 10
    for word in tokens:
        op, source = word_to_operator(word)
        if op is not None:
            counts[op] += WEIGHTS.get(source, 0.0)
    counts += smoothing
    total = counts.sum()
    return counts / total if total > 1e-12 else np.ones(10) / 10


def encode_with_explanation(text: str) -> dict:
    tokens = tokenize(text)
    attributions = []
    counts = np.zeros(10)
    for word in tokens:
        op, source = word_to_operator(word)
        attributions.append({
            "word": word,
            "operator": OPERATOR_NAMES[op] if op is not None else "UNRESOLVED",
            "fruit": FRUITS_OF_SPIRIT[op] if op is not None else "-",
            "source": source,
        })
        if op is not None:
            counts[op] += WEIGHTS.get(source, 0.0)
    counts += 0.05
    total = counts.sum()
    distribution = counts / total if total > 1e-12 else np.ones(10) / 10
    return {
        "text": text,
        "tokens": tokens,
        "attributions": attributions,
        "distribution": distribution,
        "top_operators": [
            (OPERATOR_NAMES[i], float(distribution[i]))
            for i in np.argsort(-distribution)[:3]
        ],
        "coverage": sum(
            1 for a in attributions
            if a["source"] in ("corpus", "corpus_stem", "keyword", "stem")
        ) / max(1, len(tokens)),
    }


if __name__ == "__main__":
    test_cases = [
        "I want to be more patient",
        "Help me find peace and stillness",
        "Build something new and creative",
        "I feel chaotic and overwhelmed",
        "Please reset everything and start fresh",
        "harmony and gentleness",
        "the structure of the lattice",
        "the algorithm processes inputs",
    ]
    print("encoder_v15 (canonical 112k corpus) -- self-test")
    print("=" * 70)
    for text in test_cases:
        result = encode_with_explanation(text)
        print(f"\n{text!r}")
        print(f"  coverage: {result['coverage']*100:.0f}%")
        print(f"  top: {result['top_operators']}")
