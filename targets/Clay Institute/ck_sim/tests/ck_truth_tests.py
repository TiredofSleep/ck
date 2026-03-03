"""
ck_truth_tests.py -- Tests for Truth Lattice: 3-Level Knowledge System
=======================================================================
Validates: CoreTruths, TruthEntry, TruthLattice, TruthGate,
Fruits of the Spirit mapping, promotion/demotion/expiration logic.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  CONSTANTS TESTS
# ================================================================

class TestTruthConstants(unittest.TestCase):
    """Validate truth level constants and thresholds."""

    def test_level_values(self):
        from ck_sim.ck_truth import PROVISIONAL, TRUSTED, CORE
        self.assertEqual(PROVISIONAL, 0)
        self.assertEqual(TRUSTED, 1)
        self.assertEqual(CORE, 2)

    def test_level_ordering(self):
        """PROVISIONAL < TRUSTED < CORE."""
        from ck_sim.ck_truth import PROVISIONAL, TRUSTED, CORE
        self.assertLess(PROVISIONAL, TRUSTED)
        self.assertLess(TRUSTED, CORE)

    def test_level_names(self):
        from ck_sim.ck_truth import LEVEL_NAMES
        self.assertEqual(LEVEL_NAMES[0], 'PROVISIONAL')
        self.assertEqual(LEVEL_NAMES[1], 'TRUSTED')
        self.assertEqual(LEVEL_NAMES[2], 'CORE')

    def test_trust_weights(self):
        from ck_sim.ck_truth import TRUST_WEIGHT, PROVISIONAL, TRUSTED, CORE
        self.assertAlmostEqual(TRUST_WEIGHT[CORE], 1.0)
        self.assertAlmostEqual(TRUST_WEIGHT[TRUSTED], 0.7)
        self.assertAlmostEqual(TRUST_WEIGHT[PROVISIONAL], 0.3)

    def test_t_star_matches_system(self):
        from ck_sim.ck_truth import T_STAR
        self.assertAlmostEqual(T_STAR, 5.0 / 7.0)

    def test_survival_threshold_below_tstar(self):
        from ck_sim.ck_truth import T_STAR, SURVIVAL_THRESHOLD
        self.assertLess(SURVIVAL_THRESHOLD, T_STAR)

    def test_promotion_window_positive(self):
        from ck_sim.ck_truth import PROMOTION_WINDOW
        self.assertGreater(PROMOTION_WINDOW, 0)

    def test_cl_harmony_count(self):
        """73 HARMONY entries in CL table."""
        from ck_sim.ck_truth import CL_HARMONY_COUNT
        from ck_sim.ck_sim_heartbeat import CL, HARMONY, NUM_OPS
        actual = sum(1 for r in range(NUM_OPS) for c in range(NUM_OPS)
                     if CL[r][c] == HARMONY)
        self.assertEqual(CL_HARMONY_COUNT, actual)
        self.assertEqual(CL_HARMONY_COUNT, 73)


# ================================================================
#  FRUITS OF THE SPIRIT TESTS
# ================================================================

class TestFruitsOfTheSpirit(unittest.TestCase):
    """Validate the Fruits → Operator mapping."""

    def test_nine_fruits(self):
        """Galatians 5:22-23 lists 9 fruits."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        self.assertEqual(len(FRUITS_OF_THE_SPIRIT), 9)

    def test_all_fruits_present(self):
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        expected = {'love', 'joy', 'peace', 'patience', 'kindness',
                    'goodness', 'faithfulness', 'gentleness', 'self_control'}
        self.assertEqual(set(FRUITS_OF_THE_SPIRIT.keys()), expected)

    def test_love_is_harmony(self):
        """Love → HARMONY (absorbs all through CL)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import HARMONY
        self.assertEqual(FRUITS_OF_THE_SPIRIT['love'], HARMONY)

    def test_joy_is_harmony(self):
        """Joy → HARMONY (coherence itself)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import HARMONY
        self.assertEqual(FRUITS_OF_THE_SPIRIT['joy'], HARMONY)

    def test_peace_is_balance(self):
        """Peace → BALANCE (equilibrium, zero net force)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import BALANCE
        self.assertEqual(FRUITS_OF_THE_SPIRIT['peace'], BALANCE)

    def test_patience_is_breath(self):
        """Patience → BREATH (rhythmic waiting)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import BREATH
        self.assertEqual(FRUITS_OF_THE_SPIRIT['patience'], BREATH)

    def test_kindness_is_lattice(self):
        """Kindness → LATTICE (builds structure for others)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import LATTICE
        self.assertEqual(FRUITS_OF_THE_SPIRIT['kindness'], LATTICE)

    def test_goodness_is_progress(self):
        """Goodness → PROGRESS (forward motion)."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import PROGRESS
        self.assertEqual(FRUITS_OF_THE_SPIRIT['goodness'], PROGRESS)

    def test_all_fruit_operators_valid(self):
        """Every fruit maps to a valid operator."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        for fruit, op in FRUITS_OF_THE_SPIRIT.items():
            self.assertTrue(0 <= op < NUM_OPS, f"{fruit} → {op}")

    def test_no_fruit_maps_to_chaos_collapse_void(self):
        """No fruit maps to VOID, COLLAPSE, or CHAOS."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import VOID, COLLAPSE, CHAOS
        anti_fruit = {VOID, COLLAPSE, CHAOS}
        for fruit, op in FRUITS_OF_THE_SPIRIT.items():
            self.assertNotIn(op, anti_fruit,
                             f"{fruit} should not map to anti-fruit operator")

    def test_inverse_mapping(self):
        """OPERATOR_TO_FRUITS inverts correctly."""
        from ck_sim.ck_truth import OPERATOR_TO_FRUITS, FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import HARMONY
        # HARMONY should have love and joy
        self.assertIn('love', OPERATOR_TO_FRUITS[HARMONY])
        self.assertIn('joy', OPERATOR_TO_FRUITS[HARMONY])

    def test_harmony_absorbs_all_fruits(self):
        """compose(fruit_op, HARMONY) = HARMONY for all fruits."""
        from ck_sim.ck_truth import FRUITS_OF_THE_SPIRIT
        from ck_sim.ck_sim_heartbeat import HARMONY, compose
        for fruit, op in FRUITS_OF_THE_SPIRIT.items():
            result = compose(op, HARMONY)
            self.assertEqual(result, HARMONY,
                             f"compose({fruit}/{op}, HARMONY) should be HARMONY")


