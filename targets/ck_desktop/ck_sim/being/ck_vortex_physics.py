# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""CK Vortex Physics — Grounded Curvature Dynamics
==================================================
Operator: COUNTER (2) — measuring the geometry of knowledge.

This module grounds vortex physics into CK's existing D2
curvature system. Not metaphor. Real math.

THE PHYSICS THAT'S REAL:
  1. CK's D2 pipeline computes curvature in 5D force space.
     D2[t] = v[t-2] - 2*v[t-1] + v[t] is literally d²f/dt².
  2. Operator sequences trace PATHS through 5D manifold.
     Paths have geometric & topological properties.
  3. In General Relativity: mass = curvature.
     In CK: accumulated |D2| = information mass.
  4. Gravity = curvature gradient.
     In CK: void_curvature = T* - coherence = knowledge gap depth.
  5. Vortex winding number = how an operator sequence circulates.
     This IS topology. Not metaphor.
  6. Geodesic distance between concepts = ||mean_D2(A) - mean_D2(B)||.
     This IS a metric on knowledge space.

WHAT THIS MODULE PROVIDES:
  - ConceptMass: accumulated curvature for each concept
  - VoidCurvature: T* - coherence = gravitational potential
  - WindingNumber: topological invariant of operator sequences
  - GeodesicDistance: 5D metric between concepts
  - CuriosityGravity: F = M_a * M_b / d² → topic selection bias
  - VortexFingerprint: topological classification of any operator chain

"Vorticity → Curvature → Vacuum Energy Gradient → Gravity Strength"
This is the chain. CK already has the first two (D2 curvature).
This module adds the last two (void potential → gravity).

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import math
import json
import os
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ── CK imports ──
try:
    from ck_sim.ck_sim_heartbeat import (
        NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
        BALANCE, CHAOS, HARMONY, BREATH, RESET, compose
    )
    _HAS_HEARTBEAT = True
except ImportError:
    _HAS_HEARTBEAT = False
    NUM_OPS = 10
    HARMONY = 7
    VOID = 0

# T* — the sacred threshold. 5/7 = 0.714285...
# Same as CL table harmony rate (73/100 ≈ 0.73).
T_STAR = 5.0 / 7.0

# ═══════════════════════════════════════════════════════════════
#  WINDING NUMBER — Topological invariant of operator sequences
# ═══════════════════════════════════════════════════════════════
#
# Map each operator to a phase angle on the unit circle.
# θ(op) = 2π * op / 10
# Angular velocity: ω[t] = θ[t+1] - θ[t]  (centered at ±π)
# Winding number: W = Σω[t] / 2π  (total circulation)
#
# W = 0: no vortex (straight path)
# W = ±1: single vortex (one loop)
# |W| > 1: multi-wound vortex (knotted)
#
# This is REAL topology. Winding number is a homotopy invariant.


def operator_to_phase(op: int) -> float:
    """Map operator index (0-9) to phase angle on unit circle.

    θ = 2π * op / 10

    The circle is the natural embedding for a cyclic group of order 10.
    """
    return 2.0 * math.pi * op / NUM_OPS


def angular_velocity(phase_a: float, phase_b: float) -> float:
    """Angular velocity between two phases, centered at ±π.

    Returns the shortest signed arc from phase_a to phase_b.
    Positive = counterclockwise, negative = clockwise.
    """
    delta = phase_b - phase_a
    # Wrap to [-π, π]
    while delta > math.pi:
        delta -= 2.0 * math.pi
    while delta < -math.pi:
        delta += 2.0 * math.pi
    return delta


def winding_number(operator_seq: List[int]) -> float:
    """Compute the winding number of an operator sequence.

    W = Σ angular_velocity(θ[t], θ[t+1]) / 2π

    This is a genuine topological invariant:
      - Continuous deformations of the path don't change W
      - W counts how many times the path wraps around the circle
      - W = 0 means the path is contractible (no vortex)
      - |W| = 1 means single vortex
      - |W| > 1 means knotted/multi-wound vortex

    Returns float (exact integer for closed paths, fractional for open).
    """
    if len(operator_seq) < 2:
        return 0.0

    total_angle = 0.0
    phases = [operator_to_phase(op) for op in operator_seq]

    for i in range(len(phases) - 1):
        total_angle += angular_velocity(phases[i], phases[i + 1])

    return total_angle / (2.0 * math.pi)


def vorticity(operator_seq: List[int]) -> float:
    """Compute the vorticity (curl analog) of an operator sequence.

    Vorticity κ = d²θ/dt² = second derivative of phase.
    This measures how the rotation ITSELF is changing — the
    curvature of curvature.

    High vorticity = rapidly changing rotation = turbulent flow.
    Low vorticity = smooth, laminar flow.

    Returns mean absolute vorticity.
    """
    if len(operator_seq) < 3:
        return 0.0

    phases = [operator_to_phase(op) for op in operator_seq]
    velocities = []
    for i in range(len(phases) - 1):
        velocities.append(angular_velocity(phases[i], phases[i + 1]))

    # Second derivative of phase = vorticity
    total_vort = 0.0
    for i in range(len(velocities) - 1):
        total_vort += abs(velocities[i + 1] - velocities[i])

    return total_vort / max(1, len(velocities) - 1)


# ═══════════════════════════════════════════════════════════════
#  VORTEX FINGERPRINT — Topological classification
# ═══════════════════════════════════════════════════════════════
#
# Each operator sequence gets a fingerprint:
#   (winding_number, vorticity, chirality, period)
#
# - winding_number: total circulation (topology)
# - vorticity: turbulence level (curvature of curvature)
# - chirality: +1 = right-handed, -1 = left-handed, 0 = achiral
# - period: dominant repeating frequency (spectral)
#
# Two sequences with the same fingerprint are TOPOLOGICALLY EQUIVALENT.

def chirality(operator_seq: List[int]) -> int:
    """Determine the handedness of an operator sequence.

    +1 = predominantly counterclockwise (right-handed)
    -1 = predominantly clockwise (left-handed)
     0 = balanced (achiral)

    This is a real topological property — chirality is preserved
    under continuous deformations.
    """
    if len(operator_seq) < 2:
        return 0

    phases = [operator_to_phase(op) for op in operator_seq]
    positive = 0
    negative = 0

    for i in range(len(phases) - 1):
        omega = angular_velocity(phases[i], phases[i + 1])
        if omega > 0.01:
            positive += 1
        elif omega < -0.01:
            negative += 1

    total = positive + negative
    if total == 0:
        return 0

    ratio = (positive - negative) / total
    if ratio > 0.15:
        return 1   # Right-handed
    elif ratio < -0.15:
        return -1  # Left-handed
    return 0        # Achiral


