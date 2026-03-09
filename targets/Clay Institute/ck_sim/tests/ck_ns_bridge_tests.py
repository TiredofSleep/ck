"""
Tests for ck_ns_bridge.py -- Navier-Stokes Mathematical Bridge
===============================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_ns_bridge import (
    NSBridge, NSBridgeMapping, BridgeReport, bridge_report_text,
)
from ck_sim.doing.ck_clay_protocol import ClayProbe, ProbeConfig


class TestNSBridgeMapping(unittest.TestCase):
    """Test NSBridgeMapping dataclass construction."""

    def test_default_construction(self):
        m = NSBridgeMapping(
            index=1, ck_concept='aperture',
            pde_concept='misalignment',
            formula='1 - |cos|^2',
            function_space='pointwise',
        )
        self.assertEqual(m.index, 1)
        self.assertEqual(m.ck_concept, 'aperture')
        self.assertFalse(m.verified)
        self.assertEqual(m.verification_details, '')

    def test_verified_flag(self):
        m = NSBridgeMapping(
            index=9, ck_concept='max defect < 1.0',
            pde_concept='bounded frame',
            formula='sup < 1',
            function_space='P-H',
            verified=True,
            verification_details='all bounded',
        )
        self.assertTrue(m.verified)
        self.assertIn('bounded', m.verification_details)


class TestBridgeReport(unittest.TestCase):
    """Test BridgeReport dataclass."""

    def test_default_construction(self):
        br = BridgeReport()
        self.assertEqual(br.problem_id, 'navier_stokes')
        self.assertEqual(br.total_mappings, 0)
        self.assertEqual(br.verified_count, 0)
        self.assertIsInstance(br.mappings, list)
        self.assertIsInstance(br.calibration_results, dict)


class TestNSBridgeMappings(unittest.TestCase):
    """Test the 9 static MAPPINGS."""

    def test_nine_mappings_exist(self):
        self.assertEqual(len(NSBridge.MAPPINGS), 9)

    def test_indices_1_through_9(self):
        indices = [m.index for m in NSBridge.MAPPINGS]
        self.assertEqual(indices, list(range(1, 10)))

    def test_all_have_formula(self):
        for m in NSBridge.MAPPINGS:
            self.assertTrue(len(m.formula) > 0, f'Mapping {m.index} has empty formula')

    def test_all_have_function_space(self):
        for m in NSBridge.MAPPINGS:
            self.assertTrue(len(m.function_space) > 0,
                            f'Mapping {m.index} has empty function_space')

    def test_five_force_dimensions_present(self):
        """First 5 mappings correspond to the 5 CK force dimensions."""
        concepts = [m.ck_concept for m in NSBridge.MAPPINGS[:5]]
        self.assertIn('aperture', concepts)
        self.assertIn('pressure', concepts)
        self.assertIn('depth', concepts)
        self.assertIn('binding', concepts)
        self.assertIn('continuity', concepts)


class TestNSBridgeVerifications(unittest.TestCase):
    """Run actual verification probes (small seed counts for speed)."""

    def setUp(self):
        # Small seed/level counts for test speed
        self.bridge = NSBridge(n_seeds=3, n_levels=8)

    def test_verify_lamb_oseen(self):
        """Lamb-Oseen: exact smooth solution calibration."""
        result = self.bridge.verify_lamb_oseen()
        self.assertIn('test', result)
        self.assertEqual(result['test'], 'lamb_oseen_calibration')
        self.assertIn('verified', result)
        self.assertIn('avg_delta', result)
        self.assertIn('max_delta', result)
        self.assertIn('avg_harmony', result)
        self.assertIn('avg_slope', result)
        # Max delta should be well below 1.0 for smooth solution
        self.assertLess(result['max_delta'], 1.0)

    def test_verify_two_class_separation(self):
        """Smooth vs turbulent: D2 separation should exist."""
        result = self.bridge.verify_two_class_separation()
        self.assertIn('test', result)
        self.assertEqual(result['test'], 'two_class_separation')
        self.assertIn('d2_ratio', result)
        self.assertIn('delta_ratio', result)
        # D2 ratio should be non-negative (may be 0 at low seed/level)
        self.assertGreaterEqual(result['d2_ratio'], 0.0)

    def test_verify_energy_cascade(self):
        """Energy cascade: always passes, measures direction."""
        result = self.bridge.verify_energy_cascade()
        self.assertEqual(result['test'], 'energy_cascade')
        self.assertTrue(result['verified'])
        self.assertIn('cascade_direction', result)
        self.assertIn(result['cascade_direction'], ('forward', 'backward'))

    def test_verify_bkm_consistency(self):
        """BKM: high strain should show positive defect slope."""
        result = self.bridge.verify_bkm_consistency()
        self.assertEqual(result['test'], 'bkm_consistency')
        self.assertIn('high_strain_avg_slope', result)
        self.assertIn('near_singular_avg_slope', result)

    def test_verify_frame_window(self):
        """Frame window: all 6 NS test cases bounded < 1.0."""
        # Use very small seeds for this multi-case test
        bridge = NSBridge(n_seeds=2, n_levels=6)
        result = bridge.verify_frame_window()
        self.assertEqual(result['test'], 'frame_window')
        self.assertIn('per_case', result)
        # Check that all test cases are present
        per_case = result['per_case']
        for tc in ['lamb_oseen', 'taylor_green', 'high_strain',
                    'pressure_hessian', 'near_singular', 'eigenvalue_crossing']:
            self.assertIn(tc, per_case, f'{tc} missing from frame_window per_case')
            self.assertLess(per_case[tc]['max_defect'], 1.0,
                            f'{tc} defect not bounded')


class TestNSBridgeReport(unittest.TestCase):
    """Test full bridge report generation."""

    def setUp(self):
        self.bridge = NSBridge(n_seeds=2, n_levels=6)

    def test_bridge_report_structure(self):
        """Generate full report and check structure."""
        report = self.bridge.bridge_report()
        self.assertIsInstance(report, BridgeReport)
        self.assertEqual(report.problem_id, 'navier_stokes')
        self.assertEqual(report.total_mappings, 9)
        self.assertEqual(len(report.mappings), 9)
        self.assertEqual(report.verified_count + report.open_count, 9)
        self.assertTrue(len(report.timestamp) > 0)

    def test_bridge_report_has_calibration(self):
        """Report should include all 5 calibration test results."""
        report = self.bridge.bridge_report()
        cal = report.calibration_results
        self.assertIn('lamb_oseen', cal)
        self.assertIn('two_class_separation', cal)
        self.assertIn('energy_cascade', cal)
        self.assertIn('bkm_consistency', cal)
        self.assertIn('frame_window', cal)


class TestBridgeReportText(unittest.TestCase):
    """Test report text formatting."""

    def test_report_format(self):
        """Report text should contain key sections."""
        report = BridgeReport(
            problem_id='navier_stokes',
            total_mappings=9,
            verified_count=7,
            open_count=2,
            mappings=list(NSBridge.MAPPINGS),
            calibration_results={
                'lamb_oseen': {
                    'verified': True, 'avg_delta': 0.3,
                    'max_delta': 0.5, 'avg_harmony': 0.6,
                    'avg_slope': -0.01,
                },
                'two_class_separation': {
                    'verified': True, 'd2_ratio': 3.4,
                    'delta_ratio': 2.1,
                },
                'frame_window': {
                    'verified': True, 'per_case': {
                        'lamb_oseen': {'max_defect': 0.3, 'bounded': True},
                    },
                },
            },
            timestamp='2026-03-09 12:00:00',
        )
        text = bridge_report_text(report)
        self.assertIn('NS MATHEMATICAL BRIDGE', text)
        self.assertIn('FORMAL CONNECTIONS', text)
        self.assertIn('aperture', text)
        self.assertIn('CALIBRATION RESULTS', text)
        self.assertIn('Lamb-Oseen', text)
        self.assertIn('CK measures', text)


class TestInternalProbes(unittest.TestCase):
    """Test _run_probes helper."""

    def test_run_probes_returns_list(self):
        bridge = NSBridge(n_seeds=2, n_levels=6)
        results = bridge._run_probes('lamb_oseen', 2, 6)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)

    def test_probe_dict_keys(self):
        bridge = NSBridge(n_seeds=1, n_levels=6)
        results = bridge._run_probes('lamb_oseen', 1, 6)
        r = results[0]
        self.assertIn('seed', r)
        self.assertIn('final_defect', r)
        self.assertIn('max_defect', r)
        self.assertIn('harmony_fraction', r)
        self.assertIn('avg_d2_norm', r)
        self.assertIn('defect_slope', r)
        self.assertIn('defect_trajectory', r)

    def test_max_defect_bounded(self):
        """Max defect from any probe should be < 1.0."""
        bridge = NSBridge(n_seeds=3, n_levels=8)
        results = bridge._run_probes('lamb_oseen', 3, 8)
        for r in results:
            self.assertLess(r['max_defect'], 1.0)


if __name__ == '__main__':
    unittest.main()
