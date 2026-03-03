"""
ck_metalearning_tests.py -- Tests for Meta-Learning System
=============================================================
Validates: learning rate adaptation, threshold tuning, curriculum
tracking, meta-learner integration, safety bounds, and adaptation
under extreme conditions.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.ck_sim_heartbeat import NUM_OPS, HARMONY, OP_NAMES
from ck_sim.ck_metalearning import (
    LearningRateAdapter, ThresholdTuner, CurriculumTracker, MetaLearner,
    DEFAULT_TRAUMA_MULT, DEFAULT_SUCCESS_MULT,
    MIN_TRAUMA_MULT, MAX_TRAUMA_MULT,
    MIN_SUCCESS_MULT, MAX_SUCCESS_MULT,
    ADAPTATION_ALPHA, EVALUATION_WINDOW,
    GREEN_THRESHOLD_DEFAULT, YELLOW_THRESHOLD_DEFAULT,
    MIN_GREEN_THRESHOLD, MAX_GREEN_THRESHOLD,
    MIN_YELLOW_THRESHOLD, MAX_YELLOW_THRESHOLD,
    MAX_COMPLEXITY, RED, YELLOW, GREEN,
)


class TestImport(unittest.TestCase):
    """Verify module imports cleanly."""

    def test_import(self):
        import ck_sim.ck_metalearning
        self.assertTrue(hasattr(ck_sim.ck_metalearning, 'MetaLearner'))
        self.assertTrue(hasattr(ck_sim.ck_metalearning, 'LearningRateAdapter'))
        self.assertTrue(hasattr(ck_sim.ck_metalearning, 'ThresholdTuner'))
        self.assertTrue(hasattr(ck_sim.ck_metalearning, 'CurriculumTracker'))


# ================================================================
#  LEARNING RATE ADAPTER TESTS
# ================================================================

class TestLearningRateAdapterDefaults(unittest.TestCase):
    """LearningRateAdapter initial state."""

    def test_default_trauma_mult(self):
        adapter = LearningRateAdapter()
        self.assertEqual(adapter.trauma_mult, DEFAULT_TRAUMA_MULT)

    def test_default_success_mult(self):
        adapter = LearningRateAdapter()
        self.assertEqual(adapter.success_mult, DEFAULT_SUCCESS_MULT)

    def test_stats_has_expected_keys(self):
        adapter = LearningRateAdapter()
        s = adapter.stats
        for key in ('trauma_mult', 'success_mult', 'trauma_ema',
                     'success_ema', 'trauma_samples', 'success_samples'):
            self.assertIn(key, s)


class TestLearningRateAdapterBounds(unittest.TestCase):
    """Multipliers never escape safety bounds."""

    def test_trauma_mult_never_below_min(self):
        adapter = LearningRateAdapter()
        # Feed many negative-delta traumas -> adapter should try to decrease
        for _ in range(500):
            adapter.feed_outcome(is_trauma=True,
                                 coherence_before=0.8, coherence_after=0.3)
        # Adapt many times
        for _ in range(1000):
            adapter.adapt()
        self.assertGreaterEqual(adapter.trauma_mult, MIN_TRAUMA_MULT)

    def test_trauma_mult_never_above_max(self):
        adapter = LearningRateAdapter()
        # Feed many positive-delta traumas -> adapter should try to increase
        for _ in range(500):
            adapter.feed_outcome(is_trauma=True,
                                 coherence_before=0.3, coherence_after=0.9)
        for _ in range(1000):
            adapter.adapt()
        self.assertLessEqual(adapter.trauma_mult, MAX_TRAUMA_MULT)

    def test_success_mult_never_below_min(self):
        adapter = LearningRateAdapter()
        for _ in range(500):
            adapter.feed_outcome(is_trauma=False,
                                 coherence_before=0.8, coherence_after=0.2)
        for _ in range(1000):
            adapter.adapt()
        self.assertGreaterEqual(adapter.success_mult, MIN_SUCCESS_MULT)

    def test_success_mult_never_above_max(self):
        adapter = LearningRateAdapter()
        for _ in range(500):
            adapter.feed_outcome(is_trauma=False,
                                 coherence_before=0.2, coherence_after=0.9)
        for _ in range(1000):
            adapter.adapt()
        self.assertLessEqual(adapter.success_mult, MAX_SUCCESS_MULT)


class TestLearningRateAdapterDirection(unittest.TestCase):
    """Multipliers move in the correct direction."""

    def test_trauma_helps_increases_mult(self):
        """When trauma consistently improves coherence, trauma_mult should increase."""
        adapter = LearningRateAdapter()
        initial = adapter.trauma_mult
        # Trauma events that HELP coherence (positive delta)
        for _ in range(200):
            adapter.feed_outcome(is_trauma=True,
                                 coherence_before=0.4, coherence_after=0.7)
        for _ in range(50):
            adapter.adapt()
        self.assertGreaterEqual(adapter.trauma_mult, initial)

    def test_trauma_hurts_decreases_mult(self):
        """When trauma consistently degrades coherence, trauma_mult should decrease."""
        adapter = LearningRateAdapter()
        initial = adapter.trauma_mult
        # Trauma events that HURT coherence (negative delta)
        for _ in range(200):
            adapter.feed_outcome(is_trauma=True,
                                 coherence_before=0.7, coherence_after=0.3)
        for _ in range(50):
            adapter.adapt()
        self.assertLessEqual(adapter.trauma_mult, initial)

    def test_no_data_no_change(self):
        """With no data, adapt should not change multipliers."""
        adapter = LearningRateAdapter()
        adapter.adapt()
        self.assertEqual(adapter.trauma_mult, DEFAULT_TRAUMA_MULT)
        self.assertEqual(adapter.success_mult, DEFAULT_SUCCESS_MULT)


# ================================================================
#  THRESHOLD TUNER TESTS
# ================================================================

class TestThresholdTunerDefaults(unittest.TestCase):
    """ThresholdTuner initial state."""

    def test_default_green(self):
        tuner = ThresholdTuner()
        self.assertAlmostEqual(tuner.green_threshold,
                               GREEN_THRESHOLD_DEFAULT, places=5)

    def test_default_yellow(self):
        tuner = ThresholdTuner()
        self.assertAlmostEqual(tuner.yellow_threshold,
                               YELLOW_THRESHOLD_DEFAULT, places=5)

    def test_default_band_classification(self):
        tuner = ThresholdTuner()
        self.assertEqual(tuner.get_band(0.8), GREEN)
        self.assertEqual(tuner.get_band(0.6), YELLOW)
        self.assertEqual(tuner.get_band(0.3), RED)


class TestThresholdTunerBounds(unittest.TestCase):
    """Thresholds never escape safety bounds."""

    def test_green_never_below_min(self):
        tuner = ThresholdTuner()
        # All RED -> tuner should lower thresholds, but not below min
        for _ in range(300):
            tuner.feed_coherence(0.1, RED)
        for _ in range(500):
            tuner.adapt()
        self.assertGreaterEqual(tuner.green_threshold, MIN_GREEN_THRESHOLD)

    def test_green_never_above_max(self):
        tuner = ThresholdTuner()
        # All GREEN -> tuner should raise thresholds, but not above max
        for _ in range(300):
            tuner.feed_coherence(0.95, GREEN)
        for _ in range(500):
            tuner.adapt()
        self.assertLessEqual(tuner.green_threshold, MAX_GREEN_THRESHOLD)

    def test_yellow_never_below_min(self):
        tuner = ThresholdTuner()
        for _ in range(300):
            tuner.feed_coherence(0.1, RED)
        for _ in range(500):
            tuner.adapt()
        self.assertGreaterEqual(tuner.yellow_threshold, MIN_YELLOW_THRESHOLD)

    def test_yellow_never_above_max(self):
        tuner = ThresholdTuner()
        for _ in range(300):
            tuner.feed_coherence(0.95, GREEN)
        for _ in range(500):
            tuner.adapt()
        self.assertLessEqual(tuner.yellow_threshold, MAX_YELLOW_THRESHOLD)

    def test_green_always_above_yellow(self):
        """Green threshold must always be above yellow threshold."""
        tuner = ThresholdTuner()
        # Hammer with mixed data
        for i in range(300):
            if i % 2 == 0:
                tuner.feed_coherence(0.1, RED)
            else:
                tuner.feed_coherence(0.95, GREEN)
        for _ in range(200):
            tuner.adapt()
        self.assertGreater(tuner.green_threshold, tuner.yellow_threshold)


class TestThresholdTunerAdaptation(unittest.TestCase):
    """Thresholds adapt in the correct direction."""

    def test_too_much_red_lowers_thresholds(self):
        """Spending >60% in RED should lower thresholds."""
        tuner = ThresholdTuner()
        initial_green = tuner.green_threshold
        # Feed all RED
        for _ in range(200):
            tuner.feed_coherence(0.2, RED)
        tuner.adapt()
        self.assertLessEqual(tuner.green_threshold, initial_green)

    def test_easy_green_raises_thresholds(self):
        """Spending >80% in GREEN should raise thresholds."""
        tuner = ThresholdTuner()
        initial_green = tuner.green_threshold
        # Feed all GREEN
        for _ in range(200):
            tuner.feed_coherence(0.9, GREEN)
        tuner.adapt()
        self.assertGreaterEqual(tuner.green_threshold, initial_green)


# ================================================================
#  CURRICULUM TRACKER TESTS
# ================================================================

class TestCurriculumTrackerDefaults(unittest.TestCase):
    """CurriculumTracker initial state."""

    def test_starts_at_zero(self):
        tracker = CurriculumTracker()
        self.assertEqual(tracker.get_complexity(), 0.0)

    def test_complexity_range(self):
        tracker = CurriculumTracker()
        self.assertGreaterEqual(tracker.get_complexity(), 0.0)
        self.assertLessEqual(tracker.get_complexity(), MAX_COMPLEXITY)


class TestCurriculumTrackerAdaptation(unittest.TestCase):
    """Complexity adjusts based on performance."""

    def test_good_performance_increases_complexity(self):
        """High coherence + crystals + advanced mode -> complexity increases."""
        tracker = CurriculumTracker()
        # Feed sustained good performance
        for _ in range(200):
            tracker.feed_performance(coherence=0.8, crystals_formed=3, mode=2)
        for _ in range(50):
            tracker.adapt()
        self.assertGreater(tracker.get_complexity(), 0.0)

    def test_bad_performance_decreases_complexity(self):
        """Low coherence -> complexity decreases (or stays at zero)."""
        tracker = CurriculumTracker()
        # First raise complexity
        for _ in range(200):
            tracker.feed_performance(coherence=0.8, crystals_formed=3, mode=2)
        for _ in range(100):
            tracker.adapt()
        raised = tracker.get_complexity()
        self.assertGreater(raised, 0.0)  # Should have risen

        # Now feed bad performance
        for _ in range(200):
            tracker.feed_performance(coherence=0.2, crystals_formed=0, mode=0)
        for _ in range(100):
            tracker.adapt()
        self.assertLess(tracker.get_complexity(), raised)

    def test_complexity_never_exceeds_max(self):
        tracker = CurriculumTracker()
        for _ in range(500):
            tracker.feed_performance(coherence=0.95, crystals_formed=10, mode=3)
        for _ in range(2000):
            tracker.adapt()
        self.assertLessEqual(tracker.get_complexity(), MAX_COMPLEXITY)

    def test_complexity_never_below_zero(self):
        tracker = CurriculumTracker()
        for _ in range(500):
            tracker.feed_performance(coherence=0.1, crystals_formed=0, mode=0)
        for _ in range(2000):
            tracker.adapt()
        self.assertGreaterEqual(tracker.get_complexity(), 0.0)


# ================================================================
#  META-LEARNER TESTS
# ================================================================

class TestMetaLearnerTick(unittest.TestCase):
    """MetaLearner.tick returns valid dict."""

    def test_tick_returns_expected_keys(self):
        ml = MetaLearner()
        result = ml.tick(tick=0, coherence=0.7, band=GREEN,
                         is_trauma=False, crystals=0, mode=0)
        expected_keys = {'trauma_mult', 'success_mult',
                         'green_threshold', 'yellow_threshold',
                         'complexity', 'band'}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_tick_band_uses_adapted_thresholds(self):
        """Band in tick output should use the tuned thresholds."""
        ml = MetaLearner()
        # At default thresholds, 0.72 is GREEN (5/7 ~ 0.7143)
        result = ml.tick(tick=0, coherence=0.72, band=GREEN,
                         is_trauma=False, crystals=0, mode=0)
        self.assertEqual(result['band'], GREEN)

    def test_tick_initial_values(self):
        ml = MetaLearner()
        result = ml.tick(tick=0, coherence=0.5, band=YELLOW,
                         is_trauma=False, crystals=0, mode=0)
        self.assertAlmostEqual(result['trauma_mult'], DEFAULT_TRAUMA_MULT)
        self.assertAlmostEqual(result['success_mult'], DEFAULT_SUCCESS_MULT)
        self.assertAlmostEqual(result['green_threshold'],
                               GREEN_THRESHOLD_DEFAULT, places=5)
        self.assertAlmostEqual(result['yellow_threshold'],
                               YELLOW_THRESHOLD_DEFAULT, places=5)
        self.assertEqual(result['complexity'], 0.0)


class TestMetaLearnerStats(unittest.TestCase):
    """MetaLearner.stats returns full diagnostic info."""

    def test_stats_structure(self):
        ml = MetaLearner()
        s = ml.stats()
        self.assertIn('learning_rate', s)
        self.assertIn('thresholds', s)
        self.assertIn('curriculum', s)
        self.assertIn('last_evaluation_tick', s)

    def test_stats_after_ticks(self):
        ml = MetaLearner()
        for t in range(50):
            ml.tick(tick=t, coherence=0.6, band=YELLOW,
                    is_trauma=False, crystals=0, mode=0)
        s = ml.stats()
        self.assertEqual(s['thresholds']['samples'], 50)


class TestMetaLearnerAdaptation(unittest.TestCase):
    """MetaLearner triggers adaptation at EVALUATION_WINDOW boundaries."""

    def test_adaptation_triggers_at_window(self):
        """After EVALUATION_WINDOW ticks, adaptation should run."""
        ml = MetaLearner()
        # Feed all RED to trigger threshold adaptation
        for t in range(EVALUATION_WINDOW + 1):
            ml.tick(tick=t, coherence=0.2, band=RED,
                    is_trauma=False, crystals=0, mode=0)
        # After adaptation, green threshold should have decreased
        self.assertLessEqual(ml.thresholds.green_threshold,
                             GREEN_THRESHOLD_DEFAULT)

    def test_feed_learning_outcome(self):
        """feed_learning_outcome passes through to adapter."""
        ml = MetaLearner()
        ml.feed_learning_outcome(is_trauma=True,
                                 coherence_before=0.5,
                                 coherence_after=0.7)
        self.assertEqual(ml.learning_rate.stats['trauma_samples'], 1)


# ================================================================
#  INTEGRATION TEST
# ================================================================

class TestIntegration(unittest.TestCase):
    """Full system integration under extreme conditions."""

    def test_adapted_band_differs_under_extreme_red(self):
        """After sustained RED, adapted thresholds should differ from defaults,
        potentially reclassifying a borderline coherence value."""
        ml = MetaLearner()

        # Sustained RED for many evaluation windows
        for t in range(EVALUATION_WINDOW * 5):
            ml.tick(tick=t, coherence=0.3, band=RED,
                    is_trauma=False, crystals=0, mode=0)

        # After adaptation, the green threshold should be lower
        self.assertLess(ml.thresholds.green_threshold,
                        GREEN_THRESHOLD_DEFAULT)

        # A value that was YELLOW under default should now be classified
        # higher since thresholds dropped
        borderline = 0.68
        default_tuner = ThresholdTuner()
        default_band = default_tuner.get_band(borderline)
        adapted_band = ml.thresholds.get_band(borderline)

        # Under default, 0.68 < 0.7143 (T*), so it's YELLOW
        self.assertEqual(default_band, YELLOW)
        # Under lowered thresholds, it might be GREEN now
        # (green_threshold could have dropped to ~0.65)
        self.assertGreaterEqual(adapted_band, YELLOW)

    def test_all_parameters_stable_after_mixed_input(self):
        """No parameter diverges after mixed trauma/success/coherence input."""
        ml = MetaLearner()

        for t in range(EVALUATION_WINDOW * 10):
            # Alternate between trauma and success, varying coherence
            is_trauma = (t % 3 == 0)
            coherence = 0.3 + (t % 7) * 0.1  # Cycles 0.3 - 0.9
            band = ml.thresholds.get_band(coherence)
            crystals = 1 if coherence > 0.6 else 0
            mode = min(3, int(coherence * 4))

            result = ml.tick(tick=t, coherence=coherence, band=band,
                             is_trauma=is_trauma, crystals=crystals, mode=mode)

            if is_trauma:
                ml.feed_learning_outcome(
                    is_trauma=True,
                    coherence_before=coherence,
                    coherence_after=coherence + 0.05)

            # Safety: all outputs in bounds at every tick
            self.assertGreaterEqual(result['trauma_mult'], MIN_TRAUMA_MULT)
            self.assertLessEqual(result['trauma_mult'], MAX_TRAUMA_MULT)
            self.assertGreaterEqual(result['success_mult'], MIN_SUCCESS_MULT)
            self.assertLessEqual(result['success_mult'], MAX_SUCCESS_MULT)
            self.assertGreaterEqual(result['green_threshold'],
                                    MIN_GREEN_THRESHOLD)
            self.assertLessEqual(result['green_threshold'],
                                 MAX_GREEN_THRESHOLD)
            self.assertGreaterEqual(result['yellow_threshold'],
                                    MIN_YELLOW_THRESHOLD)
            self.assertLessEqual(result['yellow_threshold'],
                                 MAX_YELLOW_THRESHOLD)
            self.assertGreaterEqual(result['complexity'], 0.0)
            self.assertLessEqual(result['complexity'], MAX_COMPLEXITY)
            self.assertIn(result['band'], (RED, YELLOW, GREEN))


if __name__ == '__main__':
    unittest.main()