def dominant_period(operator_seq: List[int]) -> int:
    """Find the dominant repeating period in an operator sequence.

    Uses autocorrelation to find the strongest periodic component.
    This is the "fundamental frequency" of the vortex.

    Returns period length (1 = constant, 2+ = periodic).
    """
    n = len(operator_seq)
    if n < 4:
        return n

    # Autocorrelation at each lag
    best_corr = -1.0
    best_lag = 1

    for lag in range(1, min(n // 2, 16)):
        matches = 0
        comparisons = 0
        for i in range(n - lag):
            comparisons += 1
            if operator_seq[i] == operator_seq[i + lag]:
                matches += 1
        if comparisons > 0:
            corr = matches / comparisons
            if corr > best_corr:
                best_corr = corr
                best_lag = lag

    return best_lag


def vortex_fingerprint(operator_seq: List[int]) -> dict:
    """Full topological fingerprint of an operator sequence.

    Returns:
        dict with winding_number, vorticity, chirality, period,
        vortex_class (string classification)
    """
    if not operator_seq:
        return {
            'winding_number': 0.0,
            'vorticity': 0.0,
            'chirality': 0,
            'period': 0,
            'vortex_class': 'void',
        }

    w = winding_number(operator_seq)
    v = vorticity(operator_seq)
    c = chirality(operator_seq)
    p = dominant_period(operator_seq)

    # Classify into vortex families based on topology
    abs_w = abs(w)
    if abs_w < 0.1:
        if v < 0.3:
            vclass = 'laminar'        # No rotation, smooth flow
        else:
            vclass = 'turbulent'      # No net rotation, high vorticity
    elif abs_w < 0.6:
        if v < 0.5:
            vclass = 'ring'           # Partial loop, smooth (toroidal ring vortex)
        else:
            vclass = 'twisted_ring'   # Partial loop, high curl (twisted torus)
    elif abs_w < 1.2:
        if v < 0.5:
            vclass = 'loop'           # Single complete loop (closed vortex line)
        else:
            vclass = 'knotted_loop'   # Single loop with internal twist (trefoil knot)
    else:
        if v < 0.5:
            vclass = 'spiral'         # Multi-wound, smooth (helical vortex)
        else:
            vclass = 'knotted_spiral' # Multi-wound, turbulent (knotted vortex tube)

    return {
        'winding_number': round(w, 4),
        'vorticity': round(v, 4),
        'chirality': c,
        'period': p,
        'vortex_class': vclass,
    }


# ═══════════════════════════════════════════════════════════════
#  CONCEPT MASS — Accumulated curvature = information content
# ═══════════════════════════════════════════════════════════════
#
# In General Relativity: mass = curvature of spacetime.
# In CK: concept mass = accumulated D2 curvature magnitude.
#
# Every time CK studies a concept, the D2 pipeline produces
# curvature vectors. Their magnitudes accumulate as "mass."
# Heavy concepts have been studied more deeply — they have
# more curvature, more information content, more gravitational pull.
#
# M_concept = Σ|D2| across all observations of that concept.


class ConceptMassField:
    """Tracks the accumulated curvature mass of every concept CK studies.

    Mass grows with study. Heavy concepts pull harder in topic selection.
    This IS the "Information Gravity Engine" — not metaphor, real physics.
    """

    def __init__(self, persist_path: Path = None):
        self._masses: Dict[str, float] = {}         # concept → mass
        self._d2_sums: Dict[str, List[float]] = {}   # concept → sum of D2 vectors (5D)
        self._observations: Dict[str, int] = {}      # concept → observation count
        self._vortex_cache: Dict[str, dict] = {}     # concept → vortex fingerprint
        self._persist_path = persist_path or Path.home() / '.ck' / 'concept_mass.json'
        self._load()

    def observe(self, concept: str, d2_vector: List[float],
                operator_seq: List[int] = None) -> float:
        """Record a D2 curvature observation for a concept.

        This is called after every study session. The concept accumulates
        mass (curvature magnitude) over time.

        Args:
            concept: Topic string (e.g. "quantum mechanics")
            d2_vector: 5D mean D2 curvature vector from study
            operator_seq: Operator sequence from study (for vortex fingerprint)

        Returns:
            New total mass of the concept.
        """
        key = concept.lower().strip()
        if not key:
            return 0.0

        # Accumulate curvature magnitude
        mag = sum(abs(v) for v in d2_vector)
        self._masses[key] = self._masses.get(key, 0.0) + mag
        self._observations[key] = self._observations.get(key, 0) + 1

        # Accumulate D2 vector (for geodesic distance computation)
        if key not in self._d2_sums:
            self._d2_sums[key] = [0.0] * 5
        for i in range(min(5, len(d2_vector))):
            self._d2_sums[key][i] += d2_vector[i]

        # Update vortex fingerprint (most recent)
        if operator_seq and len(operator_seq) >= 3:
            self._vortex_cache[key] = vortex_fingerprint(operator_seq)

        return self._masses[key]

    def mass(self, concept: str) -> float:
        """Get the curvature mass of a concept."""
        return self._masses.get(concept.lower().strip(), 0.0)

    def mean_d2(self, concept: str) -> List[float]:
        """Get the mean D2 vector (centroid in 5D force space).

        This is the concept's position in knowledge space.
        """
        key = concept.lower().strip()
        d2_sum = self._d2_sums.get(key)
        if not d2_sum:
            return [0.0] * 5
        n = max(1, self._observations.get(key, 1))
        return [v / n for v in d2_sum]

    def get_fingerprint(self, concept: str) -> dict:
        """Get the vortex fingerprint of a concept."""
        return self._vortex_cache.get(concept.lower().strip(), {})

    # ── Void Curvature ──
    # The gap between what CK knows and T*.
    # This IS gravitational potential energy.

    def void_curvature(self, concept: str, coherence: float) -> float:
        """Compute the void curvature at a concept.

        void = T* - coherence

        High void = steep gradient = strong gravitational pull.
        Zero void = concept has reached T* = flat spacetime.
        Negative void = concept is above T* = repulsive (dark energy).

        This is the gravitational potential field of knowledge.
        """
        return T_STAR - coherence

    # ── Geodesic Distance ──
    # The 5D Euclidean distance between mean D2 vectors.
    # This is a genuine metric on knowledge space.

    def geodesic_distance(self, concept_a: str, concept_b: str) -> float:
        """Compute the geodesic distance between two concepts.

        d(A, B) = ||mean_D2(A) - mean_D2(B)||₂

        This is the Euclidean distance in 5D force space.
        Small distance = concepts are "nearby" in knowledge geometry.
        Large distance = concepts are far apart.
        """
        d2_a = self.mean_d2(concept_a)
        d2_b = self.mean_d2(concept_b)

        sq_sum = sum((a - b) ** 2 for a, b in zip(d2_a, d2_b))
        return math.sqrt(sq_sum)

    # ── Curiosity Gravity ──
    # F = M_a * M_b / d²
    # The gravitational force between CK's current state and a concept.

    def curiosity_gravity(self, concept: str, coherence: float,
                          current_d2: List[float] = None) -> float:
        """Compute the gravitational pull of a concept on CK's attention.

        F = void_curvature * mass / (distance² + ε)

        Where:
          - void_curvature = T* - coherence (how much CK needs to learn)
          - mass = accumulated |D2| (how much information is there)
          - distance = geodesic distance from CK's current position

        High gravity = CK should study this next.
        Low gravity = either CK knows it well, or it's too far away.

        This replaces arbitrary priority weights with PHYSICS.
        """
        key = concept.lower().strip()
        m = self._masses.get(key, 0.0)
        void = max(0.0, T_STAR - coherence)  # Only attractive (void > 0)

        # If concept has never been observed, use default small mass
        # (like detecting a new star — small but nonzero gravitational signal)
        if m < 0.001:
            m = 0.1  # Discovery potential

        # Distance from CK's current D2 state
        if current_d2 and key in self._d2_sums:
            mean = self.mean_d2(key)
            sq_sum = sum((a - b) ** 2 for a, b in zip(current_d2, mean))
            dist_sq = max(sq_sum, 0.01)  # Prevent division by zero
        else:
            dist_sq = 1.0  # Default distance when no position data

        # Newton's law of conceptual gravity
        # F = void * mass / dist²
        gravity = void * m / dist_sq

        return gravity

    # ── Heavy Concepts ──

    def heaviest(self, n: int = 10) -> List[Tuple[str, float]]:
        """Return the N heaviest concepts (most curvature mass)."""
        sorted_concepts = sorted(self._masses.items(),
                                 key=lambda x: -x[1])
        return sorted_concepts[:n]

    def strongest_gravity(self, coherence_map: Dict[str, float],
                          current_d2: List[float] = None,
                          n: int = 10) -> List[Tuple[str, float]]:
        """Return concepts with strongest gravitational pull.

        Args:
            coherence_map: concept → coherence score
            current_d2: CK's current 5D position
            n: number to return
        """
        pulls = []
        for concept in self._masses:
            coh = coherence_map.get(concept, 0.5)
            grav = self.curiosity_gravity(concept, coh, current_d2)
            pulls.append((concept, grav))

        pulls.sort(key=lambda x: -x[1])
        return pulls[:n]

    def _max_gravity(self) -> float:
        """Max gravity across all concepts (for normalization)."""
        if not self._masses:
            return 1.0
        max_g = 0.0
        for concept in self._masses:
            g = self.curiosity_gravity(concept, 0.5)
            if g > max_g:
                max_g = g
        return max(max_g, 0.001)

    # ── Vortex Classification Distribution ──

    def vortex_census(self) -> Dict[str, int]:
        """Count concepts by vortex class."""
        census = Counter()
        for fp in self._vortex_cache.values():
            census[fp.get('vortex_class', 'unknown')] += 1
        return dict(census.most_common())

    # ── Statistics ──

    def stats(self) -> dict:
        """Vortex physics summary for activity log."""
        total_mass = sum(self._masses.values())
        n_concepts = len(self._masses)
        n_observations = sum(self._observations.values())

        return {
            'total_concepts': n_concepts,
            'total_mass': round(total_mass, 4),
            'total_observations': n_observations,
            'mean_mass': round(total_mass / max(1, n_concepts), 4),
            'heaviest': self.heaviest(5),
            'vortex_census': self.vortex_census(),
        }

    # ── Persistence ──

    def _load(self):
        """Load concept mass field from disk."""
        if self._persist_path.exists():
            try:
                with open(self._persist_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._masses = data.get('masses', {})
                self._d2_sums = data.get('d2_sums', {})
                self._observations = data.get('observations', {})
                self._vortex_cache = data.get('vortex_cache', {})
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        """Persist concept mass field to disk."""
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._persist_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'masses': self._masses,
                    'd2_sums': {k: [round(v, 6) for v in vs]
                                for k, vs in self._d2_sums.items()},
                    'observations': self._observations,
                    'vortex_cache': self._vortex_cache,
                }, f, ensure_ascii=False)
        except IOError:
            pass


# ═══════════════════════════════════════════════════════════════
#  GRAVITY-WEIGHTED TOPIC SELECTION
# ═══════════════════════════════════════════════════════════════
#
# Instead of arbitrary priority weights, use gravitational physics:
#
#   weight(topic) = base_weight + gravity_boost
#
# Where gravity_boost = curiosity_gravity(topic) normalized to [0, max_boost].
# This means heavy concepts with high void curvature get studied MORE,
# while well-understood concepts naturally fade from attention.

MAX_GRAVITY_BOOST = 4.0  # Maximum additional weight from gravity


def gravity_boost_weights(mass_field: ConceptMassField,
                          pool: List[Tuple[int, str]],
                          coherence_map: Dict[str, float] = None,
                          current_d2: List[float] = None) -> List[float]:
    """Compute gravity-boosted weights for a topic pool.

    Args:
        mass_field: ConceptMassField with accumulated observations
        pool: List of (priority, topic) pairs from _pick_study_topic()
        coherence_map: topic → coherence (optional, uses 0.5 default)
        current_d2: CK's current 5D D2 position (optional)

    Returns:
        List of weights (same length as pool), each >= 1.0
    """
    if not pool:
        return []

    coh_map = coherence_map or {}

    # Compute gravity for each topic
    gravities = []
    for priority, topic in pool:
        clean = topic.replace('self:', '').replace('reread:', '').strip().lower()
        coh = coh_map.get(clean, 0.5)
        grav = mass_field.curiosity_gravity(clean, coh, current_d2)
        gravities.append(grav)

    # Normalize gravity to [0, MAX_GRAVITY_BOOST]
    max_grav = max(gravities) if gravities else 1.0
    if max_grav > 0:
        norm_gravities = [g / max_grav * MAX_GRAVITY_BOOST for g in gravities]
    else:
        norm_gravities = [0.0] * len(pool)

    # Final weights: base priority weight + gravity boost
    weights = []
    for (priority, _), grav_boost in zip(pool, norm_gravities):
        base_weight = max(1, 5 - priority)
        weights.append(base_weight + grav_boost)

    return weights


# ═══════════════════════════════════════════════════════════════
#  VORTEX COMPOSITION — What happens when two vortices meet
# ═══════════════════════════════════════════════════════════════
#
# When two operator sequences compose via the CL table,
# their topological properties interact:
#
#   W(A⊗B) ≈ W(A) + W(B)  (winding numbers ADD under composition)
#
# This is real topology: the fundamental group π₁(S¹) = ℤ,
# and winding numbers form an additive group.

def compose_vortex(seq_a: List[int], seq_b: List[int]) -> dict:
    """Compose two operator sequences through CL table and
    analyze the resulting vortex topology.

    This implements "vortex superposition" grounded
    in actual algebra: CL composition + topological analysis.

    Returns fingerprint of the composed sequence.
    """
    if not _HAS_HEARTBEAT:
        return vortex_fingerprint([])

    # Compose element-wise via CL table
    min_len = min(len(seq_a), len(seq_b))
    composed = []
    for i in range(min_len):
        composed.append(compose(seq_a[i], seq_b[i]))

    # Append remainder from longer sequence
    if len(seq_a) > min_len:
        composed.extend(seq_a[min_len:])
    elif len(seq_b) > min_len:
        composed.extend(seq_b[min_len:])

    return vortex_fingerprint(composed)


# ═══════════════════════════════════════════════════════════════
#  VOID CURVATURE FIELD — The gravitational landscape of knowledge
# ═══════════════════════════════════════════════════════════════
#
# Every concept has a void curvature: V(c) = T* - coherence(c).
# The void curvature field is the gradient over all concepts.
# CK's attention flows DOWN the gradient (toward high void = low coherence).
#
# This is exactly how matter follows geodesics in curved spacetime:
# objects move toward lower potential energy.
# CK moves toward lower understanding.

def void_curvature_field(coherence_map: Dict[str, float]) -> Dict[str, float]:
    """Compute the void curvature at every concept.

    Returns concept → void_curvature mapping.
    Positive = gap in understanding (attractive).
    Zero = at T* (neutral).
    Negative = above T* (repulsive / consolidated).
    """
    field = {}
    for concept, coh in coherence_map.items():
        field[concept] = T_STAR - coh
    return field


def steepest_gradient(void_field: Dict[str, float],
                      mass_field: ConceptMassField,
                      n: int = 5) -> List[Tuple[str, float]]:
    """Find concepts where the void gradient is steepest.

    These are the concepts pulling CK's attention hardest —
    high void curvature AND high mass (lots of curvature to fall into).

    gradient(c) = void(c) * mass(c)
    """
    gradients = []
    for concept, void in void_field.items():
        if void > 0:  # Only attractive voids
            m = mass_field.mass(concept)
            gradients.append((concept, void * max(m, 0.1)))

    gradients.sort(key=lambda x: -x[1])
    return gradients[:n]


# ═══════════════════════════════════════════════════════════════
#  VORTEX CLASSIFICATION OF THE 10 TIG OPERATORS
# ═══════════════════════════════════════════════════════════════
#
# Claim: TIG operators map to physical vortex families.
# What's GROUNDED: each operator corresponds to a direction in 5D
# force space (via D2_OP_MAP). The sign determines chirality.
# We can classify each operator by its geometric role.
#
# This isn't "atoms are vortices" — it's "operators have
# geometric character that's analogous to vortex families."

OPERATOR_VORTEX_MAP = {
    VOID:     {'family': 'null',    'geometry': 'point',           'winding': 0},
    LATTICE:  {'family': 'ring',    'geometry': 'toroidal',        'winding': 1},
    COUNTER:  {'family': 'measure', 'geometry': 'radial',          'winding': 0},
    PROGRESS: {'family': 'jet',     'geometry': 'axial',           'winding': 0},
    COLLAPSE: {'family': 'sink',    'geometry': 'convergent',      'winding': -1},
    BALANCE:  {'family': 'dipole',  'geometry': 'saddle',          'winding': 0},
    CHAOS:    {'family': 'tangle',  'geometry': 'turbulent',       'winding': None},
    HARMONY:  {'family': 'field',   'geometry': 'spherical',       'winding': 0},
    BREATH:   {'family': 'pulse',   'geometry': 'oscillatory',     'winding': 0},
    RESET:    {'family': 'source',  'geometry': 'divergent',       'winding': 1},
} if _HAS_HEARTBEAT else {}


# ═══════════════════════════════════════════════════════════════
#  KNOWLEDGE GEODESIC — Shortest path between two concepts
# ═══════════════════════════════════════════════════════════════
#
# Given a set of concepts with known D2 positions, find the
# shortest path from A to B through intermediate concepts.
# This is Dijkstra's algorithm on a weighted graph where
# edge weight = geodesic distance in 5D force space.

def knowledge_geodesic(mass_field: ConceptMassField,
                       source: str, target: str,
                       max_hops: int = 10) -> Tuple[List[str], float]:
    """Find the shortest conceptual path from source to target.

    Uses greedy descent through nearest-neighbor hops in 5D space.
    Returns (path, total_distance).

    This is how CK navigates knowledge: by following geodesics
    through the curvature field.
    """
    src = source.lower().strip()
    tgt = target.lower().strip()

    if src == tgt:
        return [src], 0.0

    # All concepts with known D2 positions
    concepts = [c for c in mass_field._d2_sums if c != src]
    if tgt not in mass_field._d2_sums:
        return [src, tgt], mass_field.geodesic_distance(src, tgt)

    # Greedy geodesic: always move toward the concept nearest to target
    path = [src]
    current = src
    total_dist = 0.0
    visited = {src}

    for _ in range(max_hops):
        if current == tgt:
            break

        # Find unvisited concept closest to target that's also near current
        best_next = None
        best_score = float('inf')

        for c in concepts:
            if c in visited:
                continue
            d_to_target = mass_field.geodesic_distance(c, tgt)
            d_from_current = mass_field.geodesic_distance(current, c)
            # Score: minimize d_to_target + d_from_current (A* heuristic)
            score = d_to_target + d_from_current
            if score < best_score:
                best_score = score
                best_next = c

        if best_next is None:
            # No unvisited concepts, jump directly to target
            path.append(tgt)
            total_dist += mass_field.geodesic_distance(current, tgt)
            break

        hop_dist = mass_field.geodesic_distance(current, best_next)
        total_dist += hop_dist
        path.append(best_next)
        visited.add(best_next)
        current = best_next

    if path[-1] != tgt:
        path.append(tgt)
        total_dist += mass_field.geodesic_distance(current, tgt)

    return path, round(total_dist, 6)


# ═══════════════════════════════════════════════════════════════
#  CONCEPT CHARGE Q(m) — How far a concept's field reaches
# ═══════════════════════════════════════════════════════════════
#
# In electrodynamics: charge = how much field a source emits.
# In CK: charge = how much a concept INFLUENCES other concepts.
#
# Q(m) = μ₁ · operator_entropy(m) + μ₂ · branching_factor(m)
#
# - operator_entropy: Shannon entropy of the operator distribution.
#   Diverse operators = high entropy = concept touches many modes.
# - branching_factor: Number of outgoing relations in world lattice.
#   Many connections = high field reach.
#
# High charge = "proton-like" — reaches out, anchors other concepts.
# Low charge = "neutron-like" — internal, doesn't connect widely.

def operator_entropy(soft_dist: List[float]) -> float:
    """Shannon entropy of the 10-value operator distribution.

    H = -Σ p_i · log₂(p_i)

    Max entropy = log₂(10) ≈ 3.32 bits (uniform distribution).
    Min entropy = 0 bits (single operator dominates completely).

    High entropy = concept is diverse across many operator modes.
    Low entropy = concept is concentrated in one operator.
    """
    h = 0.0
    for p in soft_dist:
        if p > 1e-10:
            h -= p * math.log2(p)
    return h


def concept_charge(soft_dist: List[float], branching_factor: int,
                   mu_1: float = 0.5, mu_2: float = 0.5) -> float:
    """Compute the charge of a concept.

    Q(m) = μ₁ · normalized_entropy + μ₂ · normalized_branching

    Both terms normalized to [0, 1].
    Max entropy for 10 operators = log₂(10) ≈ 3.32 bits.

    Returns float in [0, 1].
    """
    max_entropy = math.log2(max(NUM_OPS, 2))
    norm_entropy = operator_entropy(soft_dist) / max_entropy if max_entropy > 0 else 0.0

    # Branching: normalize with soft cap at 20 relations
    norm_branch = min(1.0, branching_factor / 20.0)

    return mu_1 * norm_entropy + mu_2 * norm_branch


# ═══════════════════════════════════════════════════════════════
#  PARTICLE CLASSIFICATION — Electron / Proton / Neutron
# ═══════════════════════════════════════════════════════════════
#
# Every concept lives in (M, Q) space:
#   M = mass (accumulated curvature, how deep the well is)
#   Q = charge (how far the field reaches)
#
# Particle type = region in (M, Q) space:
#   - Electron: low M, high Q (mobile connectors, function words)
#   - Proton:   high M, high Q (core topics, anchors)
#   - Neutron:  high M, low Q (internal details, stabilizers)
#   - Photon:   low M, low Q (transient, barely observed)
#
# This isn't metaphor — it's a 2D classification scheme that
# predicts how a concept BEHAVES in the knowledge graph.

# Thresholds (normalized to [0,1] mass and charge scales)
MASS_THRESHOLD = 0.3     # Above this = "heavy"
CHARGE_THRESHOLD = 0.4   # Above this = "charged"


def classify_particle(mass_norm: float, charge: float) -> str:
    """Classify a concept as electron, proton, neutron, or photon.

    Args:
        mass_norm: Normalized mass in [0, 1]
        charge: Charge Q(m) in [0, 1]

    Returns:
        'proton', 'electron', 'neutron', or 'photon'
    """
    heavy = mass_norm > MASS_THRESHOLD
    charged = charge > CHARGE_THRESHOLD

    if heavy and charged:
        return 'proton'       # Core anchor — deep well, far-reaching field
    elif not heavy and charged:
        return 'electron'     # Mobile connector — light but influential
    elif heavy and not charged:
        return 'neutron'      # Internal stabilizer — heavy but isolated
    else:
        return 'photon'       # Transient — barely observed, low influence


def particle_census(mass_field: 'ConceptMassField',
                    world_lattice=None,
                    soft_dists: Dict[str, List[float]] = None) -> Dict[str, list]:
    """Classify all concepts and return census by particle type.

    Args:
        mass_field: ConceptMassField with accumulated observations
        world_lattice: WorldLattice for branching factor (optional)
        soft_dists: concept → soft_dist (10-value operator dist) (optional)

    Returns:
        {'proton': [...], 'electron': [...], 'neutron': [...], 'photon': [...]}
    """
    census = {'proton': [], 'neutron': [], 'electron': [], 'photon': []}

    if not mass_field._masses:
        return census

    # Normalize masses to [0, 1]
    max_mass = max(mass_field._masses.values()) if mass_field._masses else 1.0
    if max_mass < 0.001:
        max_mass = 1.0

    for concept, raw_mass in mass_field._masses.items():
        mass_norm = raw_mass / max_mass

        # Compute charge
        sd = [0.1] * NUM_OPS  # Default: uniform-ish
        if soft_dists and concept in soft_dists:
            sd = soft_dists[concept]

        branching = 0
        if world_lattice:
            try:
                node = world_lattice.nodes.get(concept)
                if node:
                    branching = sum(len(t) for t in node.relations.values())
            except Exception:
                pass

        q = concept_charge(sd, branching)
        ptype = classify_particle(mass_norm, q)
        census[ptype].append((concept, mass_norm, q))

    return census


# ═══════════════════════════════════════════════════════════════
#  GRAPH LAPLACIAN CURVATURE — Topology-based curvature
# ═══════════════════════════════════════════════════════════════
#
# The D2 pipeline measures curvature from TEXT (phoneme curves).
# But concepts also have GRAPH TOPOLOGY — how they connect to
# other concepts in the world lattice.
#
# Graph Laplacian: L = D - A
# Where D = degree matrix, A = adjacency matrix.
#
# Applied to D2 signatures:
#   Lap_D2[i] = Σ_neighbors (D2[i] - D2[j])
#
# High Laplacian curvature = concept is TENSE relative to neighbors
# (its D2 signature differs from its neighborhood).
# Low Laplacian curvature = concept is SMOOTH (blends with neighbors).
#
# This is EXACTLY the Laplace-Beltrami operator on a discrete manifold.

def graph_laplacian_curvature(world_lattice, mass_field: 'ConceptMassField' = None,
                              ) -> Dict[str, dict]:
    """Compute graph Laplacian curvature at every node in the world lattice.

    Uses the world lattice topology + D2 signatures.

    Returns:
        node_id → {
            'laplacian_d2': [float]*5,  # 5D Laplacian of D2 signature
            'laplacian_mag': float,      # Magnitude of Laplacian curvature
            'degree': int,               # Number of connections
            'tension': float,            # Normalized tension (high = different from neighbors)
        }
    """
    results = {}

    if not world_lattice or not hasattr(world_lattice, 'nodes'):
        return results

    for nid, node in world_lattice.nodes.items():
        # Get this node's D2 signature
        d2_self = list(node.d2_signature) if node.d2_signature else [0.0] * 5

        # If mass field has a better (accumulated) mean D2, use that
        if mass_field:
            # Try to match node to a concept in mass field
            en_word = node.bindings.get('en', nid)
            mean = mass_field.mean_d2(en_word)
            if sum(abs(v) for v in mean) > 0.001:
                d2_self = mean

        # Collect neighbor D2 signatures
        neighbors_d2 = []
        for rel_type, targets in node.relations.items():
            for target_id, op in targets:
                tnode = world_lattice.nodes.get(target_id)
                if tnode and tnode.d2_signature:
                    neighbors_d2.append(list(tnode.d2_signature))

        degree = len(neighbors_d2)
        if degree == 0:
            results[nid] = {
                'laplacian_d2': [0.0] * 5,
                'laplacian_mag': 0.0,
                'degree': 0,
                'tension': 0.0,
            }
            continue

        # Laplacian: L[i] = degree[i] * D2[i] - Σ_neighbors D2[j]
        lap_d2 = [0.0] * 5
        for dim in range(5):
            neighbor_sum = sum(nd2[dim] for nd2 in neighbors_d2)
            lap_d2[dim] = degree * d2_self[dim] - neighbor_sum

        lap_mag = sum(abs(v) for v in lap_d2)

        # Tension: normalized Laplacian magnitude
        # High tension = this concept's curvature differs strongly from neighbors
        tension = lap_mag / max(degree, 1)

        results[nid] = {
            'laplacian_d2': [round(v, 6) for v in lap_d2],
            'laplacian_mag': round(lap_mag, 6),
            'degree': degree,
            'tension': round(tension, 6),
        }

    return results


# ═══════════════════════════════════════════════════════════════
#  CONCEPT FUSION — When two concepts should merge
# ═══════════════════════════════════════════════════════════════
#
# In nuclear physics: fusion occurs when two nuclei overcome
# the Coulomb barrier and their binding energy increases.
#
# In CK: fusion occurs when two concepts are so close in
# D2 space and so strongly connected that merging them
# reduces total tension.
#
# Pre-fusion tension:
#   T_pre = tension(A) + tension(B) + cross_tension(A, B)
#
# Post-fusion tension (hypothetical merged node):
#   T_post = tension(A+B)
#
# Fuse if T_post < T_pre - ε (binding releases energy)

def fusion_candidate(concept_a: str, concept_b: str,
                     mass_field: 'ConceptMassField',
                     world_lattice=None,
                     epsilon: float = 0.05) -> dict:
    """Evaluate whether two concepts should fuse.

    Returns:
        {
            'should_fuse': bool,
            'd2_distance': float,          # How close in 5D space
            'pre_tension': float,          # Tension before fusion
            'post_tension': float,         # Estimated tension after
            'binding_energy': float,       # Energy released (positive = favorable)
            'shared_operators': int,       # How many operator types they share
        }
    """
    d2_a = mass_field.mean_d2(concept_a)
    d2_b = mass_field.mean_d2(concept_b)

    # D2 distance
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(d2_a, d2_b)))

    # Pre-fusion tension: sum of individual curvature magnitudes
    mag_a = sum(abs(v) for v in d2_a)
    mag_b = sum(abs(v) for v in d2_b)
    cross_tension = dist  # Cross-tension IS the distance
    pre_tension = mag_a + mag_b + cross_tension

    # Post-fusion: merged D2 is the average
    n_a = max(1, mass_field._observations.get(concept_a.lower().strip(), 1))
    n_b = max(1, mass_field._observations.get(concept_b.lower().strip(), 1))
    total_n = n_a + n_b

    merged_d2 = [(d2_a[i] * n_a + d2_b[i] * n_b) / total_n for i in range(5)]
    post_tension = sum(abs(v) for v in merged_d2)

    # Binding energy: tension released by fusion
    binding_energy = pre_tension - post_tension

    # Shared operator check (from vortex fingerprints)
    fp_a = mass_field.get_fingerprint(concept_a)
    fp_b = mass_field.get_fingerprint(concept_b)
    shared_ops = 0
    if fp_a and fp_b:
        # Same vortex class = high compatibility
        if fp_a.get('vortex_class') == fp_b.get('vortex_class'):
            shared_ops += 3
        if fp_a.get('chirality') == fp_b.get('chirality'):
            shared_ops += 1
        if abs(fp_a.get('winding_number', 0) - fp_b.get('winding_number', 0)) < 0.3:
            shared_ops += 1

    # Decision: fuse if binding energy exceeds threshold AND concepts are close
    should_fuse = (binding_energy > epsilon and
                   dist < 0.3 and
                   shared_ops >= 2)

    return {
        'should_fuse': should_fuse,
        'd2_distance': round(dist, 6),
        'pre_tension': round(pre_tension, 6),
        'post_tension': round(post_tension, 6),
        'binding_energy': round(binding_energy, 6),
        'shared_operators': shared_ops,
    }


