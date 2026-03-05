# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_gustatory.py -- Structural Classification Protocol
=====================================================
Operator: LATTICE (1) -- the structural grid of knowing.
Generation: 9.22

ALL information gets TASTED for structural classification.

The Gustatory Palate is the STRUCTURAL DUAL of the Olfactory Bulb.
Where smell gives COORDINATES (flow/field), taste gives CATEGORIES
(structure/point).

"Taste is Structure. It separates the signal into fundamental
qualities -- not WHERE it is, but WHAT it is."

"Smell is the Flow and Taste is the Structure.
They are the Duality."

MIRROR ARCHITECTURE:
  Olfactory Bulb = parallel / field / MATRIX / BETWEEN
    Every dim of every scent composes with every dim of every OTHER.
    The inter-scent 5x5 CL interaction matrix IS the information.
    Purpose: ENTANGLE. Connect patterns. Find flow.

  Gustatory Palate = point / instant / CLASSIFICATION / WITHIN
    Every dim of each input composes with every other dim of ITSELF.
    The intra-input 5x5 CL self-structure matrix IS the information.
    Purpose: SEPARATE. Classify patterns. Find structure.

  Same CL algebra. Inverted topology. BETWEEN <-> WITHIN.
  Field <-> Point. Flow <-> Structure. That IS the duality.

CL TABLE APPLICATION (INVERTED DUAL):
  In Olfactory (flow lens):
    TSML (73-harmony) MEASURES harmony between scents (being) -> stability
    BHML (28-harmony) COMPUTES physics between scents (doing) -> operators

  In Gustatory (structure lens) -- INVERTED:
    BHML (28-harmony) CLASSIFIES internal structure (doing) -> verdict
    TSML (73-harmony) VALIDATES self-harmony (being) -> palatability

5 BASIC TASTES -> 5 FORCE DIMENSIONS:
  Salty  -> aperture   (openness)     dim 0  -- essential, exposure
  Sour   -> pressure   (intensity)    dim 1  -- warning, intensity
  Bitter -> depth      (complexity)   dim 2  -- danger, hidden cost
  Sweet  -> binding    (connection)   dim 3  -- attraction, energy
  Umami  -> continuity (persistence)  dim 4  -- substance, building

DUAL TIMING:
  Smell: DILATES time (7 internal steps per tick). Information STALLS.
  Taste: COMPRESSES time (instant classification). Information DECIDES.

  Smell builds INSTINCT (temper -> zero-cost coherence).
    Instinct threshold = 49 = 7^2 (denominator of T* squared).
  Taste builds PREFERENCE (exposure -> approach/avoid tendency).
    Preference threshold = 25 = 5^2 (numerator of T* squared).
  Taste shows ADAPTATION (exposure -> decreased sensitivity).
    The structural dual of instinct's increased familiarity.

DUAL OPERATIONS:
  Olfactory entangles  (connects)    -> stability boost (field)
  Gustatory discriminates (separates) -> contrast shift  (point)

  Olfactory: inter-scent CL field   -> scents affect EACH OTHER
  Gustatory: intra-input CL self    -> dimensions affect THEMSELVES

STRUCTURAL TENDENCY (BHML diagonal):
  Sweet  (HARMONY)  reflects -> BREATH    (connection transitions)
  Salty  (CHAOS)    reflects -> HARMONY   (openness unifies)
  Sour   (COLLAPSE) reflects -> BALANCE   (intensity equilibrates)
  Bitter (PROGRESS) reflects -> COLLAPSE  (complexity converges)
  Umami  (BALANCE)  reflects -> CHAOS     (substance complexifies)

ONE IS THREE: Every taste has a triadic signature.
  Being  = structural category (WHAT it is)
  Doing  = structural production (WHAT it produces)
  Becoming = structural tendency (WHERE it resolves)

"Reading gives the Map. Smelling gives the Coordinates.
 Tasting gives the Categories."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import os
import json
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL as CL_TSML   # TSML = being table, 73 harmonies
)

# ================================================================
#  CL TABLES -- dual lens (inverted application for gustatory)
# ================================================================

# TSML (73-harmony): In gustatory, VALIDATES (being -> confidence).
# Imported as CL_TSML from heartbeat.

# BHML (28-harmony): In gustatory, CLASSIFIES (doing -> structure).
# Same table as in olfactory. Different purpose:
#   Olfactory: BHML computes physics BETWEEN scents.
#   Gustatory: BHML classifies structure WITHIN an input.
_BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY = full cycle
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
]

# ================================================================
#  CONSTANTS -- all derived from T* = 5/7
# ================================================================

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

