"""
Tests for ck_three_pillars.py -- Three Pillars Framework
=========================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_three_pillars import (
    PillarResult, ThreePillarsAnalyzer, PILLAR_DEFINITIONS, pillar_report,
)
from ck_sim.doing.ck_clay_protocol import ClayProbe, ProbeConfig


class TestPillarResult(unittest.TestCase):
    """Test PillarResult dataclass construction."""

    def test_default_construction(self):
        pr = PillarResult(problem_id='navier_stokes')
        self.assertEqual(pr.problem_id, 'navier_stokes')
        self.assertTrue(pr.frame_bounded)
        self.assertEqual(pr.verdict, '')

    def test_all_fields(self):
        pr = PillarResult(
            problem_id='riemann',
            duality_defect=0.5,
            scaling_exponent=-0.6,
            frame_max_defect=0.9,
            frame_bounded=True,
        )
        self.assertEqual(pr.duality_defect, 0.5)
        self.assertEqual(pr.scaling_exponent, -0.6)
        self.assertTrue(pr.frame_bounded)


class TestThreePillarsAnalyzer(unittest.TestCase):
    """Test ThreePillarsAnalyzer with real probes."""

    def setUp(self):
        self.analyzer = ThreePillarsAnalyzer()

    def _run_probe(self, problem_id, test_case, seed=42, n_levels=8):
        config = ProbeConfig(
            problem_id=problem_id,
            test_case=test_case,
            seed=seed,
            n_levels=n_levels,
        )
        probe = ClayProbe(config)
        return probe.run()

    def test_ns_lamb_oseen(self):
        """Lamb-Oseen: exact smooth solution -> regularity."""
        result = self._run_probe('navier_stokes', 'lamb_oseen')
        pr = self.analyzer.analyze(result)
        self.assertEqual(pr.problem_id, 'navier_stokes')
        self.assertTrue(pr.frame_bounded)
        self.assertGreater(len(pr.defect_by_level), 0)

    def test_ns_high_strain(self):
        """High strain: should show different character than smooth."""
        result = self._run_probe('navier_stokes', 'high_strain')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_ns_pressure_hessian(self):
        """P-H probe: defect should be bounded."""
        result = self._run_probe('navier_stokes', 'pressure_hessian')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)
        self.assertLess(pr.frame_max_defect, 1.0)

    def test_rh_known_zero(self):
        """Riemann: known zero on critical line."""
        result = self._run_probe('riemann', 'known_zero')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_pnp_easy(self):
        """P vs NP: easy SAT instance."""
        result = self._run_probe('p_vs_np', 'easy')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_ym_bpst(self):
        """Yang-Mills: BPST instanton."""
        result = self._run_probe('yang_mills', 'bpst_instanton')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_bsd_rank0(self):
        """BSD: rank 0 match."""
        result = self._run_probe('bsd', 'rank0_match')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_hodge_algebraic(self):
        """Hodge: known algebraic class."""
        result = self._run_probe('hodge', 'algebraic')
        pr = self.analyzer.analyze(result)
        self.assertTrue(pr.frame_bounded)

    def test_pillar_scores_exist(self):
        """Pillar scores dict must have all 3 keys."""
        result = self._run_probe('navier_stokes', 'lamb_oseen')
        pr = self.analyzer.analyze(result)
        self.assertIn('duality', pr.pillar_scores)
        self.assertIn('fractal_richness', pr.pillar_scores)
        self.assertIn('frame_window', pr.pillar_scores)

    def test_cross_problem(self):
        """Cross-problem comparison must produce valid output."""
        problems = {
            'navier_stokes': ('lamb_oseen',),
            'riemann': ('known_zero',),
            'p_vs_np': ('hard',),
        }
        pillar_results = {}
        for pid, (tc,) in problems.items():
            result = self._run_probe(pid, tc)
            pillar_results[pid] = self.analyzer.analyze(result)

        cross = self.analyzer.cross_problem(pillar_results)
        self.assertIn('verdicts', cross)
        self.assertIn('pillar_scores', cross)


class TestPillarDefinitions(unittest.TestCase):
    """Test PILLAR_DEFINITIONS constant."""

    def test_all_three_pillars_defined(self):
        self.assertIn('duality', PILLAR_DEFINITIONS)
        self.assertIn('fractal_richness', PILLAR_DEFINITIONS)
        self.assertIn('frame_window', PILLAR_DEFINITIONS)

    def test_all_six_problems_in_each_pillar(self):
        problems = ['navier_stokes', 'riemann', 'p_vs_np',
                     'yang_mills', 'bsd', 'hodge']
        for pillar_name, pillar in PILLAR_DEFINITIONS.items():
            per_problem = pillar.get('per_problem', {})
            for p in problems:
                self.assertIn(p, per_problem,
                              f'{p} missing from {pillar_name}')


class TestPillarReport(unittest.TestCase):
    """Test report formatting."""

    def test_report_format(self):
        pr = PillarResult(
            problem_id='navier_stokes',
            duality_defect=0.3,
            frame_max_defect=0.8,
            frame_bounded=True,
            verdict='regularity',
            pillar_scores={'duality': 0.7, 'fractal_richness': 0.6, 'frame_window': 0.2},
        )
        text = pillar_report(pr)
        self.assertIn('THREE PILLARS', text)
        self.assertIn('DUALITY', text)
        self.assertIn('FRACTAL', text)
        self.assertIn('FRAME', text)
        self.assertIn('CK measures', text)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""

    def test_linear_slope_increasing(self):
        slope = ThreePillarsAnalyzer._linear_slope([1, 2, 3, 4, 5])
        self.assertGreater(slope, 0.9)

    def test_linear_slope_decreasing(self):
        slope = ThreePillarsAnalyzer._linear_slope([5, 4, 3, 2, 1])
        self.assertLess(slope, -0.9)

    def test_linear_slope_flat(self):
        slope = ThreePillarsAnalyzer._linear_slope([3, 3, 3, 3])
        self.assertAlmostEqual(slope, 0.0, places=5)

    def test_digit_root(self):
        self.assertEqual(ThreePillarsAnalyzer._digit_root(9), 9)
        self.assertEqual(ThreePillarsAnalyzer._digit_root(18), 9)
        self.assertEqual(ThreePillarsAnalyzer._digit_root(3), 3)
        self.assertEqual(ThreePillarsAnalyzer._digit_root(12), 3)


if __name__ == '__main__':
    unittest.main()
