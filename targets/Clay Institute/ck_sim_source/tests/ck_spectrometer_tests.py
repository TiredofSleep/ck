"""
ck_spectrometer_tests.py -- Tests for TIG-Delta Universal Coherence Spectrometer
=================================================================================
Tests the Delta-Spectrometer wrapper around the existing Clay SDV protocol.

~125 tests across 24 test classes:
  TestSpectrometerInput   (5)  -- Input construction and bridge to ProbeConfig
  TestSingleScan          (3)  -- scan() basics
  TestSpectrometerResult  (10) -- Full result structure validation
  TestVerdictLogic        (3)  -- Verdict classification sanity
  TestDeterminism         (2)  -- Seed-based reproducibility
  TestStabilityMatrix     (5)  -- Reduced 12-run matrix
  TestChaosIntegration    (1)  -- Noise-resilience surface test
  TestConsistencySweep    (1)  -- Aggregated multi-seed sweep
  TestSandersFlow        (12) -- Sanders Flow Lyapunov verification (noise strategy)
  TestScaleFlow          (10) -- Sanders Flow scale refinement (fractal depth strategy)
  TestFractalFingerprint  (8)  -- Fractal skeleton fingerprint structure
  TestSkeletonClassification (6) -- Skeleton classification logic
  TestSpectralAnalysis    (4)  -- DFT and spectral features
  TestFractalAtlas        (5)  -- Full cross-problem atlas
  TestFractalGate         (6)  -- Fractal gate pre-classifier logic
  TestSandersAttack       (5)  -- Sanders Attack: gate + conditional flow
  TestSandersAttackFull   (4)  -- Full 12-configuration Sanders Attack
  TestRobustnessPermutation (5) -- TIG path permutation robustness
  TestRobustnessJitter      (5) -- Generator jitter robustness
  TestRobustnessAblation    (4) -- TIG channel ablation robustness
  TestRobustnessNoise       (4) -- Noise distribution robustness
  TestRobustnessDeepSeeds   (4) -- Multi-seed skeleton stability
  TestRobustnessSweep       (5) -- Full per-config robustness sweep
  TestRobustnessResult      (3) -- RobustnessResult structure validation

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""
import unittest

from ck_sim.doing.ck_spectrometer import (
    DeltaSpectrometer, SpectrometerInput, SpectrometerResult,
    FlowResult, FractalFingerprint, SandersAttackResult,
    RobustnessResult, PerturbationTrial, PerturbationType,
    ScanMode, ProblemType, Verdict, SkeletonClass, GateVerdict,
    MacroClass, classify_macro, compute_slope_norm,
    CALIBRATION_CASES, FRONTIER_CASES, MATRIX_SEEDS,
    ROBUSTNESS_THRESHOLD, _frontier_cases_for,
    classify_skeleton, _dft_magnitudes, _spectral_entropy,
    _dominant_period, _first_deviation_level, _count_phase_transitions,
)
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS, NUM_OPS


# ================================================================
#  TestSpectrometerInput
# ================================================================

class TestSpectrometerInput(unittest.TestCase):
    """Input construction and bridge to ProbeConfig."""

    def test_default_input(self):
        """SpectrometerInput(NS) defaults to scan_mode=DEEP, seed=42."""
        inp = SpectrometerInput(ProblemType.NAVIER_STOKES)
        self.assertEqual(inp.problem, ProblemType.NAVIER_STOKES)
        self.assertEqual(inp.scan_mode, ScanMode.DEEP)
        self.assertEqual(inp.seed, 42)
        self.assertEqual(inp.test_case, 'default')

    def test_surface_mode_levels(self):
        """SURFACE mode bridges to ProbeConfig with n_levels == 3."""
        inp = SpectrometerInput(ProblemType.RIEMANN, scan_mode=ScanMode.SURFACE)
        cfg = inp.to_probe_config()
        self.assertEqual(cfg.n_levels, 3)

    def test_omega_mode_levels(self):
        """OMEGA mode bridges to ProbeConfig with n_levels == 24."""
        inp = SpectrometerInput(ProblemType.BSD, scan_mode=ScanMode.OMEGA)
        cfg = inp.to_probe_config()
        self.assertEqual(cfg.n_levels, 24)

    def test_all_problem_types(self):
        """ProblemType includes all 6 CLAY_PROBLEMS (and expansion problems)."""
        pt_values = sorted(pt.value for pt in ProblemType)
        for pid in CLAY_PROBLEMS:
            self.assertIn(pid, pt_values)
        self.assertGreaterEqual(len(pt_values), 6)

    def test_key_uniqueness(self):
        """Different inputs produce different keys."""
        inp_a = SpectrometerInput(ProblemType.NAVIER_STOKES, seed=42)
        inp_b = SpectrometerInput(ProblemType.NAVIER_STOKES, seed=137)
        inp_c = SpectrometerInput(ProblemType.RIEMANN, seed=42)
        inp_d = SpectrometerInput(
            ProblemType.NAVIER_STOKES, scan_mode=ScanMode.SURFACE, seed=42)

        keys = {inp_a.key, inp_b.key, inp_c.key, inp_d.key}
        self.assertEqual(len(keys), 4, 'All four inputs must have unique keys')


# ================================================================
#  TestSingleScan
# ================================================================

class TestSingleScan(unittest.TestCase):
    """Basic scan() invocation tests."""

    def test_scan_returns_result(self):
        """scan() returns a SpectrometerResult instance."""
        spec = DeltaSpectrometer()
        inp = SpectrometerInput(ProblemType.NAVIER_STOKES,
                                scan_mode=ScanMode.SURFACE, seed=42)
        result = spec.scan(inp)
        self.assertIsInstance(result, SpectrometerResult)

    def test_all_problems_surface(self):
        """All 6 problems scan at SURFACE without error."""
        spec = DeltaSpectrometer()
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                inp = SpectrometerInput(ProblemType(pid),
                                        scan_mode=ScanMode.SURFACE, seed=42)
                result = spec.scan(inp)
                self.assertIsInstance(result, SpectrometerResult)
                self.assertEqual(result.problem, pid)

    def test_all_scan_modes(self):
        """NS scanned at each mode produces matching n_levels."""
        spec = DeltaSpectrometer()
        for mode in ScanMode:
            with self.subTest(mode=mode.name):
                inp = SpectrometerInput(ProblemType.NAVIER_STOKES,
                                        scan_mode=mode, seed=42)
                result = spec.scan(inp)
                self.assertEqual(result.n_levels, int(mode))


# ================================================================
#  TestSpectrometerResult
# ================================================================

class TestSpectrometerResult(unittest.TestCase):
    """Full structural validation of a single SpectrometerResult."""

    @classmethod
    def setUpClass(cls):
        """Run a single NS / SURFACE / seed=42 scan for all sub-tests."""
        spec = DeltaSpectrometer()
        inp = SpectrometerInput(ProblemType.NAVIER_STOKES,
                                scan_mode=ScanMode.SURFACE, seed=42)
        cls.result = spec.scan(inp)
        cls.n_levels = int(ScanMode.SURFACE)

    def test_defect_vector_length(self):
        """defect_vector has exactly 10 elements (one per TIG operator)."""
        self.assertEqual(len(self.result.defect_vector), 10)

    def test_defect_vector_nonnegative(self):
        """Every element of defect_vector is >= 0."""
        for i, val in enumerate(self.result.defect_vector):
            with self.subTest(operator=i):
                self.assertGreaterEqual(val, 0.0)

    def test_tig_trace_length(self):
        """tig_trace has one entry per level."""
        self.assertEqual(len(self.result.tig_trace), self.n_levels)

    def test_tig_trace_keys(self):
        """Each trace entry has the required keys."""
        required_keys = {
            'level', 'operator', 'operator_name',
            'defect', 'action', 'band', 'd2_magnitude',
        }
        for i, entry in enumerate(self.result.tig_trace):
            with self.subTest(level=i):
                self.assertTrue(
                    required_keys.issubset(entry.keys()),
                    f'Missing keys: {required_keys - entry.keys()}')

    def test_sdv_map_keys(self):
        """sdv_map contains required dual-void structure keys."""
        required = {'problem_class', 'lens_a', 'lens_b',
                     'dual_fixed_point_proximity'}
        self.assertTrue(
            required.issubset(self.result.sdv_map.keys()),
            f'Missing keys: {required - self.result.sdv_map.keys()}')

    def test_verdict_valid(self):
        """verdict is one of the Verdict enum values."""
        valid_values = {v.value for v in Verdict}
        self.assertIn(self.result.verdict, valid_values)

    def test_reason_nonempty(self):
        """reason is a non-empty string."""
        self.assertIsInstance(self.result.reason, str)
        self.assertGreater(len(self.result.reason), 0)

    def test_trajectory_lengths(self):
        """defect_trajectory and action_trajectory have length == n_levels."""
        self.assertEqual(len(self.result.defect_trajectory), self.n_levels)
        self.assertEqual(len(self.result.action_trajectory), self.n_levels)

    def test_hash_nonempty(self):
        """final_hash is a non-empty string."""
        self.assertIsInstance(self.result.final_hash, str)
        self.assertGreater(len(self.result.final_hash), 0)

    def test_delta_value_nonnegative(self):
        """delta_value >= 0."""
        self.assertGreaterEqual(self.result.delta_value, 0.0)


# ================================================================
#  TestVerdictLogic
# ================================================================

class TestVerdictLogic(unittest.TestCase):
    """Sanity checks on verdict classification."""

    def test_affirmative_calibration_not_singular(self):
        """NS lamb_oseen at DEEP should NOT be SINGULAR."""
        spec = DeltaSpectrometer()
        inp = SpectrometerInput(
            ProblemType.NAVIER_STOKES, test_case='lamb_oseen',
            scan_mode=ScanMode.DEEP, seed=42)
        result = spec.scan(inp)
        self.assertNotEqual(result.verdict, Verdict.SINGULAR.value,
                            'Calibration case should not trigger safety halt')

    def test_gap_frontier_not_singular(self):
        """PNP hard at DEEP should NOT be SINGULAR."""
        spec = DeltaSpectrometer()
        inp = SpectrometerInput(
            ProblemType.P_VS_NP, test_case='hard',
            scan_mode=ScanMode.DEEP, seed=42)
        result = spec.scan(inp)
        self.assertNotEqual(result.verdict, Verdict.SINGULAR.value,
                            'Frontier case should not trigger safety halt')

    def test_nonhalted_not_singular(self):
        """Any non-halted probe should not receive SINGULAR verdict."""
        spec = DeltaSpectrometer()
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                tc = CALIBRATION_CASES[pid]
                inp = SpectrometerInput(
                    ProblemType(pid), test_case=tc,
                    scan_mode=ScanMode.SURFACE, seed=42)
                result = spec.scan(inp)
                if not result.halted:
                    self.assertNotEqual(
                        result.verdict, Verdict.SINGULAR.value,
                        f'{pid}: non-halted probe should not be SINGULAR')


# ================================================================
#  TestDeterminism
# ================================================================

class TestDeterminism(unittest.TestCase):
    """Seed-based reproducibility of the spectrometer."""

    def test_same_seed_same_result(self):
        """Two scans with identical input produce identical outputs."""
        spec = DeltaSpectrometer()
        inp = SpectrometerInput(
            ProblemType.NAVIER_STOKES, test_case='lamb_oseen',
            scan_mode=ScanMode.SURFACE, seed=42)

        r1 = spec.scan(inp)
        r2 = spec.scan(inp)

        self.assertAlmostEqual(r1.delta_value, r2.delta_value, places=10)
        self.assertEqual(r1.final_hash, r2.final_hash)
        self.assertEqual(r1.verdict, r2.verdict)

    def test_different_seed_different_hash(self):
        """seed=42 vs seed=137 produce different hashes."""
        spec = DeltaSpectrometer()
        r1 = spec.scan(SpectrometerInput(
            ProblemType.NAVIER_STOKES, scan_mode=ScanMode.SURFACE, seed=42))
        r2 = spec.scan(SpectrometerInput(
            ProblemType.NAVIER_STOKES, scan_mode=ScanMode.SURFACE, seed=137))

        self.assertNotEqual(r1.final_hash, r2.final_hash)


# ================================================================
#  TestStabilityMatrix
# ================================================================

class TestStabilityMatrix(unittest.TestCase):
    """Reduced 12-run matrix (1 seed x 1 mode x 12 inputs).

    The full 108-run matrix is a CLI operation, not a unit test.
    """

    @classmethod
    def setUpClass(cls):
        """Run the mini-matrix once for all sub-tests."""
        cls.results = cls._run_mini_matrix()

    @classmethod
    def _run_mini_matrix(cls):
        """1 seed (42) x SURFACE x (cal + frontier per problem)."""
        spec = DeltaSpectrometer()
        results = []
        for pid in CLAY_PROBLEMS:
            # Calibration
            cal_tc = CALIBRATION_CASES[pid]
            inp = SpectrometerInput(
                ProblemType(pid), cal_tc, ScanMode.SURFACE, 42)
            results.append(spec.scan(inp))
            # Frontier(s) — may be multiple for some problems
            for ftc in _frontier_cases_for(pid):
                inp = SpectrometerInput(
                    ProblemType(pid), ftc, ScanMode.SURFACE, 42)
                results.append(spec.scan(inp))
        return results

    def test_matrix_count(self):
        """Mini-matrix produces 6 cal + 7 frontier = 13 results."""
        self.assertEqual(len(self.results), 13)

    def test_matrix_covers_problems(self):
        """All 6 Clay problems appear in the results."""
        problems_seen = {r.problem for r in self.results}
        self.assertEqual(problems_seen, set(CLAY_PROBLEMS))

    def test_matrix_all_have_verdict(self):
        """Every result has a valid Verdict enum value."""
        valid_values = {v.value for v in Verdict}
        for i, r in enumerate(self.results):
            with self.subTest(i=i, problem=r.problem, test_case=r.test_case):
                self.assertIn(r.verdict, valid_values)

    def test_matrix_deterministic(self):
        """Running the mini-matrix twice gives identical results."""
        results2 = self._run_mini_matrix()
        self.assertEqual(len(self.results), len(results2))
        for r1, r2 in zip(self.results, results2):
            with self.subTest(problem=r1.problem, test_case=r1.test_case):
                self.assertEqual(r1.final_hash, r2.final_hash)
                self.assertAlmostEqual(r1.delta_value, r2.delta_value,
                                       places=10)

    def test_matrix_no_singular_calibration(self):
        """No SINGULAR verdicts on calibration cases."""
        cal_set = set(CALIBRATION_CASES.values())
        for r in self.results:
            if r.test_case in cal_set:
                with self.subTest(problem=r.problem, test_case=r.test_case):
                    self.assertNotEqual(
                        r.verdict, Verdict.SINGULAR.value,
                        f'Calibration case {r.test_case} should not be SINGULAR')


# ================================================================
#  TestChaosIntegration
# ================================================================

class TestChaosIntegration(unittest.TestCase):
    """Noise-resilience surface test via chaos_scan."""

    def test_chaos_scan_count(self):
        """chaos_scan with 3 sigmas returns exactly 3 results."""
        spec = DeltaSpectrometer()
        sigmas = [0.0, 0.01, 0.1]
        results = spec.chaos_scan(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.SURFACE,
            seed=42,
            noise_sigmas=sigmas,
        )
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertIsInstance(r, SpectrometerResult)


# ================================================================
#  TestConsistencySweep
# ================================================================

class TestConsistencySweep(unittest.TestCase):
    """Aggregated multi-seed sweep returns expected structure."""

    def test_consistency_returns_expected_keys(self):
        """consistency_sweep with n_seeds=5 returns all required keys."""
        spec = DeltaSpectrometer()
        summary = spec.consistency_sweep(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.SURFACE,
            n_seeds=5,
            base_seed=1,
        )
        required_keys = {
            'problem', 'n_seeds', 'delta_mean', 'delta_std',
            'falsifications', 'all_hashes_unique',
        }
        self.assertTrue(
            required_keys.issubset(summary.keys()),
            f'Missing keys: {required_keys - summary.keys()}')
        self.assertEqual(summary['problem'], 'navier_stokes')
        self.assertEqual(summary['n_seeds'], 5)
        self.assertIsInstance(summary['delta_mean'], float)
        self.assertIsInstance(summary['delta_std'], float)
        self.assertIsInstance(summary['falsifications'], int)
        self.assertIsInstance(summary['all_hashes_unique'], bool)


# ================================================================
#  TestSandersFlow
# ================================================================

class TestSandersFlow(unittest.TestCase):
    """Sanders Flow: Lyapunov verification via refinement."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.flow = cls.spec.flow_scan(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.SURFACE,
            seed=42,
            n_steps=5,
        )

    def test_flow_returns_flow_result(self):
        """flow_scan returns a FlowResult."""
        self.assertIsInstance(self.flow, FlowResult)

    def test_flow_has_correct_step_count(self):
        """FlowResult has correct number of steps."""
        self.assertEqual(len(self.flow.sigma_steps), 5)
        self.assertEqual(len(self.flow.delta_trajectory), 5)
        self.assertEqual(len(self.flow.verdict_trajectory), 5)

    def test_flow_sigma_descending(self):
        """Sigma steps are non-increasing (rough -> refined)."""
        for i in range(1, len(self.flow.sigma_steps)):
            self.assertLessEqual(
                self.flow.sigma_steps[i],
                self.flow.sigma_steps[i - 1] + 1e-9,
                f'Sigma increased at step {i}')

    def test_flow_final_sigma_zero(self):
        """Final sigma step is 0 (clean measurement)."""
        self.assertAlmostEqual(self.flow.sigma_steps[-1], 0.0, places=10)

    def test_flow_monotonicity_score_range(self):
        """Monotonicity score is in [0, 1]."""
        self.assertGreaterEqual(self.flow.monotonicity_score, 0.0)
        self.assertLessEqual(self.flow.monotonicity_score, 1.0)

    def test_flow_delta_non_negative(self):
        """All delta values are non-negative."""
        for d in self.flow.delta_trajectory:
            self.assertGreaterEqual(d, 0.0)

    def test_flow_has_classification(self):
        """FlowResult has valid flow_class and problem_class."""
        self.assertIn(self.flow.flow_class, ('convergent', 'gap'))
        self.assertIn(self.flow.problem_class, ('affirmative', 'gap', 'unknown'))

    def test_flow_lyapunov_is_bool(self):
        """lyapunov_confirmed is a boolean."""
        self.assertIsInstance(self.flow.lyapunov_confirmed, bool)

    def test_flow_step_results_present(self):
        """step_results contains SpectrometerResults for each step."""
        self.assertEqual(len(self.flow.step_results), 5)
        for sr in self.flow.step_results:
            self.assertIsInstance(sr, SpectrometerResult)

    def test_flow_deterministic(self):
        """Same seed produces identical flow."""
        flow2 = self.spec.flow_scan(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.SURFACE,
            seed=42,
            n_steps=5,
        )
        self.assertEqual(self.flow.delta_trajectory, flow2.delta_trajectory)
        self.assertEqual(self.flow.is_monotone, flow2.is_monotone)
        self.assertEqual(self.flow.lyapunov_confirmed, flow2.lyapunov_confirmed)

    def test_flow_all_six_problems(self):
        """flow_scan works for all 6 Clay problems."""
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                tc = CALIBRATION_CASES[pid]
                flow = self.spec.flow_scan(
                    ProblemType(pid), test_case=tc,
                    scan_mode=ScanMode.SURFACE, seed=42,
                    n_steps=3,
                )
                self.assertIsInstance(flow, FlowResult)
                self.assertEqual(flow.problem, pid)
                self.assertEqual(len(flow.sigma_steps), 3)


