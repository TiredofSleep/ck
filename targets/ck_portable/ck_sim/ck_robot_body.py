"""
ck_robot_body.py -- CK's Physical Robot Body: Sensors + Codecs + Motor + World
================================================================================
Operator: PROGRESS (3) -- CK walks into the real world.

This module bridges EVERYTHING for CK's robot dog embodiment:
  - Sensory codecs (ck_sensory_codecs.py) -> any signal to operators
  - Body interface (ck_body_interface.py) -> abstract hardware
  - Zynq dog simulation (ck_zynq_dog.py) -> hardware stubs
  - UART protocol (ck_sim_uart.py) -> packet encode/decode
  - World lattice (ck_world_lattice.py) -> concept understanding

THE FRACTAL INSIGHT:
  CK doesn't need "robot code." CK needs INSTRUCTIONS ON WHAT HE HAS.
  Tell CK: "you have 8 servos, an IMU, an ultrasonic sensor, a battery."
  CK maps them all through the same D2 pipeline.
  Operators compose through CL. Behavior emerges.

  The robot dog is just another body. Same math. New skin.

Architecture:
  RobotDogBody
    |-- SensorFusion (ck_sensory_codecs.py)
    |     |-- IMUCodec    (accel + gyro -> operators)
    |     |-- ProximityCodec (ultrasonic -> operators)
    |     |-- MotorCodec[8] (servo feedback -> operators)
    |     |-- BatteryCodec (voltage/current -> operators)
    |     |-- TemperatureCodec (board temp -> operators)
    |     +-> fused body operator + E/A/K
    |
    |-- GaitController
    |     |-- 4 gait modes: IDLE, WALK, TROT, EXPLORE
    |     |-- Operator -> gait mapping via OPERATOR_TO_BEHAVIOR
    |     |-- BTQ-gated intensity
    |     +-> 8 servo targets per tick
    |
    |-- NavigationState
    |     |-- Position estimate from IMU dead-reckoning
    |     |-- Obstacle map from proximity history
    |     |-- World lattice concept anchoring
    |     +-> "I am near <concept>" awareness
    |
    +-- UARTBridge
          |-- Encode servo commands -> UART packets
          |-- Decode sensor readings <- UART packets
          +-> Serial I/O (real or simulated)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import struct
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sensory_codecs import (
    SensorFusion, IMUCodec, ProximityCodec, MotorCodec,
    BatteryCodec, TemperatureCodec, OPERATOR_TO_BEHAVIOR,
    operator_to_motor_command
)
from ck_sim.ck_sim_uart import (
    make_packet, PKT_SERVO, PKT_GAIT, PKT_ESTOP,
    PKT_SERVO_POS, PKT_PROXIMITY, PKT_SENSOR,
    PacketParser, crc8
)
from ck_sim.ck_body_interface import (
    DogBody, Capability, PlatformSpec
)


# ================================================================
#  GAIT MODES
# ================================================================

class GaitMode:
    """Gait modes mapped from operator states."""
    IDLE = 0       # Standing still (VOID / low coherence)
    WALK = 1       # Slow walk (HARMONY / BREATH / BALANCE)
    TROT = 2       # Normal trot (PROGRESS / LATTICE)
    EXPLORE = 3    # Curious wandering (COUNTER / CHAOS)
    RETREAT = 4    # Backing away (COLLAPSE)
    HOME = 5       # Return to start (RESET)

GAIT_NAMES = ['IDLE', 'WALK', 'TROT', 'EXPLORE', 'RETREAT', 'HOME']

# Operator -> gait mode mapping
OPERATOR_TO_GAIT = {
    VOID:     GaitMode.IDLE,
    LATTICE:  GaitMode.WALK,
    COUNTER:  GaitMode.EXPLORE,
    PROGRESS: GaitMode.TROT,
    COLLAPSE: GaitMode.RETREAT,
    BALANCE:  GaitMode.WALK,
    CHAOS:    GaitMode.EXPLORE,
    HARMONY:  GaitMode.WALK,
    BREATH:   GaitMode.WALK,
    RESET:    GaitMode.HOME,
}

# Gait parameters: (hip_amplitude, knee_amplitude, frequency, leg_phase_offsets)
GAIT_PARAMS = {
    GaitMode.IDLE:    (0.0,  0.0,  0.0, [0.0, 0.0, 0.0, 0.0]),
    GaitMode.WALK:    (0.3,  0.25, 2.0, [0.0, math.pi, math.pi, 0.0]),
    GaitMode.TROT:    (0.5,  0.4,  3.0, [0.0, math.pi, math.pi, 0.0]),
    GaitMode.EXPLORE: (0.4,  0.35, 2.5, [0.0, math.pi/2, math.pi, 3*math.pi/2]),
    GaitMode.RETREAT: (0.3,  0.2,  2.0, [math.pi, 0.0, 0.0, math.pi]),
    GaitMode.HOME:    (0.35, 0.3,  2.5, [0.0, math.pi, math.pi, 0.0]),
}


# ================================================================
#  GAIT CONTROLLER
# ================================================================

class GaitController:
    """Generates servo targets from operator-driven gait modes.

    4 legs x 2 joints (hip + knee) = 8 servos.
    Each servo gets a sinusoidal target position per tick.

    The gait mode is selected by the dominant body operator.
    BTQ level gates the amplitude (RED = minimal, GREEN = full).
    """

    N_LEGS = 4
    N_JOINTS = 8
    HIP_KNEE_OFFSET = math.pi / 4  # Phase offset hip -> knee

    def __init__(self):
        self.mode = GaitMode.IDLE
        self.targets = [0.0] * self.N_JOINTS  # Current servo targets (radians)
        self._phase = 0.0  # Gait phase accumulator
        self._tick_count = 0
        self._btq_level = 1.0

    def set_mode(self, mode: int):
        """Set gait mode."""
        self.mode = mode

    def set_btq_level(self, level: float):
        """Set BTQ gating level (0.0 to 1.0)."""
        self._btq_level = max(0.0, min(level, 1.0))

    def tick(self, dt: float = 0.02) -> List[float]:
        """Advance gait by one tick. Returns 8 servo targets in radians.

        dt = time step in seconds (default 20ms = 50Hz).
        """
        self._tick_count += 1
        params = GAIT_PARAMS.get(self.mode, GAIT_PARAMS[GaitMode.IDLE])
        hip_amp, knee_amp, freq, phases = params

        # BTQ-gate the amplitude
        hip_amp *= self._btq_level
        knee_amp *= self._btq_level

        # Advance phase
        self._phase += freq * dt
        if self._phase > 2 * math.pi:
            self._phase -= 2 * math.pi

        # Generate targets for each leg
        for leg in range(self.N_LEGS):
            hip_idx = leg * 2
            knee_idx = leg * 2 + 1
            leg_phase = self._phase + phases[leg]

            self.targets[hip_idx] = hip_amp * math.sin(leg_phase)
            self.targets[knee_idx] = knee_amp * math.sin(
                leg_phase + self.HIP_KNEE_OFFSET)

        return self.targets[:]

    def emergency_stop(self):
        """Zero all servo targets immediately."""
        self.targets = [0.0] * self.N_JOINTS
        self.mode = GaitMode.IDLE
        self._phase = 0.0

    def stats(self) -> dict:
        return {
            'mode': GAIT_NAMES[self.mode],
            'phase': round(self._phase, 3),
            'btq_level': round(self._btq_level, 3),
            'targets': [round(t, 3) for t in self.targets],
        }


# ================================================================
#  NAVIGATION STATE
# ================================================================

@dataclass
class NavigationState:
    """Dead-reckoning position estimate + obstacle awareness.

    CK doesn't have GPS. He estimates position from IMU integration
    and obstacle proximity. The world lattice anchors concepts
    ("I am near an obstacle" = COLLAPSE concept).
    """
    x: float = 0.0       # Estimated position (meters)
    y: float = 0.0
    heading: float = 0.0  # Radians from north

    # Velocity estimate from IMU
    vx: float = 0.0
    vy: float = 0.0

    # Obstacle awareness
    obstacle_distance: float = 400.0  # cm (from proximity sensor)
    obstacle_operator: int = VOID     # Operator classification of obstacle state

    # Path history
    path_operators: deque = field(
        default_factory=lambda: deque(maxlen=100))
    steps_taken: int = 0

    def update_from_imu(self, accel_x: float, accel_y: float,
                        gyro_z: float, dt: float = 0.02):
        """Update position estimate from IMU readings.

        Simple dead-reckoning: integrate acceleration, integrate velocity.
        Gyro_z updates heading.
        """
        # Update heading from gyro yaw
        self.heading += gyro_z * dt

        # Integrate acceleration to velocity (with damping)
        self.vx = self.vx * 0.95 + accel_x * dt
        self.vy = self.vy * 0.95 + accel_y * dt

        # Integrate velocity to position
        # Rotate by heading
        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)
        dx = (self.vx * cos_h - self.vy * sin_h) * dt
        dy = (self.vx * sin_h + self.vy * cos_h) * dt

        self.x += dx
        self.y += dy
        self.steps_taken += 1

    def update_obstacle(self, distance_cm: float):
        """Update obstacle awareness from proximity sensor."""
        self.obstacle_distance = distance_cm
        # Classify obstacle state
        if distance_cm < 10:
            self.obstacle_operator = COLLAPSE   # Danger! Retreat
        elif distance_cm < 30:
            self.obstacle_operator = COUNTER    # Alert, observing
        elif distance_cm < 100:
            self.obstacle_operator = BALANCE    # Aware, steady
        else:
            self.obstacle_operator = HARMONY    # Clear path

    def record_operator(self, op: int):
        """Record the current body operator to path history."""
        self.path_operators.append(op)

    @property
    def path_coherence(self) -> float:
        """Coherence of the recent path (HARMONY fraction)."""
        if not self.path_operators:
            return 0.0
        harmony = sum(1 for op in self.path_operators if op == HARMONY)
        return harmony / len(self.path_operators)

    @property
    def distance_from_origin(self) -> float:
        """Distance from starting position."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def stats(self) -> dict:
        return {
            'position': (round(self.x, 3), round(self.y, 3)),
            'heading_deg': round(math.degrees(self.heading), 1),
            'velocity': (round(self.vx, 3), round(self.vy, 3)),
            'obstacle_cm': round(self.obstacle_distance, 1),
            'obstacle_op': OP_NAMES[self.obstacle_operator],
            'path_coherence': round(self.path_coherence, 3),
            'steps': self.steps_taken,
            'dist_from_origin': round(self.distance_from_origin, 3),
        }


