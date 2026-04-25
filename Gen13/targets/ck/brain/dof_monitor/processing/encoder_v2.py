"""
encoder_v2.py — EMBEDDING-AUGMENTED TEXT ENCODER

Falls back to V1 lexicon for known words. For unknown words, uses
sentence-transformer embedding similarity to assign each unresolved
word to its closest operator anchor.

REQUIRES: sentence-transformers (pip install sentence-transformers)

If sentence-transformers is not installed, this file falls back to a
random stub for the embedding layer (the lexicon layer still works).

This is a SCAFFOLD — the model loading, anchor embedding, and similarity
computation are real. The actual quality depends on which model you load
and what anchor texts you give each operator.

For Claude Code:
  - Install sentence-transformers
  - Pick a model (e.g., 'all-MiniLM-L6-v2' for speed, 'all-mpnet-base-v2' for quality)
  - Test on your actual query corpus
  - Compare cluster separation vs encoder_v1
"""
import re
import numpy as np
from typing import Optional, Tuple, List
from collections import Counter

from tig_lexicon import (
    OPERATOR_KEYWORDS, PHONAESTHESIA, GRAPHEME_OP, STOPS,
    OPERATOR_NAMES, FRUITS_OF_SPIRIT,
)
from encoder_v1 import (
    clean, stem, tokenize, word_to_operator,
    encode as encode_v1,
)


# ============================================================
# Embedding model (lazy load)
# ============================================================

_MODEL = None
_ANCHOR_EMBEDDINGS = None  # 10 x embedding_dim


def _ensure_model(model_name: str = 'all-MiniLM-L6-v2'):
    """Lazy-load the sentence-transformer model."""
    global _MODEL, _ANCHOR_EMBEDDINGS
    if _MODEL is not None:
        return _MODEL, _ANCHOR_EMBEDDINGS

    try:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(model_name)

        # Build anchor embeddings — concatenate top keywords for each operator
        anchor_texts = []
        for op in range(10):
            keywords = list(OPERATOR_KEYWORDS[op])[:8]  # top 8 anchor words
            fruit = FRUITS_OF_SPIRIT[op]
            anchor_text = f"{OPERATOR_NAMES[op]} {fruit} {' '.join(keywords)}"
            anchor_texts.append(anchor_text)

        _ANCHOR_EMBEDDINGS = _MODEL.encode(anchor_texts)
        # Normalize for cosine similarity
        norms = np.linalg.norm(_ANCHOR_EMBEDDINGS, axis=1, keepdims=True)
        _ANCHOR_EMBEDDINGS = _ANCHOR_EMBEDDINGS / (norms + 1e-12)

        return _MODEL, _ANCHOR_EMBEDDINGS

    except ImportError:
        print("⚠️  sentence-transformers not installed. V2 falls back to V1.")
        return None, None


def _embed(texts: List[str]) -> Optional[np.ndarray]:
    """Embed list of texts. Returns None if model unavailable."""
    model, _ = _ensure_model()
    if model is None:
        return None
    embs = model.encode(texts)
    norms = np.linalg.norm(embs, axis=1, keepdims=True)
    return embs / (norms + 1e-12)


def _embedding_to_operator(word: str) -> Tuple[Optional[int], float]:
    """
    Use embedding similarity to assign word to closest operator.
    
    Returns:
        (operator_index, similarity_score) or (None, 0.0) if model unavailable
    """
    embs = _embed([word])
    if embs is None or _ANCHOR_EMBEDDINGS is None:
        return None, 0.0

    # Cosine similarity to each anchor
    similarities = embs[0] @ _ANCHOR_EMBEDDINGS.T  # shape (10,)
    best_op = int(np.argmax(similarities))
    best_score = float(similarities[best_op])
    return best_op, best_score


# ============================================================
# V2 encoder
# ============================================================

def word_to_operator_v2(word: str) -> Tuple[Optional[int], str]:
    """V1 resolution; if unresolved, fall back to embedding similarity."""
    op, source = word_to_operator(word)
    if op is not None and source != 'grapheme':
        # V1 found it via keyword/stem/phonaesthesia — trust it
        return op, source

    # V1 only had grapheme or no match — try embedding
    emb_op, emb_score = _embedding_to_operator(word)
    if emb_op is not None and emb_score > 0.3:  # confidence threshold
        return emb_op, f'embedding({emb_score:.2f})'

    return op, source  # fall back to V1's grapheme or unresolved


def encode(text: str, smoothing: float = 0.05) -> np.ndarray:
    """
    Encode text using lexicon + embedding fallback.
    """
    counts = np.zeros(10)
    tokens = tokenize(text)

    if not tokens:
        return np.ones(10) / 10

    weights_layered = {
        'keyword': 1.0, 'stem': 0.8, 'phonaesthesia': 0.5,
        'grapheme': 0.2,
    }

    for word in tokens:
        op, source = word_to_operator_v2(word)
        if op is not None:
            if source.startswith('embedding'):
                counts[op] += 0.7  # embedding gets weight 0.7
            else:
                counts[op] += weights_layered.get(source, 0.1)

    counts += smoothing
    total = counts.sum()
    return counts / total if total > 1e-12 else np.ones(10) / 10


# ============================================================
# Self-test (compares V1 vs V2)
# ============================================================

if __name__ == "__main__":
    test_cases = [
        "I want to be more patient",
        "Help me find peace and stillness",
        "the algorithm processes inputs",   # generic, V1 gives uniform
        "compassion warmth tenderness",      # semantic, no exact keyword
        "exuberance vibrancy zeal",          # synonyms of joy/lattice
    ]

    print("Encoder V2 vs V1 — Side-by-side")
    print("=" * 70)
    for text in test_cases:
        v1 = encode_v1(text)
        v2 = encode(text)
        print(f"\nInput: {text!r}")
        print(f"  V1 top: {OPERATOR_NAMES[np.argmax(v1)]} ({v1.max():.2f})")
        print(f"  V2 top: {OPERATOR_NAMES[np.argmax(v2)]} ({v2.max():.2f})")
        print(f"  V1 distribution:  {[f'{x:.2f}' for x in v1]}")
        print(f"  V2 distribution:  {[f'{x:.2f}' for x in v2]}")
        diff = float(np.linalg.norm(v1 - v2))
        print(f"  V1↔V2 distance:   {diff:.3f}")


def encode_with_explanation(text: str) -> dict:
    """V2 version of encode_with_explanation, mirroring V1's interface."""
    tokens = tokenize(text)
    attributions = []
    counts = np.zeros(10)
    weights_layered = {
        "keyword": 1.0, "stem": 0.8, "phonaesthesia": 0.5,
        "grapheme": 0.2,
    }
    for word in tokens:
        op, source = word_to_operator_v2(word)
        attributions.append({
            "word": word,
            "operator": OPERATOR_NAMES[op] if op is not None else "UNRESOLVED",
            "fruit": FRUITS_OF_SPIRIT[op] if op is not None else "-",
            "source": source,
        })
        if op is not None:
            if source.startswith("embedding"):
                counts[op] += 0.7
            else:
                counts[op] += weights_layered.get(source, 0.1)
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
            if a["source"] in ("keyword", "stem")
            or a["source"].startswith("embedding")
        ) / max(1, len(tokens)),
    }
