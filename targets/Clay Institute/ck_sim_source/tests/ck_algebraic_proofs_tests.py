"""
Tests for ck_algebraic_proofs.py -- Algebraic Proof Library
============================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_algebraic_proofs import (
    ProofResult,
    prove_harmony_absorber,
    prove_void_conditional_absorber,
    prove_harmony_count,
    prove_non_harmony_partition,
    prove_harmony_chain_convergence,
    prove_worst_case_non_harmony_chain,
    prove_force_defect_bound,
    prove_per_problem_ceiling,
    prove_pnp_separation_bound,
    prove_ns_regularity_bound,
    run_all_proofs,
    algebraic_proof_report,
)


class TestProofResultDataclass(unittest.TestCase):
    """Test ProofResult construction."""

    def test_default_construction(self):
        pr = ProofResult(proof_id='test', claim='Test claim')
        self.assertEqual(pr.proof_id, 'test')
        self.assertFalse(pr.verified)
        self.assertEqual(pr.confidence, 0.0)
        self.assertIsInstance(pr.proof_steps, list)
        self.assertIsInstance(pr.evidence, dict)


class TestHarmonyAbsorber(unittest.TestCase):
    """Proof 1: HARMONY is a two-sided absorber."""

    def test_verified(self):
        result = prove_harmony_absorber()
        self.assertTrue(result.verified)

    def test_confidence_1(self):
        result = prove_harmony_absorber()
        self.assertEqual(result.confidence, 1.0)

    def test_has_20_steps(self):
        result = prove_harmony_absorber()
        # 10 left checks + 10 right checks
        self.assertEqual(len(result.proof_steps), 20)

    def test_evidence_checks(self):
        result = prove_harmony_absorber()
        self.assertEqual(result.evidence['checks'], 20)
        self.assertEqual(result.evidence['passed'], 20)


class TestVoidConditionalAbsorber(unittest.TestCase):
    """Proof 2: VOID absorbs left except vs HARMONY."""

    def test_verified(self):
        result = prove_void_conditional_absorber()
        self.assertTrue(result.verified)

    def test_confidence_1(self):
        result = prove_void_conditional_absorber()
        self.assertEqual(result.confidence, 1.0)

    def test_harmony_exception(self):
        result = prove_void_conditional_absorber()
        # One of the steps should mention HARMONY wins
        harmony_step = [s for s in result.proof_steps if 'HARMONY wins' in s]
        self.assertEqual(len(harmony_step), 1)


class TestHarmonyCount(unittest.TestCase):
    """Proof 3: exactly 73 HARMONY entries."""

    def test_verified(self):
        result = prove_harmony_count()
        self.assertTrue(result.verified)

    def test_count_is_73(self):
        result = prove_harmony_count()
        self.assertEqual(result.evidence['harmony_count'], 73)

    def test_non_harmony_is_27(self):
        result = prove_harmony_count()
        self.assertEqual(result.evidence['non_harmony_count'], 27)

    def test_rate_close_to_tstar(self):
        result = prove_harmony_count()
        rate = result.evidence['rate']
        t_star = result.evidence['t_star']
        self.assertAlmostEqual(rate, 0.73)
        self.assertLess(abs(rate - t_star), 0.02)


class TestNonHarmonyPartition(unittest.TestCase):
    """Proof 4: exact non-HARMONY partition."""

    def test_verified(self):
        result = prove_non_harmony_partition()
        self.assertTrue(result.verified)

    def test_partition_exact(self):
        result = prove_non_harmony_partition()
        p = result.evidence['partition']
        self.assertEqual(p['VOID'], 17)
        self.assertEqual(p['PROGRESS'], 4)
        self.assertEqual(p['COLLAPSE'], 2)
        self.assertEqual(p['BREATH'], 2)
        self.assertEqual(p['RESET'], 2)

    def test_total_is_27(self):
        result = prove_non_harmony_partition()
        self.assertEqual(result.evidence['total'], 27)

    def test_entries_enumerate_all_27(self):
        result = prove_non_harmony_partition()
        self.assertEqual(len(result.evidence['entries']), 27)


class TestHarmonyChainConvergence(unittest.TestCase):
    """Proof 5: chains touching HARMONY stay HARMONY."""

    def test_verified(self):
        result = prove_harmony_chain_convergence()
        self.assertTrue(result.verified)

    def test_all_absorbed(self):
        result = prove_harmony_chain_convergence()
        self.assertTrue(result.evidence['all_absorbed'])

    def test_fixed_point(self):
        result = prove_harmony_chain_convergence()
        self.assertTrue(result.evidence['fixed_point'])


class TestWorstCaseChain(unittest.TestCase):
    """Proof 6: worst-case non-HARMONY chain."""

    def test_verified(self):
        result = prove_worst_case_non_harmony_chain()
        self.assertTrue(result.verified)

    def test_chain_length_bounded_by_window(self):
        result = prove_worst_case_non_harmony_chain()
        self.assertGreater(result.evidence['max_chain_length'], 0)
        self.assertLessEqual(result.evidence['max_chain_length'], 32)

    def test_void_idempotent(self):
        result = prove_worst_case_non_harmony_chain()
        self.assertTrue(result.evidence['void_is_idempotent'])

    def test_has_self_loops(self):
        result = prove_worst_case_non_harmony_chain()
        self.assertGreater(len(result.evidence['self_loops']), 0)


class TestForceDefectBound(unittest.TestCase):
    """Proof 7: safety clamp bounds defects."""

    def test_verified(self):
        result = prove_force_defect_bound()
        self.assertTrue(result.verified)

    def test_six_problems_bounded(self):
        result = prove_force_defect_bound()
        self.assertEqual(result.evidence['problems_bounded'], 6)


class TestPerProblemCeiling(unittest.TestCase):
    """Proof 8: per-problem defect ceiling."""

    def test_verified(self):
        result = prove_per_problem_ceiling()
        self.assertTrue(result.verified)

    def test_all_ceilings_at_most_1(self):
        result = prove_per_problem_ceiling()
        for pid, ceiling in result.evidence['ceilings'].items():
            self.assertLessEqual(ceiling, 1.0, '%s ceiling exceeds 1.0' % pid)


class TestPnpSeparationBound(unittest.TestCase):
    """Proof 9: P!=NP separation from first principles."""

    def test_verified(self):
        result = prove_pnp_separation_bound()
        self.assertTrue(result.verified)

    def test_confidence_gt_0(self):
        result = prove_pnp_separation_bound()
        self.assertGreater(result.confidence, 0.0)

    def test_hard_slope_positive(self):
        result = prove_pnp_separation_bound()
        self.assertGreater(result.evidence['hard_slope'], 0.0)

    def test_slope_gap_positive(self):
        result = prove_pnp_separation_bound()
        self.assertGreater(result.evidence['slope_gap'], 0.0)

    def test_hard_defect_floor_positive(self):
        result = prove_pnp_separation_bound()
        self.assertGreater(result.evidence['min_hard_defect'], 0.0)


class TestNsRegularityBound(unittest.TestCase):
    """Proof 10: NS regularity from first principles."""

    def test_verified(self):
        result = prove_ns_regularity_bound()
        self.assertTrue(result.verified)

    def test_defect_max_below_bound(self):
        result = prove_ns_regularity_bound()
        self.assertLess(result.evidence['defect_max'], 0.8)

    def test_margin_positive(self):
        result = prove_ns_regularity_bound()
        self.assertGreater(result.evidence['margin'], 0.0)


class TestRunAllProofs(unittest.TestCase):
    """Test run_all_proofs top-level function."""

    def test_returns_10_proofs(self):
        results = run_all_proofs()
        self.assertEqual(len(results), 10)

    def test_all_have_proof_id(self):
        results = run_all_proofs()
        for pid, result in results.items():
            self.assertEqual(pid, result.proof_id)

    def test_all_deterministic(self):
        """Run twice, same results."""
        r1 = run_all_proofs()
        r2 = run_all_proofs()
        for pid in r1:
            self.assertEqual(r1[pid].verified, r2[pid].verified)
            self.assertEqual(r1[pid].confidence, r2[pid].confidence)

    def test_all_verified(self):
        results = run_all_proofs()
        for pid, result in results.items():
            self.assertTrue(result.verified, '%s not verified' % pid)


class TestAlgebraicProofReport(unittest.TestCase):
    """Test report formatter."""

    def test_report_is_string(self):
        report = algebraic_proof_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 200)

    def test_report_contains_sections(self):
        report = algebraic_proof_report()
        self.assertIn('ALGEBRAIC PROOF LIBRARY', report)
        self.assertIn('PROVEN', report)
        self.assertIn('T* = 5/7', report)


if __name__ == '__main__':
    unittest.main()