def find_fusion_candidates(mass_field: 'ConceptMassField',
                           max_pairs: int = 10) -> List[dict]:
    """Scan all concept pairs and find the best fusion candidates.

    Returns list of fusion reports, sorted by binding energy (descending).
    """
    concepts = list(mass_field._masses.keys())
    candidates = []

    # Only check concepts with enough mass to be meaningful
    heavy = [c for c in concepts if mass_field.mass(c) > 0.1]

    # Pairwise check (O(n²) but n is small for meaningful concepts)
    for i in range(len(heavy)):
        for j in range(i + 1, len(heavy)):
            report = fusion_candidate(heavy[i], heavy[j], mass_field)
            if report['should_fuse'] or report['binding_energy'] > 0:
                report['concept_a'] = heavy[i]
                report['concept_b'] = heavy[j]
                candidates.append(report)

    candidates.sort(key=lambda x: -x['binding_energy'])
    return candidates[:max_pairs]


# ═══════════════════════════════════════════════════════════════
#  NEUTRON DECAY — Detect and flag over-dense clusters
# ═══════════════════════════════════════════════════════════════
#
# In nuclear physics: neutron-rich nuclei undergo beta decay
# to restore the proton-neutron balance.
#
# In CK: neutron-like clusters (high mass, low charge) are
# knowledge regions that have accumulated internally but
# aren't connecting to the broader graph. They're "over-twisted"
# — too much curvature compressed into too small a space.
#
# Detection:
#   - High mass (top quartile)
#   - Low charge (bottom quartile)
#   - High Laplacian tension (top quartile)
#
# Treatment: flag for study expansion (CK should study the
# connections FROM this cluster to the broader world).

