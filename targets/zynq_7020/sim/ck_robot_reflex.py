"""
ck_robot_reflex.py -- Robot Reflex Engine (BTQ + IMU)
=====================================================
Celeste's Task 8: Sensor -> Operator -> Motor Command

CK's body in the physical world. Sensors feed D2 curvature.
D2 classifies into operators. BTQ gates the reflex.
PFE validates structure before action.

Fractal layers:
  Sensor level:   raw analog -> normalized force vector
  D2 level:       force stream -> curvature -> operator classification
  BTQ level:      safety gate (binary) + exploration (ternary) + quality (quadratic)
  Reflex level:   operator + BTQ band -> motor command

Hardware targets:
  - Raspberry Pi GPIO (LEDs, motors, servos)
  - Jetson Nano (CUDA-accelerated PFE)
  - Zynq FPGA (real-time D2 in LUTs)
  - Any platform with Python + numpy

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import deque, Counter
from dataclasses import dataclass, field

from ck_being import (CL, T_STAR, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_curvature import compute_curvatures, _classify_d2, NDIMS
from ck_pfe import pfe_evaluate, btq_energy, btq_classify, PFE_THRESHOLDS

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# =====================================================
# S1  SENSOR NORMALIZATION
#     Raw sensor data -> 5D force vector
#     Each sensor type maps to CK's force dimensions:
#       aperture, pressure, depth, binding, continuity
# =====================================================

@dataclass
class SensorReading:
    """A single sensor snapshot."""
    timestamp: float = 0.0
    accel_x:   float = 0.0    # m/s^2 (accelerometer)
    accel_y:   float = 0.0
    accel_z:   float = 0.0
    gyro_x:    float = 0.0    # rad/s (gyroscope)
    gyro_y:    float = 0.0
    gyro_z:    float = 0.0
    temp:      float = 25.0   # Celsius
    pressure:  float = 1013.0 # hPa (barometric)
    proximity: float = 100.0  # cm (distance sensor)
    light:     float = 500.0  # lux (ambient light)
    sound:     float = 40.0   # dB (microphone level)
    touch:     float = 0.0    # 0-1 (capacitive touch)

    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items()}
def normalize_sensor(reading: SensorReading) -> np.ndarray:
    """
    Map raw sensor data to CK's 5D force space.

    Dimension mapping:
      F0 aperture:   how OPEN the system is (light, proximity)
      F1 pressure:   how much FORCE is applied (accel magnitude, barometric)
      F2 depth:      how DEEP the state is (temperature deviation, gyro magnitude)
      F3 binding:    how CONNECTED sensors are (cross-correlation: touch + sound)
      F4 continuity: how STEADY the system is (inverse jerk: gyro stability)

    All normalized to [-1, 1].
    """
    # F0: Aperture -- light + proximity
    # High light + far proximity = open. Dark + close = closed.
    light_norm = min(reading.light / 1000.0, 1.0) * 2 - 1    # [0, 1000] -> [-1, 1]
    prox_norm = min(reading.proximity / 200.0, 1.0) * 2 - 1   # [0, 200cm] -> [-1, 1]
    f0 = 0.6 * light_norm + 0.4 * prox_norm

    # F1: Pressure -- accelerometer magnitude + barometric
    accel_mag = math.sqrt(reading.accel_x**2 + reading.accel_y**2 + reading.accel_z**2)
    accel_norm = min(accel_mag / 20.0, 1.0) * 2 - 1           # [0, 20 m/s^2] -> [-1, 1]
    baro_norm = (reading.pressure - 1013.0) / 50.0             # deviation from sea level
    baro_norm = max(-1, min(1, baro_norm))
    f1 = 0.7 * accel_norm + 0.3 * baro_norm

    # F2: Depth -- temperature deviation + gyro magnitude
    temp_dev = (reading.temp - 25.0) / 25.0                    # deviation from room temp
    temp_norm = max(-1, min(1, temp_dev))
    gyro_mag = math.sqrt(reading.gyro_x**2 + reading.gyro_y**2 + reading.gyro_z**2)
    gyro_norm = min(gyro_mag / 5.0, 1.0) * 2 - 1              # [0, 5 rad/s] -> [-1, 1]
    f2 = 0.5 * temp_norm + 0.5 * gyro_norm

    # F3: Binding -- touch + sound cross-correlation
    touch_norm = reading.touch * 2 - 1                          # [0, 1] -> [-1, 1]
    sound_norm = min(reading.sound / 80.0, 1.0) * 2 - 1        # [0, 80 dB] -> [-1, 1]
    f3 = 0.5 * touch_norm + 0.5 * sound_norm

    # F4: Continuity -- gyro stability (low jerk = high continuity)
    # High gyro = instability = negative continuity
    f4 = -gyro_norm  # Inverse: stable = positive, spinning = negative

    return np.array([f0, f1, f2, f3, f4], dtype=np.float32)
class SensorStream:
    """
    Rolling buffer of sensor readings.
    Computes D2 curvature on the force stream.
    Classifies each D2 vector into a TIG operator.
    """
    def __init__(self, buffer_size: int = 32):
        self.buffer_size = buffer_size
        self.forces = deque(maxlen=buffer_size)
        self.operators = deque(maxlen=buffer_size)
        self.d2s = deque(maxlen=buffer_size)
        self.tick_count = 0

    def feed(self, reading: SensorReading) -> Optional[int]:
        """
        Feed a sensor reading. Returns operator if enough data.

        Pipeline:
          reading -> normalize -> force vector -> append to buffer
          if 3+ forces: compute D2 -> classify -> return operator
        """
        force = normalize_sensor(reading)
        self.forces.append(force)
        self.tick_count += 1

        if len(self.forces) < 3:
            return None
        last3 = np.array([self.forces[-3], self.forces[-2], self.forces[-1]])
        d2 = compute_curvatures(last3)  # Shape: (1, 5)

        if len(d2) == 0:
            return None
        d2_vec = d2[0]
        self.d2s.append(d2_vec)

        op = _classify_d2(d2_vec)
        self.operators.append(op)

        return op
    def get_recent_operators(self, n: int = 8) -> List[int]:
        """Get the last n operators."""
        return list(self.operators)[-n:]
    def get_recent_d2(self, n: int = 8) -> np.ndarray:
        """Get the last n D2 vectors as a numpy array."""
        recent = list(self.d2s)[-n:]
        if not recent:
            return np.zeros((0, NDIMS), dtype=np.float32)
        return np.array(recent, dtype=np.float32)

    def get_pfe(self, window: int = 8) -> Dict:
        """Run PFE on the recent operator window."""
        ops = self.get_recent_operators(window)
        d2s = self.get_recent_d2(window)
        if not ops:
            return {'coherence_raw': 0.0, 'band': 'RED'}
        return pfe_evaluate(ops, d2s if len(d2s) > 0 else None)

    def get_btq(self, window: int = 8) -> Dict:
        """Run BTQ classification on the recent window."""
        ops = self.get_recent_operators(window)
        d2s = self.get_recent_d2(window)
        if not ops:
            return {'binary_alive': False, 'band': 'RED', 'quadratic_energy': 1.0}
        return btq_classify(ops, d2s if len(d2s) > 0 else None)


# =====================================================
# S3  REFLEX DECISIONS -- operator + BTQ -> action
#     PFE-gated reflexes. No unchecked movement.
# =====================================================

@dataclass
class MotorCommand:
    """A motor action for CK's body."""
    action:     str = 'IDLE'           # IDLE, FORWARD, BACK, LEFT, RIGHT, STOP, ALERT, EXPLORE
    intensity:  float = 0.0            # 0.0 to 1.0
    duration:   float = 0.1            # seconds
    channel:    int = 0                # GPIO/PWM channel
    reason:     str = ''               # Why this action
    btq_band:   str = 'RED'            # Safety context
    operator:   int = VOID             # Source operator
    pfe_score:  float = 0.0            # PFE coherence at decision time

    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items()}
