"""
Tests for ck_clay_protocol.py -- SDV Experiment Runner.
"""

import unittest

from ck_sim.doing.ck_clay_protocol import (
    ProbeConfig, ClayProbe, ClayProtocol, ProbeResult, ProbeStepResult,
)
from ck_sim.being.ck_tig_bundle import (
    HARMONY, VOID, RESET, LATTICE, COUNTER, NUM_OPS, OP_NAMES,
    TIG_PATHS, CLAY_PROBLEMS,
)


class TestProbeConfig(unittest.TestCase):

    def test_default_config(self):
        cfg = ProbeConfig()
        self.assertEqual(cfg.problem_id, 'navier_stokes')
        self.assertEqual(cfg.seed, 42)
        self.assertEqual(cfg.n_levels, 8)
        self.assertIsNotNone(cfg.tig_path)
        self.assertEqual(cfg.tig_path, TIG_PATHS['navier_stokes'])

    def test_custom_config(self):
        cfg = ProbeConfig(problem_id='riemann', seed=123, n_levels=5)
        self.assertEqual(cfg.problem_id, 'riemann')
        self.assertEqual(cfg.seed, 123)
        self.assertEqual(cfg.n_levels, 5)
        self.assertEqual(cfg.tig_path, TIG_PATHS['riemann'])

    def test_custom_path_override(self):
        custom = [VOID, HARMONY, RESET]
        cfg = ProbeConfig(tig_path=custom)
        self.assertEqual(cfg.tig_path, custom)


class TestClayProbe(unittest.TestCase):

    def test_ns_probe_runs(self):
        """NavierStokes probe runs without error and returns structured result."""
        cfg = ProbeConfig(problem_id='navier_stokes', test_case='lamb_oseen',
                          seed=42, n_levels=6)
        probe = ClayProbe(cfg)
        result = probe.run()

        self.assertIsInstance(result, ProbeResult)
        self.assertEqual(result.problem_id, 'navier_stokes')
        self.assertEqual(result.test_case, 'lamb_oseen')
        self.assertEqual(result.seed, 42)
        self.assertEqual(len(result.steps), 6)

    def test_result_has_all_fields(self):
        """ProbeResult has all expected fields populated."""
        cfg = ProbeConfig(n_levels=4)
        result = ClayProbe(cfg).run()

        # Trajectories
        self.assertEqual(len(result.defect_trajectory), 4)
        self.assertEqual(len(result.action_trajectory), 4)
        self.assertEqual(len(result.master_lemma_defects), 4)
        self.assertEqual(len(result.lens_mismatches), 4)
        self.assertEqual(len(result.harmony_defect_series), 4)

        # Operator stats
        self.assertEqual(len(result.operator_distribution), NUM_OPS)
        self.assertGreaterEqual(result.harmony_fraction, 0.0)
        self.assertLessEqual(result.harmony_fraction, 1.0)

        # Hash
        self.assertTrue(len(result.final_hash) > 0)

        # Verdict
        self.assertIn(result.defect_trend,
                      ['decreasing', 'increasing', 'stable', 'oscillating', 'unknown'])
        self.assertIn(result.measurement_verdict,
                      ['supports_conjecture', 'supports_gap', 'inconclusive'])

    def test_step_results_valid(self):
        """Each step has valid force vectors and operators."""
        cfg = ProbeConfig(n_levels=4)
        result = ClayProbe(cfg).run()

        for step in result.steps:
            self.assertIsInstance(step, ProbeStepResult)
            self.assertEqual(len(step.force_vector), 5)
            for v in step.force_vector:
                self.assertGreaterEqual(v, 0.0)
                self.assertLessEqual(v, 1.0)
            self.assertGreaterEqual(step.operator, 0)
            self.assertLess(step.operator, NUM_OPS)
            self.assertTrue(len(step.step_hash) > 0)

    def test_all_six_problems_run(self):
        """Every Clay problem runs without error."""
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                cfg = ProbeConfig(problem_id=pid, n_levels=4, seed=42)
                result = ClayProbe(cfg).run()
                self.assertEqual(result.problem_id, pid)
                self.assertEqual(len(result.steps), 4)

    def test_problem_class_assigned(self):
        """Problem class is correctly assigned from DUAL_LENSES."""
        for pid in ['navier_stokes', 'riemann', 'bsd', 'hodge']:
            cfg = ProbeConfig(problem_id=pid, n_levels=2)
            result = ClayProbe(cfg).run()
            self.assertEqual(result.problem_class, 'affirmative',
                             f'{pid} should be affirmative')

        for pid in ['p_vs_np', 'yang_mills']:
            cfg = ProbeConfig(problem_id=pid, n_levels=2)
            result = ClayProbe(cfg).run()
            self.assertEqual(result.problem_class, 'gap',
                             f'{pid} should be gap')

    def test_sca_tracker_feeds(self):
        """SCA tracker receives operators during probe."""
        cfg = ProbeConfig(n_levels=6)
        result = ClayProbe(cfg).run()
        # Progress should be >= 0
        self.assertGreaterEqual(result.sca_progress, 0.0)
        self.assertLessEqual(result.sca_progress, 1.0)

    def test_spine_analysis(self):
        """Spine analysis produces valid fractions."""
        cfg = ProbeConfig(n_levels=6)
        result = ClayProbe(cfg).run()
        self.assertGreaterEqual(result.spine_fraction, 0.0)
        self.assertLessEqual(result.spine_fraction, 1.0)

    def test_commutator_computed(self):
        """Commutator persistence is computed."""
        cfg = ProbeConfig(n_levels=6)
        result = ClayProbe(cfg).run()
        self.assertGreaterEqual(result.commutator_persistence, 0.0)
        self.assertLessEqual(result.commutator_persistence, 1.0)

    def test_vortex_fingerprint(self):
        """Vortex fingerprint is populated for sufficient levels."""
        cfg = ProbeConfig(n_levels=6)
        result = ClayProbe(cfg).run()
        vf = result.vortex_fingerprint
        self.assertIn('winding_number', vf)
        self.assertIn('vortex_class', vf)