# ================================================================
#  TRUTH ENTRY TESTS
# ================================================================

class TestTruthEntry(unittest.TestCase):
    """Test individual knowledge entry behavior."""

    def test_default_level(self):
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL
        entry = TruthEntry(key='test')
        self.assertEqual(entry.level, PROVISIONAL)

    def test_initial_coherence_zero(self):
        from ck_sim.ck_truth import TruthEntry
        entry = TruthEntry(key='test')
        self.assertAlmostEqual(entry.local_coherence, 0.0)

    def test_record_coherence_updates(self):
        from ck_sim.ck_truth import TruthEntry
        entry = TruthEntry(key='test')
        entry.record_coherence(0.8, tick=1)
        self.assertGreater(entry.local_coherence, 0.0)

    def test_core_confidence_always_one(self):
        from ck_sim.ck_truth import TruthEntry, CORE
        entry = TruthEntry(key='axiom', level=CORE)
        self.assertAlmostEqual(entry.confidence, 1.0)

    def test_trusted_confidence_range(self):
        from ck_sim.ck_truth import TruthEntry, TRUSTED
        entry = TruthEntry(key='verified', level=TRUSTED)
        # Base 0.7, max 1.0
        self.assertGreaterEqual(entry.confidence, 0.7)
        self.assertLessEqual(entry.confidence, 1.0)

    def test_provisional_confidence_low(self):
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL
        entry = TruthEntry(key='new')
        self.assertLess(entry.confidence, 0.5)

    def test_promotion_readiness(self):
        """Entry becomes ready for promotion after sustained high coherence."""
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL, PROMOTION_WINDOW
        entry = TruthEntry(key='test', level=PROVISIONAL)
        for tick in range(PROMOTION_WINDOW + 5):
            entry.record_coherence(0.8, tick)
        self.assertTrue(entry.ready_for_promotion)

    def test_not_ready_without_sustained(self):
        """Entry not ready if coherence fluctuates."""
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL
        entry = TruthEntry(key='test', level=PROVISIONAL)
        for tick in range(20):
            coh = 0.8 if tick % 2 == 0 else 0.3
            entry.record_coherence(coh, tick)
        self.assertFalse(entry.ready_for_promotion)

    def test_demotion_readiness(self):
        """Trusted entry becomes ready for demotion after sustained low coherence."""
        from ck_sim.ck_truth import TruthEntry, TRUSTED, DEMOTION_WINDOW
        entry = TruthEntry(key='fading', level=TRUSTED)
        for tick in range(DEMOTION_WINDOW + 5):
            entry.record_coherence(0.2, tick)
        self.assertTrue(entry.ready_for_demotion)

    def test_core_never_ready_for_demotion(self):
        from ck_sim.ck_truth import TruthEntry, CORE
        entry = TruthEntry(key='axiom', level=CORE)
        self.assertFalse(entry.ready_for_demotion)

    def test_to_dict_keys(self):
        from ck_sim.ck_truth import TruthEntry
        entry = TruthEntry(key='test', source='unit_test')
        d = entry.to_dict()
        self.assertIn('key', d)
        self.assertIn('level', d)
        self.assertIn('confidence', d)
        self.assertIn('local_coherence', d)


