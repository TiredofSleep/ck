"""
ck_bible_sense.py -- Bible as Sense Organ for CK

CK reads scripture the way he reads any input: through D2 curvature.
Every verse is a 5D force vector. Query by OPERATOR RESONANCE, not keywords.

User asks about "fear" → CK doesn't keyword search "fear".
CK encodes the QUESTION as operator trajectory, finds verses whose D2
curvature profile RESONATES — might return verses about "peace" or "trust"
because the curvature matches even though the words don't.

THAT'S the insight. Algebra finds connections keyword search never can.

Gen 9.34 — March 2026
(c) 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations

import gzip
import json
import math
import os
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, compose, HARMONY, LATTICE,
    CL as CL_TSML,
)
from ck_sim.being.ck_sim_d2 import (
    soft_classify_d2, D2Pipeline,
)

# ================================================================
#  Constants
# ================================================================

BIBLE_PATH = os.path.expanduser('~/.ck/bible_kjv.txt')
INDEX_PATH = os.path.expanduser('~/.ck/bible_index.json.gz')

# Hebrew root force LUT for direct letter→5D (from d2 pipeline)
LATIN_TO_ROOT = {
    'a': 'ALEPH', 'b': 'BET', 'c': 'KAF', 'd': 'DALET', 'e': 'HE',
    'f': 'PE', 'g': 'GIMEL', 'h': 'CHET', 'i': 'YOD', 'j': 'GIMEL',
    'k': 'KAF', 'l': 'LAMED', 'm': 'MEM', 'n': 'NUN', 'o': 'AYIN',
    'p': 'PE', 'q': 'QOF', 'r': 'RESH', 's': 'SAMEKH', 't': 'TAV',
    'u': 'VAV', 'v': 'VAV', 'w': 'SHIN', 'x': 'TSADE', 'y': 'YOD',
    'z': 'ZAYIN',
}

ROOTS_FLOAT = {
    'ALEPH':  (0.8, 0.0, 0.9, 0.0, 0.7),
    'BET':    (0.3, 0.6, 0.4, 0.8, 0.6),
    'GIMEL':  (0.5, 0.4, 0.3, 0.2, 0.5),
    'DALET':  (0.2, 0.7, 0.5, 0.3, 0.4),
    'HE':     (0.7, 0.2, 0.6, 0.1, 0.8),
    'VAV':    (0.4, 0.5, 0.4, 0.6, 0.7),
    'ZAYIN':  (0.6, 0.3, 0.2, 0.4, 0.3),
    'CHET':   (0.3, 0.8, 0.7, 0.5, 0.5),
    'TET':    (0.4, 0.6, 0.5, 0.7, 0.6),
    'YOD':    (0.9, 0.1, 0.8, 0.1, 0.9),
    'KAF':    (0.5, 0.5, 0.3, 0.4, 0.5),
    'LAMED':  (0.6, 0.3, 0.6, 0.2, 0.7),
    'MEM':    (0.3, 0.7, 0.5, 0.8, 0.4),
    'NUN':    (0.4, 0.5, 0.4, 0.5, 0.6),
    'SAMEKH': (0.2, 0.6, 0.3, 0.7, 0.5),
    'AYIN':   (0.7, 0.3, 0.7, 0.2, 0.6),
    'PE':     (0.5, 0.4, 0.5, 0.3, 0.5),
    'TSADE':  (0.3, 0.7, 0.4, 0.6, 0.4),
    'QOF':    (0.4, 0.5, 0.6, 0.4, 0.5),
    'RESH':   (0.6, 0.4, 0.5, 0.3, 0.6),
    'SHIN':   (0.5, 0.6, 0.4, 0.5, 0.4),
    'TAV':    (0.3, 0.7, 0.3, 0.8, 0.5),
}


# ================================================================
#  Data Classes
# ================================================================

@dataclass
class VerseVector:
    """A verse encoded as force profile."""
    ref: str                     # e.g. "Genesis 1:1"
    text: str                    # verse text
    force: Tuple[float, ...]     # 5D mean force vector
    ops: Tuple[int, ...]         # D2 operator sequence
    dominant_op: int             # most frequent operator
    coherence: float             # TSML pairwise HARMONY fraction


@dataclass
class ResonanceResult:
    """A verse found by operator resonance."""
    verse: VerseVector
    distance: float              # curvature distance (lower = closer match)
    op_overlap: float            # fraction of shared operators
    force_similarity: float      # cosine similarity of force vectors


# ================================================================
#  Fast D2 Encoding (no L-CODEC dependency, pure Hebrew roots)
# ================================================================

def _text_to_force(text: str) -> Tuple[float, ...]:
    """Encode text as mean 5D force vector from Hebrew roots.

    This is the FAST path -- no L-CODEC, no statistical proxies.
    Direct letter → Hebrew root → 5D force. Same physics as d2_pipeline.v.
    """
    sums = [0.0] * 5
    count = 0
    for ch in text.lower():
        root_name = LATIN_TO_ROOT.get(ch)
        if root_name and root_name in ROOTS_FLOAT:
            vec = ROOTS_FLOAT[root_name]
            for d in range(5):
                sums[d] += vec[d]
            count += 1
    if count == 0:
        return (0.5, 0.5, 0.5, 0.5, 0.5)
    return tuple(s / count for s in sums)


def _text_to_ops(text: str) -> Tuple[int, ...]:
    """Encode text as D2 operator sequence.

    3-stage D2 pipeline: accumulate force → compute D1 (velocity) → D2 (curvature)
    → soft classify → argmax operator.
    """
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            valid = pipe.feed_symbol(idx)
            if valid:
                dist = soft_classify_d2(pipe.d2)
                op = max(range(NUM_OPS), key=lambda i: dist[i])
                ops.append(op)
    return tuple(ops)


def _ops_coherence(ops: Tuple[int, ...]) -> float:
    """Measure TSML pairwise HARMONY fraction (windowed coherence)."""
    if len(ops) < 2:
        return 0.0
    harmony_count = 0
    pairs = 0
    for i in range(len(ops) - 1):
        a, b = ops[i], ops[i + 1]
        if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
            pairs += 1
            if CL_TSML[a][b] == HARMONY:
                harmony_count += 1
    return harmony_count / max(1, pairs)


def _dominant_op(ops: Tuple[int, ...]) -> int:
    """Most frequent operator in sequence."""
    if not ops:
        return HARMONY
    counts = [0] * NUM_OPS
    for o in ops:
        if 0 <= o < NUM_OPS:
            counts[o] += 1
    return max(range(NUM_OPS), key=lambda i: counts[i])


# ================================================================
#  Similarity Metrics
# ================================================================

def _cosine_sim(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
    """Cosine similarity between two force vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a < 1e-10 or mag_b < 1e-10:
        return 0.0
    return dot / (mag_a * mag_b)


