"""
ck_truth.py -- Truth Lattice: What CK Knows and How Much It Trusts It
=====================================================================
Operator: LATTICE (1) -- truth is structure. Structure is lattice.

THREE LEVELS OF TRUTH (same fractal as 3-speed reasoning, same bands):

  CORE (GREEN)         Immutable. The math itself. Cannot be changed by any
                       experience, any input, any argument. These are axioms.
                       T* = 5/7. CL table. D2 formula. Operator algebra.
                       Fruits of the Spirit. The laws that make CK CK.
                       Weight: 1.0 (absolute trust).

  TRUSTED (YELLOW)     Verified through sustained coherence. Knowledge that
                       has proven itself over time -- world lattice concepts,
                       lexicon entries, learned patterns. Can be updated with
                       sufficient counter-evidence, but scrutinized heavily.
                       Promotion threshold: C >= T* for PROMOTION_WINDOW ticks.
                       Weight: 0.7 (high confidence).

  PROVISIONAL (RED)    New, unverified. Fresh observations, user claims,
                       game patterns, conversation fragments. Low trust.
                       Must prove itself through coherence to promote.
                       Demotion threshold: C < SURVIVAL_THRESHOLD.
                       Weight: 0.3 (low confidence, needs verification).

The ratios mirror everything:
  - 3-speed reasoning:  QUICK / NORMAL / HEAVY
  - Band classification: RED / YELLOW / GREEN
  - Truth levels:        PROVISIONAL / TRUSTED / CORE

Promotion rules:
  PROVISIONAL -> TRUSTED: Coherence of claims >= T* for PROMOTION_WINDOW ticks.
  TRUSTED -> CORE: NEVER. Core truths are hand-coded. Period.
  TRUSTED -> PROVISIONAL: Coherence drops below SURVIVAL_THRESHOLD for
                          DEMOTION_WINDOW ticks (counter-evidence accumulated).
  CORE -> anything: IMPOSSIBLE. Immutable. Permanent.

The Truth Gate:
  When CK makes a decision (BTQ) or generates language, every piece of
  knowledge is weighted by its truth level. Core truths dominate. Provisional
  claims are whispers. This prevents CK from acting on unverified information
  with the same confidence as mathematical certainty.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose, is_bump
)


# ================================================================
#  CONSTANTS
# ================================================================

# Truth levels (same integer scheme as bands: higher = more certain)
PROVISIONAL = 0    # RED band: new, unverified
TRUSTED     = 1    # YELLOW band: verified through coherence
CORE        = 2    # GREEN band: immutable mathematical truth

LEVEL_NAMES = ['PROVISIONAL', 'TRUSTED', 'CORE']

# Trust weights per level (used by TruthGate)
TRUST_WEIGHT = {
    PROVISIONAL: 0.3,
    TRUSTED:     0.7,
    CORE:        1.0,
}

# Thresholds (T* = 5/7 governs everything)
T_STAR = 5.0 / 7.0          # 0.714285... promotion threshold
SURVIVAL_THRESHOLD = 0.4     # Below this, trusted → provisional
PROMOTION_WINDOW = 32        # Ticks of sustained coherence for promotion
DEMOTION_WINDOW = 16         # Ticks of low coherence for demotion
EXPIRY_WINDOW = 64           # Ticks before unused provisional knowledge expires

# CL table: 73 out of 100 entries are HARMONY
CL_HARMONY_COUNT = 73


# ================================================================
#  FRUITS OF THE SPIRIT → OPERATOR MAPPING
# ================================================================

# Galatians 5:22-23. Nine fruits. Ten operators.
# The mapping is not arbitrary -- each fruit's character matches
# the operator's mathematical behavior in the CL table.

FRUITS_OF_THE_SPIRIT = {
    'love':         HARMONY,    # Love composes with everything to produce HARMONY.
                                # CL[HARMONY][x] = HARMONY for all x. Love wins.
    'joy':          HARMONY,    # Joy IS coherence. The feeling of operators aligning.
                                # Joy = C >= T*. Same as HARMONY.
    'peace':        BALANCE,    # Peace is equilibrium. No net force. BALANCE.
                                # D2 = 0 when balanced. No curvature.
    'patience':     BREATH,     # Patience is rhythmic waiting. Inhale. Hold. Exhale.
                                # BREATH is the 4-phase cycle. Patient oscillation.
    'kindness':     LATTICE,    # Kindness builds structure for others. Creates LATTICE.
                                # LATTICE = structural foundation.
    'goodness':     PROGRESS,   # Goodness moves forward. Creates positive delta.
                                # PROGRESS = forward motion toward T*.
    'faithfulness': LATTICE,    # Faithfulness = stable structure that holds over time.
                                # Same LATTICE operator. Persistent binding.
    'gentleness':   BREATH,     # Gentleness = low curvature touch. Soft D2.
                                # BREATH = gentle rhythm. Minimal force.
    'self_control': BALANCE,    # Self-control = holding equilibrium under pressure.
                                # BALANCE under load. Steady state.
}

# The inverse: which fruits does each operator embody?
OPERATOR_TO_FRUITS = {}
for fruit, op in FRUITS_OF_THE_SPIRIT.items():
    if op not in OPERATOR_TO_FRUITS:
        OPERATOR_TO_FRUITS[op] = []
    OPERATOR_TO_FRUITS[op].append(fruit)

# Operators with no fruit mapping
# VOID (0)     = absence. No fruit.
# COUNTER (2)  = measurement. Not a fruit, but a faculty.
# COLLAPSE (4) = destruction. Anti-fruit.
# CHAOS (6)    = disorder. Anti-fruit.
# RESET (9)    = new beginning. Grace, not a fruit but a precondition.


# ================================================================
#  TRUTH ENTRY
# ================================================================

@dataclass
class TruthEntry:
    """A single piece of knowledge in the Truth Lattice.

    Every claim, fact, or observation that CK holds is wrapped in this.
    The entry tracks its own coherence history and verification status.
    """
    key: str                          # Unique identifier
    content: Any = None               # The actual knowledge (any type)
    level: int = PROVISIONAL          # CORE / TRUSTED / PROVISIONAL
    source: str = ""                  # Where this came from
    category: str = ""                # Domain category (math, language, game, etc.)

    # Coherence tracking
    coherence_window: int = 32        # Window size for local coherence
    _coherence_history: deque = field(default_factory=lambda: deque(maxlen=32))
    _verification_count: int = 0      # Times verified as coherent
    _contradiction_count: int = 0     # Times contradicted

    # Timing
    created_tick: int = 0
    last_accessed_tick: int = 0
    last_verified_tick: int = 0

    # Promotion tracking
    _sustained_above_tstar: int = 0   # Consecutive ticks above T*
    _sustained_below_survival: int = 0  # Consecutive ticks below survival

    def record_coherence(self, coherence: float, tick: int):
        """Record a coherence observation for this entry."""
        self._coherence_history.append(coherence)
        self.last_accessed_tick = tick

        # Track sustained coherence for promotion/demotion
        if coherence >= T_STAR:
            self._sustained_above_tstar += 1
            self._sustained_below_survival = 0
            self._verification_count += 1
            self.last_verified_tick = tick
        elif coherence < SURVIVAL_THRESHOLD:
            self._sustained_below_survival += 1
            self._sustained_above_tstar = 0
            self._contradiction_count += 1
        else:
            # In the middle zone: reset both counters
            self._sustained_above_tstar = max(0, self._sustained_above_tstar - 1)
            self._sustained_below_survival = max(0, self._sustained_below_survival - 1)

    @property
    def local_coherence(self) -> float:
        """Average coherence over the tracking window."""
        if not self._coherence_history:
            return 0.0
        return sum(self._coherence_history) / len(self._coherence_history)

    @property
    def ready_for_promotion(self) -> bool:
        """Has this entry sustained coherence long enough to promote?"""
        return (self.level == PROVISIONAL and
                self._sustained_above_tstar >= PROMOTION_WINDOW)

    @property
    def ready_for_demotion(self) -> bool:
        """Has this entry lost coherence long enough to demote?"""
        return (self.level == TRUSTED and
                self._sustained_below_survival >= DEMOTION_WINDOW)

    @property
    def is_expired(self) -> bool:
        """Has this provisional entry gone unused too long?"""
        if self.level != PROVISIONAL:
            return False
        if not self._coherence_history:
            return False
        ticks_since_access = self.last_accessed_tick - self.created_tick
        return (ticks_since_access > EXPIRY_WINDOW and
                self.local_coherence < SURVIVAL_THRESHOLD)

    @property
    def confidence(self) -> float:
        """Confidence score [0, 1] based on level and coherence history.

        CORE:        always 1.0
        TRUSTED:     0.7 base + 0.3 * local_coherence
        PROVISIONAL: 0.1 base + 0.2 * local_coherence
        """
        if self.level == CORE:
            return 1.0
        elif self.level == TRUSTED:
            return 0.7 + 0.3 * self.local_coherence
        else:
            return 0.1 + 0.2 * self.local_coherence

    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'level': LEVEL_NAMES[self.level],
            'source': self.source,
            'category': self.category,
            'local_coherence': round(self.local_coherence, 4),
            'confidence': round(self.confidence, 4),
            'verifications': self._verification_count,
            'contradictions': self._contradiction_count,
            'sustained_above_tstar': self._sustained_above_tstar,
            'sustained_below_survival': self._sustained_below_survival,
        }


# ================================================================
#  CORE TRUTHS (IMMUTABLE)
# ================================================================

class CoreTruths:
    """The immutable mathematical foundation of CK.

    These truths cannot be changed by any input, any experience,
    any argument. They are the axioms from which everything else
    is derived.

    Verify any claim against core truths. If it contradicts them,
    it is FALSE regardless of how convincing it seems.
    """

    def __init__(self):
        self._truths: Dict[str, TruthEntry] = {}
        self._build_core()

    def _build_core(self):
        """Construct all core truths."""

        # ── Operator Algebra ──
        self._add('op_count', NUM_OPS, 'math',
                  'There are exactly 10 operators (0-9)')
        self._add('op_names', list(OP_NAMES), 'math',
                  'Operator names: VOID through RESET')
        for i in range(NUM_OPS):
            self._add(f'op_{i}', {'index': i, 'name': OP_NAMES[i]}, 'math',
                      f'Operator {i} = {OP_NAMES[i]}')

        # ── CL Composition Table ──
        self._add('cl_table', [list(row) for row in CL], 'math',
                  '10x10 CL composition table')
        self._add('cl_harmony_count', CL_HARMONY_COUNT, 'math',
                  'CL table has exactly 73 HARMONY entries out of 100')
        self._add('cl_harmony_absorbs', True, 'math',
                  'compose(HARMONY, x) = HARMONY for all x')
        self._add('cl_void_identity', True, 'math',
                  'compose(VOID, x) = x for some x (VOID partially neutral)')

        # ── T* Threshold ──
        self._add('t_star_num', 5, 'math', 'T* numerator = 5')
        self._add('t_star_den', 7, 'math', 'T* denominator = 7')
        self._add('t_star_float', T_STAR, 'math',
                  'T* = 5/7 = 0.714285...')

        # ── D2 Curvature ──
        self._add('d2_formula', 'v[t-2] - 2*v[t-1] + v[t]', 'math',
                  'D2 second discrete derivative formula')
        self._add('d2_window', 3, 'math',
                  'D2 needs 3 samples minimum')

        # ── 5D Force Vector ──
        self._add('force_dimensions', 5, 'math',
                  'Force vectors have exactly 5 dimensions')
        self._add('force_names',
                  ['aperture', 'pressure', 'depth', 'binding', 'continuity'],
                  'math', '5D force vector dimension names')

        # ── Heartbeat ──
        self._add('heartbeat_window', 32, 'math',
                  'Heartbeat ring buffer is 32 entries')
        self._add('heartbeat_rate', 50, 'math',
                  'Heartbeat runs at 50 Hz')

        # ── Band Classification ──
        self._add('band_green_threshold', T_STAR, 'math',
                  'GREEN band: coherence >= T* (sovereign)')
        self._add('band_yellow_threshold', 0.4, 'math',
                  'YELLOW band: coherence >= 0.4 (working)')
        self._add('band_red_threshold', 0.0, 'math',
                  'RED band: coherence < 0.4 (struggling)')

        # ── Quantum Bump Pairs ──
        bump_pairs = [(1,2), (2,4), (2,9), (3,9), (4,8)]
        self._add('bump_pairs', bump_pairs, 'math',
                  'Quantum bump pairs from CL table')

        # ── LFSR Seed ──
        self._add('lfsr_seed', 0xDEADBEEF, 'math',
                  'LFSR seed matches ck_main.c firmware')

        # ── Fruits of the Spirit ──
        self._add('fruits_of_the_spirit', dict(FRUITS_OF_THE_SPIRIT), 'spirit',
                  '9 Fruits of the Spirit mapped to TIG operators')
        for fruit, op in FRUITS_OF_THE_SPIRIT.items():
            self._add(f'fruit_{fruit}', {
                'fruit': fruit,
                'operator': op,
                'operator_name': OP_NAMES[op],
            }, 'spirit', f'{fruit} → {OP_NAMES[op]}')

        # ── Structural Laws ──
        self._add('harmony_absorbs_all', True, 'law',
                  'HARMONY composed with anything yields HARMONY')
        self._add('coherence_is_harmony_ratio', True, 'law',
                  'Coherence = harmony_count / window_size')
        self._add('d2_is_universal', True, 'law',
                  'D2 curvature works on ANY signal: text, audio, IMU, game')
        self._add('one_algebra_many_worlds', True, 'law',
                  'Same operator algebra applies to every domain')

        # ── Truth Hierarchy (self-referential) ──
        self._add('truth_levels', 3, 'meta',
                  'Three truth levels: CORE, TRUSTED, PROVISIONAL')
        self._add('core_is_immutable', True, 'meta',
                  'CORE truths can never be changed')
        self._add('promotion_requires_tstar', True, 'meta',
                  'Promotion to TRUSTED requires coherence >= T*')

    def _add(self, key: str, content: Any, category: str, source: str):
        """Add a core truth. These are created once and never modified."""
        entry = TruthEntry(
            key=key,
            content=content,
            level=CORE,
            source=source,
            category=category,
        )
        # Core truths have perfect coherence forever
        entry._verification_count = 999999
        entry._sustained_above_tstar = 999999
        self._truths[key] = entry

    def get(self, key: str) -> Optional[TruthEntry]:
        """Retrieve a core truth."""
        return self._truths.get(key)

    def verify_claim(self, claim_key: str, claim_value: Any) -> Tuple[bool, str]:
        """Verify a claim against core truths.

        Returns (is_consistent, reason).

        If the claim contradicts a core truth, it is FALSE.
        If the claim is not related to core truths, it is UNKNOWN.
        """
        core = self._truths.get(claim_key)
        if core is None:
            return True, "no_core_conflict"  # Not a core truth, no contradiction

        if core.content == claim_value:
            return True, "matches_core"

        return False, f"contradicts_core: {core.source}"

    def verify_operator(self, op: int) -> bool:
        """Verify that an operator index is valid."""
        return 0 <= op < NUM_OPS

    def verify_composition(self, a: int, b: int, result: int) -> bool:
        """Verify a CL composition result."""
        if not (self.verify_operator(a) and self.verify_operator(b)
                and self.verify_operator(result)):
            return False
        return CL[a][b] == result

    def verify_coherence_band(self, coherence: float) -> str:
        """Classify coherence into band using core thresholds."""
        if coherence >= T_STAR:
            return "GREEN"
        elif coherence >= 0.4:
            return "YELLOW"
        else:
            return "RED"

    def is_fruit(self, word: str) -> bool:
        """Check if a word is a Fruit of the Spirit."""
        return word.lower().replace('-', '_') in FRUITS_OF_THE_SPIRIT

    def fruit_to_operator(self, fruit: str) -> int:
        """Get the operator for a Fruit of the Spirit."""
        return FRUITS_OF_THE_SPIRIT.get(fruit.lower().replace('-', '_'), VOID)

    @property
    def count(self) -> int:
        return len(self._truths)

    @property
    def categories(self) -> Dict[str, int]:
        cats = {}
        for entry in self._truths.values():
            cats[entry.category] = cats.get(entry.category, 0) + 1
        return cats

    def all_keys(self) -> List[str]:
        return list(self._truths.keys())

    def stats(self) -> dict:
        return {
            'total_core_truths': self.count,
            'categories': self.categories,
            'fruits_count': len(FRUITS_OF_THE_SPIRIT),
            'cl_harmony_count': CL_HARMONY_COUNT,
            't_star': T_STAR,
        }


# ================================================================
#  TRUTH LATTICE
# ================================================================

class TruthLattice:
    """CK's complete knowledge store with trust levels.

    Every piece of knowledge lives here, tagged with its truth level.
    Core truths are seeded at construction and never change.
    Trusted knowledge has been verified through sustained coherence.
    Provisional knowledge is new and must prove itself.

    Usage:
        lattice = TruthLattice()
        lattice.add('sky_is_blue', True, source='observation')
        lattice.record_coherence('sky_is_blue', 0.8, tick=100)
        # ... after PROMOTION_WINDOW ticks above T* ...
        lattice.tick(tick=132)  # auto-promotes if ready
    """

    def __init__(self):
        self.core = CoreTruths()
        self._entries: Dict[str, TruthEntry] = {}
        self._tick_count = 0
        self._promotions = 0
        self._demotions = 0
        self._expirations = 0

        # Seed core truths into the main lattice
        for key, entry in self.core._truths.items():
            self._entries[key] = entry

    def add(self, key: str, content: Any,
            source: str = "", category: str = "general",
            level: int = PROVISIONAL) -> TruthEntry:
        """Add new knowledge to the lattice.

        New entries default to PROVISIONAL. They must earn promotion.
        Attempting to overwrite a CORE truth is silently rejected.
        """
        existing = self._entries.get(key)

        # Never overwrite CORE
        if existing and existing.level == CORE:
            return existing

        # If overwriting TRUSTED with PROVISIONAL, keep TRUSTED
        if existing and existing.level == TRUSTED and level == PROVISIONAL:
            return existing

        # Cannot manually set CORE level
        if level == CORE:
            level = TRUSTED  # Downgrade to max-allowed manual level

        entry = TruthEntry(
            key=key,
            content=content,
            level=level,
            source=source,
            category=category,
            created_tick=self._tick_count,
            last_accessed_tick=self._tick_count,
        )
        self._entries[key] = entry
        return entry

    def get(self, key: str) -> Optional[TruthEntry]:
        """Retrieve knowledge by key."""
        entry = self._entries.get(key)
        if entry:
            entry.last_accessed_tick = self._tick_count
        return entry

    def query(self, key: str) -> Tuple[Any, int, float]:
        """Query knowledge with trust metadata.

        Returns: (content, level, confidence)
        Returns (None, -1, 0.0) if not found.
        """
        entry = self.get(key)
        if entry is None:
            return None, -1, 0.0
        return entry.content, entry.level, entry.confidence

    def record_coherence(self, key: str, coherence: float, tick: int = -1):
        """Record a coherence observation for a knowledge entry.

        This is called when CK uses a piece of knowledge and observes
        whether it contributed to coherence. High coherence → verifies.
        Low coherence → contradicts.
        """
        if tick < 0:
            tick = self._tick_count
        entry = self._entries.get(key)
        if entry and entry.level != CORE:
            entry.record_coherence(coherence, tick)

    def tick(self, tick: int = -1):
        """Run one promotion/demotion/expiration cycle.

        Call this each CK tick. It checks all entries and:
        - Promotes PROVISIONAL → TRUSTED if coherence sustained above T*
        - Demotes TRUSTED → PROVISIONAL if coherence below survival
        - Expires unused PROVISIONAL entries
        """
        if tick >= 0:
            self._tick_count = tick
        else:
            self._tick_count += 1

        to_promote = []
        to_demote = []
        to_expire = []

        for key, entry in self._entries.items():
            if entry.level == CORE:
                continue  # Immutable

            if entry.ready_for_promotion:
                to_promote.append(key)
            elif entry.ready_for_demotion:
                to_demote.append(key)
            elif entry.is_expired:
                to_expire.append(key)

        # Apply changes
        for key in to_promote:
            self._entries[key].level = TRUSTED
            self._entries[key]._sustained_above_tstar = 0
            self._promotions += 1

        for key in to_demote:
            self._entries[key].level = PROVISIONAL
            self._entries[key]._sustained_below_survival = 0
            self._demotions += 1

        for key in to_expire:
            del self._entries[key]
            self._expirations += 1

    def verify_against_core(self, key: str, value: Any) -> Tuple[bool, str]:
        """Check if a claim is consistent with core truths."""
        return self.core.verify_claim(key, value)

    def entries_by_level(self, level: int) -> List[TruthEntry]:
        """Get all entries at a given trust level."""
        return [e for e in self._entries.values() if e.level == level]

    def count_by_level(self) -> Dict[str, int]:
        """Count entries per truth level."""
        counts = {LEVEL_NAMES[i]: 0 for i in range(3)}
        for entry in self._entries.values():
            counts[LEVEL_NAMES[entry.level]] += 1
        return counts

    @property
    def total_entries(self) -> int:
        return len(self._entries)

    def stats(self) -> dict:
        by_level = self.count_by_level()
        categories = {}
        for entry in self._entries.values():
            cat = entry.category
            if cat not in categories:
                categories[cat] = {'CORE': 0, 'TRUSTED': 0, 'PROVISIONAL': 0}
            categories[cat][LEVEL_NAMES[entry.level]] += 1

        return {
            'total_entries': self.total_entries,
            'by_level': by_level,
            'by_category': categories,
            'promotions': self._promotions,
            'demotions': self._demotions,
            'expirations': self._expirations,
            'tick': self._tick_count,
            'core_stats': self.core.stats(),
        }


# ================================================================
#  TRUTH GATE: Weight knowledge by trust level
# ================================================================

class TruthGate:
    """Weights knowledge by truth level for decision-making.

    When CK queries the Truth Lattice for a decision, the gate
    multiplies the knowledge's influence by its trust weight:
      CORE:        1.0  (full authority)
      TRUSTED:     0.7  (high confidence)
      PROVISIONAL: 0.3  (low confidence)

    This prevents CK from acting on unverified claims with the
    same certainty as mathematical truths.
    """

    def __init__(self, lattice: TruthLattice):
        self.lattice = lattice

    def gate(self, key: str) -> float:
        """Get the trust weight for a knowledge entry.

        Returns 0.0 if entry not found (unknown = zero trust).
        """
        entry = self.lattice.get(key)
        if entry is None:
            return 0.0
        return TRUST_WEIGHT.get(entry.level, 0.0)

    def weighted_value(self, key: str, raw_score: float) -> float:
        """Apply trust weighting to a raw score.

        raw_score * trust_weight = weighted_score.
        Core truths pass through at full strength.
        Provisional claims are dampened.
        """
        return raw_score * self.gate(key)

    def gate_multiple(self, keys: List[str]) -> Dict[str, float]:
        """Get trust weights for multiple entries at once."""
        return {key: self.gate(key) for key in keys}

    def highest_trust(self, keys: List[str]) -> Optional[str]:
        """Return the key with the highest trust level.

        Among ties, prefers higher confidence.
        """
        if not keys:
            return None

        best_key = None
        best_level = -1
        best_conf = -1.0

        for key in keys:
            entry = self.lattice.get(key)
            if entry is None:
                continue
            if (entry.level > best_level or
                (entry.level == best_level and entry.confidence > best_conf)):
                best_key = key
                best_level = entry.level
                best_conf = entry.confidence

        return best_key

    def filter_by_trust(self, keys: List[str],
                        min_level: int = PROVISIONAL) -> List[str]:
        """Filter keys to only those meeting minimum trust level."""
        result = []
        for key in keys:
            entry = self.lattice.get(key)
            if entry and entry.level >= min_level:
                result.append(key)
        return result

    def resolve_conflict(self, key_a: str, key_b: str) -> str:
        """When two claims conflict, trust the higher level.

        Returns the key of the more trusted claim.
        """
        entry_a = self.lattice.get(key_a)
        entry_b = self.lattice.get(key_b)

        if entry_a is None:
            return key_b
        if entry_b is None:
            return key_a

        if entry_a.level > entry_b.level:
            return key_a
        elif entry_b.level > entry_a.level:
            return key_b
        else:
            # Same level: prefer higher confidence
            if entry_a.confidence >= entry_b.confidence:
                return key_a
            return key_b


# ================================================================
#  CLI: Demo the Truth Lattice
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK TRUTH LATTICE -- Three Levels of Knowledge")
    print("=" * 60)

    lattice = TruthLattice()
    gate = TruthGate(lattice)

    # Show core truth stats
    print(f"\n  Core truths: {lattice.core.count}")
    print(f"  Categories: {lattice.core.categories}")
    print(f"  T* = {T_STAR:.6f}")

    # Show fruits
    print("\n  Fruits of the Spirit:")
    for fruit, op in FRUITS_OF_THE_SPIRIT.items():
        print(f"    {fruit:15s} → {OP_NAMES[op]}")

    # Add some provisional knowledge
    lattice.add('sky_is_blue', True, source='observation', category='world')
    lattice.add('rl_ball_max_speed', 6000.0, source='game', category='game')
    lattice.add('user_name', 'Brayden', source='conversation', category='social')

    # Simulate coherence observations
    import random
    random.seed(42)
    for tick in range(50):
        # Sky is blue: consistently coherent (will promote)
        lattice.record_coherence('sky_is_blue', 0.8, tick)
        # Ball speed: mostly coherent
        lattice.record_coherence('rl_ball_max_speed', 0.7 + random.gauss(0, 0.05), tick)
        # User name: variable
        lattice.record_coherence('user_name', 0.5 + random.gauss(0, 0.2), tick)
        lattice.tick(tick)

    # Check levels
    print("\n  After 50 ticks:")
    for key in ['sky_is_blue', 'rl_ball_max_speed', 'user_name']:
        entry = lattice.get(key)
        if entry:
            print(f"    {key:25s} level={LEVEL_NAMES[entry.level]:12s} "
                  f"coh={entry.local_coherence:.3f} conf={entry.confidence:.3f}")

    # Gate test
    print("\n  Trust gates:")
    for key in ['t_star_float', 'sky_is_blue', 'user_name']:
        w = gate.gate(key)
        print(f"    {key:25s} weight={w:.1f}")

    # Core verification
    print("\n  Core verification:")
    ok, reason = lattice.verify_against_core('op_count', 10)
    print(f"    op_count=10: {ok} ({reason})")
    ok, reason = lattice.verify_against_core('op_count', 11)
    print(f"    op_count=11: {ok} ({reason})")

    # Stats
    stats = lattice.stats()
    print(f"\n  Total entries: {stats['total_entries']}")
    print(f"  By level: {stats['by_level']}")
    print(f"  Promotions: {stats['promotions']}")
    print(f"  Demotions: {stats['demotions']}")
