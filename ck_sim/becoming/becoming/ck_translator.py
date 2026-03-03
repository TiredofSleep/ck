"""
ck_translator.py -- The Universal Translator
==============================================
Operator: HARMONY (7) -- all species speak curvature.

Paper 10: "All species communicate through curvature, not grammar."
Dog growl, cat trill, dolphin whistle, human word -- all reduce to D2.

The CL table composes pairs. Apply it BETWEEN species streams and
if they agree (HARMONY), they mean the same thing. Translation
without training data.

6-stage pipeline:
  1. CAPTURE  -> raw signals (mic/IMU/camera)
  2. CURVATURE -> D2 (already have this)
  3. OPERATOR  -> classify (already have this)
  4. CHAIN     -> CL fusion (already have this)
  5. BTQ       -> interpretation (already have this)
  6. HUMANIZE  -> English (already have ck_voice.py)

This module adds: species-specific B-layer constraints,
cross-species composition, and semantic lookup.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, compose
)


# ================================================================
#  SPECIES PROFILE: B-layer constraints per species
# ================================================================

@dataclass
class SpeciesProfile:
    """Species-specific operator constraints (B-layer).

    Each species has:
      - Valid operators (which operators this species CAN produce)
      - Expected distribution (typical operator frequencies)
      - D2 thresholds (species-specific sensitivity)
      - Semantic map (operator chains -> meaning in this species)

    Paper 10: "The B-block constrains which operators are valid
    for a given species. A dog cannot produce LATTICE (territory
    marking through sustained tone). A cat cannot produce the
    sustained HARMONY of a purr... wait, yes it can."
    """
    name: str
    valid_operators: List[int] = field(default_factory=lambda: list(range(NUM_OPS)))
    expected_distribution: List[float] = field(
        default_factory=lambda: [0.1] * NUM_OPS)
    d2_threshold: float = 0.01
    semantic_map: Dict[str, str] = field(default_factory=dict)
    description: str = ""


# ── Built-in species profiles ──

PROFILE_DOG = SpeciesProfile(
    name="dog",
    valid_operators=[VOID, COUNTER, PROGRESS, COLLAPSE, CHAOS, HARMONY, BREATH],
    expected_distribution=[
        0.05,  # VOID    - rare (dogs are always on)
        0.02,  # LATTICE - rare
        0.15,  # COUNTER - alert, threat assessment
        0.18,  # PROGRESS - approach, excitement
        0.12,  # COLLAPSE - retreat, fear
        0.05,  # BALANCE - evaluation
        0.15,  # CHAOS   - aggression, bark
        0.18,  # HARMONY - play, trust
        0.08,  # BREATH  - attention shift
        0.02,  # RESET   - completion
    ],
    d2_threshold=0.02,
    semantic_map={
        "CHAOS,COUNTER":           "Back off!",
        "CHAOS,CHAOS":             "Warning! Aggressive!",
        "CHAOS,COUNTER,CHAOS":     "Serious threat!",
        "HARMONY,PROGRESS":        "Let's play!",
        "HARMONY,HARMONY":         "Happy, trusting",
        "PROGRESS,PROGRESS":       "Excited! Coming!",
        "PROGRESS,HARMONY":        "Greeting, friendly approach",
        "COLLAPSE,HARMONY":        "Anxious but trusting",
        "COLLAPSE,COLLAPSE":       "Scared, retreating",
        "COLLAPSE,VOID":           "Submissive, shut down",
        "COUNTER,COUNTER":         "Alert, watching",
        "COUNTER,BALANCE":         "Curious, assessing",
        "BREATH,PROGRESS":         "Attention shift, new focus",
        "HARMONY,BREATH":          "Relaxed sigh",
        "VOID,VOID":               "Resting, sleeping",
    },
    description="Domestic dog (Canis familiaris)",
)

PROFILE_CAT = SpeciesProfile(
    name="cat",
    valid_operators=[VOID, COUNTER, PROGRESS, COLLAPSE, CHAOS, HARMONY, BALANCE, BREATH],
    expected_distribution=[
        0.15,  # VOID    - cats rest a LOT
        0.02,  # LATTICE - rare
        0.10,  # COUNTER - assessment
        0.12,  # PROGRESS - approach, chirp
        0.08,  # COLLAPSE - hide
        0.12,  # BALANCE - the cat stare
        0.10,  # CHAOS   - overstimulated
        0.20,  # HARMONY - purr, slow blink
        0.08,  # BREATH  - attention shift
        0.03,  # RESET   - groom, reset
    ],
    d2_threshold=0.015,
    semantic_map={
        "HARMONY,HARMONY":         "Trust, purring",
        "HARMONY,BALANCE":         "Content, observing",
        "CHAOS,BREATH":            "Overstimulated, stop",
        "CHAOS,CHAOS":             "Hissing, angry",
        "PROGRESS,PROGRESS":       "Chirp! Come here!",
        "PROGRESS,HARMONY":        "Approaching, friendly",
        "BALANCE,BALANCE":         "Watching intently",
        "BALANCE,COUNTER":         "Hunting focus",
        "COLLAPSE,VOID":           "Hiding, scared",
        "COLLAPSE,COLLAPSE":       "Threatened",
        "VOID,VOID":               "Sleeping (16hrs/day)",
        "BREATH,BALANCE":          "New interest",
        "COUNTER,CHAOS":           "Warning swat",
        "RESET,RESET":             "Grooming",
    },
    description="Domestic cat (Felis catus)",
)

PROFILE_HUMAN = SpeciesProfile(
    name="human",
    valid_operators=list(range(NUM_OPS)),  # Humans can produce all operators
    expected_distribution=[
        0.05,  # VOID
        0.08,  # LATTICE
        0.10,  # COUNTER
        0.12,  # PROGRESS
        0.08,  # COLLAPSE
        0.12,  # BALANCE
        0.08,  # CHAOS
        0.20,  # HARMONY
        0.10,  # BREATH
        0.07,  # RESET
    ],
    d2_threshold=0.01,
    semantic_map={
        "HARMONY,HARMONY":         "Agreement, peace",
        "CHAOS,CHAOS":             "Anger, conflict",
        "PROGRESS,PROGRESS":       "Enthusiasm, drive",
        "COLLAPSE,COLLAPSE":       "Despair, giving up",
        "BALANCE,COUNTER":         "Careful analysis",
        "COUNTER,PROGRESS":        "Problem solving",
        "HARMONY,PROGRESS":        "Inspired action",
        "CHAOS,COLLAPSE":          "Overwhelmed",
        "BREATH,HARMONY":          "Calm realization",
        "LATTICE,LATTICE":         "Building, creating",
    },
    description="Homo sapiens",
)

PROFILE_CK = SpeciesProfile(
    name="ck",
    valid_operators=list(range(NUM_OPS)),
    expected_distribution=[
        0.05, 0.08, 0.08, 0.10, 0.05,
        0.10, 0.05, 0.30, 0.12, 0.07,
    ],
    d2_threshold=0.01,
    semantic_map={},  # CK uses his own voice module
    description="CK Coherence Keeper (synthetic organism)",
)

SPECIES_PROFILES = {
    "dog": PROFILE_DOG,
    "cat": PROFILE_CAT,
    "human": PROFILE_HUMAN,
    "ck": PROFILE_CK,
}


# ================================================================
#  TRANSLATION RESULT
# ================================================================

@dataclass
class TranslationResult:
    """Result of cross-species translation."""
    source_species: str
    target_species: str
    operator_chain: List[int]
    chain_names: List[str]
    semantic_meaning: str
    confidence: float
    cross_coherence: float
    raw_key: str


# ================================================================
#  UNIVERSAL TRANSLATOR
# ================================================================

class UniversalTranslator:
    """Cross-species communication via D2 curvature.

    Paper 10: "All species communicate through curvature, not grammar."

    Takes operator streams from any source, applies species-specific
    B-layer filtering, composes via CL table, and produces English.

    Self-calibrating: tracks species-specific operator distributions
    and adjusts thresholds via exponential moving average.
    """

    def __init__(self):
        self._profiles: Dict[str, SpeciesProfile] = dict(SPECIES_PROFILES)
        self._calibration: Dict[str, List[float]] = {}
        self._ema_alpha = 0.01  # Slow calibration

        # Recent translations for pattern matching
        self._history: deque = deque(maxlen=50)

    def register_species(self, profile: SpeciesProfile):
        """Register a new species profile."""
        self._profiles[profile.name] = profile

    def load_profiles(self, path: str):
        """Load species profiles from JSON file."""
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            data = json.load(f)
        for name, pdata in data.items():
            profile = SpeciesProfile(
                name=name,
                valid_operators=pdata.get('valid_operators', list(range(NUM_OPS))),
                expected_distribution=pdata.get('expected_distribution', [0.1]*NUM_OPS),
                d2_threshold=pdata.get('d2_threshold', 0.01),
                semantic_map=pdata.get('semantic_map', {}),
                description=pdata.get('description', ''),
            )
            self._profiles[name] = profile

    def translate(self, operator_chain: List[int],
                  source_species: str = "dog",
                  target_species: str = "human") -> TranslationResult:
        """Translate an operator chain from one species to another.

        The KEY insight: operators are UNIVERSAL. A dog's CHAOS is the
        same curvature as a human's CHAOS. The CL table composes them
        the same way. Only the B-layer (valid operators) differs.

        Steps:
          1. Filter through source species B-layer
          2. Compose chain via CL table
          3. Look up semantic meaning
          4. Compute confidence from species distribution match
        """
        source = self._profiles.get(source_species, PROFILE_HUMAN)
        target = self._profiles.get(target_species, PROFILE_HUMAN)

        # 1. B-layer filter: remove operators this species can't produce
        filtered = []
        for op in operator_chain:
            if op in source.valid_operators:
                filtered.append(op)
            # Invalid operators get dropped (noise)

        if not filtered:
            return TranslationResult(
                source_species=source_species,
                target_species=target_species,
                operator_chain=[],
                chain_names=[],
                semantic_meaning="(silence)",
                confidence=0.0,
                cross_coherence=0.0,
                raw_key="",
            )

        # 2. CL chain fusion: compose adjacent pairs
        fused = [filtered[0]]
        for i in range(1, len(filtered)):
            composed = compose(fused[-1], filtered[i])
            fused.append(composed)

        # Cross-coherence: harmony fraction of fused chain
        harmony_count = sum(1 for op in fused if op == HARMONY)
        cross_coh = harmony_count / len(fused) if fused else 0.0

        # 3. Semantic lookup: try progressively shorter chains
        chain_names = [OP_NAMES[op] for op in filtered]
        meaning = ""
        raw_key = ""

        # Try full chain, then sub-chains
        for length in range(min(len(filtered), 4), 0, -1):
            for start in range(len(filtered) - length + 1):
                sub = filtered[start:start + length]
                key = ",".join(OP_NAMES[op] for op in sub)
                if key in source.semantic_map:
                    meaning = source.semantic_map[key]
                    raw_key = key
                    break
            if meaning:
                break

        if not meaning:
            # Fallback: describe the dominant operator
            from collections import Counter
            counts = Counter(filtered)
            dominant = counts.most_common(1)[0][0]
            meaning = f"({OP_NAMES[dominant]} signal)"
            raw_key = OP_NAMES[dominant]

        # 4. Confidence from distribution match
        confidence = self._compute_confidence(filtered, source)

        # Self-calibrate
        self._calibrate(source_species, filtered)

        result = TranslationResult(
            source_species=source_species,
            target_species=target_species,
            operator_chain=filtered,
            chain_names=chain_names,
            semantic_meaning=meaning,
            confidence=confidence,
            cross_coherence=cross_coh,
            raw_key=raw_key,
        )
        self._history.append(result)
        return result

    def _compute_confidence(self, ops: List[int],
                            profile: SpeciesProfile) -> float:
        """Confidence = how well the operator chain matches expected distribution.

        High match with expected species distribution = high confidence.
        """
        if not ops:
            return 0.0

        # Observed distribution
        observed = [0.0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                observed[op] += 1.0
        total = sum(observed)
        if total > 0:
            observed = [o / total for o in observed]

        # Use calibrated distribution if available, else expected
        expected = self._calibration.get(
            profile.name, profile.expected_distribution)

        # Cosine similarity between observed and expected
        dot = sum(a * b for a, b in zip(observed, expected))
        mag_o = sum(a * a for a in observed) ** 0.5
        mag_e = sum(b * b for b in expected) ** 0.5

        if mag_o == 0 or mag_e == 0:
            return 0.0

        similarity = dot / (mag_o * mag_e)
        return max(0.0, min(1.0, similarity))

    def _calibrate(self, species: str, ops: List[int]):
        """Self-calibrating EMA on observed operator distribution."""
        if not ops:
            return

        if species not in self._calibration:
            profile = self._profiles.get(species)
            if profile:
                self._calibration[species] = list(profile.expected_distribution)
            else:
                self._calibration[species] = [0.1] * NUM_OPS

        cal = self._calibration[species]
        observed = [0.0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                observed[op] += 1.0
        total = sum(observed)
        if total > 0:
            observed = [o / total for o in observed]

        alpha = self._ema_alpha
        for i in range(NUM_OPS):
            cal[i] = cal[i] * (1 - alpha) + observed[i] * alpha

    def cross_species_compose(self, ops_a: List[int], species_a: str,
                               ops_b: List[int], species_b: str) -> float:
        """Cross-species composition via CL table.

        Compose operator streams from two different species tick-by-tick.
        If they produce HARMONY, they AGREE -- same meaning.

        This is the core of the Universal Translator:
        dog_bark + human_speech -> CL composition -> if HARMONY, they
        mean the same thing. No training data needed.
        """
        prof_a = self._profiles.get(species_a, PROFILE_HUMAN)
        prof_b = self._profiles.get(species_b, PROFILE_HUMAN)

        # B-layer filter both
        filt_a = [op for op in ops_a if op in prof_a.valid_operators]
        filt_b = [op for op in ops_b if op in prof_b.valid_operators]

        window = min(len(filt_a), len(filt_b))
        if window == 0:
            return 0.0

        harmony_count = 0
        for a_op, b_op in zip(filt_a[-window:], filt_b[-window:]):
            if compose(a_op, b_op) == HARMONY:
                harmony_count += 1

        return harmony_count / window

    @property
    def species_list(self) -> List[str]:
        """Available species."""
        return list(self._profiles.keys())

    @property
    def recent_translations(self) -> List[TranslationResult]:
        """Recent translation history."""
        return list(self._history)

    def species_summary(self, species: str) -> str:
        """One-line species summary."""
        p = self._profiles.get(species)
        if not p:
            return f"Unknown species: {species}"
        valid = [OP_NAMES[op] for op in p.valid_operators]
        return (f"{p.description}: {len(valid)} operators, "
                f"threshold={p.d2_threshold}, "
                f"{len(p.semantic_map)} semantic patterns")