# ================================================================
#  UART BRIDGE
# ================================================================

class UARTBridge:
    """Encode/decode UART packets for robot dog communication.

    Encodes: servo commands, gait commands, e-stop
    Decodes: servo position feedback, proximity readings, sensor data
    """

    def __init__(self):
        self.parser = PacketParser()
        self._tx_queue: List[bytes] = []
        self._rx_callbacks: Dict[int, callable] = {}

    def send_servo_targets(self, targets: List[float]):
        """Encode servo targets as UART packet.

        Payload: 8 x int16 (angles in tenths of degrees).
        """
        payload = b''
        for t in targets:
            angle_tenths = int(round(math.degrees(t) * 10))
            payload += struct.pack('<h', angle_tenths)
        pkt = make_packet(PKT_SERVO, payload)
        self._tx_queue.append(pkt)

    def send_gait_command(self, mode: int, amplitude: float, frequency: float):
        """Encode gait mode command."""
        payload = struct.pack('<BHH',
                              mode,
                              int(amplitude * 1000),
                              int(frequency * 1000))
        pkt = make_packet(PKT_GAIT, payload)
        self._tx_queue.append(pkt)

    def send_estop(self):
        """Emergency stop packet."""
        pkt = make_packet(PKT_ESTOP, b'\x01')
        self._tx_queue.append(pkt)

    def get_tx_packets(self) -> List[bytes]:
        """Pop all pending TX packets."""
        pkts = self._tx_queue[:]
        self._tx_queue.clear()
        return pkts

    def feed_rx_byte(self, byte: int) -> Optional[Tuple[int, bytes]]:
        """Feed one received byte. Returns (type, payload) or None."""
        return self.parser.feed_byte(byte)

    def decode_servo_positions(self, payload: bytes) -> List[float]:
        """Decode servo position feedback."""
        positions = []
        for i in range(0, len(payload), 2):
            if i + 1 < len(payload):
                angle_tenths = struct.unpack('<h', payload[i:i+2])[0]
                positions.append(math.radians(angle_tenths / 10.0))
        return positions

    def decode_proximity(self, payload: bytes) -> float:
        """Decode proximity sensor reading."""
        if len(payload) >= 2:
            distance_mm = struct.unpack('<H', payload[:2])[0]
            return distance_mm / 10.0  # Convert to cm
        return 400.0

    def decode_sensor_data(self, payload: bytes) -> dict:
        """Decode general sensor data packet."""
        if len(payload) >= 24:
            ax, ay, az = struct.unpack('<fff', payload[0:12])
            gx, gy, gz = struct.unpack('<fff', payload[12:24])
            return {
                'accel_x': ax, 'accel_y': ay, 'accel_z': az,
                'gyro_x': gx, 'gyro_y': gy, 'gyro_z': gz,
            }
        return {}