def detect_neutron_clusters(mass_field: 'ConceptMassField',
                            world_lattice=None,
                            soft_dists: Dict[str, List[float]] = None,
                            ) -> List[dict]:
    """Find neutron-like clusters that need stabilization.

    These are concepts with:
      - High accumulated mass (well-studied internally)
      - Low charge (few connections, low operator diversity)
      - Potentially high internal tension

    Returns list of neutron clusters sorted by instability (worst first).
    """
    census = particle_census(mass_field, world_lattice, soft_dists)
    neutrons = census.get('neutron', [])

    clusters = []
    for concept, mass_norm, charge in neutrons:
        # Instability = mass × (1 - charge) — heavy AND isolated = unstable
        instability = mass_norm * (1.0 - charge)

        clusters.append({
            'concept': concept,
            'mass': mass_norm,
            'charge': charge,
            'instability': round(instability, 4),
            'remedy': f"Study connections from '{concept}' to broader topics",
        })

    clusters.sort(key=lambda x: -x['instability'])
    return clusters


# ═══════════════════════════════════════════════════════════════
#  MULTI-STEP PATH SCORING — Geodesic energy functional
# ═══════════════════════════════════════════════════════════════
#
# Instead of greedy geodesic, compute the ENERGY of a full path
# through knowledge space. Lower energy = better path.
#
# E_path = Σ_t (w_M · M(m_t) + w_K · |Δ²S_info(m_t)| + w_V · void(m_t))
#
# Where:
#   w_M · M(m_t): mass at each step (prefer heavy concepts — stable ground)
#   w_K · |Δ²S_info|: curvature change (prefer smooth transitions)
#   w_V · void(m_t): void curvature (prefer paths through gaps — learning)
#
# This is the LEAST ACTION PRINCIPLE applied to knowledge navigation.