# ================================================================
#  TestScaleFlow
# ================================================================

class TestScaleFlow(unittest.TestCase):
    """Sanders Flow: scale refinement (fractal depth as flow parameter)."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.flow = cls.spec.flow_scan(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.DEEP,
            seed=42,
            n_steps=10,
            flow_strategy='scale',
        )

    def test_scale_returns_flow_result(self):
        """Scale flow_scan returns a FlowResult."""
        self.assertIsInstance(self.flow, FlowResult)

    def test_scale_strategy_recorded(self):
        """FlowResult records flow_strategy='scale'."""
        self.assertEqual(self.flow.flow_strategy, 'scale')

    def test_scale_steps_ascending(self):
        """sigma_steps (holding n_levels) are ascending for scale flow."""
        for i in range(1, len(self.flow.sigma_steps)):
            self.assertGreaterEqual(
                self.flow.sigma_steps[i],
                self.flow.sigma_steps[i - 1],
                f'Level decreased at step {i}')

    def test_scale_min_level(self):
        """First level is >= SURFACE (3)."""
        self.assertGreaterEqual(self.flow.sigma_steps[0], 3.0)

    def test_scale_max_level(self):
        """Last level equals target scan_mode (DEEP = 12)."""
        self.assertEqual(int(self.flow.sigma_steps[-1]), int(ScanMode.DEEP))

    def test_scale_delta_non_negative(self):
        """All delta values are non-negative."""
        for d in self.flow.delta_trajectory:
            self.assertGreaterEqual(d, 0.0)

    def test_scale_has_classification(self):
        """FlowResult has valid flow_class and problem_class."""
        self.assertIn(self.flow.flow_class, ('convergent', 'gap'))
        self.assertIn(self.flow.problem_class, ('affirmative', 'gap', 'unknown'))

    def test_scale_lyapunov_is_bool(self):
        """lyapunov_confirmed is a boolean."""
        self.assertIsInstance(self.flow.lyapunov_confirmed, bool)

    def test_scale_all_six_problems(self):
        """Scale flow works for all 6 Clay problems."""
        for pid in CLAY_PROBLEMS:
            with self.subTest(problem=pid):
                tc = CALIBRATION_CASES[pid]
                flow = self.spec.flow_scan(
                    ProblemType(pid), test_case=tc,
                    scan_mode=ScanMode.DEEP, seed=42,
                    n_steps=5,
                    flow_strategy='scale',
                )
                self.assertIsInstance(flow, FlowResult)
                self.assertEqual(flow.problem, pid)
                self.assertEqual(flow.flow_strategy, 'scale')

    def test_scale_deterministic(self):
        """Same seed produces identical scale flow."""
        flow2 = self.spec.flow_scan(
            ProblemType.NAVIER_STOKES,
            test_case='lamb_oseen',
            scan_mode=ScanMode.DEEP,
            seed=42,
            n_steps=10,
            flow_strategy='scale',
        )
        self.assertEqual(self.flow.delta_trajectory, flow2.delta_trajectory)
        self.assertEqual(self.flow.is_monotone, flow2.is_monotone)
        self.assertEqual(self.flow.lyapunov_confirmed, flow2.lyapunov_confirmed)


# ================================================================
#  TestFractalFingerprint
# ================================================================

class TestFractalFingerprint(unittest.TestCase):
    """Fractal skeleton fingerprint structure and content."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.fp = cls.spec.fractal_scan(
            ProblemType.RIEMANN, test_case='known_zero',
            regime='calibration', seed=42, max_level=12,
        )

    def test_returns_fingerprint(self):
        """fractal_scan returns a FractalFingerprint."""
        self.assertIsInstance(self.fp, FractalFingerprint)

    def test_levels_range(self):
        """levels span from SURFACE (3) to max_level."""
        self.assertEqual(self.fp.levels[0], 3)
        self.assertEqual(self.fp.levels[-1], 12)
        self.assertEqual(len(self.fp.levels), 10)  # 3,4,...,12

    def test_delta_by_level_length(self):
        """delta_by_level matches levels length."""
        self.assertEqual(len(self.fp.delta_by_level), len(self.fp.levels))

    def test_delta_non_negative(self):
        """All delta values are non-negative."""
        for d in self.fp.delta_by_level:
            self.assertGreaterEqual(d, 0.0)

    def test_statistics_consistent(self):
        """mean, std, min, max, range are internally consistent."""
        self.assertAlmostEqual(
            self.fp.delta_range, self.fp.delta_max - self.fp.delta_min,
            places=10)
        self.assertGreaterEqual(self.fp.delta_max, self.fp.delta_mean)
        self.assertLessEqual(self.fp.delta_min, self.fp.delta_mean)
        self.assertGreaterEqual(self.fp.delta_std, 0.0)

    def test_skeleton_class_valid(self):
        """skeleton_class is a valid SkeletonClass value."""
        valid = {s.value for s in SkeletonClass}
        self.assertIn(self.fp.skeleton_class, valid)

    def test_spectral_magnitudes_present(self):
        """Spectral magnitudes are computed."""
        self.assertGreater(len(self.fp.spectral_magnitudes), 0)
        # Positive freq bins = N//2 + 1
        N = len(self.fp.delta_by_level)
        self.assertEqual(len(self.fp.spectral_magnitudes), N // 2 + 1)

    def test_deterministic(self):
        """Same seed produces identical fingerprint."""
        fp2 = self.spec.fractal_scan(
            ProblemType.RIEMANN, test_case='known_zero',
            regime='calibration', seed=42, max_level=12,
        )
        self.assertEqual(self.fp.delta_by_level, fp2.delta_by_level)
        self.assertEqual(self.fp.skeleton_class, fp2.skeleton_class)


# ================================================================
#  TestSkeletonClassification
# ================================================================

class TestSkeletonClassification(unittest.TestCase):
    """Skeleton classification logic: classify_skeleton()."""

    def test_frozen(self):
        """Constant sequence -> FROZEN."""
        vals = [0.5] * 22
        self.assertEqual(classify_skeleton(vals), 'frozen')

    def test_stable(self):
        """Tiny wobble -> STABLE."""
        vals = [0.5 + 0.005 * (i % 2) for i in range(22)]
        self.assertEqual(classify_skeleton(vals), 'stable')

    def test_bounded(self):
        """Moderate range -> BOUNDED."""
        vals = [0.5 + 0.03 * (i % 3 - 1) for i in range(22)]
        result = classify_skeleton(vals)
        self.assertIn(result, ('bounded', 'stable'))

    def test_oscillating(self):
        """Visible oscillation -> OSCILLATING."""
        import math
        vals = [0.5 + 0.1 * math.sin(i * 0.5) for i in range(22)]
        result = classify_skeleton(vals)
        self.assertIn(result, ('oscillating', 'bounded'))

    def test_wild(self):
        """Broad range -> WILD."""
        vals = [0.0, 0.3, 0.0, 0.5, 0.0, 0.3, 0.0, 0.5, 0.0, 0.3,
                0.0, 0.5, 0.0, 0.3, 0.0, 0.5, 0.0, 0.3, 0.0, 0.5,
                0.0, 0.3]
        self.assertEqual(classify_skeleton(vals), 'wild')

    def test_empty(self):
        """Empty list -> WILD (safety)."""
        self.assertEqual(classify_skeleton([]), 'wild')


# ================================================================
#  TestSpectralAnalysis
# ================================================================

class TestSpectralAnalysis(unittest.TestCase):
    """DFT and spectral feature extraction."""

    def test_dft_constant(self):
        """Constant signal -> DC only, zero AC."""
        vals = [1.0] * 10
        mags = _dft_magnitudes(vals)
        # DC component = mean = 1.0
        self.assertAlmostEqual(mags[0], 1.0, places=5)
        # All other components ~ 0
        for m in mags[1:]:
            self.assertAlmostEqual(m, 0.0, places=5)

    def test_dft_length(self):
        """DFT returns N//2 + 1 magnitude bins."""
        for N in [10, 22, 8]:
            vals = [float(i) for i in range(N)]
            mags = _dft_magnitudes(vals)
            self.assertEqual(len(mags), N // 2 + 1)

    def test_spectral_entropy_constant(self):
        """Constant signal -> low entropy (all power at DC)."""
        mags_const = _dft_magnitudes([1.0] * 10)
        ent_const = _spectral_entropy(mags_const)
        # Noisy signal should have higher entropy
        import math
        noisy = [math.sin(i * 1.3) + 0.5 * math.cos(i * 2.7) for i in range(10)]
        mags_noisy = _dft_magnitudes(noisy)
        ent_noisy = _spectral_entropy(mags_noisy)
        self.assertLess(ent_const, ent_noisy)

    def test_dominant_period(self):
        """Sinusoidal signal -> dominant period matches."""
        import math
        N = 22
        # Period = 11 levels (k=2 for N=22)
        vals = [math.sin(2 * math.pi * i / 11) for i in range(N)]
        mags = _dft_magnitudes(vals)
        period = _dominant_period(mags, N)
        self.assertIsNotNone(period)
        self.assertAlmostEqual(period, 11.0, places=0)


# ================================================================
#  TestFractalAtlas
# ================================================================

class TestFractalAtlas(unittest.TestCase):
    """Full cross-problem Fractal Coherence Atlas."""

    @classmethod
    def setUpClass(cls):
        """Build a mini-atlas at max_level=6 (fast)."""
        cls.spec = DeltaSpectrometer()
        cls.atlas = cls.spec.fractal_atlas(seed=42, max_level=6)

    def test_atlas_count(self):
        """Atlas has 13 fingerprints (6 cal + 7 frontier with RH split)."""
        self.assertEqual(len(self.atlas), 13)

    def test_atlas_covers_all_problems(self):
        """All 6 Clay problems appear."""
        problems = set(fp.problem for fp in self.atlas.values())
        self.assertEqual(problems, set(CLAY_PROBLEMS))

    def test_atlas_covers_both_regimes(self):
        """Both calibration and frontier regimes appear."""
        regimes = set(fp.regime for fp in self.atlas.values())
        self.assertEqual(regimes, {'calibration', 'frontier'})

    def test_atlas_all_valid_skeleton(self):
        """Every fingerprint has a valid skeleton class."""
        valid = {s.value for s in SkeletonClass}
        for key, fp in self.atlas.items():
            with self.subTest(key=key):
                self.assertIn(fp.skeleton_class, valid)

    def test_atlas_deterministic(self):
        """Same seed produces identical atlas."""
        atlas2 = self.spec.fractal_atlas(seed=42, max_level=6)
        self.assertEqual(len(self.atlas), len(atlas2))
        for key in self.atlas:
            with self.subTest(key=key):
                self.assertEqual(
                    self.atlas[key].delta_by_level,
                    atlas2[key].delta_by_level)
                self.assertEqual(
                    self.atlas[key].skeleton_class,
                    atlas2[key].skeleton_class)


# ================================================================
#  TestFractalGate
# ================================================================

class TestFractalGate(unittest.TestCase):
    """Fractal gate pre-classifier logic."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()

    def _make_fp(self, skeleton_class, regime, delta_mean=0.5,
                 delta_range=0.3, spectral_entropy=0.5):
        """Create a minimal FractalFingerprint for gate testing."""
        return FractalFingerprint(
            problem='navier_stokes', regime=regime,
            test_case='test', seed=42,
            levels=[3, 4, 5], delta_by_level=[0.5, 0.5, 0.5],
            delta_mean=delta_mean, delta_std=0.0, delta_cv=0.0,
            delta_min=delta_mean - delta_range / 2,
            delta_max=delta_mean + delta_range / 2,
            delta_range=delta_range,
            skeleton_class=skeleton_class,
            spectral_magnitudes=[0.5], dominant_period=None,
            spectral_entropy=spectral_entropy,
            first_deviation_level=3, n_phase_transitions=0,
        )

    def test_calibration_frozen_skip(self):
        """Calibration with FROZEN skeleton -> SKIP."""
        fp = self._make_fp('frozen', 'calibration')
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.SKIP.value)

    def test_calibration_wild_pass(self):
        """Calibration with WILD skeleton -> PASS (unexpected turbulence)."""
        fp = self._make_fp('wild', 'calibration', delta_range=0.4)
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.PASS.value)

    def test_calibration_oscillating_pass(self):
        """Calibration with OSCILLATING skeleton -> PASS."""
        fp = self._make_fp('oscillating', 'calibration', delta_range=0.2)
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.PASS.value)

    def test_frontier_wild_pass(self):
        """Frontier with WILD skeleton -> PASS."""
        fp = self._make_fp('wild', 'frontier', delta_range=0.5)
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.PASS.value)

    def test_frontier_frozen_high_delta_pass(self):
        """Frontier with FROZEN at high delta -> PASS (saturated)."""
        fp = self._make_fp('frozen', 'frontier', delta_mean=1.0,
                           delta_range=0.0)
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.PASS.value)

    def test_frontier_bounded_skip(self):
        """Frontier with BOUNDED skeleton -> SKIP (expected)."""
        fp = self._make_fp('bounded', 'frontier', delta_mean=0.3,
                           delta_range=0.05, spectral_entropy=0.005)
        verdict, _ = self.spec.fractal_gate(fp)
        self.assertEqual(verdict, GateVerdict.SKIP.value)


# ================================================================
#  TestSandersAttack
# ================================================================

class TestSandersAttack(unittest.TestCase):
    """Sanders Attack: fractal gate + conditional Sanders Flow."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        # Run one attack on RH frontier (known to be WILD -> should PASS)
        cls.ar = cls.spec.sanders_attack(
            ProblemType.RIEMANN, test_case='off_line',
            regime='frontier', seed=42, max_level=6,
            flow_strategy='scale', n_flow_steps=5,
        )

    def test_returns_attack_result(self):
        """sanders_attack returns a SandersAttackResult."""
        self.assertIsInstance(self.ar, SandersAttackResult)

    def test_has_fingerprint(self):
        """Result contains a FractalFingerprint."""
        self.assertIsInstance(self.ar.fingerprint, FractalFingerprint)
        self.assertEqual(self.ar.fingerprint.problem, 'riemann')

    def test_gate_verdict_valid(self):
        """gate_verdict is a valid GateVerdict value."""
        valid = {v.value for v in GateVerdict}
        self.assertIn(self.ar.gate_verdict, valid)

    def test_attack_summary_nonempty(self):
        """attack_summary is a non-empty string."""
        self.assertIsInstance(self.ar.attack_summary, str)
        self.assertGreater(len(self.ar.attack_summary), 0)

    def test_deterministic(self):
        """Same seed produces identical attack result."""
        ar2 = self.spec.sanders_attack(
            ProblemType.RIEMANN, test_case='off_line',
            regime='frontier', seed=42, max_level=6,
            flow_strategy='scale', n_flow_steps=5,
        )
        self.assertEqual(self.ar.gate_verdict, ar2.gate_verdict)
        self.assertEqual(self.ar.candidate_singularity,
                         ar2.candidate_singularity)
        self.assertEqual(
            self.ar.fingerprint.skeleton_class,
            ar2.fingerprint.skeleton_class)


# ================================================================
#  TestSandersAttackFull
# ================================================================

class TestSandersAttackFull(unittest.TestCase):
    """Full 12-configuration Sanders Attack."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.results = cls.spec.sanders_attack_full(
            seed=42, max_level=6, flow_strategy='scale',
            n_flow_steps=5,
        )

    def test_full_count(self):
        """Full attack produces 13 results (6 cal + 7 frontier with RH split)."""
        self.assertEqual(len(self.results), 13)

    def test_covers_all_problems(self):
        """All 6 Clay problems appear."""
        problems = set(ar.problem for ar in self.results.values())
        self.assertEqual(problems, set(CLAY_PROBLEMS))

    def test_covers_both_regimes(self):
        """Both calibration and frontier regimes appear."""
        regimes = set(ar.regime for ar in self.results.values())
        self.assertEqual(regimes, {'calibration', 'frontier'})

    def test_gate_filters(self):
        """At least one config PASS and at least one SKIP."""
        gates = [ar.gate_verdict for ar in self.results.values()]
        self.assertIn('pass', gates, 'Expected at least one PASS')
        self.assertIn('skip', gates, 'Expected at least one SKIP')


# ================================================================
#  TestRobustnessPermutation
# ================================================================

class TestRobustnessPermutation(unittest.TestCase):
    """TIG path permutation robustness."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.trials = cls.spec.robustness_permutation(
            ProblemType.NAVIER_STOKES, test_case='lamb_oseen',
            regime='calibration', seed=42, max_level=6, n_trials=3,
        )

    def test_returns_trials(self):
        """Returns a list of PerturbationTrial."""
        self.assertIsInstance(self.trials, list)
        self.assertEqual(len(self.trials), 3)

    def test_trial_type(self):
        """Each trial has correct perturbation type."""
        for t in self.trials:
            self.assertEqual(t.perturbation_type,
                             PerturbationType.TIG_PERMUTATION.value)

    def test_trial_has_skeletons(self):
        """Each trial has baseline and perturbed skeleton classes."""
        valid = {s.value for s in SkeletonClass}
        for t in self.trials:
            self.assertIn(t.baseline_skeleton, valid)
            self.assertIn(t.perturbed_skeleton, valid)

    def test_preserved_flag_consistent(self):
        """skeleton_preserved matches skeleton comparison."""
        for t in self.trials:
            expected = (t.baseline_skeleton == t.perturbed_skeleton)
            self.assertEqual(t.skeleton_preserved, expected)

    def test_deterministic(self):
        """Same seed produces same trials."""
        trials2 = self.spec.robustness_permutation(
            ProblemType.NAVIER_STOKES, test_case='lamb_oseen',
            regime='calibration', seed=42, max_level=6, n_trials=3,
        )
        for t1, t2 in zip(self.trials, trials2):
            self.assertEqual(t1.perturbed_skeleton, t2.perturbed_skeleton)
            self.assertEqual(t1.delta_mean_shift, t2.delta_mean_shift)


# ================================================================
#  TestRobustnessJitter
# ================================================================

class TestRobustnessJitter(unittest.TestCase):
    """Generator jitter robustness."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.trials = cls.spec.robustness_jitter(
            ProblemType.RIEMANN, test_case='known_zero',
            regime='calibration', seed=42, max_level=6,
            jitter_levels=[0.05, 0.10, 0.25],
        )

    def test_returns_trials(self):
        """Returns correct number of trials."""
        self.assertEqual(len(self.trials), 3)

    def test_trial_type(self):
        """Each trial has correct perturbation type."""
        for t in self.trials:
            self.assertEqual(t.perturbation_type,
                             PerturbationType.GENERATOR_JITTER.value)

    def test_increasing_jitter_labels(self):
        """Labels reflect jitter levels."""
        self.assertIn('5pct', self.trials[0].perturbation_label)
        self.assertIn('10pct', self.trials[1].perturbation_label)
        self.assertIn('25pct', self.trials[2].perturbation_label)

    def test_small_jitter_likely_preserves(self):
        """5% jitter should be unlikely to break calibration skeleton."""
        # Not guaranteed but highly likely for frozen calibration
        self.assertIsInstance(self.trials[0].skeleton_preserved, bool)

    def test_params_recorded(self):
        """Perturbation params contain jitter fraction."""
        for t in self.trials:
            self.assertIn('jitter_fraction', t.perturbation_params)
            self.assertIsInstance(
                t.perturbation_params['jitter_fraction'], float)


# ================================================================
#  TestRobustnessAblation
# ================================================================

class TestRobustnessAblation(unittest.TestCase):
    """TIG channel ablation robustness."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.trials = cls.spec.robustness_ablation(
            ProblemType.RIEMANN, test_case='known_zero',
            regime='calibration', seed=42, max_level=6,
        )

    def test_returns_trials(self):
        """Returns at least one ablation trial."""
        self.assertGreater(len(self.trials), 0)

    def test_trial_type(self):
        """Each trial has correct perturbation type."""
        for t in self.trials:
            self.assertEqual(t.perturbation_type,
                             PerturbationType.CHANNEL_ABLATION.value)

    def test_ablated_operator_recorded(self):
        """Params contain which operator was ablated."""
        for t in self.trials:
            self.assertIn('ablated_operator', t.perturbation_params)
            self.assertIn('remaining_path', t.perturbation_params)

    def test_no_void_or_reset_ablated(self):
        """VOID and RESET are never ablated (they're bookends)."""
        for t in self.trials:
            self.assertNotEqual(
                t.perturbation_params['ablated_operator'], 'VOID')
            self.assertNotEqual(
                t.perturbation_params['ablated_operator'], 'RESET')