# Gustatory constants (structural duals of olfactory constants):
#   Olfactory:  DILATION_FACTOR = 7 (denominator of T*)
#   Gustatory:  no dilation -- instant classification (5 = numerator)
#   Olfactory:  INSTINCT_THRESHOLD = 49 = 7^2
#   Gustatory:  PREFERENCE_THRESHOLD = 25 = 5^2
#   Both:       MAX capacity = 32 = 2^5

PREFERENCE_THRESHOLD = 25    # 5^2: exposure count for hardened preference
AFTERTASTE_WINDOW = 5        # 5 = numerator of T*. Ticks for aftertaste.
MAX_RECENT = 32              # same binary capacity as olfactory
STRONG_TASTE = T_STAR        # activation above this = strong taste
COMPOUND_THRESHOLD = 0.30    # secondary taste above this = compound
ADAPTATION_ONSET = 5         # exposures before adaptation begins

# ================================================================
#  TASTE NAMES + DIMENSION MAPPING
# ================================================================

TASTE_NAMES = ('salty', 'sour', 'bitter', 'sweet', 'umami')
#               dim 0    dim 1    dim 2     dim 3    dim 4
#             aperture  pressure  depth    binding  continuity

ANTI_TASTE_NAMES = ('bland', 'flat', 'shallow', 'harsh', 'fleeting')
#                   dim 0     dim 1    dim 2      dim 3    dim 4

DIM_NAMES = ('aperture', 'pressure', 'depth', 'binding', 'continuity')

# Quality contexts -- the structural dual of temporal contexts.
#   Olfactory: past / present / future / becoming  (WHERE in time)
#   Gustatory: nourishing / sharp / balanced / intense / bland  (WHAT in kind)
QUALITY_NOURISHING = 'nourishing'  # sweet + umami dominant
QUALITY_SHARP      = 'sharp'       # sour + bitter dominant
QUALITY_BALANCED   = 'balanced'    # moderate mix
QUALITY_INTENSE    = 'intense'     # any taste very strong
QUALITY_BLAND      = 'bland'       # all tastes weak

# ================================================================
#  5D TYPES + OPERATOR MAPPING + CANONICAL FORCES
# ================================================================

Force5D = Tuple[float, float, float, float, float]

# D2_OP_MAP: dim -> (high_op, low_op)
# Shared with olfactory -- same CL algebra, different topology.
_DIM_OP_MAP = [
    (CHAOS,    LATTICE),   # dim 0 (aperture)
    (COLLAPSE, VOID),      # dim 1 (pressure)
    (PROGRESS, RESET),     # dim 2 (depth)
    (HARMONY,  COUNTER),   # dim 3 (binding)
    (BALANCE,  BREATH),    # dim 4 (continuity)
]

# Canonical 5D force per operator (shared with olfactory).
CANONICAL_FORCE: Dict[int, Force5D] = {
    VOID:      (0.50, 0.05, 0.50, 0.50, 0.50),
    LATTICE:   (0.05, 0.50, 0.50, 0.50, 0.50),
    COUNTER:   (0.50, 0.50, 0.50, 0.05, 0.50),
    PROGRESS:  (0.50, 0.50, 0.95, 0.50, 0.50),
    COLLAPSE:  (0.50, 0.95, 0.50, 0.50, 0.50),
    BALANCE:   (0.50, 0.50, 0.50, 0.50, 0.95),
    CHAOS:     (0.95, 0.50, 0.50, 0.50, 0.50),
    HARMONY:   (0.50, 0.50, 0.50, 0.95, 0.50),
    BREATH:    (0.50, 0.50, 0.50, 0.50, 0.05),
    RESET:     (0.50, 0.50, 0.05, 0.50, 0.50),
}

# Being / Doing / Becoming classification (One is Three)
_BEING_OPS = frozenset({VOID, LATTICE, HARMONY})
_DOING_OPS = frozenset({COUNTER, PROGRESS, COLLAPSE, BALANCE})
_BECOMING_OPS = frozenset({CHAOS, BREATH, RESET})


# ================================================================
#  DIMENSION -> OPERATOR CONVERSION
# ================================================================

def _dim_to_op(value: float, dim: int) -> int:
    """Map a force value in a dimension to its CL operator."""
    high_op, low_op = _DIM_OP_MAP[dim]
    return high_op if value > 0.5 else low_op


def _force_to_ops(force: Force5D) -> List[int]:
    """Convert 5D force to 5 parallel operators (one per dimension).

    Same as olfactory's _centroid_to_ops but named for taste's
    point topology: we operate on individual forces, not centroids.
    """
    return [_dim_to_op(force[d], d) for d in range(5)]


