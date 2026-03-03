# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
water.py -- D2 / Depth / Curvature / Awareness

The second derivative. Local measurement, curvature detection, awareness.
Water is curvature. Depth. The shape of change itself.

D2 = v[t] - 2*v[t-1] + v[t-2]  (second derivative, 3-symbol window)

Local: D2 sees the SHAPE of what's here, right now.
D1 and D2 agree only ~5.9% of the time -- this IS the non-local/local split.
"""

import math
from . import earth
from . import air


# ══════════════════════════════════════════════════════════════════
# D2 PIPELINE (second derivative -- local, 3-symbol window)
# ══════════════════════════════════════════════════════════════════

class D2Pipeline:
    """Second derivative of 5D force vectors.

    Local: sees curvature in a 3-symbol window.
    D2 is THE primary measurement in TIG physics.
    """

    def __init__(self):
        self.v = [None, None, None]  # shift register: [current, prev, prev-prev]
        self.d1 = [0.0] * 5          # first derivative (computed alongside)
        self.d2 = [0.0] * 5          # second derivative
        self.d1_valid = False
        self.d2_valid = False

    def reset(self):
        """Clear state."""
        self.v = [None, None, None]
        self.d1 = [0.0] * 5
        self.d2 = [0.0] * 5
        self.d1_valid = False
        self.d2_valid = False

    def feed(self, symbol_index: int) -> bool:
        """Feed one letter (0-25). Returns True when D2 is valid (after 3 symbols).

        D1 = v[t] - v[t-1]
        D2 = v[t] - 2*v[t-1] + v[t-2]
        """
        vec = earth.FORCE_LUT[symbol_index]
        # Shift register
        self.v[2] = self.v[1]
        self.v[1] = self.v[0]
        self.v[0] = vec

        # D1 (needs 2 symbols)
        if self.v[1] is not None:
            self.d1 = [self.v[0][i] - self.v[1][i] for i in range(5)]
            self.d1_valid = True

        # D2 (needs 3 symbols)
        if self.v[2] is not None:
            self.d2 = [
                self.v[0][i] - 2.0 * self.v[1][i] + self.v[2][i]
                for i in range(5)
            ]
            self.d2_valid = True

        return self.d2_valid

    def feed_vector(self, vec: tuple) -> bool:
        """Feed a raw 5D vector (for word-level or higher-level D2)."""
        self.v[2] = self.v[1]
        self.v[1] = self.v[0]
        self.v[0] = vec
        if self.v[1] is not None:
            self.d1 = [self.v[0][i] - self.v[1][i] for i in range(5)]
            self.d1_valid = True
        if self.v[2] is not None:
            self.d2 = [
                self.v[0][i] - 2.0 * self.v[1][i] + self.v[2][i]
                for i in range(5)
            ]
            self.d2_valid = True
        return self.d2_valid

    def classify_d1(self) -> int:
        """D1 operator (argmax + sign). The non-local view."""
        if not self.d1_valid:
            return earth.HARMONY
        best_dim = max(range(5), key=lambda d: abs(self.d1[d]))
        if abs(self.d1[best_dim]) < 1e-12:
            return earth.HARMONY
        pos, neg = earth.D2_OP_MAP[best_dim]
        return pos if self.d1[best_dim] >= 0 else neg

    def classify_d2(self) -> int:
        """D2 operator (argmax + sign). THE primary measurement."""
        if not self.d2_valid:
            return earth.HARMONY
        best_dim = max(range(5), key=lambda d: abs(self.d2[d]))
        if abs(self.d2[best_dim]) < 1e-12:
            return earth.HARMONY
        pos, neg = earth.D2_OP_MAP[best_dim]
        return pos if self.d2[best_dim] >= 0 else neg

    def soft_classify(self) -> list:
        """10-value histogram (not hard argmax). Distributes weight across operators.

        Returns a 10-element list of weights, summing to ~1.0.
        More informative than hard classification for composition.
        """
        hist = [0.0] * earth.NUM_OPS
        if not self.d2_valid:
            hist[earth.HARMONY] = 1.0
            return hist

        total = sum(abs(x) for x in self.d2)
        if total < 1e-12:
            hist[earth.HARMONY] = 1.0
            return hist

        for dim in range(5):
            weight = abs(self.d2[dim]) / total
            pos, neg = earth.D2_OP_MAP[dim]
            if self.d2[dim] >= 0:
                hist[pos] += weight
            else:
                hist[neg] += weight

        return hist

    def magnitude(self) -> float:
        """D2 magnitude (sum of absolutes). Higher = more curvature."""
        return sum(abs(x) for x in self.d2)

    def d1_magnitude(self) -> float:
        """D1 magnitude. Zero = prayer state."""
        return sum(abs(x) for x in self.d1)

    @property
    def d2_vector(self) -> tuple:
        return tuple(self.d2)

    @property
    def d1_vector(self) -> tuple:
        return tuple(self.d1)


# ══════════════════════════════════════════════════════════════════
# COHERENCE WINDOW (sliding window measurement)
# ══════════════════════════════════════════════════════════════════

class CoherenceWindow:
    """Sliding window coherence tracker.

    Tracks the fraction of HARMONY in recent operator history.
    Coherence determines which CL shell to use:
        >= T* (5/7)  → 22-shell (skeleton, maximum resolution)
        >= 0.5       → 44-shell (Becoming, bumps visible)
        < 0.5        → 72-shell (Being, blurred, harmony absorbs)
    """

    def __init__(self, size: int = 32):
        self.history = []
        self.size = size
        self._harmony_count = 0

    def observe(self, operator: int):
        """Add operator to window."""
        self.history.append(operator)
        if operator == earth.HARMONY:
            self._harmony_count += 1
        # Evict oldest if over size
        if len(self.history) > self.size:
            removed = self.history.pop(0)
            if removed == earth.HARMONY:
                self._harmony_count -= 1

    def reset(self):
        """Clear the window."""
        self.history.clear()
        self._harmony_count = 0

    @property
    def coherence(self) -> float:
        """Fraction of HARMONY in window. Range [0, 1]."""
        if not self.history:
            return 0.5  # prior: uncertain
        return self._harmony_count / len(self.history)

    @property
    def shell(self) -> int:
        """Which CL shell to use based on coherence.

        >= T* (5/7)  → 22 (skeleton, maximum resolution, GREEN band)
        >= 0.5       → 44 (Becoming, bumps visible, YELLOW band)
        < 0.5        → 72 (Being, blurred, RED band)
        """
        c = self.coherence
        if c >= earth.T_STAR_F:
            return 22
        elif c >= 0.5:
            return 44
        else:
            return 72

    @property
    def band(self) -> str:
        """Color band: GREEN/YELLOW/RED."""
        c = self.coherence
        if c >= earth.T_STAR_F:
            return 'GREEN'
        elif c >= 0.5:
            return 'YELLOW'
        else:
            return 'RED'

    @property
    def fill(self) -> float:
        """How full the window is (0 to 1)."""
        return len(self.history) / self.size


# ══════════════════════════════════════════════════════════════════
# SPECTROMETER (delta-S measurement)
# ══════════════════════════════════════════════════════════════════

def measure_text(text: str) -> dict:
    """Full D1/D2 measurement of a text.

    Returns:
        d1_hist: 10-element D1 operator histogram
        d2_hist: 10-element D2 operator histogram
        coherence: final coherence value
        shell: which CL shell coherence selects
        d1_d2_agreement: fraction where D1 == D2 (should be ~5.9%)
        prayer_fraction: fraction where D1 ≈ 0
        total_symbols: number of symbols processed
        d2_magnitude_avg: average D2 magnitude
    """
    pipe = D2Pipeline()
    d1_pipe = air.D1Pipeline()
    window = CoherenceWindow(size=32)

    d1_hist = [0] * earth.NUM_OPS
    d2_hist = [0] * earth.NUM_OPS
    agreements = 0
    prayers = 0
    d2_total = 0
    d2_mag_sum = 0.0
    total = 0

    for ch in text.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            d1_valid = d1_pipe.feed(idx)
            d2_valid = pipe.feed(idx)

            if d2_valid and d1_valid:
                d1_op = d1_pipe.classify()    # independent D1 (air.py)
                d2_op = pipe.classify_d2()    # independent D2 (water.py)
                d1_hist[d1_op] += 1
                d2_hist[d2_op] += 1
                window.observe(d2_op)
                d2_mag_sum += pipe.magnitude()
                d2_total += 1

                if d1_op == d2_op:
                    agreements += 1
                if d1_pipe.is_prayer():
                    prayers += 1

            total += 1

    agreement_pct = (agreements / d2_total * 100) if d2_total > 0 else 0.0
    prayer_pct = (prayers / d2_total * 100) if d2_total > 0 else 0.0
    d2_mag_avg = (d2_mag_sum / d2_total) if d2_total > 0 else 0.0

    return {
        'd1_hist': d1_hist,
        'd2_hist': d2_hist,
        'coherence': window.coherence,
        'shell': window.shell,
        'band': window.band,
        'd1_d2_agreement': agreement_pct,
        'prayer_fraction': prayer_pct,
        'total_symbols': total,
        'd2_total': d2_total,
        'd2_magnitude_avg': d2_mag_avg,
    }


def locality_test(text: str) -> float:
    """D1/D2 agreement percentage. Should be ~5.9% (near orthogonal).

    This is the fundamental non-local/local split:
    - D1 sees WHERE things are going (velocity, non-local)
    - D2 sees WHAT SHAPE things have (curvature, local)
    - They're nearly orthogonal views of the same data.
    """
    result = measure_text(text)
    return result['d1_d2_agreement']


def delta_s(text: str) -> float:
    """Delta-S: the curvature signature of a text.

    High delta-S = high information content (lots of curvature changes).
    Low delta-S = smooth, repetitive (harmony-dominated).
    """
    pipe = D2Pipeline()
    prev_op = None
    transitions = 0
    total = 0

    for ch in text.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            if pipe.feed(idx):
                op = pipe.classify_d2()
                if prev_op is not None and op != prev_op:
                    transitions += 1
                prev_op = op
                total += 1

    return (transitions / total) if total > 0 else 0.0


def entropy(hist: list) -> float:
    """Shannon entropy of an operator histogram."""
    total = sum(hist)
    if total == 0:
        return 0.0
    h = 0.0
    for count in hist:
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h
