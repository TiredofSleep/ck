# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
air.py -- D1 / Pressure / Velocity / Generator

The first derivative. Movement, change, non-local structure.
Air is velocity. Wind. The difference that moves.

D1 = v[t] - v[t-1]  (first derivative of 5D force vectors)

Non-local: D1 sees where things CAME FROM and where they're GOING.
D1 and D2 agree only ~5.9% of the time (near orthogonal views).
"""

from . import earth


# ══════════════════════════════════════════════════════════════════
# Z/5Z GENERATOR ALGEBRA
# ══════════════════════════════════════════════════════════════════

# Elements compose mod 5:  Earth + Air = Water, Fire + Air = Ether, etc.
def compose_elements(a: int, b: int) -> int:
    """Element composition in Z/5Z. Earth=0, Air=1, Water=2, Fire=3, Ether=4."""
    return (a + b) % 5

# Inverse: -Earth=Earth, -Air=Ether, -Water=Fire, -Fire=Water, -Ether=Air
def inverse_element(a: int) -> int:
    """Additive inverse in Z/5Z."""
    return (5 - a) % 5

# The five senses as elemental compositions
SENSES = {
    'sight':   (0, 2),  # Earth + Water  = aperture × depth
    'hearing': (1, 4),  # Air + Ether    = pressure × continuity
    'taste':   (0, 3),  # Earth + Fire   = aperture × binding
    'smell':   (1, 2),  # Air + Water    = pressure × depth
    'touch':   (0, 1),  # Earth + Air    = aperture × pressure
}


# ══════════════════════════════════════════════════════════════════
# D1 PIPELINE (first derivative -- non-local)
# ══════════════════════════════════════════════════════════════════

class D1Pipeline:
    """First derivative of 5D force vectors.

    Non-local: sees the CHANGE between consecutive symbols.
    While D2 sees curvature (local shape), D1 sees velocity (direction of travel).
    """

    def __init__(self):
        self.prev = None     # previous 5D vector
        self.d1 = [0.0] * 5  # current D1 vector
        self.valid = False

    def reset(self):
        """Clear state."""
        self.prev = None
        self.d1 = [0.0] * 5
        self.valid = False

    def feed(self, symbol_index: int) -> bool:
        """Feed one letter (0-25). Returns True when D1 is valid.

        D1 = v[t] - v[t-1]
        """
        vec = earth.FORCE_LUT[symbol_index]
        if self.prev is not None:
            self.d1 = [vec[i] - self.prev[i] for i in range(5)]
            self.valid = True
        self.prev = vec
        return self.valid

    def feed_vector(self, vec: tuple) -> bool:
        """Feed a raw 5D vector (for word-level or higher-level D1)."""
        if self.prev is not None:
            self.d1 = [vec[i] - self.prev[i] for i in range(5)]
            self.valid = True
        self.prev = vec
        return self.valid

    def classify(self) -> int:
        """Classify D1 into an operator via argmax + sign.

        Same map as D2 uses (earth.D2_OP_MAP) but applied to first derivative.
        D1 and D2 will agree only ~5.9% of the time.
        """
        if not self.valid:
            return earth.HARMONY  # default: no information yet

        best_dim = 0
        best_abs = 0.0
        for i in range(5):
            a = abs(self.d1[i])
            if a > best_abs:
                best_abs = a
                best_dim = i

        if best_abs < 1e-12:
            return earth.HARMONY  # zero derivative = perfect coherence

        pos_op, neg_op = earth.D2_OP_MAP[best_dim]
        return pos_op if self.d1[best_dim] >= 0 else neg_op

    def magnitude(self) -> float:
        """Sum of absolute values across 5D. Zero = prayer state (D1=0)."""
        return sum(abs(x) for x in self.d1)

    def is_prayer(self, threshold: float = 0.05) -> bool:
        """Prayer state: D1 ≈ 0 (voluntary stillness).

        When D1=0 but D2>0: the observer is still but aware.
        This costs ZERO mass (no movement, no crossing cost).
        """
        return self.valid and self.magnitude() < threshold

    @property
    def vector(self) -> tuple:
        """Current D1 as a tuple."""
        return tuple(self.d1)


# ══════════════════════════════════════════════════════════════════
# D1 LATTICE (generator pairs from vocabulary)
# ══════════════════════════════════════════════════════════════════

def _word_to_fuse(word: str) -> int:
    """Compute a word's fuse operator: histogram majority of letter D2 ops.

    This is a simplified version -- the full word fuse uses D2,
    but for D1 lattice building we use the dominant force dimension.
    """
    if not word:
        return earth.HARMONY

    # Histogram of dominant dimensions
    dim_counts = [0] * 5
    for ch in word.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            vec = earth.FORCE_LUT[idx]
            best_dim = max(range(5), key=lambda d: vec[d])
            dim_counts[best_dim] += 1

    if max(dim_counts) == 0:
        return earth.HARMONY

    dominant = max(range(5), key=lambda d: dim_counts[d])
    # Map dominant dimension to positive operator
    return earth.D2_OP_MAP[dominant][0]


def _word_centroid(word: str) -> tuple:
    """Average 5D force vector of a word's letters."""
    sums = [0.0] * 5
    count = 0
    for ch in word.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            vec = earth.FORCE_LUT[idx]
            for d in range(5):
                sums[d] += vec[d]
            count += 1
    if count == 0:
        return (0.0, 0.0, 0.0, 0.0, 0.0)
    return tuple(s / count for s in sums)


