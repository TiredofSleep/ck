"""
ck_robot_body_tests.py -- Tests for CK's Physical Robot Body
=============================================================
Validates: GaitController, NavigationState, UARTBridge,
           RobotDogBody integration, BehaviorPlanner.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import math
import os
import sys
import struct

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGaitModes(unittest.TestCase):
    """Test operator-to-gait mapping."""

    def test_all_operators_mapped(self):
        """Every operator has a gait mapping."""
        from ck_sim.ck_robot_body import OPERATOR_TO_GAIT, NUM_OPS
        for op in range(NUM_OPS):
            self.assertIn(op, OPERATOR_TO_GAIT)

    def test_void_is_idle(self):
        from ck_sim.ck_robot_body import OPERATOR_TO_GAIT, VOID, GaitMode
        self.assertEqual(OPERATOR_TO_GAIT[VOID], GaitMode.IDLE)

    def test_progress_is_trot(self):
        from ck_sim.ck_robot_body import OPERATOR_TO_GAIT, PROGRESS, GaitMode
        self.assertEqual(OPERATOR_TO_GAIT[PROGRESS], GaitMode.TROT)

    def test_collapse_is_retreat(self):
        from ck_sim.ck_robot_body import OPERATOR_TO_GAIT, COLLAPSE, GaitMode
        self.assertEqual(OPERATOR_TO_GAIT[COLLAPSE], GaitMode.RETREAT)

    def test_gait_params_complete(self):
        """All gait modes have parameters."""
        from ck_sim.ck_robot_body import GAIT_PARAMS, GaitMode
        for mode in range(6):
            self.assertIn(mode, GAIT_PARAMS)


class TestGaitController(unittest.TestCase):
    """Test gait trajectory generation."""

    def test_import(self):
        from ck_sim.ck_robot_body import GaitController
        gc = GaitController()
        self.assertIsNotNone(gc)

    def test_idle_produces_zeros(self):
        """IDLE gait -> all servo targets at 0."""
        from ck_sim.ck_robot_body import GaitController, GaitMode
        gc = GaitController()
        gc.set_mode(GaitMode.IDLE)
        targets = gc.tick()
        self.assertEqual(len(targets), 8)
        for t in targets:
            self.assertAlmostEqual(t, 0.0)

    def test_walk_produces_nonzero(self):
        """WALK gait -> non-zero servo targets after some ticks."""
        from ck_sim.ck_robot_body import GaitController, GaitMode
        gc = GaitController()
        gc.set_mode(GaitMode.WALK)
        for _ in range(10):
            targets = gc.tick()
        has_nonzero = any(abs(t) > 0.001 for t in targets)
        self.assertTrue(has_nonzero)

    def test_btq_gating_reduces_amplitude(self):
        """Lower BTQ level reduces servo amplitudes."""
        from ck_sim.ck_robot_body import GaitController, GaitMode
        gc_full = GaitController()
        gc_full.set_mode(GaitMode.TROT)
        gc_full.set_btq_level(1.0)

        gc_red = GaitController()
        gc_red.set_mode(GaitMode.TROT)
        gc_red.set_btq_level(0.3)

        for _ in range(20):
            full_targets = gc_full.tick()
            red_targets = gc_red.tick()

        full_max = max(abs(t) for t in full_targets)
        red_max = max(abs(t) for t in red_targets)
        self.assertGreater(full_max, red_max)

    def test_emergency_stop(self):
        """Emergency stop zeros all targets."""
        from ck_sim.ck_robot_body import GaitController, GaitMode
        gc = GaitController()
        gc.set_mode(GaitMode.TROT)
        gc.tick()
        gc.tick()
        gc.emergency_stop()
        self.assertEqual(gc.mode, GaitMode.IDLE)
        for t in gc.targets:
            self.assertAlmostEqual(t, 0.0)

    def test_eight_joints(self):
        """Always returns exactly 8 joint values."""
        from ck_sim.ck_robot_body import GaitController, GaitMode
        gc = GaitController()
        for mode in range(6):
            gc.set_mode(mode)
            targets = gc.tick()
            self.assertEqual(len(targets), 8)

    def test_stats_well_formed(self):
        from ck_sim.ck_robot_body import GaitController
        gc = GaitController()
        gc.tick()
        s = gc.stats()
        self.assertIn('mode', s)
        self.assertIn('phase', s)
        self.assertIn('btq_level', s)
        self.assertIn('targets', s)


class TestNavigationState(unittest.TestCase):
    """Test dead-reckoning and obstacle awareness."""

    def test_import(self):
        from ck_sim.ck_robot_body import NavigationState
        nav = NavigationState()
        self.assertAlmostEqual(nav.x, 0.0)
        self.assertAlmostEqual(nav.y, 0.0)

    def test_imu_integration(self):
        """Forward acceleration moves position forward."""
        from ck_sim.ck_robot_body import NavigationState
        nav = NavigationState()
        for _ in range(100):
            nav.update_from_imu(accel_x=1.0, accel_y=0.0, gyro_z=0.0)
        self.assertGreater(nav.x, 0.0)
        self.assertEqual(nav.steps_taken, 100)

    def test_heading_from_gyro(self):
        """Gyro yaw rotates heading."""
        from ck_sim.ck_robot_body import NavigationState
        nav = NavigationState()
        for _ in range(50):
            nav.update_from_imu(accel_x=0.0, accel_y=0.0, gyro_z=1.0)
        self.assertGreater(abs(nav.heading), 0.5)

    def test_obstacle_close(self):
        """Close obstacle -> COLLAPSE operator."""
        from ck_sim.ck_robot_body import NavigationState, COLLAPSE
        nav = NavigationState()
        nav.update_obstacle(5.0)  # 5 cm = danger
        self.assertEqual(nav.obstacle_operator, COLLAPSE)

    def test_obstacle_far(self):
        """Far obstacle -> HARMONY operator."""
        from ck_sim.ck_robot_body import NavigationState, HARMONY
        nav = NavigationState()
        nav.update_obstacle(200.0)  # 200 cm = clear
        self.assertEqual(nav.obstacle_operator, HARMONY)

    def test_obstacle_medium(self):
        """Medium distance -> COUNTER or BALANCE."""
        from ck_sim.ck_robot_body import NavigationState, COUNTER, BALANCE
        nav = NavigationState()
        nav.update_obstacle(20.0)  # 20 cm = alert
        self.assertEqual(nav.obstacle_operator, COUNTER)
        nav.update_obstacle(60.0)  # 60 cm = aware
        self.assertEqual(nav.obstacle_operator, BALANCE)

    def test_path_coherence(self):
        """Path coherence is HARMONY fraction."""
        from ck_sim.ck_robot_body import NavigationState, HARMONY, COLLAPSE
        nav = NavigationState()
        for _ in range(7):
            nav.record_operator(HARMONY)
        for _ in range(3):
            nav.record_operator(COLLAPSE)
        coh = nav.path_coherence
        self.assertAlmostEqual(coh, 0.7)

    def test_distance_from_origin(self):
        """Distance from origin = sqrt(x^2 + y^2)."""
        from ck_sim.ck_robot_body import NavigationState
        nav = NavigationState()
        nav.x = 3.0
        nav.y = 4.0
        self.assertAlmostEqual(nav.distance_from_origin, 5.0)

    def test_stats(self):
        from ck_sim.ck_robot_body import NavigationState
        nav = NavigationState()
        s = nav.stats()
        self.assertIn('position', s)
        self.assertIn('heading_deg', s)
        self.assertIn('obstacle_cm', s)
        self.assertIn('path_coherence', s)


class TestUARTBridge(unittest.TestCase):
    """Test UART encode/decode for robot communication."""

    def test_import(self):
        from ck_sim.ck_robot_body import UARTBridge
        bridge = UARTBridge()
        self.assertIsNotNone(bridge)

    def test_send_servo_targets(self):
        """Encoding servo targets produces valid UART packets."""
        from ck_sim.ck_robot_body import UARTBridge
        bridge = UARTBridge()
        targets = [0.5, -0.3, 0.7, -0.1, 0.4, -0.2, 0.6, -0.5]
        bridge.send_servo_targets(targets)
        pkts = bridge.get_tx_packets()
        self.assertEqual(len(pkts), 1)
        self.assertTrue(len(pkts[0]) > 5)
        # Check header
        self.assertEqual(pkts[0][0], 0x43)  # 'C'
        self.assertEqual(pkts[0][1], 0x4B)  # 'K'

    def test_send_estop(self):
        """E-stop produces valid packet."""
        from ck_sim.ck_robot_body import UARTBridge, PKT_ESTOP
        bridge = UARTBridge()
        bridge.send_estop()
        pkts = bridge.get_tx_packets()
        self.assertEqual(len(pkts), 1)
        self.assertEqual(pkts[0][2], PKT_ESTOP)

    def test_decode_proximity(self):
        """Decode proximity from payload."""
        from ck_sim.ck_robot_body import UARTBridge
        bridge = UARTBridge()
        # 500mm = 50.0cm
        payload = struct.pack('<H', 500)
        dist = bridge.decode_proximity(payload)
        self.assertAlmostEqual(dist, 50.0)

    def test_decode_servo_positions(self):
        """Decode servo positions from payload."""
        from ck_sim.ck_robot_body import UARTBridge
        bridge = UARTBridge()
        # Encode 45.0 degrees as 450 tenths
        payload = struct.pack('<h', 450)
        positions = bridge.decode_servo_positions(payload)
        self.assertEqual(len(positions), 1)
        self.assertAlmostEqual(math.degrees(positions[0]), 45.0, places=1)

    def test_tx_queue_clears(self):
        """get_tx_packets clears the queue."""
        from ck_sim.ck_robot_body import UARTBridge
        bridge = UARTBridge()
        bridge.send_estop()
        bridge.send_estop()
        self.assertEqual(len(bridge.get_tx_packets()), 2)
        self.assertEqual(len(bridge.get_tx_packets()), 0)


class TestRobotDogBody(unittest.TestCase):
    """Test the full robot dog body integration."""

    def test_import(self):
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        self.assertIsNotNone(robot)
        robot.stop()

    def test_tick_returns_result(self):
        """Each tick returns a well-formed result dict."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        result = robot.tick()
        self.assertIn('tick', result)
        self.assertIn('operator', result)
        self.assertIn('operator_name', result)
        self.assertIn('coherence', result)
        self.assertIn('eak', result)
        self.assertIn('gait', result)
        self.assertIn('nav', result)
        robot.stop()

    def test_tick_count_increments(self):
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        r1 = robot.tick()
        r2 = robot.tick()
        self.assertEqual(r1['tick'], 1)
        self.assertEqual(r2['tick'], 2)
        robot.stop()

    def test_five_sensors_registered(self):
        """All 5 sensor codecs are active."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        self.assertEqual(len(robot.fusion.codecs), 5)
        robot.stop()

    def test_simulation_runs_200_ticks(self):
        """200 ticks without error."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        for _ in range(200):
            result = robot.tick()
        self.assertEqual(result['tick'], 200)
        robot.stop()

    def test_btq_level_gating(self):
        """Setting BTQ level propagates to gait controller."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        robot.set_btq_level(0.3)
        self.assertAlmostEqual(robot.gait._btq_level, 0.3)
        robot.stop()

    def test_emergency_stop(self):
        """Emergency stop zeros gait and body motors."""
        from ck_sim.ck_robot_body import RobotDogBody, GaitMode
        robot = RobotDogBody(simulated=True)
        for _ in range(10):
            robot.tick()
        robot.emergency_stop()
        self.assertEqual(robot.gait.mode, GaitMode.IDLE)
        robot.stop()

    def test_body_eak_tuple(self):
        """body_eak returns 3-tuple of floats."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        robot.tick()
        e, a, k = robot.body_eak
        self.assertIsInstance(e, float)
        self.assertIsInstance(a, float)
        self.assertIsInstance(k, float)
        robot.stop()

    def test_stats_comprehensive(self):
        """stats() returns all expected sections."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        for _ in range(10):
            robot.tick()
        s = robot.stats()
        self.assertIn('tick_count', s)
        self.assertIn('body_operator', s)
        self.assertIn('body_coherence', s)
        self.assertIn('eak', s)
        self.assertIn('gait', s)
        self.assertIn('nav', s)
        self.assertIn('sensor_fusion', s)
        self.assertIn('btq_level', s)
        self.assertIn('simulated', s)
        robot.stop()

    def test_custom_sensor_readings(self):
        """Can feed custom sensor readings."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        custom = {
            'imu': {
                'accel_x': 5.0, 'accel_y': 0, 'accel_z': 9.81,
                'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            },
            'proximity': {'distance_cm': 10.0, 'max_range_cm': 400},
            'motor': {
                'position_deg': 45, 'target_deg': 45,
                'load': 0.5, 'speed': 10,
            },
            'battery': {'voltage': 7.0, 'current_a': 2.0},
            'temperature': {'temp_c': 30.0},
        }
        result = robot.tick(sensor_readings=custom)
        self.assertIsNotNone(result)
        robot.stop()