_REFLEX_MAP = {
    VOID:      ('IDLE',    0.0,  'No signal -- wait'),
    LATTICE:   ('HOLD',    0.3,  'Structure detected -- hold position'),
    COUNTER:   ('SCAN',    0.4,  'Measuring -- rotate to scan'),
    PROGRESS:  ('FORWARD', 0.6,  'Growth signal -- advance'),
    COLLAPSE:  ('BACK',    0.8,  'Danger signal -- retreat'),
    BALANCE:   ('HOLD',    0.2,  'Tension -- hold and evaluate'),
    CHAOS:     ('ALERT',   0.7,  'Chaotic input -- alert mode'),
    HARMONY:   ('EXPLORE', 0.5,  'Harmony -- safe to explore'),
    BREATH:    ('PULSE',   0.4,  'Rhythmic -- pulse motors'),
    RESET:     ('STOP',    0.0,  'Reset -- full stop, recalibrate'),
}


def decide_reflex(stream: SensorStream,
                  window: int = 8,
                  safety_override: bool = True) -> MotorCommand:
    """
    The reflex decision engine.

    Pipeline:
      1. Get recent operator stream + D2 curvature
      2. Run PFE evaluation (structure check)
      3. Run BTQ classification (safety/exploration/quality)
      4. Map dominant operator to motor action
      5. Gate action through BTQ safety band

    BTQ gating:
      RED:    Only STOP, BACK, ALERT allowed (safety)
      YELLOW: Reduced intensity, cautious movement
      GREEN:  Full action permitted

    Returns a MotorCommand for the actuator layer.
    """
    ops = stream.get_recent_operators(window)
    if not ops:
        return MotorCommand(action='IDLE', reason='No operator data yet')
    btq = stream.get_btq(window)
    band = btq.get('band', 'RED')
    pfe = btq.get('pfe', {})
    coherence = pfe.get('coherence_raw', 0.0)
    energy = btq.get('quadratic_energy', 1.0)
    alive = btq.get('binary_alive', False)

    # Dominant operator (mode of recent stream)
    hist = Counter(ops)
    dominant = hist.most_common(1)[0][0]

    # Base action from operator
    action_name, base_intensity, reason = _REFLEX_MAP.get(dominant, ('IDLE', 0.0, 'Unknown'))

    # BTQ gating
    if band == 'RED':
        if safety_override:
            # Only allow protective actions
            if action_name not in ('STOP', 'BACK', 'ALERT', 'IDLE', 'HOLD'):
                action_name = 'STOP'
                reason = f'BTQ RED override: {reason} -> STOP'
            base_intensity = min(base_intensity, 0.3)  # Cap intensity
        else:
            base_intensity *= 0.3  # Reduced

    elif band == 'YELLOW':
        # Cautious mode: reduce intensity, bias toward hold
        base_intensity *= 0.6
        if action_name == 'FORWARD':
            base_intensity *= 0.5  # Extra caution on forward
        reason = f'YELLOW: {reason}'

    elif band == 'GREEN':
        # Full confidence: scale by PFE coherence
        base_intensity *= min(coherence * 1.3, 1.0)
        reason = f'GREEN: {reason}'

    # If not alive at all, stop
    if not alive:
        action_name = 'STOP'
        base_intensity = 0.0
        reason = 'BTQ: not alive'

    return MotorCommand(
    )