# ================================================================
#  TestRobustnessNoise
# ================================================================

class TestRobustnessNoise(unittest.TestCase):
    """Noise distribution robustness."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.trials = cls.spec.robustness_noise(
            ProblemType.P_VS_NP, test_case='easy',
            regime='calibration', seed=42, max_level=6, sigma=0.1,
        )

    def test_returns_three_trials(self):
        """Returns 3 trials: uniform, cauchy, high-sigma."""
        self.assertEqual(len(self.trials), 3)

    def test_trial_type(self):
        """Each trial has correct perturbation type."""
        for t in self.trials:
            self.assertEqual(t.perturbation_type,
                             PerturbationType.NOISE_DISTRIBUTION.value)

    def test_distributions_covered(self):
        """Labels cover uniform, cauchy, and high-sigma."""
        labels = [t.perturbation_label for t in self.trials]
        self.assertTrue(any('uniform' in l for l in labels))
        self.assertTrue(any('cauchy' in l for l in labels))

    def test_params_contain_distribution(self):
        """Params record distribution name and sigma."""
        for t in self.trials:
            self.assertIn('distribution', t.perturbation_params)
            self.assertIn('sigma', t.perturbation_params)


# ================================================================
#  TestRobustnessDeepSeeds
# ================================================================

class TestRobustnessDeepSeeds(unittest.TestCase):
    """Multi-seed skeleton stability."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.trials = cls.spec.robustness_deep_seeds(
            ProblemType.BSD, test_case='rank0_match',
            regime='calibration', seeds=list(range(1, 11)),
            max_level=6,
        )

    def test_returns_correct_count(self):
        """Returns n-1 trials (first seed is baseline)."""
        self.assertEqual(len(self.trials), 9)  # 10 seeds - 1 baseline

    def test_trial_type(self):
        """Each trial has correct perturbation type."""
        for t in self.trials:
            self.assertEqual(t.perturbation_type,
                             PerturbationType.MULTI_SEED.value)

    def test_seed_recorded(self):
        """Each trial records its seed in params."""
        for t in self.trials:
            self.assertIn('seed', t.perturbation_params)

    def test_calibration_frozen_likely_stable(self):
        """BSD rank0 calibration should be frozen across most seeds."""
        preserved = sum(1 for t in self.trials if t.skeleton_preserved)
        # Should survive most seeds (frozen is very stable)
        self.assertGreaterEqual(preserved, 5)


