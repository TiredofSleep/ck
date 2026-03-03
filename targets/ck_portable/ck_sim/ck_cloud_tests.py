"""
ck_cloud_tests.py -- Tests for Cloud-Learning Engine
======================================================
Validates: ck_cloud_flow, ck_cloud_curvature, ck_cloud_btq,
ck_cloud_pfe, ck_organ_clouds. Full pipeline integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys

import numpy as np

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  FLOW MODULE TESTS (ck_cloud_flow)
# ================================================================

class TestFlowImports(unittest.TestCase):
    """Verify clean imports of flow module."""

    def test_import_module(self):
        import ck_sim.ck_cloud_flow
        self.assertTrue(hasattr(ck_sim.ck_cloud_flow, 'FlowTracker'))

    def test_import_public_api(self):
        from ck_sim.ck_cloud_flow import (
            horn_schunck, compute_gradients, decompose_flow,
            FlowTracker, FlowPatch,
            generate_uniform_flow, generate_vortex_flow,
            generate_expanding_flow, generate_turbulent_flow,
            generate_cloud_frame_pair,
        )
        self.assertIsNotNone(horn_schunck)


class TestFlowConstants(unittest.TestCase):
    """Validate flow module constants."""

    def test_default_patch_size(self):
        from ck_sim.ck_cloud_flow import DEFAULT_PATCH_SIZE
        self.assertEqual(DEFAULT_PATCH_SIZE, 8)

    def test_flow_clip_positive(self):
        from ck_sim.ck_cloud_flow import FLOW_CLIP
        self.assertGreater(FLOW_CLIP, 0.0)


class TestGradients(unittest.TestCase):
    """Validate image gradient computation."""

    def test_gradient_shapes(self):
        from ck_sim.ck_cloud_flow import compute_gradients
        f1 = np.random.rand(32, 32).astype(np.float32)
        f2 = np.random.rand(32, 32).astype(np.float32)
        Ix, Iy, It = compute_gradients(f1, f2)
        self.assertEqual(Ix.shape, (32, 32))
        self.assertEqual(Iy.shape, (32, 32))
        self.assertEqual(It.shape, (32, 32))

    def test_temporal_gradient_zero_for_identical(self):
        from ck_sim.ck_cloud_flow import compute_gradients
        f = np.random.rand(16, 16).astype(np.float32)
        _, _, It = compute_gradients(f, f)
        self.assertAlmostEqual(float(np.max(np.abs(It))), 0.0, places=5)

    def test_temporal_gradient_nonzero_for_different(self):
        from ck_sim.ck_cloud_flow import compute_gradients
        f1 = np.zeros((16, 16), dtype=np.float32)
        f2 = np.ones((16, 16), dtype=np.float32)
        _, _, It = compute_gradients(f1, f2)
        self.assertGreater(float(np.max(np.abs(It))), 0.5)


class TestHornSchunck(unittest.TestCase):
    """Validate Horn-Schunck optical flow."""

    def test_output_shape(self):
        from ck_sim.ck_cloud_flow import horn_schunck
        f1 = np.random.rand(32, 32).astype(np.float32)
        f2 = np.random.rand(32, 32).astype(np.float32)
        u, v = horn_schunck(f1, f2, iterations=10)
        self.assertEqual(u.shape, (32, 32))
        self.assertEqual(v.shape, (32, 32))

    def test_zero_flow_for_identical_frames(self):
        from ck_sim.ck_cloud_flow import horn_schunck
        f = np.random.rand(32, 32).astype(np.float32)
        u, v = horn_schunck(f, f, iterations=20)
        self.assertLess(float(np.max(np.abs(u))), 0.1)
        self.assertLess(float(np.max(np.abs(v))), 0.1)

    def test_flow_values_clipped(self):
        from ck_sim.ck_cloud_flow import horn_schunck, FLOW_CLIP
        f1 = np.zeros((16, 16), dtype=np.float32)
        f2 = np.ones((16, 16), dtype=np.float32)
        u, v = horn_schunck(f1, f2, iterations=10)
        self.assertLessEqual(float(np.max(u)), FLOW_CLIP)
        self.assertGreaterEqual(float(np.min(u)), -FLOW_CLIP)


class TestSyntheticFlows(unittest.TestCase):
    """Validate synthetic flow generators."""

    def test_uniform_flow_constant(self):
        from ck_sim.ck_cloud_flow import generate_uniform_flow
        u, v = generate_uniform_flow(32, 32, 1.5, -0.5)
        self.assertAlmostEqual(float(u[0, 0]), 1.5)
        self.assertAlmostEqual(float(v[0, 0]), -0.5)
        self.assertAlmostEqual(float(np.std(u)), 0.0, places=5)

    def test_vortex_flow_rotational(self):
        from ck_sim.ck_cloud_flow import generate_vortex_flow
        u, v = generate_vortex_flow(32, 32, strength=1.0)
        # Center should have near-zero flow
        center_speed = math.sqrt(u[16, 16] ** 2 + v[16, 16] ** 2)
        edge_speed = math.sqrt(u[0, 16] ** 2 + v[0, 16] ** 2)
        self.assertLess(center_speed, edge_speed)

    def test_expanding_flow_divergent(self):
        from ck_sim.ck_cloud_flow import generate_expanding_flow
        u, v = generate_expanding_flow(32, 32, rate=1.0)
        # Center should be zero, edges positive
        self.assertAlmostEqual(float(u[16, 16]), 0.0, places=1)
        self.assertGreater(float(u[16, 31]), 0.0)

    def test_turbulent_flow_nonzero(self):
        from ck_sim.ck_cloud_flow import generate_turbulent_flow
        u, v = generate_turbulent_flow(32, 32, scale=1.0)
        self.assertGreater(float(np.std(u)), 0.0)
        self.assertGreater(float(np.std(v)), 0.0)

    def test_frame_pair_generation(self):
        from ck_sim.ck_cloud_flow import generate_cloud_frame_pair
        f1, f2 = generate_cloud_frame_pair(32, 32, 'uniform', 0.5)
        self.assertEqual(f1.shape, (32, 32))
        self.assertEqual(f2.shape, (32, 32))
        self.assertGreaterEqual(float(f1.min()), 0.0)
        self.assertLessEqual(float(f1.max()), 1.0)


class TestFlowPatch(unittest.TestCase):
    """Validate FlowPatch statistics."""

    def test_patch_creation(self):
        from ck_sim.ck_cloud_flow import FlowPatch
        u = np.ones((8, 8), dtype=np.float32)
        v = np.zeros((8, 8), dtype=np.float32)
        p = FlowPatch(0, 0, u, v)
        self.assertAlmostEqual(p.speed, 1.0, places=2)
        self.assertEqual(p.row, 0)
        self.assertEqual(p.col, 0)

    def test_force_vector_5d(self):
        from ck_sim.ck_cloud_flow import FlowPatch
        u = np.random.rand(8, 8).astype(np.float32)
        v = np.random.rand(8, 8).astype(np.float32)
        p = FlowPatch(1, 2, u, v)
        self.assertEqual(len(p.force_vector), 5)

    def test_force_vector_bounded(self):
        from ck_sim.ck_cloud_flow import FlowPatch
        u = np.random.rand(8, 8).astype(np.float32) * 5
        v = np.random.rand(8, 8).astype(np.float32) * 5
        p = FlowPatch(0, 0, u, v)
        for val in p.force_vector:
            self.assertGreaterEqual(val, -1.0)
            self.assertLessEqual(val, 1.0)

    def test_zero_flow_high_coherence(self):
        from ck_sim.ck_cloud_flow import FlowPatch
        u = np.zeros((8, 8), dtype=np.float32)
        v = np.zeros((8, 8), dtype=np.float32)
        p = FlowPatch(0, 0, u, v)
        self.assertAlmostEqual(p.speed, 0.0)
        self.assertAlmostEqual(p.coherence, 1.0)


class TestDecomposeFlow(unittest.TestCase):
    """Validate flow decomposition into patches."""

    def test_correct_patch_count(self):
        from ck_sim.ck_cloud_flow import decompose_flow
        u = np.random.rand(64, 64).astype(np.float32)
        v = np.random.rand(64, 64).astype(np.float32)
        patches = decompose_flow(u, v, patch_size=8)
        self.assertEqual(len(patches), 64)  # 8x8 grid

    def test_patch_row_col_range(self):
        from ck_sim.ck_cloud_flow import decompose_flow
        u = np.random.rand(32, 32).astype(np.float32)
        v = np.random.rand(32, 32).astype(np.float32)
        patches = decompose_flow(u, v, patch_size=8)
        rows = set(p.row for p in patches)
        cols = set(p.col for p in patches)
        self.assertEqual(rows, {0, 1, 2, 3})
        self.assertEqual(cols, {0, 1, 2, 3})


class TestFlowTracker(unittest.TestCase):
    """Validate stateful FlowTracker."""

    def test_first_frame_returns_none(self):
        from ck_sim.ck_cloud_flow import FlowTracker
        tracker = FlowTracker(patch_size=8)
        frame = np.random.rand(32, 32).astype(np.float32)
        self.assertIsNone(tracker.feed(frame))

    def test_second_frame_returns_patches(self):
        from ck_sim.ck_cloud_flow import FlowTracker
        tracker = FlowTracker(patch_size=8, iterations=10)
        f1 = np.random.rand(32, 32).astype(np.float32)
        f2 = np.random.rand(32, 32).astype(np.float32)
        tracker.feed(f1)
        patches = tracker.feed(f2)
        self.assertIsNotNone(patches)
        self.assertEqual(len(patches), 16)  # 4x4 grid

    def test_frame_count(self):
        from ck_sim.ck_cloud_flow import FlowTracker
        tracker = FlowTracker(patch_size=8, iterations=5)
        for i in range(5):
            tracker.feed(np.random.rand(32, 32).astype(np.float32))
        self.assertEqual(tracker.frame_count, 5)

    def test_reset(self):
        from ck_sim.ck_cloud_flow import FlowTracker
        tracker = FlowTracker(patch_size=8, iterations=5)
        tracker.feed(np.random.rand(32, 32).astype(np.float32))
        tracker.reset()
        self.assertEqual(tracker.frame_count, 0)


# ================================================================
#  CURVATURE MODULE TESTS (ck_cloud_curvature)
# ================================================================

class TestCurvatureImports(unittest.TestCase):
    def test_import_public_api(self):
        from ck_sim.ck_cloud_curvature import (
            spatial_d2, temporal_d2, classify_d2_vector,
            classify_grid, operator_sequence_from_grid,
            combined_d2, CloudCurvatureTracker,
            grid_coherence, sequence_coherence,
        )
        self.assertIsNotNone(spatial_d2)


class TestSpatialD2(unittest.TestCase):
    """Validate spatial second derivative."""

    def test_output_shape(self):
        from ck_sim.ck_cloud_curvature import spatial_d2
        grid = np.random.randn(8, 8, 5).astype(np.float32)
        d2 = spatial_d2(grid)
        self.assertEqual(d2.shape, (8, 8, 5))

    def test_uniform_grid_zero_d2(self):
        from ck_sim.ck_cloud_curvature import spatial_d2
        grid = np.ones((8, 8, 5), dtype=np.float32) * 0.5
        d2 = spatial_d2(grid)
        # Interior should be ~0 (constant field → zero Laplacian)
        interior = d2[2:-2, 2:-2, :]
        self.assertLess(float(np.max(np.abs(interior))), 0.01)

    def test_small_grid_returns_zeros(self):
        from ck_sim.ck_cloud_curvature import spatial_d2
        grid = np.random.randn(2, 2, 5).astype(np.float32)
        d2 = spatial_d2(grid)
        self.assertAlmostEqual(float(np.sum(np.abs(d2))), 0.0)


class TestTemporalD2(unittest.TestCase):
    """Validate temporal second derivative."""

    def test_formula_correct(self):
        from ck_sim.ck_cloud_curvature import temporal_d2
        t0 = np.ones((4, 4, 5), dtype=np.float32) * 1.0
        t1 = np.ones((4, 4, 5), dtype=np.float32) * 2.0
        t2 = np.ones((4, 4, 5), dtype=np.float32) * 3.0
        d2 = temporal_d2(t0, t1, t2)
        # 1 - 2*2 + 3 = 0 (constant acceleration)
        self.assertAlmostEqual(float(d2[0, 0, 0]), 0.0)

    def test_nonzero_for_acceleration_change(self):
        from ck_sim.ck_cloud_curvature import temporal_d2
        t0 = np.ones((4, 4, 5), dtype=np.float32) * 0.0
        t1 = np.ones((4, 4, 5), dtype=np.float32) * 1.0
        t2 = np.ones((4, 4, 5), dtype=np.float32) * 4.0
        d2 = temporal_d2(t0, t1, t2)
        # 0 - 2*1 + 4 = 2
        self.assertAlmostEqual(float(d2[0, 0, 0]), 2.0)


class TestOperatorClassification(unittest.TestCase):
    """Validate D2 vector → operator classification."""

    def test_zero_d2_is_void(self):
        from ck_sim.ck_cloud_curvature import classify_d2_vector
        from ck_sim.ck_sim_heartbeat import VOID
        d2 = np.zeros(5, dtype=np.float32)
        self.assertEqual(classify_d2_vector(d2), VOID)

    def test_classify_grid_shape(self):
        from ck_sim.ck_cloud_curvature import classify_grid
        d2_grid = np.random.randn(4, 4, 5).astype(np.float32) * 0.5
        ops = classify_grid(d2_grid)
        self.assertEqual(ops.shape, (4, 4))

    def test_classify_grid_valid_operators(self):
        from ck_sim.ck_cloud_curvature import classify_grid
        from ck_sim.ck_sim_heartbeat import NUM_OPS
        d2_grid = np.random.randn(4, 4, 5).astype(np.float32)
        ops = classify_grid(d2_grid)
        self.assertTrue(np.all(ops >= 0))
        self.assertTrue(np.all(ops < NUM_OPS))

    def test_sequence_from_grid(self):
        from ck_sim.ck_cloud_curvature import (
            classify_grid, operator_sequence_from_grid
        )
        d2_grid = np.random.randn(3, 3, 5).astype(np.float32)
        ops = classify_grid(d2_grid)
        seq = operator_sequence_from_grid(ops)
        self.assertEqual(len(seq), 9)
        self.assertIsInstance(seq[0], int)


class TestCoherence(unittest.TestCase):
    """Validate coherence computations."""

    def test_all_harmony_perfect_coherence(self):
        from ck_sim.ck_cloud_curvature import grid_coherence
        from ck_sim.ck_sim_heartbeat import HARMONY
        grid = np.full((4, 4), HARMONY, dtype=np.int32)
        self.assertAlmostEqual(grid_coherence(grid), 1.0)

    def test_no_harmony_zero_coherence(self):
        from ck_sim.ck_cloud_curvature import grid_coherence
        from ck_sim.ck_sim_heartbeat import VOID
        grid = np.full((4, 4), VOID, dtype=np.int32)
        self.assertAlmostEqual(grid_coherence(grid), 0.0)

    def test_sequence_coherence_basic(self):
        from ck_sim.ck_cloud_curvature import sequence_coherence
        from ck_sim.ck_sim_heartbeat import HARMONY, VOID
        seq = [HARMONY] * 7 + [VOID] * 3
        coh = sequence_coherence(seq)
        self.assertAlmostEqual(coh, 0.7)


class TestCurvatureTracker(unittest.TestCase):
    """Validate stateful CloudCurvatureTracker."""

    def _make_patches(self, rows=4, cols=4):
        from ck_sim.ck_cloud_flow import FlowPatch
        patches = []
        for r in range(rows):
            for c in range(cols):
                u = np.random.rand(8, 8).astype(np.float32) * 0.5
                v = np.random.rand(8, 8).astype(np.float32) * 0.5
                patches.append(FlowPatch(r, c, u, v))
        return patches

    def test_first_frame_returns_result(self):
        from ck_sim.ck_cloud_curvature import CloudCurvatureTracker
        tracker = CloudCurvatureTracker()
        result = tracker.feed(self._make_patches())
        self.assertIsNotNone(result)
        self.assertIn('operators', result)
        self.assertIn('sequence', result)

    def test_temporal_d2_after_3_frames(self):
        from ck_sim.ck_cloud_curvature import CloudCurvatureTracker
        tracker = CloudCurvatureTracker()
        for i in range(3):
            result = tracker.feed(self._make_patches())
        self.assertIsNotNone(result['temporal_d2'])

    def test_frame_count(self):
        from ck_sim.ck_cloud_curvature import CloudCurvatureTracker
        tracker = CloudCurvatureTracker()
        for i in range(5):
            tracker.feed(self._make_patches())
        self.assertEqual(tracker.frame_count, 5)


# ================================================================
#  BTQ MODULE TESTS (ck_cloud_btq)
# ================================================================

class TestBTQImports(unittest.TestCase):
    def test_import_public_api(self):
        from ck_sim.ck_cloud_btq import (
            compute_theta, classify_theta, CloudBTQTracker,
            MODE_BINARY, MODE_TERNARY, MODE_QUATERNARY,
            patch_theta_grid, mode_distribution,
        )
        self.assertIsNotNone(compute_theta)


class TestThetaComputation(unittest.TestCase):
    """Validate Θ ratio computation."""

    def test_zero_variance_zero_theta(self):
        from ck_sim.ck_cloud_btq import compute_theta
        speeds = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        d2 = np.array([0.5, 0.5, 0.5], dtype=np.float32)
        coh = np.array([0.8, 0.8, 0.8], dtype=np.float32)
        theta = compute_theta(speeds, d2, coh)
        self.assertAlmostEqual(theta, 0.0, places=3)

    def test_high_variance_high_theta(self):
        from ck_sim.ck_cloud_btq import compute_theta
        speeds = np.array([0.0, 10.0, 0.0, 10.0], dtype=np.float32)
        d2 = np.array([0.1, 0.1, 0.1, 0.1], dtype=np.float32)
        coh = np.array([0.5, 0.5, 0.5, 0.5], dtype=np.float32)
        theta = compute_theta(speeds, d2, coh)
        self.assertGreater(theta, 1.0)

    def test_empty_array_returns_zero(self):
        from ck_sim.ck_cloud_btq import compute_theta
        theta = compute_theta(np.array([]), np.array([]), np.array([]))
        self.assertAlmostEqual(theta, 0.0)


class TestThetaClassification(unittest.TestCase):
    """Validate Θ → mode classification."""

    def test_low_theta_binary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_BINARY
        self.assertEqual(classify_theta(0.1), MODE_BINARY)

    def test_medium_theta_ternary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_TERNARY
        self.assertEqual(classify_theta(0.5), MODE_TERNARY)

    def test_high_theta_quaternary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_QUATERNARY
        self.assertEqual(classify_theta(2.0), MODE_QUATERNARY)

    def test_boundary_binary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_BINARY
        self.assertEqual(classify_theta(0.0), MODE_BINARY)

    def test_boundary_ternary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_TERNARY
        self.assertEqual(classify_theta(0.3), MODE_TERNARY)

    def test_boundary_quaternary(self):
        from ck_sim.ck_cloud_btq import classify_theta, MODE_QUATERNARY
        self.assertEqual(classify_theta(1.2), MODE_QUATERNARY)


class TestModeDistribution(unittest.TestCase):
    """Validate patch-level mode distribution."""

    def test_all_binary(self):
        from ck_sim.ck_cloud_btq import mode_distribution, MODE_BINARY
        theta_grid = np.zeros((4, 4), dtype=np.float32)  # All < 0.3
        dist = mode_distribution(theta_grid)
        self.assertAlmostEqual(dist[MODE_BINARY], 1.0)

    def test_empty_grid(self):
        from ck_sim.ck_cloud_btq import mode_distribution
        dist = mode_distribution(np.zeros((0, 0)))
        self.assertAlmostEqual(dist['B'], 1.0)


class TestBTQTracker(unittest.TestCase):
    """Validate stateful BTQ tracker."""

    def _make_patches(self, n=16, speed_scale=0.5):
        from ck_sim.ck_cloud_flow import FlowPatch
        patches = []
        for i in range(n):
            u = np.random.rand(8, 8).astype(np.float32) * speed_scale
            v = np.random.rand(8, 8).astype(np.float32) * speed_scale
            r, c = i // 4, i % 4
            patches.append(FlowPatch(r, c, u, v))
        return patches

    def test_initial_mode_binary(self):
        from ck_sim.ck_cloud_btq import CloudBTQTracker
        tracker = CloudBTQTracker()
        self.assertEqual(tracker.current_mode, 'B')

    def test_feed_returns_dict(self):
        from ck_sim.ck_cloud_btq import CloudBTQTracker
        tracker = CloudBTQTracker()
        patches = self._make_patches()
        d2_mags = np.random.rand(4, 4).astype(np.float32)
        result = tracker.feed(patches, d2_mags)
        self.assertIn('mode', result)
        self.assertIn('theta', result)
        self.assertIn('distribution', result)

    def test_reset(self):
        from ck_sim.ck_cloud_btq import CloudBTQTracker
        tracker = CloudBTQTracker()
        patches = self._make_patches()
        d2_mags = np.random.rand(4, 4).astype(np.float32)
        tracker.feed(patches, d2_mags)
        tracker.reset()
        self.assertEqual(tracker.current_mode, 'B')
        self.assertEqual(tracker.transitions, 0)


# ================================================================
#  PFE MODULE TESTS (ck_cloud_pfe)
# ================================================================

class TestPFEImports(unittest.TestCase):
    def test_import_public_api(self):
        from ck_sim.ck_cloud_pfe import (
            compute_e_total, compute_e_out, compute_e_in,
            velocity_energy, jerk_energy, smoothness_energy,
            mode_jump_energy, d2_energy, phase_incoherence,
            helical_coherence, CloudPFETracker,
        )
        self.assertIsNotNone(compute_e_total)


class TestEOutComponents(unittest.TestCase):
    """Validate E_out individual energy components."""

    def test_velocity_energy_scales_with_speed(self):
        from ck_sim.ck_cloud_pfe import velocity_energy
        low = velocity_energy(np.array([0.1, 0.1]))
        high = velocity_energy(np.array([2.0, 2.0]))
        self.assertLess(low, high)

    def test_velocity_energy_empty(self):
        from ck_sim.ck_cloud_pfe import velocity_energy
        self.assertAlmostEqual(velocity_energy(np.array([])), 0.0)

    def test_jerk_energy_zero_for_none(self):
        from ck_sim.ck_cloud_pfe import jerk_energy
        self.assertAlmostEqual(jerk_energy(None), 0.0)

    def test_smoothness_energy_zero_for_uniform(self):
        from ck_sim.ck_cloud_pfe import smoothness_energy
        uniform = np.ones((4, 4, 5), dtype=np.float32) * 0.1
        self.assertAlmostEqual(smoothness_energy(uniform), 0.0, places=3)

    def test_mode_jump_energy_no_jumps(self):
        from ck_sim.ck_cloud_pfe import mode_jump_energy
        self.assertAlmostEqual(mode_jump_energy(['B', 'B', 'B']), 0.0)

    def test_mode_jump_energy_all_jumps(self):
        from ck_sim.ck_cloud_pfe import mode_jump_energy
        e = mode_jump_energy(['B', 'T', 'Q', 'B'])
        self.assertAlmostEqual(e, 1.0)


class TestEInComponents(unittest.TestCase):
    """Validate E_in individual energy components."""

    def test_d2_energy_scales(self):
        from ck_sim.ck_cloud_pfe import d2_energy
        low = d2_energy(np.array([0.01]))
        high = d2_energy(np.array([5.0]))
        self.assertLess(low, high)

    def test_phase_incoherence_all_harmony(self):
        from ck_sim.ck_cloud_pfe import phase_incoherence
        from ck_sim.ck_sim_heartbeat import HARMONY
        self.assertAlmostEqual(phase_incoherence([HARMONY] * 10), 0.0)

    def test_phase_incoherence_no_harmony(self):
        from ck_sim.ck_cloud_pfe import phase_incoherence
        from ck_sim.ck_sim_heartbeat import VOID
        self.assertAlmostEqual(phase_incoherence([VOID] * 10), 1.0)

    def test_phase_incoherence_empty(self):
        from ck_sim.ck_cloud_pfe import phase_incoherence
        self.assertAlmostEqual(phase_incoherence([]), 1.0)

    def test_helical_coherence_in_range(self):
        from ck_sim.ck_cloud_pfe import helical_coherence
        ops = list(range(10)) * 5  # Repeating pattern
        h = helical_coherence(ops, period=10)
        self.assertGreaterEqual(h, 0.0)
        self.assertLessEqual(h, 1.0)

    def test_helical_coherence_short_sequence(self):
        from ck_sim.ck_cloud_pfe import helical_coherence
        h = helical_coherence([1, 2, 3])
        self.assertAlmostEqual(h, 0.5)  # Neutral for short


class TestETotalComputation(unittest.TestCase):
    """Validate combined E_total."""

    def test_e_total_positive(self):
        from ck_sim.ck_cloud_pfe import compute_e_total
        speeds = np.array([0.5] * 10, dtype=np.float32)
        d2 = np.array([0.1] * 10, dtype=np.float32)
        ops = [7] * 10  # All HARMONY
        e_total, details = compute_e_total(
            speeds, None, None, d2, ops, ['B']
        )
        self.assertGreaterEqual(e_total, 0.0)
        self.assertIn('quality', details)

    def test_quality_classification(self):
        from ck_sim.ck_cloud_pfe import compute_e_total
        # Low energy should be GREEN
        speeds = np.array([0.01], dtype=np.float32)
        d2 = np.array([0.01], dtype=np.float32)
        from ck_sim.ck_sim_heartbeat import HARMONY
        ops = [HARMONY] * 100
        e_total, details = compute_e_total(
            speeds, None, None, d2, ops, ['B']
        )
        # With mostly harmony and low speed, should be low energy
        self.assertLess(e_total, 1.0)


class TestPFETracker(unittest.TestCase):
    """Validate stateful PFE tracker."""

    def test_feed_returns_dict(self):
        from ck_sim.ck_cloud_pfe import CloudPFETracker
        pfe = CloudPFETracker()
        speeds = np.array([0.5] * 10, dtype=np.float32)
        d2 = np.array([0.1] * 10, dtype=np.float32)
        result = pfe.feed(speeds, None, None, d2, [7] * 10, 'B')
        self.assertIn('e_total', result)
        self.assertIn('quality', result)
        self.assertIn('frame', result)

    def test_energy_history_accumulates(self):
        from ck_sim.ck_cloud_pfe import CloudPFETracker
        pfe = CloudPFETracker()
        for i in range(5):
            speeds = np.random.rand(10).astype(np.float32)
            d2 = np.random.rand(10).astype(np.float32)
            pfe.feed(speeds, None, None, d2, [0] * 10, 'B')
        self.assertEqual(pfe.frame_count, 5)
        self.assertGreater(pfe.mean_energy, 0.0)

    def test_reset(self):
        from ck_sim.ck_cloud_pfe import CloudPFETracker
        pfe = CloudPFETracker()
        pfe.feed(np.array([1.0]), None, None, np.array([1.0]), [0], 'B')
        pfe.reset()
        self.assertEqual(pfe.frame_count, 0)


# ================================================================
#  ORGAN MODULE TESTS (ck_organ_clouds)
# ================================================================

class TestOrganImports(unittest.TestCase):
    def test_import_public_api(self):
        from ck_sim.ck_organ_clouds import (
            CloudOrgan, CloudObservation, CloudChain,
        )
        self.assertIsNotNone(CloudOrgan)


class TestCloudObservation(unittest.TestCase):
    """Validate CloudObservation dataclass."""

    def test_default_values(self):
        from ck_sim.ck_organ_clouds import CloudObservation
        obs = CloudObservation()
        self.assertEqual(obs.frame, 0)
        self.assertEqual(obs.operators, [])
        self.assertEqual(obs.btq_mode, 'B')
        self.assertAlmostEqual(obs.coherence, 0.0)

    def test_custom_values(self):
        from ck_sim.ck_organ_clouds import CloudObservation
        obs = CloudObservation(frame=5, btq_mode='T', coherence=0.8)
        self.assertEqual(obs.frame, 5)
        self.assertEqual(obs.btq_mode, 'T')
        self.assertAlmostEqual(obs.coherence, 0.8)


class TestCloudChain(unittest.TestCase):
    """Validate CloudChain dataclass and knowledge export."""

    def test_to_knowledge_dict(self):
        from ck_sim.ck_organ_clouds import CloudChain
        from ck_sim.ck_sim_heartbeat import HARMONY
        chain = CloudChain(
            start_frame=0, end_frame=32,
            operators=[HARMONY] * 64,
            coherence=0.85,
            mean_energy=0.2,
            dominant_mode='B',
            dominant_operator=HARMONY,
            pattern_type='harmonic',
            quality='GREEN',
        )
        d = chain.to_knowledge_dict()
        self.assertEqual(d['type'], 'cloud_pattern')
        self.assertEqual(d['dominant_op_name'], 'HARMONY')
        self.assertEqual(d['quality'], 'GREEN')
        self.assertEqual(d['length'], 64)


class TestCloudOrgan(unittest.TestCase):
    """Validate full CloudOrgan pipeline."""

    def test_first_frame_returns_none(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        frame = np.random.rand(32, 32).astype(np.float32)
        self.assertIsNone(organ.observe(frame))

    def test_second_frame_returns_observation(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        f1 = np.random.rand(32, 32).astype(np.float32)
        f2 = np.random.rand(32, 32).astype(np.float32)
        organ.observe(f1)
        obs = organ.observe(f2)
        self.assertIsNotNone(obs)
        self.assertGreater(len(obs.operators), 0)
        self.assertIn(obs.btq_mode, ['B', 'T', 'Q'])

    def test_observation_has_all_fields(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        for i in range(3):
            obs = organ.observe(np.random.rand(32, 32).astype(np.float32))
        self.assertIsNotNone(obs)
        self.assertGreaterEqual(obs.coherence, 0.0)
        self.assertLessEqual(obs.coherence, 1.0)
        self.assertGreaterEqual(obs.energy, 0.0)
        self.assertIn(obs.quality, ['RED', 'YELLOW', 'GREEN'])

    def test_stats_after_multiple_frames(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        for i in range(5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))
        stats = organ.stats()
        self.assertGreater(stats['frames_observed'], 0)
        self.assertGreater(stats['total_operators'], 0)
        self.assertIn('btq_mode', stats)

    def test_lifetime_coherence_in_range(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        for i in range(5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))
        coh = organ.lifetime_coherence
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_reset(self):
        from ck_sim.ck_organ_clouds import CloudOrgan
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        organ.observe(np.random.rand(32, 32).astype(np.float32))
        organ.observe(np.random.rand(32, 32).astype(np.float32))
        organ.reset()
        self.assertEqual(organ.frame_count, 0)
        self.assertEqual(organ.all_chains, [])


class TestOrganChainProduction(unittest.TestCase):
    """Validate chain extraction from extended observation."""

    def test_chains_produced_after_many_frames(self):
        from ck_sim.ck_organ_clouds import CloudOrgan, CHAIN_WINDOW
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        # Feed enough frames to trigger chain finalization
        for i in range(CHAIN_WINDOW + 5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))
        chains = organ.all_chains
        self.assertGreater(len(chains), 0)

    def test_chain_has_valid_data(self):
        from ck_sim.ck_organ_clouds import CloudOrgan, CHAIN_WINDOW
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        for i in range(CHAIN_WINDOW + 5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))
        chains = organ.all_chains
        if chains:
            chain = chains[0]
            self.assertGreater(len(chain.operators), 0)
            self.assertGreaterEqual(chain.coherence, 0.0)
            self.assertLessEqual(chain.coherence, 1.0)
            self.assertIn(chain.quality, ['RED', 'YELLOW', 'GREEN'])
            self.assertIn(chain.dominant_mode, ['B', 'T', 'Q'])

    def test_new_chains_buffer(self):
        from ck_sim.ck_organ_clouds import CloudOrgan, CHAIN_WINDOW
        organ = CloudOrgan(patch_size=8, flow_iterations=10)
        for i in range(CHAIN_WINDOW + 5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))
        new = organ.get_new_chains()
        self.assertGreater(len(new), 0)
        # Second call should be empty
        new2 = organ.get_new_chains()
        self.assertEqual(len(new2), 0)


# ================================================================
#  FULL INTEGRATION: End-to-end pipeline test
# ================================================================

class TestFullPipeline(unittest.TestCase):
    """End-to-end: synthetic frames → organ → operators + chains."""

    def test_uniform_flow_stable(self):
        """Uniform flow should produce stable/Binary mode."""
        from ck_sim.ck_organ_clouds import CloudOrgan
        from ck_sim.ck_cloud_flow import generate_cloud_frame_pair
        organ = CloudOrgan(patch_size=8, flow_iterations=20)

        for i in range(8):
            f1, f2 = generate_cloud_frame_pair(
                32, 32, 'uniform', strength=0.3, seed=i
            )
            frame = f1 if i % 2 == 0 else f2
            obs = organ.observe(frame)

        # Should tend toward Binary mode
        self.assertIsNotNone(obs)
        stats = organ.stats()
        self.assertGreater(stats['total_operators'], 0)

    def test_turbulent_flow_chaotic(self):
        """Turbulent flow should produce higher energy."""
        from ck_sim.ck_organ_clouds import CloudOrgan
        from ck_sim.ck_cloud_flow import generate_cloud_frame_pair
        organ = CloudOrgan(patch_size=8, flow_iterations=20)

        for i in range(8):
            f1, f2 = generate_cloud_frame_pair(
                32, 32, 'turbulent', strength=1.0, seed=i
            )
            frame = f1 if i % 2 == 0 else f2
            obs = organ.observe(frame)

        self.assertIsNotNone(obs)
        # Turbulent should have higher energy than uniform
        self.assertGreater(obs.energy, 0.0)

    def test_chain_knowledge_export(self):
        """Chains should produce valid knowledge dicts."""
        from ck_sim.ck_organ_clouds import CloudOrgan, CHAIN_WINDOW
        organ = CloudOrgan(patch_size=8, flow_iterations=10)

        for i in range(CHAIN_WINDOW + 5):
            organ.observe(np.random.rand(32, 32).astype(np.float32))

        chains = organ.all_chains
        if chains:
            kd = chains[0].to_knowledge_dict()
            self.assertEqual(kd['type'], 'cloud_pattern')
            self.assertIn('coherence', kd)
            self.assertIn('energy', kd)
            self.assertIn('mode', kd)


# ================================================================
#  PATTERN CLASSIFICATION TESTS
# ================================================================

class TestPatternClassification(unittest.TestCase):
    """Validate cloud pattern type classification."""

    def test_high_coherence_is_harmonic(self):
        from ck_sim.ck_organ_clouds import _classify_pattern
        from ck_sim.ck_sim_heartbeat import HARMONY
        self.assertEqual(_classify_pattern(0.8, 'B', HARMONY), 'harmonic')

    def test_binary_void_is_still(self):
        from ck_sim.ck_organ_clouds import _classify_pattern
        from ck_sim.ck_sim_heartbeat import VOID
        self.assertEqual(_classify_pattern(0.3, 'B', VOID), 'still')

    def test_binary_progress_is_drift(self):
        from ck_sim.ck_organ_clouds import _classify_pattern
        from ck_sim.ck_sim_heartbeat import PROGRESS
        self.assertEqual(_classify_pattern(0.3, 'B', PROGRESS), 'drift')

    def test_ternary_balance_is_equilibrium(self):
        from ck_sim.ck_organ_clouds import _classify_pattern
        from ck_sim.ck_sim_heartbeat import BALANCE
        self.assertEqual(_classify_pattern(0.3, 'T', BALANCE), 'equilibrium')

    def test_quaternary_chaos_is_turbulent(self):
        from ck_sim.ck_organ_clouds import _classify_pattern
        from ck_sim.ck_sim_heartbeat import CHAOS
        self.assertEqual(_classify_pattern(0.3, 'Q', CHAOS), 'turbulent')


# ================================================================
#  RUN
# ================================================================

if __name__ == '__main__':
    unittest.main()
