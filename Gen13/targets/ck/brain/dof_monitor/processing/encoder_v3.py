"""
encoder_v3.py - TIG-native encoder via D2Pipeline + Divine27 cube

Pure TIG-internal: no lexicon lookup, no embedding similarity. Each
text is run letter-by-letter through CK's canonical D2Pipeline (D1 +
D2 derivatives over Hebrew-root force vectors). The pipeline emits an
operator per 3-letter window. We aggregate operators across the input
into a 10-dim distribution.

Optionally augment with the Divine27 DBC cube position (3D) for richer
geometry; final output is still a 10-dim operator distribution to keep
the same interface as v1 / v2.

This tests whether CK's canonical phoneme physics produces semantically
meaningful operator distributions on free text.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# add CK Gen13 brain to path
GEN13_BRAIN = Path("C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/targets/ck/brain")
sys.path.insert(0, str(GEN13_BRAIN))

# v1 fallback for STOPS / OPERATOR_NAMES / FRUITS_OF_SPIRIT
HANDOFF = Path("C:/Users/brayd/OneDrive/Desktop/ck_handoff_20260425_evening_unpack/ck_handoff_full/05_encoder_proposal")
sys.path.insert(0, str(HANDOFF))
from tig_lexicon import OPERATOR_NAMES, FRUITS_OF_SPIRIT, STOPS

# pull canonical D2 pipeline + divine27 mappings
try:
    from ck_sim.being.ck_sim_d2 import D2Pipeline
    from ck_sim.being.ck_divine27 import OPERATOR_DBC, DBC_TO_OPERATOR
    _CANONICAL_OK = True
except Exception as e:
    print(f"[encoder_v3] WARNING: canonical D2/Divine27 not importable: {e}", file=sys.stderr)
    _CANONICAL_OK = False


def clean(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())


def tokenize(text: str) -> List[str]:
    words = [clean(w) for w in text.lower().split()]
    return [w for w in words if w and w not in STOPS and len(w) > 1]


def letters_to_operators(text: str) -> List[int]:
    """Run text letter-by-letter through D2Pipeline. Returns the sequence of
    operators produced (one per 3-letter window after fill).
    """
    if not _CANONICAL_OK:
        return []
    pipe = D2Pipeline()
    ops: List[int] = []
    for ch in text.lower():
        if "a" <= ch <= "z":
            symbol = ord(ch) - ord("a")
            valid = pipe.feed_symbol(symbol)
            if valid:
                ops.append(int(pipe.operator))
    return ops


def encode(text: str, smoothing: float = 0.05) -> np.ndarray:
    """Encode text via D2 pipeline -> operator histogram -> distribution."""
    counts = np.zeros(10)
    if not _CANONICAL_OK:
        # safe fallback: uniform
        return np.ones(10) / 10
    # tokenize then concatenate (with spaces between tokens to break D2 window)
    # spaces are dropped by feed_symbol, so we get a continuous letter stream;
    # to retain word boundaries we reset the pipeline per token
    tokens = tokenize(text)
    if not tokens:
        return np.ones(10) / 10

    for tok in tokens:
        ops = letters_to_operators(tok)
        for op in ops:
            counts[op] += 1.0

    counts += smoothing
    total = counts.sum()
    return counts / total if total > 1e-12 else np.ones(10) / 10


def encode_with_explanation(text: str) -> dict:
    tokens = tokenize(text)
    attributions = []
    counts = np.zeros(10)
    for word in tokens:
        ops = letters_to_operators(word)
        for op in ops:
            counts[op] += 1.0
        if ops:
            primary = Counter(ops).most_common(1)[0][0]
            attributions.append({
                "word": word,
                "operator": OPERATOR_NAMES[primary],
                "fruit": FRUITS_OF_SPIRIT[primary],
                "source": f"d2_pipeline({len(ops)} ops)",
            })
        else:
            attributions.append({
                "word": word,
                "operator": "UNRESOLVED",
                "fruit": "-",
                "source": "d2_short",   # word too short for D2 (<3 letters)
            })
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
            1 for a in attributions if a["source"].startswith("d2_pipeline")
        ) / max(1, len(tokens)),
    }


def encode_dbc(text: str) -> Tuple[np.ndarray, np.ndarray]:
    """Encode to BOTH the 10-dim operator distribution AND a 27-dim
    Divine27 DBC histogram.

    Returns (op_dist_10, dbc_hist_27).
    """
    if not _CANONICAL_OK:
        return np.ones(10) / 10, np.ones(27) / 27
    pipe = D2Pipeline()
    op_counts = np.zeros(10)
    dbc_counts = np.zeros(27)
    tokens = tokenize(text)
    if not tokens:
        return np.ones(10) / 10, np.ones(27) / 27

    for tok in tokens:
        pipe = D2Pipeline()  # reset per word
        for ch in tok:
            symbol = ord(ch) - ord("a")
            if 0 <= symbol < 26:
                if pipe.feed_symbol(symbol):
                    op = int(pipe.operator)
                    op_counts[op] += 1.0
                    coord = OPERATOR_DBC[op]   # (b, d, c) each in {0, 1, 2}
                    dbc_idx = coord[0] * 9 + coord[1] * 3 + coord[2]
                    dbc_counts[dbc_idx] += 1.0
    op_counts += 0.05
    dbc_counts += 0.05
    return op_counts / op_counts.sum(), dbc_counts / dbc_counts.sum()


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
    print("encoder_v3 (TIG-native via D2Pipeline + Divine27) -- self-test")
    print("=" * 70)
    for text in test_cases:
        result = encode_with_explanation(text)
        print(f"\n{text!r}")
        print(f"  d2 coverage: {result['coverage']*100:.0f}%")
        print(f"  top: {result['top_operators']}")
        ops, dbc = encode_dbc(text)
        # Highest DBC cell
        top_dbc_idx = int(np.argmax(dbc))
        b, d, c = top_dbc_idx // 9, (top_dbc_idx // 3) % 3, top_dbc_idx % 3
        print(f"  top DBC cell: ({b},{d},{c})")