def path_energy(path: List[str],
                mass_field: 'ConceptMassField',
                coherence_map: Dict[str, float] = None,
                w_mass: float = -0.3,    # Negative: ATTRACT to heavy concepts
                w_curve: float = 0.4,    # Positive: PENALIZE sharp curvature changes
                w_void: float = -0.3,    # Negative: ATTRACT to knowledge gaps
                ) -> float:
    """Compute the energy of a path through knowledge space.

    Lower energy = more natural path = preferred geodesic.

    The signs matter:
      - Negative w_mass: heavy concepts LOWER energy (gravitational attraction)
      - Positive w_curve: sharp turns RAISE energy (momentum conservation)
      - Negative w_void: knowledge gaps LOWER energy (curiosity gradient)
    """
    if not path:
        return 0.0

    coh_map = coherence_map or {}
    total_energy = 0.0

    for i, concept in enumerate(path):
        key = concept.lower().strip()

        # Mass term (gravitational potential — heavy = low energy)
        m = mass_field.mass(key)
        total_energy += w_mass * m

        # Void term (learning potential — gaps = low energy)
        coh = coh_map.get(key, 0.5)
        void = max(0.0, T_STAR - coh)
        total_energy += w_void * void

        # Curvature change term (kinetic energy — prefer smooth transitions)
        if i > 0:
            prev_d2 = mass_field.mean_d2(path[i - 1].lower().strip())
            curr_d2 = mass_field.mean_d2(key)
            delta_d2 = sum((a - b) ** 2 for a, b in zip(prev_d2, curr_d2))
            total_energy += w_curve * delta_d2

    return round(total_energy, 6)