class TestClayProtocol(unittest.TestCase):

    def test_run_all(self):
        """Protocol runs all 6 problems."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        results = protocol.run_all()
        self.assertEqual(len(results), 6)
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, results)
            self.assertEqual(results[pid].problem_id, pid)

    def test_run_single(self):
        """Protocol runs a single problem."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        result = protocol.run_problem('riemann', test_case='known_zero')
        self.assertEqual(result.problem_id, 'riemann')
        self.assertEqual(result.test_case, 'known_zero')

    def test_cross_problem_summary(self):
        """Cross-problem summary produces valid structure."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        results = protocol.run_all()
        summary = protocol.cross_problem_summary(results)

        self.assertIn('problems', summary)
        self.assertEqual(len(summary['problems']), 6)
        self.assertIn('affirmative_results', summary)
        self.assertIn('gap_results', summary)

    def test_calibration(self):
        """Calibration probes use default (known-answer) test cases."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        results = protocol.run_calibration()
        self.assertEqual(results['navier_stokes'].test_case, 'lamb_oseen')
        self.assertEqual(results['riemann'].test_case, 'known_zero')
        self.assertEqual(results['p_vs_np'].test_case, 'easy')

    def test_frontier(self):
        """Frontier probes use open-question test cases."""
        protocol = ClayProtocol(seed=42, n_levels=4)
        results = protocol.run_frontier()
        self.assertEqual(results['navier_stokes'].test_case, 'high_strain')
        self.assertEqual(results['riemann'].test_case, 'off_line')
        self.assertEqual(results['p_vs_np'].test_case, 'hard')


if __name__ == '__main__':
    unittest.main()
