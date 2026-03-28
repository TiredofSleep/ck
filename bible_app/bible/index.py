"""
Bible Index — Every verse encoded as 5D force + operator sequence.

Query by OPERATOR RESONANCE, not keywords.
"I'm scared" might return verses about peace or mountains
because the D2 curvature matches, even though no words overlap.

That's the insight. Algebra finds connections keyword search never can.

(c) 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations

import gzip
import json
import math
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from bible_app.algebra import (
    NUM_OPS, HARMONY, OP_NAMES, T_STAR,
    compose, coherence, dominant_op,
    text_to_force, text_to_ops,
    cosine_similarity, force_distance,
)

# ── Paths ─────────────────────────────────────────────────────────
# Look for Bible in app directory first, then ~/.ck/
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Default to BBE (Bible in Basic English) — modern, simple, public domain
BIBLE_PATH = os.path.join(APP_DIR, 'bible', 'bbe.txt')
INDEX_PATH = os.path.join(APP_DIR, 'bible', 'bbe_index.json.gz')

# Fallback to ~/.ck/ (CK's existing data)
BIBLE_PATH_FALLBACK = os.path.expanduser('~/.ck/bible_kjv.txt')
INDEX_PATH_FALLBACK = os.path.expanduser('~/.ck/bible_index.json.gz')


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
    distance: float              # curvature distance (lower = closer)
    op_overlap: float            # fraction of shared operators
    force_similarity: float      # cosine similarity of force vectors


def _op_distribution(ops):
    """Normalized operator distribution."""
    d = [0.0] * NUM_OPS
    for o in ops:
        if 0 <= o < NUM_OPS:
            d[o] += 1.0
    total = sum(d)
    if total > 0:
        d = [x / total for x in d]
    return d


def _op_dist_distance(a_ops, b_ops):
    """Jensen-Shannon-like distance between operator distributions."""
    if not a_ops or not b_ops:
        return 1.0
    da = _op_distribution(a_ops)
    db = _op_distribution(b_ops)
    return sum(abs(a - b) for a, b in zip(da, db)) / 2.0


def _op_overlap(a_ops, b_ops):
    """Jaccard overlap of operator sets."""
    if not a_ops or not b_ops:
        return 0.0
    a_set, b_set = set(a_ops), set(b_ops)
    intersection = a_set & b_set
    union = a_set | b_set
    return len(intersection) / len(union) if union else 0.0


class BibleIndex:
    """Bible indexed by operator resonance. Every verse is a force vector.

    Usage:
        bible = BibleIndex()
        bible.load()
        results = bible.resonate("I am afraid of what comes next", top_k=5)
    """

    def __init__(self, bible_path=None, index_path=None):
        self._bible_path = bible_path or BIBLE_PATH
        self._index_path = index_path or INDEX_PATH
        self._verses: List[VerseVector] = []
        self._by_ref: Dict[str, VerseVector] = {}
        self._by_chapter: Dict[str, List[VerseVector]] = {}
        self._by_op: Dict[int, List[VerseVector]] = {i: [] for i in range(NUM_OPS)}
        self._by_book: Dict[str, List[VerseVector]] = {}
        self._ready = False

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def verse_count(self) -> int:
        return len(self._verses)

    def load(self) -> int:
        """Load pre-built index, or build from raw text if missing."""
        # Try primary index (matches the Bible text file we're using)
        if os.path.exists(self._index_path):
            return self._load_index(self._index_path)
        # Build from raw text (will create the index for next time)
        return self.build_index()

    def build_index(self) -> int:
        """Build force vector index from raw KJV text. Takes ~30-60s."""
        # Find Bible text
        path = self._bible_path
        if not os.path.exists(path):
            path = BIBLE_PATH_FALLBACK
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"KJV Bible not found. Place kjv.txt at:\n"
                f"  {self._bible_path}\n"
                f"  or {BIBLE_PATH_FALLBACK}\n"
                f"Format: one line per verse, tab-separated: 'Genesis 1:1\\tIn the beginning...'"
            )

        print(f"[Bible] Building index from {path}...")
        t0 = time.time()
        self._clear()

        with open(path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                ref, text = line.split('\t', 1)
                text = text.replace('[', '').replace(']', '')
                self._add_verse(ref, text)

        self._ready = True
        elapsed = time.time() - t0
        print(f"[Bible] Indexed {len(self._verses)} verses in {elapsed:.1f}s")

        # Save compressed index for fast reload
        self._save_index()
        return len(self._verses)

    def _add_verse(self, ref, text):
        force = text_to_force(text)
        ops = text_to_ops(text)
        dom = dominant_op(ops)
        coh = coherence(ops)

        vv = VerseVector(
            ref=ref, text=text, force=force,
            ops=ops, dominant_op=dom, coherence=coh,
        )
        self._verses.append(vv)
        self._by_ref[ref] = vv

        chapter = ref.rsplit(':', 1)[0]
        self._by_chapter.setdefault(chapter, []).append(vv)
        self._by_op[dom].append(vv)

        book = ref.split()[0]
        self._by_book.setdefault(book, []).append(vv)

    def _clear(self):
        self._verses.clear()
        self._by_ref.clear()
        self._by_chapter.clear()
        self._by_op = {i: [] for i in range(NUM_OPS)}
        self._by_book.clear()
        self._ready = False

    def _save_index(self):
        data = [{
            'r': v.ref, 't': v.text,
            'f': [round(x, 5) for x in v.force],
            'o': list(v.ops), 'd': v.dominant_op,
            'c': round(v.coherence, 4),
        } for v in self._verses]

        os.makedirs(os.path.dirname(self._index_path), exist_ok=True)
        with gzip.open(self._index_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f)
        print(f"[Bible] Saved index to {self._index_path}")

    def _load_index(self, path):
        print(f"[Bible] Loading index from {path}...")
        t0 = time.time()
        self._clear()

        with gzip.open(path, 'rt', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            vv = VerseVector(
                ref=item['r'], text=item['t'],
                force=tuple(item['f']), ops=tuple(item['o']),
                dominant_op=item['d'], coherence=item['c'],
            )
            self._verses.append(vv)
            self._by_ref[vv.ref] = vv
            chapter = vv.ref.rsplit(':', 1)[0]
            self._by_chapter.setdefault(chapter, []).append(vv)
            self._by_op[vv.dominant_op].append(vv)
            book = vv.ref.split()[0]
            self._by_book.setdefault(book, []).append(vv)

        self._ready = True
        elapsed = time.time() - t0
        print(f"[Bible] Loaded {len(self._verses)} verses in {elapsed:.1f}s")
        return len(self._verses)

    # ── Core: Resonance Search ────────────────────────────────────

    def resonate(self, query: str, top_k: int = 5,
                 op_weight: float = 0.35,
                 force_weight: float = 0.25,
                 coherence_weight: float = 0.15,
                 topic_weight: float = 0.25) -> List[ResonanceResult]:
        """Find verses by operator resonance + topic affinity.

        Primary: operator distribution match (algebra finds the shape)
        Secondary: topic keyword affinity (keeps verses relevant)
        Tertiary: force vector similarity + coherence bonus

        The algebra finds connections keywords can't.
        The keywords keep the conversation grounded.
        """
        if not self._ready:
            self.load()

        q_force = text_to_force(query)
        q_ops = text_to_ops(query)

        # Extract topic words from query (3+ letter words, lowered)
        q_words = set(
            w.lower() for w in query.split()
            if len(w) >= 3 and w.isalpha()
        )

        scored = []
        for v in self._verses:
            f_dist = force_distance(q_force, v.force)
            o_dist = _op_dist_distance(q_ops, v.ops)
            o_overlap = _op_overlap(q_ops, v.ops)
            f_sim = cosine_similarity(q_force, v.force)

            # Topic affinity: shared meaningful words
            topic_score = 0.0
            if q_words:
                v_words = set(
                    w.lower().strip('.,;:!?()[]') for w in v.text.split()
                    if len(w) >= 3
                )
                shared = q_words & v_words
                if shared:
                    topic_score = len(shared) / len(q_words)

            # Verse length bonus: prefer medium-length verses (not too short, not too long)
            word_count = len(v.text.split())
            length_penalty = 0.0
            if word_count < 8:
                length_penalty = 0.02  # Too short to be helpful
            elif word_count > 60:
                length_penalty = 0.01  # Very long can be overwhelming

            distance = (
                force_weight * f_dist +
                op_weight * o_dist -
                coherence_weight * v.coherence -
                topic_weight * topic_score +
                length_penalty
            )

            scored.append(ResonanceResult(
                verse=v, distance=distance,
                op_overlap=o_overlap, force_similarity=f_sim,
            ))

        scored.sort(key=lambda r: r.distance)

        # Deduplicate: remove verses from same chapter that are nearly identical
        seen_chapters = set()
        unique = []
        for r in scored:
            chapter = r.verse.ref.rsplit(':', 1)[0]
            if chapter not in seen_chapters:
                unique.append(r)
                seen_chapters.add(chapter)
            if len(unique) >= top_k:
                break

        return unique

    def resonate_by_op(self, operator: int, top_k: int = 10) -> List[VerseVector]:
        """Find verses dominated by a specific operator."""
        if not self._ready:
            self.load()
        candidates = self._by_op.get(operator, [])
        return sorted(candidates, key=lambda v: v.coherence, reverse=True)[:top_k]

    def cross_references(self, ref: str, top_k: int = 10) -> List[ResonanceResult]:
        """Find verses that compose to HARMONY with a given verse.

        These are the "arcs" — genuine algebraic connections.
        """
        if not self._ready:
            self.load()
        source = self._by_ref.get(ref)
        if not source:
            return []

        scored = []
        for v in self._verses:
            if v.ref == ref:
                continue
            # Score: how many operator pairs compose to HARMONY?
            harmony_count = 0
            pairs = 0
            for s_op in source.ops[:8]:
                for v_op in v.ops[:8]:
                    pairs += 1
                    if compose(s_op, v_op) == HARMONY:
                        harmony_count += 1
            if pairs == 0:
                continue
            harmony_score = harmony_count / pairs

            f_sim = cosine_similarity(source.force, v.force)
            o_overlap = _op_overlap(source.ops, v.ops)

            scored.append(ResonanceResult(
                verse=v,
                distance=1.0 - harmony_score,  # Lower = stronger connection
                op_overlap=o_overlap,
                force_similarity=f_sim,
            ))

        scored.sort(key=lambda r: r.distance)
        return scored[:top_k]

    def get_verse(self, ref: str) -> Optional[VerseVector]:
        if not self._ready:
            self.load()
        return self._by_ref.get(ref)

    def get_chapter(self, chapter: str) -> List[VerseVector]:
        if not self._ready:
            self.load()
        return self._by_chapter.get(chapter, [])

    def stats(self) -> dict:
        if not self._ready:
            return {'ready': False}
        op_counts = [0] * NUM_OPS
        for v in self._verses:
            op_counts[v.dominant_op] += 1
        total_coh = sum(v.coherence for v in self._verses)
        return {
            'ready': True,
            'verses': len(self._verses),
            'chapters': len(self._by_chapter),
            'books': len(self._by_book),
            'mean_coherence': round(total_coh / max(1, len(self._verses)), 4),
            'op_distribution': {
                OP_NAMES[i]: op_counts[i] for i in range(NUM_OPS)
            },
        }
