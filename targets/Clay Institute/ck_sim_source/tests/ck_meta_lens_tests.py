"""
ck_meta_lens_tests.py -- Tests for Meta-Lens Architecture
===========================================================
Tests TopologyLens, Russell Codec, SSA Engine, SIGA Classifier, RATE Engine,
and full meta-lens atlas integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import unittest

from ck_sim.being.ck_sdv_safety import clamp, safe_div
from ck_sim.being.ck_tig_bundle import (
    CLAY_PROBLEMS, ALL_PROBLEMS, DUAL_LENSES, TOPOLOGY_SHEET, RUSSELL_CONFIG,
)
from ck_sim.doing.ck_spectrometer import CALIBRATION_CASES, FRONTIER_CASES


# ================================================================
#  HELPER: Generate raw readings for each Clay codec
# ================================================================

def make_ns_raw(**overrides):
    """Create a valid Navier-Stokes raw reading."""
    raw = {
        'omega_mag': 0.5, 'omega_max': 1.0,
        'strain_alignment': 0.8, 'scale_epsilon': 0.3,
        'energy_dissipation': 0.4, 'diss_max': 1.0,
        'omega_gradient': 0.2, 'grad_max': 1.0,
        'energy': 0.6,
    }
    raw.update(overrides)
    return raw


def make_pnp_raw(**overrides):
    """Create a valid P vs NP raw reading."""
    raw = {
        'n_variables': 100, 'n_clauses': 430,
        'clause_ratio': 4.3, 'overlap_fraction': 0.7,
        'phantom_entropy': 0.6,
        'local_state_count': 50, 'global_state_count': 100,
        'tv_distance': 0.65, 'watched_literal_reach': 0.4,
        'propagation_depth': 5, 'max_prop_depth': 20,
    }
    raw.update(overrides)
    return raw


def make_rh_raw(**overrides):
    """Create a valid Riemann Hypothesis raw reading."""
    raw = {
        'sigma': 0.5, 'z_phase': 0.01,
        'prime_sum_value': 0.5, 'zero_sum_value': 0.49,
        'N_terms': 100, 'zero_count': 50,
        'S_function_value': 0.02,
    }
    raw.update(overrides)
    return raw


def make_ym_raw(**overrides):
    """Create a valid Yang-Mills raw reading."""
    raw = {
        'vacuum_energy': 0.0, 'excited_energy': 1.0,
        'coupling_constant': 0.8,
        'reflection_positivity': 1.0,
        'correlation_length': 0.5,
        'beta': 1.0,
    }
    raw.update(overrides)
    return raw


def make_bsd_raw(**overrides):
    """Create a valid BSD raw reading."""
    raw = {
        'algebraic_rank': 1, 'analytic_rank': 1,
        'l_value_at_1': 0.0, 'l_derivative_at_1': 0.31,
        'height_matrix_det': 0.31,
        'conductor': 37, 'torsion_order': 1,
    }
    raw.update(overrides)
    return raw


def make_hodge_raw(**overrides):
    """Create a valid Hodge raw reading."""
    raw = {
        'motivic_defect': 0.05,
        'absolute_hodge_value': 0.95,
        'p_level': 1, 'variety_dimension': 4,
        'betti_rank': 10, 'algebraic_rank': 9,
        'tate_twist_value': 0.93,
    }
    raw.update(overrides)
    return raw


RAW_MAKERS = {
    'navier_stokes': make_ns_raw,
    'p_vs_np': make_pnp_raw,
    'riemann': make_rh_raw,
    'yang_mills': make_ym_raw,
    'bsd': make_bsd_raw,
    'hodge': make_hodge_raw,
}


# ================================================================
#  TEST: TopologyLens
# ================================================================

class TestTopologyLens(unittest.TestCase):
    """TopologyLens base class and subclasses produce valid output."""

    def test_base_class_interface(self):
        """TopologyLens has required methods."""
        from ck_sim.being.ck_topology_lens import TopologyLens
        for method in ['compute_core', 'compute_boundary', 'compute_flow',
                       'compute_defect', 'standardized_output']:
            self.assertTrue(hasattr(TopologyLens, method))

    def test_create_topology_lens_clay(self):
        """create_topology_lens returns specialized lens for each Clay problem."""
        from ck_sim.being.ck_topology_lens import create_topology_lens
        from ck_sim.being.ck_clay_codecs import create_codec

        for pid in CLAY_PROBLEMS:
            codec = create_codec(pid)
            lens = create_topology_lens(pid, codec)
            self.assertIsNotNone(lens)
            self.assertEqual(lens.problem_id, pid)

    def test_create_topology_lens_neighbor(self):
        """Neighbors get their parent's specialized lens."""
        from ck_sim.being.ck_topology_lens import (
            create_topology_lens, NEIGHBOR_TOPOLOGY_PARENT, TOPOLOGY_LENS_CLASSES
        )
        from ck_sim.being.ck_clay_codecs import create_codec

        for nid, parent in NEIGHBOR_TOPOLOGY_PARENT.items():
            codec = create_codec(nid)
            lens = create_topology_lens(nid, codec)
            # Should be same class as parent
            expected_cls = TOPOLOGY_LENS_CLASSES[parent]
            self.assertIsInstance(lens, expected_cls)

    def test_create_topology_lens_generic(self):
        """Standalone/bridge problems get Generic lens."""
        from ck_sim.being.ck_topology_lens import create_topology_lens, TopologyLens_Generic
        from ck_sim.being.ck_clay_codecs import create_codec

        for pid in ['collatz', 'abc', 'bridge_rmt']:
            codec = create_codec(pid)
            lens = create_topology_lens(pid, codec)
            self.assertIsInstance(lens, TopologyLens_Generic)


