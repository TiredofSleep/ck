"""
Tests for ck_clay_codecs.py -- Mathematical sensory codecs for Clay SDV.
Tests for ck_tig_bundle.py -- TIG 4D operator bundle.
"""

import math
import unittest

from ck_sim.being.ck_clay_codecs import (
    NavierStokesCodec, RiemannCodec, PvsNPCodec,
    YangMillsCodec, BSDCodec, HodgeCodec,
    CLAY_CODEC_REGISTRY, create_codec,
)
from ck_sim.being.ck_tig_bundle import (
    TIG_MATRIX, TIG_PATHS, DUAL_LENSES, CLAY_PROBLEMS,
    digit_reduction, is_spine_word, spine_class,
    unfold_level, build_fractal_levels,
    SCALoopTracker, commutator_nonzero, commutator_persistence,
    NUM_OPS, VOID, LATTICE, COUNTER, HARMONY, RESET,
)
from ck_sim.being.ck_sensory_codecs import CODEC_REGISTRY, register_clay_codecs


# ================================================================
#  TIG BUNDLE TESTS
# ================================================================

class TestTIGMatrix(unittest.TestCase):

    def test_all_10_operators_present(self):
        self.assertEqual(len(TIG_MATRIX), 10)
        for i in range(10):
            self.assertIn(i, TIG_MATRIX)

    def test_each_has_4_components(self):
        for op, bundle in TIG_MATRIX.items():
            self.assertIn('D', bundle)
            self.assertIn('P', bundle)
            self.assertIn('R', bundle)
            self.assertIn('Delta', bundle)


class TestTIGPaths(unittest.TestCase):

    def test_all_6_problems_have_paths(self):
        self.assertGreaterEqual(len(TIG_PATHS), 6)
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, TIG_PATHS)

    def test_all_paths_end_at_reset(self):
        for pid, path in TIG_PATHS.items():
            self.assertEqual(path[-1], RESET,
                             f'{pid} path does not end at RESET')

    def test_clay_paths_contain_harmony(self):
        """Original 6 Clay problems all contain HARMONY."""
        for pid in CLAY_PROBLEMS:
            path = TIG_PATHS[pid]
            self.assertIn(HARMONY, path,
                          f'{pid} path missing HARMONY operator')

    def test_ns_path(self):
        self.assertEqual(TIG_PATHS['navier_stokes'], [0, 1, 2, 3, 7, 9])


class TestDualLenses(unittest.TestCase):

    def test_all_6_problems(self):
        self.assertGreaterEqual(len(DUAL_LENSES), 6)
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, DUAL_LENSES)

    def test_each_has_required_keys(self):
        for pid, lens in DUAL_LENSES.items():
            self.assertIn('lens_a', lens)
            self.assertIn('lens_b', lens)
            self.assertIn('generator', lens)
            self.assertIn('dual', lens)
            self.assertIn('problem_class', lens)

    def test_problem_classes(self):
        self.assertEqual(DUAL_LENSES['navier_stokes']['problem_class'], 'affirmative')
        self.assertEqual(DUAL_LENSES['p_vs_np']['problem_class'], 'gap')
        self.assertEqual(DUAL_LENSES['yang_mills']['problem_class'], 'gap')


class TestDigitReduction(unittest.TestCase):

    def test_single_digits(self):
        self.assertEqual(digit_reduction([3]), 3)
        self.assertEqual(digit_reduction([6]), 6)
        self.assertEqual(digit_reduction([9]), 9)
        self.assertEqual(digit_reduction([7]), 7)

    def test_multi_digit(self):
        self.assertEqual(digit_reduction([4, 5]), 9)  # 4+5=9
        self.assertEqual(digit_reduction([7, 2]), 9)  # 7+2=9
        self.assertEqual(digit_reduction([1, 2]), 3)  # 1+2=3

    def test_spine_membership(self):
        self.assertTrue(is_spine_word([3]))
        self.assertTrue(is_spine_word([6]))
        self.assertTrue(is_spine_word([9]))
        self.assertTrue(is_spine_word([4, 5]))
        self.assertFalse(is_spine_word([7]))
        self.assertFalse(is_spine_word([1]))

    def test_spine_class(self):
        self.assertEqual(spine_class([3]), 'sheath_3')
        self.assertEqual(spine_class([6]), 'sheath_6')
        self.assertEqual(spine_class([9]), 'anchor_9')
        self.assertEqual(spine_class([7]), 'off_spine')


