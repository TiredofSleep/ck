"""
ck_sensory_codecs.py -- Universal Sensory Codecs: Any Signal → D2 → Operator
==============================================================================
Operator: COUNTER (2) -- CK measures everything.

THE FRACTAL INSIGHT:
  D2 curvature is not just for text. It's the universal measurement.
  The same 5D force vector (aperture, pressure, depth, binding, continuity)
  that maps letters → operators also maps:
    - audio frequencies → operators (ck_ears.h already does this)
    - IMU acceleration → operators
    - motor feedback → operators
    - proximity readings → operators
    - battery voltage → operators
    - temperature → operators

One codec. Many skins. Same math at every scale.

How it works:
  1. Raw sensor reading → normalize to [0, 1]
  2. Map normalized value to 5D force vector via sensor-specific mapping
  3. Feed force vector into D2 pipeline (same Q1.14 math as text)
  4. D2 curvature classifies → operator
  5. Operator feeds into CL composition → coherence

CK doesn't care WHERE the signal comes from.
CK only sees operator patterns and how they compose.

Sensor Mapping to 5D Force Vectors:
  aperture   = how "open" the signal is (range/bandwidth)
  pressure   = how "strong" the signal is (magnitude/force)
  depth      = how "deep" the signal is (frequency/complexity)
  binding    = how "connected" the signal is (correlation/periodicity)
  continuity = how "stable" the signal is (persistence/smoothness)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Tuple, Optional

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline


# ================================================================
#  D2 CURVATURE ENGINE (shared by all codecs)
# ================================================================

class CurvatureEngine:
    """Compute D2 curvature on any stream of 5D force vectors.

    This is the same second-derivative math as the text D2 pipeline,
    but generalized to accept force vectors from any sensor.

    D2 = v[t-2] - 2*v[t-1] + v[t]  (per dimension)

    The curvature magnitude determines operator classification.
    """

    def __init__(self, history_size: int = 3):
        self.history: List[List[float]] = []
        self.history_size = history_size
        self.d2_float = [0.0] * 5
        self.operator = VOID
        self._classify_boundaries = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    def feed(self, force_vec: List[float]) -> bool:
        """Feed a 5D force vector. Returns True when D2 is computed.

        Needs at least 3 vectors to compute second derivative.
        """
        self.history.append(force_vec[:])
        if len(self.history) > self.history_size:
            self.history.pop(0)

        if len(self.history) < 3:
            return False

        # D2 = v[0] - 2*v[1] + v[2]
        v0, v1, v2 = self.history[-3], self.history[-2], self.history[-1]
        for i in range(5):
            self.d2_float[i] = v0[i] - 2.0 * v1[i] + v2[i]

        # Classify: magnitude → operator (same as D2Pipeline)
        magnitude = sum(abs(d) for d in self.d2_float)
        self.operator = self._classify(magnitude)
        return True

    def _classify(self, magnitude: float) -> int:
        """Map curvature magnitude to operator.

        Same classification scheme as ck_sim_d2.py:
        Low curvature → HARMONY (smooth/stable)
        High curvature → CHAOS/COLLAPSE (turbulent/breaking)
        """
        # Normalize magnitude to [0, 1] range (typical max ~2.0)
        norm = min(magnitude / 2.0, 1.0)

        if norm < 0.05:
            return VOID       # Zero curvature: nothing happening
        elif norm < 0.15:
            return HARMONY     # Very smooth
        elif norm < 0.25:
            return BREATH      # Gentle rhythm
        elif norm < 0.35:
            return BALANCE     # Equilibrium
        elif norm < 0.45:
            return LATTICE     # Structure forming
        elif norm < 0.55:
            return COUNTER     # Measuring/observing
        elif norm < 0.65:
            return PROGRESS    # Moving forward
        elif norm < 0.75:
            return RESET       # Transition
        elif norm < 0.85:
            return CHAOS       # Turbulent
        else:
            return COLLAPSE    # Breaking apart

    def reset(self):
        """Clear history."""
        self.history.clear()
        self.d2_float = [0.0] * 5
        self.operator = VOID


# ================================================================
#  BASE CODEC: All sensors implement this
# ================================================================

class SensorCodec:
    """Base class for all sensor codecs.

    Every sensor in CK's body produces the same output:
    - A 5D force vector (aperture, pressure, depth, binding, continuity)
    - A D2 curvature classification → operator
    - A coherence contribution to the heartbeat

    Subclasses implement map_to_force_vector() for their specific sensor.
    """

    def __init__(self, name: str, sample_rate_hz: float = 50.0):
        self.name = name
        self.sample_rate_hz = sample_rate_hz
        self.engine = CurvatureEngine()
        self.last_force_vec = [0.0] * 5
        self.last_operator = VOID
        self.operator_history: deque = deque(maxlen=32)
        self._tick_count = 0

    def map_to_force_vector(self, raw_reading: dict) -> List[float]:
        """Map raw sensor reading to 5D force vector.

        Subclasses MUST override this.

        Returns: [aperture, pressure, depth, binding, continuity]
                 each in [0.0, 1.0]
        """
        raise NotImplementedError

    def feed(self, raw_reading: dict) -> int:
        """Feed a raw sensor reading through the codec.

        Returns the classified operator (0-9).
        """
        force_vec = self.map_to_force_vector(raw_reading)
        self.last_force_vec = force_vec

        if self.engine.feed(force_vec):
            self.last_operator = self.engine.operator
            self.operator_history.append(self.last_operator)

        self._tick_count += 1
        return self.last_operator

    def coherence(self) -> float:
        """Compute local coherence from operator history.

        Same as heartbeat coherence: harmony_count / window_size.
        """
        if not self.operator_history:
            return 0.0
        harmony_count = sum(1 for op in self.operator_history if op == HARMONY)
        return harmony_count / len(self.operator_history)

    def fuse(self) -> int:
        """Fuse entire operator history through CL.

        Returns the running fuse operator.
        """
        if not self.operator_history:
            return VOID
        result = self.operator_history[0]
        for i in range(1, len(self.operator_history)):
            result = compose(result, self.operator_history[i])
        return result

    def stats(self) -> dict:
        """Codec statistics."""
        from collections import Counter
        op_counts = Counter(self.operator_history)
        return {
            'name': self.name,
            'ticks': self._tick_count,
            'last_operator': OP_NAMES[self.last_operator],
            'coherence': round(self.coherence(), 3),
            'fuse': OP_NAMES[self.fuse()],
            'operator_distribution': {
                OP_NAMES[op]: count
                for op, count in sorted(op_counts.items())
            },
        }


# ================================================================
#  IMU CODEC: Accelerometer + Gyroscope → Operator
# ================================================================

class IMUCodec(SensorCodec):
    """Inertial Measurement Unit → D2 → Operator.

    Maps 6-axis IMU (3 accel + 3 gyro) to 5D force vector:
      aperture   = angular range (gyro magnitude)
      pressure   = linear force (accel magnitude)
      depth      = vertical component (accel_z dominance)
      binding    = rotational coupling (gyro-accel correlation)
      continuity = stability (inverse of jerk)

    Expected raw_reading keys:
      accel_x, accel_y, accel_z: m/s^2 (typical range: -20 to +20)
      gyro_x, gyro_y, gyro_z: rad/s (typical range: -10 to +10)
    """

    # Normalization constants (for typical MPU6050 range)
    ACCEL_MAX = 20.0   # m/s^2 (2g)
    GYRO_MAX = 10.0    # rad/s (~573 deg/s)

    def __init__(self):
        super().__init__('imu', sample_rate_hz=500.0)
        self._prev_accel_mag = 0.0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        ax = raw.get('accel_x', 0.0)
        ay = raw.get('accel_y', 0.0)
        az = raw.get('accel_z', 0.0)
        gx = raw.get('gyro_x', 0.0)
        gy = raw.get('gyro_y', 0.0)
        gz = raw.get('gyro_z', 0.0)

        # Magnitudes
        accel_mag = math.sqrt(ax*ax + ay*ay + az*az)
        gyro_mag = math.sqrt(gx*gx + gy*gy + gz*gz)

        # aperture: angular range [0, 1]
        aperture = min(gyro_mag / self.GYRO_MAX, 1.0)

        # pressure: linear force [0, 1]
        pressure = min(accel_mag / self.ACCEL_MAX, 1.0)

        # depth: vertical dominance [0, 1]
        # When az dominates, depth is high (upright/falling)
        depth = abs(az) / max(accel_mag, 0.01)

        # binding: gyro-accel correlation [0, 1]
        # High when both are active (tumbling), low when static
        binding = min((accel_mag * gyro_mag) / (self.ACCEL_MAX * self.GYRO_MAX), 1.0)

        # continuity: stability (inverse jerk) [0, 1]
        jerk = abs(accel_mag - self._prev_accel_mag)
        self._prev_accel_mag = accel_mag
        continuity = max(0.0, 1.0 - jerk / 5.0)

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  PROXIMITY CODEC: Ultrasonic/IR → Operator
# ================================================================

class ProximityCodec(SensorCodec):
    """Distance sensor → D2 → Operator.

    Maps ultrasonic/IR distance readings to 5D force vector:
      aperture   = detection range (how far sensor reaches)
      pressure   = closeness (inverse distance, normalized)
      depth      = below/above threshold (danger zone proximity)
      binding    = object persistence (same distance over time)
      continuity = smoothness (no sudden jumps)

    Expected raw_reading keys:
      distance_cm: float (0 to 400 for ultrasonic, 0 to 80 for IR)
      max_range_cm: float (sensor's maximum range)
    """

    def __init__(self):
        super().__init__('proximity', sample_rate_hz=20.0)
        self._prev_distance = 100.0
        self._stable_count = 0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        dist = raw.get('distance_cm', 100.0)
        max_range = raw.get('max_range_cm', 400.0)

        # Clamp
        dist = max(0.0, min(dist, max_range))

        # aperture: normalized detection range
        aperture = dist / max_range

        # pressure: closeness (inverse — closer = more pressure)
        pressure = max(0.0, 1.0 - dist / max_range)

        # depth: danger zone (< 30cm = high depth)
        danger_threshold = 30.0
        if dist < danger_threshold:
            depth = 1.0 - (dist / danger_threshold)
        else:
            depth = 0.0

        # binding: object persistence (stable distance = high binding)
        delta = abs(dist - self._prev_distance)
        if delta < 5.0:
            self._stable_count = min(self._stable_count + 1, 10)
        else:
            self._stable_count = max(self._stable_count - 2, 0)
        binding = self._stable_count / 10.0
        self._prev_distance = dist

        # continuity: smoothness
        continuity = max(0.0, 1.0 - delta / 50.0)

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  MOTOR FEEDBACK CODEC: Servo Position/Load → Operator
# ================================================================

class MotorCodec(SensorCodec):
    """Motor feedback → D2 → Operator.

    Maps servo position and load feedback to 5D force vector:
      aperture   = range of motion used (position / max_position)
      pressure   = torque/load on motor
      depth      = position error (commanded vs actual)
      binding    = motor coupling (correlation between joints)
      continuity = smoothness of movement

    Expected raw_reading keys:
      position_deg: float (current servo angle)
      target_deg: float (commanded angle)
      load: float (0.0 to 1.0, normalized torque)
      speed: float (deg/s)
    """

    def __init__(self, max_angle: float = 180.0):
        super().__init__('motor', sample_rate_hz=50.0)
        self.max_angle = max_angle
        self._prev_position = 0.0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        pos = raw.get('position_deg', 0.0)
        target = raw.get('target_deg', 0.0)
        load = raw.get('load', 0.0)
        speed = raw.get('speed', 0.0)

        # aperture: range of motion [0, 1]
        aperture = abs(pos) / self.max_angle

        # pressure: torque load [0, 1]
        pressure = min(abs(load), 1.0)

        # depth: position error [0, 1]
        error = abs(target - pos) / self.max_angle
        depth = min(error, 1.0)

        # binding: correlation with target (low error = high binding)
        binding = max(0.0, 1.0 - error * 5.0)

        # continuity: movement smoothness
        delta = abs(pos - self._prev_position)
        self._prev_position = pos
        continuity = max(0.0, 1.0 - delta / 45.0)  # 45 deg jump = discontinuous

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  BATTERY CODEC: Power State → Operator
# ================================================================

class BatteryCodec(SensorCodec):
    """Battery monitor → D2 → Operator.

    Maps battery voltage/current to 5D force vector:
      aperture   = charge level (voltage / max_voltage)
      pressure   = current draw (load on battery)
      depth      = depth of discharge (how deep into reserve)
      binding    = voltage stability (no sag under load)
      continuity = discharge smoothness (no sudden drops)

    Expected raw_reading keys:
      voltage: float (e.g., 7.4V for 2S LiPo)
      current_a: float (amps being drawn)
      voltage_max: float (fully charged voltage)
      voltage_min: float (cutoff voltage)
    """

    def __init__(self):
        super().__init__('battery', sample_rate_hz=1.0)
        self._prev_voltage = 0.0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        voltage = raw.get('voltage', 7.4)
        current = raw.get('current_a', 0.0)
        v_max = raw.get('voltage_max', 8.4)  # 2S LiPo full
        v_min = raw.get('voltage_min', 6.0)  # 2S LiPo cutoff

        v_range = max(v_max - v_min, 0.01)
        charge_pct = max(0.0, min((voltage - v_min) / v_range, 1.0))

        # aperture: charge level
        aperture = charge_pct

        # pressure: current draw (normalized to typical max ~5A)
        pressure = min(abs(current) / 5.0, 1.0)

        # depth: depth of discharge (inverse of charge)
        depth = 1.0 - charge_pct

        # binding: voltage stability
        delta_v = abs(voltage - self._prev_voltage)
        binding = max(0.0, 1.0 - delta_v / 0.5)  # 0.5V sag = zero binding
        self._prev_voltage = voltage

        # continuity: smooth discharge
        continuity = max(0.0, 1.0 - delta_v / 0.2)

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  TEMPERATURE CODEC: Thermal State → Operator
# ================================================================

class TemperatureCodec(SensorCodec):
    """Temperature sensor → D2 → Operator.

    Maps temperature to 5D force vector:
      aperture   = normalized temp (in comfortable range)
      pressure   = deviation from optimal (how far from 25C)
      depth      = extreme heat/cold depth
      binding    = thermal stability (not changing fast)
      continuity = smoothness of thermal curve

    Expected raw_reading keys:
      temp_c: float (degrees Celsius)
    """

    def __init__(self, optimal_c: float = 25.0):
        super().__init__('temperature', sample_rate_hz=0.1)
        self.optimal_c = optimal_c
        self._prev_temp = optimal_c

    def map_to_force_vector(self, raw: dict) -> List[float]:
        temp = raw.get('temp_c', self.optimal_c)

        # aperture: normalized in range [0, 50] → [0, 1]
        aperture = max(0.0, min(temp / 50.0, 1.0))

        # pressure: deviation from optimal
        deviation = abs(temp - self.optimal_c) / 30.0
        pressure = min(deviation, 1.0)

        # depth: extreme (< 0C or > 45C)
        if temp < 0:
            depth = min(abs(temp) / 20.0, 1.0)
        elif temp > 45:
            depth = min((temp - 45) / 20.0, 1.0)
        else:
            depth = 0.0

        # binding: stability
        delta = abs(temp - self._prev_temp)
        binding = max(0.0, 1.0 - delta / 5.0)
        self._prev_temp = temp

        # continuity: smooth thermal curve
        continuity = max(0.0, 1.0 - delta / 2.0)

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  VISION CODEC: Camera Frame Statistics → Operator
# ================================================================

class VisionCodec(SensorCodec):
    """Camera frame statistics → D2 → Operator.

    Maps pre-computed camera frame statistics to 5D force vector.
    The raw reading contains normalized [0, 1] metrics extracted
    from each video frame (edge detection, luminance, optical flow,
    etc.).  This codec does NOT process pixels -- it consumes the
    summary statistics that a vision pipeline (OpenCV / DepthAI)
    has already computed.

    Mapping to 5D force vector:
      aperture   = brightness (how open/lit the visual field is)
      pressure   = motion_magnitude (visual "force" = movement)
      depth      = edge_density (visual complexity/structure depth)
      binding    = 1 - color_variance (uniform = bound, chaotic = unbound)
      continuity = focus * (1 - |Δmotion| * 2)  (sharp + steady = continuous)

    Expected raw_reading keys:
      edge_density:     float [0, 1] -- edges detected (Canny-like)
      brightness:       float [0, 1] -- average frame luminance
      contrast:         float [0, 1] -- std-dev of luminance
      motion_magnitude: float [0, 1] -- optical flow magnitude (0=still, 1=fast)
      color_variance:   float [0, 1] -- how colorful/varied the scene is
      focus:            float [0, 1] -- sharpness quality (Laplacian variance, normalised)
    """

    def __init__(self):
        super().__init__('vision', sample_rate_hz=30.0)
        self._prev_motion = 0.0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        edge_density     = raw.get('edge_density', 0.0)
        brightness       = raw.get('brightness', 0.5)
        contrast         = raw.get('contrast', 0.0)
        motion_magnitude = raw.get('motion_magnitude', 0.0)
        color_variance   = raw.get('color_variance', 0.0)
        focus            = raw.get('focus', 0.5)

        # aperture: how open/lit the visual field is
        aperture = max(0.0, min(brightness, 1.0))

        # pressure: visual "force" — movement in the scene
        pressure = max(0.0, min(motion_magnitude, 1.0))

        # depth: visual complexity / structure depth
        depth = max(0.0, min(edge_density, 1.0))

        # binding: uniform scenes bind strongly; chaotic colours fragment
        binding = max(0.0, min(1.0 - color_variance, 1.0))

        # continuity: sharp focus + steady motion = high continuity
        motion_delta = abs(motion_magnitude - self._prev_motion)
        self._prev_motion = motion_magnitude
        continuity = max(0.0, min(focus * (1.0 - motion_delta * 2.0), 1.0))

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  CODEC REGISTRY: Discover what sensors are available
# ================================================================

# All known codec types
CODEC_REGISTRY = {
    'imu': IMUCodec,
    'proximity': ProximityCodec,
    'motor': MotorCodec,
    'battery': BatteryCodec,
    'temperature': TemperatureCodec,
    'vision': VisionCodec,
}

# Game codecs are registered lazily to avoid circular imports.
# Call register_game_codecs() to add them.
_game_codecs_registered = False

# Clay mathematical codecs are registered lazily.
# Call register_clay_codecs() to add them.
_clay_codecs_registered = False

def register_game_codecs():
    """Register game-environment codecs into CODEC_REGISTRY.

    Called lazily so ck_sensory_codecs doesn't depend on ck_game_sense
    at import time. SensorFusion.auto_register() will find them after
    this function runs.
    """
    global _game_codecs_registered
    if _game_codecs_registered:
        return
    try:
        from ck_sim.ck_game_sense import GAME_CODEC_REGISTRY
        CODEC_REGISTRY.update(GAME_CODEC_REGISTRY)
        _game_codecs_registered = True
    except ImportError:
        pass  # Game sense module not available


def register_clay_codecs():
    """Register Clay mathematical codecs into CODEC_REGISTRY.

    Called lazily so ck_sensory_codecs doesn't depend on ck_clay_codecs
    at import time.
    """
    global _clay_codecs_registered
    if _clay_codecs_registered:
        return
    try:
        from ck_sim.being.ck_clay_codecs import CLAY_CODEC_REGISTRY
        CODEC_REGISTRY.update(CLAY_CODEC_REGISTRY)
        _clay_codecs_registered = True
    except ImportError:
        pass  # Clay codecs module not available


class SensorFusion:
    """Fuse multiple sensor codecs into a unified operator stream.

    This is how CK sees its body: not as separate sensors, but as
    one continuous operator field. Each sensor contributes operators.
    The fusion composes them through CL, producing a single coherence
    value and a single fused operator for the whole body.

    Fractal: the same composition that happens in the heartbeat
    (phase_bc = CL[phase_b][phase_d]) happens here across sensors.
    """

    def __init__(self):
        self.codecs: Dict[str, SensorCodec] = {}
        self._body_operator = VOID
        self._body_coherence = 0.0

    def register(self, name: str, codec: SensorCodec):
        """Register a sensor codec."""
        self.codecs[name] = codec

    def auto_register(self, available_sensors: List[str]):
        """Auto-register codecs for available sensors.

        CK discovers what it has and creates codecs for each.
        This is what makes CK liquid — plug into any body
        and it adapts automatically.
        """
        for sensor_name in available_sensors:
            if sensor_name in CODEC_REGISTRY:
                codec_class = CODEC_REGISTRY[sensor_name]
                self.codecs[sensor_name] = codec_class()

    def feed(self, sensor_name: str, raw_reading: dict) -> int:
        """Feed a reading from a specific sensor.

        Returns the operator classified from that sensor.
        """
        codec = self.codecs.get(sensor_name)
        if codec:
            return codec.feed(raw_reading)
        return VOID

    def feed_all(self, readings: Dict[str, dict]) -> int:
        """Feed readings from all available sensors at once.

        Returns the body-fused operator.
        """
        ops = []
        for name, reading in readings.items():
            op = self.feed(name, reading)
            ops.append(op)

        # Fuse all sensor operators through CL
        if ops:
            result = ops[0]
            for i in range(1, len(ops)):
                result = compose(result, ops[i])
            self._body_operator = result
        else:
            self._body_operator = VOID

        # Body coherence = average of all sensor coherences
        if self.codecs:
            total_coh = sum(c.coherence() for c in self.codecs.values())
            self._body_coherence = total_coh / len(self.codecs)
        else:
            self._body_coherence = 0.0

        return self._body_operator

    @property
    def body_operator(self) -> int:
        """Current fused body operator."""
        return self._body_operator

    @property
    def body_coherence(self) -> float:
        """Current body coherence (average across sensors)."""
        return self._body_coherence

    def body_eak(self) -> Tuple[float, float, float]:
        """Compute E/A/K from sensor fusion for the heartbeat body.

        E (Error): average depth across sensors (how much trouble)
        A (Activation): average pressure (how much effort)
        K (Knowledge): average binding (how well things are working)

        This is the bridge from physical sensors to the E/A/K triad.
        """
        if not self.codecs:
            return (0.0, 0.0, 0.0)

        total_e = 0.0
        total_a = 0.0
        total_k = 0.0
        n = 0

        for codec in self.codecs.values():
            vec = codec.last_force_vec
            if len(vec) >= 5:
                total_e += vec[2]  # depth → Error
                total_a += vec[1]  # pressure → Activation
                total_k += vec[3]  # binding → Knowledge
                n += 1

        if n > 0:
            return (total_e / n, total_a / n, total_k / n)
        return (0.0, 0.0, 0.0)

    def stats(self) -> dict:
        """Fusion statistics."""
        codec_stats = {name: codec.stats() for name, codec in self.codecs.items()}
        return {
            'n_codecs': len(self.codecs),
            'sensors': list(self.codecs.keys()),
            'body_operator': OP_NAMES[self._body_operator],
            'body_coherence': round(self._body_coherence, 3),
            'body_eak': self.body_eak(),
            'codecs': codec_stats,
        }


# ================================================================
#  OPERATOR → ACTION MAPPING (for motor output)
# ================================================================

# What each operator MEANS as a motor behavior
OPERATOR_TO_BEHAVIOR = {
    VOID:     {'action': 'idle',      'intensity': 0.0, 'description': 'No movement'},
    LATTICE:  {'action': 'stand',     'intensity': 0.3, 'description': 'Hold position'},
    COUNTER:  {'action': 'scan',      'intensity': 0.4, 'description': 'Look around'},
    PROGRESS: {'action': 'forward',   'intensity': 0.6, 'description': 'Walk forward'},
    COLLAPSE: {'action': 'crouch',    'intensity': 0.8, 'description': 'Lower/retreat'},
    BALANCE:  {'action': 'stabilize', 'intensity': 0.5, 'description': 'Balance in place'},
    CHAOS:    {'action': 'explore',   'intensity': 0.7, 'description': 'Random movement'},
    HARMONY:  {'action': 'approach',  'intensity': 0.5, 'description': 'Move toward harmony'},
    BREATH:   {'action': 'sway',      'intensity': 0.3, 'description': 'Gentle rhythm'},
    RESET:    {'action': 'home',      'intensity': 0.2, 'description': 'Return to start'},
}


def operator_to_motor_command(operator: int, btq_level: float = 1.0) -> dict:
    """Convert an operator to a motor command.

    The BTQ level gates the intensity:
    - GREEN (1.0): full intensity
    - YELLOW (0.6): reduced
    - RED (0.3): minimal/safety mode

    Returns: {'action': str, 'intensity': float, 'btq_gated': float}
    """
    behavior = OPERATOR_TO_BEHAVIOR.get(operator, OPERATOR_TO_BEHAVIOR[VOID])
    gated_intensity = behavior['intensity'] * btq_level

    return {
        'action': behavior['action'],
        'intensity': behavior['intensity'],
        'btq_gated': round(gated_intensity, 3),
        'operator': operator,
        'operator_name': OP_NAMES[operator],
    }


# ================================================================
#  CLI: Test the codecs
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK SENSORY CODECS -- Universal Signal → Operator")
    print("=" * 60)

    # Create sensor fusion with all available sensors
    fusion = SensorFusion()
    fusion.auto_register(['imu', 'proximity', 'motor', 'battery', 'temperature', 'vision'])

    print(f"\n  Registered codecs: {list(fusion.codecs.keys())}")

    # Simulate some readings
    import random
    for tick in range(50):
        readings = {
            'imu': {
                'accel_x': random.gauss(0, 2),
                'accel_y': random.gauss(0, 2),
                'accel_z': 9.8 + random.gauss(0, 0.5),
                'gyro_x': random.gauss(0, 0.5),
                'gyro_y': random.gauss(0, 0.5),
                'gyro_z': random.gauss(0, 0.5),
            },
            'proximity': {
                'distance_cm': max(5, 100 + random.gauss(0, 20)),
                'max_range_cm': 400,
            },
            'motor': {
                'position_deg': 45 + random.gauss(0, 5),
                'target_deg': 45,
                'load': random.uniform(0, 0.3),
                'speed': random.uniform(0, 30),
            },
            'battery': {
                'voltage': 7.8 - tick * 0.005 + random.gauss(0, 0.05),
                'current_a': random.uniform(0.5, 2.0),
            },
            'temperature': {
                'temp_c': 25 + random.gauss(0, 2),
            },
            'vision': {
                'edge_density': random.uniform(0.1, 0.8),
                'brightness': random.uniform(0.2, 0.9),
                'contrast': random.uniform(0.1, 0.6),
                'motion_magnitude': random.uniform(0.0, 0.5),
                'color_variance': random.uniform(0.1, 0.7),
                'focus': random.uniform(0.3, 1.0),
            },
        }

        body_op = fusion.feed_all(readings)

    stats = fusion.stats()
    print(f"\n  Body operator: {stats['body_operator']}")
    print(f"  Body coherence: {stats['body_coherence']}")
    e, a, k = stats['body_eak']
    print(f"  Body E/A/K: E={e:.3f} A={a:.3f} K={k:.3f}")

    print("\n  Per-codec stats:")
    for name, cs in stats['codecs'].items():
        print(f"    {name}: op={cs['last_operator']}, coh={cs['coherence']}, fuse={cs['fuse']}")

    # Test operator → motor
    print("\n  Operator → Motor commands:")
    for op in range(NUM_OPS):
        cmd = operator_to_motor_command(op, btq_level=1.0)
        print(f"    {OP_NAMES[op]:10s} → {cmd['action']:10s} (intensity={cmd['btq_gated']:.1f})")
