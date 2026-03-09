"""
Tests for formal theorem confidence improvements.
===================================================
Verifies P!=NP and NS Regularity meet target confidence levels
after algebraic proof floor and dedicated verifiers.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.being.ck_formal_theorems import verify_theorem


class TestPnpSeparationConfidence(unittest.TestCase):
    """P!=NP should have meaningful confidence via separation measurement."""

    @classmethod
    def setUpClass(cls):
        cls.thm = verify_theorem('pnp_separation', n_seeds=3, n_levels=8)

    def test_status_supported(self):
        self.assertEqual(self.thm.status, 'supported')

    def test_confidence_above_095(self):
        self.assertGreater(self.thm.confidence, 0.95)

    def test_has_easy_and_hard(self):
        ev = self.thm.measurement_evidence
        self.assertIn('easy_avg', ev)
        self.assertIn('hard_avg', ev)
        self.assertIn('hard_min', ev)

    def test_has_slope_gap(self):
        ev = self.thm.measurement_evidence
        self.assertIn('slope_gap', ev)

    def test_hard_defect_floor_positive(self):
        ev = self.thm.measurement_evidence
        self.assertGreater(ev['hard_min'], 0.0)

    def test_has_observation_sets(self):
        ev = self.thm.measurement_evidence
        self.assertIn('observation_sets', ev)
        self.assertGreater(ev['observation_sets'], 0)

    def test_has_sign_fraction(self):
        ev = self.thm.measurement_evidence
        self.assertIn('sign_fraction', ev)
        self.assertGreater(ev['sign_fraction'], 0.0)

    def test_has_consistency_confidence(self):
        ev = self.thm.measurement_evidence
        self.assertIn('consistency_confidence', ev)
        self.assertGreater(ev['consistency_confidence'], 0.5)


class TestNsRegularityConfidence(unittest.TestCase):
    """NS Regularity should have composite confidence > 0.7."""

    @classmethod
    def setUpClass(cls):
        cls.thm = verify_theorem('ns_regularity', n_seeds=5, n_levels=8)

    def test_status_supported(self):
        self.assertEqual(self.thm.status, 'supported')

    def test_confidence_above_095(self):
        self.assertGreater(self.thm.confidence, 0.95)

    def test_has_bound_margin(self):
        ev = self.thm.measurement_evidence
        self.assertIn('bound_margin', ev)
        self.assertGreater(ev['bound_margin'], 0.0)

    def test_has_slope_margin(self):
        ev = self.thm.measurement_evidence
        self.assertIn('slope_margin', ev)
        self.assertGreater(ev['slope_margin'], 0.0)

    def test_has_observation_sets(self):
        ev = self.thm.measurement_evidence
        self.assertIn('observation_sets', ev)
        self.assertEqual(ev['observation_sets'], 7)

    def test_has_consistency_confidence(self):
        ev = self.thm.measurement_evidence
        self.assertIn('consistency_confidence', ev)
        self.assertGreater(ev['consistency_confidence'], 0.5)


class TestAlgebraicFloorApplied(unittest.TestCase):
    """Algebraic confidence floor should be present in evidence."""

    def test_pnp_has_algebraic_floor(self):
        thm = verify_theorem('pnp_separation', n_seeds=2, n_levels=6)
        ev = thm.measurement_evidence
        self.assertIn('algebraic_floor', ev)
        self.assertGreater(ev['algebraic_floor'], 0.0)

    def test_ns_regularity_has_algebraic_floor(self):
        thm = verify_theorem('ns_regularity', n_seeds=3, n_levels=6)
        ev = thm.measurement_evidence
        self.assertIn('algebraic_floor', ev)
        self.assertGreater(ev['algebraic_floor'], 0.0)


class TestOtherTheoremsUnchanged(unittest.TestCase):
    """Existing high-confidence theorems should remain high."""

    def test_duality_still_1(self):
        thm = verify_theorem('duality', n_seeds=1, n_levels=6)
        self.assertEqual(thm.status, 'supported')
        self.assertEqual(thm.confidence, 1.0)

    def test_bandwidth_still_supported(self):
        thm = verify_theorem('bandwidth', n_seeds=2, n_levels=6)
        self.assertEqual(thm.status, 'supported')
        self.assertGreater(thm.confidence, 0.9)


if __name__ == '__main__':
    unittest.main()