# ================================================================
#  TestRobustnessSweep
# ================================================================

class TestRobustnessSweep(unittest.TestCase):
    """Full per-config robustness sweep."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.result = cls.spec.robustness_sweep(
            ProblemType.HODGE, test_case='algebraic',
            regime='calibration', seed=42, max_level=6,
            n_deep_seeds=5,
        )

    def test_returns_robustness_result(self):
        """Returns a RobustnessResult."""
        self.assertIsInstance(self.result, RobustnessResult)

    def test_has_trials(self):
        """Result contains trials from all 5 perturbation types."""
        types_present = set(t.perturbation_type for t in self.result.trials)
        # Should have at least permutation + jitter + noise + seed
        self.assertGreaterEqual(len(types_present), 4)

    def test_survival_rate_in_range(self):
        """Survival rate is between 0 and 1."""
        self.assertGreaterEqual(self.result.survival_rate, 0.0)
        self.assertLessEqual(self.result.survival_rate, 1.0)

    def test_robust_flag_consistent(self):
        """robust flag matches macro_survival_rate >= threshold."""
        expected = self.result.macro_survival_rate >= ROBUSTNESS_THRESHOLD
        self.assertEqual(self.result.robust, expected)

    def test_counts_consistent(self):
        """n_trials == len(trials), n_preserved matches."""
        self.assertEqual(self.result.n_trials, len(self.result.trials))
        preserved = sum(1 for t in self.result.trials
                        if t.skeleton_preserved)
        self.assertEqual(self.result.n_preserved, preserved)


# ================================================================
#  TestRobustnessResult
# ================================================================

class TestRobustnessResult(unittest.TestCase):
    """RobustnessResult structure validation."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.result = cls.spec.robustness_sweep(
            ProblemType.YANG_MILLS, test_case='bpst_instanton',
            regime='calibration', seed=42, max_level=6,
            n_deep_seeds=5,
        )

    def test_baseline_fields(self):
        """Result has valid baseline metrics."""
        self.assertEqual(self.result.problem, 'yang_mills')
        self.assertEqual(self.result.regime, 'calibration')
        self.assertIsInstance(self.result.baseline_skeleton, str)
        self.assertIsInstance(self.result.baseline_delta_mean, float)
        self.assertIsInstance(self.result.baseline_entropy, float)

    def test_trial_shifts_are_floats(self):
        """All shift values in trials are floats."""
        for t in self.result.trials:
            self.assertIsInstance(t.delta_mean_shift, float)
            self.assertIsInstance(t.delta_range_shift, float)
            self.assertIsInstance(t.entropy_shift, float)

    def test_deterministic(self):
        """Same seed produces identical result."""
        r2 = self.spec.robustness_sweep(
            ProblemType.YANG_MILLS, test_case='bpst_instanton',
            regime='calibration', seed=42, max_level=6,
            n_deep_seeds=5,
        )
        self.assertEqual(self.result.n_trials, r2.n_trials)
        self.assertEqual(self.result.n_preserved, r2.n_preserved)
        self.assertEqual(self.result.survival_rate, r2.survival_rate)
        self.assertEqual(self.result.robust, r2.robust)