class TestTopologyLensOutput(unittest.TestCase):
    """Standardized output format is valid for all 6 Clay problems."""

    def _test_output(self, pid):
        from ck_sim.being.ck_topology_lens import create_topology_lens
        from ck_sim.being.ck_clay_codecs import create_codec

        codec = create_codec(pid)
        lens = create_topology_lens(pid, codec)
        raw = RAW_MAKERS[pid]()
        output = lens.standardized_output(raw)

        # Required keys
        self.assertIn('problem_id', output)
        self.assertIn('core', output)
        self.assertIn('boundary', output)
        self.assertIn('flow', output)
        self.assertIn('defect', output)
        self.assertIn('tig_class', output)

        # Core/boundary structure
        self.assertIn('label', output['core'])
        self.assertIn('features', output['core'])
        self.assertIn('magnitude', output['core'])
        self.assertIn('label', output['boundary'])
        self.assertIn('features', output['boundary'])

        # Flow structure
        self.assertIn('difference_magnitude', output['flow'])
        self.assertIn('direction', output['flow'])
        self.assertIn('alignment', output['flow'])

        # Defect is float in [0, 1]
        self.assertIsInstance(output['defect'], float)
        self.assertGreaterEqual(output['defect'], 0.0)
        self.assertLessEqual(output['defect'], 1.0)

        return output

    def test_ns_output(self):
        out = self._test_output('navier_stokes')
        self.assertEqual(out['core']['label'], 'vorticity_axis')
        self.assertIn('vortex_alignment', out['flow'])

    def test_pnp_output(self):
        out = self._test_output('p_vs_np')
        self.assertEqual(out['core']['label'], 'clause_variable_graph')
        self.assertIn('phantom_count', out['flow'])

    def test_rh_output(self):
        out = self._test_output('riemann')
        self.assertEqual(out['core']['label'], 'critical_line')
        self.assertIn('zero_deviation', out['flow'])

    def test_ym_output(self):
        out = self._test_output('yang_mills')
        self.assertIn('gap_ratio', out['flow'])

    def test_bsd_output(self):
        out = self._test_output('bsd')
        self.assertIn('rank_match', out['flow'])

    def test_hodge_output(self):
        out = self._test_output('hodge')
        self.assertIn('reachability', out['flow'])


# ================================================================
#  TEST: Russell Codec
# ================================================================