class TestFractalUnfolding(unittest.TestCase):

    def test_level_0(self):
        words = unfold_level([], 0)
        self.assertEqual(len(words), 10)
        self.assertEqual(words[0], [0])
        self.assertEqual(words[9], [9])

    def test_level_1(self):
        level0 = unfold_level([], 0)
        level1 = unfold_level(level0, 1)
        self.assertEqual(len(level1), 100)
        self.assertEqual(level1[0], [0, 0])
        self.assertEqual(level1[99], [9, 9])

    def test_build_levels(self):
        levels = build_fractal_levels(2)
        self.assertEqual(len(levels), 3)
        self.assertEqual(len(levels[0]), 10)
        self.assertEqual(len(levels[1]), 100)
        self.assertEqual(len(levels[2]), 1000)


class TestSCALoopTracker(unittest.TestCase):

    def test_full_loop(self):
        tracker = SCALoopTracker()
        self.assertFalse(tracker.completed)

        tracker.feed(LATTICE)   # 1 = Quadratic
        self.assertEqual(tracker.stage, 'duality')

        tracker.feed(COUNTER)   # 2 = Duality
        self.assertEqual(tracker.stage, 'fixed_point')

        tracker.feed(RESET)     # 9 = Fixed Point
        self.assertEqual(tracker.stage, 'coherence')

        tracker.feed(LATTICE)   # 1 = Coherence
        self.assertTrue(tracker.completed)
        self.assertEqual(tracker.stage, 'coherence_achieved')

    def test_partial_loop(self):
        tracker = SCALoopTracker()
        tracker.feed(LATTICE)
        tracker.feed(HARMONY)   # Wrong -- not COUNTER
        self.assertEqual(tracker.progress, 0.25)  # Still at step 1

    def test_progress(self):
        tracker = SCALoopTracker()
        self.assertAlmostEqual(tracker.progress, 0.0)
        tracker.feed(LATTICE)
        self.assertAlmostEqual(tracker.progress, 0.25)


class TestCommutator(unittest.TestCase):

    def test_with_real_cl_table(self):
        from ck_sim.being.ck_sim_heartbeat import compose
        # CL[1][2] = 3, CL[2][1] = 3 -> commute
        self.assertFalse(commutator_nonzero(1, 2, compose))
        # CL[2][4] = 4, CL[4][2] = 4 -> commute
        self.assertFalse(commutator_nonzero(2, 4, compose))

    def test_persistence_metric(self):
        from ck_sim.being.ck_sim_heartbeat import compose
        pairs = [(i, j) for i in range(10) for j in range(i+1, 10)]
        p = commutator_persistence(pairs, compose)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)


# ================================================================
#  CODEC TESTS: Force Vector Ranges
# ================================================================