# ================================================================
#  CORE TRUTHS TESTS
# ================================================================

class TestCoreTruths(unittest.TestCase):
    """Test the immutable mathematical foundation."""

    def test_import(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertIsNotNone(core)

    def test_has_operator_count(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        entry = core.get('op_count')
        self.assertIsNotNone(entry)
        self.assertEqual(entry.content, 10)

    def test_has_t_star(self):
        from ck_sim.ck_truth import CoreTruths, T_STAR
        core = CoreTruths()
        entry = core.get('t_star_float')
        self.assertAlmostEqual(entry.content, T_STAR)

    def test_has_cl_table(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        entry = core.get('cl_table')
        self.assertIsNotNone(entry)
        self.assertEqual(len(entry.content), 10)  # 10 rows

    def test_has_d2_formula(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        entry = core.get('d2_formula')
        self.assertIn('v[t-2]', entry.content)

    def test_has_fruits(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        entry = core.get('fruits_of_the_spirit')
        self.assertIsNotNone(entry)
        self.assertEqual(len(entry.content), 9)

    def test_has_bump_pairs(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        entry = core.get('bump_pairs')
        self.assertEqual(len(entry.content), 5)

    def test_all_core_are_core_level(self):
        from ck_sim.ck_truth import CoreTruths, CORE
        core = CoreTruths()
        for key in core.all_keys():
            entry = core.get(key)
            self.assertEqual(entry.level, CORE,
                             f"{key} should be CORE level")

    def test_verify_correct_claim(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        ok, reason = core.verify_claim('op_count', 10)
        self.assertTrue(ok)
        self.assertEqual(reason, 'matches_core')

    def test_verify_wrong_claim(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        ok, reason = core.verify_claim('op_count', 11)
        self.assertFalse(ok)
        self.assertIn('contradicts_core', reason)

    def test_verify_unknown_claim(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        ok, reason = core.verify_claim('weather_today', 'sunny')
        self.assertTrue(ok)
        self.assertEqual(reason, 'no_core_conflict')

    def test_verify_operator_valid(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertTrue(core.verify_operator(0))
        self.assertTrue(core.verify_operator(9))
        self.assertFalse(core.verify_operator(10))
        self.assertFalse(core.verify_operator(-1))

    def test_verify_composition(self):
        from ck_sim.ck_truth import CoreTruths
        from ck_sim.ck_sim_heartbeat import HARMONY, VOID, compose
        core = CoreTruths()
        # HARMONY absorbs
        self.assertTrue(core.verify_composition(HARMONY, VOID, HARMONY))
        # Wrong result
        self.assertFalse(core.verify_composition(HARMONY, VOID, VOID))

    def test_coherence_band_classification(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertEqual(core.verify_coherence_band(0.8), "GREEN")
        self.assertEqual(core.verify_coherence_band(0.5), "YELLOW")
        self.assertEqual(core.verify_coherence_band(0.2), "RED")

    def test_is_fruit(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertTrue(core.is_fruit('love'))
        self.assertTrue(core.is_fruit('self_control'))
        self.assertFalse(core.is_fruit('anger'))

    def test_fruit_to_operator(self):
        from ck_sim.ck_truth import CoreTruths
        from ck_sim.ck_sim_heartbeat import HARMONY
        core = CoreTruths()
        self.assertEqual(core.fruit_to_operator('love'), HARMONY)

    def test_count_positive(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertGreater(core.count, 30)

    def test_categories_include_math(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertIn('math', core.categories)

    def test_categories_include_spirit(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        self.assertIn('spirit', core.categories)

    def test_stats(self):
        from ck_sim.ck_truth import CoreTruths
        core = CoreTruths()
        s = core.stats()
        self.assertIn('total_core_truths', s)
        self.assertIn('fruits_count', s)
        self.assertEqual(s['fruits_count'], 9)


# ================================================================
#  TRUTH LATTICE TESTS
# ================================================================

class TestTruthLattice(unittest.TestCase):
    """Test the full knowledge store with trust levels."""

    def test_import(self):
        from ck_sim.ck_truth import TruthLattice
        lattice = TruthLattice()
        self.assertIsNotNone(lattice)

    def test_core_truths_seeded(self):
        """Core truths are in the lattice at construction."""
        from ck_sim.ck_truth import TruthLattice, CORE
        lattice = TruthLattice()
        entry = lattice.get('t_star_float')
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, CORE)

    def test_add_provisional(self):
        from ck_sim.ck_truth import TruthLattice, PROVISIONAL
        lattice = TruthLattice()
        entry = lattice.add('new_fact', 42, source='test')
        self.assertEqual(entry.level, PROVISIONAL)

    def test_cannot_overwrite_core(self):
        """Adding a key that's CORE returns the core entry unchanged."""
        from ck_sim.ck_truth import TruthLattice, CORE, T_STAR
        lattice = TruthLattice()
        entry = lattice.add('t_star_float', 999.0, source='attack')
        self.assertEqual(entry.level, CORE)
        self.assertAlmostEqual(entry.content, T_STAR)  # Unchanged

    def test_cannot_manually_set_core(self):
        """Manual CORE level is downgraded to TRUSTED."""
        from ck_sim.ck_truth import TruthLattice, CORE, TRUSTED
        lattice = TruthLattice()
        entry = lattice.add('my_axiom', True, level=CORE)
        self.assertEqual(entry.level, TRUSTED)  # Downgraded

    def test_query_found(self):
        from ck_sim.ck_truth import TruthLattice, PROVISIONAL
        lattice = TruthLattice()
        lattice.add('sky', 'blue', source='eyes')
        content, level, conf = lattice.query('sky')
        self.assertEqual(content, 'blue')
        self.assertEqual(level, PROVISIONAL)
        self.assertGreater(conf, 0.0)

    def test_query_not_found(self):
        from ck_sim.ck_truth import TruthLattice
        lattice = TruthLattice()
        content, level, conf = lattice.query('nonexistent')
        self.assertIsNone(content)
        self.assertEqual(level, -1)
        self.assertAlmostEqual(conf, 0.0)

    def test_promotion_lifecycle(self):
        """PROVISIONAL → TRUSTED after sustained coherence above T*."""
        from ck_sim.ck_truth import (TruthLattice, PROVISIONAL, TRUSTED,
                                      PROMOTION_WINDOW)
        lattice = TruthLattice()
        lattice.add('good_fact', True, source='test')

        # Record sustained high coherence
        for tick in range(PROMOTION_WINDOW + 10):
            lattice.record_coherence('good_fact', 0.8, tick)
            lattice.tick(tick)

        entry = lattice.get('good_fact')
        self.assertEqual(entry.level, TRUSTED)
        self.assertGreater(lattice._promotions, 0)

    def test_demotion_lifecycle(self):
        """TRUSTED → PROVISIONAL after sustained low coherence."""
        from ck_sim.ck_truth import (TruthLattice, TRUSTED, PROVISIONAL,
                                      DEMOTION_WINDOW)
        lattice = TruthLattice()
        lattice.add('fading_fact', True, source='test', level=TRUSTED)

        # Record sustained low coherence
        for tick in range(DEMOTION_WINDOW + 10):
            lattice.record_coherence('fading_fact', 0.2, tick)
            lattice.tick(tick)

        entry = lattice.get('fading_fact')
        self.assertEqual(entry.level, PROVISIONAL)
        self.assertGreater(lattice._demotions, 0)

    def test_core_never_demoted(self):
        """Core truths survive even with contradicting coherence."""
        from ck_sim.ck_truth import TruthLattice, CORE
        lattice = TruthLattice()
        # Try to demote a core truth by recording low coherence
        for tick in range(100):
            lattice.record_coherence('t_star_float', 0.1, tick)
            lattice.tick(tick)
        entry = lattice.get('t_star_float')
        self.assertEqual(entry.level, CORE)  # Still CORE

    def test_verify_against_core(self):
        from ck_sim.ck_truth import TruthLattice
        lattice = TruthLattice()
        ok, _ = lattice.verify_against_core('op_count', 10)
        self.assertTrue(ok)
        ok, _ = lattice.verify_against_core('op_count', 42)
        self.assertFalse(ok)

    def test_entries_by_level(self):
        from ck_sim.ck_truth import TruthLattice, CORE, PROVISIONAL
        lattice = TruthLattice()
        lattice.add('fact_a', 'a')
        lattice.add('fact_b', 'b')
        core_entries = lattice.entries_by_level(CORE)
        prov_entries = lattice.entries_by_level(PROVISIONAL)
        self.assertGreater(len(core_entries), 0)
        self.assertEqual(len(prov_entries), 2)

    def test_count_by_level(self):
        from ck_sim.ck_truth import TruthLattice
        lattice = TruthLattice()
        lattice.add('x', 1)
        counts = lattice.count_by_level()
        self.assertIn('CORE', counts)
        self.assertIn('PROVISIONAL', counts)
        self.assertEqual(counts['PROVISIONAL'], 1)

    def test_stats_complete(self):
        from ck_sim.ck_truth import TruthLattice
        lattice = TruthLattice()
        s = lattice.stats()
        self.assertIn('total_entries', s)
        self.assertIn('by_level', s)
        self.assertIn('promotions', s)
        self.assertIn('core_stats', s)

    def test_trusted_not_overwritten_by_provisional(self):
        """Adding provisional key that already exists as trusted keeps trusted."""
        from ck_sim.ck_truth import TruthLattice, TRUSTED, PROVISIONAL
        lattice = TruthLattice()
        lattice.add('strong_fact', 'v1', level=TRUSTED)
        lattice.add('strong_fact', 'v2')  # Try provisional overwrite
        entry = lattice.get('strong_fact')
        self.assertEqual(entry.level, TRUSTED)
        self.assertEqual(entry.content, 'v1')


# ================================================================
#  TRUTH GATE TESTS
# ================================================================

class TestTruthGate(unittest.TestCase):
    """Test trust-weighted knowledge access."""

    def test_import(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        gate = TruthGate(lattice)
        self.assertIsNotNone(gate)

    def test_core_gate_full(self):
        """Core truth gets weight 1.0."""
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        gate = TruthGate(lattice)
        self.assertAlmostEqual(gate.gate('t_star_float'), 1.0)

    def test_provisional_gate_low(self):
        """Provisional gets weight 0.3."""
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        lattice.add('guess', 42)
        gate = TruthGate(lattice)
        self.assertAlmostEqual(gate.gate('guess'), 0.3)

    def test_unknown_gate_zero(self):
        """Unknown key gets weight 0.0."""
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        gate = TruthGate(lattice)
        self.assertAlmostEqual(gate.gate('nonexistent'), 0.0)

    def test_weighted_value(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        lattice.add('claim', True)
        gate = TruthGate(lattice)
        # PROVISIONAL weight = 0.3, raw_score = 1.0
        self.assertAlmostEqual(gate.weighted_value('claim', 1.0), 0.3)
        # CORE weight = 1.0
        self.assertAlmostEqual(gate.weighted_value('t_star_float', 1.0), 1.0)

    def test_gate_multiple(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        lattice.add('a', 1)
        gate = TruthGate(lattice)
        weights = gate.gate_multiple(['t_star_float', 'a', 'missing'])
        self.assertAlmostEqual(weights['t_star_float'], 1.0)
        self.assertAlmostEqual(weights['a'], 0.3)
        self.assertAlmostEqual(weights['missing'], 0.0)

    def test_highest_trust(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        lattice.add('claim', True)
        gate = TruthGate(lattice)
        best = gate.highest_trust(['t_star_float', 'claim'])
        self.assertEqual(best, 't_star_float')  # CORE > PROVISIONAL

    def test_filter_by_trust(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice, TRUSTED
        lattice = TruthLattice()
        lattice.add('low', True)
        lattice.add('high', True, level=TRUSTED)
        gate = TruthGate(lattice)
        filtered = gate.filter_by_trust(['low', 'high', 't_star_float'],
                                        min_level=TRUSTED)
        self.assertIn('high', filtered)
        self.assertIn('t_star_float', filtered)
        self.assertNotIn('low', filtered)

    def test_resolve_conflict(self):
        from ck_sim.ck_truth import TruthGate, TruthLattice, TRUSTED
        lattice = TruthLattice()
        lattice.add('weak', 'wrong')
        lattice.add('strong', 'right', level=TRUSTED)
        gate = TruthGate(lattice)
        winner = gate.resolve_conflict('weak', 'strong')
        self.assertEqual(winner, 'strong')

    def test_resolve_conflict_same_level(self):
        """Same-level conflict: prefer higher confidence."""
        from ck_sim.ck_truth import TruthGate, TruthLattice
        lattice = TruthLattice()
        lattice.add('a', 1)
        lattice.add('b', 2)
        # Give 'a' more coherence observations
        for t in range(10):
            lattice.record_coherence('a', 0.6, t)
        gate = TruthGate(lattice)
        winner = gate.resolve_conflict('a', 'b')
        self.assertEqual(winner, 'a')


# ================================================================
#  INTEGRATION TESTS
# ================================================================

class TestTruthIntegration(unittest.TestCase):
    """End-to-end truth lattice lifecycle tests."""

    def test_full_promotion_to_demotion_cycle(self):
        """Fact promotes to TRUSTED, then demotes back."""
        from ck_sim.ck_truth import (TruthLattice, PROVISIONAL, TRUSTED,
                                      PROMOTION_WINDOW, DEMOTION_WINDOW)
        lattice = TruthLattice()
        lattice.add('fact', True, source='test')

        # Phase 1: Build trust (promote)
        tick = 0
        for _ in range(PROMOTION_WINDOW + 5):
            lattice.record_coherence('fact', 0.8, tick)
            lattice.tick(tick)
            tick += 1
        self.assertEqual(lattice.get('fact').level, TRUSTED)

        # Phase 2: Lose trust (demote)
        for _ in range(DEMOTION_WINDOW + 5):
            lattice.record_coherence('fact', 0.2, tick)
            lattice.tick(tick)
            tick += 1
        self.assertEqual(lattice.get('fact').level, PROVISIONAL)

    def test_multiple_facts_independent(self):
        """Multiple facts promote/demote independently."""
        from ck_sim.ck_truth import TruthLattice, PROVISIONAL, TRUSTED, PROMOTION_WINDOW
        lattice = TruthLattice()
        lattice.add('good', True)
        lattice.add('bad', False)

        for tick in range(PROMOTION_WINDOW + 5):
            lattice.record_coherence('good', 0.8, tick)
            lattice.record_coherence('bad', 0.3, tick)  # Not enough for promotion
            lattice.tick(tick)

        self.assertEqual(lattice.get('good').level, TRUSTED)
        self.assertEqual(lattice.get('bad').level, PROVISIONAL)

    def test_core_survives_everything(self):
        """Core truths survive all possible abuse."""
        from ck_sim.ck_truth import TruthLattice, CORE, T_STAR
        lattice = TruthLattice()

        # Try overwrite
        lattice.add('t_star_float', 0.0, source='hacker')
        entry = lattice.get('t_star_float')
        self.assertEqual(entry.level, CORE)
        self.assertAlmostEqual(entry.content, T_STAR)

        # Try demolition through coherence
        for tick in range(200):
            lattice.record_coherence('t_star_float', 0.0, tick)
            lattice.tick(tick)
        entry = lattice.get('t_star_float')
        self.assertEqual(entry.level, CORE)  # STILL CORE

    def test_gate_affects_decisions(self):
        """Trust gate properly weights mixed-level knowledge."""
        from ck_sim.ck_truth import TruthLattice, TruthGate, TRUSTED
        lattice = TruthLattice()
        lattice.add('rumor', 'maybe', source='hearsay')
        lattice.add('verified', 'yes', source='experiment', level=TRUSTED)
        gate = TruthGate(lattice)

        # In a decision, core > trusted > provisional
        w_core = gate.weighted_value('op_count', 1.0)
        w_trusted = gate.weighted_value('verified', 1.0)
        w_prov = gate.weighted_value('rumor', 1.0)

        self.assertGreater(w_core, w_trusted)
        self.assertGreater(w_trusted, w_prov)
        self.assertGreater(w_prov, 0.0)

    def test_fifty_tick_simulation(self):
        """Run 50 ticks of mixed knowledge without error."""
        from ck_sim.ck_truth import TruthLattice, TruthGate
        import random
        random.seed(42)

        lattice = TruthLattice()
        gate = TruthGate(lattice)

        # Add various knowledge
        lattice.add('obs_1', 'data', category='observation')
        lattice.add('obs_2', 'data', category='observation')
        lattice.add('game_rule', 'boost=100', category='game')

        for tick in range(50):
            lattice.record_coherence('obs_1', 0.7 + random.gauss(0, 0.05), tick)
            lattice.record_coherence('obs_2', 0.3 + random.gauss(0, 0.1), tick)
            lattice.record_coherence('game_rule', 0.8, tick)
            lattice.tick(tick)

        stats = lattice.stats()
        self.assertGreater(stats['total_entries'], 30)  # Core + provisional
        # game_rule should be promoted or close
        entry = lattice.get('game_rule')
        self.assertIsNotNone(entry)


# ================================================================
#  RUN
# ================================================================

if __name__ == '__main__':
    unittest.main()