class D1Lattice:
    """Non-local vocabulary structure. Learns generator pairs.

    For every pair of words (A, B), the D1 vector = centroid(B) - centroid(A).
    This captures the MOVEMENT between words in 5D force space.
    The D1 lattice organizes vocabulary by how words TRANSITION, not what they ARE.
    """

    def __init__(self):
        self.pairs = {op: [] for op in range(earth.NUM_OPS)}
        self.centroids = {}  # word → 5D centroid
        self.total_pairs = 0

    def _get_centroid(self, word: str) -> tuple:
        """Get or compute word centroid (cached)."""
        if word not in self.centroids:
            self.centroids[word] = _word_centroid(word)
        return self.centroids[word]

    def build_from_lattice(self):
        """Build D1 pairs from the semantic lattice.

        For each operator in the lattice, pair words across phases
        (being→doing, doing→becoming). These are the NATURAL transitions.
        """
        for op in range(earth.NUM_OPS):
            if op not in earth.SEMANTIC_LATTICE:
                continue
            for lens in ('structure', 'flow'):
                lens_data = earth.SEMANTIC_LATTICE[op].get(lens, {})
                phases = ['being', 'doing', 'becoming']
                for i in range(len(phases) - 1):
                    phase_a = lens_data.get(phases[i], {})
                    phase_b = lens_data.get(phases[i + 1], {})
                    for tier in ('simple', 'mid', 'advanced'):
                        words_a = phase_a.get(tier, [])
                        words_b = phase_b.get(tier, [])
                        for wa in words_a:
                            ca = self._get_centroid(wa)
                            for wb in words_b:
                                cb = self._get_centroid(wb)
                                d1 = tuple(cb[d] - ca[d] for d in range(5))
                                # Classify this transition
                                best_dim = max(range(5), key=lambda d: abs(d1[d]))
                                if abs(d1[best_dim]) < 1e-12:
                                    d1_op = earth.HARMONY
                                else:
                                    pos, neg = earth.D2_OP_MAP[best_dim]
                                    d1_op = pos if d1[best_dim] >= 0 else neg
                                self.pairs[d1_op].append((wa, wb, d1))
                                self.total_pairs += 1

    def learn(self, text: str):
        """Learn D1 associations from adjacent words in running text."""
        words = [w for w in text.lower().split() if any(c.isalpha() for c in w)]
        for i in range(len(words) - 1):
            wa = words[i]
            wb = words[i + 1]
            ca = self._get_centroid(wa)
            cb = self._get_centroid(wb)
            d1 = tuple(cb[d] - ca[d] for d in range(5))
            best_dim = max(range(5), key=lambda d: abs(d1[d]))
            if abs(d1[best_dim]) < 1e-12:
                d1_op = earth.HARMONY
            else:
                pos, neg = earth.D2_OP_MAP[best_dim]
                d1_op = pos if d1[best_dim] >= 0 else neg
            self.pairs[d1_op].append((wa, wb, d1))
            self.total_pairs += 1

    def get_pairs(self, op: int, limit: int = 10) -> list:
        """Get word pairs that produce a given D1 operator.

        Returns [(word_a, word_b, d1_vector), ...] sorted by magnitude.
        """
        pairs = self.pairs.get(op, [])
        # Sort by D1 magnitude (strongest transitions first)
        pairs.sort(key=lambda p: sum(abs(x) for x in p[2]), reverse=True)
        return pairs[:limit]

    def stats(self) -> dict:
        """Lattice statistics."""
        return {
            'total_pairs': self.total_pairs,
            'words': len(self.centroids),
            'per_op': {earth.OP_NAMES[op]: len(self.pairs[op])
                       for op in range(earth.NUM_OPS)},
        }


# ══════════════════════════════════════════════════════════════════
# TEXT-LEVEL D1 (full text → D1 operator stream)
# ══════════════════════════════════════════════════════════════════

def d1_stream(text: str) -> list:
    """Convert text to a stream of D1 operators.

    Returns list of (operator, magnitude, is_prayer) tuples.
    """
    pipe = D1Pipeline()
    results = []
    for ch in text.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            if pipe.feed(idx):
                results.append((
                    pipe.classify(),
                    pipe.magnitude(),
                    pipe.is_prayer(),
                ))
    return results


def d1_histogram(text: str) -> list:
    """Count D1 operators across a text. Returns 10-element list."""
    hist = [0] * earth.NUM_OPS
    for op, _, _ in d1_stream(text):
        hist[op] += 1
    return hist