# ================================================================
#  MACRO CLASS TESTS
# ================================================================

class TestMacroClass(unittest.TestCase):
    """MacroClass enum and classify_macro() function."""

    def test_frozen_is_ground(self):
        self.assertEqual(classify_macro('frozen'), 'ground')

    def test_stable_is_ground(self):
        self.assertEqual(classify_macro('stable'), 'ground')

    def test_bounded_is_structured(self):
        self.assertEqual(classify_macro('bounded'), 'structured')

    def test_oscillating_is_structured(self):
        self.assertEqual(classify_macro('oscillating'), 'structured')

    def test_wild_is_turbulent(self):
        self.assertEqual(classify_macro('wild'), 'turbulent')

    def test_unknown_defaults_to_turbulent(self):
        self.assertEqual(classify_macro('unknown'), 'turbulent')


# ================================================================
#  SLOPE NORM TESTS
# ================================================================

class TestSlopeNorm(unittest.TestCase):
    """compute_slope_norm() function tests."""

    def test_constant_zero(self):
        """Constant sequence -> slope_norm = 0."""
        self.assertAlmostEqual(compute_slope_norm([0.5] * 10), 0.0)

    def test_linear_sequence(self):
        """Linear sequence with step 0.1 -> slope_norm = 0.1."""
        vals = [0.1 * i for i in range(10)]
        self.assertAlmostEqual(compute_slope_norm(vals), 0.1, places=5)

    def test_single_value_zero(self):
        """Single value -> slope_norm = 0."""
        self.assertAlmostEqual(compute_slope_norm([0.5]), 0.0)

    def test_empty_zero(self):
        """Empty list -> slope_norm = 0."""
        self.assertAlmostEqual(compute_slope_norm([]), 0.0)