class TestNavierStokesCodec(unittest.TestCase):

    def setUp(self):
        self.codec = NavierStokesCodec()

    def test_force_vector_range(self):
        raw = {
            'omega_mag': 5.0, 'omega_max': 10.0,
            'strain_alignment': 0.8,
            'scale_epsilon': 0.3,
            'energy_dissipation': 2.0, 'diss_max': 5.0,
            'omega_gradient': 1.0, 'grad_max': 4.0,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_perfect_alignment(self):
        """Perfect alignment -> aperture=0 (fully closed), low defect."""
        raw = {
            'omega_mag': 1.0, 'omega_max': 1.0,
            'strain_alignment': 1.0,
            'scale_epsilon': 0.5,
            'energy_dissipation': 0.5, 'diss_max': 1.0,
            'omega_gradient': 0.0, 'grad_max': 1.0,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[0], 0.0)  # aperture = 1 - 1.0 = 0

    def test_master_lemma_defect(self):
        raw = {'strain_alignment': 0.8}
        delta = self.codec.master_lemma_defect(raw)
        self.assertAlmostEqual(delta, 0.2)

        raw = {'strain_alignment': 1.0}
        delta = self.codec.master_lemma_defect(raw)
        self.assertAlmostEqual(delta, 0.0)

    def test_lens_mismatch(self):
        raw = {
            'omega_mag': 1.0, 'omega_max': 1.0,
            'strain_alignment': 1.0,
            'omega_gradient': 0.0, 'grad_max': 1.0,
            'energy_dissipation': 1.0, 'diss_max': 1.0,
            'energy': 1.0, 'scale_epsilon': 1.0,
        }
        mm = self.codec.lens_mismatch(raw)
        self.assertGreaterEqual(mm, 0.0)

    def test_feed_produces_operator(self):
        for _ in range(5):
            raw = {
                'omega_mag': 1.0, 'omega_max': 2.0,
                'strain_alignment': 0.5,
                'scale_epsilon': 0.5,
                'energy_dissipation': 0.5, 'diss_max': 1.0,
                'omega_gradient': 0.5, 'grad_max': 1.0,
            }
            op = self.codec.feed(raw)
            self.assertGreaterEqual(op, 0)
            self.assertLess(op, 10)


class TestRiemannCodec(unittest.TestCase):

    def setUp(self):
        self.codec = RiemannCodec()

    def test_force_vector_range(self):
        raw = {
            'sigma': 0.5, 't': 14.134,
            'zeta_mag': 0.001, 'height_max': 100.0,
            'dzeta_dt': 0.1, 'phase': 0.5,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_critical_line_high_aperture(self):
        """On critical line (sigma=0.5), aperture should be 1.0."""
        raw = {'sigma': 0.5, 't': 14.0, 'zeta_mag': 1.0,
               'height_max': 100.0, 'dzeta_dt': 0.0, 'phase': 0.0}
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[0], 1.0)

    def test_off_line_low_aperture(self):
        """Off critical line (sigma=0.75), aperture should be 0.0."""
        raw = {'sigma': 0.75, 't': 14.0, 'zeta_mag': 1.0,
               'height_max': 100.0, 'dzeta_dt': 0.0, 'phase': 0.0}
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[0], 0.0)

    def test_zero_proximity_high_pressure(self):
        """Near a zero (low zeta_mag), pressure should be high."""
        raw = {'sigma': 0.5, 't': 14.134, 'zeta_mag': 0.001,
               'height_max': 100.0, 'dzeta_dt': 0.0, 'phase': 0.0}
        vec = self.codec.map_to_force_vector(raw)
        self.assertGreater(vec[1], 0.9)  # Near 1/(1+0.001)


