"""
Bible Study Net — The neural net studies the Bible using CK's algebra.

Before talking to anyone, the net reads every verse, composes every
pair through CL tables, detects theological chains, and builds a
verse-to-verse resonance graph. It KNOWS the Bible through math.

This runs at build time (once, ~5 min). The learned graph persists.
At runtime, queries hit the pre-computed graph instantly.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import gzip
import json
import math
import os
import random
import time
from collections import defaultdict

from bible_app.algebra import (
    NUM_OPS, HARMONY, VOID, BREATH, COLLAPSE, PROGRESS, LATTICE,
    RESET, COUNTER, BALANCE, CHAOS,
    OP_NAMES, T_STAR, compose, coherence, dominant_op,
    text_to_ops, text_to_force, cosine_similarity, force_distance,
)
from bible_app.voice.bible_lattice import MACRO_CHAINS, detect_macro_chains

STUDY_DIR = os.path.expanduser('~/.ck/bible_study')
GRAPH_PATH = os.path.join(STUDY_DIR, 'verse_graph.json.gz')


class BibleStudyNet:
    """Neural net that has STUDIED the Bible through algebra.

    After study(), it knows:
      - verse_clusters: {corridor: [verse_refs]} — which verses live where
      - verse_connections: {ref: [(ref, harmony_score)]} — algebraic cross-refs
      - macro_index: {chain_name: [verse_refs]} — theological concepts found
      - corridor_exemplars: {corridor: [best_verse_refs]} — strongest examples
      - operator_index: {op: [verse_refs]} — verses by dominant operator
      - topic_index: {word: [verse_refs]} — keyword → verse lookup
    """

    def __init__(self):
        self.verse_clusters = defaultdict(list)
        self.verse_connections = defaultdict(list)
        self.macro_index = defaultdict(list)
        self.corridor_exemplars = defaultdict(list)
        self.operator_index = defaultdict(list)
        self.topic_index = defaultdict(list)
        self._studied = False
        self._verse_count = 0

    @property
    def studied(self):
        return self._studied

    def study(self, bible_index):
        """Study the entire Bible through algebraic analysis.

        This is the heavy lift — runs once, results persist.
        Takes ~2-5 minutes on first run.
        """
        if not bible_index.ready:
            bible_index.load()

        # Try loading pre-computed study
        if self._load():
            print(f"[Study] Loaded pre-computed study ({self._verse_count} verses)")
            return

        print(f"[Study] Studying {bible_index.verse_count} verses through algebra...")
        t0 = time.time()

        verses = bible_index._verses
        self._verse_count = len(verses)

        # ── Phase 1: Classify every verse by corridor ─────────────
        print("[Study] Phase 1: Corridor classification...")
        from bible_app.algebra.corridor import classify_corridor
        for v in verses:
            corridor = classify_corridor(v.ops, text=v.text)
            self.verse_clusters[corridor].append(v.ref)

        # ── Phase 2: Index by dominant operator ───────────────────
        print("[Study] Phase 2: Operator indexing...")
        for v in verses:
            self.operator_index[v.dominant_op].append(v.ref)

        # ── Phase 3: Detect macro chains (theological concepts) ───
        print("[Study] Phase 3: Theological chain detection...")
        for v in verses:
            if len(v.ops) >= 3:
                chains = detect_macro_chains(v.ops)
                for chain in chains:
                    self.macro_index[chain].append(v.ref)

        # ── Phase 4: Build topic index (common Biblical keywords) ─
        print("[Study] Phase 4: Topic indexing...")
        important_words = {
            'god', 'lord', 'jesus', 'christ', 'spirit', 'holy',
            'love', 'faith', 'hope', 'grace', 'mercy', 'peace',
            'sin', 'salvation', 'forgiveness', 'redemption',
            'prayer', 'praise', 'worship', 'glory',
            'fear', 'trust', 'believe', 'truth', 'light', 'life',
            'death', 'heaven', 'hell', 'eternal', 'kingdom',
            'heart', 'soul', 'mind', 'strength',
            'father', 'son', 'shepherd', 'lamb', 'bread', 'water',
            'joy', 'comfort', 'healing', 'wisdom', 'righteous',
            'covenant', 'promise', 'blessing', 'cursing',
            'cross', 'blood', 'sacrifice', 'temple', 'altar',
            'angel', 'devil', 'satan', 'demon',
            'Moses', 'David', 'Abraham', 'Paul', 'Peter',
            'prophet', 'apostle', 'church', 'Israel',
            'suffer', 'suffering', 'affliction', 'tribulation',
            'forgive', 'repent', 'baptize', 'baptism',
        }
        for v in verses:
            words = set(w.lower().strip('.,;:!?()[]') for w in v.text.split())
            for w in words & important_words:
                self.topic_index[w].append(v.ref)

        # ── Phase 4b: Detect repetition in verses ────────────────
        # Verses that contain repeated words/phrases ARE the answer
        # to "why is the Bible repetitive"
        print("[Study] Phase 4b: Detecting repetition patterns...")
        for v in verses:
            words_list = [w.lower().strip('.,;:!?()[]') for w in v.text.split()
                          if len(w) >= 3]
            # Find words repeated 2+ times in the same verse
            word_counts = defaultdict(int)
            for w in words_list:
                word_counts[w] += 1
            repeated = [w for w, c in word_counts.items() if c >= 2 and len(w) >= 4]
            if repeated:
                self.topic_index['repetitive'].append(v.ref)
                self.topic_index['repetition'].append(v.ref)
                self.topic_index['repeat'].append(v.ref)
                self.topic_index['pattern'].append(v.ref)

        # ── Phase 4c: Meta-question verse index ──────────────────
        # Special verses that answer questions ABOUT the Bible
        meta_verses = {
            # Why repetition? Because emphasis = holiness
            'repetitive': [
                'Isaiah 6:3',       # "Holy, holy, holy"
                'Revelation 4:8',   # "Holy, holy, holy, Lord God"
                'Psalm 136:1',      # "for his mercy is for ever" (26x repeated)
                'Isaiah 40:1',      # "Give comfort, give comfort"
                'Psalm 118:1',      # "his mercy is for ever"
                'Psalm 107:1',      # "his mercy is for ever"
                'Psalm 150:1',      # "Praise God" (13x in 6 verses)
            ],
            # Why contradictions?
            'contradiction': [
                'Proverbs 26:4',    # "Do not answer a fool" vs next verse
                'Proverbs 26:5',    # "Answer a fool" — the paradox IS the point
                'Ecclesiastes 3:1', # "a time for every purpose"
            ],
            # How was it written/inspired?
            'inspired': [
                '2 Timothy 3:16',   # "All scripture is inspired by God"
                '2 Peter 1:21',     # "men moved by the Holy Spirit"
                'Hebrews 4:12',     # "the word of God is living and active"
            ],
        }
        for topic, refs in meta_verses.items():
            for ref in refs:
                if ref not in self.topic_index.get(topic, []):
                    self.topic_index[topic].insert(0, ref)  # Priority position

        # ── Phase 5: Find corridor exemplars (highest coherence) ──
        print("[Study] Phase 5: Finding corridor exemplars...")
        from bible_app.algebra.corridor import classify_corridor
        corridor_scores = defaultdict(list)
        for v in verses:
            corridor = classify_corridor(v.ops, text=v.text)
            corridor_scores[corridor].append((v.coherence, v.ref))
        for corridor, scored in corridor_scores.items():
            scored.sort(reverse=True)
            self.corridor_exemplars[corridor] = [ref for _, ref in scored[:50]]

        # ── Phase 6: Algebraic cross-references (sampled) ─────────
        # Full N^2 is too expensive (31K^2 = ~1B pairs).
        # Sample: for each verse, compare against 200 random + all
        # verses with matching dominant operator.
        print("[Study] Phase 6: Algebraic cross-references (sampled)...")
        rng = random.Random(42)
        ref_to_verse = {v.ref: v for v in verses}

        for i, v in enumerate(verses):
            if i % 5000 == 0:
                elapsed = time.time() - t0
                print(f"  [{i}/{len(verses)}] {elapsed:.0f}s elapsed...")

            # Compare against: same-operator verses + random sample
            candidates = set()
            # Same dominant operator (max 50)
            same_op = self.operator_index.get(v.dominant_op, [])
            for ref in same_op[:50]:
                if ref != v.ref:
                    candidates.add(ref)
            # Random sample (100)
            sample = rng.sample(range(len(verses)), min(100, len(verses)))
            for j in sample:
                if verses[j].ref != v.ref:
                    candidates.add(verses[j].ref)

            best = []
            for cand_ref in candidates:
                cand = ref_to_verse.get(cand_ref)
                if not cand:
                    continue

                # CL harmony score: compose dominant operators
                h_score = 1.0 if compose(v.dominant_op, cand.dominant_op) == HARMONY else 0.0

                # Force similarity
                f_sim = cosine_similarity(v.force, cand.force)

                # Combined score
                score = 0.5 * h_score + 0.3 * f_sim + 0.2 * cand.coherence

                if score > 0.5:
                    best.append((score, cand_ref))

            best.sort(reverse=True)
            self.verse_connections[v.ref] = [
                (ref, round(s, 3)) for s, ref in best[:10]
            ]

        elapsed = time.time() - t0
        self._studied = True
        print(f"[Study] Complete in {elapsed:.0f}s")
        print(f"  Corridors: {dict((k, len(v)) for k, v in self.verse_clusters.items())}")
        print(f"  Macro chains found: {dict((k, len(v)) for k, v in self.macro_index.items())}")
        print(f"  Topics indexed: {len(self.topic_index)}")
        print(f"  Cross-references: {sum(len(v) for v in self.verse_connections.values())}")

        self._save()

    def get_verses_for_topic(self, topic, max_k=20):
        """Get verses related to a topic keyword."""
        topic = topic.lower().strip()
        refs = self.topic_index.get(topic, [])
        return refs[:max_k]

    def get_verses_for_corridor(self, corridor, max_k=10):
        """Get the best exemplar verses for a corridor."""
        return self.corridor_exemplars.get(corridor, [])[:max_k]

    def get_cross_refs(self, verse_ref, max_k=5):
        """Get algebraic cross-references for a verse."""
        return self.verse_connections.get(verse_ref, [])[:max_k]

    def get_macro_verses(self, chain_name, max_k=10):
        """Get verses containing a theological macro chain."""
        return self.macro_index.get(chain_name, [])[:max_k]

    def find_relevant_verses(self, user_ops, corridor, intent, text='', max_k=10):
        """Use ALL knowledge to find the most relevant verses.

        Combines: topic index + corridor exemplars + operator match +
        macro chain detection + cross-reference graph.
        """
        candidates = defaultdict(float)  # {ref: cumulative_score}

        # 1. Topic keyword matches (strongest signal for relevance)
        if text:
            words = set(w.lower().strip('.,;:!?()[]') for w in text.split()
                       if len(w) >= 3)
            for word in words:
                for ref in self.topic_index.get(word, [])[:30]:
                    candidates[ref] += 2.0

        # 2. Corridor exemplars (what's worked for this emotional state)
        for ref in self.get_verses_for_corridor(corridor, 20):
            candidates[ref] += 1.0

        # 3. Operator match (same dominant operator)
        dom = dominant_op(user_ops) if user_ops else HARMONY
        for ref in self.operator_index.get(dom, [])[:30]:
            candidates[ref] += 0.5

        # 4. Macro chain detection
        if user_ops and len(user_ops) >= 3:
            chains = detect_macro_chains(user_ops)
            for chain in chains:
                for ref in self.macro_index.get(chain, [])[:10]:
                    candidates[ref] += 1.5

        # Sort by cumulative score
        ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)

        # Deduplicate by chapter
        seen_chapters = set()
        result = []
        for ref, score in ranked:
            chapter = ref.rsplit(':', 1)[0]
            if chapter not in seen_chapters:
                result.append(ref)
                seen_chapters.add(chapter)
            if len(result) >= max_k:
                break

        return result

    def stats(self):
        return {
            'studied': self._studied,
            'verses': self._verse_count,
            'corridors': {k: len(v) for k, v in self.verse_clusters.items()},
            'macro_chains': {k: len(v) for k, v in self.macro_index.items()},
            'topics': len(self.topic_index),
            'cross_refs': sum(len(v) for v in self.verse_connections.values()),
        }

    def _save(self):
        os.makedirs(STUDY_DIR, exist_ok=True)
        data = {
            'verse_clusters': dict(self.verse_clusters),
            'verse_connections': dict(self.verse_connections),
            'macro_index': dict(self.macro_index),
            'corridor_exemplars': dict(self.corridor_exemplars),
            'operator_index': {str(k): v for k, v in self.operator_index.items()},
            'topic_index': dict(self.topic_index),
            'verse_count': self._verse_count,
        }
        with gzip.open(GRAPH_PATH, 'wt', encoding='utf-8') as f:
            json.dump(data, f)
        print(f"[Study] Saved to {GRAPH_PATH}")

    def _load(self):
        if not os.path.exists(GRAPH_PATH):
            return False
        try:
            with gzip.open(GRAPH_PATH, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            self.verse_clusters = defaultdict(list, data.get('verse_clusters', {}))
            self.verse_connections = defaultdict(list, data.get('verse_connections', {}))
            self.macro_index = defaultdict(list, data.get('macro_index', {}))
            self.corridor_exemplars = defaultdict(list, data.get('corridor_exemplars', {}))
            self.operator_index = defaultdict(list, {
                int(k): v for k, v in data.get('operator_index', {}).items()
            })
            self.topic_index = defaultdict(list, data.get('topic_index', {}))
            self._verse_count = data.get('verse_count', 0)
            self._studied = True
            return True
        except Exception:
            return False
