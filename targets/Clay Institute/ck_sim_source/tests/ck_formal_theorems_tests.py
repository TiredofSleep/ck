"""
Tests for ck_formal_theorems.py -- Formal Theorem Library
==========================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_formal_theorems import (
    FormalTheorem, LemmaDependency, TheoremLibrary,
    build_theorem_library, verify_theorem, dependency_order,
    theorem_library_report,
)


class TestFormalTheorem(unittest.TestCase):
    """Test FormalTheorem dataclass."""

    def test_basic_construction(self):
        thm = FormalTheorem(
            theorem_id='test',
            name='Test Theorem',
            problem_id='universal',
            statement='A = B',
        )
        self.assertEqual(thm.theorem_id, 'test')
        self.assertEqual(thm.status, 'open')
        self.assertEqual(thm.confidence, 0.0)

    def test_default_fields(self):
        thm = FormalTheorem(
            theorem_id='t', name='T', problem_id='x', statement='s')
        self.assertIsInstance(thm.hypotheses, list)
        self.assertIsInstance(thm.falsifiable_predictions, list)
        self.assertIsInstance(thm.measurement_evidence, dict)


class TestLemmaDependency(unittest.TestCase):
    """Test LemmaDependency dataclass."""

    def test_construction(self):
        dep = LemmaDependency(
            from_theorem='bandwidth',
            to_theorem='frame_window',
            dependency_type='implies',
            explanation='test',
        )
        self.assertEqual(dep.from_theorem, 'bandwidth')
        self.assertEqual(dep.dependency_type, 'implies')


class TestBuildTheoremLibrary(unittest.TestCase):
    """Test static library construction."""

    def setUp(self):
        self.lib = build_theorem_library()

    def test_twelve_theorems(self):
        self.assertEqual(len(self.lib.theorems), 12)

    def test_expected_theorem_ids(self):
        expected = {
            'bandwidth', 'frame_window',
            'ns_coercivity', 'ns_regularity',
            'rh_symmetry', 'pnp_separation',
            'ym_mass_gap', 'bsd_rank', 'hodge_algebraicity',
            'duality', 'scaling', 'universality',
        }
        self.assertEqual(set(self.lib.theorems.keys()), expected)

    def test_all_have_statements(self):
        for tid, thm in self.lib.theorems.items():
            self.assertGreater(len(thm.statement), 0,
                               f'{tid} has empty statement')

    def test_all_have_predictions(self):
        for tid, thm in self.lib.theorems.items():
            self.assertGreater(len(thm.falsifiable_predictions), 0,
                               f'{tid} has no predictions')

    def test_all_have_problem_id(self):
        for tid, thm in self.lib.theorems.items():
            self.assertGreater(len(thm.problem_id), 0,
                               f'{tid} has no problem_id')

    def test_all_start_open(self):
        for tid, thm in self.lib.theorems.items():
            self.assertEqual(thm.status, 'open',
                             f'{tid} should start as open')

    def test_n_open_is_twelve(self):
        self.assertEqual(self.lib.n_open, 12)

    def test_has_dependencies(self):
        self.assertGreater(len(self.lib.dependencies), 0)

    def test_has_timestamp(self):
        self.assertGreater(len(self.lib.build_timestamp), 0)


class TestDependencyGraph(unittest.TestCase):
    """Test the dependency graph structure."""

    def setUp(self):
        self.lib = build_theorem_library()

    def test_all_dependencies_reference_valid_theorems(self):
        theorem_ids = set(self.lib.theorems.keys())
        for dep in self.lib.dependencies:
            self.assertIn(dep.from_theorem, theorem_ids,
                          f'{dep.from_theorem} not in theorems')
            self.assertIn(dep.to_theorem, theorem_ids,
                          f'{dep.to_theorem} not in theorems')

    def test_dependency_types_valid(self):
        valid_types = {'requires', 'implies', 'strengthens'}
        for dep in self.lib.dependencies:
            self.assertIn(dep.dependency_type, valid_types)

    def test_bandwidth_has_outgoing_edges(self):
        """Bandwidth is the root -- should have outgoing edges."""
        outgoing = [d for d in self.lib.dependencies
                    if d.from_theorem == 'bandwidth']
        self.assertGreater(len(outgoing), 0)

    def test_universality_has_incoming_edges(self):
        """Universality is the capstone -- should have incoming edges."""
        incoming = [d for d in self.lib.dependencies
                    if d.to_theorem == 'universality']
        self.assertGreater(len(incoming), 0)

    def test_frame_window_depends_on_bandwidth(self):
        deps = [d for d in self.lib.dependencies
                if d.from_theorem == 'bandwidth'
                and d.to_theorem == 'frame_window']
        self.assertEqual(len(deps), 1)


class TestDependencyOrder(unittest.TestCase):
    """Test topological sort of dependency graph."""

    def setUp(self):
        self.lib = build_theorem_library()
        self.order = dependency_order(self.lib)

    def test_all_theorems_in_order(self):
        self.assertEqual(set(self.order), set(self.lib.theorems.keys()))

    def test_bandwidth_before_frame_window(self):
        bw_idx = self.order.index('bandwidth')
        fw_idx = self.order.index('frame_window')
        self.assertLess(bw_idx, fw_idx)

    def test_frame_window_before_ns_coercivity(self):
        fw_idx = self.order.index('frame_window')
        ns_idx = self.order.index('ns_coercivity')
        self.assertLess(fw_idx, ns_idx)

    def test_universality_is_last_or_near_last(self):
        """Universality depends on most others, should be near end."""
        uni_idx = self.order.index('universality')
        self.assertGreater(uni_idx, len(self.order) // 2)


class TestVerifyTheorem(unittest.TestCase):
    """Test verifying individual theorems (quick mode)."""

    def test_verify_bandwidth(self):
        thm = verify_theorem('bandwidth', n_seeds=2, n_levels=6)
        self.assertIsInstance(thm, FormalTheorem)
        self.assertIn(thm.status, ['supported', 'open'])
        self.assertGreater(thm.confidence, 0.0)

    def test_verify_duality(self):
        thm = verify_theorem('duality', n_seeds=1, n_levels=6)
        self.assertEqual(thm.status, 'supported')
        self.assertEqual(thm.confidence, 1.0)
        # Duality is algebraic (73 vs 28), always passes
        ev = thm.measurement_evidence
        self.assertEqual(ev['tsml_harmony'], 73)
        self.assertEqual(ev['bhml_harmony'], 28)

    def test_verify_unknown_raises(self):
        with self.assertRaises(ValueError):
            verify_theorem('nonexistent')


class TestTheoremLibraryReport(unittest.TestCase):
    """Test the report formatter."""

    def test_report_contains_key_sections(self):
        lib = build_theorem_library()
        report = theorem_library_report(lib)
        self.assertIn('FORMAL THEOREM LIBRARY', report)
        self.assertIn('SUMMARY', report)
        self.assertIn('THEOREMS', report)
        self.assertIn('DEPENDENCY GRAPH', report)
        self.assertIn('Bandwidth', report)
        self.assertIn('CK measures', report)

    def test_report_is_string(self):
        lib = build_theorem_library()
        report = theorem_library_report(lib)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 200)


if __name__ == '__main__':
    unittest.main()