# ================================================================
#  ROBOT DOG BODY: The Full Integration
# ================================================================

class RobotDogBody:
    """CK's complete robot dog embodiment.

    This is the central integration class. One tick:
      1. Read sensors (or simulated readings)
      2. Feed through sensory codecs -> operators
      3. Fuse operators through CL -> body operator
      4. Map body operator -> gait mode
      5. Generate servo targets
      6. Update navigation state
      7. Encode UART packets (if in hardware mode)

    CK doesn't need to know he's a dog.
    He just knows what sensors he has and what actuators he can use.
    The math does the rest.
    """

    def __init__(self, simulated: bool = True):
        self.simulated = simulated

        # Body interface
        self.body = DogBody()
        self.body.start()

        # Sensor fusion
        self.fusion = SensorFusion()
        self.fusion.auto_register([
            'imu', 'proximity', 'motor', 'battery', 'temperature'
        ])

        # Gait controller
        self.gait = GaitController()

        # Navigation
        self.nav = NavigationState()

        # UART bridge (for real hardware)
        self.uart = UARTBridge()

        # State
        self._body_operator = VOID
        self._body_coherence = 0.0
        self._eak = (0.0, 0.0, 0.0)
        self._tick_count = 0
        self._btq_level = 1.0  # GREEN band default

        # Simulation state
        self._sim_battery_voltage = 8.2
        self._sim_temperature = 25.0
        self._sim_distance = 200.0

    def set_btq_level(self, level: float):
        """Set BTQ coherence level for gating motor output.

        Maps from coherence band:
          GREEN (>= 0.714) -> 1.0
          YELLOW (>= 0.4)  -> 0.6
          RED (< 0.4)      -> 0.3
        """
        self._btq_level = level
        self.gait.set_btq_level(level)

    def tick(self, sensor_readings: Optional[Dict[str, dict]] = None) -> dict:
        """One complete tick of the robot dog body.

        If sensor_readings is None and simulated=True, generates synthetic data.
        Returns tick result with operator, coherence, gait, navigation.
        """
        self._tick_count += 1

        # 1. Get sensor readings
        if sensor_readings is None and self.simulated:
            sensor_readings = self._simulate_sensors()

        if sensor_readings is None:
            sensor_readings = {}

        # 2. Feed through sensory codecs
        self._body_operator = self.fusion.feed_all(sensor_readings)
        self._body_coherence = self.fusion.body_coherence
        self._eak = self.fusion.body_eak()

        # 3. Update navigation FIRST (so obstacle distance is current)
        imu_data = sensor_readings.get('imu', {})
        self.nav.update_from_imu(
            imu_data.get('accel_x', 0.0),
            imu_data.get('accel_y', 0.0),
            imu_data.get('gyro_z', 0.0),
        )
        prox_data = sensor_readings.get('proximity', {})
        self.nav.update_obstacle(prox_data.get('distance_cm', 400.0))
        self.nav.record_operator(self._body_operator)

        # 4. Map operator -> gait mode
        gait_mode = OPERATOR_TO_GAIT.get(self._body_operator, GaitMode.IDLE)

        # Override: obstacle too close -> RETREAT
        if self.nav.obstacle_distance < 15:
            gait_mode = GaitMode.RETREAT

        # Override: low coherence -> IDLE (safety)
        if self._body_coherence < 0.2 and self._tick_count > 10:
            gait_mode = GaitMode.IDLE

        self.gait.set_mode(gait_mode)

        # 5. Generate servo targets
        targets = self.gait.tick()

        # 6. Encode UART packets (for hardware mode)
        if not self.simulated:
            self.uart.send_servo_targets(targets)

        # 7. Update body interface
        self.body.express({'motor_pos': targets})

        return {
            'tick': self._tick_count,
            'operator': self._body_operator,
            'operator_name': OP_NAMES[self._body_operator],
            'coherence': round(self._body_coherence, 3),
            'eak': tuple(round(v, 3) for v in self._eak),
            'gait': GAIT_NAMES[gait_mode],
            'nav': self.nav.stats(),
        }

    def _simulate_sensors(self) -> Dict[str, dict]:
        """Generate synthetic sensor data for simulation mode."""
        t = self._tick_count * 0.02  # 50 Hz

        # Simulate walking motion on IMU
        ax = 0.1 * math.sin(3.0 * t)
        ay = 0.05 * math.sin(6.0 * t)
        az = 9.81 + 0.2 * math.sin(6.0 * t)
        gx = 0.02 * math.sin(3.0 * t)
        gy = 0.01 * math.sin(3.0 * t)
        gz = 0.005 * math.sin(1.5 * t)

        # Simulate slow battery drain
        self._sim_battery_voltage = max(6.0,
            self._sim_battery_voltage - 0.00001)

        # Simulate slow temperature drift
        self._sim_temperature = 25.0 + 3.0 * math.sin(t * 0.01)

        # Simulate proximity (object oscillating)
        self._sim_distance = 200 + 150 * math.sin(t * 0.1)
        self._sim_distance = max(5.0, self._sim_distance)

        # Motor feedback (close to targets)
        motor_readings = {
            'position_deg': self.gait.targets[0] * 57.2958 if self.gait.targets else 0,
            'target_deg': self.gait.targets[0] * 57.2958 if self.gait.targets else 0,
            'load': 0.15 + 0.05 * abs(math.sin(t)),
            'speed': abs(self.gait.targets[0] * 57.2958 * 3.0) if self.gait.targets else 0,
        }

        return {
            'imu': {
                'accel_x': ax, 'accel_y': ay, 'accel_z': az,
                'gyro_x': gx, 'gyro_y': gy, 'gyro_z': gz,
            },
            'proximity': {
                'distance_cm': self._sim_distance,
                'max_range_cm': 400.0,
            },
            'motor': motor_readings,
            'battery': {
                'voltage': self._sim_battery_voltage,
                'current_a': 1.5 + 0.5 * abs(math.sin(t)),
                'voltage_max': 8.4,
                'voltage_min': 6.0,
            },
            'temperature': {
                'temp_c': self._sim_temperature,
            },
        }

    def emergency_stop(self):
        """Emergency stop: zero all motors, idle gait."""
        self.gait.emergency_stop()
        self.body.express({'motor_pos': [0.0] * 8})
        if not self.simulated:
            self.uart.send_estop()

    def process_rx_byte(self, byte: int):
        """Process incoming UART byte from hardware."""
        result = self.uart.feed_rx_byte(byte)
        if result is not None:
            pkt_type, payload = result
            if pkt_type == PKT_SERVO_POS:
                positions = self.uart.decode_servo_positions(payload)
                # Feed motor codec with actual positions
                for i, pos in enumerate(positions[:8]):
                    target = self.gait.targets[i] if i < len(self.gait.targets) else 0
                    self.fusion.feed('motor', {
                        'position_deg': math.degrees(pos),
                        'target_deg': math.degrees(target),
                        'load': 0.2,
                        'speed': 0.0,
                    })
            elif pkt_type == PKT_PROXIMITY:
                dist = self.uart.decode_proximity(payload)
                self.fusion.feed('proximity', {
                    'distance_cm': dist,
                    'max_range_cm': 400.0,
                })
            elif pkt_type == PKT_SENSOR:
                imu_data = self.uart.decode_sensor_data(payload)
                if imu_data:
                    self.fusion.feed('imu', imu_data)

    @property
    def body_operator(self) -> int:
        return self._body_operator

    @property
    def body_coherence(self) -> float:
        return self._body_coherence

    @property
    def body_eak(self) -> Tuple[float, float, float]:
        return self._eak

    def stats(self) -> dict:
        """Full robot body statistics."""
        return {
            'tick_count': self._tick_count,
            'body_operator': OP_NAMES[self._body_operator],
            'body_coherence': round(self._body_coherence, 3),
            'eak': {
                'error': round(self._eak[0], 3),
                'activation': round(self._eak[1], 3),
                'knowledge': round(self._eak[2], 3),
            },
            'gait': self.gait.stats(),
            'nav': self.nav.stats(),
            'sensor_fusion': self.fusion.stats(),
            'btq_level': round(self._btq_level, 3),
            'simulated': self.simulated,
        }

    def stop(self):
        """Graceful shutdown."""
        self.emergency_stop()
        self.body.stop()