class TestRussellCodec(unittest.TestCase):
    """Russell 6D toroidal coordinates and delta_R."""

    def setUp(self):
        from ck_sim.being.ck_russell_codec import RussellCodec
        self.rc = RussellCodec()

    def _make_topo(self, pid):
        from ck_sim.being.ck_topology_lens import create_topology_lens
        from ck_sim.being.ck_clay_codecs import create_codec
        codec = create_codec(pid)
        lens = create_topology_lens(pid, codec)
        raw = RAW_MAKERS[pid]()
        return lens.standardized_output(raw)

    def test_coords_keys(self):
        """Russell coords have all 6 dimensions."""
        topo = self._make_topo('navier_stokes')
        coords = self.rc.compute_russell_coords(topo)
        for key in ['divergence', 'curl', 'helicity',
                     'axial_contrast', 'imbalance', 'void_proximity']:
            self.assertIn(key, coords)

    def test_coords_bounded(self):
        """All Russell coords are bounded."""
        for pid in CLAY_PROBLEMS:
            topo = self._make_topo(pid)
            coords = self.rc.compute_russell_coords(topo)
            for key, val in coords.items():
                self.assertGreaterEqual(val, -1.0, f'{pid}.{key} too low')
                self.assertLessEqual(val, 1.0, f'{pid}.{key} too high')

    def test_delta_russell_bounded(self):
        """delta_R is in [0, 1] for all Clay problems."""
        for pid in CLAY_PROBLEMS:
            topo = self._make_topo(pid)
            coords = self.rc.compute_russell_coords(topo)
            dr = self.rc.delta_russell(coords)
            self.assertGreaterEqual(dr, 0.0)
            self.assertLessEqual(dr, 1.0)

    def test_full_analysis_keys(self):
        """full_analysis returns all required keys."""
        topo = self._make_topo('riemann')
        result = self.rc.full_analysis(topo)
        for key in ['problem_id', 'coords', 'coords_vector', 'delta_russell',
                     'delta_standard', 'classification', 'tig_signature']:
            self.assertIn(key, result)

    def test_classification_values(self):
        """Classification is one of primary/derived/redundant."""
        for pid in CLAY_PROBLEMS:
            topo = self._make_topo(pid)
            result = self.rc.full_analysis(topo)
            self.assertIn(result['classification'],
                          ['primary', 'derived', 'redundant'])

    def test_coords_to_vector(self):
        """coords_to_vector returns 6-element list."""
        topo = self._make_topo('yang_mills')
        coords = self.rc.compute_russell_coords(topo)
        vec = self.rc.coords_to_vector(coords)
        self.assertEqual(len(vec), 6)

    def test_tig_signature_nonempty(self):
        """TIG signature is always non-empty."""
        for pid in CLAY_PROBLEMS:
            topo = self._make_topo(pid)
            coords = self.rc.compute_russell_coords(topo)
            sig = self.rc.russell_tig_signature(coords)
            self.assertGreater(len(sig), 0)


class TestRussellCorrelation(unittest.TestCase):
    """Russell-standard correlation helper."""

    def test_correlation_constant(self):
        """Constant sequences have zero correlation."""
        from ck_sim.being.ck_russell_codec import compute_russell_correlation
        corr = compute_russell_correlation([0.5, 0.5, 0.5], [0.1, 0.2, 0.3])
        self.assertAlmostEqual(corr, 0.0, places=5)

    def test_correlation_perfect(self):
        """Identical sequences have correlation 1.0."""
        from ck_sim.being.ck_russell_codec import compute_russell_correlation
        corr = compute_russell_correlation([0.1, 0.5, 0.9], [0.1, 0.5, 0.9])
        self.assertAlmostEqual(corr, 1.0, places=5)

    def test_correlation_short_sequence(self):
        """Too-short sequences return 0.0."""
        from ck_sim.being.ck_russell_codec import compute_russell_correlation
        corr = compute_russell_correlation([0.5], [0.5])
        self.assertEqual(corr, 0.0)


# ================================================================
#  TEST: SSA Engine
# ================================================================

