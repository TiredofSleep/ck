"""
D2 Pipeline — Text to 5D force vectors to operator classification.

Every letter maps to a Hebrew root with 5 force dimensions:
  Aperture (mouth openness), Pressure (articulatory force),
  Depth (pharyngeal depth), Binding (consonant closure),
  Continuity (sustained voicing).

D1 = first derivative (velocity). D2 = second derivative (curvature).
Curvature IS the physics. The shape of language through force-space.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import math
from .cl_tables import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)

# ── Hebrew Root Force LUT (26 letters → 5D) ──────────────────────
# Each letter maps to a Hebrew root. Each root has 5 force dimensions.
# [aperture, pressure, depth, binding, continuity]

ROOTS_FLOAT = {
    'a': (0.8, 0.0, 0.9, 0.0, 0.7),  # ALEPH
    'b': (0.3, 0.6, 0.4, 0.8, 0.6),  # BET
    'c': (0.5, 0.5, 0.3, 0.4, 0.5),  # KAF
    'd': (0.2, 0.7, 0.5, 0.3, 0.4),  # DALET
    'e': (0.7, 0.2, 0.6, 0.1, 0.8),  # HE
    'f': (0.5, 0.4, 0.5, 0.3, 0.5),  # PE
    'g': (0.5, 0.4, 0.3, 0.2, 0.5),  # GIMEL
    'h': (0.3, 0.8, 0.7, 0.5, 0.5),  # CHET
    'i': (0.9, 0.1, 0.8, 0.1, 0.9),  # YOD
    'j': (0.5, 0.4, 0.3, 0.2, 0.5),  # GIMEL
    'k': (0.5, 0.5, 0.3, 0.4, 0.5),  # KAF
    'l': (0.6, 0.3, 0.6, 0.2, 0.7),  # LAMED
    'm': (0.3, 0.7, 0.5, 0.8, 0.4),  # MEM
    'n': (0.4, 0.5, 0.4, 0.5, 0.6),  # NUN
    'o': (0.7, 0.3, 0.7, 0.2, 0.6),  # AYIN
    'p': (0.5, 0.4, 0.5, 0.3, 0.5),  # PE
    'q': (0.4, 0.5, 0.6, 0.4, 0.5),  # QOF
    'r': (0.6, 0.4, 0.5, 0.3, 0.6),  # RESH
    's': (0.2, 0.6, 0.3, 0.7, 0.5),  # SAMEKH
    't': (0.3, 0.7, 0.3, 0.8, 0.5),  # TAV
    'u': (0.4, 0.5, 0.4, 0.6, 0.7),  # VAV
    'v': (0.4, 0.5, 0.4, 0.6, 0.7),  # VAV
    'w': (0.5, 0.6, 0.4, 0.5, 0.4),  # SHIN
    'x': (0.3, 0.7, 0.4, 0.6, 0.4),  # TSADE
    'y': (0.9, 0.1, 0.8, 0.1, 0.9),  # YOD
    'z': (0.6, 0.3, 0.2, 0.4, 0.3),  # ZAYIN
}

# D2 dimension → operator pair mapping (positive/negative)
# Each of the 5 D2 dimensions maps to two operators
D2_OP_MAP = [
    (CHAOS, LATTICE),     # aperture:    +open → CHAOS,    -closed → LATTICE
    (COLLAPSE, VOID),     # pressure:    +force → COLLAPSE, -none → VOID
    (PROGRESS, RESET),    # depth:       +deep → PROGRESS, -shallow → RESET
    (HARMONY, COUNTER),   # binding:     +bound → HARMONY, -free → COUNTER
    (BALANCE, BREATH),    # continuity:  +sustained → BALANCE, -pulsed → BREATH
]


class D2Pipeline:
    """3-stage shift register: feed letters → compute D1 (velocity) → D2 (curvature)."""

    def __init__(self):
        self._shift = [None, None, None]  # [v0, v1, v2]
        self._count = 0
        self.d1 = None       # First derivative (5D)
        self.d2 = None       # Second derivative (5D)
        self.d1_valid = False
        self.d2_valid = False
        self.operator = HARMONY  # Last classified operator

    def feed(self, ch: str) -> bool:
        """Feed a character. Returns True when D2 fires (after 3 letters)."""
        ch = ch.lower()
        if ch not in ROOTS_FLOAT:
            return False

        vec = ROOTS_FLOAT[ch]
        # Shift register: new → v0, old v0 → v1, old v1 → v2
        self._shift[2] = self._shift[1]
        self._shift[1] = self._shift[0]
        self._shift[0] = vec
        self._count += 1

        # D1 after 2 letters
        if self._count >= 2 and self._shift[1] is not None:
            self.d1 = tuple(
                self._shift[0][d] - self._shift[1][d] for d in range(5)
            )
            self.d1_valid = True

        # D2 after 3 letters
        if self._count >= 3 and self._shift[2] is not None:
            self.d2 = tuple(
                self._shift[0][d] - 2.0 * self._shift[1][d] + self._shift[2][d]
                for d in range(5)
            )
            self.d2_valid = True
            self.operator = classify_d2(self.d2)
            return True

        return False

    def reset(self):
        self._shift = [None, None, None]
        self._count = 0
        self.d1 = self.d2 = None
        self.d1_valid = self.d2_valid = False
        self.operator = HARMONY


def classify_d2(d2_vec) -> int:
    """Classify a D2 curvature vector to its dominant operator."""
    best_dim = 0
    best_mag = 0.0
    for d in range(5):
        mag = abs(d2_vec[d])
        if mag > best_mag:
            best_mag = mag
            best_dim = d
    if best_mag < 1e-10:
        return HARMONY
    pos_op, neg_op = D2_OP_MAP[best_dim]
    return pos_op if d2_vec[best_dim] > 0 else neg_op


def soft_classify_d2(d2_vec):
    """Soft classification: returns probability distribution over 10 operators."""
    dist = [0.0] * NUM_OPS
    total = 0.0
    for d in range(5):
        mag = abs(d2_vec[d])
        if mag < 1e-10:
            continue
        pos_op, neg_op = D2_OP_MAP[d]
        if d2_vec[d] > 0:
            dist[pos_op] += mag
        else:
            dist[neg_op] += mag
        total += mag
    if total > 0:
        dist = [x / total for x in dist]
    else:
        dist[HARMONY] = 1.0
    return dist


def text_to_force(text: str):
    """Encode text as mean 5D force vector from Hebrew roots."""
    sums = [0.0] * 5
    count = 0
    for ch in text.lower():
        if ch in ROOTS_FLOAT:
            vec = ROOTS_FLOAT[ch]
            for d in range(5):
                sums[d] += vec[d]
            count += 1
    if count == 0:
        return (0.5, 0.5, 0.5, 0.5, 0.5)
    return tuple(s / count for s in sums)


def text_to_ops(text: str):
    """Encode text as D2 operator sequence."""
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        if pipe.feed(ch):
            ops.append(pipe.operator)
    return tuple(ops)


def text_to_force_and_ops(text: str):
    """Encode text as both 5D force vector and operator sequence."""
    return text_to_force(text), text_to_ops(text)


def word_triadic_signature(word: str):
    """Compute 15D triadic signature: Being (5D) + Doing (5D) + Becoming (5D).

    Being  = mean of all letter forces (position)
    Doing  = mean of D1 vectors (velocity)
    Becoming = mean of D2 vectors (curvature)
    """
    pipe = D2Pipeline()
    forces = []
    d1s = []
    d2s = []

    for ch in word.lower():
        if ch in ROOTS_FLOAT:
            forces.append(ROOTS_FLOAT[ch])
            if pipe.feed(ch):
                if pipe.d1_valid and pipe.d1:
                    d1s.append(pipe.d1)
                if pipe.d2_valid and pipe.d2:
                    d2s.append(pipe.d2)

    def mean_vec(vecs):
        if not vecs:
            return (0.0, 0.0, 0.0, 0.0, 0.0)
        n = len(vecs)
        return tuple(sum(v[d] for v in vecs) / n for d in range(5))

    being = mean_vec(forces)
    doing = mean_vec(d1s)
    becoming = mean_vec(d2s)
    return being, doing, becoming


def cosine_similarity(a, b):
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a < 1e-10 or mag_b < 1e-10:
        return 0.0
    return dot / (mag_a * mag_b)


def force_distance(a, b):
    """Euclidean distance in 5D force space."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
