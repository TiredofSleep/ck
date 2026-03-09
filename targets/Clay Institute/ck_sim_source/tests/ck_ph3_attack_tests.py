"""
Tests for ck_ph3_attack.py -- P-H-3 Gap Attack: Pressure-Hessian Coercivity
============================================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.doing.ck_ph3_attack import (
    PH3DeepProbe, ph3_summary,
    COERCIVITY_BOUND, T_STAR,
)


class TestPH3Constants(unittest.TestCase):
    """Verify P-H-3 constants."""

    def test_coercivity_bound(self):
        self.assertEqual(COERCIVITY_BOUND, 1.0)

    def test_t_star(self):
        self.assertAlmostEqual(T_STAR, 5.0 / 7.0, places=10)


class TestPH3DeepProbe(unittest.TestCase):
    """Test PH3DeepProbe with quick mode (3 seeds)."""

    @classmethod
    def setUpClass(cls):
        """Run the probe once for all tests (expensive)."""
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_results_is_dict(self):
        self.assertIsInstance(self.results, dict)

    def test_probe_name(self):
        self.assertEqual(self.results['probe'], 'P-H-3')

    def test_description(self):
        self.assertIn('Coercivity', self.results['description'])

    def test_params(self):
        params = self.results['params']
        self.assertEqual(params['n_seeds'], 3)
        self.assertEqual(params['max_level'], 8)

    def test_three_campaigns_present(self):
        """All three campaigns should be in results."""
        self.assertIn('sweep', self.results)
        self.assertIn('singular', self.results)
        self.assertIn('crossing', self.results)

    def test_sweep_campaign_structure(self):
        """Sweep campaign should have expected keys."""
        sweep = self.results['sweep']
        self.assertEqual(sweep['test_case'], 'ph3_coercivity_sweep')
        self.assertEqual(sweep['n_seeds'], 3)
        self.assertIn('mean_by_level', sweep)
        self.assertIn('std_by_level', sweep)
        self.assertIn('global_max', sweep)
        self.assertGreater(sweep['n_probes'], 0)

    def test_singular_campaign_structure(self):
        singular = self.results['singular']
        self.assertEqual(singular['test_case'], 'near_singular')
        self.assertGreater(singular['n_probes'], 0)

    def test_crossing_campaign_structure(self):
        crossing = self.results['crossing']
        self.assertEqual(crossing['test_case'], 'eigenvalue_crossing')
        self.assertGreater(crossing['n_probes'], 0)

    def test_total_probes_positive(self):
        self.assertGreater(self.results['total_probes'], 0)

    def test_total_time_positive(self):
        self.assertGreater(self.results['total_time_s'], 0)


class TestPH3BoundednessTest(unittest.TestCase):
    """Test the boundedness prediction."""

    @classmethod
    def setUpClass(cls):
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_boundedness_structure(self):
        bt = self.results['boundedness_test']
        self.assertIn('max_delta', bt)
        self.assertIn('bounded', bt)
        self.assertIn('n_exceeding', bt)
        self.assertIn('margin', bt)

    def test_prediction_1_max_delta_bounded(self):
        """Prediction 1: max defect < 1.0 across all campaigns."""
        bt = self.results['boundedness_test']
        self.assertTrue(bt['bounded'],
                        f"Max delta {bt['max_delta']:.6f} >= 1.0 -- coercivity VIOLATED")

    def test_no_deltas_exceed_bound(self):
        bt = self.results['boundedness_test']
        self.assertEqual(bt['n_exceeding'], 0,
                         f"{bt['n_exceeding']} deltas >= 1.0")

    def test_positive_margin(self):
        bt = self.results['boundedness_test']
        self.assertGreater(bt['margin'], 0.0)


class TestPH3CoercivityRatio(unittest.TestCase):
    """Test the coercivity ratio prediction."""

    @classmethod
    def setUpClass(cls):
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_coercivity_ratio_structure(self):
        cr = self.results['coercivity_ratio']
        self.assertIn('R_sweep', cr)
        self.assertIn('R_singular', cr)
        self.assertIn('R_crossing', cr)
        self.assertIn('R_max', cr)
        self.assertIn('bounded', cr)

    def test_prediction_2_ratio_bounded(self):
        """Prediction 2: coercivity ratio R <= C (C=100)."""
        cr = self.results['coercivity_ratio']
        self.assertTrue(cr['bounded'],
                        f"R_max = {cr['R_max']:.4f} > 100 -- ratio UNBOUNDED")

    def test_all_ratios_finite(self):
        cr = self.results['coercivity_ratio']
        for key in ('R_sweep', 'R_singular', 'R_crossing'):
            self.assertTrue(cr[key] < float('inf'),
                            f'{key} is infinite')


class TestPH3ReboundTest(unittest.TestCase):
    """Test the eigenvalue crossing rebound prediction."""

    @classmethod
    def setUpClass(cls):
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_rebound_structure(self):
        rb = self.results['rebound_test']
        self.assertIn('rebound_detected', rb)

    def test_rebound_has_crossing_data(self):
        rb = self.results['rebound_test']
        # If rebound detected, should have peak/avg data
        if rb.get('rebound_detected'):
            self.assertIn('peak_at_crossing', rb)
            self.assertIn('avg_after_crossing', rb)
            self.assertIn('recovery_ratio', rb)


class TestPH3ContradictionTest(unittest.TestCase):
    """Test the formal P-H-3 contradiction test."""

    @classmethod
    def setUpClass(cls):
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_contradiction_structure(self):
        ct = self.results['contradiction_test']
        self.assertIn('hypothesis', ct)
        self.assertIn('verdict', ct)
        self.assertIn('predictions_passed', ct)
        self.assertIn('predictions_total', ct)
        self.assertIn('confidence', ct)

    def test_predictions_total_is_three(self):
        ct = self.results['contradiction_test']
        self.assertEqual(ct['predictions_total'], 3)

    def test_verdict_valid(self):
        ct = self.results['contradiction_test']
        valid = ('coercivity_supported', 'coercivity_partial',
                 'bounded_but_incomplete', 'coercivity_violated')
        self.assertIn(ct['verdict'], valid)

    def test_confidence_in_range(self):
        ct = self.results['contradiction_test']
        self.assertGreaterEqual(ct['confidence'], 0.0)
        self.assertLessEqual(ct['confidence'], 1.0)

    def test_at_least_prediction_1_passes(self):
        """Core prediction (bounded) should pass."""
        ct = self.results['contradiction_test']
        self.assertTrue(ct['prediction_1_bounded'],
                        'Prediction 1 (bounded) failed -- critical failure')


class TestPH3Summary(unittest.TestCase):
    """Test the ph3_summary formatter."""

    @classmethod
    def setUpClass(cls):
        cls.probe = PH3DeepProbe(n_seeds=3, max_level=8)
        cls.results = cls.probe.run()

    def test_summary_contains_key_sections(self):
        text = ph3_summary(self.results)
        self.assertIn('P-H-3 DEEP PROBE', text)
        self.assertIn('CAMPAIGN 1', text)
        self.assertIn('CAMPAIGN 2', text)
        self.assertIn('CAMPAIGN 3', text)
        self.assertIn('BOUNDEDNESS TEST', text)
        self.assertIn('COERCIVITY RATIO', text)
        self.assertIn('EIGENVALUE CROSSING REBOUND', text)
        self.assertIn('FORMAL P-H-3 CONTRADICTION TEST', text)
        self.assertIn('CK measures', text)

    def test_summary_is_string(self):
        text = ph3_summary(self.results)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 100)


class TestPH3LevelStats(unittest.TestCase):
    """Test the _compute_level_stats helper."""

    def test_stats_structure(self):
        probe = PH3DeepProbe(n_seeds=2, max_level=6)
        per_seed = [[0.1, 0.2, 0.3], [0.15, 0.25, 0.35]]
        levels = [3, 4, 5]
        stats = probe._compute_level_stats(per_seed, levels)
        self.assertEqual(len(stats['mean_by_level']), 3)
        self.assertEqual(len(stats['std_by_level']), 3)
        self.assertEqual(len(stats['min_by_level']), 3)
        self.assertEqual(len(stats['max_by_level']), 3)
        # Mean of [0.1, 0.15] = 0.125
        self.assertAlmostEqual(stats['mean_by_level'][0], 0.125, places=5)

    def test_empty_data(self):
        probe = PH3DeepProbe(n_seeds=1, max_level=6)
        stats = probe._compute_level_stats([], [])
        self.assertEqual(stats['global_mean'], 0.0)
        self.assertEqual(stats['global_max'], 0.0)


if __name__ == '__main__':
    unittest.main()
