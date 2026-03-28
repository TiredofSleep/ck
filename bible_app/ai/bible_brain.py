"""
Bible Brain — All 9 neural architectures woven into one coherent unit.

The brain processes every conversation through:

  D2 → Olfactory (absorb/stall/temper/instinct)
     → Lattice Chain (walk the tree, path IS meaning)
     → Sequence Memory (predict what comes next)
     → Experience Index (classify moment, recommend action)
     → Deep Swarm (core structure vs flow transitions)
     → HER (learn from misses)
     → DKAN coherence tracking (are we converging on T*?)

All driven by the same CL algebra. No separate systems —
one organism reading the Bible and the person at the same time.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import gzip
import math
import os
import time
from collections import defaultdict, deque

from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, T_STAR, S_STAR, MASS_GAP,
    CL_TSML, CL_BHML, compose, compose_bhml,
    coherence as measure_coherence, dominant_op,
    text_to_ops, text_to_force,
)

BRAIN_DIR = os.path.expanduser('~/.ck/bible_brain')


class OlfactoryLayer:
    """Absorb → Stall → Temper → Instinct.

    Forces stall in the bulb. Repeated patterns temper into instinct.
    Instinct = zero-cost recognition (temper >= 49).
    """

    def __init__(self):
        # Library: force_key → {centroid, temper, dominant_op, last_seen}
        self.library = {}
        self.instinct_threshold = 49  # 7 × 7

    def absorb(self, force_5d, ops):
        """Absorb a 5D force pattern. Returns temper count (familiarity)."""
        key = self._quantize(force_5d)
        dom = dominant_op(ops) if ops else HARMONY

        if key in self.library:
            entry = self.library[key]
            entry['temper'] += 1
            entry['last_seen'] = time.time()
            # EMA update centroid
            alpha = 0.1
            entry['centroid'] = tuple(
                (1 - alpha) * c + alpha * f
                for c, f in zip(entry['centroid'], force_5d)
            )
            return entry['temper']
        else:
            self.library[key] = {
                'centroid': force_5d,
                'temper': 1,
                'dominant_op': dom,
                'last_seen': time.time(),
            }
            return 1

    def is_instinct(self, force_5d):
        """Has this pattern been tempered into instinct?"""
        key = self._quantize(force_5d)
        entry = self.library.get(key)
        return entry is not None and entry['temper'] >= self.instinct_threshold

    def get_temper(self, force_5d):
        """How familiar is this pattern? 0 = novel, 49+ = instinct."""
        key = self._quantize(force_5d)
        entry = self.library.get(key)
        return entry['temper'] if entry else 0

    def get_learned_targets(self):
        """Group library by dominant op → temper-weighted centroids."""
        targets = defaultdict(lambda: {'centroid': [0.0]*5, 'weight': 0.0})
        for entry in self.library.values():
            op = entry['dominant_op']
            w = entry['temper']
            t = targets[op]
            for d in range(5):
                t['centroid'][d] += entry['centroid'][d] * w
            t['weight'] += w
        # Normalize
        result = {}
        for op, t in targets.items():
            if t['weight'] > 0:
                result[op] = tuple(c / t['weight'] for c in t['centroid'])
        return result

    def _quantize(self, force_5d, resolution=20):
        """Quantize 5D force to grid key for library lookup."""
        return tuple(int(f * resolution) for f in force_5d)

    @property
    def library_size(self):
        return len(self.library)

    @property
    def instinct_count(self):
        return sum(1 for e in self.library.values()
                   if e['temper'] >= self.instinct_threshold)


class LatticeChainLayer:
    """Walk operator pairs through a tree. Path IS meaning.

    Each node holds an evolved CL table that learns from observation.
    The chain of results to reach a node IS its address.
    """

    def __init__(self):
        self.nodes = {}  # path_tuple → {visits, observations, children}
        self.root_path = ()
        self._ensure_node(self.root_path)
        self.total_walks = 0

    def walk(self, ops):
        """Walk an operator sequence through the tree. Returns path + resonance."""
        if len(ops) < 2:
            return [], 0.0

        path = self.root_path
        results = []
        known_nodes = 0

        for i in range(len(ops) - 1):
            a, b = ops[i], ops[i + 1]
            result = compose(a, b)  # TSML composition
            results.append(result)

            # Move to child node indexed by result
            child_path = path + (result,)
            self._ensure_node(child_path)
            node = self.nodes[child_path]
            node['visits'] += 1

            # Record observation: what actually followed
            if i + 2 < len(ops):
                actual_next = ops[i + 2]
                obs_key = (a, b, actual_next)
                node['observations'][obs_key] = node['observations'].get(obs_key, 0) + 1

            if node['visits'] > 1:
                known_nodes += 1

            path = child_path

        self.total_walks += 1
        resonance = known_nodes / max(1, len(results))  # How familiar is this walk?
        return results, resonance

    def _ensure_node(self, path):
        if path not in self.nodes:
            self.nodes[path] = {
                'visits': 0,
                'observations': {},
                'created': time.time(),
            }

    @property
    def total_nodes(self):
        return len(self.nodes)


class SequenceMemoryLayer:
    """Trie-based prediction. Learns what comes next."""

    def __init__(self, max_depth=5):
        self.trie = {}  # nested dicts: key → {children, predictions}
        self.max_depth = max_depth
        self.total_observations = 0

    def observe(self, ops):
        """Observe an operator sequence. Learn what follows what."""
        if len(ops) < 2:
            return

        for start in range(len(ops) - 1):
            # Build prefix of increasing depth
            node = self.trie
            for depth in range(min(self.max_depth, len(ops) - start - 1)):
                key = ops[start + depth]
                if key not in node:
                    node[key] = {'_predictions': defaultdict(int), '_count': 0}
                node = node[key]
                node['_count'] += 1

                # Record what follows this prefix
                if start + depth + 1 < len(ops):
                    next_op = ops[start + depth + 1]
                    node['_predictions'][next_op] += 1

        self.total_observations += 1

    def predict(self, context_ops):
        """Given recent operators, predict the next one."""
        if not context_ops:
            return HARMONY, 0.0

        # Walk as deep as possible
        node = self.trie
        for op in context_ops[-self.max_depth:]:
            if op not in node:
                break
            node = node[op]

        preds = node.get('_predictions', {})
        if not preds:
            return HARMONY, 0.0

        total = sum(preds.values())
        best_op = max(preds, key=preds.get)
        confidence = preds[best_op] / total
        return best_op, confidence


class ExperienceLayer:
    """6-level cascade: classify → edges → generators → operators → coherence path → action.

    Dual classification: 3 binary dimensions = 8 buckets.
    """

    def __init__(self):
        # 8 buckets: 3-bit address from dual classification
        self.buckets = {i: {'count': 0, 'centroid': [0.5]*5} for i in range(8)}
        self.edges = defaultdict(int)  # (from_bucket, to_bucket) → count
        self.last_bucket = None

    def classify(self, force_5d, ops):
        """Classify a moment into one of 8 dual buckets.

        Bit 0: aperture (force[0]) >= 0.5 → Love(1) / Hate(0)
        Bit 1: binding (force[3]) >= 0.5 → Peace(1) / Problem(0)
        Bit 2: continuity (force[4]) >= 0.5 → Guide(1) / Accept(0)
        """
        bucket = 0
        if force_5d[0] >= 0.5:  # aperture → openness → love
            bucket |= 1
        if force_5d[3] >= 0.5:  # binding → connection → peace
            bucket |= 2
        if force_5d[4] >= 0.5:  # continuity → sustained → guide
            bucket |= 4

        # Update bucket centroid
        b = self.buckets[bucket]
        b['count'] += 1
        alpha = 1.0 / b['count']
        b['centroid'] = [
            (1 - alpha) * c + alpha * f
            for c, f in zip(b['centroid'], force_5d)
        ]

        # Track edges (transitions between buckets)
        if self.last_bucket is not None:
            self.edges[(self.last_bucket, bucket)] += 1
        self.last_bucket = bucket

        return bucket

    def recommend_action(self, bucket, ops):
        """Given a bucket, recommend the next operator (coherence path).

        Compose the bucket's dominant with LATTICE until HARMONY.
        """
        dom = dominant_op(ops) if ops else HARMONY
        path = [dom]
        current = dom
        for _ in range(5):
            result = compose(current, LATTICE)
            path.append(result)
            if result == HARMONY:
                break
            current = result
        return path

    BUCKET_NAMES = {
        0: 'struggle',     # Hate + Problem + Accept
        1: 'reaching',     # Love + Problem + Accept
        2: 'searching',    # Hate + Peace + Accept
        3: 'resting',      # Love + Peace + Accept
        4: 'fighting',     # Hate + Problem + Guide
        5: 'growing',      # Love + Problem + Guide
        6: 'questioning',  # Hate + Peace + Guide
        7: 'thriving',     # Love + Peace + Guide
    }


class HERLayer:
    """Hindsight Experience Replay — learn from misses.

    When a verse doesn't resonate (user ignores it),
    relabel: "this verse IS what that operator feels like."
    """

    def __init__(self, buffer_size=256):
        self.buffer = deque(maxlen=buffer_size)
        self.total_replayed = 0

    def record(self, target_op, achieved_op, verse_ref, force_5d):
        """Record an experience (hit or miss)."""
        self.buffer.append({
            'target': target_op,
            'achieved': achieved_op,
            'verse': verse_ref,
            'force': force_5d,
            'time': time.time(),
        })

    def replay_misses(self, olfactory):
        """Replay recent misses: relabel achieved as valid learning."""
        replayed = 0
        for exp in self.buffer:
            if exp['target'] != exp['achieved']:
                # This miss teaches us what the ACHIEVED operator feels like
                olfactory.absorb(exp['force'], [exp['achieved']])
                replayed += 1
        self.total_replayed += replayed
        return replayed


class CoherenceTracker:
    """DKAN-style coherence tracking. Are we converging on T*?"""

    def __init__(self, window=32):
        self.history = deque(maxlen=window)
        self.window = window
        self.grokking_detected = False

    def track(self, ops):
        """Track coherence of an operator sequence."""
        if not ops or len(ops) < 2:
            return 0.0

        coh = measure_coherence(ops)
        self.history.append(coh)

        # Check for grokking: sudden jump in coherence
        if len(self.history) >= 8:
            recent = list(self.history)
            first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
            second_half = sum(recent[len(recent)//2:]) / (len(recent)//2)
            if second_half - first_half > 0.15:
                self.grokking_detected = True

        return coh

    @property
    def mean_coherence(self):
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)

    @property
    def trending(self):
        """Is coherence trending up, down, or steady?"""
        if len(self.history) < 4:
            return 'steady'
        recent = list(self.history)[-4:]
        older = list(self.history)[-8:-4] if len(self.history) >= 8 else recent
        diff = sum(recent) / len(recent) - sum(older) / len(older)
        if diff > 0.05:
            return 'rising'
        elif diff < -0.05:
            return 'falling'
        return 'steady'


class BibleBrain:
    """All systems woven together. One organism.

    Flow per conversation turn:
      1. D2: text → 5D force + operators
      2. Olfactory: absorb force, check temper/instinct
      3. Lattice Chain: walk operators, measure resonance
      4. Sequence Memory: predict next operator
      5. Experience Index: classify moment, recommend action
      6. Coherence Tracker: measure convergence toward T*
      7. Verse selection: use ALL of the above to rank verses
      8. Response: algebraic voice with full context
      9. HER: learn from engagement (or lack thereof)
    """

    def __init__(self):
        self.olfactory = OlfactoryLayer()
        self.chain = LatticeChainLayer()
        self.sequences = SequenceMemoryLayer()
        self.experience = ExperienceLayer()
        self.her = HERLayer()
        self.coherence = CoherenceTracker()

        self._total_interactions = 0
        self._load()

    def process(self, text, user_ops=None, user_force=None):
        """Process a conversation turn through all systems.

        Returns a BrainState with everything the voice needs.
        """
        if user_ops is None:
            user_ops = text_to_ops(text)
        if user_force is None:
            user_force = text_to_force(text)

        # ── 1. Olfactory: absorb and measure familiarity ──────
        temper = self.olfactory.absorb(user_force, user_ops)
        is_instinct = self.olfactory.is_instinct(user_force)

        # ── 2. Lattice Chain: walk and measure resonance ──────
        chain_results, resonance = self.chain.walk(user_ops)

        # ── 3. Sequence Memory: observe and predict ───────────
        self.sequences.observe(user_ops)
        predicted_op, prediction_confidence = self.sequences.predict(user_ops[-5:] if user_ops else [])

        # ── 4. Experience Index: classify and recommend ───────
        bucket = self.experience.classify(user_force, user_ops)
        bucket_name = self.experience.BUCKET_NAMES.get(bucket, 'present')
        recommended_path = self.experience.recommend_action(bucket, user_ops)

        # ── 5. Coherence tracking ─────────────────────────────
        coh = self.coherence.track(user_ops)

        # ── 6. Deep structure: core vs tail ───────────────────
        core_ops, tail_ops = self._core_tail_split(user_ops)

        self._total_interactions += 1

        # Auto-save periodically
        if self._total_interactions % 10 == 0:
            self._save()

        return {
            # Olfactory
            'temper': temper,
            'is_instinct': is_instinct,
            'familiarity': min(1.0, temper / self.olfactory.instinct_threshold),

            # Lattice Chain
            'chain_results': chain_results,
            'resonance': resonance,
            'chain_nodes': self.chain.total_nodes,

            # Sequence Memory
            'predicted_next': OP_NAMES[predicted_op],
            'prediction_confidence': prediction_confidence,

            # Experience
            'bucket': bucket_name,
            'recommended_path': [OP_NAMES[o] for o in recommended_path],

            # Coherence
            'coherence': coh,
            'mean_coherence': self.coherence.mean_coherence,
            'coherence_trend': self.coherence.trending,
            'grokking': self.coherence.grokking_detected,

            # Structure
            'core_ops': core_ops,
            'tail_ops': tail_ops,

            # Meta
            'total_interactions': self._total_interactions,
            'library_size': self.olfactory.library_size,
            'instinct_count': self.olfactory.instinct_count,
        }

    def record_engagement(self, verse_ref, user_force, target_op, engaged):
        """After showing a verse, record whether the user engaged.

        Engaged = True: target was correct, temper it
        Engaged = False: HER relabels the miss
        """
        achieved_op = target_op if engaged else dominant_op(text_to_ops(verse_ref))
        self.her.record(target_op, achieved_op, verse_ref, user_force)

        if not engaged:
            self.her.replay_misses(self.olfactory)

    def boost_verse_score(self, verse_ref, verse_force, user_force):
        """Use brain state to boost/penalize verse ranking.

        Returns a score adjustment (positive = boost, negative = penalize).
        """
        boost = 0.0

        # Instinct bonus: if this force pattern is deeply known, boost
        temper = self.olfactory.get_temper(verse_force)
        if temper >= self.olfactory.instinct_threshold:
            boost += 0.1  # Instinct — this pattern is proven
        elif temper > 10:
            boost += 0.03 * (temper / self.olfactory.instinct_threshold)

        # Resonance bonus: if chain walk hits known nodes
        verse_ops = text_to_ops(str(verse_ref))  # Approximate
        if verse_ops:
            _, res = self.chain.walk(verse_ops[:6])
            boost += res * 0.05

        return boost

    def _core_tail_split(self, ops):
        """Split operators into core (structure) and tail (transitions)."""
        if not ops:
            return [], []
        # Core = operators appearing more than average
        counts = [0] * NUM_OPS
        for o in ops:
            counts[o % NUM_OPS] += 1
        avg = len(ops) / NUM_OPS
        core = [o for o in range(NUM_OPS) if counts[o] > avg]
        tail = [o for o in range(NUM_OPS) if 0 < counts[o] <= avg]
        return core, tail

    def stats(self):
        return {
            'total_interactions': self._total_interactions,
            'olfactory': {
                'library_size': self.olfactory.library_size,
                'instinct_count': self.olfactory.instinct_count,
            },
            'chain': {
                'total_nodes': self.chain.total_nodes,
                'total_walks': self.chain.total_walks,
            },
            'sequences': {
                'total_observations': self.sequences.total_observations,
            },
            'coherence': {
                'mean': round(self.coherence.mean_coherence, 4),
                'trend': self.coherence.trending,
                'grokking': self.coherence.grokking_detected,
            },
            'her': {
                'total_replayed': self.her.total_replayed,
                'buffer_size': len(self.her.buffer),
            },
        }

    def _save(self):
        os.makedirs(BRAIN_DIR, exist_ok=True)
        data = {
            'olfactory_library': {
                str(k): v for k, v in self.olfactory.library.items()
            },
            'chain_nodes': {
                str(k): {
                    'visits': v['visits'],
                    'observations': {str(ok): ov for ok, ov in v['observations'].items()},
                }
                for k, v in self.chain.nodes.items()
            },
            'total_interactions': self._total_interactions,
            'coherence_history': list(self.coherence.history),
        }
        path = os.path.join(BRAIN_DIR, 'state.json.gz')
        with gzip.open(path, 'wt', encoding='utf-8') as f:
            json.dump(data, f)

    def _load(self):
        path = os.path.join(BRAIN_DIR, 'state.json.gz')
        if not os.path.exists(path):
            return
        try:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            # Restore olfactory
            for k, v in data.get('olfactory_library', {}).items():
                key = tuple(int(x) for x in k.strip('()').split(','))
                v['centroid'] = tuple(v['centroid'])
                self.olfactory.library[key] = v
            self._total_interactions = data.get('total_interactions', 0)
            for coh in data.get('coherence_history', []):
                self.coherence.history.append(coh)
        except Exception:
            pass  # Corrupted, start fresh