class TestSSAEngine(unittest.TestCase):
    """SSA trilemma testing."""

    def setUp(self):
        from ck_sim.doing.ck_ssa_engine import SSAEngine
        self.engine = SSAEngine(None)  # No spectrometer needed for direct tests

    def test_c1_all_zero(self):
        """C1 holds when all deltas are near zero."""
        result = self.engine.test_c1_coherence('test', [0.001, 0.005, 0.003])
        self.assertTrue(result.holds)

    def test_c1_nonzero(self):
        """C1 breaks when deltas are significantly nonzero."""
        result = self.engine.test_c1_coherence('test', [0.5, 0.6, 0.4])
        self.assertFalse(result.holds)

    def test_c2_consistent(self):
        """C2 holds when classification is consistent."""
        # All should classify as 'gap'
        result = self.engine.test_c2_completeness('test', [0.8, 0.9, 0.7, 0.85])
        self.assertTrue(result.holds)
        self.assertEqual(result.majority_class, 'gap')

    def test_c2_inconsistent(self):
        """C2 breaks when classification flips."""
        # Mix of near-zero and high deltas
        result = self.engine.test_c2_completeness('test', [0.001, 0.8, 0.002, 0.9])
        self.assertFalse(result.holds)

    def test_c3_smooth(self):
        """C3 holds when delta trace is smooth."""
        traces = [[0.5, 0.48, 0.46, 0.45, 0.44]]
        result = self.engine.test_c3_singularity('test', traces)
        self.assertTrue(result.holds)

    def test_c3_divergent(self):
        """C3 breaks when delta trace diverges."""
        traces = [[0.1, 0.9, 0.1, 0.9, 0.1]]  # Wild oscillation
        result = self.engine.test_c3_singularity('test', traces)
        self.assertFalse(result.holds)

    def test_trilemma_affirmative(self):
        """Affirmative-type problem: C1 breaks (nonzero delta), C2+C3 hold."""
        deltas = [0.15, 0.12, 0.14, 0.13, 0.11, 0.12, 0.13, 0.14, 0.12, 0.13]
        tr = self.engine.trilemma('test_aff', deltas)
        self.assertFalse(tr.c1.holds)  # C1 breaks (deltas nonzero)
        self.assertTrue(tr.c2.holds)   # C2 holds (consistent classification)

    def test_trilemma_gap(self):
        """Gap-type problem: C1 breaks, C2 holds, C3 may break."""
        deltas = [0.9, 0.95, 0.88, 0.92, 0.91, 0.9, 0.93, 0.89, 0.91, 0.9]
        tr = self.engine.trilemma('test_gap', deltas)
        self.assertFalse(tr.c1.holds)  # C1 breaks
        self.assertTrue(tr.c2.holds)   # C2 holds (all classify as gap)


# ================================================================
#  TEST: SIGA Classifier
# ================================================================

class TestSIGAClassifier(unittest.TestCase):
    """SIGA geometry/topology classification."""

    def setUp(self):
        from ck_sim.doing.ck_ssa_engine import SIGAClassifier
        self.siga = SIGAClassifier()

    def test_complete_gluing(self):
        """Low delta -> complete gluing, restored topology."""
        result = self.siga.classify('navier_stokes', {}, 0.01)
        self.assertEqual(result['gluing_status'], 'complete')
        self.assertEqual(result['topology_status'], 'restored')

    def test_partial_gluing(self):
        """Medium delta -> partial gluing, emerging topology."""
        result = self.siga.classify('riemann', {}, 0.15)
        self.assertEqual(result['gluing_status'], 'partial')
        self.assertEqual(result['topology_status'], 'emerging')

    def test_broken_gluing(self):
        """High delta -> broken gluing, absent topology."""
        result = self.siga.classify('p_vs_np', {}, 0.65)
        self.assertEqual(result['gluing_status'], 'broken')
        self.assertEqual(result['topology_status'], 'absent')

    def test_domain_info(self):
        """Clay problems have domain-specific info."""
        for pid in CLAY_PROBLEMS:
            result = self.siga.classify(pid, {}, 0.1)
            self.assertNotEqual(result['geometry_base'], 'unknown')
            self.assertNotEqual(result['coherence_operator'], 'unknown')


# ================================================================
#  TEST: RATE Engine (unit-level, no spectrometer dependency)
# ================================================================

