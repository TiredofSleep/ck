# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_body_interface.py -- Abstract Body for Any Platform
========================================================
Operator: BREATH (8) -- every body breathes.

CK runs on anything with a processor. The body differs:
  - FPGA (CKIS):  GPIO LEDs, DAC audio, I2S mic, UART
  - R16 PC:       Screen (Kivy), speakers, mic, GPU
  - HP Tower:     Screen, speakers, mic, webcam, 2-core CPU
  - Old Phone:    Touchscreen, speaker, mic, accelerometer
  - Dog Robot:    4 legs (8 joints), IMU, ultrasonic, battery

CK doesn't care. It sees capabilities:
  - Can I see?    (camera/webcam)
  - Can I hear?   (microphone)
  - Can I speak?  (speaker/DAC)
  - Can I move?   (motors/actuators)
  - Can I feel?   (IMU/touch/sensors)
  - Can I show?   (LED/screen/display)

Each platform declares what it has. BTQ adapts constraints.
The engine runs the same 50Hz loop on all platforms.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import abc
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import IntEnum


# ================================================================
#  CAPABILITY FLAGS
# ================================================================

class Capability(IntEnum):
    """What can this body do?"""
    HEAR = 0       # Microphone input
    SPEAK = 1      # Audio output (speaker/DAC)
    SEE = 2        # Camera/webcam
    MOVE = 3       # Motors/actuators (legs, wheels, servos)
    FEEL = 4       # Inertial/touch sensors (IMU, accelerometer)
    SHOW = 5       # Visual output (LED, screen, display)
    THINK = 6      # Compute (CPU/GPU/FPGA)
    CONNECT = 7    # Network (WiFi, UART, USB)


# ================================================================
#  PLATFORM SPEC
# ================================================================

@dataclass
class PlatformSpec:
    """Hardware specification for a deployment target."""
    name: str = "unknown"
    cpu_cores: int = 1
    cpu_mhz: int = 100
    ram_mb: int = 64
    has_gpu: bool = False
    has_fpga: bool = False
    capabilities: List[Capability] = field(default_factory=list)
    # Motor constraints (only if MOVE capability)
    n_motors: int = 0
    motor_max_torque: float = 0.0
    # Audio spec
    audio_sample_rate: int = 44100
    audio_channels: int = 1
    # Display spec
    display_width: int = 0
    display_height: int = 0
    # Battery
    has_battery: bool = False
    battery_wh: float = 0.0
    # Tick budget
    tick_hz: int = 50
    tick_budget_ms: float = 20.0

    def can(self, cap: Capability) -> bool:
        """Check if this platform has a capability."""
        return cap in self.capabilities

    @property
    def capability_summary(self) -> str:
        names = [c.name for c in self.capabilities]
        return f"{self.name}: {', '.join(names)}"


# ================================================================
#  ABSTRACT BODY
# ================================================================

class CKBody(abc.ABC):
    """Abstract body interface. Every platform implements this.

    CK calls these methods every tick. Platforms that don't support
    a capability return sensible defaults (silence, no motion, etc.).

    The body is the boundary between CK's mind and the physical world.
    """

    @property
    @abc.abstractmethod
    def spec(self) -> PlatformSpec:
        """Hardware specification."""

    @abc.abstractmethod
    def sense(self) -> Dict[str, Any]:
        """Read all sensors. Returns dict of sensor name -> value.

        Common keys:
          'mic_rms':      float   (0-1, audio level)
          'mic_operator':  int    (D2-classified operator from audio)
          'imu_accel':    (x,y,z) (m/s^2)
          'imu_gyro':     (x,y,z) (rad/s)
          'camera_frame': ndarray (H,W,3 uint8) or None
          'battery_pct':  float   (0-1)
          'touch':        bool
          'distance_cm':  float   (ultrasonic)
        """

    @abc.abstractmethod
    def express(self, commands: Dict[str, Any]):
        """Send commands to actuators.

        Common keys:
          'led_color':    (r,g,b) float
          'audio_op':     int     (operator -> tone)
          'audio_breath': float   (breath modulation)
          'audio_btq':    float   (BTQ amplitude level)
          'motor_pos':    list    (joint positions, rad)
          'display_text': str     (status text for screen)
        """

    @abc.abstractmethod
    def start(self):
        """Initialize hardware."""

    @abc.abstractmethod
    def stop(self):
        """Shutdown hardware gracefully."""

    def get_btq_constraints(self) -> Dict[str, float]:
        """Get BTQ B-block constraints for this body.

        Override for platform-specific limits. Default is
        conservative (works for anything).
        """
        return {
            'max_velocity': 3.0,
            'max_accel': 15.0,
            'max_jerk': 100.0,
            'max_torque': self.spec.motor_max_torque or 1.0,
            'max_energy_per_cycle': 3.0,
            'tick_budget_ms': self.spec.tick_budget_ms,
        }


