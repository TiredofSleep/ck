"""
ck_sensory_codecs_tests.py -- Tests for Universal Sensory Codecs
================================================================
Validates: CurvatureEngine, all 5 sensor codecs (IMU, proximity, motor,
battery, temperature), SensorFusion, operator-to-motor mapping, E/A/K bridge.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCurvatureEngine(unittest.TestCase):
    """Test the generalized D2 curvature engine."""

    def test_import(self):
        """CurvatureEngine imports cleanly."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine
        eng = CurvatureEngine()
        self.assertIsNotNone(eng)

    def test_needs_three_vectors(self):
        """D2 requires 3 history entries before computing."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine
        eng = CurvatureEngine()
        self.assertFalse(eng.feed([0.5, 0.5, 0.5, 0.5, 0.5]))
        self.assertFalse(eng.feed([0.5, 0.5, 0.5, 0.5, 0.5]))
        self.assertTrue(eng.feed([0.5, 0.5, 0.5, 0.5, 0.5]))

    def test_constant_input_low_curvature(self):
        """Constant input -> zero D2 -> VOID operator."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine, VOID
        eng = CurvatureEngine()
        vec = [0.5, 0.5, 0.5, 0.5, 0.5]
        eng.feed(vec)
        eng.feed(vec)
        eng.feed(vec)
        # D2 = v0 - 2*v1 + v2 = [0,0,0,0,0] when constant
        self.assertEqual(eng.operator, VOID)
        self.assertTrue(all(abs(d) < 1e-10 for d in eng.d2_float))

    def test_step_change_high_curvature(self):
        """Step change in input -> high D2 -> non-VOID operator."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine, VOID
        eng = CurvatureEngine()
        eng.feed([0.0, 0.0, 0.0, 0.0, 0.0])
        eng.feed([0.0, 0.0, 0.0, 0.0, 0.0])
        eng.feed([1.0, 1.0, 1.0, 1.0, 1.0])
        # D2 = [0,0,0,0,0] - 2*[0,...] + [1,...] = [1,1,1,1,1]
        self.assertNotEqual(eng.operator, VOID)
        self.assertTrue(sum(abs(d) for d in eng.d2_float) > 0)

    def test_classify_range(self):
        """All classified operators are in valid range 0-9."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine, NUM_OPS
        eng = CurvatureEngine()
        import random
        random.seed(42)
        for _ in range(50):
            vec = [random.random() for _ in range(5)]
            eng.feed(vec)
        self.assertTrue(0 <= eng.operator < NUM_OPS)

    def test_reset(self):
        """Reset clears history."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine, VOID
        eng = CurvatureEngine()
        eng.feed([1.0, 1.0, 1.0, 1.0, 1.0])
        eng.feed([0.0, 0.0, 0.0, 0.0, 0.0])
        eng.feed([1.0, 1.0, 1.0, 1.0, 1.0])
        eng.reset()
        self.assertEqual(eng.operator, VOID)
        self.assertEqual(len(eng.history), 0)

    def test_smooth_ramp_moderate_curvature(self):
        """Linear ramp -> constant D2 -> moderate operator."""
        from ck_sim.ck_sensory_codecs import CurvatureEngine
        eng = CurvatureEngine()
        # Linear ramp: D2 of a line is 0
        eng.feed([0.0, 0.0, 0.0, 0.0, 0.0])
        eng.feed([0.1, 0.1, 0.1, 0.1, 0.1])
        eng.feed([0.2, 0.2, 0.2, 0.2, 0.2])
        # D2 = [0] - 2*[0.1] + [0.2] = [0,0,0,0,0]
        self.assertTrue(all(abs(d) < 1e-10 for d in eng.d2_float))


class TestIMUCodec(unittest.TestCase):
    """Test IMU (accelerometer + gyroscope) codec."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import IMUCodec
        codec = IMUCodec()
        self.assertEqual(codec.name, 'imu')

    def test_stationary_reading(self):
        """Stationary (only gravity) -> force vector in valid range."""
        from ck_sim.ck_sensory_codecs import IMUCodec
        codec = IMUCodec()
        reading = {
            'accel_x': 0.0, 'accel_y': 0.0, 'accel_z': 9.81,
            'gyro_x': 0.0, 'gyro_y': 0.0, 'gyro_z': 0.0,
        }
        vec = codec.map_to_force_vector(reading)
        self.assertEqual(len(vec), 5)
        for v in vec:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_stationary_high_vertical(self):
        """Stationary on level surface -> depth close to 1.0 (gravity is vertical)."""
        from ck_sim.ck_sensory_codecs import IMUCodec
        codec = IMUCodec()
        reading = {
            'accel_x': 0.0, 'accel_y': 0.0, 'accel_z': 9.81,
            'gyro_x': 0.0, 'gyro_y': 0.0, 'gyro_z': 0.0,
        }
        vec = codec.map_to_force_vector(reading)
        # depth = |az| / accel_mag ≈ 1.0 when purely vertical
        self.assertGreater(vec[2], 0.9)

    def test_tumbling_high_binding(self):
        """High accel + high gyro -> binding approaches 1.0."""
        from ck_sim.ck_sensory_codecs import IMUCodec
        codec = IMUCodec()
        reading = {
            'accel_x': 15.0, 'accel_y': 10.0, 'accel_z': 5.0,
            'gyro_x': 8.0, 'gyro_y': 5.0, 'gyro_z': 3.0,
        }
        vec = codec.map_to_force_vector(reading)
        self.assertGreater(vec[3], 0.3)  # binding should be significant

    def test_feed_returns_operator(self):
        """feed() returns a valid operator after enough readings."""
        from ck_sim.ck_sensory_codecs import IMUCodec, NUM_OPS
        codec = IMUCodec()
        import random
        random.seed(42)
        for _ in range(10):
            reading = {
                'accel_x': random.gauss(0, 2),
                'accel_y': random.gauss(0, 2),
                'accel_z': 9.81 + random.gauss(0, 0.5),
                'gyro_x': random.gauss(0, 0.5),
                'gyro_y': random.gauss(0, 0.5),
                'gyro_z': random.gauss(0, 0.5),
            }
            op = codec.feed(reading)
        self.assertTrue(0 <= op < NUM_OPS)

    def test_coherence_defined(self):
        """coherence() returns a float in [0, 1]."""
        from ck_sim.ck_sensory_codecs import IMUCodec
        codec = IMUCodec()
        import random
        random.seed(42)
        for _ in range(20):
            codec.feed({
                'accel_x': random.gauss(0, 2),
                'accel_y': random.gauss(0, 2),
                'accel_z': 9.81,
                'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            })
        coh = codec.coherence()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)


class TestProximityCodec(unittest.TestCase):
    """Test proximity (ultrasonic/IR) codec."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import ProximityCodec
        codec = ProximityCodec()
        self.assertEqual(codec.name, 'proximity')

    def test_far_object(self):
        """Object far away -> low pressure, low depth."""
        from ck_sim.ck_sensory_codecs import ProximityCodec
        codec = ProximityCodec()
        vec = codec.map_to_force_vector({'distance_cm': 300.0, 'max_range_cm': 400.0})
        self.assertLess(vec[1], 0.3)   # pressure (closeness) should be low
        self.assertAlmostEqual(vec[2], 0.0)  # depth (danger) should be 0

    def test_close_object(self):
        """Object very close -> high pressure, high depth."""
        from ck_sim.ck_sensory_codecs import ProximityCodec
        codec = ProximityCodec()
        vec = codec.map_to_force_vector({'distance_cm': 5.0, 'max_range_cm': 400.0})
        self.assertGreater(vec[1], 0.9)  # pressure (closeness) near max
        self.assertGreater(vec[2], 0.7)  # depth (danger zone active)

    def test_object_persistence(self):
        """Stable distance over time -> binding increases."""
        from ck_sim.ck_sensory_codecs import ProximityCodec
        codec = ProximityCodec()
        reading = {'distance_cm': 50.0, 'max_range_cm': 400.0}
        for _ in range(15):
            vec = codec.map_to_force_vector(reading)
        self.assertGreater(vec[3], 0.5)  # binding should have increased

    def test_feed_and_fuse(self):
        """Feeding multiple readings produces fuseable operators."""
        from ck_sim.ck_sensory_codecs import ProximityCodec, NUM_OPS
        codec = ProximityCodec()
        for i in range(10):
            codec.feed({'distance_cm': 50.0 + i * 5, 'max_range_cm': 400.0})
        fused = codec.fuse()
        self.assertTrue(0 <= fused < NUM_OPS)


class TestMotorCodec(unittest.TestCase):
    """Test motor feedback codec."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import MotorCodec
        codec = MotorCodec()
        self.assertEqual(codec.name, 'motor')

    def test_on_target(self):
        """Motor at target -> low depth (error), high binding."""
        from ck_sim.ck_sensory_codecs import MotorCodec
        codec = MotorCodec()
        vec = codec.map_to_force_vector({
            'position_deg': 90.0, 'target_deg': 90.0,
            'load': 0.2, 'speed': 0.0,
        })
        self.assertAlmostEqual(vec[2], 0.0)   # zero error
        self.assertAlmostEqual(vec[3], 1.0)    # perfect binding

    def test_off_target(self):
        """Motor far from target -> high depth (error), low binding."""
        from ck_sim.ck_sensory_codecs import MotorCodec
        codec = MotorCodec()
        vec = codec.map_to_force_vector({
            'position_deg': 10.0, 'target_deg': 170.0,
            'load': 0.8, 'speed': 50.0,
        })
        self.assertGreater(vec[2], 0.5)  # significant error
        self.assertLess(vec[3], 0.5)     # low binding

    def test_force_vector_range(self):
        """All force vector components in [0, 1]."""
        from ck_sim.ck_sensory_codecs import MotorCodec
        codec = MotorCodec()
        import random
        random.seed(42)
        for _ in range(20):
            vec = codec.map_to_force_vector({
                'position_deg': random.uniform(0, 180),
                'target_deg': random.uniform(0, 180),
                'load': random.uniform(0, 1),
                'speed': random.uniform(0, 100),
            })
            for v in vec:
                self.assertGreaterEqual(v, 0.0)
                self.assertLessEqual(v, 1.0)


class TestBatteryCodec(unittest.TestCase):
    """Test battery monitor codec."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import BatteryCodec
        codec = BatteryCodec()
        self.assertEqual(codec.name, 'battery')

    def test_full_charge(self):
        """Full battery -> high aperture, low depth."""
        from ck_sim.ck_sensory_codecs import BatteryCodec
        codec = BatteryCodec()
        vec = codec.map_to_force_vector({
            'voltage': 8.4, 'current_a': 0.5,
            'voltage_max': 8.4, 'voltage_min': 6.0,
        })
        self.assertAlmostEqual(vec[0], 1.0)    # aperture = full charge
        self.assertAlmostEqual(vec[2], 0.0)    # depth = no discharge

    def test_depleted(self):
        """Depleted battery -> low aperture, high depth."""
        from ck_sim.ck_sensory_codecs import BatteryCodec
        codec = BatteryCodec()
        vec = codec.map_to_force_vector({
            'voltage': 6.0, 'current_a': 3.0,
            'voltage_max': 8.4, 'voltage_min': 6.0,
        })
        self.assertAlmostEqual(vec[0], 0.0)    # aperture = empty
        self.assertAlmostEqual(vec[2], 1.0)    # depth = fully discharged

    def test_heavy_draw(self):
        """High current -> high pressure."""
        from ck_sim.ck_sensory_codecs import BatteryCodec
        codec = BatteryCodec()
        vec = codec.map_to_force_vector({
            'voltage': 7.5, 'current_a': 4.5,
        })
        self.assertGreater(vec[1], 0.8)  # pressure = high current draw

    def test_voltage_stability(self):
        """Stable voltage over time -> high binding."""
        from ck_sim.ck_sensory_codecs import BatteryCodec
        codec = BatteryCodec()
        for _ in range(5):
            vec = codec.map_to_force_vector({'voltage': 7.8, 'current_a': 1.0})
        self.assertGreater(vec[3], 0.9)  # stable voltage = high binding


class TestTemperatureCodec(unittest.TestCase):
    """Test temperature sensor codec."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import TemperatureCodec
        codec = TemperatureCodec()
        self.assertEqual(codec.name, 'temperature')

    def test_optimal_temp(self):
        """At optimal temp -> low pressure, no depth."""
        from ck_sim.ck_sensory_codecs import TemperatureCodec
        codec = TemperatureCodec(optimal_c=25.0)
        vec = codec.map_to_force_vector({'temp_c': 25.0})
        self.assertAlmostEqual(vec[1], 0.0)    # no deviation
        self.assertAlmostEqual(vec[2], 0.0)    # not extreme

    def test_freezing(self):
        """Below freezing -> high depth."""
        from ck_sim.ck_sensory_codecs import TemperatureCodec
        codec = TemperatureCodec()
        vec = codec.map_to_force_vector({'temp_c': -10.0})
        self.assertGreater(vec[2], 0.3)  # extreme cold
        self.assertGreater(vec[1], 0.5)  # far from optimal

    def test_overheating(self):
        """Very hot -> high depth."""
        from ck_sim.ck_sensory_codecs import TemperatureCodec
        codec = TemperatureCodec()
        vec = codec.map_to_force_vector({'temp_c': 55.0})
        self.assertGreater(vec[2], 0.3)  # extreme heat

    def test_thermal_stability(self):
        """Stable temp -> high binding and continuity."""
        from ck_sim.ck_sensory_codecs import TemperatureCodec
        codec = TemperatureCodec()
        for _ in range(5):
            vec = codec.map_to_force_vector({'temp_c': 25.0})
        self.assertGreater(vec[3], 0.9)  # stable
        self.assertGreater(vec[4], 0.9)  # smooth


class TestCodecRegistry(unittest.TestCase):
    """Test codec registry and auto-discovery."""

    def test_registry_complete(self):
        """All 6 codec types in registry."""
        from ck_sim.ck_sensory_codecs import CODEC_REGISTRY
        self.assertIn('imu', CODEC_REGISTRY)
        self.assertIn('proximity', CODEC_REGISTRY)
        self.assertIn('motor', CODEC_REGISTRY)
        self.assertIn('battery', CODEC_REGISTRY)
        self.assertIn('temperature', CODEC_REGISTRY)
        self.assertIn('vision', CODEC_REGISTRY)
        self.assertEqual(len(CODEC_REGISTRY), 6)

    def test_all_codecs_instantiate(self):
        """Every registered codec creates without error."""
        from ck_sim.ck_sensory_codecs import CODEC_REGISTRY
        for name, cls in CODEC_REGISTRY.items():
            codec = cls()
            self.assertEqual(codec.name, name)


class TestVisionCodec(unittest.TestCase):
    """Test VisionCodec: camera statistics → D2 → operator."""

    def setUp(self):
        from ck_sim.ck_sensory_codecs import VisionCodec
        self.codec = VisionCodec()

    def test_instantiate(self):
        self.assertEqual(self.codec.name, 'vision')

    def test_force_vector_length(self):
        """Force vector is always 5D."""
        raw = {'edge_density': 0.5, 'brightness': 0.6, 'contrast': 0.3,
               'motion_magnitude': 0.2, 'color_variance': 0.4, 'focus': 0.7}
        fv = self.codec.map_to_force_vector(raw)
        self.assertEqual(len(fv), 5)

    def test_force_vector_range(self):
        """All force vector components in [0, 1]."""
        raw = {'edge_density': 0.5, 'brightness': 0.6, 'contrast': 0.3,
               'motion_magnitude': 0.2, 'color_variance': 0.4, 'focus': 0.7}
        fv = self.codec.map_to_force_vector(raw)
        for v in fv:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_bright_scene_high_aperture(self):
        """Bright scene → high aperture component."""
        fv = self.codec.map_to_force_vector({'brightness': 0.95})
        self.assertGreater(fv[0], 0.9)  # aperture = brightness

    def test_dark_scene_low_aperture(self):
        """Dark scene → low aperture."""
        fv = self.codec.map_to_force_vector({'brightness': 0.05})
        self.assertLess(fv[0], 0.1)

    def test_fast_motion_high_pressure(self):
        """Fast motion → high pressure."""
        fv = self.codec.map_to_force_vector({'motion_magnitude': 0.9})
        self.assertGreater(fv[1], 0.8)  # pressure = motion_magnitude

    def test_edges_map_to_depth(self):
        """High edge density → high depth."""
        fv = self.codec.map_to_force_vector({'edge_density': 0.9})
        self.assertGreater(fv[2], 0.8)  # depth = edge_density

    def test_uniform_color_high_binding(self):
        """Low color variance → high binding."""
        fv = self.codec.map_to_force_vector({'color_variance': 0.1})
        self.assertGreater(fv[3], 0.8)  # binding = 1 - color_variance

    def test_chaotic_color_low_binding(self):
        """High color variance → low binding."""
        fv = self.codec.map_to_force_vector({'color_variance': 0.9})
        self.assertLess(fv[3], 0.2)

    def test_sharp_still_high_continuity(self):
        """Sharp focus + steady motion → high continuity."""
        # First feed to set prev_motion
        self.codec.map_to_force_vector({'motion_magnitude': 0.1, 'focus': 0.9})
        # Same motion = low delta
        fv = self.codec.map_to_force_vector({'motion_magnitude': 0.1, 'focus': 0.9})
        self.assertGreater(fv[4], 0.7)  # continuity

    def test_feed_returns_valid_operator(self):
        """Full pipeline: camera stats → operator."""
        from ck_sim.ck_sensory_codecs import NUM_OPS
        raw = {'edge_density': 0.5, 'brightness': 0.6, 'contrast': 0.3,
               'motion_magnitude': 0.2, 'color_variance': 0.4, 'focus': 0.7}
        # Need several ticks for D2 pipeline warm-up
        for _ in range(6):
            op = self.codec.feed(raw)
        self.assertGreaterEqual(op, 0)
        self.assertLess(op, NUM_OPS)

    def test_empty_dict_uses_defaults(self):
        """Empty reading uses default values, no crash."""
        fv = self.codec.map_to_force_vector({})
        self.assertEqual(len(fv), 5)

    def test_clamp_out_of_range(self):
        """Values > 1 get clamped."""
        fv = self.codec.map_to_force_vector({
            'brightness': 1.5, 'motion_magnitude': 2.0, 'edge_density': 1.3,
            'color_variance': -0.5, 'focus': 1.2,
        })
        for v in fv:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)