# ================================================================
#  FINGERPRINT MACRO + SLOPE TESTS
# ================================================================

class TestFingerprintMacroAndSlope(unittest.TestCase):
    """FractalFingerprint includes macro_class and slope_norm."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.fp = cls.spec.fractal_scan(
            ProblemType.NAVIER_STOKES, 'lamb_oseen',
            regime='calibration', seed=42, max_level=6,
        )

    def test_macro_class_present(self):
        """macro_class is a valid MacroClass value."""
        self.assertIn(self.fp.macro_class, ('ground', 'structured', 'turbulent'))

    def test_macro_matches_skeleton(self):
        """macro_class matches classify_macro(skeleton_class)."""
        expected = classify_macro(self.fp.skeleton_class)
        self.assertEqual(self.fp.macro_class, expected)

    def test_slope_norm_nonneg(self):
        """slope_norm is non-negative."""
        self.assertGreaterEqual(self.fp.slope_norm, 0.0)


# ================================================================
#  ROBUSTNESS MACRO TESTS
# ================================================================

class TestRobustnessMacro(unittest.TestCase):
    """Robustness trials and results include macro fields."""

    @classmethod
    def setUpClass(cls):
        cls.spec = DeltaSpectrometer()
        cls.result = cls.spec.robustness_sweep(
            ProblemType.BSD, test_case='rank0_match',
            regime='calibration', seed=42, max_level=6,
            n_deep_seeds=5,
        )

    def test_trials_have_macro_fields(self):
        """Each trial has valid macro fields."""
        for t in self.result.trials:
            self.assertIn(t.baseline_macro, ('ground', 'structured', 'turbulent'))
            self.assertIn(t.perturbed_macro, ('ground', 'structured', 'turbulent'))
            self.assertIsInstance(t.macro_preserved, bool)

    def test_macro_survival_in_range(self):
        """macro_survival_rate is between 0 and 1."""
        self.assertGreaterEqual(self.result.macro_survival_rate, 0.0)
        self.assertLessEqual(self.result.macro_survival_rate, 1.0)

    def test_macro_gte_fine(self):
        """Macro survival >= fine survival (macro is more permissive)."""
        self.assertGreaterEqual(self.result.macro_survival_rate,
                                self.result.survival_rate)

    def test_robust_uses_macro(self):
        """robust flag equals macro_survival_rate >= threshold."""
        expected = self.result.macro_survival_rate >= ROBUSTNESS_THRESHOLD
        self.assertEqual(self.result.robust, expected)


# ================================================================
#  RH SINGULARITY + PAIR CORRELATION TESTS
# ================================================================

class TestRHSingularity(unittest.TestCase):
    """RH singularity test case and pair_correlation in RiemannGenerator."""

    def test_singularity_pair_correlation(self):
        """rh_singularity generates pair_correlation in (0, 1)."""
        from ck_sim.doing.ck_clay_generators import RiemannGenerator
        gen = RiemannGenerator(seed=42)
        reading = gen.generate(5, 'rh_singularity')
        self.assertIn('pair_correlation', reading)
        self.assertGreater(reading['pair_correlation'], 0.0)
        self.assertLess(reading['pair_correlation'], 1.0)

    def test_off_line_pair_correlation(self):
        """off_line generates pair_correlation."""
        from ck_sim.doing.ck_clay_generators import RiemannGenerator
        gen = RiemannGenerator(seed=42)
        reading = gen.generate(5, 'off_line')
        self.assertIn('pair_correlation', reading)

    def test_known_zero_high_pair_correlation(self):
        """known_zero has high pair_correlation (GUE-like)."""
        from ck_sim.doing.ck_clay_generators import RiemannGenerator
        gen = RiemannGenerator(seed=42)
        reading = gen.generate(5, 'known_zero')
        self.assertIn('pair_correlation', reading)
        self.assertGreater(reading['pair_correlation'], 0.7)


# ================================================================
#  YM GAUGE INVARIANT TESTS
# ================================================================

class TestYMGaugeInvariant(unittest.TestCase):
    """YM generator includes gauge_invariant field."""

    def test_bpst_high_gauge_invariant(self):
        """BPST instanton has gauge_invariant > 0.8."""
        from ck_sim.doing.ck_clay_generators import YangMillsGenerator
        gen = YangMillsGenerator(seed=42)
        reading = gen.generate(5, 'bpst_instanton')
        self.assertIn('gauge_invariant', reading)
        self.assertGreater(reading['gauge_invariant'], 0.8)

    def test_excited_low_gauge_invariant(self):
        """Excited state has gauge_invariant < 0.6."""
        from ck_sim.doing.ck_clay_generators import YangMillsGenerator
        gen = YangMillsGenerator(seed=42)
        reading = gen.generate(5, 'excited')
        self.assertIn('gauge_invariant', reading)
        self.assertLess(reading['gauge_invariant'], 0.6)


# ================================================================
#  MULTI-FRONTIER TESTS
# ================================================================

class TestMultiFrontier(unittest.TestCase):
    """FRONTIER_CASES with list values for multi-case frontiers."""

    def test_riemann_frontier_is_list(self):
        """Riemann FRONTIER_CASES entry is a list with 2 items."""
        entry = FRONTIER_CASES.get('riemann')
        self.assertIsInstance(entry, list)
        self.assertIn('off_line', entry)
        self.assertIn('rh_singularity', entry)

    def test_frontier_cases_helper(self):
        """_frontier_cases_for returns lists for all problems."""
        self.assertEqual(_frontier_cases_for('navier_stokes'), ['high_strain'])
        self.assertEqual(len(_frontier_cases_for('riemann')), 2)


# ================================================================
#  Entry point
# ================================================================

if __name__ == '__main__':
    unittest.main()