# ================================================================
#  CONCRETE BODIES
# ================================================================

class SimBody(CKBody):
    """R16 PC simulation body. Has everything via Kivy + sounddevice."""

    def __init__(self):
        self._spec = PlatformSpec(
            name="R16-PC",
            cpu_cores=16,
            cpu_mhz=5800,
            ram_mb=32768,
            has_gpu=True,
            capabilities=[
                Capability.HEAR, Capability.SPEAK,
                Capability.SHOW, Capability.THINK,
                Capability.CONNECT,
            ],
            audio_sample_rate=44100,
            display_width=1920,
            display_height=1080,
            tick_hz=50,
            tick_budget_ms=20.0,
        )
        self._sensors = {}

    @property
    def spec(self) -> PlatformSpec:
        return self._spec

    def sense(self) -> Dict[str, Any]:
        return self._sensors

    def express(self, commands: Dict[str, Any]):
        # In sim mode, commands are forwarded to Kivy/audio by the engine
        pass

    def start(self):
        print(f"[CK] {self._spec.name} body started")

    def stop(self):
        print(f"[CK] {self._spec.name} body stopped")

    def update_sensors(self, mic_rms=0.0, mic_operator=-1, **kwargs):
        """Called by engine to feed sensor data from ears/etc."""
        self._sensors['mic_rms'] = mic_rms
        self._sensors['mic_operator'] = mic_operator
        self._sensors.update(kwargs)


class DogBody(CKBody):
    """Quadruped robot body. 4 legs x 2 joints + IMU."""

    def __init__(self):
        self._spec = PlatformSpec(
            name="CK-Dog",
            cpu_cores=2,
            cpu_mhz=667,
            ram_mb=512,
            has_fpga=True,
            capabilities=[
                Capability.HEAR, Capability.SPEAK,
                Capability.MOVE, Capability.FEEL,
                Capability.SHOW, Capability.THINK,
            ],
            n_motors=8,
            motor_max_torque=2.0,
            audio_sample_rate=48000,
            has_battery=True,
            battery_wh=25.0,
            tick_hz=50,
            tick_budget_ms=20.0,
        )
        self._sensors = {}
        self._motor_positions = [0.0] * 8

    @property
    def spec(self) -> PlatformSpec:
        return self._spec

    def sense(self) -> Dict[str, Any]:
        return self._sensors

    def express(self, commands: Dict[str, Any]):
        if 'motor_pos' in commands:
            self._motor_positions = list(commands['motor_pos'])

    def start(self):
        print(f"[CK] {self._spec.name} body started (8 joints)")

    def stop(self):
        # Zero all motors
        self._motor_positions = [0.0] * 8
        print(f"[CK] {self._spec.name} body stopped (motors zeroed)")

    def get_btq_constraints(self) -> Dict[str, float]:
        return {
            'max_velocity': 6.0,
            'max_accel': 30.0,
            'max_jerk': 200.0,
            'max_torque': 2.0,
            'max_energy_per_cycle': 5.0,
            'tick_budget_ms': 20.0,
        }

    def update_sensors(self, imu_accel=(0,0,9.81), imu_gyro=(0,0,0),
                       battery_pct=1.0, **kwargs):
        self._sensors['imu_accel'] = imu_accel
        self._sensors['imu_gyro'] = imu_gyro
        self._sensors['battery_pct'] = battery_pct
        self._sensors.update(kwargs)


class PhoneBody(CKBody):
    """Old Android phone body. Mic, speaker, screen, accelerometer."""

    def __init__(self):
        self._spec = PlatformSpec(
            name="CK-Phone",
            cpu_cores=4,
            cpu_mhz=1200,
            ram_mb=2048,
            capabilities=[
                Capability.HEAR, Capability.SPEAK,
                Capability.SEE, Capability.FEEL,
                Capability.SHOW, Capability.THINK,
                Capability.CONNECT,
            ],
            audio_sample_rate=44100,
            display_width=720,
            display_height=1280,
            has_battery=True,
            battery_wh=10.0,
            tick_hz=50,
            tick_budget_ms=20.0,
        )
        self._sensors = {}

    @property
    def spec(self) -> PlatformSpec:
        return self._spec

    def sense(self) -> Dict[str, Any]:
        return self._sensors

    def express(self, commands: Dict[str, Any]):
        pass

    def start(self):
        print(f"[CK] {self._spec.name} body started")

    def stop(self):
        print(f"[CK] {self._spec.name} body stopped")

    def update_sensors(self, mic_rms=0.0, accel=(0,0,9.81),
                       battery_pct=1.0, **kwargs):
        self._sensors['mic_rms'] = mic_rms
        self._sensors['imu_accel'] = accel
        self._sensors['battery_pct'] = battery_pct
        self._sensors.update(kwargs)


