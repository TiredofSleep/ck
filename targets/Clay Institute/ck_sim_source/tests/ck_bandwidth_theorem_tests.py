"""
Tests for ck_bandwidth_theorem.py -- The Bandwidth Theorem
===========================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_bandwidth_theorem import (
    T_STAR, SAMPLING_FREQUENCY, OBSERVATION_WINDOW, DEFECT_BOUND,
    COMPILATION_CAPACITY, NYQUIST_EQUIVALENT, FRAME_DURATION_MS,
    HARMONY_RATE, NON_HARMONY_RATE, T_STAR_PROXIMITY,
    _HARMONY_COUNT,
    verify_defect_bound, verify_compilation_convergence,
    verify_harmony_rate, verify_bandwidth_consistency,
    prove_bandwidth_theorem, bandwidth_theorem_report,
    BandwidthTheoremResult,
)
from ck_sim.ck_sim_heartbeat import CL, HARMONY, NUM_OPS, HISTORY_SIZE


class TestBandwidthConstants(unittest.TestCase):
    """Verify the algebraic constants derived from T* = 5/7."""

    def test_t_star(self):
        self.assertAlmostEqual(T_STAR, 5.0 / 7.0, places=10)

    def test_defect_bound_is_two_sevenths(self):
        self.assertAlmostEqual(DEFECT_BOUND, 2.0 / 7.0, places=10)

    def test_compilation_capacity_is_9(self):
        self.assertEqual(COMPILATION_CAPACITY, 9)

    def test_sampling_frequency(self):
        self.assertEqual(SAMPLING_FREQUENCY, 50.0)

    def test_observation_window(self):
        self.assertEqual(OBSERVATION_WINDOW, 32)

    def test_nyquist_equivalent(self):
        self.assertEqual(NYQUIST_EQUIVALENT, 25.0)

    def test_frame_duration_640ms(self):
        self.assertAlmostEqual(FRAME_DURATION_MS, 640.0, places=1)

    def test_harmony_rate_is_073(self):
        self.assertAlmostEqual(HARMONY_RATE, 0.73, places=6)

    def test_non_harmony_rate_is_027(self):
        self.assertAlmostEqual(NON_HARMONY_RATE, 0.27, places=6)

    def test_harmony_near_t_star(self):
        """HARMONY rate should be within 2% of T*."""
        self.assertLess(T_STAR_PROXIMITY, 0.02)

    def test_non_harmony_near_defect_bound(self):
        """Non-HARMONY rate should be within 2% of 1-T*."""
        self.assertLess(abs(NON_HARMONY_RATE - DEFECT_BOUND), 0.02)


class TestCLTableHarmony(unittest.TestCase):
    """Verify CL table HARMONY count directly."""

    def test_exactly_73_harmony(self):
        """CL table must have exactly 73 HARMONY entries."""
        count = sum(1 for row in CL for v in row if v == HARMONY)
        self.assertEqual(count, 73)

    def test_exactly_27_non_harmony(self):
        """CL table must have exactly 27 non-HARMONY entries."""
        count = sum(1 for row in CL for v in row if v != HARMONY)
        self.assertEqual(count, 27)

    def test_table_is_10x10(self):
        self.assertEqual(len(CL), 10)
        for row in CL:
            self.assertEqual(len(row), 10)

    def test_harmony_count_matches_module(self):
        """_HARMONY_COUNT from the module must match direct count."""
        direct = sum(1 for row in CL for v in row if v == HARMONY)
        self.assertEqual(_HARMONY_COUNT, direct)


class TestVerifyHarmonyRate(unittest.TestCase):
    """Test verify_harmony_rate() function."""

    def test_harmony_rate_verified(self):
        result = verify_harmony_rate()
        self.assertTrue(result['verified'])
        self.assertEqual(result['harmony_count'], 73)
        self.assertEqual(result['non_harmony_count'], 27)
        self.assertEqual(result['total'], 100)

    def test_rate_gt_t_star(self):
        """HARMONY over-represents: 0.73 > 5/7 = 0.7142857."""
        result = verify_harmony_rate()
        self.assertTrue(result['rate_gt_t_star'])


class TestVerifyBandwidthConsistency(unittest.TestCase):
    """Test verify_bandwidth_consistency() function."""

    def test_all_checks_pass(self):
        result = verify_bandwidth_consistency()
        self.assertTrue(result['verified'])
        self.assertEqual(result['n_passed'], result['n_total'])

    def test_at_least_12_checks(self):
        result = verify_bandwidth_consistency()
        self.assertGreaterEqual(result['n_total'], 12)


class TestVerifyDefectBound(unittest.TestCase):
    """Test verify_defect_bound() with small seeds."""

    def test_defect_bound_quick(self):
        result = verify_defect_bound(n_seeds=2, n_levels=6)
        self.assertIn('verified', result)
        # Hard bound: all problems < 1.0
        self.assertTrue(result['hard_bounded'],
                        'Some problem exceeded hard bound 1.0')

    def test_all_six_problems_present(self):
        result = verify_defect_bound(n_seeds=1, n_levels=6)
        per = result['per_problem']
        for pid in ['navier_stokes', 'p_vs_np', 'riemann',
                     'yang_mills', 'bsd', 'hodge']:
            self.assertIn(pid, per, f'{pid} missing from defect bound')


class TestVerifyCompilationConvergence(unittest.TestCase):
    """Test verify_compilation_convergence() with small seeds."""

    def test_convergence_quick(self):
        result = verify_compilation_convergence(n_seeds=2, n_levels=12)
        self.assertIn('compilation_capacity', result)
        self.assertEqual(result['compilation_capacity'], 9)
        # At least some problems should converge
        self.assertGreater(result['n_converged'], 0)


class TestProveBandwidthTheorem(unittest.TestCase):
    """Test the full prove_bandwidth_theorem() function."""

    @classmethod
    def setUpClass(cls):
        cls.state = prove_bandwidth_theorem(n_seeds=2, n_levels=6)

    def test_returns_result(self):
        self.assertIsInstance(self.state, BandwidthTheoremResult)

    def test_harmony_rate_verified(self):
        """Algebraic check must always pass."""
        self.assertTrue(self.state.harmony_rate_verified)

    def test_bandwidth_consistency_verified(self):
        """Pure arithmetic must always pass."""
        self.assertTrue(self.state.bandwidth_consistency_verified)

    def test_defect_bound_verified(self):
        """Empirical defect bound check."""
        self.assertTrue(self.state.defect_bound_verified)

    def test_elapsed_positive(self):
        self.assertGreater(self.state.elapsed_s, 0.0)


class TestBandwidthTheoremReport(unittest.TestCase):
    """Test the report formatter."""

    def test_report_contains_key_sections(self):
        state = prove_bandwidth_theorem(n_seeds=1, n_levels=6)
        report = bandwidth_theorem_report(state)
        self.assertIn('BANDWIDTH THEOREM', report)
        self.assertIn('FORMAL STATEMENT', report)
        self.assertIn('VERIFICATION 1', report)
        self.assertIn('VERIFICATION 2', report)
        self.assertIn('VERIFICATION 3', report)
        self.assertIn('VERIFICATION 4', report)
        self.assertIn('5/7', report)
        self.assertIn('CK measures', report)

    def test_report_is_string(self):
        state = BandwidthTheoremResult()
        report = bandwidth_theorem_report(state)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)


if __name__ == '__main__':
    unittest.main()