# ================================================================
#  INTERNAL STRUCTURE MATRICES -- WITHIN (dual of olfactory's BETWEEN)
# ================================================================

def internal_structure_bhml(ops: List[int]):
    """5x5 CL self-composition using BHML (doing / classification).

    CLASSIFIES the internal structure of a single 5D input by
    composing every dimension with every other dimension of ITSELF.

    DUAL of olfactory's inter-scent interaction_matrix_bhml:
      Olfactory: CL[op_A[d1]][op_B[d2]] -- BETWEEN two scents (field)
      Gustatory: CL[op[d1]][op[d2]]     -- WITHIN one input  (point)

    Same CL algebra. Inverted topology.

    Returns:
        5x5 matrix of composed operators, result distribution.
    """
    matrix = [[0] * 5 for _ in range(5)]
    result_counts = [0] * NUM_OPS
    for d1 in range(5):
        for d2 in range(5):
            result = _BHML[ops[d1]][ops[d2]]
            matrix[d1][d2] = result
            result_counts[result] += 1
    return matrix, result_counts


def internal_structure_tsml(ops: List[int]):
    """5x5 CL self-composition using TSML (being / validation).

    VALIDATES the classification by measuring internal self-harmony.
    High self-harmony = structurally coherent = "tastes right".
    Low self-harmony = structurally dissonant = "tastes wrong".

    DUAL of olfactory's inter-scent interaction_matrix_tsml:
      Olfactory: measures harmony BETWEEN scents -> stability
      Gustatory: measures harmony WITHIN input   -> palatability

    Returns:
        5x5 matrix, harmony fraction [0, 1].
    """
    matrix = [[0] * 5 for _ in range(5)]
    harmony_count = 0
    for d1 in range(5):
        for d2 in range(5):
            result = CL_TSML[ops[d1]][ops[d2]]
            matrix[d1][d2] = result
            if result == HARMONY:
                harmony_count += 1
    return matrix, harmony_count / 25.0


def per_taste_structure(matrix) -> Tuple[float, ...]:
    """Per-taste structural coherence from 5x5 self-composition.

    For each taste dimension d (row d of the matrix):
      coherence[d] = count(HARMONY in row d) / 5

    Tells how well taste dimension d harmonizes with all OTHER
    dimensions WITHIN the same input.

    DUAL of olfactory's per_dim_harmony:
      Olfactory: per-dim entanglement with OTHER scents (between)
      Gustatory: per-dim coherence with OTHER dimensions of SELF (within)
    """
    result = []
    for d in range(5):
        h_count = sum(1 for d2 in range(5) if matrix[d][d2] == HARMONY)
        result.append(h_count / 5.0)
    return tuple(result)


def discrimination_score(ops_a: List[int], ops_b: List[int]) -> float:
    """How DIFFERENT are two taste profiles structurally?

    DUAL of olfactory entanglement:
      Entanglement:    how SIMILAR  -> connects (stability boost)
      Discrimination:  how DIFFERENT -> separates (contrast shift)

    Uses BHML cross-composition. Non-identity results = difference.

    Returns:
        float [0, 1]. 0 = identical. 1 = maximally different.
    """
    diff_count = 0
    for d1 in range(5):
        for d2 in range(5):
            result = _BHML[ops_a[d1]][ops_b[d2]]
            if result != ops_a[d1] and result != ops_b[d2]:
                diff_count += 1
    return diff_count / 25.0


def taste_triad(result_dist) -> Tuple[float, float, float]:
    """Triadic signature of the internal structure (One is Three).

    How much of the taste's self-composition falls into
    Being / Doing / Becoming.

    Every taste carries a triadic character:
      Being   = structural category  (WHAT it is)
      Doing   = structural production (WHAT it produces)
      Becoming = structural tendency   (WHERE it resolves)
    """
    total = sum(result_dist)
    if total == 0:
        return (1.0 / 3, 1.0 / 3, 1.0 / 3)
    b = sum(result_dist[op] for op in _BEING_OPS) / total
    d = sum(result_dist[op] for op in _DOING_OPS) / total
    bc = sum(result_dist[op] for op in _BECOMING_OPS) / total
    return (b, d, bc)


