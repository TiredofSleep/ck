"""
Tests for ck_proof_certificate.py -- Proof-by-Measurement Certificate System
=============================================================================
(c) 2026 Brayden Sanders / 7Site LLC
"""

import unittest
from ck_sim.doing.ck_proof_certificate import (
    FormalClaim, MeasurementProtocol, ProofCertificate, CertificateChain,
    certify_claim, verify_certificate, build_chain, certificate_report,
    CLAIM_NS_COERCIVITY, CLAIM_RH_SYMMETRY, CLAIM_PNP_SEPARATION,
    CLAIM_YM_MASS_GAP, CLAIM_BSD_RANK, CLAIM_HODGE_ALGEBRAICITY,
    CLAIM_BANDWIDTH, CLAIM_FRAME_WINDOW,
    ALL_CLAIMS, PROTOCOL_NS_QUICK,
)


class TestFormalClaim(unittest.TestCase):
    """Test FormalClaim dataclass construction."""

    def test_basic_construction(self):
        claim = FormalClaim(
            name='Test Claim',
            claim_id='test',
            statement='delta < 1',
            hypotheses=['smooth data'],
            conclusion='bounded',
            problem_id='navier_stokes',
            falsifiable_predictions=['max_defect < 1.0'],
        )
        self.assertEqual(claim.name, 'Test Claim')
        self.assertEqual(claim.claim_id, 'test')
        self.assertEqual(len(claim.falsifiable_predictions), 1)

    def test_pre_built_ns_coercivity(self):
        self.assertEqual(CLAIM_NS_COERCIVITY.claim_id, 'ns_coercivity')
        self.assertEqual(CLAIM_NS_COERCIVITY.problem_id, 'navier_stokes')
        self.assertGreater(len(CLAIM_NS_COERCIVITY.statement), 0)

    def test_all_eight_claims_exist(self):
        self.assertEqual(len(ALL_CLAIMS), 8)
        expected = {'ns_coercivity', 'rh_symmetry', 'pnp_separation',
                    'ym_mass_gap', 'bsd_rank', 'hodge_algebraicity',
                    'bandwidth', 'frame_window'}
        self.assertEqual(set(ALL_CLAIMS.keys()), expected)

    def test_all_claims_have_predictions(self):
        for cid, claim in ALL_CLAIMS.items():
            self.assertGreater(len(claim.falsifiable_predictions), 0,
                               f'{cid} has no predictions')


class TestMeasurementProtocol(unittest.TestCase):
    """Test MeasurementProtocol dataclass."""

    def test_basic_construction(self):
        protocol = MeasurementProtocol(
            protocol_id='test_v1',
            n_seeds=5,
            n_levels=8,
            test_cases=['lamb_oseen'],
            falsification_thresholds={'max_defect': 1.0},
            problem_ids=['navier_stokes'],
        )
        self.assertEqual(protocol.n_seeds, 5)
        self.assertEqual(protocol.n_levels, 8)

    def test_pre_built_ns_quick(self):
        self.assertEqual(PROTOCOL_NS_QUICK.protocol_id, 'ns_quick_v1')
        self.assertGreater(len(PROTOCOL_NS_QUICK.test_cases), 0)


class TestCertifyClaim(unittest.TestCase):
    """Test certify_claim with minimal parameters."""

    @classmethod
    def setUpClass(cls):
        """Certify NS coercivity claim (quick mode)."""
        protocol = MeasurementProtocol(
            protocol_id='test_minimal',
            n_seeds=2,
            n_levels=6,
            test_cases=['lamb_oseen'],
            falsification_thresholds={'max_defect': 1.0},
            problem_ids=['navier_stokes'],
        )
        cls.cert = certify_claim(CLAIM_NS_COERCIVITY, protocol)

    def test_returns_certificate(self):
        self.assertIsInstance(self.cert, ProofCertificate)

    def test_has_certificate_id(self):
        self.assertIn('ns_coercivity', self.cert.certificate_id)

    def test_has_timestamp(self):
        self.assertGreater(len(self.cert.timestamp), 0)

    def test_has_determinism_hash(self):
        self.assertGreater(len(self.cert.determinism_hash), 0)

    def test_predictions_tested(self):
        self.assertGreater(self.cert.predictions_tested, 0)

    def test_verdict_valid(self):
        self.assertIn(self.cert.verdict,
                      ['supported', 'inconclusive', 'falsified'])

    def test_confidence_in_range(self):
        self.assertGreaterEqual(self.cert.confidence, 0.0)
        self.assertLessEqual(self.cert.confidence, 1.0)

    def test_total_probes_positive(self):
        self.assertGreater(self.cert.total_probes, 0)

    def test_probe_summaries_not_empty(self):
        self.assertGreater(len(self.cert.probe_summaries), 0)

    def test_ns_coercivity_supported(self):
        """NS coercivity with lamb_oseen should be supported."""
        self.assertEqual(self.cert.verdict, 'supported')


class TestCertificateReport(unittest.TestCase):
    """Test certificate_report formatter."""

    @classmethod
    def setUpClass(cls):
        protocol = MeasurementProtocol(
            protocol_id='test_report',
            n_seeds=1,
            n_levels=6,
            test_cases=['lamb_oseen'],
            falsification_thresholds={'max_defect': 1.0},
            problem_ids=['navier_stokes'],
        )
        cls.cert = certify_claim(CLAIM_NS_COERCIVITY, protocol)

    def test_report_contains_key_sections(self):
        report = certificate_report(self.cert)
        self.assertIn('PROOF-BY-MEASUREMENT CERTIFICATE', report)
        self.assertIn('CLAIM', report)
        self.assertIn('PROTOCOL', report)
        self.assertIn('RESULTS', report)
        self.assertIn('VERDICT', report)
        self.assertIn('CK measures', report)

    def test_report_is_string(self):
        report = certificate_report(self.cert)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)


class TestBuildChain(unittest.TestCase):
    """Test certificate chain building."""

    def test_empty_chain(self):
        chain = build_chain([], {})
        self.assertIsInstance(chain, CertificateChain)
        self.assertEqual(chain.overall_verdict, 'inconclusive')
        self.assertEqual(chain.overall_confidence, 0.0)

    def test_chain_with_one_certificate(self):
        protocol = MeasurementProtocol(
            protocol_id='chain_test',
            n_seeds=1, n_levels=6,
            test_cases=['lamb_oseen'],
            falsification_thresholds={'max_defect': 1.0},
            problem_ids=['navier_stokes'],
        )
        cert = certify_claim(CLAIM_NS_COERCIVITY, protocol)
        chain = build_chain([cert], {})
        self.assertIsInstance(chain, CertificateChain)
        self.assertEqual(len(chain.certificates), 1)


class TestDeterminism(unittest.TestCase):
    """Test that certificates are deterministic."""

    def test_same_protocol_same_hash(self):
        """Same claim + same protocol should produce same hash."""
        protocol = MeasurementProtocol(
            protocol_id='det_test',
            n_seeds=1, n_levels=6,
            test_cases=['lamb_oseen'],
            falsification_thresholds={'max_defect': 1.0},
            problem_ids=['navier_stokes'],
        )
        cert1 = certify_claim(CLAIM_NS_COERCIVITY, protocol)
        cert2 = certify_claim(CLAIM_NS_COERCIVITY, protocol)
        self.assertEqual(cert1.determinism_hash, cert2.determinism_hash)


if __name__ == '__main__':
    unittest.main()
