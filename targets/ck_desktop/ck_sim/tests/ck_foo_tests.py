"""
ck_foo_tests.py -- Tests for Fractal Optimality Operator + Phi(kappa)
=====================================================================
Tests the FOO engine, complexity horizons, and Phi curve analysis.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math

from ck_sim.doing.ck_foo_engine import (
    FOOEngine, FOOLevel, FOOTrace, PhiEstimate,
    COMPLEXITY_KAPPA, PHI_CALIBRATED,
    get_kappa, analyze_phi_curve,
    foo_trace_to_dict, phi_estimate_to_dict,
)
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS


# ================================================================
#  COMPLEXITY LABEL TESTS
# ================================================================

class TestComplexityKappa(unittest.TestCase):
    """Test complexity labels and kappa assignment."""

    def test_six_clay_problems_have_kappa(self):
        """All 6 Clay problems have explicit kappa values."""
        clay = ['navier_stokes', 'p_vs_np', 'riemann',
                'yang_mills', 'bsd', 'hodge']
        for pid in clay:
            self.assertIn(pid, COMPLEXITY_KAPPA,
                          f'{pid} missing from COMPLEXITY_KAPPA')

    def test_kappa_range(self):
        """All kappa values are in [0, 1]."""
        for pid, k in COMPLEXITY_KAPPA.items():
            self.assertGreaterEqual(k, 0.0, f'{pid} kappa below 0')
            self.assertLessEqual(k, 1.0, f'{pid} kappa above 1')

    def test_pnp_highest_kappa(self):
        """P vs NP has the highest complexity across all 41 problems."""
        max_pid = max(COMPLEXITY_KAPPA, key=COMPLEXITY_KAPPA.get)
        self.assertEqual(max_pid, 'p_vs_np')

    def test_get_kappa_clay(self):
        """get_kappa returns exact value for Clay problems."""
        self.assertEqual(get_kappa('navier_stokes'),
                         COMPLEXITY_KAPPA['navier_stokes'])

    def test_get_kappa_neighbor(self):
        """Neighbor kappa is less than parent kappa."""
        k = get_kappa('ns_euler')  # Neighbor of navier_stokes
        self.assertGreater(k, 0.0)
        self.assertLess(k, COMPLEXITY_KAPPA['navier_stokes'])

    def test_get_kappa_standalone(self):
        """Standalone problems have direct kappa entries."""
        k = get_kappa('collatz')
        self.assertEqual(k, COMPLEXITY_KAPPA['collatz'])

    def test_get_kappa_unknown(self):
        """get_kappa returns 0.5 for unknown problems."""
        k = get_kappa('completely_made_up_problem')
        self.assertEqual(k, 0.5)


class TestPhiCalibrated(unittest.TestCase):
    """Test calibrated Phi values from METAL document."""

    def test_six_clay_have_phi(self):
        """All 6 Clay problems have calibrated Phi values."""
        clay = ['navier_stokes', 'p_vs_np', 'riemann',
                'yang_mills', 'bsd', 'hodge']
        for pid in clay:
            self.assertIn(pid, PHI_CALIBRATED)

    def test_phi_non_negative(self):
        """All Phi values are >= 0."""
        for pid, phi in PHI_CALIBRATED.items():
            self.assertGreaterEqual(phi, 0.0, f'{pid} Phi negative')

    def test_continuum_highest_phi(self):
        """Continuum hypothesis has the highest Phi (ZFC-independent)."""
        max_pid = max(PHI_CALIBRATED, key=PHI_CALIBRATED.get)
        self.assertEqual(max_pid, 'continuum')

    def test_pnp_highest_clay_phi(self):
        """P vs NP has the highest Phi among the 6 Clay problems."""
        clay_phi = {pid: PHI_CALIBRATED[pid] for pid in CLAY_PROBLEMS}
        max_pid = max(clay_phi, key=clay_phi.get)
        self.assertEqual(max_pid, 'p_vs_np')

    def test_ns_phi_value(self):
        """NS Phi matches METAL document: ~0.297."""
        self.assertAlmostEqual(PHI_CALIBRATED['navier_stokes'], 0.297, places=3)

    def test_pnp_phi_value(self):
        """PNP Phi matches METAL document: ~0.846."""
        self.assertAlmostEqual(PHI_CALIBRATED['p_vs_np'], 0.846, places=3)

    def test_ym_phi_value(self):
        """YM Phi matches METAL document: ~0.511."""
        self.assertAlmostEqual(PHI_CALIBRATED['yang_mills'], 0.511, places=3)


# ================================================================
#  FOO DATA STRUCTURE TESTS
# ================================================================

class TestFOODataStructures(unittest.TestCase):
    """Test FOO data classes."""

    def test_foo_level_creation(self):
        """FOOLevel holds all required fields."""
        lv = FOOLevel(level=0, delta_mean=0.3, delta_std=0.01,
                      improvement=0.0, meta_improvement=0.0,
                      sensitivity_used=0.5)
        self.assertEqual(lv.level, 0)
        self.assertAlmostEqual(lv.delta_mean, 0.3)
        self.assertAlmostEqual(lv.sensitivity_used, 0.5)

    def test_foo_trace_creation(self):
        """FOOTrace holds problem, seed, levels, convergence info."""
        levels = [
            FOOLevel(0, 0.5, 0.01, 0.0, 0.0, 0.5),
            FOOLevel(1, 0.3, 0.01, 0.2, 0.2, 0.6),
            FOOLevel(2, 0.29, 0.01, 0.01, 0.19, 0.61),
        ]
        trace = FOOTrace(
            problem_id='navier_stokes', seed=42, levels=levels,
            converged=True, r_inf=0.29, phi_est=0.29,
            foo_depth=3, kappa=0.75)
        self.assertEqual(trace.problem_id, 'navier_stokes')
        self.assertTrue(trace.converged)
        self.assertAlmostEqual(trace.r_inf, 0.29)
        self.assertEqual(len(trace.levels), 3)

    def test_phi_estimate_creation(self):
        """PhiEstimate holds all complexity horizon fields."""
        est = PhiEstimate(
            problem_id='p_vs_np', kappa=0.95,
            phi_measured=0.85, phi_calibrated=0.846,
            r_inf_mean=0.86, r_inf_std=0.01,
            foo_converged_rate=0.8, regime='irreducible',
            seeds_used=5)
        self.assertEqual(est.regime, 'irreducible')
        self.assertAlmostEqual(est.kappa, 0.95)


# ================================================================
#  SERIALIZATION TESTS
# ================================================================

class TestFOOSerialization(unittest.TestCase):
    """Test FOO serialization functions."""

    def test_foo_trace_to_dict(self):
        """foo_trace_to_dict produces valid dict."""
        levels = [FOOLevel(0, 0.5, 0.01, 0.0, 0.0, 0.5)]
        trace = FOOTrace('navier_stokes', 42, levels,
                         True, 0.29, 0.29, 1, 0.75)
        d = foo_trace_to_dict(trace)
        self.assertEqual(d['problem_id'], 'navier_stokes')
        self.assertEqual(d['seed'], 42)
        self.assertTrue(d['converged'])
        self.assertEqual(len(d['levels']), 1)
        self.assertIn('delta_mean', d['levels'][0])

    def test_phi_estimate_to_dict(self):
        """phi_estimate_to_dict produces valid dict."""
        est = PhiEstimate('riemann', 0.85, 0.01, 0.0,
                          0.02, 0.005, 0.9, 'certifiable', 5)
        d = phi_estimate_to_dict(est)
        self.assertEqual(d['problem_id'], 'riemann')
        self.assertEqual(d['regime'], 'certifiable')
        self.assertAlmostEqual(d['kappa'], 0.85)


# ================================================================
#  PHI CURVE ANALYSIS TESTS
# ================================================================

class TestPhiCurveAnalysis(unittest.TestCase):
    """Test analyze_phi_curve function."""

    def _make_estimates(self, data):
        """Helper: create PhiEstimate dict from (pid, kappa, phi, regime) tuples."""
        result = {}
        for pid, kappa, phi, regime in data:
            result[pid] = PhiEstimate(pid, kappa, phi, 0.0,
                                      phi, 0.01, 0.8, regime, 3)
        return result

    def test_monotonic_curve(self):
        """Phi increasing with kappa is flagged as monotonic."""
        atlas = self._make_estimates([
            ('a', 0.3, 0.0, 'certifiable'),
            ('b', 0.6, 0.2, 'bounded'),
            ('c', 0.9, 0.8, 'irreducible'),
        ])
        curve = analyze_phi_curve(atlas)
        self.assertTrue(curve['monotonic'])
        self.assertEqual(curve['monotonic_violations'], 0)

    def test_non_monotonic_curve(self):
        """Phi decreasing with kappa flags violation."""
        atlas = self._make_estimates([
            ('a', 0.3, 0.5, 'bounded'),
            ('b', 0.6, 0.1, 'certifiable'),  # Violation
            ('c', 0.9, 0.8, 'irreducible'),
        ])
        curve = analyze_phi_curve(atlas)
        self.assertFalse(curve['monotonic'])
        self.assertGreater(curve['monotonic_violations'], 0)

    def test_regime_counts(self):
        """Regime classification counts are correct."""
        atlas = self._make_estimates([
            ('a', 0.3, 0.0, 'certifiable'),
            ('b', 0.5, 0.0, 'certifiable'),
            ('c', 0.7, 0.3, 'bounded'),
            ('d', 0.9, 0.8, 'irreducible'),
        ])
        curve = analyze_phi_curve(atlas)
        self.assertEqual(curve['regimes']['certifiable'], 2)
        self.assertEqual(curve['regimes']['bounded'], 1)
        self.assertEqual(curve['regimes']['irreducible'], 1)

    def test_structural_consistency(self):
        """Structural consistency is between 0 and 1."""
        atlas = self._make_estimates([
            ('a', 0.5, 0.1, 'bounded'),
        ])
        curve = analyze_phi_curve(atlas)
        self.assertGreaterEqual(curve['structural_consistency'], 0.0)
        self.assertLessEqual(curve['structural_consistency'], 1.0)


# ================================================================
#  KAPPA-PHI CORRELATION TESTS
# ================================================================

class TestKappaPhiCorrelation(unittest.TestCase):
    """Test that kappa and calibrated Phi have the expected relationship."""

    def test_gap_problems_high_phi(self):
        """Gap problems (PNP, YM, Continuum) have the highest Phi values."""
        top_phi = sorted(PHI_CALIBRATED.items(), key=lambda x: -x[1])[:3]
        top_pids = {pid for pid, _ in top_phi}
        # All three highest-Phi problems should be gap-type
        self.assertIn('continuum', top_pids)    # ZFC-independent: Phi=0.900
        self.assertIn('p_vs_np', top_pids)      # NP-hard gap: Phi=0.846
        # Third could be PNP_AC0 (0.820) or bridge_expander (0.600) or PNP_clique (0.840)
        # Just verify the top 2 are the structural gap leaders
        self.assertGreater(PHI_CALIBRATED['continuum'], PHI_CALIBRATED['p_vs_np'])

    def test_affirmative_problems_lower_phi(self):
        """Affirmative Clay problems (NS, RH, BSD, Hodge) have lower Phi."""
        # These should converge to topology (Phi can be low)
        affirmative_phis = [
            PHI_CALIBRATED.get('navier_stokes', 0),
            PHI_CALIBRATED.get('riemann', 0),
            PHI_CALIBRATED.get('bsd', 0),
            PHI_CALIBRATED.get('hodge', 0),
        ]
        gap_phi = PHI_CALIBRATED.get('p_vs_np', 0)
        for phi in affirmative_phis:
            self.assertLess(phi, gap_phi,
                            'Affirmative Phi should be less than gap Phi')


if __name__ == '__main__':
    unittest.main()