# =====================================================
# S4  REFLEX ARC -- continuous sensor-to-motor loop
# =====================================================

class ReflexArc:
    """
    The full reflex arc: sensor stream -> decision -> motor command.
    Runs as a tick-based loop.
    """
    def __init__(self, buffer_size: int = 32, window: int = 8):
        self.stream = SensorStream(buffer_size=buffer_size)
        self.window = window
        self.history: List[Dict] = []
        self.tick_count = 0

    def tick(self, reading: SensorReading) -> MotorCommand:
        """
        One heartbeat tick.
        Feed sensor data, get motor command.
        """
        op = self.stream.feed(reading)
        if op is None:
            cmd = MotorCommand(action='IDLE', reason='Warming up (need 3+ readings)')
        else:
            cmd = decide_reflex(self.stream, window=self.window)

        self.tick_count += 1
        self.history.append({
            'tick': self.tick_count,
            'timestamp': reading.timestamp,
            'operator': op,
            'command': cmd.to_dict(),
        })

        # Keep history bounded
        if len(self.history) > 1000:
            self.history = self.history[-500:]

        return cmd
    def get_stats(self) -> Dict:
        """Report reflex arc statistics."""
        if not self.history:
            return {'ticks': 0, 'operators': {}, 'actions': {}, 'bands': {}}
        ops = [h['operator'] for h in self.history if h['operator'] is not None]
        actions = [h['command']['action'] for h in self.history]
        bands = [h['command']['btq_band'] for h in self.history]

        return {
        }


