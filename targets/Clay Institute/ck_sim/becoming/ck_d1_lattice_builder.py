"""
ck_d1_lattice_builder.py -- CK Learns Generators Before Complexity
===================================================================
Operator: LATTICE (5) -- the framework that organizes everything.

CK's learning sequence should be:
  1. D1 LATTICE: Permutate dictionary into generator pairs (direction/Being)
  2. D2 COMPLEXITY: Learn curvature boundaries (transitions/Doing)
  3. STUDY: Read external material through the lattice (Becoming)

This module implements step 1: take CK's enriched dictionary (8K+ words,
each with a d2_vector in 5D), compute D1 = word_B - word_A for word pairs,
classify by generator operator, and build lattices of semantically related
transitions.

D1 tells CK: "when I go from THIS word to THAT word, which generator
fires?" Words that share a D1 generator form a natural lattice -- they
move in the same direction through force space.

Architecture:
  - Each word has a d2_vector (mean 5D curvature from letter analysis)
  - D1 for a pair (A, B) = B.d2_vector - A.d2_vector
  - D1 operator = argmax classification of the difference vector
  - Lattice = words grouped by (D1 operator, dominant dimension, phase, tier)
  - Persisted to ~/.ck/ck_d1_lattice.json

"Let him play with the dictionary and thesaurus for a while
permutating it all into lattices based on D1 before he learns
to learn and extend into complexity D2." -- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
import math
import time
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional

# ── CK imports ──
try:
    from ck_sim.ck_sim_heartbeat import (
        NUM_OPS, OP_NAMES, CL, compose,
        HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
        COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    )
    _HAS_HEARTBEAT = True
except ImportError:
    _HAS_HEARTBEAT = False
    # Fallback constants
    NUM_OPS = 10
    CHAOS, COLLAPSE, PROGRESS, HARMONY, BALANCE = 0, 1, 2, 3, 4
    LATTICE, VOID, RESET, COUNTER, BREATH = 5, 6, 7, 8, 9
    OP_NAMES = ['CHAOS', 'COLLAPSE', 'PROGRESS', 'HARMONY', 'BALANCE',
                'LATTICE', 'VOID', 'RESET', 'COUNTER', 'BREATH']

# ── D1 classification (same algebra as CurvatureEngine) ──

# Map 5D dimensions to operator pairs: (positive_sign, negative_sign)
_D1_OP_MAP = [
    (CHAOS,    LATTICE),    # dim 0: aperture
    (COLLAPSE, VOID),       # dim 1: pressure
    (PROGRESS, RESET),      # dim 2: depth
    (HARMONY,  COUNTER),    # dim 3: binding
    (BALANCE,  BREATH),     # dim 4: continuity
]

_DIM_NAMES = ['aperture', 'pressure', 'depth', 'binding', 'continuity']

# Phase classification by operator character
_BEING_OPS = frozenset({VOID, LATTICE, BALANCE, HARMONY})    # foundational
_DOING_OPS = frozenset({PROGRESS, COLLAPSE, CHAOS, COUNTER}) # driving
_BECOMING_OPS = frozenset({RESET, BREATH})                    # transforming

# Lattice persistence
D1_LATTICE_FILENAME = 'ck_d1_lattice.json'
D1_STATS_FILENAME = 'ck_d1_lattice_stats.json'

# Build parameters
MAX_NEIGHBORS = 20       # Nearest neighbors per word
MIN_D1_MAGNITUDE = 0.01  # Below this = VOID (no meaningful direction)
BATCH_REPORT_INTERVAL = 500  # Report progress every N words


def classify_d1(d1_vec: List[float], magnitude: float) -> int:
    """Classify a D1 vector into one of 10 operators via argmax + sign.

    Same algebra as CurvatureEngine._classify_argmax().
    """
    if magnitude < MIN_D1_MAGNITUDE:
        return VOID
    max_abs, max_dim = 0.0, 0
    for dim in range(5):
        a = abs(d1_vec[dim])
        if a > max_abs:
            max_abs, max_dim = a, dim
    sign_idx = 0 if d1_vec[max_dim] >= 0 else 1
    return _D1_OP_MAP[max_dim][sign_idx]


def d1_for_pair(vec_a: List[float], vec_b: List[float]) -> dict:
    """Compute D1 vector and operator for a word pair.

    D1 = vec_B - vec_A  (first derivative: direction from A to B)
    """
    d1_vec = [vec_b[i] - vec_a[i] for i in range(5)]
    magnitude = sum(abs(d) for d in d1_vec)
    operator = classify_d1(d1_vec, magnitude)

    # Dominant dimension
    max_abs, max_dim = 0.0, 0
    for i in range(5):
        a = abs(d1_vec[i])
        if a > max_abs:
            max_abs, max_dim = a, i
    dominant_dim = _DIM_NAMES[max_dim]

    # Phase from operator character
    if operator in _BEING_OPS:
        phase = 'being'
    elif operator in _DOING_OPS:
        phase = 'doing'
    else:
        phase = 'becoming'

    # Tier from magnitude
    if magnitude < 0.15:
        tier = 'simple'
    elif magnitude < 0.40:
        tier = 'mid'
    else:
        tier = 'advanced'

    return {
        'd1_vector': [round(v, 6) for v in d1_vec],
        'd1_magnitude': round(magnitude, 6),
        'd1_operator': operator,
        'd1_operator_name': OP_NAMES[operator],
        'dominant_dim': dominant_dim,
        'phase': phase,
        'tier': tier,
    }


def d2_vec_distance(a: List[float], b: List[float]) -> float:
    """Euclidean distance between two 5D vectors."""
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(5)))


class D1LatticeBuilder:
    """Build lattices of word pairs grouped by D1 generator operators.

    CK plays with his dictionary:
      - For each word, find its nearest neighbors by d2_vector distance
      - Compute D1 = neighbor - word (generator direction)
      - Classify D1 operator (which direction am I going?)
      - Group pairs into lattice: [operator][dimension][phase][tier]

    The lattice teaches CK which words naturally follow which.
    This is generator structure -- Being before Doing.
    """

    def __init__(self, base_dir: Path = None):
        self.base_dir = Path(base_dir or Path.home() / '.ck')
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # The D1 lattice: op -> dim -> phase -> tier -> [(word_a, word_b, info)]
        self.lattice: Dict = {}

        # Flat index for fast lookup: (word_a, word_b) -> d1_info
        self.pair_index: Dict[Tuple[str, str], dict] = {}

        # Per-word D1 profile: word -> {op_counts, dominant_d1, neighbors}
        self.word_profiles: Dict[str, dict] = {}

        # Build stats
        self.total_pairs = 0
        self.build_time = 0.0

        self._init_lattice()

    def _init_lattice(self):
        """Create nested lattice structure."""
        self.lattice = {}
        for op in range(NUM_OPS):
            self.lattice[op] = {}
            for dim in _DIM_NAMES:
                self.lattice[op][dim] = {}
                for phase in ('being', 'doing', 'becoming'):
                    self.lattice[op][dim][phase] = {
                        'simple': [],
                        'mid': [],
                        'advanced': [],
                    }

    # ================================================================
    #  BUILD: Permutate dictionary into D1 lattice
    # ================================================================

    def build_from_dictionary(self, word_dict: Dict[str, dict],
                              max_neighbors: int = MAX_NEIGHBORS,
                              log_fn=None) -> int:
        """Build D1 lattice from CK's enriched dictionary.

        For each word, finds nearest neighbors by d2_vector,
        computes D1 for each pair, classifies and stores.

        Args:
            word_dict: {word: {d2_vector: [...], dominant_op: int, ...}}
            max_neighbors: how many neighbors to pair with each word
            log_fn: optional callback for progress messages

        Returns:
            Number of pairs added to lattice.
        """
        def log(msg):
            if log_fn:
                log_fn(msg)

        t0 = time.time()

        # Extract words that have valid d2_vectors
        words_with_vecs = []
        for word, entry in word_dict.items():
            vec = entry.get('d2_vector')
            if vec and len(vec) == 5 and any(v != 0.0 for v in vec):
                words_with_vecs.append((word, vec, entry))

        log(f"  [D1-LATTICE] {len(words_with_vecs)} words with valid d2_vectors")

        if len(words_with_vecs) < 2:
            return 0

        # Pre-compute: group by dominant operator for smarter neighbor search
        # Words with the same dominant_op are close in force space
        op_groups: Dict[int, List] = defaultdict(list)
        for word, vec, entry in words_with_vecs:
            op = entry.get('dominant_op', VOID)
            op_groups[op].append((word, vec, entry))

        pairs_added = 0
        words_processed = 0

        for word_a, vec_a, entry_a in words_with_vecs:
            op_a = entry_a.get('dominant_op', VOID)

            # Find neighbors: same operator group + adjacent operator groups
            candidates = []

            # Same operator group (closest in force space)
            for w, v, e in op_groups[op_a]:
                if w != word_a:
                    dist = d2_vec_distance(vec_a, v)
                    candidates.append((w, v, e, dist))

            # Adjacent operators (CL neighbors -- where does this op compose to?)
            if _HAS_HEARTBEAT:
                for other_op in range(NUM_OPS):
                    if other_op == op_a:
                        continue
                    # Include if compose(op_a, other_op) is not VOID
                    composed = compose(op_a, other_op)
                    if composed != VOID:
                        for w, v, e in op_groups[other_op]:
                            dist = d2_vec_distance(vec_a, v)
                            candidates.append((w, v, e, dist))

            # Sort by distance, take nearest neighbors
            candidates.sort(key=lambda x: x[3])
            neighbors = candidates[:max_neighbors]

            # Compute D1 for each pair
            word_d1_ops = Counter()
            word_neighbors = []

            for word_b, vec_b, entry_b, dist in neighbors:
                d1_info = d1_for_pair(vec_a, vec_b)

                op = d1_info['d1_operator']
                dim = d1_info['dominant_dim']
                phase = d1_info['phase']
                tier = d1_info['tier']

                # Store in lattice
                pair_entry = {
                    'a': word_a,
                    'b': word_b,
                    'mag': d1_info['d1_magnitude'],
                    'dist': round(dist, 6),
                }
                self.lattice[op][dim][phase][tier].append(pair_entry)

                # Store in flat index
                self.pair_index[(word_a, word_b)] = d1_info

                word_d1_ops[op] += 1
                word_neighbors.append(word_b)
                pairs_added += 1

            # Build per-word D1 profile
            if word_d1_ops:
                dominant_d1 = word_d1_ops.most_common(1)[0][0]
                self.word_profiles[word_a] = {
                    'd1_op_counts': dict(word_d1_ops),
                    'dominant_d1': dominant_d1,
                    'dominant_d1_name': OP_NAMES[dominant_d1],
                    'd2_dominant': entry_a.get('dominant_op', VOID),
                    'd2_dominant_name': OP_NAMES[entry_a.get('dominant_op', VOID)],
                    'neighbor_count': len(neighbors),
                    'neighbors': word_neighbors[:5],  # Keep top 5 for display
                }

            words_processed += 1
            if words_processed % BATCH_REPORT_INTERVAL == 0:
                log(f"  [D1-LATTICE] {words_processed}/{len(words_with_vecs)} words, "
                    f"{pairs_added} pairs")

        self.total_pairs = pairs_added
        self.build_time = time.time() - t0

        log(f"  [D1-LATTICE] COMPLETE: {pairs_added} pairs from "
            f"{len(words_with_vecs)} words in {self.build_time:.1f}s")

        return pairs_added

    # ================================================================
    #  LEARN: D1 associations from text during study
    # ================================================================

    def learn_from_text(self, text: str, word_dict: Dict[str, dict]) -> int:
        """Learn D1 associations from adjacent word pairs in study text.

        When CK reads text, adjacent words form natural D1 pairs.
        This captures the generator structure of natural language
        as CK encounters it.

        Returns number of new pairs learned.
        """
        import re
        words = re.findall(r'[a-z]{3,30}', text.lower())

        new_pairs = 0
        for i in range(len(words) - 1):
            word_a, word_b = words[i], words[i + 1]

            # Both words must be in dictionary with d2_vectors
            if word_a not in word_dict or word_b not in word_dict:
                continue

            entry_a = word_dict[word_a]
            entry_b = word_dict[word_b]

            vec_a = entry_a.get('d2_vector')
            vec_b = entry_b.get('d2_vector')

            if not vec_a or not vec_b:
                continue

            key = (word_a, word_b)

            if key in self.pair_index:
                # Already known -- increment frequency
                if 'frequency' in self.pair_index[key]:
                    self.pair_index[key]['frequency'] += 1
                else:
                    self.pair_index[key]['frequency'] = 2
                continue

            # New pair -- compute D1 and store
            d1_info = d1_for_pair(vec_a, vec_b)
            d1_info['frequency'] = 1
            d1_info['source'] = 'study'

            self.pair_index[key] = d1_info

            # Add to lattice
            op = d1_info['d1_operator']
            dim = d1_info['dominant_dim']
            phase = d1_info['phase']
            tier = d1_info['tier']

            self.lattice[op][dim][phase][tier].append({
                'a': word_a,
                'b': word_b,
                'mag': d1_info['d1_magnitude'],
                'dist': 0.0,  # Not computed for text pairs
            })

            new_pairs += 1

        return new_pairs

    # ================================================================
    #  QUERY: Get word pairs by generator
    # ================================================================

    def get_pairs_for_operator(self, op: int,
                               dim: str = None,
                               phase: str = None,
                               tier: str = None,
                               limit: int = 10) -> List[dict]:
        """Get word pairs that produce a given D1 operator.

        Used by voice system to pick word transitions
        that match the current operator sequence.
        """
        results = []
        dims = [dim] if dim else _DIM_NAMES
        phases = [phase] if phase else ('being', 'doing', 'becoming')
        tiers = [tier] if tier else ('advanced', 'mid', 'simple')

        for d in dims:
            for p in phases:
                for t in tiers:
                    entries = self.lattice.get(op, {}).get(d, {}).get(p, {}).get(t, [])
                    results.extend(entries)
                    if len(results) >= limit:
                        return results[:limit]

        return results[:limit]

    def get_word_profile(self, word: str) -> Optional[dict]:
        """Get the D1 profile for a word: what generators does it trigger?"""
        return self.word_profiles.get(word)

    def get_transition(self, word_a: str, word_b: str) -> Optional[dict]:
        """Get D1 info for a specific word pair."""
        return self.pair_index.get((word_a, word_b))

    # ================================================================
    #  STATS: Distribution analysis
    # ================================================================

    def stats(self) -> dict:
        """Full D1 lattice statistics."""
        # Operator distribution
        op_counts = Counter()
        dim_counts = Counter()
        phase_counts = Counter()
        tier_counts = Counter()

        for op in range(NUM_OPS):
            for dim in _DIM_NAMES:
                for phase in ('being', 'doing', 'becoming'):
                    for tier in ('simple', 'mid', 'advanced'):
                        n = len(self.lattice.get(op, {}).get(dim, {})
                                .get(phase, {}).get(tier, []))
                        op_counts[op] += n
                        dim_counts[dim] += n
                        phase_counts[phase] += n
                        tier_counts[tier] += n

        total = sum(op_counts.values())

        # D1 vs D2 agreement: how often does a word's D1 dominant match its D2 dominant?
        agreement_count = 0
        profiled = 0
        for word, profile in self.word_profiles.items():
            profiled += 1
            if profile['dominant_d1'] == profile['d2_dominant']:
                agreement_count += 1

        return {
            'total_pairs': total,
            'unique_words': len(self.word_profiles),
            'build_time_s': round(self.build_time, 2),
            'operator_distribution': {
                OP_NAMES[op]: count for op, count in op_counts.most_common()
            },
            'dimension_distribution': dict(dim_counts.most_common()),
            'phase_distribution': dict(phase_counts.most_common()),
            'tier_distribution': dict(tier_counts.most_common()),
            'd1_d2_agreement': round(agreement_count / max(profiled, 1), 4),
            'profiled_words': profiled,
        }

    def report(self, log_fn=None) -> str:
        """Generate human-readable report of D1 lattice."""
        s = self.stats()
        lines = []
        lines.append("=" * 60)
        lines.append("  D1 GENERATOR LATTICE REPORT")
        lines.append("=" * 60)
        lines.append(f"  Total pairs:  {s['total_pairs']}")
        lines.append(f"  Unique words: {s['unique_words']}")
        lines.append(f"  Build time:   {s['build_time_s']}s")
        lines.append(f"  D1/D2 agree:  {s['d1_d2_agreement']:.1%}")
        lines.append("")
        lines.append("  OPERATOR DISTRIBUTION:")
        for name, count in s['operator_distribution'].items():
            pct = 100 * count / max(s['total_pairs'], 1)
            bar = '#' * int(pct / 2)
            lines.append(f"    {name:12s}: {count:6d} ({pct:5.1f}%) {bar}")
        lines.append("")
        lines.append("  DIMENSION DISTRIBUTION:")
        for name, count in s['dimension_distribution'].items():
            pct = 100 * count / max(s['total_pairs'], 1)
            lines.append(f"    {name:12s}: {count:6d} ({pct:5.1f}%)")
        lines.append("")
        lines.append("  PHASE DISTRIBUTION:")
        for name, count in s['phase_distribution'].items():
            pct = 100 * count / max(s['total_pairs'], 1)
            lines.append(f"    {name:12s}: {count:6d} ({pct:5.1f}%)")
        lines.append("")
        lines.append("  TIER DISTRIBUTION:")
        for name, count in s['tier_distribution'].items():
            pct = 100 * count / max(s['total_pairs'], 1)
            lines.append(f"    {name:12s}: {count:6d} ({pct:5.1f}%)")
        lines.append("=" * 60)

        text = '\n'.join(lines)
        if log_fn:
            for line in lines:
                log_fn(line)
        return text

    # ================================================================
    #  PERSISTENCE
    # ================================================================

    def save(self):
        """Persist D1 lattice and stats to disk."""
        # Save lattice (convert int keys to string for JSON)
        lattice_path = self.base_dir / D1_LATTICE_FILENAME
        serializable = {}
        for op in range(NUM_OPS):
            serializable[str(op)] = self.lattice.get(op, {})
        try:
            with open(lattice_path, 'w', encoding='utf-8') as f:
                json.dump(serializable, f)
        except IOError:
            pass

        # Save stats
        stats_path = self.base_dir / D1_STATS_FILENAME
        try:
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats(), f, indent=2)
        except IOError:
            pass

    def load(self) -> bool:
        """Load D1 lattice from disk. Returns True if loaded."""
        lattice_path = self.base_dir / D1_LATTICE_FILENAME
        if not lattice_path.exists():
            return False
        try:
            with open(lattice_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            # Convert string keys back to int
            self.lattice = {}
            for op_str, dim_data in raw.items():
                self.lattice[int(op_str)] = dim_data
            # Rebuild pair count
            total = 0
            for op in range(NUM_OPS):
                for dim in _DIM_NAMES:
                    for phase in ('being', 'doing', 'becoming'):
                        for tier in ('simple', 'mid', 'advanced'):
                            entries = (self.lattice.get(op, {}).get(dim, {})
                                       .get(phase, {}).get(tier, []))
                            total += len(entries)
            self.total_pairs = total
            return True
        except (json.JSONDecodeError, IOError, KeyError):
            self._init_lattice()
            return False


# ================================================================
#  STANDALONE: Run D1 lattice build on enriched dictionary
# ================================================================

def build_d1_lattice(dict_path: str = None, log_fn=None) -> D1LatticeBuilder:
    """Build D1 lattice from CK's enriched dictionary.

    Can be called standalone or from ck_study.py before study begins.
    """
    def log(msg):
        if log_fn:
            log_fn(msg)
        else:
            print(msg)

    # Find enriched dictionary
    if dict_path is None:
        # Try standard locations
        candidates = [
            'ck_sim/ck_dictionary_enriched.json',
            'ck_dictionary_enriched.json',
        ]
        for c in candidates:
            if os.path.exists(c):
                dict_path = c
                break

    if not dict_path or not os.path.exists(dict_path):
        log("  [D1-LATTICE] ERROR: No enriched dictionary found")
        return D1LatticeBuilder()

    log(f"  [D1-LATTICE] Loading dictionary: {dict_path}")
    with open(dict_path, 'r', encoding='utf-8') as f:
        word_dict = json.load(f)
    log(f"  [D1-LATTICE] {len(word_dict)} words loaded")

    # Check if we have a cached lattice newer than the dictionary
    builder = D1LatticeBuilder()
    lattice_path = builder.base_dir / D1_LATTICE_FILENAME
    if lattice_path.exists():
        dict_mtime = os.path.getmtime(dict_path)
        lattice_mtime = os.path.getmtime(str(lattice_path))
        if lattice_mtime > dict_mtime:
            log("  [D1-LATTICE] Loading cached lattice (newer than dictionary)")
            if builder.load():
                log(f"  [D1-LATTICE] Loaded {builder.total_pairs} cached pairs")
                return builder

    # Build fresh
    log("  [D1-LATTICE] Building fresh D1 lattice...")
    builder.build_from_dictionary(word_dict, log_fn=log)
    builder.save()
    builder.report(log_fn=log)

    return builder


if __name__ == '__main__':
    """Run standalone: python -m ck_sim.becoming.ck_d1_lattice_builder"""
    import sys

    print()
    print("  CK D1 LATTICE BUILDER")
    print("  Learn generators before complexity.")
    print()

    builder = build_d1_lattice(log_fn=print)

    print()
    print("  D1 lattice built. CK knows his generators.")
    print("  Now he can study with direction.")
    print()
