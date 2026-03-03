"""
Tests for ck_sdv_safety.py -- Safety rails for Clay SDV Protocol.
"""

import math
import unittest

from ck_sim.being.ck_sdv_safety import (
    clamp, clamp_vector, safe_div, safe_sqrt, safe_log,
    CompressOnlySafety, state_hash, probe_step_hash,
    DeterministicRNG, FORCE_MIN, FORCE_MAX, D2_MAG_CEILING,
)


class TestClamp(unittest.TestCase):

    def test_clamp_in_range(self):
        self.assertEqual(clamp(0.5), 0.5)

    def test_clamp_below(self):
        self.assertEqual(clamp(-0.1), 0.0)

    def test_clamp_above(self):
        self.assertEqual(clamp(1.5), 1.0)

    def test_clamp_nan(self):
        result = clamp(float('nan'))
        self.assertEqual(result, 0.5)  # Midpoint

    def test_clamp_inf(self):
        result = clamp(float('inf'))
        self.assertEqual(result, 0.5)

    def test_clamp_neg_inf(self):
        result = clamp(float('-inf'))
        self.assertEqual(result, 0.5)

    def test_clamp_custom_bounds(self):
        self.assertEqual(clamp(5.0, 0.0, 10.0), 5.0)
        self.assertEqual(clamp(-1.0, 0.0, 10.0), 0.0)
        self.assertEqual(clamp(15.0, 0.0, 10.0), 10.0)


class TestClampVector(unittest.TestCase):

    def test_valid_vector(self):
        vec = [0.1, 0.2, 0.3, 0.4, 0.5]
        result = clamp_vector(vec)
        self.assertEqual(result, vec)

    def test_out_of_range(self):
        vec = [-0.5, 1.5, 0.5, -1.0, 2.0]
        result = clamp_vector(vec)
        self.assertEqual(result, [0.0, 1.0, 0.5, 0.0, 1.0])

    def test_nan_in_vector(self):
        vec = [0.5, float('nan'), 0.5, 0.5, 0.5]
        result = clamp_vector(vec)
        self.assertEqual(result[1], 0.5)  # NaN -> midpoint


class TestSafeMath(unittest.TestCase):

    def test_safe_div_normal(self):
        self.assertAlmostEqual(safe_div(1.0, 2.0), 0.5)

    def test_safe_div_zero(self):
        self.assertEqual(safe_div(1.0, 0.0), 0.0)

    def test_safe_div_nan(self):
        self.assertEqual(safe_div(1.0, float('nan')), 0.0)

    def test_safe_sqrt_normal(self):
        self.assertAlmostEqual(safe_sqrt(4.0), 2.0)

    def test_safe_sqrt_negative(self):
        self.assertEqual(safe_sqrt(-1.0), 0.0)

    def test_safe_log_normal(self):
        self.assertAlmostEqual(safe_log(math.e), 1.0, places=5)

    def test_safe_log_zero(self):
        self.assertEqual(safe_log(0.0), 0.0)

    def test_safe_log_negative(self):
        self.assertEqual(safe_log(-1.0), 0.0)


class TestCompressOnlySafety(unittest.TestCase):

    def setUp(self):
        self.safety = CompressOnlySafety(halt_threshold=5)

    def test_valid_vector_passes(self):
        vec = [0.1, 0.2, 0.3, 0.4, 0.5]
        result = self.safety.check_force_vector(vec, 'test')
        self.assertEqual(result, vec)
        self.assertEqual(self.safety.anomaly_count, 0)

    def test_out_of_range_clamped(self):
        vec = [0.5, 1.5, 0.5, -0.1, 0.5]
        result = self.safety.check_force_vector(vec, 'test')
        self.assertEqual(result[1], 1.0)
        self.assertEqual(result[3], 0.0)
        self.assertEqual(self.safety.anomaly_count, 2)

    def test_nan_detected(self):
        vec = [float('nan'), 0.5, 0.5, 0.5, 0.5]
        result = self.safety.check_force_vector(vec, 'test')
        self.assertEqual(result[0], 0.5)
        self.assertEqual(self.safety.anomaly_count, 1)

    def test_halt_on_threshold(self):
        for i in range(5):
            self.safety.check_force_vector([float('nan')] * 5, 'test')
        self.assertTrue(self.safety.halted)
        result = self.safety.check_force_vector([0.5] * 5, 'test')
        self.assertEqual(result, [0.5] * 5)  # Returns midpoint when halted

    def test_wrong_length_padded(self):
        vec = [0.5, 0.5]
        result = self.safety.check_force_vector(vec, 'test')
        self.assertEqual(len(result), 5)
        self.assertEqual(self.safety.anomaly_count, 1)

    def test_d2_magnitude_cap(self):
        self.assertEqual(self.safety.check_d2_magnitude(1.0), 1.0)
        self.assertEqual(self.safety.check_d2_magnitude(3.0), D2_MAG_CEILING)
        self.assertEqual(self.safety.check_d2_magnitude(float('nan')), 0.0)

    def test_reset(self):
        self.safety.check_force_vector([float('nan')] * 5, 'test')
        self.assertEqual(self.safety.anomaly_count, 5)
        self.safety.reset()
        self.assertEqual(self.safety.anomaly_count, 0)
        self.assertFalse(self.safety.halted)


class TestStateHash(unittest.TestCase):

    def test_deterministic(self):
        vals = [0.1, 0.2, 0.3, 0.4, 0.5]
        h1 = state_hash(vals)
        h2 = state_hash(vals)
        self.assertEqual(h1, h2)

    def test_different_values(self):
        h1 = state_hash([0.1, 0.2, 0.3])
        h2 = state_hash([0.4, 0.5, 0.6])
        self.assertNotEqual(h1, h2)

    def test_probe_step_hash(self):
        h = probe_step_hash(0, 7, 0.5, [0.1, 0.2, 0.3, 0.4, 0.5])
        self.assertEqual(len(h), 16)


class TestDeterministicRNG(unittest.TestCase):

    def test_reproducible(self):
        rng1 = DeterministicRNG(42)
        rng2 = DeterministicRNG(42)
        for _ in range(100):
            self.assertEqual(rng1.next_int(), rng2.next_int())

    def test_float_range(self):
        rng = DeterministicRNG(123)
        for _ in range(1000):
            f = rng.next_float()
            self.assertGreaterEqual(f, 0.0)
            self.assertLess(f, 1.0)

    def test_gauss(self):
        rng = DeterministicRNG(42)
        vals = [rng.next_gauss(0.0, 1.0) for _ in range(1000)]
        mean = sum(vals) / len(vals)
        self.assertAlmostEqual(mean, 0.0, places=0)  # Rough check

    def test_different_seeds(self):
        rng1 = DeterministicRNG(1)
        rng2 = DeterministicRNG(2)
        self.assertNotEqual(rng1.next_int(), rng2.next_int())


if __name__ == '__main__':
    unittest.main()