class TestPvsNPCodec(unittest.TestCase):

    def setUp(self):
        self.codec = PvsNPCodec()

    def test_force_vector_range(self):
        raw = {
            'backbone_fraction': 0.5,
            'clause_density': 4.267,
            'propagation_depth': 0.5,
            'local_coherence': 0.5,
            'search_tree_balance': 0.5,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_easy_sat_low_pressure(self):
        """Easy SAT (low density) should have low pressure."""
        raw = {'clause_density': 2.0, 'backbone_fraction': 0.1,
               'propagation_depth': 0.9, 'local_coherence': 0.9,
               'search_tree_balance': 0.9}
        vec = self.codec.map_to_force_vector(raw)
        self.assertLess(vec[1], 0.6)  # pressure < 0.6


class TestYangMillsCodec(unittest.TestCase):

    def setUp(self):
        self.codec = YangMillsCodec()

    def test_force_vector_range(self):
        raw = {
            'vacuum_overlap': 0.9,
            'action_density': 0.5, 'action_max': 1.0,
            'momentum': 0.5, 'p_max': 1.0,
            'topological_charge': 1.0,
            'field_gradient': 0.1,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_integer_charge_high_binding(self):
        """Integer topological charge + high gauge_invariant => binding near 1.0."""
        raw = {'vacuum_overlap': 0.5, 'action_density': 0.5, 'action_max': 1.0,
               'momentum': 0.5, 'p_max': 1.0,
               'topological_charge': 1.0, 'field_gradient': 0.0,
               'gauge_invariant': 1.0}
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[3], 1.0)


class TestBSDCodec(unittest.TestCase):

    def setUp(self):
        self.codec = BSDCodec()

    def test_force_vector_range(self):
        raw = {
            'rank_analytic': 1, 'rank_algebraic': 1,
            'regulator': 1.0, 'reg_max': 10.0,
            'conductor': 37.0, 'sha_order': 1.0, 'torsion_order': 2,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_rank_match_high_aperture(self):
        """Matching ranks => aperture = 1/(1+0) = 1.0."""
        raw = {'rank_analytic': 1, 'rank_algebraic': 1,
               'regulator': 1.0, 'reg_max': 10.0,
               'conductor': 37.0, 'sha_order': 1.0, 'torsion_order': 2}
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[0], 1.0)

    def test_rank_mismatch_low_aperture(self):
        """Mismatched ranks => aperture < 1.0."""
        raw = {'rank_analytic': 2, 'rank_algebraic': 0,
               'regulator': 1.0, 'reg_max': 10.0,
               'conductor': 37.0, 'sha_order': 1.0, 'torsion_order': 2}
        vec = self.codec.map_to_force_vector(raw)
        self.assertLess(vec[0], 0.5)

    def test_master_lemma_defect(self):
        raw = {'rank_analytic': 1, 'rank_algebraic': 1,
               'leading_coeff_analytic': 0.5, 'leading_coeff_arithmetic': 0.5}
        self.assertAlmostEqual(self.codec.master_lemma_defect(raw), 0.0)

        raw = {'rank_analytic': 2, 'rank_algebraic': 0,
               'leading_coeff_analytic': 0.5, 'leading_coeff_arithmetic': 0.5}
        self.assertAlmostEqual(self.codec.master_lemma_defect(raw), 2.0)


class TestHodgeCodec(unittest.TestCase):

    def setUp(self):
        self.codec = HodgeCodec()

    def test_force_vector_range(self):
        raw = {
            'algebraic_projection': 0.8,
            'analytic_residual': 0.1,
            'dimension': 3,
            'period_coherence': 0.9,
            'residual_gradient': 0.1,
        }
        vec = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_algebraic_class_high_aperture(self):
        """Known algebraic class => high aperture."""
        raw = {'algebraic_projection': 1.0, 'analytic_residual': 0.0,
               'dimension': 2, 'period_coherence': 1.0, 'residual_gradient': 0.0}
        vec = self.codec.map_to_force_vector(raw)
        self.assertAlmostEqual(vec[0], 1.0)


# ================================================================
#  CODEC REGISTRY TESTS
# ================================================================

class TestCodecRegistry(unittest.TestCase):

    def test_all_6_in_registry(self):
        self.assertEqual(len(CLAY_CODEC_REGISTRY), 6)
        for pid in ['navier_stokes', 'riemann', 'p_vs_np',
                     'yang_mills', 'bsd', 'hodge']:
            self.assertIn(pid, CLAY_CODEC_REGISTRY)

    def test_create_codec_factory(self):
        for pid in CLAY_CODEC_REGISTRY:
            codec = create_codec(pid)
            self.assertEqual(codec.problem_id, pid)

    def test_create_codec_invalid(self):
        with self.assertRaises(ValueError):
            create_codec('nonexistent')

    def test_register_clay_codecs(self):
        register_clay_codecs()
        for pid in ['navier_stokes', 'riemann', 'p_vs_np',
                     'yang_mills', 'bsd', 'hodge']:
            self.assertIn(pid, CODEC_REGISTRY)


# ================================================================
#  SAFETY INTEGRATION: Codecs use safety rails
# ================================================================

class TestCodecSafety(unittest.TestCase):

    def test_nan_input_handled(self):
        codec = NavierStokesCodec()
        raw = {'omega_mag': float('nan'), 'omega_max': 1.0,
               'strain_alignment': 0.5, 'scale_epsilon': 0.5,
               'energy_dissipation': 0.5, 'diss_max': 1.0,
               'omega_gradient': 0.5, 'grad_max': 1.0}
        # Feed 3 times to get D2
        for _ in range(3):
            op = codec.feed(raw)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, 10)

    def test_extreme_values_clamped(self):
        codec = RiemannCodec()
        raw = {'sigma': 100.0, 't': 1e15, 'zeta_mag': 1e10,
               'height_max': 1.0, 'dzeta_dt': 1e5, 'phase': 100.0}
        vec = codec.map_to_force_vector(raw)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)


if __name__ == '__main__':
    unittest.main()