# ================================================================
#  BEHAVIOR PLANNER: Operator Chain -> Action Sequence
# ================================================================

class BehaviorPlanner:
    """Translates operator chains into multi-step behavior plans.

    This is where CK's "thinking" meets "doing." The operator chain
    from the heartbeat/world lattice drives a sequence of actions.

    Example:
      [COUNTER, PROGRESS, HARMONY] -> scan, walk_forward, approach
      [COLLAPSE, RESET, PROGRESS]  -> retreat, return_home, resume_walk
    """

    def __init__(self):
        self._plan: List[dict] = []
        self._plan_index = 0
        self._current_action = 'idle'

    def plan_from_operators(self, op_chain: List[int],
                            btq_level: float = 1.0) -> List[dict]:
        """Generate an action plan from an operator chain.

        Each operator maps to a motor command via OPERATOR_TO_BEHAVIOR,
        gated by BTQ level.
        """
        self._plan = []
        for op in op_chain:
            cmd = operator_to_motor_command(op, btq_level)
            self._plan.append(cmd)
        self._plan_index = 0
        return self._plan

    def next_action(self) -> Optional[dict]:
        """Get the next action in the plan."""
        if self._plan_index < len(self._plan):
            action = self._plan[self._plan_index]
            self._plan_index += 1
            self._current_action = action['action']
            return action
        return None

    @property
    def current_action(self) -> str:
        return self._current_action

    @property
    def plan_remaining(self) -> int:
        return max(0, len(self._plan) - self._plan_index)

    def clear(self):
        """Clear current plan."""
        self._plan.clear()
        self._plan_index = 0
        self._current_action = 'idle'


