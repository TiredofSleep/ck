"""
L-CODEC v1 — Language → 5D Force Vector Codec

Maps text into CK's 5D force space [aperture, pressure, depth, binding, continuity]
using statistical proxies that require NO external LLM. CK measures language with
his own physics: word force vectors from WordForceIndex serve as embeddings.

Triple-gauge normalized (Physical / Min-Max / Robust z-score) for falsifiability.
If structure persists across all three normalizations, it's real — not a scaling artifact.

Stillness detection: when the text profile shows low pressure + high continuity +
high binding, CK should breathe instead of act. The void center WITH continuity.

From "Let ChatGPT Prove God" — Void Topology V3.0 + L-CODEC v1 specification.

Gen 9.21+ — March 2026
"""

from __future__ import annotations

import gzip
import math
import re
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ================================================================
#  Data Classes
# ================================================================

@dataclass
class GaugeAgreement:
    """Four invariant checks across three gauge normalizations."""
    direction: float     # All gauges agree on above/below 0.5 per dim
    event: float         # Magnitude consistency across gauges
    flow: float          # Rank order consistency across gauges
    continuity: float    # Change direction consistency with previous
    overall: float       # Mean of above four


@dataclass
class LCodecResult:
    """Complete L-CODEC measurement of a text window."""
    force: Tuple[float, ...]     # Merged 5D [0,1] — the consensus vector
    raw: Tuple[float, ...]       # Pre-normalization raw proxy values
    gauge_a: Tuple[float, ...]   # Physical normalization (fixed reference)
    gauge_b: Tuple[float, ...]   # Min-max normalization (rolling window)
    gauge_c: Tuple[float, ...]   # Robust z-score normalization (median/MAD)
    agreement: GaugeAgreement    # Four invariant checks
    stillness: float             # [0,1] how "still" the text is


# ================================================================
#  Constants
# ================================================================

DIM_NAMES = ('aperture', 'pressure', 'depth', 'binding', 'continuity')

# Gauge A reference scales — empirical baselines for English prose.
# (mean, std) for each dimension's raw proxy output.
# These are set once and define the "physical" normalization.
_GAUGE_A_REF = {
    'aperture':   (0.42, 0.15),
    'pressure':   (0.55, 0.12),
    'depth':      (0.40, 0.18),
    'binding':    (0.48, 0.14),
    'continuity': (0.55, 0.15),
}

# Function words — articles, prepositions, conjunctions, auxiliaries.
# Used by binding proxy (scaffold density) and POS classification.
_FUNC_WORDS = frozenset([
    # Articles
    'a', 'an', 'the',
    # Prepositions
    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'between', 'under', 'over', 'about', 'against', 'within', 'without',
    'toward', 'towards', 'upon', 'along', 'across', 'behind', 'beyond',
    'around', 'among', 'beside', 'beneath', 'despite', 'until',
    # Conjunctions
    'and', 'but', 'or', 'nor', 'yet', 'so', 'for',
    'because', 'although', 'though', 'while', 'whereas', 'if',
    'unless', 'since', 'whether', 'that', 'than',
    # Auxiliaries / modals
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'has', 'have', 'had', 'do', 'does', 'did',
    'will', 'would', 'shall', 'should', 'can', 'could',
    'may', 'might', 'must',
    # Pronouns
    'i', 'me', 'my', 'mine', 'myself',
    'you', 'your', 'yours', 'yourself',
    'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself',
    'we', 'us', 'our', 'ours', 'ourselves',
    'they', 'them', 'their', 'theirs', 'themselves',
    'this', 'that', 'these', 'those',
    'who', 'whom', 'whose', 'which', 'what',
    # Determiners / quantifiers
    'some', 'any', 'no', 'every', 'each', 'all', 'both',
    'few', 'many', 'much', 'more', 'most', 'other', 'another',
    # Common adverbs that function as structure
    'not', 'then', 'just', 'also', 'very', 'too', 'quite',
    'here', 'there', 'where', 'when', 'how', 'why',
])