class TestBehaviorPlanner(unittest.TestCase):
    """Test operator-chain to action-sequence planning."""

    def test_import(self):
        from ck_sim.ck_robot_body import BehaviorPlanner
        bp = BehaviorPlanner()
        self.assertIsNotNone(bp)

    def test_plan_from_operators(self):
        """Plan generates action for each operator."""
        from ck_sim.ck_robot_body import BehaviorPlanner, COUNTER, PROGRESS, HARMONY
        bp = BehaviorPlanner()
        plan = bp.plan_from_operators([COUNTER, PROGRESS, HARMONY])
        self.assertEqual(len(plan), 3)
        self.assertEqual(plan[0]['action'], 'scan')
        self.assertEqual(plan[1]['action'], 'forward')
        self.assertEqual(plan[2]['action'], 'approach')

    def test_next_action_sequence(self):
        """next_action() walks through the plan."""
        from ck_sim.ck_robot_body import BehaviorPlanner, COUNTER, PROGRESS
        bp = BehaviorPlanner()
        bp.plan_from_operators([COUNTER, PROGRESS])
        a1 = bp.next_action()
        a2 = bp.next_action()
        a3 = bp.next_action()
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)
        self.assertIsNone(a3)  # Past end of plan

    def test_plan_remaining(self):
        from ck_sim.ck_robot_body import BehaviorPlanner, HARMONY
        bp = BehaviorPlanner()
        bp.plan_from_operators([HARMONY, HARMONY, HARMONY])
        self.assertEqual(bp.plan_remaining, 3)
        bp.next_action()
        self.assertEqual(bp.plan_remaining, 2)

    def test_clear_plan(self):
        from ck_sim.ck_robot_body import BehaviorPlanner, HARMONY
        bp = BehaviorPlanner()
        bp.plan_from_operators([HARMONY])
        bp.clear()
        self.assertEqual(bp.plan_remaining, 0)
        self.assertEqual(bp.current_action, 'idle')

    def test_btq_gating_in_plan(self):
        """BTQ level gates intensity in planned actions."""
        from ck_sim.ck_robot_body import BehaviorPlanner, PROGRESS
        bp = BehaviorPlanner()
        plan_full = bp.plan_from_operators([PROGRESS], btq_level=1.0)
        plan_red = bp.plan_from_operators([PROGRESS], btq_level=0.3)
        self.assertGreater(plan_full[0]['btq_gated'], plan_red[0]['btq_gated'])