class TestRATEEngine(unittest.TestCase):
    """RATE engine data structures and helpers."""

    def test_rate_step_creation(self):
        """RATEStep stores values correctly."""
        from ck_sim.doing.ck_rate_engine import RATEStep
        step = RATEStep(depth=6, delta=0.3, delta_change=0.05, sensitivity=0.65)
        self.assertEqual(step.depth, 6)
        self.assertAlmostEqual(step.delta, 0.3)

    def test_rate_trace_creation(self):
        """RATETrace stores converged state."""
        from ck_sim.doing.ck_rate_engine import RATETrace, RATEStep
        steps = [RATEStep(3, 0.5, 0.1, 0.75), RATEStep(6, 0.45, 0.05, 0.73)]
        trace = RATETrace('test', 42, steps, True, 0.45, 6, True, 0.05)
        self.assertTrue(trace.converged)
        self.assertTrue(trace.topology_emerged)
        self.assertEqual(trace.convergence_depth, 6)

    def test_rate_fixed_point_stability(self):
        """RATEFixedPoint classifies stability."""
        from ck_sim.doing.ck_rate_engine import RATEFixedPoint
        fp = RATEFixedPoint('test', 0.1, 0.005, 'frozen', 1.0, 10, 10)
        self.assertEqual(fp.stability, 'frozen')
        self.assertAlmostEqual(fp.convergence_rate, 1.0)

    def test_trace_to_dict(self):
        """trace_to_dict produces valid JSON-serializable output."""
        from ck_sim.doing.ck_rate_engine import RATEEngine, RATETrace, RATEStep
        steps = [RATEStep(3, 0.5, 0.1, 0.75)]
        trace = RATETrace('test', 42, steps, False, 0.5, 24, False, 0.1)
        engine = RATEEngine(None)
        d = engine.trace_to_dict(trace)
        self.assertEqual(d['problem_id'], 'test')
        self.assertFalse(d['converged'])
        self.assertEqual(len(d['steps']), 1)


class TestRATEDefect(unittest.TestCase):
    """RATE defect convergence properties."""

    def test_converged_trace_low_defect(self):
        """Converged trace has low rate_defect."""
        from ck_sim.doing.ck_rate_engine import RATETrace, RATEStep
        steps = [
            RATEStep(3, 0.5, 0.1, 0.75),
            RATEStep(6, 0.42, 0.08, 0.71),
            RATEStep(9, 0.41, 0.01, 0.71),
            RATEStep(12, 0.405, 0.005, 0.70),
            RATEStep(15, 0.403, 0.002, 0.70),
        ]
        trace = RATETrace('test', 42, steps, True, 0.403, 15, True, 0.002)
        self.assertLess(trace.rate_defect, 0.01)

    def test_divergent_trace_high_defect(self):
        """Divergent trace has high rate_defect."""
        from ck_sim.doing.ck_rate_engine import RATETrace, RATEStep
        steps = [
            RATEStep(3, 0.5, 0.5, 0.75),
            RATEStep(6, 0.2, 0.3, 0.60),
            RATEStep(9, 0.8, 0.6, 0.90),
        ]
        trace = RATETrace('test', 42, steps, False, 0.8, 24, False, 0.6)
        self.assertGreater(trace.rate_defect, 0.1)


# ================================================================
#  TEST: Registration & Metadata
# ================================================================

class TestMetaLensRegistration(unittest.TestCase):
    """All registries and metadata are consistent."""

    def test_topology_sheet_covers_clay(self):
        """TOPOLOGY_SHEET has entries for all 6 Clay problems."""
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, TOPOLOGY_SHEET, f'{pid} missing from TOPOLOGY_SHEET')

    def test_russell_config_covers_clay(self):
        """RUSSELL_CONFIG has entries for all 6 Clay problems."""
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, RUSSELL_CONFIG, f'{pid} missing from RUSSELL_CONFIG')

    def test_topology_sheet_keys(self):
        """Each TOPOLOGY_SHEET entry has required keys."""
        for pid, entry in TOPOLOGY_SHEET.items():
            for key in ['I', '0', 'flow', 'defect_type', 'tig_class']:
                self.assertIn(key, entry, f'{pid} missing {key}')

    def test_russell_config_keys(self):
        """Each RUSSELL_CONFIG entry has operator weights."""
        for pid, entry in RUSSELL_CONFIG.items():
            for key in ['axial', 'spiral', 'void', 'sheath']:
                self.assertIn(key, entry, f'{pid} missing {key}')


# ================================================================
#  TEST: Journal Serialization
# ================================================================