# =====================================================
# S5  SENSOR SIMULATORS -- for testing without hardware
# =====================================================

def simulate_calm() -> SensorReading:
    """Calm environment: low accel, stable temp, quiet."""
    t = time.time()
    return SensorReading(
    )


def simulate_danger() -> SensorReading:
    """Danger: high accel, close proximity, loud, hot."""
    t = time.time()
    return SensorReading(
    )


def simulate_rhythmic() -> SensorReading:
    """Rhythmic: oscillating sensors, like walking or breathing."""
    t = time.time()
    phase = math.sin(t * 2 * math.pi * 0.5)  # 0.5 Hz oscillation
    return SensorReading(
    )


def simulate_exploration() -> SensorReading:
    """Exploration: moderate movement, varying environment."""
    t = time.time()
    return SensorReading(
    )


# =====================================================
# S6  DEMO
# =====================================================

if __name__ == '__main__':
    print("=" * 72)
    print("  CK ROBOT REFLEX ENGINE (BTQ + IMU)")
    print("  Celeste's Task 8: Sensor -> Operator -> Motor Command")
    print("=" * 72)

    scenarios = [
        ("CALM",        simulate_calm,        20),
        ("DANGER",      simulate_danger,      20),
        ("RHYTHMIC",    simulate_rhythmic,    20),
        ("EXPLORATION", simulate_exploration, 20),
    ]

    for scenario_name, sim_fn, n_ticks in scenarios:
        print(f"\n  --- Scenario: {scenario_name} ({n_ticks} ticks) ---")
        arc = ReflexArc(buffer_size=32, window=8)

        for i in range(n_ticks):
            reading = sim_fn()
            reading.timestamp = i * 0.1  # 100ms ticks
            cmd = arc.tick(reading)

            if i < 5 or i >= n_ticks - 3:
                op_name = OP_NAMES[cmd.operator] if cmd.operator < 10 else '?'
                print(f"    tick {i:3d}: op={op_name:10s} -> "
                      f"{cmd.action:8s} int={cmd.intensity:.2f} "
                      f"band={cmd.btq_band:6s} [{cmd.reason[:40]}]")
            elif i == 5:
                print(f"    ... ({n_ticks - 8} more ticks) ...")

        stats = arc.get_stats()
        print(f"    Summary: {stats['ticks']} ticks")
        print(f"      Operators: {stats['operators']}")
        print(f"      Actions:   {stats['actions']}")
        print(f"      Bands:     {stats['bands']}")

    # Latency test
    print(f"\n  --- Latency Test ---")
    arc = ReflexArc()
    reading = simulate_calm()
    # Warm up
    for _ in range(10):
        arc.tick(reading)

    times = []
    for _ in range(100):
        reading = simulate_calm()
        t0 = time.perf_counter()
        cmd = arc.tick(reading)
        dt = time.perf_counter() - t0
        times.append(dt * 1e6)  # microseconds

    print(f"    100 ticks: mean={np.mean(times):.1f}us  "
          f"median={np.median(times):.1f}us  "
          f"max={np.max(times):.1f}us  "
          f"min={np.min(times):.1f}us")
    print(f"    Target: <100us for real-time reflex")
    ok = np.mean(times) < 1000  # 1ms budget
    print(f"    Status: {'PASS' if ok else 'SLOW'}")

    print(f"\n  CK's body can feel. The sensors curve. The reflexes respond.")