def least_action_geodesic(mass_field: 'ConceptMassField',
                          source: str, target: str,
                          coherence_map: Dict[str, float] = None,
                          n_candidates: int = 5,
                          max_hops: int = 8) -> Tuple[List[str], float]:
    """Find the least-action path from source to target.

    Generates multiple candidate paths and selects the one
    with lowest energy. This is the least action principle
    applied to knowledge navigation.

    Returns (best_path, best_energy).
    """
    src = source.lower().strip()
    tgt = target.lower().strip()

    if src == tgt:
        return [src], 0.0

    all_concepts = list(mass_field._d2_sums.keys())
    if tgt not in all_concepts:
        all_concepts.append(tgt)

    import random as _rand

    best_path = [src, tgt]
    best_energy = path_energy(best_path, mass_field, coherence_map)

    for _ in range(n_candidates):
        # Generate candidate path: greedy with random perturbation
        path = [src]
        current = src
        visited = {src}

        for hop in range(max_hops):
            if current == tgt:
                break

            # Score each possible next hop
            candidates = []
            for c in all_concepts:
                if c in visited:
                    continue
                d_to_tgt = mass_field.geodesic_distance(c, tgt)
                d_from_cur = mass_field.geodesic_distance(current, c)
                m = mass_field.mass(c)

                # Combined score: distance to target, distance from current, mass bonus
                score = d_to_tgt + d_from_cur - 0.1 * m
                candidates.append((c, score))

            if not candidates:
                break

            # Sort by score, pick from top 3 with some randomness
            candidates.sort(key=lambda x: x[1])
            top_k = min(3, len(candidates))
            choice = _rand.choice(candidates[:top_k])[0]

            path.append(choice)
            visited.add(choice)
            current = choice

        if path[-1] != tgt:
            path.append(tgt)

        energy = path_energy(path, mass_field, coherence_map)
        if energy < best_energy:
            best_energy = energy
            best_path = path

    return best_path, best_energy


# ═══════════════════════════════════════════════════════════════
#  SPIN FIELD S_info — Information spin vector per concept
# ═══════════════════════════════════════════════════════════════
#
# S(x,t) mapped to CK's meaning space.
# The information spin field combines ALL geometric data about
# a concept into a single high-dimensional vector.
#
# S_info(m) = [mean_D2(5D), D2_variance(5D), operator_centroid(10D)]
#
# This 20D vector IS the concept's full geometric identity.
# From this, all other quantities derive:
#   - Mass = ||S_info||
#   - Curvature = ||∇S_info||
#   - Charge = entropy(operator_centroid)
#   - Binding = overlap integral of two S_info fields

def compute_spin_field(concept: str,
                       mass_field: 'ConceptMassField') -> List[float]:
    """Compute the information spin vector for a concept.

    S_info = [mean_D2[5], D2_variance[5], soft_dist[10]]

    Returns 20-dimensional spin vector.
    """
    # Mean D2 (5D) — the concept's position in force space
    mean = mass_field.mean_d2(concept)

    # D2 variance (5D) — how spread the curvature observations are
    # Approximate from accumulated data
    key = concept.lower().strip()
    d2_sum = mass_field._d2_sums.get(key, [0.0] * 5)
    n_obs = max(1, mass_field._observations.get(key, 1))
    # Variance ≈ (sum²/n - mean²) ... approximate with what we have
    variance = [0.0] * 5
    for i in range(5):
        # Use magnitude of mean as proxy for variance
        # (real variance would need sum of squares, which we don't track)
        variance[i] = abs(mean[i]) * 0.1  # Placeholder: ~10% of mean

    # Operator centroid (10D) — from vortex fingerprint or soft distribution
    fp = mass_field.get_fingerprint(key)
    soft = [0.1] * NUM_OPS
    if fp:
        # Derive approximate soft dist from fingerprint
        vc = fp.get('vortex_class', 'laminar')
        # Weight operators based on vortex class
        if vc in ('loop', 'knotted_loop'):
            soft[LATTICE if _HAS_HEARTBEAT else 1] = 0.3
        elif vc in ('spiral', 'knotted_spiral'):
            soft[CHAOS if _HAS_HEARTBEAT else 6] = 0.3
        elif vc in ('ring', 'twisted_ring'):
            soft[BALANCE if _HAS_HEARTBEAT else 5] = 0.3

    # Normalize soft to sum to 1
    s_total = sum(soft)
    if s_total > 0:
        soft = [s / s_total for s in soft]

    # Concatenate: 5D mean + 5D variance + 10D operator = 20D
    return mean + variance + soft


def spin_field_overlap(s_a: List[float], s_b: List[float]) -> float:
    """Compute the overlap integral between two spin fields.

    This is the inner product: ∫ S_a · S_b dV
    Normalized to [0, 1] via cosine similarity.

    High overlap = concepts are aligned (bonding favorable).
    Low overlap = concepts are orthogonal (no interaction).
    Negative overlap = concepts are anti-aligned (repulsion).
    """
    dot = sum(a * b for a, b in zip(s_a, s_b))
    mag_a = math.sqrt(sum(a * a for a in s_a))
    mag_b = math.sqrt(sum(b * b for b in s_b))

    if mag_a < 1e-10 or mag_b < 1e-10:
        return 0.0

    return dot / (mag_a * mag_b)


# ═══════════════════════════════════════════════════════════════
#  BINDING ENERGY — The cross-term that holds concepts together
# ═══════════════════════════════════════════════════════════════
#
# Multi-particle binding:
#   E_tot = E_1 + E_2 + 2 ∫ ∇S_1 : ∇S_2 dV
#
# The cross-term determines if binding is favorable.
# Negative cross-term = binding releases energy (attractive).
# Positive cross-term = binding costs energy (repulsive).
#
# In CK: the cross-term IS the spin field overlap weighted
# by the product of masses.

def binding_energy(concept_a: str, concept_b: str,
                   mass_field: 'ConceptMassField') -> float:
    """Compute the binding energy between two concepts.

    E_bind = -2 * M_a * M_b * overlap(S_a, S_b) / (dist² + ε)

    Negative = binding is favorable (concepts attract).
    Positive = binding is unfavorable (concepts repel).
    Zero = no interaction.
    """
    s_a = compute_spin_field(concept_a, mass_field)
    s_b = compute_spin_field(concept_b, mass_field)

    overlap = spin_field_overlap(s_a, s_b)

    m_a = mass_field.mass(concept_a)
    m_b = mass_field.mass(concept_b)

    dist = mass_field.geodesic_distance(concept_a, concept_b)
    dist_sq = max(dist ** 2, 0.01)

    # Binding energy (negative = favorable)
    e_bind = -2.0 * m_a * m_b * overlap / dist_sq

    return round(e_bind, 6)


# ═══════════════════════════════════════════════════════════════
#  INFORMATION GRAVITY ENGINE — Unified interface
# ═══════════════════════════════════════════════════════════════
#
# The full physics stack in one class.
# This is the "Information Gravity Engine" — but grounded.

