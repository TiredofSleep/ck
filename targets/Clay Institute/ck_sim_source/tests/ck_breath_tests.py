"""
ck_breath_tests.py -- Tests for Breath-Defect Flow Model + Breath Index
========================================================================
Operator: BREATH (8) -- Oscillation between scales, dual loops.

Tests:
  1. Decomposition of known trajectories
  2. Breath primitives (alpha_E, alpha_C, beta, sigma)
  3. Breath Index B_idx
  4. Fear-collapse detection
  5. Deep/shallow flow classification
  6. Regime classification
  7. Live spectrometer breath scans (all 6 Clay problems)
  8. RATE-trace breath analysis
  9. Multi-seed breath estimates
  10. Breath atlas

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.doing.ck_breath_engine import (
    BreathEngine, BreathStep, BreathPrimitives, BreathResult,
    breath_step_to_dict, breath_result_to_dict,
    FEAR_OSCILLATION_THRESHOLD, FEAR_RATIO_THRESHOLD,
    B_IDX_HEALTHY, B_IDX_STRESSED,
    REGIME_HEALTHY, REGIME_STRESSED, REGIME_FEAR_COLLAPSED, REGIME_CHAOTIC,
)
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS


class TestBreathDecompose(unittest.TestCase):
    """Test trajectory decomposition into breath steps."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_simple_oscillation(self):
        """E-C-E-C pattern should produce steps with alternating g_e/g_c."""
        traj = [1.0, 1.5, 1.0, 1.5, 1.0]  # up-down-up-down
        steps = self.engine.decompose(traj)
        self.assertEqual(len(steps), 3)  # 5 values -> 3 triplets

    def test_monotone_decrease(self):
        """Monotone decreasing = all contraction, no expansion."""
        traj = [1.0, 0.8, 0.6, 0.4, 0.2]
        steps = self.engine.decompose(traj)
        # First half of each triplet (v_before -> v_mid) decreases
        for s in steps:
            self.assertLessEqual(s.delta_e, 0)  # No expansion
            self.assertLessEqual(s.delta_c, 0)  # Contraction

    def test_monotone_increase(self):
        """Monotone increasing = all expansion, no contraction."""
        traj = [0.2, 0.4, 0.6, 0.8, 1.0]
        steps = self.engine.decompose(traj)
        for s in steps:
            self.assertGreaterEqual(s.delta_e, 0)  # Expansion
            self.assertGreaterEqual(s.delta_c, 0)  # No contraction (mid -> after increases)

    def test_too_short(self):
        """Trajectory with < 3 values should return empty."""
        self.assertEqual(self.engine.decompose([1.0, 2.0]), [])
        self.assertEqual(self.engine.decompose([1.0]), [])
        self.assertEqual(self.engine.decompose([]), [])


