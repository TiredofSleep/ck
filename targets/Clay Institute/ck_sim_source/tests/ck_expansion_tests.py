"""
ck_expansion_tests.py -- Tests for 35 Expansion Problems
=========================================================
Operator: PULSE (3) -- Testing the expanded coherence manifold.

Tests:
  TestNeighborGenerators    (18) -- Each neighbor produces valid raw_reading
  TestNeighborCodecDispatch (18) -- Neighbors route to correct parent codec
  TestExpansionCodecs       (17) -- Each expansion codec produces valid 5D vector
  TestExpansionGenerators   (17) -- Each expansion generator produces valid raw_reading
  TestRegistration           (5) -- All 41 problems registered in all registries
  TestExpandedAtlas           (3) -- Atlas extraction + equation fitting

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.being.ck_tig_bundle import (
    TIG_PATHS, DUAL_LENSES, CLAY_PROBLEMS, ALL_PROBLEMS, RESET,
)
from ck_sim.doing.ck_spectrometer import (
    ProblemType, CALIBRATION_CASES, FRONTIER_CASES,
)
from ck_sim.doing.ck_clay_generators import create_generator
from ck_sim.being.ck_clay_codecs import create_codec, CLAY_CODEC_REGISTRY
from ck_sim.doing.ck_neighbor_generators import (
    NEIGHBOR_GENERATOR_REGISTRY, NEIGHBOR_CODEC_MAP,
)
from ck_sim.doing.ck_expansion_generators import EXPANSION_GENERATOR_REGISTRY
from ck_sim.being.ck_expansion_codecs import EXPANSION_CODEC_REGISTRY


# ================================================================
#  TestNeighborGenerators
# ================================================================

class TestNeighborGenerators(unittest.TestCase):
    """Each neighbor generator produces valid raw_reading for parent codec."""

    def _check_neighbor(self, pid):
        """Helper: generate and feed through parent codec."""
        gen = create_generator(pid)
        codec = create_codec(pid)
        cal_tc = CALIBRATION_CASES.get(pid, 'default')
        raw = gen.generate(5, cal_tc)
        self.assertIsInstance(raw, dict)
        self.assertGreater(len(raw), 0)
        vec = codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)
        defect = codec.master_lemma_defect(raw)
        self.assertGreaterEqual(defect, 0.0)
        self.assertLessEqual(defect, 1.0)

    def test_ns_2d(self): self._check_neighbor('ns_2d')
    def test_ns_sqg(self): self._check_neighbor('ns_sqg')
    def test_ns_euler(self): self._check_neighbor('ns_euler')
    def test_pnp_ac0(self): self._check_neighbor('pnp_ac0')
    def test_pnp_clique(self): self._check_neighbor('pnp_clique')
    def test_pnp_bpp(self): self._check_neighbor('pnp_bpp')
    def test_rh_dirichlet(self): self._check_neighbor('rh_dirichlet')
    def test_rh_function_field(self): self._check_neighbor('rh_function_field')
    def test_rh_fake(self): self._check_neighbor('rh_fake')
    def test_ym_schwinger(self): self._check_neighbor('ym_schwinger')
    def test_ym_lattice(self): self._check_neighbor('ym_lattice')
    def test_ym_phi4(self): self._check_neighbor('ym_phi4')
    def test_bsd_function_field(self): self._check_neighbor('bsd_function_field')
    def test_bsd_avg_rank(self): self._check_neighbor('bsd_avg_rank')
    def test_bsd_sato_tate(self): self._check_neighbor('bsd_sato_tate')
    def test_hodge_tate(self): self._check_neighbor('hodge_tate')
    def test_hodge_standard(self): self._check_neighbor('hodge_standard')
    def test_hodge_transcendental(self): self._check_neighbor('hodge_transcendental')


class TestNeighborCodecDispatch(unittest.TestCase):
    """Neighbors route to the correct parent codec class."""

    def _check_dispatch(self, pid, expected_parent):
        codec = create_codec(pid)
        parent_codec = CLAY_CODEC_REGISTRY[expected_parent]
        self.assertIsInstance(codec, parent_codec)

    def test_ns_2d_uses_ns_codec(self): self._check_dispatch('ns_2d', 'navier_stokes')
    def test_ns_sqg_uses_ns_codec(self): self._check_dispatch('ns_sqg', 'navier_stokes')
    def test_ns_euler_uses_ns_codec(self): self._check_dispatch('ns_euler', 'navier_stokes')
    def test_pnp_ac0_uses_pnp_codec(self): self._check_dispatch('pnp_ac0', 'p_vs_np')
    def test_pnp_clique_uses_pnp_codec(self): self._check_dispatch('pnp_clique', 'p_vs_np')
    def test_pnp_bpp_uses_pnp_codec(self): self._check_dispatch('pnp_bpp', 'p_vs_np')
    def test_rh_dirichlet_uses_rh_codec(self): self._check_dispatch('rh_dirichlet', 'riemann')
    def test_rh_ff_uses_rh_codec(self): self._check_dispatch('rh_function_field', 'riemann')
    def test_rh_fake_uses_rh_codec(self): self._check_dispatch('rh_fake', 'riemann')
    def test_ym_schwinger_uses_ym_codec(self): self._check_dispatch('ym_schwinger', 'yang_mills')
    def test_ym_lattice_uses_ym_codec(self): self._check_dispatch('ym_lattice', 'yang_mills')
    def test_ym_phi4_uses_ym_codec(self): self._check_dispatch('ym_phi4', 'yang_mills')
    def test_bsd_ff_uses_bsd_codec(self): self._check_dispatch('bsd_function_field', 'bsd')
    def test_bsd_avg_uses_bsd_codec(self): self._check_dispatch('bsd_avg_rank', 'bsd')
    def test_bsd_st_uses_bsd_codec(self): self._check_dispatch('bsd_sato_tate', 'bsd')
    def test_hodge_tate_uses_hodge_codec(self): self._check_dispatch('hodge_tate', 'hodge')
    def test_hodge_std_uses_hodge_codec(self): self._check_dispatch('hodge_standard', 'hodge')
    def test_hodge_trans_uses_hodge_codec(self): self._check_dispatch('hodge_transcendental', 'hodge')


# ================================================================
#  TestExpansionCodecs
# ================================================================

class TestExpansionCodecs(unittest.TestCase):
    """Each expansion codec produces valid 5D force vector + defect."""

    def _check_codec(self, pid):
        gen = create_generator(pid)
        codec = create_codec(pid)
        cal_tc = CALIBRATION_CASES.get(pid, 'default')
        raw = gen.generate(5, cal_tc)
        vec = codec.map_to_force_vector(raw)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)
        defect = codec.master_lemma_defect(raw)
        self.assertGreaterEqual(defect, 0.0)
        self.assertLessEqual(defect, 1.0)
        lens_a = codec.lens_a(raw)
        lens_b = codec.lens_b(raw)
        self.assertGreater(len(lens_a), 0)
        self.assertGreater(len(lens_b), 0)

    def test_collatz(self): self._check_codec('collatz')
    def test_abc(self): self._check_codec('abc')
    def test_langlands(self): self._check_codec('langlands')
    def test_continuum(self): self._check_codec('continuum')
    def test_ramsey(self): self._check_codec('ramsey')
    def test_twin_primes(self): self._check_codec('twin_primes')
    def test_poincare_4d(self): self._check_codec('poincare_4d')
    def test_cosmo_constant(self): self._check_codec('cosmo_constant')
    def test_falconer(self): self._check_codec('falconer')
    def test_jacobian(self): self._check_codec('jacobian')
    def test_inverse_galois(self): self._check_codec('inverse_galois')
    def test_banach_tarski(self): self._check_codec('banach_tarski')
    def test_info_paradox(self): self._check_codec('info_paradox')
    def test_bridge_rmt(self): self._check_codec('bridge_rmt')
    def test_bridge_expander(self): self._check_codec('bridge_expander')
    def test_bridge_fractal(self): self._check_codec('bridge_fractal')
    def test_bridge_spectral(self): self._check_codec('bridge_spectral')


# ================================================================
#  TestExpansionGenerators
# ================================================================

class TestExpansionGenerators(unittest.TestCase):
    """Each expansion generator produces valid raw_reading."""

    def _check_generator(self, pid):
        gen = create_generator(pid)
        # Test both calibration and frontier
        cal_tc = CALIBRATION_CASES.get(pid, 'default')
        raw_cal = gen.generate(5, cal_tc)
        self.assertIsInstance(raw_cal, dict)
        self.assertGreater(len(raw_cal), 0)

        frontier = FRONTIER_CASES.get(pid, 'default')
        ftc = frontier if isinstance(frontier, str) else frontier[0]
        gen.reset()
        raw_fro = gen.generate(5, ftc)
        self.assertIsInstance(raw_fro, dict)
        self.assertGreater(len(raw_fro), 0)

    def test_collatz(self): self._check_generator('collatz')
    def test_abc(self): self._check_generator('abc')
    def test_langlands(self): self._check_generator('langlands')
    def test_continuum(self): self._check_generator('continuum')
    def test_ramsey(self): self._check_generator('ramsey')
    def test_twin_primes(self): self._check_generator('twin_primes')
    def test_poincare_4d(self): self._check_generator('poincare_4d')
    def test_cosmo_constant(self): self._check_generator('cosmo_constant')
    def test_falconer(self): self._check_generator('falconer')
    def test_jacobian(self): self._check_generator('jacobian')
    def test_inverse_galois(self): self._check_generator('inverse_galois')
    def test_banach_tarski(self): self._check_generator('banach_tarski')
    def test_info_paradox(self): self._check_generator('info_paradox')
    def test_bridge_rmt(self): self._check_generator('bridge_rmt')
    def test_bridge_expander(self): self._check_generator('bridge_expander')
    def test_bridge_fractal(self): self._check_generator('bridge_fractal')
    def test_bridge_spectral(self): self._check_generator('bridge_spectral')


# ================================================================
#  TestRegistration
# ================================================================

class TestRegistration(unittest.TestCase):
    """All 41 problems registered in all 5 registries."""

    def test_all_problems_in_tig_paths(self):
        """Every ALL_PROBLEMS entry has a TIG path."""
        for pid in ALL_PROBLEMS:
            self.assertIn(pid, TIG_PATHS, f'{pid} missing from TIG_PATHS')

    def test_all_problems_in_dual_lenses(self):
        """Every ALL_PROBLEMS entry has dual lenses."""
        for pid in ALL_PROBLEMS:
            self.assertIn(pid, DUAL_LENSES, f'{pid} missing from DUAL_LENSES')

    def test_all_problems_have_problem_type(self):
        """Every ALL_PROBLEMS entry has a ProblemType enum value."""
        pt_values = {pt.value for pt in ProblemType}
        for pid in ALL_PROBLEMS:
            self.assertIn(pid, pt_values, f'{pid} missing from ProblemType enum')

    def test_all_problems_have_calibration(self):
        """Every ALL_PROBLEMS entry has a calibration test case."""
        for pid in ALL_PROBLEMS:
            self.assertIn(pid, CALIBRATION_CASES, f'{pid} missing from CALIBRATION_CASES')

    def test_all_problems_have_frontier(self):
        """Every ALL_PROBLEMS entry has a frontier test case."""
        for pid in ALL_PROBLEMS:
            self.assertIn(pid, FRONTIER_CASES, f'{pid} missing from FRONTIER_CASES')

    def test_all_tig_paths_end_at_reset(self):
        """All TIG paths end at RESET."""
        for pid, path in TIG_PATHS.items():
            self.assertEqual(path[-1], RESET, f'{pid} path does not end at RESET')

    def test_problem_count(self):
        """41 total problems."""
        self.assertEqual(len(ALL_PROBLEMS), 41)
        self.assertEqual(len(TIG_PATHS), 41)

    def test_generator_coverage(self):
        """Every problem has a generator (6 Clay + 18 neighbor + 17 expansion)."""
        for pid in ALL_PROBLEMS:
            gen = create_generator(pid)
            self.assertIsNotNone(gen, f'No generator for {pid}')

    def test_codec_coverage(self):
        """Every problem has a codec."""
        for pid in ALL_PROBLEMS:
            codec = create_codec(pid)
            self.assertIsNotNone(codec, f'No codec for {pid}')


# ================================================================
#  TestExpandedAtlas
# ================================================================

class TestExpandedAtlas(unittest.TestCase):
    """Equation atlas extraction across expanded manifold."""

    def test_atlas_covers_all_clay(self):
        """Equation atlas works for original 6 Clay problems."""
        from ck_sim.doing.ck_governing_equations import extract_governing_equation
        for pid in CLAY_PROBLEMS:
            levels = list(range(3, 10))  # Short for speed
            delta = [0.5 * (1.0 - 0.05 * lv) for lv in levels]
            eq = extract_governing_equation(levels, delta, pid, 'cal', 'tc')
            self.assertIsNotNone(eq.best_model)
            self.assertIn(eq.asymptotic_class,
                          ['affirmative', 'gap', 'indeterminate'])

    def test_atlas_covers_expansion(self):
        """Equation extraction works for expansion problems."""
        from ck_sim.doing.ck_governing_equations import extract_governing_equation
        expansion_pids = list(NEIGHBOR_GENERATOR_REGISTRY.keys()) + \
                         list(EXPANSION_GENERATOR_REGISTRY.keys())
        for pid in expansion_pids[:5]:  # Sample for speed
            levels = list(range(3, 10))
            delta = [0.3 + 0.01 * lv for lv in levels]
            eq = extract_governing_equation(levels, delta, pid, 'cal', 'tc')
            self.assertIsNotNone(eq.best_model)

    def test_all_41_dispatch(self):
        """All 41 problems can generate + codec + get 5D vector."""
        for pid in ALL_PROBLEMS:
            gen = create_generator(pid)
            codec = create_codec(pid)
            cal_tc = CALIBRATION_CASES[pid]
            raw = gen.generate(3, cal_tc)
            vec = codec.map_to_force_vector(raw)
            self.assertEqual(len(vec), 5, f'{pid} failed: vec len != 5')
            defect = codec.master_lemma_defect(raw)
            self.assertGreaterEqual(defect, 0.0)
            self.assertLessEqual(defect, 1.0)


if __name__ == '__main__':
    unittest.main()