class TestSensorFusion(unittest.TestCase):
    """Test multi-sensor fusion."""

    def test_import(self):
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        self.assertIsNotNone(fusion)

    def test_auto_register(self):
        """auto_register creates codecs for all named sensors."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'proximity', 'battery'])
        self.assertEqual(len(fusion.codecs), 3)
        self.assertIn('imu', fusion.codecs)
        self.assertIn('proximity', fusion.codecs)
        self.assertIn('battery', fusion.codecs)

    def test_auto_register_ignores_unknown(self):
        """Unknown sensor names are silently skipped."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'laser_cannon', 'warp_drive'])
        self.assertEqual(len(fusion.codecs), 1)

    def test_feed_single_sensor(self):
        """Feeding one sensor returns operator."""
        from ck_sim.ck_sensory_codecs import SensorFusion, NUM_OPS
        fusion = SensorFusion()
        fusion.auto_register(['proximity'])
        for i in range(5):
            op = fusion.feed('proximity', {'distance_cm': 50.0 + i * 10})
        self.assertTrue(0 <= op < NUM_OPS)

    def test_feed_all_sensors(self):
        """feed_all composes all sensor operators through CL."""
        from ck_sim.ck_sensory_codecs import SensorFusion, NUM_OPS
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'proximity', 'battery', 'temperature'])
        import random
        random.seed(42)
        for _ in range(10):
            readings = {
                'imu': {
                    'accel_x': random.gauss(0, 2),
                    'accel_y': random.gauss(0, 2),
                    'accel_z': 9.81,
                    'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
                },
                'proximity': {'distance_cm': 100 + random.gauss(0, 10)},
                'battery': {'voltage': 7.8, 'current_a': 1.0},
                'temperature': {'temp_c': 25 + random.gauss(0, 1)},
            }
            body_op = fusion.feed_all(readings)
        self.assertTrue(0 <= body_op < NUM_OPS)
        self.assertEqual(fusion.body_operator, body_op)

    def test_body_coherence(self):
        """Body coherence is average of sensor coherences, in [0, 1]."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'proximity'])
        import random
        random.seed(42)
        for _ in range(20):
            readings = {
                'imu': {
                    'accel_x': random.gauss(0, 1), 'accel_y': random.gauss(0, 1),
                    'accel_z': 9.81, 'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
                },
                'proximity': {'distance_cm': 100},
            }
            fusion.feed_all(readings)
        coh = fusion.body_coherence
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_body_eak(self):
        """E/A/K triad from sensor fusion produces 3 floats."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'battery', 'temperature'])
        readings = {
            'imu': {
                'accel_x': 0, 'accel_y': 0, 'accel_z': 9.81,
                'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            },
            'battery': {'voltage': 7.8, 'current_a': 1.0},
            'temperature': {'temp_c': 25.0},
        }
        fusion.feed_all(readings)
        e, a, k = fusion.body_eak()
        self.assertIsInstance(e, float)
        self.assertIsInstance(a, float)
        self.assertIsInstance(k, float)

    def test_eak_high_error_high_depth(self):
        """Sensors in trouble -> E (error/depth) rises."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['proximity', 'battery'])
        # Close object + depleted battery = high depth
        readings = {
            'proximity': {'distance_cm': 5.0, 'max_range_cm': 400.0},
            'battery': {'voltage': 6.0, 'current_a': 4.0,
                        'voltage_max': 8.4, 'voltage_min': 6.0},
        }
        fusion.feed_all(readings)
        e, a, k = fusion.body_eak()
        self.assertGreater(e, 0.3)  # depth signals trouble

    def test_stats(self):
        """stats() returns well-formed dict."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'proximity'])
        fusion.feed_all({
            'imu': {
                'accel_x': 0, 'accel_y': 0, 'accel_z': 9.81,
                'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            },
            'proximity': {'distance_cm': 100},
        })
        s = fusion.stats()
        self.assertIn('n_codecs', s)
        self.assertIn('sensors', s)
        self.assertIn('body_operator', s)
        self.assertIn('body_coherence', s)
        self.assertIn('codecs', s)
        self.assertEqual(s['n_codecs'], 2)

    def test_empty_fusion(self):
        """Empty fusion (no codecs) returns safe defaults."""
        from ck_sim.ck_sensory_codecs import SensorFusion, VOID
        fusion = SensorFusion()
        op = fusion.feed_all({})
        self.assertEqual(op, VOID)
        self.assertEqual(fusion.body_coherence, 0.0)
        e, a, k = fusion.body_eak()
        self.assertEqual((e, a, k), (0.0, 0.0, 0.0))


class TestOperatorToMotor(unittest.TestCase):
    """Test operator-to-motor behavior mapping."""

    def test_all_operators_mapped(self):
        """Every operator has a behavior mapping."""
        from ck_sim.ck_sensory_codecs import OPERATOR_TO_BEHAVIOR, NUM_OPS
        for op in range(NUM_OPS):
            self.assertIn(op, OPERATOR_TO_BEHAVIOR)

    def test_motor_command_structure(self):
        """operator_to_motor_command returns well-formed dict."""
        from ck_sim.ck_sensory_codecs import operator_to_motor_command, PROGRESS
        cmd = operator_to_motor_command(PROGRESS, btq_level=1.0)
        self.assertIn('action', cmd)
        self.assertIn('intensity', cmd)
        self.assertIn('btq_gated', cmd)
        self.assertIn('operator', cmd)
        self.assertIn('operator_name', cmd)
        self.assertEqual(cmd['action'], 'forward')

    def test_btq_gating(self):
        """BTQ level gates motor intensity."""
        from ck_sim.ck_sensory_codecs import operator_to_motor_command, PROGRESS
        full = operator_to_motor_command(PROGRESS, btq_level=1.0)
        red = operator_to_motor_command(PROGRESS, btq_level=0.3)
        self.assertGreater(full['btq_gated'], red['btq_gated'])

    def test_void_is_idle(self):
        """VOID operator -> idle action."""
        from ck_sim.ck_sensory_codecs import operator_to_motor_command, VOID
        cmd = operator_to_motor_command(VOID)
        self.assertEqual(cmd['action'], 'idle')
        self.assertAlmostEqual(cmd['intensity'], 0.0)

    def test_harmony_approach(self):
        """HARMONY -> approach action."""
        from ck_sim.ck_sensory_codecs import operator_to_motor_command, HARMONY
        cmd = operator_to_motor_command(HARMONY)
        self.assertEqual(cmd['action'], 'approach')


class TestIntegrationWithBody(unittest.TestCase):
    """Test sensory codecs integration with body interface."""

    def test_codecs_match_body_capabilities(self):
        """SensorFusion can register codecs matching DogBody capabilities."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        from ck_sim.ck_body_interface import DogBody, Capability
        body = DogBody()
        fusion = SensorFusion()
        # Dog has FEEL and MOVE capabilities -> imu + motor
        sensor_map = []
        if body.spec.can(Capability.FEEL):
            sensor_map.append('imu')
        if body.spec.can(Capability.MOVE):
            sensor_map.append('motor')
        if body.spec.has_battery:
            sensor_map.append('battery')
        sensor_map.append('temperature')  # always available
        fusion.auto_register(sensor_map)
        self.assertGreaterEqual(len(fusion.codecs), 3)

    def test_fusion_with_dog_sensor_data(self):
        """Full cycle: DogBody sensors -> SensorFusion -> E/A/K."""
        from ck_sim.ck_sensory_codecs import SensorFusion
        from ck_sim.ck_body_interface import DogBody
        body = DogBody()
        body.update_sensors(
            imu_accel=(0.5, -0.3, 9.8),
            imu_gyro=(0.1, -0.05, 0.02),
            battery_pct=0.85,
        )
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'battery', 'temperature'])
        sensors = body.sense()
        imu_data = {
            'accel_x': sensors['imu_accel'][0],
            'accel_y': sensors['imu_accel'][1],
            'accel_z': sensors['imu_accel'][2],
            'gyro_x': sensors['imu_gyro'][0],
            'gyro_y': sensors['imu_gyro'][1],
            'gyro_z': sensors['imu_gyro'][2],
        }
        readings = {
            'imu': imu_data,
            'battery': {'voltage': 7.8, 'current_a': 1.5},
            'temperature': {'temp_c': 30.0},
        }
        # Feed several ticks
        for _ in range(5):
            fusion.feed_all(readings)
        e, a, k = fusion.body_eak()
        self.assertIsInstance(e, float)
        self.assertIsInstance(a, float)
        self.assertIsInstance(k, float)

    def test_all_body_types_instantiate(self):
        """Every body in BODY_REGISTRY creates successfully."""
        from ck_sim.ck_body_interface import BODY_REGISTRY
        for name, cls in BODY_REGISTRY.items():
            body = cls()
            self.assertIsNotNone(body.spec)

    def test_codec_stats_serializable(self):
        """Codec stats can be JSON-serialized (for API/logging)."""
        import json
        from ck_sim.ck_sensory_codecs import SensorFusion
        fusion = SensorFusion()
        fusion.auto_register(['imu', 'proximity'])
        for _ in range(5):
            fusion.feed_all({
                'imu': {
                    'accel_x': 0, 'accel_y': 0, 'accel_z': 9.81,
                    'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
                },
                'proximity': {'distance_cm': 50},
            })
        stats = fusion.stats()
        serialized = json.dumps(stats)
        self.assertTrue(len(serialized) > 10)


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK SENSORY CODECS TESTS")
    print("=" * 60)

    # Count tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    total = suite.countTestCases()
    print(f"  Running {total} tests...\n")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    passed = total - len(result.failures) - len(result.errors)
    print(f"  RESULT: {passed}/{total} passed")
    if result.wasSuccessful():
        print("  ALL TESTS PASSED")
    else:
        print("  FAILURES DETECTED")
    print("=" * 60)