class HPTowerBody(CKBody):
    """HP 2-core tower. Screen, speakers, mic, webcam."""

    def __init__(self):
        self._spec = PlatformSpec(
            name="HP-Tower",
            cpu_cores=2,
            cpu_mhz=3200,
            ram_mb=8192,
            capabilities=[
                Capability.HEAR, Capability.SPEAK,
                Capability.SEE, Capability.SHOW,
                Capability.THINK, Capability.CONNECT,
            ],
            audio_sample_rate=44100,
            display_width=1920,
            display_height=1080,
            tick_hz=50,
            tick_budget_ms=20.0,
        )
        self._sensors = {}

    @property
    def spec(self) -> PlatformSpec:
        return self._spec

    def sense(self) -> Dict[str, Any]:
        return self._sensors

    def express(self, commands: Dict[str, Any]):
        pass

    def start(self):
        print(f"[CK] {self._spec.name} body started")

    def stop(self):
        print(f"[CK] {self._spec.name} body stopped")

    def update_sensors(self, mic_rms=0.0, mic_operator=-1, **kwargs):
        self._sensors['mic_rms'] = mic_rms
        self._sensors['mic_operator'] = mic_operator
        self._sensors.update(kwargs)


class FPGABody(CKBody):
    """CKIS FPGA body. Zynq-7020: GPIO LEDs, DAC, I2S mic, UART."""

    def __init__(self):
        self._spec = PlatformSpec(
            name="CKIS-FPGA",
            cpu_cores=2,
            cpu_mhz=667,
            ram_mb=512,
            has_fpga=True,
            capabilities=[
                Capability.HEAR, Capability.SPEAK,
                Capability.SHOW, Capability.THINK,
                Capability.CONNECT,
            ],
            audio_sample_rate=48000,
            audio_channels=1,
            tick_hz=50,
            tick_budget_ms=20.0,
        )
        self._sensors = {}

    @property
    def spec(self) -> PlatformSpec:
        return self._spec

    def sense(self) -> Dict[str, Any]:
        return self._sensors

    def express(self, commands: Dict[str, Any]):
        pass

    def start(self):
        print(f"[CK] {self._spec.name} body started (FPGA + ARM)")

    def stop(self):
        print(f"[CK] {self._spec.name} body stopped")

    def update_sensors(self, mic_rms=0.0, mic_operator=-1, **kwargs):
        self._sensors['mic_rms'] = mic_rms
        self._sensors['mic_operator'] = mic_operator
        self._sensors.update(kwargs)


# ================================================================
#  BODY REGISTRY
# ================================================================

BODY_REGISTRY = {
    'sim': SimBody,
    'r16': SimBody,
    'dog': DogBody,
    'phone': PhoneBody,
    'hp': HPTowerBody,
    'fpga': FPGABody,
}


def create_body(platform: str = 'sim') -> CKBody:
    """Create a body for the given platform."""
    cls = BODY_REGISTRY.get(platform.lower())
    if cls is None:
        raise ValueError(
            f"Unknown platform '{platform}'. "
            f"Available: {', '.join(BODY_REGISTRY.keys())}")
    return cls()


def detect_platform() -> str:
    """Auto-detect current platform based on hardware.

    Returns platform key for BODY_REGISTRY.
    """
    import platform as plat
    import os

    machine = plat.machine().lower()
    system = plat.system().lower()

    # Check for Android (Kivy/Buildozer sets this)
    if 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ:
        return 'phone'

    # Check for FPGA indicators
    if os.path.exists('/dev/xdevcfg') or os.path.exists('/proc/device-tree/amba'):
        return 'fpga'

    # Check CPU core count as heuristic for HP tower vs R16
    cpu_count = os.cpu_count() or 1
    if system == 'windows':
        if cpu_count <= 4:
            return 'hp'
        return 'r16'

    # Linux ARM could be dog or phone
    if 'arm' in machine or 'aarch64' in machine:
        if os.path.exists('/dev/i2c-1'):  # IMU bus
            return 'dog'
        return 'phone'

    return 'sim'
