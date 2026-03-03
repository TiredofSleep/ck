"""
ck_zynq_dog.py -- Zynq Dog Hardware Wiring (Simulation Stubs)
================================================================
Operator: PROGRESS (3) -- building the bridge to hardware.

Architecture doc + runnable stubs showing the Zynq-7020 dual-core
ARM + FPGA partition for the CK quadruped dog:

  PS Core 0 (ARM): Brain + B-block + Q-block (Einstein reasoning)
    - Global constraints, path planning, energy management
    - Mode transitions, sovereignty pipeline

  PS Core 1 (ARM): Body + breath + action execution
    - Breath cycle, audio synthesis, execute chosen gait
    - Walk-to-dock control law

  PL (FPGA): T-block + IMU fusion + heartbeat + D2 pipeline
    - IMU fusion @ 500Hz (3-axis gyro + accel)
    - Joint phase timing (8 PWM channels)
    - D2 curvature pipeline (Q1.14 fixed-point)
    - Helical pattern generation
    - Candidate trajectory generation

Communication: Shared BRAM (simulated as SharedMemory dataclass)

+-------------------------------------------------------+
|                    ZYNQ-7020                           |
|  +------------------+    +------------------+          |
|  |   PS Core 0      |    |   PS Core 1      |         |
|  |  Brain + B + Q   |    |  Body + Execute  |         |
|  +--------+----------+    +--------+----------+        |
|           |     Shared BRAM        |                   |
|  +--------+------------------------+----------+        |
|  |              PL (FPGA Fabric)               |       |
|  |  T-Block + Heartbeat + D2 + IMU             |      |
|  +---------------------------------------------+      |
+-------------------------------------------------------+

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    HeartbeatFPGA, NUM_OPS, HARMONY, VOID, OP_NAMES
)
from ck_sim.ck_sim_brain import (
    BrainState, brain_init, brain_tick
)
from ck_sim.ck_sim_body import (
    BodyState, body_init, body_tick,
    BAND_GREEN, BAND_NAMES
)
from ck_sim.ck_sim_d2 import D2Pipeline
from ck_sim.ck_btq import UniversalBTQ, Candidate
from ck_sim.ck_sim_btq import (
    LocomotionDomain, MotorConstraints, GaitCandidate
)
from ck_sim.ck_fractal_health import HealthMonitor


# ================================================================
#  SHARED MEMORY (Simulates Zynq BRAM)
# ================================================================

@dataclass
class SharedMemory:
    """Simulates the shared BRAM between PS cores and PL fabric.

    In real hardware:
      - PL writes: coherence_window, candidate_buffer, imu data
      - PS Core 0 writes: score_registers, chosen_idx, health_flags
      - PS Core 1 reads: chosen_idx, health_flags
      - Both PS cores read: coherence_window, imu data
    """
    # From PL -> PS
    coherence_window: List[int] = field(
        default_factory=lambda: [0] * 32)
    candidate_count: int = 0
    imu_accel: np.ndarray = field(
        default_factory=lambda: np.zeros(3))   # m/s^2
    imu_gyro: np.ndarray = field(
        default_factory=lambda: np.zeros(3))   # rad/s

    # From PS Core 0 -> PS Core 1
    chosen_idx: int = -1
    chosen_gait: Optional[GaitCandidate] = None
    health_flags: int = 0   # Bit-packed: bit 0 = motion, bit 1 = overall

    # Phase operators (PL -> PS)
    phase_b: int = HARMONY
    phase_d: int = HARMONY
    phase_bc: int = HARMONY
    coherence: float = 0.0
    bump_detected: bool = False

    # System tick counter
    tick_count: int = 0


# ================================================================
#  PS CORE 0: Brain + B-block + Q-block (Einstein)
# ================================================================

class PSCore0:
    """PS Core 0: Einstein reasoning.

    Runs at 50Hz (20ms budget per tick):
      1. Read shared memory (FPGA state)
      2. Brain tick (sovereignty pipeline)
      3. BTQ decide: B-filter -> Q-score -> Q-select
      4. Write chosen gait + health flags to shared memory
    """

    def __init__(self, shared: SharedMemory):
        self.shared = shared
        self.brain = brain_init()
        self.heartbeat = HeartbeatFPGA()
        self.btq = UniversalBTQ(w_out=0.5, w_in=0.5)
        self.btq.register_domain(LocomotionDomain())
        self.health = HealthMonitor(window_size=100)
        self._lfsr = 0xDEADBEEF

    def _lfsr_next(self) -> int:
        self._lfsr ^= (self._lfsr << 13) & 0xFFFFFFFF
        self._lfsr ^= (self._lfsr >> 17)
        self._lfsr ^= (self._lfsr << 5) & 0xFFFFFFFF
        self._lfsr &= 0xFFFFFFFF
        return self._lfsr

    def tick(self):
        """One Core 0 tick at 50Hz."""
        # Generate operators
        val = self._lfsr_next()
        phase_b = HARMONY if (val % 10 < 7) else (val % NUM_OPS)
        val = self._lfsr_next()
        phase_d = HARMONY if (val % 10 < 7) else (val % NUM_OPS)

        # Heartbeat composition
        self.heartbeat.tick(phase_b, phase_d)

        # Brain sovereignty tick
        brain_tick(self.brain, self.heartbeat)

        # BTQ decision (every 10th tick = 5Hz decision rate)
        if self.shared.tick_count % 10 == 0:
            env = {
                'coherence': self.brain.coherence,
                'mode': self.brain.mode,
                'band': self.heartbeat.coherence,
            }
            goal = {'task': 'walk'}

            chosen, approved = self.btq.decide(
                "locomotion", env, goal, n_candidates=32)

            if chosen and chosen.score:
                self.shared.chosen_gait = chosen.payload
                self.shared.chosen_idx = 0
                self.health.feed("locomotion", chosen.score)

                # Health flags
                band = self.health.classify_system_band()
                self.shared.health_flags = (
                    (0 if band == "GREEN" else (1 if band == "YELLOW" else 2))
                )

        # Write state to shared memory
        self.shared.phase_b = self.heartbeat.phase_b
        self.shared.phase_d = self.heartbeat.phase_d
        self.shared.phase_bc = self.heartbeat.phase_bc
        self.shared.coherence = self.heartbeat.coherence
        self.shared.bump_detected = self.heartbeat.bump_detected


# ================================================================
#  PS CORE 1: Body + Breath + Action Execution
# ================================================================

class PSCore1:
    """PS Core 1: Body management and action execution.

    Runs at 50Hz:
      1. Read chosen gait from shared memory
      2. Body tick (E/A/K, breath, pulse)
      3. Execute chosen gait step (update motor positions)
      4. Walk-to-dock control law
    """

    def __init__(self, shared: SharedMemory):
        self.shared = shared
        self.body = body_init()
        self.dock = DockController()
        self.motor_positions = np.zeros(8)  # 4 legs x 2 joints
        self._gait_step = 0

    def tick(self):
        """One Core 1 tick at 50Hz."""
        # Body update
        self.body.brain_coherence = self.shared.coherence
        self.body.brain_bump = self.shared.bump_detected
        self.body.current_op = self.shared.phase_bc
        body_tick(self.body)

        # Execute chosen gait
        gait = self.shared.chosen_gait
        if gait is not None and gait.trajectory is not None:
            n_steps = gait.trajectory.shape[0]
            step = self._gait_step % n_steps
            self.motor_positions = gait.trajectory[step].copy()
            self._gait_step += 1

        # Dock controller update
        self.dock.update(
            imu_data=self.shared.imu_accel,
            health_flags=self.shared.health_flags,
        )


# ================================================================
#  PL FABRIC: T-block + IMU + Heartbeat
# ================================================================

class PLFabric:
    """PL (FPGA fabric): fast-tick subsystems.

    In real hardware, this runs as concurrent logic:
      - IMU fusion at 500Hz
      - D2 pipeline (combinational + 3 pipeline stages)
      - Heartbeat composition (1 clock cycle per tick)
      - T-block candidate generation (fills shared buffer)

    In simulation, we model the 500Hz rate and the 50Hz output.
    """

    def __init__(self, shared: SharedMemory):
        self.shared = shared
        self.d2_pipeline = D2Pipeline()
        self._imu_tick = 0

    def tick_fast(self):
        """Fast tick at ~500Hz: IMU fusion simulation.

        In real FPGA: SPI read from MPU-6050, complementary filter.
        Here: just simulate gentle motion.
        """
        self._imu_tick += 1
        t = self._imu_tick * 0.002  # 500Hz -> 2ms per tick

        # Simulate walking motion on IMU
        self.shared.imu_accel = np.array([
            0.1 * math.sin(3.0 * t),       # forward/back
            0.05 * math.sin(6.0 * t),      # lateral sway
            9.81 + 0.2 * math.sin(6.0 * t) # vertical bounce
        ])
        self.shared.imu_gyro = np.array([
            0.02 * math.sin(3.0 * t),  # roll
            0.01 * math.sin(3.0 * t),  # pitch
            0.005 * math.sin(1.5 * t), # yaw
        ])

    def tick_slow(self):
        """Slow tick at 50Hz: outputs for PS cores."""
        self.shared.tick_count += 1


# ================================================================
#  DOCK CONTROLLER (Walk-to-Dock State Machine)
# ================================================================

class DockController:
    """Walk-to-dock control law using BTQ decisions.

    State machine:
      IDLE      -> WALK      (when dock target set)
      WALK      -> APPROACH  (distance < 0.5m)
      APPROACH  -> ALIGN     (distance < 0.1m)
      ALIGN     -> DOCK      (distance < 0.02m)
      DOCK      -> IDLE      (after settling)

    Each state adjusts motor constraints for the BTQ B-block:
      WALK:     Normal constraints, trot gait
      APPROACH: Tighter velocity, walk gait
      ALIGN:    Half velocity, precision mode
      DOCK:     Stop motors
    """

    def __init__(self):
        self.state = "IDLE"
        self.target_pos = np.zeros(3)
        self.current_pos = np.zeros(3)
        self.distance = float('inf')
        self.step_count = 0
        self.step_size = 0.3  # meters per decision cycle

    def set_target(self, x: float, y: float, z: float = 0.0):
        """Set dock target position."""
        self.target_pos = np.array([x, y, z])
        self.distance = float(np.linalg.norm(self.target_pos - self.current_pos))
        if self.state == "IDLE" and self.distance > 0.02:
            self.state = "WALK"

    def update(self, imu_data: np.ndarray = None,
               health_flags: int = 0):
        """One control tick. Advance state machine based on distance."""
        if self.state == "IDLE":
            return

        # Simulate forward motion
        if self.state in ("WALK", "APPROACH", "ALIGN"):
            direction = self.target_pos - self.current_pos
            dist = float(np.linalg.norm(direction))
            if dist > 0.001:
                step = min(self.step_size, dist)
                if self.state == "APPROACH":
                    step = min(step, 0.1)
                elif self.state == "ALIGN":
                    step = min(step, 0.02)
                self.current_pos += (direction / dist) * step

            self.distance = float(np.linalg.norm(
                self.target_pos - self.current_pos))
            self.step_count += 1

        # State transitions
        if self.state == "WALK" and self.distance < 0.5:
            self.state = "APPROACH"

        elif self.state == "APPROACH" and self.distance < 0.1:
            self.state = "ALIGN"

        elif self.state == "ALIGN" and self.distance < 0.02:
            self.state = "DOCK"

        elif self.state == "DOCK":
            # Settle for 5 ticks then go IDLE
            self.step_count += 1
            if self.step_count > 5:
                self.state = "IDLE"
                self.step_count = 0

        # Emergency: if health is RED, stop
        if health_flags >= 2 and self.state != "IDLE":
            self.state = "IDLE"

    def get_constraints(self) -> MotorConstraints:
        """Get motor constraints for current state."""
        c = MotorConstraints()

        if self.state == "APPROACH":
            c.max_velocity = 3.0   # Half normal
            c.max_accel = 15.0
        elif self.state == "ALIGN":
            c.max_velocity = 1.5   # Quarter normal
            c.max_accel = 8.0
            c.max_jerk = 100.0
        elif self.state == "DOCK":
            c.max_velocity = 0.0   # Stop
            c.max_accel = 0.0

        return c

    @property
    def status(self) -> str:
        return (f"state={self.state} dist={self.distance:.3f}m "
                f"steps={self.step_count}")


# ================================================================
#  FULL ZYNQ DOG SIMULATION
# ================================================================

class ZynqDogSim:
    """Full Zynq dog simulation.

    Ties PS Core 0 + PS Core 1 + PL Fabric together via SharedMemory.
    Models the real hardware timing:
      - PL: 10 fast ticks (500Hz) per system tick
      - PS Core 0: 1 tick (50Hz)
      - PS Core 1: 1 tick (50Hz)

    Usage:
        sim = ZynqDogSim()
        sim.dock.set_target(3.0, 0.0)
        for _ in range(100):
            sim.run_tick()
            print(sim.status())
    """

    def __init__(self):
        self.shared = SharedMemory()
        self.core0 = PSCore0(self.shared)
        self.core1 = PSCore1(self.shared)
        self.pl = PLFabric(self.shared)
        self.dock = self.core1.dock

    def run_tick(self):
        """One system tick: PL fast ticks, then PS0, then PS1."""
        # PL: 10 fast ticks (simulating 500Hz within one 50Hz frame)
        for _ in range(10):
            self.pl.tick_fast()

        # PL: slow tick (update shared counters)
        self.pl.tick_slow()

        # PS Core 0: brain + BTQ
        self.core0.tick()

        # PS Core 1: body + execute + dock
        self.core1.tick()

    def status(self) -> str:
        """One-line status."""
        return (f"tick={self.shared.tick_count:5d} "
                f"BC={OP_NAMES[self.shared.phase_bc]:8s} "
                f"C={self.shared.coherence:.3f} "
                f"mode={self.core0.brain.mode} "
                f"dock={self.dock.state:8s} "
                f"dist={self.dock.distance:.3f}m "
                f"health={self.shared.health_flags}")