class TestMetaLensJournal(unittest.TestCase):
    """Meta-lens journal serialization functions."""

    def test_topology_to_dict(self):
        from ck_sim.becoming.ck_spectrometer_journal import topology_to_dict
        topo = {
            'problem_id': 'test', 'domain': 'generic',
            'core': {'label': 'I', 'features': [0.5], 'magnitude': 0.5},
            'boundary': {'label': '0', 'features': [0.5], 'magnitude': 0.5},
            'flow': {'difference_magnitude': 0.0, 'direction': 0.0, 'alignment': 1.0},
            'defect': 0.1, 'tig_class': [7, 9],
        }
        d = topology_to_dict(topo)
        self.assertEqual(d['problem_id'], 'test')
        self.assertAlmostEqual(d['defect'], 0.1)

    def test_russell_to_dict(self):
        from ck_sim.becoming.ck_spectrometer_journal import russell_to_dict
        r = {
            'problem_id': 'test', 'coords': {'divergence': 0.1},
            'delta_russell': 0.2, 'delta_standard': 0.15,
            'delta_difference': 0.05, 'classification': 'derived',
            'tig_signature': [7, 8],
        }
        d = russell_to_dict(r)
        self.assertEqual(d['classification'], 'derived')

    def test_ssa_to_dict(self):
        from ck_sim.becoming.ck_spectrometer_journal import ssa_to_dict
        s = {
            'problem_id': 'test',
            'c1_holds': False, 'c2_holds': True, 'c3_holds': True,
            'breaking': 'C1', 'interpretation': 'Incompleteness of coherence',
        }
        d = ssa_to_dict(s)
        self.assertFalse(d['c1_holds'])
        self.assertEqual(d['breaking'], 'C1')


# ================================================================
#  LIVE OPERATIONAL TESTS -- Fire real engines through spectrometer
# ================================================================

class TestLiveSSA(unittest.TestCase):
    """Test SSA engine through the spectrometer wrapper with real deltas."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer, ProblemType
        cls.spec = DeltaSpectrometer()
        cls.ProblemType = ProblemType

    def test_ssa_analyze_ns(self):
        """SSA trilemma runs on Navier-Stokes without crashing."""
        result = self.spec.ssa_analyze(
            self.ProblemType.NAVIER_STOKES, seeds=[42, 43])
        self.assertIn('c1_holds', result)
        self.assertIn('c2_holds', result)
        self.assertIn('c3_holds', result)
        self.assertIn('breaking', result)
        # Deltas should be real values, not zeros
        deltas = result['deltas']
        self.assertTrue(len(deltas) > 0)
        self.assertTrue(any(d != 0.0 for d in deltas),
                        'All deltas are zero -- measurement channel broken')

    def test_ssa_analyze_pnp(self):
        """SSA trilemma runs on P vs NP."""
        result = self.spec.ssa_analyze(
            self.ProblemType.P_VS_NP, seeds=[42, 43])
        self.assertTrue(any(d != 0.0 for d in result['deltas']))


class TestLiveRATE(unittest.TestCase):
    """Test RATE engine through the spectrometer wrapper with real deltas."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer, ProblemType
        cls.spec = DeltaSpectrometer()
        cls.ProblemType = ProblemType

    def test_rate_scan_ns(self):
        """RATE iteration on NS produces non-zero deltas."""
        result = self.spec.rate_scan(
            self.ProblemType.NAVIER_STOKES, seed=42, max_depth=12)
        self.assertIn('converged', result)
        self.assertIn('fixed_point_delta', result)
        steps = result.get('steps', [])
        self.assertTrue(len(steps) > 0, 'No RATE steps produced')
        # At least one step should have a non-zero delta
        self.assertTrue(any(s['delta'] != 0.0 for s in steps),
                        'All RATE deltas are zero')

    def test_rate_scan_pnp(self):
        """RATE iteration on PNP produces non-zero deltas."""
        result = self.spec.rate_scan(
            self.ProblemType.P_VS_NP, seed=42, max_depth=12)
        steps = result.get('steps', [])
        self.assertTrue(any(s['delta'] != 0.0 for s in steps))

    def test_rate_depth_variation(self):
        """Different RATE depth levels produce different deltas (real feedback)."""
        result = self.spec.rate_scan(
            self.ProblemType.NAVIER_STOKES, seed=42, max_depth=12)
        steps = result.get('steps', [])
        if len(steps) >= 2:
            deltas = [s['delta'] for s in steps]
            # Not all deltas should be identical (feedback is working)
            self.assertFalse(
                all(d == deltas[0] for d in deltas),
                'All RATE deltas identical -- no depth variation')