class TestIntegration(unittest.TestCase):
    """Integration tests across robot body subsystems."""

    def test_sensor_to_gait_pipeline(self):
        """Full pipeline: sensors -> codecs -> operator -> gait -> targets."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        results = []
        for _ in range(50):
            results.append(robot.tick())
        # After 50 ticks, gait should have a name
        self.assertIn(results[-1]['gait'],
                      ['IDLE', 'WALK', 'TROT', 'EXPLORE', 'RETREAT', 'HOME'])
        robot.stop()

    def test_obstacle_triggers_retreat(self):
        """Very close obstacle -> gait becomes RETREAT."""
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        # Warm up
        for _ in range(5):
            robot.tick()
        # Feed close obstacle
        close_reading = {
            'imu': {
                'accel_x': 0, 'accel_y': 0, 'accel_z': 9.81,
                'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0,
            },
            'proximity': {'distance_cm': 5.0, 'max_range_cm': 400},
            'motor': {
                'position_deg': 0, 'target_deg': 0,
                'load': 0, 'speed': 0,
            },
            'battery': {'voltage': 7.8, 'current_a': 1.0},
            'temperature': {'temp_c': 25.0},
        }
        result = robot.tick(sensor_readings=close_reading)
        self.assertEqual(result['gait'], 'RETREAT')
        robot.stop()

    def test_stats_json_serializable(self):
        """Full stats can be JSON-serialized."""
        import json
        from ck_sim.ck_robot_body import RobotDogBody
        robot = RobotDogBody(simulated=True)
        for _ in range(10):
            robot.tick()
        stats = robot.stats()
        serialized = json.dumps(stats)
        self.assertTrue(len(serialized) > 50)
        robot.stop()

    def test_body_interface_compatibility(self):
        """RobotDogBody.body is a valid CKBody with DogBody spec."""
        from ck_sim.ck_robot_body import RobotDogBody
        from ck_sim.ck_body_interface import Capability
        robot = RobotDogBody(simulated=True)
        self.assertEqual(robot.body.spec.name, "CK-Dog")
        self.assertTrue(robot.body.spec.can(Capability.MOVE))
        self.assertTrue(robot.body.spec.can(Capability.FEEL))
        self.assertEqual(robot.body.spec.n_motors, 8)
        robot.stop()


# ================================================================
#  MAIN
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK ROBOT BODY TESTS")
    print("=" * 60)

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