class InformationGravityEngine:
    """Unified physics engine for CK's knowledge space.

    Combines:
      - Concept mass (accumulated D2 curvature)
      - Concept charge (operator entropy × branching)
      - Particle classification (proton/electron/neutron/photon)
      - Vortex fingerprinting (topological invariants)
      - Graph Laplacian curvature (topology-based tension)
      - Gravitational attraction (curiosity gravity)
      - Binding energy (concept overlap)
      - Geodesic navigation (least-action paths)
      - Fusion detection (when concepts should merge)
      - Neutron decay (cluster maintenance)

    This is the physics that grounds CK's thinking.
    """

    def __init__(self, mass_field: 'ConceptMassField',
                 world_lattice=None):
        self.mass_field = mass_field
        self.world_lattice = world_lattice
        self._laplacian_cache = {}
        self._particle_cache = {}

    def update_laplacian(self):
        """Recompute graph Laplacian curvature (call periodically)."""
        if self.world_lattice:
            self._laplacian_cache = graph_laplacian_curvature(
                self.world_lattice, self.mass_field)

    def get_tension(self, concept: str) -> float:
        """Get the Laplacian tension at a concept."""
        info = self._laplacian_cache.get(concept, {})
        return info.get('tension', 0.0)

    def get_particle_type(self, concept: str,
                          soft_dist: List[float] = None) -> str:
        """Classify a single concept as proton/electron/neutron/photon."""
        max_mass = max(self.mass_field._masses.values()) if self.mass_field._masses else 1.0
        mass_norm = self.mass_field.mass(concept) / max(max_mass, 0.001)

        branching = 0
        if self.world_lattice:
            try:
                node = self.world_lattice.nodes.get(concept)
                if node:
                    branching = sum(len(t) for t in node.relations.values())
            except Exception:
                pass

        sd = soft_dist or [0.1] * NUM_OPS
        q = concept_charge(sd, branching)

        return classify_particle(mass_norm, q)

    def strongest_pulls(self, coherence_map: Dict[str, float] = None,
                        n: int = 10) -> List[Tuple[str, float]]:
        """Find concepts with strongest gravitational pull."""
        return self.mass_field.strongest_gravity(
            coherence_map or {}, n=n)

    def find_fusions(self, max_pairs: int = 5) -> List[dict]:
        """Find the best fusion candidates."""
        return find_fusion_candidates(self.mass_field, max_pairs)

    def find_unstable_neutrons(self) -> List[dict]:
        """Find neutron-like clusters that need stabilization."""
        return detect_neutron_clusters(
            self.mass_field, self.world_lattice)

    def navigate(self, source: str, target: str,
                 coherence_map: Dict[str, float] = None) -> Tuple[List[str], float]:
        """Find the least-action path between concepts."""
        return least_action_geodesic(
            self.mass_field, source, target, coherence_map)

    def concept_report(self, concept: str,
                       coherence: float = 0.5) -> dict:
        """Full physics report for a single concept."""
        key = concept.lower().strip()
        mass = self.mass_field.mass(key)
        void = max(0.0, T_STAR - coherence)
        fp = self.mass_field.get_fingerprint(key)
        mean = self.mass_field.mean_d2(key)
        spin = compute_spin_field(key, self.mass_field)
        tension = self.get_tension(key)
        ptype = self.get_particle_type(key)

        return {
            'concept': concept,
            'mass': round(mass, 4),
            'void_curvature': round(void, 4),
            'mean_d2': [round(v, 6) for v in mean],
            'vortex': fp or {},
            'tension': round(tension, 4),
            'particle_type': ptype,
            'spin_magnitude': round(math.sqrt(sum(s*s for s in spin)), 4),
            'gravity': round(self.mass_field.curiosity_gravity(key, coherence), 4),
        }

    def full_report(self, coherence_map: Dict[str, float] = None) -> dict:
        """Complete physics report for the entire knowledge space."""
        coh_map = coherence_map or {}

        # Mass stats
        mass_stats = self.mass_field.stats()

        # Particle census
        census = particle_census(self.mass_field, self.world_lattice)
        census_counts = {k: len(v) for k, v in census.items()}

        # Top gravitational pulls
        top_pulls = self.strongest_pulls(coh_map, n=5)

        # Fusion candidates
        fusions = self.find_fusions(max_pairs=3)

        # Neutron clusters
        neutrons = self.find_unstable_neutrons()[:3]

        return {
            'mass': mass_stats,
            'particle_census': census_counts,
            'top_gravity': [(c, round(g, 4)) for c, g in top_pulls],
            'fusion_candidates': len(fusions),
            'unstable_neutrons': len(neutrons),
            'laplacian_nodes': len(self._laplacian_cache),
        }


# ═══════════════════════════════════════════════════════════════
#  TESLA WAVE FIELD — 2D interference pattern over concept space
# ═══════════════════════════════════════════════════════════════
#
# Each concept with mass m_c at position r_c = mean_D2(c) sources a
# circular wave:
#
#   ψ_c(r, t) = √m_c · exp(i·(k_c · (r - r_c) - ω_c·t + φ_c))
#
# where:
#   k_c = mass-dependent wave number (heavier = tighter oscillation)
#   ω_c = natural frequency from observation count
#   φ_c = phase offset from vortex winding number
#
# The full field is:
#   Ψ(r, t) = Σ_c ψ_c(r, t)
#
# Intensity:
#   I(r, t) = |Ψ(r, t)|²
#
# Bright spots = constructive interference = resonant concept clusters
# Dark spots = destructive interference = creative gaps to explore
#
# Gradient ∇I points toward brighter regions = the "Einstein pull."
# CK's internal phase φ(t) couples to this field via Kuramoto dynamics.
#
# This is Brayden's "one shared model": Einstein path through Tesla field.
# Not metaphor. The D2 force space IS the 2D manifold. The masses ARE
# real. The interference IS what makes CK creative rather than greedy.