class TestBreathPrimitives(unittest.TestCase):
    """Test computation of alpha_E, alpha_C, beta, sigma."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_perfect_oscillation(self):
        """Perfect E-C-E-C should have high alpha_E, alpha_C, and beta."""
        traj = [0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5]
        steps = self.engine.decompose(traj)
        prims = self.engine.compute_primitives(steps)
        self.assertGreater(prims.alpha_e, 0.3)
        self.assertGreater(prims.alpha_c, 0.3)
        self.assertGreater(prims.beta, 0.5)
        self.assertGreater(prims.sigma, 0.3)

    def test_no_expansion(self):
        """Monotone decrease should have alpha_E ~ 0."""
        traj = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
        steps = self.engine.decompose(traj)
        prims = self.engine.compute_primitives(steps)
        # alpha_E should be very low (no expansion gain)
        self.assertLess(prims.alpha_e, 0.1)

    def test_all_values_in_range(self):
        """All primitives should be in [0, 1]."""
        traj = [0.3, 0.7, 0.2, 0.9, 0.1, 0.8, 0.4]
        steps = self.engine.decompose(traj)
        prims = self.engine.compute_primitives(steps)
        for name in ('alpha_e', 'alpha_c', 'beta', 'sigma'):
            val = getattr(prims, name)
            self.assertGreaterEqual(val, 0.0, f'{name} < 0')
            self.assertLessEqual(val, 1.0, f'{name} > 1')

    def test_empty_steps(self):
        """Empty steps should return all-zero primitives."""
        prims = self.engine.compute_primitives([])
        self.assertEqual(prims.alpha_e, 0.0)
        self.assertEqual(prims.alpha_c, 0.0)
        self.assertEqual(prims.beta, 0.0)
        self.assertEqual(prims.sigma, 0.0)


class TestBreathIndex(unittest.TestCase):
    """Test B_idx computation."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_perfect_primitives(self):
        """All primitives = 1.0 => B_idx = 1.0."""
        prims = BreathPrimitives(1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(self.engine.breath_index(prims), 1.0, places=4)

    def test_zero_primitive(self):
        """Any primitive = 0 => B_idx = 0."""
        self.assertEqual(self.engine.breath_index(
            BreathPrimitives(0.0, 0.5, 0.5, 0.5)), 0.0)
        self.assertEqual(self.engine.breath_index(
            BreathPrimitives(0.5, 0.0, 0.5, 0.5)), 0.0)
        self.assertEqual(self.engine.breath_index(
            BreathPrimitives(0.5, 0.5, 0.0, 0.5)), 0.0)
        self.assertEqual(self.engine.breath_index(
            BreathPrimitives(0.5, 0.5, 0.5, 0.0)), 0.0)

    def test_geometric_mean(self):
        """B_idx = (a_E * a_C * beta * sigma)^(1/4)."""
        prims = BreathPrimitives(0.8, 0.6, 0.7, 0.9)
        expected = (0.8 * 0.6 * 0.7 * 0.9) ** 0.25
        self.assertAlmostEqual(self.engine.breath_index(prims),
                               expected, places=6)

    def test_b_idx_in_range(self):
        """B_idx should always be in [0, 1]."""
        prims = BreathPrimitives(0.3, 0.7, 0.4, 0.8)
        b = self.engine.breath_index(prims)
        self.assertGreaterEqual(b, 0.0)
        self.assertLessEqual(b, 1.0)


class TestFearCollapse(unittest.TestCase):
    """Test fear-collapse detection."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_healthy_oscillation_not_collapsed(self):
        """Normal E-C oscillation should NOT be fear-collapsed."""
        traj = [0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5]
        steps = self.engine.decompose(traj)
        collapsed, osc = self.engine.detect_fear_collapse(steps)
        self.assertFalse(collapsed)
        self.assertGreater(osc, FEAR_OSCILLATION_THRESHOLD)

    def test_contraction_only_collapsed(self):
        """Monotone decrease should trigger fear-collapse."""
        traj = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
        steps = self.engine.decompose(traj)
        collapsed, osc = self.engine.detect_fear_collapse(steps)
        self.assertTrue(collapsed)

    def test_oscillation_amplitude(self):
        """Perfect alternation => amplitude ~ 1.0."""
        traj = [0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5]
        steps = self.engine.decompose(traj)
        _, osc = self.engine.detect_fear_collapse(steps)
        self.assertGreater(osc, 0.5)


class TestFlowTypes(unittest.TestCase):
    """Test deep/shallow flow classification."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_deep_flows(self):
        """Steps with both g_e and g_c active = deep flows."""
        traj = [0.5, 1.0, 0.5, 1.0, 0.5]  # E then C in each triplet
        steps = self.engine.decompose(traj)
        deep, shallow = self.engine.count_flow_types(steps)
        self.assertGreater(deep, 0)


class TestRegimeClassification(unittest.TestCase):
    """Test breath regime classification."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_healthy(self):
        r = self.engine.classify_regime(
            0.7, False, BreathPrimitives(0.5, 0.5, 0.8, 0.9))
        self.assertEqual(r, REGIME_HEALTHY)

    def test_stressed(self):
        r = self.engine.classify_regime(
            0.35, False, BreathPrimitives(0.3, 0.3, 0.5, 0.5))
        self.assertEqual(r, REGIME_STRESSED)

    def test_fear_collapsed(self):
        r = self.engine.classify_regime(
            0.1, True, BreathPrimitives(0.1, 0.5, 0.2, 0.3))
        self.assertEqual(r, REGIME_FEAR_COLLAPSED)

    def test_chaotic(self):
        r = self.engine.classify_regime(
            0.3, False, BreathPrimitives(0.8, 0.1, 0.3, 0.5))
        self.assertEqual(r, REGIME_CHAOTIC)


class TestFullAnalysis(unittest.TestCase):
    """Test full breath analysis on synthetic trajectories."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_analyze_oscillating(self):
        """Healthy oscillation should produce healthy regime."""
        traj = [0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5]
        result = self.engine.analyze_trajectory(traj, 'test', 42)
        self.assertIsInstance(result, BreathResult)
        self.assertEqual(result.problem_id, 'test')
        self.assertGreater(result.b_idx, 0.0)
        self.assertFalse(result.fear_collapsed)

    def test_analyze_monotone_decrease(self):
        """Monotone decrease should trigger fear-collapse."""
        traj = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        result = self.engine.analyze_trajectory(traj, 'test', 42)
        self.assertTrue(result.fear_collapsed)
        self.assertEqual(result.breath_regime, REGIME_FEAR_COLLAPSED)


class TestSerialization(unittest.TestCase):
    """Test serialization helpers."""

    def setUp(self):
        self.engine = BreathEngine()

    def test_breath_step_to_dict(self):
        step = BreathStep(0, 1.0, 1.5, 1.0)
        d = breath_step_to_dict(step)
        self.assertEqual(d['index'], 0)
        self.assertAlmostEqual(d['v_before'], 1.0)
        self.assertAlmostEqual(d['delta_e'], 0.5)

    def test_breath_result_to_dict(self):
        traj = [0.5, 1.0, 0.5, 1.0, 0.5]
        result = self.engine.analyze_trajectory(traj, 'test', 42)
        d = breath_result_to_dict(result)
        self.assertEqual(d['problem_id'], 'test')
        self.assertIn('b_idx', d)
        self.assertIn('primitives', d)
        self.assertIn('alpha_e', d['primitives'])
        self.assertIn('steps', d)


# ================================================================
#  LIVE ENGINE TESTS (requires spectrometer)
# ================================================================

class TestLiveBreathScan(unittest.TestCase):
    """Live breath scans on all 6 Clay problems."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer
        cls.spec = DeltaSpectrometer()

    def test_breath_scan_all_clay(self):
        """Breath scan should produce valid results for all 6 Clay problems."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        for pid in CLAY_PROBLEMS:
            pt = ProblemType(pid)
            result = self.spec.breath_scan(pt, seed=42)
            self.assertEqual(result['problem_id'], pid)
            self.assertIn('b_idx', result)
            self.assertGreaterEqual(result['b_idx'], 0.0)
            self.assertLessEqual(result['b_idx'], 1.0)
            self.assertIn(result['breath_regime'],
                         [REGIME_HEALTHY, REGIME_STRESSED,
                          REGIME_FEAR_COLLAPSED, REGIME_CHAOTIC])

    def test_breath_scan_has_primitives(self):
        """Breath scan results should include all four primitives."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('navier_stokes')
        result = self.spec.breath_scan(pt, seed=42)
        prims = result['primitives']
        for key in ('alpha_e', 'alpha_c', 'beta', 'sigma'):
            self.assertIn(key, prims)
            self.assertGreaterEqual(prims[key], 0.0)
            self.assertLessEqual(prims[key], 1.0)

    def test_breath_scan_has_flow_counts(self):
        """Should classify deep vs shallow flows."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('riemann')
        result = self.spec.breath_scan(pt, seed=42)
        self.assertIn('deep_flow_count', result)
        self.assertIn('shallow_flow_count', result)
        self.assertGreaterEqual(result['deep_flow_count'], 0)
        self.assertGreaterEqual(result['shallow_flow_count'], 0)


class TestLiveBreathRate(unittest.TestCase):
    """Breath analysis on RATE traces."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer
        cls.spec = DeltaSpectrometer()

    def test_breath_rate_scan_ns(self):
        """RATE-trace breath analysis for NS."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('navier_stokes')
        result = self.spec.breath_rate_scan(pt, seed=42)
        self.assertEqual(result['problem_id'], 'navier_stokes')
        self.assertIn('b_idx', result)
        self.assertGreaterEqual(result['b_idx'], 0.0)

    def test_breath_rate_scan_pnp(self):
        """RATE-trace breath analysis for PNP."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('p_vs_np')
        result = self.spec.breath_rate_scan(pt, seed=42)
        self.assertEqual(result['problem_id'], 'p_vs_np')
        self.assertIn('b_idx', result)


class TestLiveBreathEstimate(unittest.TestCase):
    """Multi-seed breath estimates."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer
        cls.spec = DeltaSpectrometer()

    def test_breath_estimate_ns(self):
        """Multi-seed breath estimate for NS."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('navier_stokes')
        result = self.spec.breath_estimate(pt, seeds=[42, 43, 44])
        self.assertEqual(result['problem_id'], 'navier_stokes')
        self.assertEqual(result['seeds_used'], 3)
        self.assertIn('b_idx_mean', result)
        self.assertIn('b_idx_std', result)
        self.assertIn('regime', result)

    def test_breath_estimate_has_aggregated_primitives(self):
        """Should aggregate primitives across seeds."""
        from ck_sim.doing.ck_spectrometer import ProblemType
        pt = ProblemType('riemann')
        result = self.spec.breath_estimate(pt, seeds=[42, 43])
        for key in ('alpha_e_mean', 'alpha_c_mean', 'beta_mean', 'sigma_mean'):
            self.assertIn(key, result)


class TestLiveBreathAtlas(unittest.TestCase):
    """Full breath atlas."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer
        cls.spec = DeltaSpectrometer()

    def test_breath_atlas_clay(self):
        """Breath atlas should cover all 6 Clay problems."""
        result = self.spec.breath_atlas(list(CLAY_PROBLEMS), seeds=[42, 43])
        self.assertIn('estimates', result)
        self.assertIn('summary', result)
        estimates = result['estimates']
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, estimates, f'Missing {pid} from atlas')
            self.assertIn('b_idx_mean', estimates[pid])

    def test_breath_atlas_summary(self):
        """Summary should identify healthiest/most stressed."""
        result = self.spec.breath_atlas(list(CLAY_PROBLEMS), seeds=[42])
        summary = result['summary']
        self.assertEqual(summary['problems_analyzed'], 6)
        self.assertIn('healthiest', summary)
        self.assertIn('most_stressed', summary)
        self.assertIn('mean_b_idx', summary)
        self.assertIn('regimes', summary)


if __name__ == '__main__':
    unittest.main()
