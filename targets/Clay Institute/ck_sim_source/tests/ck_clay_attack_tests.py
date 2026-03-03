"""
Tests for ck_clay_attack.py + ck_thermal_probe.py + adversarial test cases.
Hardware Attack infrastructure validation.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest

from ck_sim.doing.ck_clay_attack import (
    StatisticalSweep, SweepResult, NoisyGenerator, NoiseResilienceSweep,
    NoiseResult, sweep_result_to_dict, noise_result_to_dict,
)
from ck_sim.being.ck_thermal_probe import (
    ThermalProbe, ThermalProbeResult, ThermalSnapshot,
    thermal_result_to_dict, _pearson, _r_squared,
)
from ck_sim.doing.ck_clay_protocol import ProbeConfig, ClayProbe
from ck_sim.doing.ck_clay_generators import (
    create_generator, NavierStokesGenerator, RiemannGenerator,
    PvsNPGenerator, YangMillsGenerator, BSDGenerator, HodgeGenerator,
)
from ck_sim.being.ck_sdv_safety import DeterministicRNG, clamp


# ================================================================
#  STATISTICAL SWEEP TESTS
# ================================================================

class TestStatisticalSweep(unittest.TestCase):
    """Tests for StatisticalSweep class."""

    def test_sweep_produces_result(self):
        """StatisticalSweep returns a valid SweepResult."""
        sweep = StatisticalSweep('navier_stokes', 'high_strain',
                                 n_seeds=5, n_levels=4)
        result = sweep.run()
        self.assertIsInstance(result, SweepResult)
        self.assertEqual(result.n_seeds, 5)
        self.assertEqual(result.n_levels, 4)
        self.assertEqual(len(result.per_seed_finals), 5)

    def test_sweep_delta_statistics(self):
        """Mean and std computed correctly."""
        sweep = StatisticalSweep('riemann', 'off_line',
                                 n_seeds=10, n_levels=4)
        result = sweep.run()
        self.assertGreater(result.delta_mean, 0)
        self.assertGreaterEqual(result.delta_std, 0)
        self.assertLessEqual(result.delta_ci_lower, result.delta_mean)
        self.assertGreaterEqual(result.delta_ci_upper, result.delta_mean)

    def test_sweep_ci_contains_mean(self):
        """99.9% CI contains the mean."""
        sweep = StatisticalSweep('p_vs_np', 'hard',
                                 n_seeds=5, n_levels=4)
        result = sweep.run()
        self.assertLessEqual(result.delta_ci_lower, result.delta_mean)
        self.assertGreaterEqual(result.delta_ci_upper, result.delta_mean)

    def test_sweep_hashes_unique(self):
        """Different seeds produce different hashes."""
        sweep = StatisticalSweep('yang_mills', 'excited',
                                 n_seeds=5, n_levels=4)
        result = sweep.run()
        self.assertTrue(result.all_hashes_unique)

    def test_sweep_timing(self):
        """Timing information is recorded."""
        sweep = StatisticalSweep('bsd', 'rank_mismatch',
                                 n_seeds=3, n_levels=4)
        result = sweep.run()
        self.assertGreater(result.total_time_s, 0)
        self.assertGreater(result.per_probe_time_s, 0)

    def test_sweep_mean_trajectory(self):
        """Mean trajectory has correct length."""
        sweep = StatisticalSweep('hodge', 'analytic_only',
                                 n_seeds=3, n_levels=6)
        result = sweep.run()
        self.assertEqual(len(result.mean_trajectory), 6)
        self.assertEqual(len(result.std_trajectory), 6)

    def test_sweep_serialization(self):
        """SweepResult serializes to dict correctly."""
        sweep = StatisticalSweep('navier_stokes', 'lamb_oseen',
                                 n_seeds=3, n_levels=4)
        result = sweep.run()
        d = sweep_result_to_dict(result)
        self.assertEqual(d['problem_id'], 'navier_stokes')
        self.assertEqual(d['n_seeds'], 3)
        self.assertIn('delta_mean', d)
        self.assertIn('sweep_hash', d)


# ================================================================
#  NOISY GENERATOR TESTS
# ================================================================

class TestNoisyGenerator(unittest.TestCase):
    """Tests for NoisyGenerator wrapper."""

    def test_noisy_generator_produces_output(self):
        """NoisyGenerator returns a dict with all expected keys."""
        base = create_generator('navier_stokes', seed=42)
        noisy = NoisyGenerator(base, noise_sigma=0.1)
        reading = noisy.generate(0, 'lamb_oseen')
        self.assertIn('omega_mag', reading)
        self.assertIn('strain_alignment', reading)

    def test_zero_noise_matches_base(self):
        """With sigma=0, noisy output matches base (integer rounding aside)."""
        base = create_generator('riemann', seed=42)
        noisy = NoisyGenerator(base, noise_sigma=0.0, noise_seed=1)
        # Reset both to same state
        base.reset(42)
        clean = base.generate(0, 'known_zero')
        noisy.base.reset(42)
        noisy_reading = noisy.generate(0, 'known_zero')
        # Float fields should be exactly equal at sigma=0
        self.assertAlmostEqual(clean['sigma'], noisy_reading['sigma'], places=5)

    def test_noise_clamping(self):
        """Clamped fields stay in [0,1] even with large noise."""
        base = create_generator('navier_stokes', seed=42)
        noisy = NoisyGenerator(base, noise_sigma=5.0)  # Very large noise
        reading = noisy.generate(0, 'lamb_oseen')
        # strain_alignment was originally [0,1], should stay clamped
        self.assertGreaterEqual(reading['strain_alignment'], 0.0)
        self.assertLessEqual(reading['strain_alignment'], 1.0)

    def test_noisy_probe_runs(self):
        """A probe with a noisy generator completes without error."""
        base = create_generator('p_vs_np', seed=42)
        noisy = NoisyGenerator(base, noise_sigma=0.1)
        config = ProbeConfig(problem_id='p_vs_np', test_case='hard',
                             seed=42, n_levels=4)
        probe = ClayProbe(config)
        probe.generator = noisy
        result = probe.run()
        self.assertGreater(len(result.steps), 0)


# ================================================================
#  NOISE RESILIENCE SWEEP TESTS
# ================================================================

class TestNoiseResilienceSweep(unittest.TestCase):
    """Tests for NoiseResilienceSweep class."""

    def test_noise_sweep_produces_result(self):
        """NoiseResilienceSweep returns a valid NoiseResult."""
        sweep = NoiseResilienceSweep('navier_stokes', 'high_strain',
                                    sigmas=[0.0, 0.1, 0.5],
                                    n_levels=4)
        result = sweep.run()
        self.assertIsInstance(result, NoiseResult)
        self.assertEqual(len(result.noise_levels), 3)
        self.assertEqual(len(result.delta_at_noise), 3)

    def test_noise_base_delta(self):
        """Base delta (sigma=0) is recorded."""
        sweep = NoiseResilienceSweep('riemann', 'off_line',
                                    sigmas=[0.0, 0.1],
                                    n_levels=4)
        result = sweep.run()
        self.assertEqual(result.base_delta, result.delta_at_noise[0])

    def test_noise_structural_depth(self):
        """Structural depth is computed."""
        sweep = NoiseResilienceSweep('yang_mills', 'excited',
                                    sigmas=[0.0, 0.01, 0.05, 0.1],
                                    n_levels=4)
        result = sweep.run()
        self.assertGreater(result.structural_depth, 0)

    def test_noise_serialization(self):
        """NoiseResult serializes to dict correctly."""
        sweep = NoiseResilienceSweep('hodge', 'algebraic',
                                    sigmas=[0.0, 0.1],
                                    n_levels=4)
        result = sweep.run()
        d = noise_result_to_dict(result)
        self.assertEqual(d['problem_id'], 'hodge')
        self.assertIn('critical_noise', d)


# ================================================================
#  THERMAL PROBE TESTS
# ================================================================

class TestThermalProbe(unittest.TestCase):
    """Tests for ThermalProbe class."""

    def test_thermal_probe_produces_result(self):
        """ThermalProbe returns a valid ThermalProbeResult."""
        config = ProbeConfig(problem_id='navier_stokes',
                             test_case='high_strain',
                             seed=42, n_levels=4)
        probe = ThermalProbe(config)
        result = probe.run()
        self.assertIsInstance(result, ThermalProbeResult)
        self.assertEqual(len(result.thermal_snapshots), 4)

    def test_thermal_snapshots_have_data(self):
        """Each snapshot has temperature and timing data."""
        config = ProbeConfig(problem_id='riemann',
                             test_case='off_line',
                             seed=42, n_levels=4)
        probe = ThermalProbe(config)
        result = probe.run()
        for snap in result.thermal_snapshots:
            self.assertIsInstance(snap, ThermalSnapshot)
            self.assertGreater(snap.gpu_temp_c, 0)
            self.assertGreaterEqual(snap.wall_time_ms, 0)

    def test_thermal_correlation_computed(self):
        """Correlations are computed (may be 0 but must be finite)."""
        config = ProbeConfig(problem_id='yang_mills',
                             test_case='excited',
                             seed=42, n_levels=6)
        probe = ThermalProbe(config)
        result = probe.run()
        self.assertGreaterEqual(result.thermal_delta_correlation, -1.0)
        self.assertLessEqual(result.thermal_delta_correlation, 1.0)

    def test_thermal_scaling_determined(self):
        """Compute time scaling is determined."""
        config = ProbeConfig(problem_id='bsd',
                             test_case='rank_mismatch',
                             seed=42, n_levels=6)
        probe = ThermalProbe(config)
        result = probe.run()
        self.assertIn(result.compute_time_scaling,
                      ['linear', 'quadratic', 'exponential', 'unknown'])

    def test_thermal_probe_result_matches_base(self):
        """Thermal probe produces same defect trajectory as base probe."""
        config = ProbeConfig(problem_id='hodge',
                             test_case='algebraic',
                             seed=42, n_levels=4)
        # Base probe
        base_probe = ClayProbe(config)
        base_result = base_probe.run()
        # Thermal probe
        thermal_probe = ThermalProbe(config)
        thermal_result = thermal_probe.run()
        # Defect trajectories should match (same seed, same config)
        base_defects = base_result.defect_trajectory
        thermal_defects = thermal_result.probe_result.defect_trajectory
        self.assertEqual(len(base_defects), len(thermal_defects))
        for bd, td in zip(base_defects, thermal_defects):
            self.assertAlmostEqual(bd, td, places=6)

    def test_thermal_serialization(self):
        """ThermalProbeResult serializes correctly."""
        config = ProbeConfig(problem_id='p_vs_np',
                             test_case='hard',
                             seed=42, n_levels=4)
        probe = ThermalProbe(config)
        result = probe.run()
        d = thermal_result_to_dict(result)
        self.assertEqual(d['problem_id'], 'p_vs_np')
        self.assertIn('thermal_snapshots', d)
        self.assertEqual(len(d['thermal_snapshots']), 4)


# ================================================================
#  PEARSON / R-SQUARED HELPER TESTS
# ================================================================

class TestStatHelpers(unittest.TestCase):
    """Tests for internal statistical helper functions."""

    def test_pearson_perfect_positive(self):
        """Perfectly correlated data gives r=1."""
        r = _pearson([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        self.assertAlmostEqual(r, 1.0, places=5)

    def test_pearson_perfect_negative(self):
        """Perfectly anti-correlated data gives r=-1."""
        r = _pearson([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])
        self.assertAlmostEqual(r, -1.0, places=5)

    def test_pearson_zero_variance(self):
        """Constant data gives r=0 (no variance)."""
        r = _pearson([1, 1, 1], [2, 3, 4])
        self.assertEqual(r, 0.0)

    def test_pearson_short_list(self):
        """Lists shorter than 2 return 0."""
        self.assertEqual(_pearson([1], [2]), 0.0)

    def test_r_squared_perfect_fit(self):
        """Perfect linear data gives R^2=1."""
        r2 = _r_squared([0, 1, 2, 3], [0, 2, 4, 6])
        self.assertAlmostEqual(r2, 1.0, places=5)


# ================================================================
#  ADVERSARIAL TEST CASE TESTS
# ================================================================

class TestAdversarialNS(unittest.TestCase):
    """Tests for NS adversarial generators."""

    def test_near_singular_produces_valid(self):
        gen = NavierStokesGenerator(seed=42)
        reading = gen.generate(5, 'near_singular')
        self.assertIn('omega_mag', reading)
        self.assertGreater(reading['omega_mag'], 100)  # Should be large
        self.assertGreater(reading['strain_alignment'], 0)
        self.assertLessEqual(reading['strain_alignment'], 1.0)

    def test_eigenvalue_crossing_produces_valid(self):
        gen = NavierStokesGenerator(seed=42)
        reading = gen.generate(6, 'eigenvalue_crossing')  # At crossing
        self.assertIn('omega_mag', reading)
        self.assertIn('strain_alignment', reading)

    def test_near_singular_probe(self):
        config = ProbeConfig(problem_id='navier_stokes',
                             test_case='near_singular', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


class TestAdversarialRH(unittest.TestCase):
    """Tests for RH adversarial generators."""

    def test_off_line_dense_produces_valid(self):
        gen = RiemannGenerator(seed=42)
        reading = gen.generate(5, 'off_line_dense')
        self.assertIn('sigma', reading)
        self.assertGreater(reading['sigma'], 0.5)

    def test_quarter_gap_produces_valid(self):
        gen = RiemannGenerator(seed=42)
        reading = gen.generate(3, 'quarter_gap')
        self.assertIn('sigma', reading)
        self.assertGreater(reading['sigma'], 0.5)
        self.assertLess(reading['sigma'], 1.0)

    def test_off_line_dense_probe(self):
        config = ProbeConfig(problem_id='riemann',
                             test_case='off_line_dense', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


class TestAdversarialPNP(unittest.TestCase):
    """Tests for PvsNP adversarial generators."""

    def test_scaling_sweep_produces_valid(self):
        gen = PvsNPGenerator(seed=42)
        reading = gen.generate(5, 'scaling_sweep')
        self.assertIn('backbone_fraction', reading)
        self.assertIn('clause_density', reading)

    def test_adversarial_local_produces_valid(self):
        gen = PvsNPGenerator(seed=42)
        reading = gen.generate(5, 'adversarial_local')
        self.assertIn('local_coherence', reading)
        self.assertGreater(reading['local_coherence'], 0.5)

    def test_scaling_sweep_probe(self):
        config = ProbeConfig(problem_id='p_vs_np',
                             test_case='scaling_sweep', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


class TestAdversarialYM(unittest.TestCase):
    """Tests for YM adversarial generators."""

    def test_weak_coupling_produces_valid(self):
        gen = YangMillsGenerator(seed=42)
        reading = gen.generate(5, 'weak_coupling')
        self.assertIn('vacuum_overlap', reading)
        self.assertIn('topological_charge', reading)

    def test_scaling_lattice_produces_valid(self):
        gen = YangMillsGenerator(seed=42)
        reading = gen.generate(5, 'scaling_lattice')
        self.assertIn('vacuum_overlap', reading)

    def test_weak_coupling_probe(self):
        config = ProbeConfig(problem_id='yang_mills',
                             test_case='weak_coupling', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


class TestAdversarialBSD(unittest.TestCase):
    """Tests for BSD adversarial generators."""

    def test_rank2_explicit_produces_valid(self):
        gen = BSDGenerator(seed=42)
        reading = gen.generate(0, 'rank2_explicit')
        self.assertEqual(reading['rank_analytic'], 2)
        self.assertEqual(reading['rank_algebraic'], 2)

    def test_large_sha_produces_valid(self):
        gen = BSDGenerator(seed=42)
        reading = gen.generate(5, 'large_sha_candidate')
        self.assertGreater(reading['sha_order'], 5)

    def test_rank2_probe(self):
        config = ProbeConfig(problem_id='bsd',
                             test_case='rank2_explicit', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


class TestAdversarialHodge(unittest.TestCase):
    """Tests for Hodge adversarial generators."""

    def test_prime_sweep_deep_produces_valid(self):
        gen = HodgeGenerator(seed=42)
        reading = gen.generate(5, 'prime_sweep_deep')
        self.assertIn('algebraic_projection', reading)
        self.assertGreater(reading['algebraic_projection'], 0)

    def test_known_transcendental_produces_valid(self):
        gen = HodgeGenerator(seed=42)
        reading = gen.generate(5, 'known_transcendental')
        self.assertIn('analytic_residual', reading)
        self.assertGreater(reading['analytic_residual'], 0.5)

    def test_known_transcendental_probe(self):
        config = ProbeConfig(problem_id='hodge',
                             test_case='known_transcendental', seed=42, n_levels=4)
        result = ClayProbe(config).run()
        self.assertGreater(len(result.steps), 0)


if __name__ == '__main__':
    unittest.main()