class TestLiveFOO(unittest.TestCase):
    """Test FOO engine through the spectrometer wrapper with real deltas."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer, ProblemType
        cls.spec = DeltaSpectrometer()
        cls.ProblemType = ProblemType

    def test_foo_scan_ns(self):
        """FOO iteration on NS produces non-zero R_inf."""
        result = self.spec.foo_scan(
            self.ProblemType.NAVIER_STOKES, seed=42)
        self.assertIn('r_inf', result)
        self.assertIn('converged', result)
        self.assertNotEqual(result['r_inf'], 0.0,
                            'R_inf is zero -- FOO not reading deltas')

    def test_foo_scan_pnp(self):
        """FOO iteration on PNP produces non-zero R_inf."""
        result = self.spec.foo_scan(self.ProblemType.P_VS_NP, seed=42)
        self.assertNotEqual(result['r_inf'], 0.0)

    def test_phi_estimate_ns(self):
        """Phi estimate on NS produces real measurement."""
        result = self.spec.phi_estimate(
            self.ProblemType.NAVIER_STOKES, seeds=[42, 43])
        self.assertIn('phi_measured', result)
        self.assertIn('regime', result)
        # Phi_measured should be > 0 for NS (expected ~0.297)
        self.assertGreater(result['phi_measured'], 0.0,
                           'Phi_measured is zero -- FOO channel broken')

    def test_foo_levels_vary(self):
        """FOO levels show different deltas (meta-recursion is working)."""
        result = self.spec.foo_scan(
            self.ProblemType.NAVIER_STOKES, seed=42)
        levels = result.get('levels', [])
        if len(levels) >= 2:
            deltas = [lv['delta_mean'] for lv in levels]
            self.assertFalse(
                all(d == deltas[0] for d in deltas),
                'All FOO level deltas identical -- no meta-recursion')


class TestLiveMetaLens(unittest.TestCase):
    """Test meta_lens_atlas on a small problem set."""

    @classmethod
    def setUpClass(cls):
        from ck_sim.doing.ck_spectrometer import DeltaSpectrometer, ProblemType
        cls.spec = DeltaSpectrometer()
        cls.ProblemType = ProblemType

    def test_meta_lens_atlas_2_problems(self):
        """meta_lens_atlas runs on 2 problems without crashing."""
        result = self.spec.meta_lens_atlas(
            problem_set=['navier_stokes', 'p_vs_np'],
            seeds=[42, 43])
        self.assertIn('navier_stokes', result)
        self.assertIn('p_vs_np', result)
        # Each entry has topology + russell + ssa + siga
        ns = result['navier_stokes']
        self.assertIn('topology', ns)
        self.assertIn('russell', ns)
        self.assertIn('ssa', ns)
        self.assertIn('siga', ns)

    def test_meta_lens_ssa_has_classification(self):
        """meta_lens_atlas SSA produces real classification."""
        result = self.spec.meta_lens_atlas(
            problem_set=['navier_stokes'], seeds=[42, 43])
        ssa = result['navier_stokes']['ssa']
        # breaking should be a real classification, not empty
        self.assertIn(ssa['breaking'], ['C1', 'C2', 'C3', 'C1+C3', 'none'],
                      'SSA breaking not a valid classification')
        self.assertTrue(len(ssa['interpretation']) > 0,
                        'SSA interpretation empty')

    def test_meta_lens_expansion_problem(self):
        """meta_lens_atlas handles expansion problems."""
        result = self.spec.meta_lens_atlas(
            problem_set=['collatz'], seeds=[42])
        self.assertIn('collatz', result)
        coll = result['collatz']
        self.assertIn('siga', coll)
        # SIGA should have real domain info, not 'unknown'
        self.assertNotEqual(coll['siga']['geometry_base'], 'unknown',
                            'Standalone problem has unknown SIGA domain')


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    unittest.main()