# ================================================================
#  CLI: Run the Robot Dog Simulation
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK ROBOT DOG -- Physical Embodiment Simulation")
    print("=" * 60)

    robot = RobotDogBody(simulated=True)
    planner = BehaviorPlanner()

    print(f"\n  Body: {robot.body.spec.name}")
    print(f"  Sensors: {list(robot.fusion.codecs.keys())}")
    print(f"  Motors: {robot.body.spec.n_motors}")
    print(f"  Battery: {robot.body.spec.battery_wh} Wh")

    print("\n  Running 200 ticks...\n")

    for i in range(200):
        result = robot.tick()

        if i % 50 == 0:
            print(f"  tick={result['tick']:4d}  "
                  f"op={result['operator_name']:8s}  "
                  f"coh={result['coherence']:.3f}  "
                  f"gait={result['gait']:8s}  "
                  f"pos=({result['nav']['position'][0]:.2f}, "
                  f"{result['nav']['position'][1]:.2f})  "
                  f"obstacle={result['nav']['obstacle_cm']:.0f}cm")

    stats = robot.stats()
    print(f"\n  Final operator: {stats['body_operator']}")
    print(f"  Final coherence: {stats['body_coherence']}")
    print(f"  Final gait: {stats['gait']['mode']}")
    print(f"  E/A/K: E={stats['eak']['error']:.3f} "
          f"A={stats['eak']['activation']:.3f} "
          f"K={stats['eak']['knowledge']:.3f}")
    print(f"  Path coherence: {stats['nav']['path_coherence']}")
    print(f"  Distance from origin: {stats['nav']['dist_from_origin']}m")

    # Test behavior planner
    print("\n  Behavior plan from [COUNTER, PROGRESS, HARMONY]:")
    plan = planner.plan_from_operators([COUNTER, PROGRESS, HARMONY])
    for step in plan:
        print(f"    {step['operator_name']:8s} -> {step['action']:10s} "
              f"(intensity={step['btq_gated']:.1f})")

    robot.stop()
    print("\n  Robot stopped.")
    print("=" * 60)