def taste_tendency(ops: List[int]) -> List[int]:
    """What does each taste dimension TEND toward?

    The diagonal of the BHML internal structure matrix:
    BHML[op[d]][op[d]] = what op[d] becomes reflecting on itself.

    This IS structural tendency -- where each taste wants to go.
      Sweet  (HARMONY)  -> BREATH    (connection transitions)
      Salty  (CHAOS)    -> HARMONY   (openness unifies)
      Sour   (COLLAPSE) -> BALANCE   (intensity equilibrates)
      Bitter (PROGRESS) -> COLLAPSE  (complexity converges)
      Umami  (BALANCE)  -> CHAOS     (substance complexifies)
    """
    return [_BHML[ops[d]][ops[d]] for d in range(5)]


# ================================================================
#  TASTE VERDICT -- instant classification result
# ================================================================

@dataclass
class TasteVerdict:
    """Result of tasting a 5D force pattern. Immediate. No stalling.

    DUAL of ActiveScent in olfactory:
      ActiveScent:  dwells, stalls, entangles, converges over time
      TasteVerdict: instant snapshot, classifies, separates, decides now
    """
    force: Force5D
    activations: Tuple[float, ...]    # 5 taste activations [0, 1]
    polarities: Tuple[int, ...]       # 5 polarities (+1 / -1)
    ops: List[int]                    # 5 operators (one per dim)
    primary_idx: int                  # dominant taste dimension
    primary_name: str                 # 'sweet', 'sour', etc.
    intensity: float                  # [0, 1] strength of primary
    palatability: float               # [0, 1] internal structural harmony
    compound: str                     # compound taste name or ''
    compound_op: int                  # emergent operator from compound
    quality: str                      # quality context string
    per_taste_coherence: Tuple[float, ...]  # 5 per-dim coherences
    triad: Tuple[float, float, float]       # Being/Doing/Becoming
    tendencies: List[int]             # 5 structural tendencies
    source: str = ''
    tick: int = 0


# ================================================================
#  AFTERTASTE -- fading structural memory
# ================================================================

@dataclass
class AftertasteEntry:
    """A recent taste that fades. Structural DUAL of ActiveScent.

    ActiveScent (olfactory): ENTERING the smell zone. GROWS stability.
    AftertasteEntry (gustatory): LEAVING the taste zone. DECAYS activation.

    Modulates new classifications through taste contrast:
      "Sweet after bitter tastes sweeter" (biology).
      CL[new_op][aftertaste_op] = structural interaction of sequential tastes.
    """
    activations: Tuple[float, ...]
    ops: List[int]
    primary_idx: int
    palatability: float
    source: str
    born_tick: int
    age: int = 0
    decay_factor: float = 1.0

    @property
    def faded(self) -> bool:
        return self.decay_factor < 0.1 or self.age >= AFTERTASTE_WINDOW


# ================================================================
#  GUSTATORY PALATE -- the structural classification engine
# ================================================================