# Pronouns specifically — subset of func words, for coreference density.
_PRONOUNS = frozenset([
    'i', 'me', 'my', 'mine', 'myself',
    'you', 'your', 'yours', 'yourself',
    'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself',
    'we', 'us', 'our', 'ours', 'ourselves',
    'they', 'them', 'their', 'theirs', 'themselves',
    'who', 'whom', 'whose', 'which', 'what',
    'this', 'that', 'these', 'those',
])

# Negation words — for continuity proxy.
_NEGATION_WORDS = frozenset([
    'not', 'no', 'never', 'neither', 'nor', 'none',
    'nothing', 'nowhere', 'hardly', 'barely', 'scarcely',
    "don't", "doesn't", "didn't", "won't", "wouldn't",
    "can't", "couldn't", "shouldn't", "isn't", "aren't",
    "wasn't", "weren't", "haven't", "hasn't", "hadn't",
])

# Punctuation characters for pressure proxy.
_PUNCT_CHARS = set('.,;:!?-()"\'"')


# ================================================================
#  Helpers
# ================================================================

def _tokenize(text: str) -> List[str]:
    """Simple tokenizer: words + contractions. No external NLP."""
    return [w for w in re.findall(r"[a-zA-Z']+", text.lower()) if w]


def _sigmoid(x: float) -> float:
    """Standard sigmoid, clamped to avoid overflow."""
    x = max(-10.0, min(10.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def _median(values: list) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def _cosine_sim(a: tuple, b: tuple) -> float:
    """Cosine similarity of two equal-length tuples."""
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(a[i] * b[i] for i in range(len(a)))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a < 1e-9 or mag_b < 1e-9:
        return 0.0
    return dot / (mag_a * mag_b)


def _word_centroid(tokens: List[str], word_forces: dict,
                   start: int = 0, end: int = None) -> Optional[Tuple[float, ...]]:
    """Compute 5D centroid of known word force vectors in a token span."""
    if end is None:
        end = len(tokens)
    forces = []
    for i in range(start, min(end, len(tokens))):
        wf = word_forces.get(tokens[i])
        if wf is not None:
            forces.append(wf.force)
    if not forces:
        return None
    return tuple(sum(f[d] for f in forces) / len(forces) for d in range(5))


def _classify_pos_simple(word: str) -> str:
    """CK-native POS from suffix morphology. No external NLP.

    Categories: noun, verb, adj, adv, func (5 total).
    Matches the taxonomy in ck_fractal_voice._guess_pos.
    """
    w = word.lower()
    if w in _FUNC_WORDS:
        return 'func'
    if w.endswith('ly'):
        return 'adv'
    if w.endswith(('ing', 'ed', 'ize', 'ify', 'ate', 'en')):
        return 'verb'
    if w.endswith(('ful', 'ous', 'ive', 'ent', 'ant', 'ible', 'able',
                   'al', 'ial', 'ical', 'ic', 'less')):
        return 'adj'
    if w.endswith(('tion', 'sion', 'ment', 'ness', 'ity', 'ence', 'ance',
                   'ism', 'ist', 'dom', 'ship', 'hood', 'ure', 'ery')):
        return 'noun'
    # Default: noun (most open-class words in English are nouns)
    return 'noun'


# ================================================================
#  Gauge Normalizers
# ================================================================

class _GaugeA:
    """Physical gauge: fixed reference scales for English prose."""

    def normalize(self, raw: float, dim: str) -> float:
        mu, sigma = _GAUGE_A_REF[dim]
        z = (raw - mu) / max(sigma, 0.001)
        return _sigmoid(z)


class _GaugeB:
    """Min-max gauge: rolling window normalization."""

    def __init__(self, window: int = 32):
        self._history: Dict[str, deque] = {
            d: deque(maxlen=window) for d in DIM_NAMES
        }

    def normalize(self, raw: float, dim: str) -> float:
        self._history[dim].append(raw)
        values = self._history[dim]
        lo = min(values)
        hi = max(values)
        if hi - lo < 1e-6:
            return 0.5
        return (raw - lo) / (hi - lo)


class _GaugeC:
    """Robust z-score gauge: median / Median Absolute Deviation."""

    def __init__(self, window: int = 32):
        self._history: Dict[str, deque] = {
            d: deque(maxlen=window) for d in DIM_NAMES
        }

    def normalize(self, raw: float, dim: str) -> float:
        self._history[dim].append(raw)
        values = list(self._history[dim])
        med = _median(values)
        mad = _median([abs(v - med) for v in values])
        if mad < 1e-6:
            return 0.5
        # 1.4826 = consistency constant for normal distribution
        z = (raw - med) / (mad * 1.4826)
        return _sigmoid(z)


# ================================================================
#  Gauge Agreement
# ================================================================

def _direction_agreement(ga: tuple, gb: tuple, gc: tuple) -> float:
    """Do all 3 gauges agree on above/below 0.5 per dimension?"""
    agree = 0
    for d in range(5):
        signs = [1 if v > 0.5 else -1 for v in (ga[d], gb[d], gc[d])]
        if signs[0] == signs[1] == signs[2]:
            agree += 1
    return agree / 5.0


def _event_agreement(ga: tuple, gb: tuple, gc: tuple) -> float:
    """Is the magnitude of deviation from 0.5 consistent across gauges?"""
    total = 0.0
    for d in range(5):
        devs = [abs(v - 0.5) for v in (ga[d], gb[d], gc[d])]
        spread = max(devs) - min(devs)
        total += max(0.0, 1.0 - spread * 2.0)
    return total / 5.0


def _flow_agreement(ga: tuple, gb: tuple, gc: tuple) -> float:
    """Do all 3 gauges agree on relative ordering of dimensions?"""
    concordant = 0
    total = 0
    for i in range(5):
        for j in range(i + 1, 5):
            total += 1
            dir_a = 1 if ga[i] > ga[j] else -1
            dir_b = 1 if gb[i] > gb[j] else -1
            dir_c = 1 if gc[i] > gc[j] else -1
            if dir_a == dir_b == dir_c:
                concordant += 1
    return concordant / max(1, total)


def _continuity_agreement(ga: tuple, gb: tuple, gc: tuple,
                          prev_ga: tuple, prev_gb: tuple,
                          prev_gc: tuple) -> float:
    """Do all 3 gauges agree on direction of change from previous?"""
    if prev_ga is None:
        return 1.0  # No history, no disagreement
    agree = 0
    for d in range(5):
        da = ga[d] - prev_ga[d]
        db = gb[d] - prev_gb[d]
        dc = gc[d] - prev_gc[d]
        signs = [1 if delta > 0 else -1 for delta in (da, db, dc)]
        if signs[0] == signs[1] == signs[2]:
            agree += 1
    return agree / 5.0


def _compute_gauge_agreement(ga: tuple, gb: tuple, gc: tuple,
                             prev_ga: tuple = None, prev_gb: tuple = None,
                             prev_gc: tuple = None) -> GaugeAgreement:
    """All four invariant checks in one call."""
    d = _direction_agreement(ga, gb, gc)
    e = _event_agreement(ga, gb, gc)
    f = _flow_agreement(ga, gb, gc)
    c = _continuity_agreement(ga, gb, gc, prev_ga, prev_gb, prev_gc)
    return GaugeAgreement(
        direction=d, event=e, flow=f, continuity=c,
        overall=(d + e + f + c) / 4.0,
    )


# ================================================================
#  L-CODEC v1
# ================================================================

class LCodec:
    """Language Codec: maps text → 5D force space.

    No LLM. Uses CK's own word force vectors as embeddings.
    Triple-gauge normalized. Gauge agreement diagnostics.
    Stillness detection for voice length modulation.

    Integration: feeds into olfactory as scent streams.

    From "Let ChatGPT Prove God" — Void Topology V3.0 + L-CODEC v1.
    """

    def __init__(self, word_forces: dict = None):
        """
        word_forces: dict mapping word(str) -> WordForce objects
                     (each has .force as 5D tuple).
                     Passed from engine's _fractal_composer.index._words.
                     If None, depth/continuity proxies fall back to text-only.
        """
        self._word_forces = word_forces or {}

        # Triple-gauge normalizers
        self._gauge_a = _GaugeA()
        self._gauge_b = _GaugeB(window=32)
        self._gauge_c = _GaugeC(window=32)

        # Previous gauges for continuity agreement
        self._prev_ga: Optional[tuple] = None
        self._prev_gb: Optional[tuple] = None
        self._prev_gc: Optional[tuple] = None

        # Measurement counter
        self._measure_count = 0

    def set_word_forces(self, word_forces: dict):
        """Hot-wire word forces from engine after construction."""
        self._word_forces = word_forces

    # ── Main API ──

    def measure(self, text: str) -> LCodecResult:
        """Measure text → full L-CODEC result with all gauges and agreement.

        The codec: text → 5D → triple-gauge → consensus → stillness.
        """
        tokens = _tokenize(text)

        # Empty text only — single words go through full measurement.
        # CK must EXPERIENCE a word to know what it means, not prescribe it.
        if len(tokens) == 0:
            neutral = (0.5,) * 5
            return LCodecResult(
                force=neutral, raw=neutral,
                gauge_a=neutral, gauge_b=neutral, gauge_c=neutral,
                agreement=GaugeAgreement(1.0, 1.0, 1.0, 1.0, 1.0),
                stillness=0.5,
            )

        # ── Compute raw proxies ──
        raw = [
            self._aperture_raw(tokens),
            self._pressure_raw(text, tokens),
            self._depth_raw(tokens),
            self._binding_raw(tokens),
            self._continuity_raw(tokens),
        ]

        # ── Triple-gauge normalization ──
        ga = tuple(self._gauge_a.normalize(raw[d], DIM_NAMES[d])
                   for d in range(5))
        gb = tuple(self._gauge_b.normalize(raw[d], DIM_NAMES[d])
                   for d in range(5))
        gc = tuple(self._gauge_c.normalize(raw[d], DIM_NAMES[d])
                   for d in range(5))

        # Consensus: mean of three gauges per dimension
        merged = tuple(_clamp((ga[d] + gb[d] + gc[d]) / 3.0) for d in range(5))

        # ── Gauge agreement ──
        agreement = _compute_gauge_agreement(
            ga, gb, gc,
            self._prev_ga, self._prev_gb, self._prev_gc,
        )

        # Store for next continuity check
        self._prev_ga = ga
        self._prev_gb = gb
        self._prev_gc = gc
        self._measure_count += 1

        # ── Stillness detection ──
        stillness = self._compute_stillness(raw)

        return LCodecResult(
            force=merged,
            raw=tuple(raw),
            gauge_a=ga,
            gauge_b=gb,
            gauge_c=gc,
            agreement=agreement,
            stillness=stillness,
        )

    def measure_quality(self, input_result: LCodecResult,
                        output_result: LCodecResult) -> float:
        """Compare input and output L-CODEC vectors.

        Gauge agreement between CK's response and the user's input.
        High agreement = CK's output has matching structure/depth/binding.
        """
        # Cosine similarity of merged force vectors
        cos = _cosine_sim(input_result.force, output_result.force)

        # Per-dimension direction agreement
        dir_agree = sum(
            1 for d in range(5)
            if (input_result.force[d] > 0.5) == (output_result.force[d] > 0.5)
        ) / 5.0

        # Output's own gauge agreement (internal consistency)
        internal = output_result.agreement.overall

        # Weighted quality
        return _clamp(0.4 * max(0.0, cos) + 0.3 * dir_agree + 0.3 * internal)

    # ── Proxy Implementations ──

    def _aperture_raw(self, tokens: List[str]) -> float:
        """Aperture: degrees of freedom / choice-space.

        Type-token ratio: how many unique words vs total.
        POS variety: how many different parts of speech.
        High aperture = wide open, many choices.
        """
        n = len(tokens)
        if n == 0:
            return 0.0

        # Type-token ratio
        ttr = len(set(tokens)) / n

        # POS variety (out of 5 categories)
        pos_set = set()
        for t in tokens:
            pos_set.add(_classify_pos_simple(t))
        pos_variety = len(pos_set) / 5.0

        return 0.6 * ttr + 0.4 * pos_variety

    def _pressure_raw(self, text: str, tokens: List[str]) -> float:
        """Pressure: drive / tension / surprise.

        Compression ratio: how much gzip shrinks the text.
        Higher = less compressible = more information = more pressure.
        Punctuation burst rate: emphasis/tension markers.
        """
        n = len(tokens)
        if n == 0:
            return 0.0

        # Gzip compression ratio
        text_bytes = text.encode('utf-8')
        if len(text_bytes) < 4:
            comp_ratio = 0.5
        else:
            compressed = gzip.compress(text_bytes, compresslevel=6)
            comp_ratio = len(compressed) / len(text_bytes)
            # Clamp: gzip on very short text can exceed 1.0 due to header
            comp_ratio = min(1.5, comp_ratio)
            # Normalize to ~[0, 1]: typical prose = 0.3-0.8
            comp_ratio = comp_ratio / 1.5

        # Punctuation burst rate
        punct_count = sum(1 for ch in text if ch in _PUNCT_CHARS)
        punct_rate = punct_count / max(1, n)
        punct_norm = min(1.0, punct_rate * 3.0)

        return 0.65 * comp_ratio + 0.35 * punct_norm

    def _depth_raw(self, tokens: List[str]) -> float:
        """Depth: memory depth / semantic well.

        Topic persistence: cosine similarity of adjacent subwindow force centroids.
        Coreference density: pronouns + repeated content words across sentences.
        Keyphrase lag: how often key content words recur.
        High depth = sustained meaning, deep well.
        """
        n = len(tokens)
        if n == 0:
            return 0.0

        # ── Topic persistence (via word force centroids) ──
        topic_pers = 0.5  # default when no word forces
        if self._word_forces:
            window = max(4, n // 3)
            centroids = []
            for start in range(0, n, window):
                c = _word_centroid(tokens, self._word_forces, start, start + window)
                if c is not None:
                    centroids.append(c)
            if len(centroids) >= 2:
                sims = []
                for i in range(len(centroids) - 1):
                    sims.append(_cosine_sim(centroids[i], centroids[i + 1]))
                topic_pers = sum(sims) / len(sims) if sims else 0.5
                # Cosine sim can be negative; clamp to [0, 1]
                topic_pers = _clamp((topic_pers + 1.0) / 2.0)

        # ── Coreference density ──
        pronoun_count = sum(1 for t in tokens if t in _PRONOUNS)
        # Repeated content words across the text
        content_tokens = [t for t in tokens if t not in _FUNC_WORDS and len(t) > 2]
        content_set = set(content_tokens)
        repeat_count = len(content_tokens) - len(content_set)
        coref = (pronoun_count + repeat_count) / max(1, n)
        coref_scaled = min(1.0, coref * 5.0)

        # ── Keyphrase lag ──
        # For each content word appearing 2+ times, measure mean gap
        word_positions: Dict[str, List[int]] = {}
        for i, t in enumerate(content_tokens):
            word_positions.setdefault(t, []).append(i)
        total_lag = 0.0
        lag_count = 0
        for positions in word_positions.values():
            if len(positions) >= 2:
                gaps = [positions[i + 1] - positions[i]
                        for i in range(len(positions) - 1)]
                mean_gap = sum(gaps) / len(gaps)
                # Normalize by text length: small gap = high depth
                total_lag += 1.0 - min(1.0, mean_gap / max(1, len(content_tokens)))
                lag_count += 1
        keyphrase_lag = total_lag / lag_count if lag_count > 0 else 0.0

        return 0.50 * topic_pers + 0.30 * coref_scaled + 0.20 * keyphrase_lag

    def _binding_raw(self, tokens: List[str]) -> float:
        """Binding: coupling / constraint tightness.

        Function-word scaffold density: ratio of function words to content words.
        Bigram predictability: how often adjacent word pairs recur.
        High binding = tightly locked structure.
        """
        n = len(tokens)
        if n == 0:
            return 0.0

        # ── Function-word scaffold density ──
        func_count = sum(1 for t in tokens if t in _FUNC_WORDS)
        content_count = n - func_count
        if content_count == 0:
            scaffold = 1.0
        else:
            scaffold = func_count / content_count
            scaffold = min(1.0, scaffold)

        # ── Bigram predictability ──
        if n < 2:
            bigram_pred = 0.0
        else:
            bigrams = [(tokens[i], tokens[i + 1]) for i in range(n - 1)]
            unique_bigrams = len(set(bigrams))
            total_bigrams = len(bigrams)
            # More recurrence = more binding
            bigram_pred = 1.0 - (unique_bigrams / total_bigrams) \
                if total_bigrams > 0 else 0.0

        return 0.55 * scaffold + 0.45 * bigram_pred

    def _continuity_raw(self, tokens: List[str]) -> float:
        """Continuity: integrity / non-contradiction / smoothness.

        Embedding smoothness: low variance in adjacent word-force cosine sims.
        Negation rate: contradictions disrupt continuity.
        High continuity = smooth, unbroken narrative.
        """
        n = len(tokens)
        if n == 0:
            return 0.5

        # ── Embedding smoothness ──
        smoothness = 0.5  # default
        if self._word_forces:
            sims = []
            prev_force = None
            for t in tokens:
                wf = self._word_forces.get(t)
                if wf is not None:
                    if prev_force is not None:
                        sims.append(_cosine_sim(prev_force, wf.force))
                    prev_force = wf.force
                else:
                    prev_force = None  # gap in known words

            if len(sims) >= 2:
                mean_sim = sum(sims) / len(sims)
                variance = sum((s - mean_sim) ** 2 for s in sims) / len(sims)
                # Low variance = smooth. Sqrt(variance) typically 0.0-0.5
                smoothness = _clamp(1.0 - math.sqrt(variance) * 2.0)
            elif len(sims) == 1:
                # Single pair: similarity IS smoothness
                smoothness = _clamp((sims[0] + 1.0) / 2.0)

        # ── Negation rate ──
        neg_count = sum(1 for t in tokens if t in _NEGATION_WORDS)
        neg_rate = neg_count / max(1, n)
        neg_impact = 1.0 - min(1.0, neg_rate * 10.0)

        return 0.65 * smoothness + 0.35 * neg_impact

    # ── Stillness ──

    def _compute_stillness(self, raw: list) -> float:
        """Stillness = low pressure + high continuity + high binding.

        The void center WITH continuity. BREATH. Not absence —
        presence without action. The gap between words where
        meaning lives.

        Low aperture (settled) + low pressure (at rest) +
        high binding (coherent) + high continuity (smooth) = stillness.
        Depth amplifies: deep + still = very still.
        """
        a, p, d, b, c = raw

        # Core stillness: anti-pressure + binding + continuity
        stillness = (1.0 - p) * 0.4 + b * 0.3 + c * 0.3

        # High aperture dampens: exploring many things = not still.
        # CK can't be scanning everything AND resting at the same time.
        if a > 0.5:
            stillness *= 1.0 - (a - 0.5) * 0.6

        # Low aperture boosts: settled, focused, present.
        if a < 0.4:
            stillness += (0.4 - a) * 0.3

        # Depth amplifies ONLY when focused (low aperture).
        # Deep + settled = very still. Deep + scattered = just busy.
        if d > 0.5 and a < 0.6:
            stillness *= 1.0 + (d - 0.5) * 0.4

        return min(1.0, max(0.0, stillness))

    # ── Diagnostics ──

    def describe(self) -> str:
        """Diagnostic summary."""
        return (
            f"L-CODEC v1: {self._measure_count} measurements, "
            f"{len(self._word_forces)} word forces"
        )