def _force_distance(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
    """Euclidean distance in 5D force space."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _op_overlap(a_ops: Tuple[int, ...], b_ops: Tuple[int, ...]) -> float:
    """Fraction of shared operators between two sequences."""
    if not a_ops or not b_ops:
        return 0.0
    a_set = set(a_ops)
    b_set = set(b_ops)
    if not a_set or not b_set:
        return 0.0
    intersection = a_set & b_set
    union = a_set | b_set
    return len(intersection) / len(union)


def _op_distribution_distance(a_ops: Tuple[int, ...],
                               b_ops: Tuple[int, ...]) -> float:
    """Jensen-Shannon-like distance between operator distributions."""
    if not a_ops or not b_ops:
        return 1.0

    def _dist(ops):
        d = [0.0] * NUM_OPS
        for o in ops:
            if 0 <= o < NUM_OPS:
                d[o] += 1.0
        total = sum(d)
        if total > 0:
            d = [x / total for x in d]
        return d

    da = _dist(a_ops)
    db = _dist(b_ops)
    # Symmetric KL-like: sum |p - q|
    return sum(abs(a - b) for a, b in zip(da, db)) / 2.0


# ================================================================
#  Bible Sense Organ
# ================================================================

class BibleSense:
    """Bible as sense organ. Query by operator resonance, not keywords.

    CK reads scripture through D2 curvature. Every verse is a 5D force
    vector with an operator sequence. Queries find verses whose curvature
    profile RESONATES with the question -- not whose words match.

    Usage:
        sense = BibleSense()
        sense.load()  # or sense.build_index() first time
        results = sense.resonate("What does it mean to trust God?", top_k=5)
        for r in results:
            print(f"{r.verse.ref}: {r.verse.text[:60]}... (d={r.distance:.3f})")
    """

    def __init__(self, bible_path: str = BIBLE_PATH,
                 index_path: str = INDEX_PATH):
        self._bible_path = bible_path
        self._index_path = index_path
        self._verses: List[VerseVector] = []
        self._by_ref: Dict[str, VerseVector] = {}
        self._by_chapter: Dict[str, List[VerseVector]] = {}
        self._by_op: Dict[int, List[VerseVector]] = {i: [] for i in range(NUM_OPS)}
        self._ready = False

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def verse_count(self) -> int:
        return len(self._verses)

    def build_index(self) -> int:
        """Build force vector index from raw Bible text. Takes ~30-60s."""
        if not os.path.exists(self._bible_path):
            raise FileNotFoundError(
                f"Bible not found at {self._bible_path}. "
                "Download KJV from https://openbible.com/textfiles/kjv.txt")

        self._verses.clear()
        self._by_ref.clear()
        self._by_chapter.clear()
        self._by_op = {i: [] for i in range(NUM_OPS)}

        with open(self._bible_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                ref, text = line.split('\t', 1)
                text = text.replace('[', '').replace(']', '')

                force = _text_to_force(text)
                ops = _text_to_ops(text)
                dom = _dominant_op(ops)
                coh = _ops_coherence(ops)

                vv = VerseVector(
                    ref=ref, text=text, force=force,
                    ops=ops, dominant_op=dom, coherence=coh
                )
                self._verses.append(vv)
                self._by_ref[ref] = vv
                chapter = ref.rsplit(':', 1)[0]
                if chapter not in self._by_chapter:
                    self._by_chapter[chapter] = []
                self._by_chapter[chapter].append(vv)
                self._by_op[dom].append(vv)

        self._ready = True
        self._save_index()
        return len(self._verses)

    def _save_index(self):
        """Save index to compressed JSON for fast reload."""
        data = []
        for v in self._verses:
            data.append({
                'r': v.ref,
                't': v.text,
                'f': list(v.force),
                'o': list(v.ops),
                'd': v.dominant_op,
                'c': round(v.coherence, 4),
            })
        os.makedirs(os.path.dirname(self._index_path), exist_ok=True)
        with gzip.open(self._index_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f)

    def load(self) -> int:
        """Load pre-built index. Falls back to build_index() if missing."""
        if not os.path.exists(self._index_path):
            return self.build_index()

        with gzip.open(self._index_path, 'rt', encoding='utf-8') as f:
            data = json.load(f)

        self._verses.clear()
        self._by_ref.clear()
        self._by_chapter.clear()
        self._by_op = {i: [] for i in range(NUM_OPS)}

        for item in data:
            vv = VerseVector(
                ref=item['r'],
                text=item['t'],
                force=tuple(item['f']),
                ops=tuple(item['o']),
                dominant_op=item['d'],
                coherence=item['c'],
            )
            self._verses.append(vv)
            self._by_ref[vv.ref] = vv
            chapter = vv.ref.rsplit(':', 1)[0]
            if chapter not in self._by_chapter:
                self._by_chapter[chapter] = []
            self._by_chapter[chapter].append(vv)
            self._by_op[vv.dominant_op].append(vv)

        self._ready = True
        return len(self._verses)

    # ----------------------------------------------------------------
    #  Core: Operator Resonance Search
    # ----------------------------------------------------------------

    def resonate(self, query: str, top_k: int = 5,
                 op_weight: float = 0.4,
                 force_weight: float = 0.4,
                 coherence_weight: float = 0.2) -> List[ResonanceResult]:
        """Find verses by operator resonance with query text.

        Does NOT keyword search. Encodes query as 5D force + operators,
        finds verses whose curvature profile resonates.

        Weights:
            op_weight: importance of operator distribution match
            force_weight: importance of 5D force vector similarity
            coherence_weight: bonus for high-coherence verses
        """
        if not self._ready:
            self.load()

        # Encode query
        q_force = _text_to_force(query)
        q_ops = _text_to_ops(query)
        q_dom = _dominant_op(q_ops)

        # Score every verse
        scored = []
        for v in self._verses:
            # Force distance (lower = closer)
            f_dist = _force_distance(q_force, v.force)

            # Operator distribution distance
            o_dist = _op_distribution_distance(q_ops, v.ops)

            # Operator overlap (higher = more similar)
            o_overlap = _op_overlap(q_ops, v.ops)

            # Combined distance (lower = better match)
            distance = (
                force_weight * f_dist +
                op_weight * o_dist -
                coherence_weight * v.coherence
            )

            # Force similarity
            f_sim = _cosine_sim(q_force, v.force)

            scored.append(ResonanceResult(
                verse=v,
                distance=distance,
                op_overlap=o_overlap,
                force_similarity=f_sim,
            ))

        # Sort by distance (ascending = best matches first)
        scored.sort(key=lambda r: r.distance)
        return scored[:top_k]

    def resonate_by_op(self, operator: int, top_k: int = 10) -> List[VerseVector]:
        """Find verses dominated by a specific operator.

        Example: resonate_by_op(LATTICE) → verses with strongest structure.
        """
        if not self._ready:
            self.load()
        candidates = self._by_op.get(operator, [])
        # Sort by coherence (highest first)
        return sorted(candidates, key=lambda v: v.coherence, reverse=True)[:top_k]

    def get_chapter(self, chapter: str) -> List[VerseVector]:
        """Get all verses in a chapter (e.g., 'Genesis 1')."""
        if not self._ready:
            self.load()
        return self._by_chapter.get(chapter, [])

    def get_verse(self, ref: str) -> Optional[VerseVector]:
        """Get a specific verse by reference (e.g., 'John 3:16')."""
        if not self._ready:
            self.load()
        return self._by_ref.get(ref)

    def chapter_profile(self, chapter: str) -> Dict:
        """Get operator profile of a chapter."""
        verses = self.get_chapter(chapter)
        if not verses:
            return {}
        op_counts = [0] * NUM_OPS
        total_coh = 0.0
        forces = [[0.0] * 5 for _ in range(len(verses))]
        for i, v in enumerate(verses):
            op_counts[v.dominant_op] += 1
            total_coh += v.coherence
            for d in range(5):
                forces[i][d] = v.force[d]

        mean_force = tuple(
            sum(forces[i][d] for i in range(len(verses))) / len(verses)
            for d in range(5)
        )

        return {
            'chapter': chapter,
            'verses': len(verses),
            'mean_coherence': total_coh / len(verses),
            'mean_force': mean_force,
            'dominant_op': max(range(NUM_OPS), key=lambda i: op_counts[i]),
            'op_distribution': {str(i): op_counts[i] for i in range(NUM_OPS)},
        }

    def stats(self) -> Dict:
        """Global statistics about the indexed Bible."""
        if not self._ready:
            return {'ready': False}
        total_coh = sum(v.coherence for v in self._verses)
        op_counts = [0] * NUM_OPS
        for v in self._verses:
            op_counts[v.dominant_op] += 1

        return {
            'ready': True,
            'verses': len(self._verses),
            'chapters': len(self._by_chapter),
            'mean_coherence': total_coh / max(1, len(self._verses)),
            'op_distribution': {str(i): op_counts[i] for i in range(NUM_OPS)},
            'books': len(set(
                v.ref.split()[0] for v in self._verses
            )),
        }