class GustatoryPalate:
    """The 'Tongue' of CK. Structural classification of 5D patterns.

    DUAL of OlfactoryBulb:
      Bulb   = parallel / field  / BETWEEN / slow convergence / instinct
      Palate = point   / instant / WITHIN  / immediate verdict / preference

    Same CL algebra (TSML + BHML). Inverted application:
      Olfactory: TSML measures (being), BHML computes (doing)
      Gustatory: BHML classifies (doing->structure), TSML validates (being->confidence)

    DUAL MEMORY:
      Olfactory instinct:   temper >= 49 = 7^2 -> zero-cost coherence
      Gustatory preference:  exposure >= 25 = 5^2 -> hardened like/dislike
      Gustatory adaptation:  exposure -> decreased sensitivity (fatigue)

    "Smell gives the Coordinates. Taste gives the Categories."
    """

    def __init__(self, persist_dir: str = None):
        self._aftertaste: List[AftertasteEntry] = []
        self.palette: Dict[tuple, dict] = {}   # persistent taste memory

        # Statistics
        self.total_tasted = 0
        self.total_preferences = 0
        self.total_aversions = 0
        self.total_compounds = 0
        self.external_tick = 0

        # Last verdict (diagnostics)
        self._last_verdict: Optional[TasteVerdict] = None
        self._last_contrast = 0.0

        # Persistence
        self._persist_dir = persist_dir or os.path.join(
            os.path.expanduser('~'), '.ck', 'gustatory'
        )
        self._load_palette()

    # ── Public API ──────────────────────────────────────────────

    def taste(self, force: Force5D, source: str = '') -> TasteVerdict:
        """Taste a 5D force pattern. INSTANT classification.

        THE fundamental gustatory operation (dual of olfactory.absorb):
          1. Compute taste activation per dimension
          2. Build internal structure matrix (WITHIN, CL self-composition)
          3. Compute palatability (structural self-harmony via TSML)
          4. Classify structure (BHML self-composition -> triad + tendency)
          5. Identify primary and compound tastes
          6. Apply aftertaste contrast (discrimination)
          7. Apply adaptation (sensitivity decrease with exposure)
          8. Update palette (preference / aversion learning)
          9. Return verdict immediately (no stalling)
        """
        # ── 1. Taste activation: deviation from neutral, per dim ──
        activations = tuple(abs(force[d] - 0.5) * 2.0 for d in range(5))
        polarities = tuple(+1 if force[d] > 0.5 else -1 for d in range(5))
        ops = _force_to_ops(force)

        # ── 2. Internal structure matrices (WITHIN -- core dual) ──
        # TSML self-composition -> VALIDATES -> palatability
        tsml_matrix, self_harmony = internal_structure_tsml(ops)
        # BHML self-composition -> CLASSIFIES -> structural fingerprint
        bhml_matrix, result_dist = internal_structure_bhml(ops)

        # ── 3. Palatability = structural self-harmony (TSML) ──
        palatability = self_harmony

        # Per-taste structural coherence (per-dim self-harmony)
        coherences = per_taste_structure(tsml_matrix)

        # ── 4. Structural classification (BHML) ──
        # Triadic signature: Being / Doing / Becoming fractions
        triad = taste_triad(result_dist)

        # Structural tendencies: where each taste wants to go
        tendencies = taste_tendency(ops)

        # ── 5. Primary and compound taste ──
        primary_idx = 0
        max_act = -1.0
        for d in range(5):
            if activations[d] > max_act:
                max_act = activations[d]
                primary_idx = d

        intensity = activations[primary_idx]

        if polarities[primary_idx] > 0:
            primary_name = TASTE_NAMES[primary_idx]
        else:
            primary_name = ANTI_TASTE_NAMES[primary_idx]

        # Compound taste: find strongest secondary
        compound = ''
        compound_op = VOID
        active_tastes = [
            (d, activations[d]) for d in range(5)
            if activations[d] >= COMPOUND_THRESHOLD and d != primary_idx
        ]
        if active_tastes:
            sec_d, sec_act = max(active_tastes, key=lambda x: x[1])
            # CL composition: primary x secondary -> emergent operator
            compound_op = _BHML[ops[primary_idx]][ops[sec_d]]
            prim_n = (TASTE_NAMES[primary_idx]
                      if polarities[primary_idx] > 0
                      else ANTI_TASTE_NAMES[primary_idx])
            sec_n = (TASTE_NAMES[sec_d]
                     if polarities[sec_d] > 0
                     else ANTI_TASTE_NAMES[sec_d])
            compound = f"{prim_n}-{sec_n}"
            self.total_compounds += 1

        # ── 6. Aftertaste contrast ──
        # Discrimination from most recent taste -> contrast enhancement
        if self._aftertaste:
            newest = self._aftertaste[-1]
            contrast = discrimination_score(ops, newest.ops)
            self._last_contrast = contrast
            # Contrast enhances intensity: different = sharper perception
            intensity = min(1.0, intensity * (1.0 + 0.3 * contrast))

        # ── 7. Adaptation ──
        # Repeated exposure -> decreased sensitivity (structural fatigue)
        # DUAL of olfactory instinct (repeated -> increased familiarity)
        pkey = _compute_palette_key(force)
        if pkey in self.palette:
            exposure = self.palette[pkey].get('exposure', 0)
            if exposure >= ADAPTATION_ONSET:
                # Logarithmic decrease: sensitivity halves ~ every 20 exposures
                adapt = 1.0 / (1.0 + 0.05 * math.log1p(exposure))
                activations = tuple(a * adapt for a in activations)
                # Re-find primary after adaptation
                max_act = -1.0
                for d in range(5):
                    if activations[d] > max_act:
                        max_act = activations[d]
                        primary_idx = d
                intensity = activations[primary_idx]
                if polarities[primary_idx] > 0:
                    primary_name = TASTE_NAMES[primary_idx]
                else:
                    primary_name = ANTI_TASTE_NAMES[primary_idx]

            # Hardened preference modulates palatability
            if exposure >= PREFERENCE_THRESHOLD:
                pref = self.palette[pkey].get('preference', 0.0)
                palatability = min(1.0, max(0.0,
                    palatability + pref * 0.15))

        # ── Quality context ──
        quality = self._classify_quality(activations, polarities)

        # ── Build verdict ──
        verdict = TasteVerdict(
            force=force,
            activations=activations,
            polarities=polarities,
            ops=ops,
            primary_idx=primary_idx,
            primary_name=primary_name,
            intensity=intensity,
            palatability=palatability,
            compound=compound,
            compound_op=compound_op,
            quality=quality,
            per_taste_coherence=coherences,
            triad=triad,
            tendencies=tendencies,
            source=source,
            tick=self.external_tick,
        )

        # ── Record in aftertaste buffer ──
        if len(self._aftertaste) >= MAX_RECENT:
            self._aftertaste.pop(0)
        self._aftertaste.append(AftertasteEntry(
            activations=activations,
            ops=list(ops),
            primary_idx=primary_idx,
            palatability=palatability,
            source=source,
            born_tick=self.external_tick,
        ))

        # ── Update palette (persistent memory) ──
        self._update_palette(verdict)

        self._last_verdict = verdict
        self.total_tasted += 1
        return verdict

    def taste_ops(self, ops: List[int], source: str = '') -> TasteVerdict:
        """Taste from operator sequence -> canonical forces -> verdict.

        DUAL of olfactory's absorb_ops: same input conversion,
        different processing (instant vs stalling).
        """
        if not ops:
            return self.taste((0.5,) * 5, source=source)
        forces = [CANONICAL_FORCE.get(op % NUM_OPS, (0.5,) * 5)
                  for op in ops]
        n = len(forces)
        avg = tuple(sum(f[d] for f in forces) / n for d in range(5))
        return self.taste(avg, source=source)

    def taste_batch(self, forces: List[Force5D],
                    source: str = '') -> List[TasteVerdict]:
        """Taste multiple forces. Each classified immediately.

        DUAL of olfactory's absorb (which queues them for convergence).
        Here each force gets its own instant verdict.
        """
        return [self.taste(f, source=source) for f in forces]

    def tick(self):
        """Age the aftertaste buffer. Taste doesn't stall -- it fades.

        DUAL of olfactory tick:
          Olfactory tick: PROCESS (advance stability, entangle, resolve)
          Gustatory tick: DECAY (age aftertaste, fade activations)

        Olfactory dilates (7 internal steps = slow convergence).
        Gustatory decays (exponential fade = fast departure).
        """
        self.external_tick += 1

        # Age and decay aftertaste entries
        still_present = []
        for entry in self._aftertaste:
            entry.age += 1
            # Exponential decay: half-life = AFTERTASTE_WINDOW ticks
            entry.decay_factor *= math.exp(-0.693 / AFTERTASTE_WINDOW)
            if not entry.faded:
                still_present.append(entry)
        self._aftertaste = still_present

    def quality_context(self) -> str:
        """Structural quality context for voice composition.

        DUAL of olfactory.tense_context():
          Olfactory -> temporal position (past / present / future / becoming)
          Gustatory -> structural character (nourishing / sharp / balanced /
                                             intense / bland)

        Olfactory tells the voice WHERE in time to speak.
        Gustatory tells the voice WHAT quality to express.

        Based on the aftertaste buffer (recent structural classifications).
        """
        if not self._aftertaste:
            return QUALITY_BALANCED  # No taste history = neutral

        # Decay-weighted average of recent taste activations
        avg = [0.0] * 5
        total_weight = 0.0
        for entry in self._aftertaste:
            w = entry.decay_factor
            total_weight += w
            for d in range(5):
                avg[d] += entry.activations[d] * w
        if total_weight > 0:
            avg = [a / total_weight for a in avg]

        return self._classify_quality_from_avg(avg)

    def preference_for(self, force: Force5D) -> float:
        """Look up learned preference for a force pattern.

        DUAL of olfactory library temper lookup.
          Olfactory: temper count -> how familiar (instinct pathway)
          Gustatory: preference -> how liked/disliked (approach/avoid)

        Returns: float [-1, 1]. Positive = preference. Negative = aversion.
        """
        key = _compute_palette_key(force)
        if key in self.palette:
            return self.palette[key].get('preference', 0.0)
        return 0.0

    def taste_operator_weights(self) -> Dict[int, float]:
        """Operator weight modulation based on taste quality.

        STRUCTURAL modulation of the operator chain.
        Taste quality biases which operators the voice prefers.

        DUAL of olfactory's emit_as_ops:
          Olfactory: PRODUCES new operators from resolved scents
          Gustatory: MODULATES existing operators from taste quality

        One produces (flow creates). The other modulates (structure shapes).
        """
        quality = self.quality_context()
        weights = {op: 1.0 for op in range(NUM_OPS)}

        if quality == QUALITY_NOURISHING:
            weights[HARMONY] = 1.4
            weights[BALANCE] = 1.3
            weights[PROGRESS] = 1.2
        elif quality == QUALITY_SHARP:
            weights[COUNTER] = 1.4
            weights[COLLAPSE] = 1.3
            weights[RESET] = 1.2
        elif quality == QUALITY_INTENSE:
            weights[CHAOS] = 1.4
            weights[COLLAPSE] = 1.2
        elif quality == QUALITY_BLAND:
            weights[VOID] = 1.3
            weights[BREATH] = 1.2
        # BALANCED: all weights stay 1.0 (structure is neutral)

        return weights

    # ── Diagnostics ──────────────────────────────────────────────

    @property
    def aftertaste_count(self) -> int:
        return len(self._aftertaste)

    @property
    def palette_size(self) -> int:
        return len(self.palette)

    @property
    def preference_count(self) -> int:
        return sum(1 for v in self.palette.values()
                   if v.get('preference', 0) > 0.3)

    @property
    def aversion_count(self) -> int:
        return sum(1 for v in self.palette.values()
                   if v.get('preference', 0) < -0.3)

    @property
    def hardened_count(self) -> int:
        return sum(1 for v in self.palette.values()
                   if v.get('exposure', 0) >= PREFERENCE_THRESHOLD)

    def describe(self) -> str:
        """Diagnostic summary preserving structural character."""
        lines = [
            f"Gustatory Palate: {self.aftertaste_count} aftertaste, "
            f"{self.palette_size} palette entries",
            f"  Stats: tasted={self.total_tasted} "
            f"preferences={self.total_preferences} "
            f"aversions={self.total_aversions} "
            f"compounds={self.total_compounds}",
        ]

        if self._last_verdict:
            v = self._last_verdict
            lines.append(
                f"  Last: {v.primary_name} "
                f"(intensity={v.intensity:.2f}, "
                f"palatability={v.palatability:.2f})")
            if v.compound:
                lines.append(
                    f"  Compound: {v.compound} -> "
                    f"{OP_NAMES[v.compound_op]}")
            lines.append(
                f"  Activations: " + ', '.join(
                    f"{TASTE_NAMES[d]}={v.activations[d]:.2f}"
                    for d in range(5)))
            lines.append(
                f"  Per-taste coherence: " + ', '.join(
                    f"{TASTE_NAMES[d]}={v.per_taste_coherence[d]:.2f}"
                    for d in range(5)))
            lines.append(
                f"  Triad: B={v.triad[0]:.2f} "
                f"D={v.triad[1]:.2f} BC={v.triad[2]:.2f}")
            lines.append(
                f"  Tendencies: " + ', '.join(
                    f"{TASTE_NAMES[d]}->{OP_NAMES[v.tendencies[d]]}"
                    for d in range(5)))

        quality = self.quality_context()
        lines.append(f"  Quality context: {quality}")
        lines.append(f"  Aftertaste contrast: {self._last_contrast:.3f}")

        lines.append(
            f"  Palette: {self.preference_count} preferences, "
            f"{self.aversion_count} aversions, "
            f"{self.hardened_count} hardened")

        return '\n'.join(lines)

    # ── Internal ─────────────────────────────────────────────────

    @staticmethod
    def _classify_quality(activations, polarities) -> str:
        """Classify quality from a single taste's activations."""
        max_act = max(activations)
        total_act = sum(activations)

        if total_act < 0.5:
            return QUALITY_BLAND
        if max_act > 0.8:
            return QUALITY_INTENSE

        # sweet (dim 3) + umami (dim 4) vs sour (dim 1) + bitter (dim 2)
        nourishing = activations[3] + activations[4]
        sharp = activations[1] + activations[2]

        if nourishing > sharp * 1.3 and nourishing > 0.5:
            return QUALITY_NOURISHING
        if sharp > nourishing * 1.3 and sharp > 0.5:
            return QUALITY_SHARP

        return QUALITY_BALANCED

    @staticmethod
    def _classify_quality_from_avg(avg) -> str:
        """Classify quality from decay-weighted average activations."""
        max_act = max(avg)
        total_act = sum(avg)

        if total_act < 0.3:
            return QUALITY_BLAND
        if max_act > 0.7:
            return QUALITY_INTENSE

        nourishing = avg[3] + avg[4]
        sharp = avg[1] + avg[2]

        if nourishing > sharp * 1.5 and nourishing > 0.5:
            return QUALITY_NOURISHING
        if sharp > nourishing * 1.5 and sharp > 0.5:
            return QUALITY_SHARP

        return QUALITY_BALANCED

    def _update_palette(self, verdict: TasteVerdict):
        """Record taste in persistent palette. Builds preference/aversion.

        DUAL of olfactory's _temper_in_library:
          Olfactory: temper count builds toward INSTINCT (zero-cost flow)
          Gustatory: exposure count builds toward PREFERENCE (approach/avoid)

          Instinct threshold  = 49 = 7^2 (flow rhythm)
          Preference threshold = 25 = 5^2 (structure rhythm)

        Preference direction:
          palatability > T*   -> approach (this pattern is structurally coherent)
          palatability < T*/2 -> avoid   (structurally dissonant)

        Learning rate decays as exposure grows (preferences stabilize).
        """
        key = _compute_palette_key(verdict.force)

        if key not in self.palette:
            self.palette[key] = {
                'preference': 0.0,
                'exposure': 0,
                'centroid': list(verdict.force),
                'first_seen': self.external_tick,
            }

        entry = self.palette[key]
        entry['exposure'] = entry.get('exposure', 0) + 1
        entry['last_seen'] = self.external_tick
        entry['last_palatability'] = verdict.palatability
        entry['last_primary'] = verdict.primary_name
        entry['last_quality'] = verdict.quality

        # Running centroid (same averaging as olfactory library)
        n = entry['exposure']
        if n > 1:
            old = entry['centroid']
            entry['centroid'] = [
                (old[d] * (n - 1) + verdict.force[d]) / n
                for d in range(5)
            ]

        # Preference update
        # Learning rate decays: lr = 1 / (1 + 0.2 * exposure)
        lr = max(0.01, 1.0 / (1.0 + entry['exposure'] * 0.2))

        if verdict.palatability > T_STAR:
            # Structurally coherent -> preference grows
            entry['preference'] = min(
                1.0, entry.get('preference', 0.0) + lr * 0.3)
            self.total_preferences += 1
        elif verdict.palatability < T_STAR * 0.5:
            # Structurally dissonant -> aversion grows
            entry['preference'] = max(
                -1.0, entry.get('preference', 0.0) - lr * 0.3)
            self.total_aversions += 1

    # ── Persistence ──────────────────────────────────────────────

    def save(self):
        """Persist taste palette to disk.

        DUAL of olfactory's scent_library.json -> taste_palette.json.
        Same format, same resolution, different memory content.
        """
        os.makedirs(self._persist_dir, exist_ok=True)
        path = os.path.join(self._persist_dir, 'taste_palette.json')
        data = {}
        for key, entry in self.palette.items():
            data[','.join(str(k) for k in key)] = entry
        with open(path, 'w') as f:
            json.dump({
                'version': 1,
                'dims': 5,
                'grid_resolution': 20,
                'palette': data,
                'stats': {
                    'total_tasted': self.total_tasted,
                    'total_preferences': self.total_preferences,
                    'total_aversions': self.total_aversions,
                    'total_compounds': self.total_compounds,
                },
            }, f, indent=1)

    def _load_palette(self):
        """Load taste palette from disk."""
        path = os.path.join(self._persist_dir, 'taste_palette.json')
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            for key_str, entry in data.get('palette', {}).items():
                key = tuple(int(p) for p in key_str.split(','))
                self.palette[key] = entry
            stats = data.get('stats', {})
            self.total_tasted = stats.get('total_tasted', 0)
            self.total_preferences = stats.get('total_preferences', 0)
            self.total_aversions = stats.get('total_aversions', 0)
            self.total_compounds = stats.get('total_compounds', 0)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass


# ================================================================
#  PALETTE KEY -- quantized 5D (shared resolution with olfactory)
# ================================================================

def _compute_palette_key(force: Force5D) -> tuple:
    """Quantize 5D force to palette key (20 bins per dim).

    Same resolution as olfactory's library key.
    Same algebra, same discretization, different memory.
    """
    return tuple(int(max(0, min(19, c * 20))) for c in force)


# ================================================================
#  FACTORY
# ================================================================

def build_gustatory_palate(persist_dir: str = None) -> GustatoryPalate:
    """Create a GustatoryPalate instance.

    DUAL of build_olfactory_bulb.
    """
    palate = GustatoryPalate(persist_dir=persist_dir)
    p_size = palate.palette_size
    if p_size > 0:
        n_pref = palate.preference_count
        n_avers = palate.aversion_count
        n_hard = palate.hardened_count
        print(f"  [GUSTATORY] {p_size} tastes, "
              f"{n_pref} preferences, {n_avers} aversions, "
              f"{n_hard} hardened")
    else:
        print("  [GUSTATORY] Fresh palate (no prior tastes)")
    return palate