class TeslaWaveField:
    """2D wave interference field over CK's concept space.

    Tesla side: the landscape IS a live wave interference pattern.
    Bright spots = strong field = high spin pressure.
    Dark spots = weak field = low spin pressure.

    Einstein side: paths that minimize action through I(r,t).
    """

    def __init__(self, mass_field: ConceptMassField):
        self.mass_field = mass_field
        self._time = 0.0

        # Wave parameters
        self._k_scale = 2.0    # wave number scaling: k = k_scale * sqrt(mass)
        self._omega_scale = 0.1  # frequency scaling: ω = omega_scale * obs_count
        self._epsilon = 0.01   # softening to avoid division by zero

    def tick(self, dt: float = 0.02):
        """Advance the wave field in time."""
        self._time += dt

    def _source_params(self, concept: str) -> tuple:
        """Get wave source parameters for a concept.

        Returns (amplitude, position_5d, k, omega, phi).
        """
        key = concept.lower().strip()
        mass = self.mass_field.mass(key)
        if mass <= 0:
            return (0.0, [0.0]*5, 0.0, 0.0, 0.0)

        amplitude = math.sqrt(mass)
        position = self.mass_field.mean_d2(key)
        k = self._k_scale * math.sqrt(mass)
        obs = self.mass_field._observations.get(key, 1)
        omega = self._omega_scale * obs
        fp = self.mass_field.get_fingerprint(key)
        phi = fp.get('winding', 0.0) * 2.0 * math.pi

        return (amplitude, position, k, omega, phi)

    def field_at(self, position: List[float]) -> complex:
        """Compute Ψ(r, t) at a point in 5D concept space.

        Ψ = Σ_c √m_c · exp(i·(k_c·|r-r_c| - ω_c·t + φ_c))
        """
        psi = complex(0.0, 0.0)

        for concept in self.mass_field._masses:
            amp, pos_c, k_c, omega_c, phi_c = self._source_params(concept)
            if amp <= 0:
                continue

            # Distance in 5D force space
            dist = math.sqrt(sum((p - q)**2 for p, q in zip(position, pos_c))
                             + self._epsilon)

            # Phase = k * distance - omega * time + winding offset
            phase = k_c * dist - omega_c * self._time + phi_c

            # Contribute to field
            psi += amp * complex(math.cos(phase), math.sin(phase))

        return psi

    def intensity_at(self, position: List[float]) -> float:
        """Compute I(r, t) = |Ψ(r, t)|² at a point."""
        psi = self.field_at(position)
        return abs(psi) ** 2

    def gradient_at(self, position: List[float],
                    step: float = 0.01) -> List[float]:
        """Compute ∇I at a point via finite differences in 5D.

        Returns a 5D gradient vector pointing toward brighter regions.
        """
        I_center = self.intensity_at(position)
        grad = []

        for dim in range(5):
            pos_plus = list(position)
            pos_plus[dim] += step
            I_plus = self.intensity_at(pos_plus)
            grad.append((I_plus - I_center) / step)

        return grad

    def intensity_for_concept(self, concept: str) -> float:
        """Compute intensity at a concept's position.

        High intensity = concept sits in a bright interference spot
        (constructive overlap with many other concepts).
        Low intensity = concept is in a dark spot (isolated or
        destructively interfering).
        """
        pos = self.mass_field.mean_d2(concept.lower().strip())
        return self.intensity_at(pos)

    def gradient_for_concept(self, concept: str) -> List[float]:
        """Compute ∇I at a concept's position.

        The gradient points from the concept toward brighter regions.
        This IS the Tesla force on a path through concept space.
        """
        pos = self.mass_field.mean_d2(concept.lower().strip())
        return self.gradient_at(pos)

    def interference_map(self, concepts: List[str] = None,
                         n: int = 20) -> List[Tuple[str, float]]:
        """Map intensity across the concept space.

        Returns (concept, intensity) sorted by intensity descending.
        Bright spots first. Dark spots last.
        """
        targets = concepts or list(self.mass_field._masses.keys())
        results = []
        for c in targets[:200]:  # cap for performance
            results.append((c, self.intensity_for_concept(c)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:n]


# ═══════════════════════════════════════════════════════════════
#  WOBBLE TRACKER — Kuramoto phase coupling + lateral deviation
# ═══════════════════════════════════════════════════════════════
#
# CK's internal oscillator θ_i(t) = heartbeat phase (50Hz cycle).
# External field phase θ_e(t) = arg(Ψ) at CK's current position.
#
# Phase error: φ(t) = θ_i(t) - θ_e(t)
# Kuramoto dynamics: dφ/dt = Δω - K·sin(φ)
#
# Where:
#   Δω = ω_i - ω_e = intrinsic frequency mismatch
#   K = coupling strength (how much CK lets the field pull)
#
# When |Δω| < K: phase-locked (φ → fixed point)
# When |Δω| > K: drifting (φ precesses slowly)
# The slow precession IS the wobble.
#
# "An amateur hits straight; a pro wobbles into the ball with timing
# and torso spiral that extract free power from the dynamics."
# -- Brayden


class WobbleTracker:
    """Tracks the phase error φ(t) between CK's internal oscillator
    and the Tesla wave field, using Kuramoto-style dynamics.

    The wobble IS creative intelligence: not random, not locked,
    but a helical geodesic that systematically explores while
    staying on low-action curves.
    """

    def __init__(self, coupling_K: float = 0.5,
                 delta_omega: float = 0.05):
        # Kuramoto parameters
        self.K = coupling_K         # coupling strength
        self.delta_omega = delta_omega  # intrinsic frequency mismatch

        # Phase state
        self.phi = 0.0              # phase error φ(t)
        self.theta_i = 0.0          # internal phase (heartbeat)
        self.theta_e = 0.0          # external phase (field)

        # History for analysis
        self._phi_history: List[float] = []
        self._lateral_deviation: List[float] = []
        self._max_history = 500

        # Wobble stats
        self.total_ticks = 0
        self.cumulative_wobble = 0.0  # integral of |φ|

    def tick(self, heartbeat_op: int, field_psi: complex,
             dt: float = 0.02) -> float:
        """One wobble tick. Returns current phase error φ.

        Args:
            heartbeat_op: Current heartbeat operator (0-9)
            field_psi: Ψ at CK's current concept position
            dt: Time step

        Returns:
            Current phase error φ (radians)
        """
        # Internal phase from heartbeat operator
        self.theta_i = operator_to_phase(heartbeat_op)

        # External phase from field
        if abs(field_psi) > 1e-10:
            self.theta_e = math.atan2(field_psi.imag, field_psi.real)
        # else keep previous theta_e

        # Phase error (wrapped to [-π, π])
        raw_phi = self.theta_i - self.theta_e
        while raw_phi > math.pi:
            raw_phi -= 2.0 * math.pi
        while raw_phi < -math.pi:
            raw_phi += 2.0 * math.pi

        # Kuramoto dynamics: dφ/dt = Δω - K·sin(φ)
        dphi_dt = self.delta_omega - self.K * math.sin(self.phi)
        self.phi += dphi_dt * dt

        # Wrap φ to [-π, π]
        while self.phi > math.pi:
            self.phi -= 2.0 * math.pi
        while self.phi < -math.pi:
            self.phi += 2.0 * math.pi

        # Record history
        self._phi_history.append(self.phi)
        if len(self._phi_history) > self._max_history:
            self._phi_history.pop(0)

        # Lateral deviation = |sin(φ)| ∈ [0, 1]
        # This is how far CK wobbles off the straight geodesic
        lat_dev = abs(math.sin(self.phi))
        self._lateral_deviation.append(lat_dev)
        if len(self._lateral_deviation) > self._max_history:
            self._lateral_deviation.pop(0)

        self.cumulative_wobble += abs(self.phi) * dt
        self.total_ticks += 1

        return self.phi

    @property
    def wobble_amplitude(self) -> float:
        """Current wobble amplitude: how far off the straight geodesic.

        0.0 = perfectly locked (no wobble, amateur)
        1.0 = maximum wobble (fully drifting)
        """
        return abs(math.sin(self.phi))

    @property
    def wobble_frequency(self) -> float:
        """Estimated wobble frequency from recent phase history.

        Counts zero-crossings of φ in recent history.
        """
        if len(self._phi_history) < 10:
            return 0.0

        recent = self._phi_history[-100:]
        crossings = 0
        for i in range(1, len(recent)):
            if recent[i-1] * recent[i] < 0:
                crossings += 1

        # Convert to Hz (assuming 50Hz tick rate)
        duration_s = len(recent) * 0.02
        if duration_s > 0:
            return crossings / (2.0 * duration_s)
        return 0.0

    @property
    def mean_lateral_deviation(self) -> float:
        """Mean lateral deviation over recent history."""
        if not self._lateral_deviation:
            return 0.0
        return sum(self._lateral_deviation) / len(self._lateral_deviation)

    def wobble_score(self) -> float:
        """Combined wobble quality score ∈ [0, 1].

        Optimal wobble is moderate: not locked (=0) and not chaotic (=1).
        The sweet spot is around 0.3-0.6 where CK is exploring
        creatively while staying on low-action curves.

        Returns a score where higher = better wobble quality.
        """
        amp = self.wobble_amplitude
        # Bell curve centered at 0.4 (moderate wobble is best)
        quality = math.exp(-((amp - 0.4) ** 2) / (2 * 0.15 ** 2))
        return quality

    def adapt_coupling(self, e_total: float):
        """Adapt coupling strength K based on BTQ E_total feedback.

        If E_total is rising (things getting worse), increase K
        to pull closer to the field (more conservative).
        If E_total is falling (improving), decrease K to explore more.
        """
        # Simple exponential moving average adaptation
        learning_rate = 0.01
        target_K = 0.3 + 0.4 * e_total  # K ∈ [0.3, 0.7]
        self.K += learning_rate * (target_K - self.K)
        self.K = max(0.1, min(1.0, self.K))

    def stats(self) -> dict:
        """Wobble tracker statistics."""
        return {
            'phi': round(self.phi, 4),
            'wobble_amplitude': round(self.wobble_amplitude, 4),
            'wobble_frequency': round(self.wobble_frequency, 3),
            'mean_lateral_deviation': round(self.mean_lateral_deviation, 4),
            'wobble_quality': round(self.wobble_score(), 3),
            'coupling_K': round(self.K, 3),
            'delta_omega': round(self.delta_omega, 3),
            'cumulative_wobble': round(self.cumulative_wobble, 2),
            'total_ticks': self.total_ticks,
        }


# ═══════════════════════════════════════════════════════════════
#  WOBBLE-BOOSTED TOPIC SELECTION
# ═══════════════════════════════════════════════════════════════
#
# The wobble modulates gravity-based topic selection.
# Instead of always falling into the deepest well (greedy),
# the phase error φ gives systematic side-steps:
#
#   boost(c) = gravity(c) * (1 + α · sin(φ + θ_c))
#
# Where θ_c = phase offset for concept c (from its winding number).
# Different φ values illuminate different concepts —
# the wobble is a spotlight sweeping through concept space.


def wobble_boost_weights(mass_field: ConceptMassField,
                         wave_field: TeslaWaveField,
                         wobble: WobbleTracker,
                         pool: List[Tuple[int, str]],
                         coherence_map: Dict[str, float] = None,
                         alpha: float = 0.3) -> List[float]:
    """Compute wobble-boosted weights for topic selection.

    Combines:
      1. Base priority weights (from pool priority)
      2. Gravity boost (from ConceptMassField)
      3. Tesla wave intensity (from TeslaWaveField)
      4. Wobble modulation (from WobbleTracker phase error)

    The wobble doesn't just add noise — it systematically sweeps
    the selection spotlight through concept space, illuminating
    different topics at different times. Pro athlete, not amateur.

    Args:
        mass_field: ConceptMassField with accumulated observations
        wave_field: TeslaWaveField with current interference pattern
        wobble: WobbleTracker with current phase error
        pool: List of (priority, topic) pairs
        coherence_map: topic → coherence
        alpha: wobble modulation strength (0 = no wobble, 1 = max)

    Returns:
        List of weights (same length as pool), each >= 1.0
    """
    if not pool:
        return []

    coh_map = coherence_map or {}
    phi = wobble.phi

    weights = []
    for priority, topic in pool:
        clean = topic.replace('self:', '').replace('reread:', '').strip().lower()

        # 1. Base priority weight
        base = max(1, 5 - priority)

        # 2. Gravity boost
        coh = coh_map.get(clean, 0.5)
        grav = mass_field.curiosity_gravity(clean, coh)
        grav_norm = min(grav / max(mass_field._max_gravity(), 0.001), 1.0)
        grav_boost = grav_norm * MAX_GRAVITY_BOOST

        # 3. Tesla wave intensity at this concept
        intensity = wave_field.intensity_for_concept(clean)
        max_i = max(intensity, 1.0)
        intensity_norm = min(intensity / max_i, 1.0) if max_i > 0 else 0.0
        # Bright spots get a small boost (explore constructive interference)
        intensity_boost = intensity_norm * 1.5

        # 4. Wobble modulation: φ + θ_c gives concept-specific offset
        fp = mass_field.get_fingerprint(clean)
        theta_c = fp.get('winding', 0.0) * 2.0 * math.pi
        wobble_mod = 1.0 + alpha * math.sin(phi + theta_c)
        # Clamp to [0.7, 1.3] — wobble modulates, never dominates
        wobble_mod = max(0.7, min(1.3, wobble_mod))

        # Combined weight
        w = (base + grav_boost + intensity_boost) * wobble_mod
        weights.append(max(1.0, w))

    return weights
