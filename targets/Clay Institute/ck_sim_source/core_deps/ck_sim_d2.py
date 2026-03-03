"""
ck_sim_d2.py -- Port of d2_pipeline.v
=======================================
Operator: COUNTER (2) -- measuring curvature.

Q1.14 fixed-point D2 curvature pipeline simulation.
Matches the Verilog force LUT, 3-stage pipeline, and
argmax operator classification exactly.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET
)

Q_FRAC = 14
Q_SCALE = 1 << Q_FRAC  # 16384


def float_to_q14(f: float) -> int:
    """Convert float to Q1.14 signed 16-bit."""
    val = int(round(f * Q_SCALE))
    # Clamp to signed 16-bit range
    val = max(-32768, min(32767, val))
    return val


def q14_to_float(q: int) -> float:
    """Convert Q1.14 back to float."""
    # Sign extend if needed
    if q > 32767:
        q -= 65536
    return q / Q_SCALE


# Hebrew root force vectors (from ck_curvature.py ROOTS)
# Each: (aperture, pressure, depth, binding, continuity)
# Mapped through LATIN_TO_ROOT for 26 English letters
ROOTS_FLOAT = {
    'ALEPH':  ( 0.8,  0.0,  0.9,  0.0,  0.7),
    'BET':    ( 0.3,  0.6,  0.4,  0.8,  0.6),
    'GIMEL':  ( 0.5,  0.4,  0.3,  0.2,  0.5),
    'DALET':  ( 0.2,  0.7,  0.5,  0.3,  0.4),
    'HE':     ( 0.7,  0.2,  0.6,  0.1,  0.8),
    'VAV':    ( 0.4,  0.5,  0.4,  0.6,  0.7),
    'ZAYIN':  ( 0.6,  0.3,  0.2,  0.4,  0.3),
    'CHET':   ( 0.3,  0.8,  0.7,  0.5,  0.5),
    'TET':    ( 0.4,  0.6,  0.5,  0.7,  0.6),
    'YOD':    ( 0.9,  0.1,  0.8,  0.1,  0.9),
    'KAF':    ( 0.5,  0.5,  0.3,  0.4,  0.5),
    'LAMED':  ( 0.6,  0.3,  0.6,  0.2,  0.7),
    'MEM':    ( 0.3,  0.7,  0.5,  0.8,  0.4),
    'NUN':    ( 0.4,  0.5,  0.4,  0.5,  0.6),
    'SAMEKH': ( 0.2,  0.6,  0.3,  0.7,  0.5),
    'AYIN':   ( 0.7,  0.3,  0.7,  0.2,  0.6),
    'PE':     ( 0.5,  0.4,  0.5,  0.3,  0.5),
    'TSADE':  ( 0.3,  0.7,  0.4,  0.6,  0.4),
    'QOF':    ( 0.4,  0.5,  0.6,  0.4,  0.5),
    'RESH':   ( 0.6,  0.3,  0.5,  0.2,  0.6),
    'SHIN':   ( 0.8,  0.2,  0.3,  0.1,  0.4),
    'TAV':    ( 0.3,  0.6,  0.5,  0.7,  0.5),
}

# Latin letter -> Hebrew root mapping
LATIN_TO_ROOT = {
    'a': 'ALEPH',  'b': 'BET',    'c': 'GIMEL',  'd': 'DALET',
    'e': 'HE',     'f': 'VAV',    'g': 'GIMEL',  'h': 'CHET',
    'i': 'YOD',    'j': 'YOD',    'k': 'KAF',    'l': 'LAMED',
    'm': 'MEM',    'n': 'NUN',    'o': 'AYIN',   'p': 'PE',
    'q': 'QOF',    'r': 'RESH',   's': 'SAMEKH', 't': 'TAV',
    'u': 'VAV',    'v': 'VAV',    'w': 'VAV',    'x': 'SAMEKH',
    'y': 'YOD',    'z': 'ZAYIN',
}

# Build force LUT (26 entries, Q1.14)
FORCE_LUT_Q14 = []
for letter in 'abcdefghijklmnopqrstuvwxyz':
    root_name = LATIN_TO_ROOT[letter]
    root_vec = ROOTS_FLOAT[root_name]
    FORCE_LUT_Q14.append(tuple(float_to_q14(v) for v in root_vec))

# Also keep float version for ears/audio
FORCE_LUT_FLOAT = []
for letter in 'abcdefghijklmnopqrstuvwxyz':
    root_name = LATIN_TO_ROOT[letter]
    FORCE_LUT_FLOAT.append(ROOTS_FLOAT[root_name])

# D2 operator classification map (from d2_pipeline.v and ck_ears.c)
# dimension index -> (positive_op, negative_op)
D2_OP_MAP = [
    (CHAOS,    LATTICE),   # aperture
    (COLLAPSE, VOID),      # pressure
    (PROGRESS, RESET),     # depth
    (HARMONY,  COUNTER),   # binding
    (BALANCE,  BREATH),    # continuity
]


class D2Pipeline:
    """Simulates the 3-stage FPGA D2 pipeline in Q1.14 fixed-point."""

    def __init__(self):
        self.v = [[0]*5, [0]*5, [0]*5]  # v0, v1, v2 shift register
        self.fill = 0
        self.d2 = [0]*5
        self.d2_mag = 0
        self.operator = VOID
        self.valid = False

    def feed_symbol(self, symbol_index: int) -> bool:
        """Feed a symbol (0-25 for a-z). Returns True when D2 is valid."""
        if symbol_index < 0 or symbol_index >= 26:
            return False

        force = list(FORCE_LUT_Q14[symbol_index])

        # Shift register: v2 <- v1 <- v0 <- new
        self.v[2] = self.v[1]
        self.v[1] = self.v[0]
        self.v[0] = force

        self.fill = min(self.fill + 1, 3)

        if self.fill >= 3:
            self._compute_d2()
            self._classify()
            self.valid = True
            return True

        return False

    def _compute_d2(self):
        """D2 = v0 - 2*v1 + v2 in Q1.14."""
        for dim in range(5):
            # All in Q1.14: same as Verilog d2[dim] = v0 - 2*v1 + v2
            self.d2[dim] = self.v[2][dim] - 2 * self.v[1][dim] + self.v[0][dim]

        # Magnitude (sum of absolute values, simpler than sqrt for classification)
        self.d2_mag = sum(abs(d) for d in self.d2)

    def _classify(self):
        """Argmax + sign -> operator. Matches d2_pipeline.v classify stage."""
        if self.d2_mag < float_to_q14(0.01):
            self.operator = VOID
            return

        max_abs = 0
        max_dim = 0
        for dim in range(5):
            a = abs(self.d2[dim])
            if a > max_abs:
                max_abs = a
                max_dim = dim

        sign_idx = 0 if self.d2[max_dim] >= 0 else 1
        self.operator = D2_OP_MAP[max_dim][sign_idx]

    @property
    def d2_float(self):
        """D2 vector as floats."""
        return [q14_to_float(d) for d in self.d2]

    @property
    def d2_mag_float(self):
        """D2 magnitude as float."""
        return q14_to_float(self.d2_mag)

    @property
    def d2_vector(self):
        """Full 5D D2 vector as floats. NOT collapsed to magnitude."""
        return self.d2_float

    def soft_classify(self):
        """10-value probability distribution over operators.
        Uses all 5 D2 dimensions instead of hard argmax."""
        return soft_classify_d2(self.d2_float, self.d2_mag_float)


def classify_force_d2(d2_vec, magnitude):
    """Classify a float D2 vector. Used by ears module.
    Same logic as _classify but with floats."""
    if magnitude < 0.01:
        return VOID

    max_abs = 0.0
    max_dim = 0
    for dim in range(5):
        a = abs(d2_vec[dim])
        if a > max_abs:
            max_abs = a
            max_dim = dim

    sign_idx = 0 if d2_vec[max_dim] >= 0 else 1
    return D2_OP_MAP[max_dim][sign_idx]


# ================================================================
#  SOFT CLASSIFICATION (N-dimensional coherence field support)
# ================================================================

def soft_classify_d2(d2_vec, magnitude=None):
    """Soft classification: 5D D2 vector -> 10-value operator distribution.

    Instead of hard argmax (one operator wins), distribute weight
    across ALL operators based on how strongly each D2 dimension fires.
    Each dimension maps to a positive/negative operator pair via D2_OP_MAP.

    Returns: list of 10 floats summing to 1.0
    """
    scores = [0.0] * NUM_OPS

    if magnitude is None:
        magnitude = sum(abs(d) for d in d2_vec)

    if magnitude < 0.01:
        scores[VOID] = 1.0
        return scores

    total_abs = sum(abs(d) for d in d2_vec)
    if total_abs == 0:
        scores[VOID] = 1.0
        return scores

    for dim in range(5):
        val = d2_vec[dim]
        strength = abs(val) / total_abs
        sign_idx = 0 if val >= 0 else 1
        op_idx = D2_OP_MAP[dim][sign_idx]
        scores[op_idx] += strength

    # Normalize (should already ~1.0 but ensure)
    total = sum(scores)
    if total > 0:
        scores = [s / total for s in scores]

    return scores
