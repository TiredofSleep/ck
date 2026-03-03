"""
ck_deploy.py -- CK Deployment Configurations
=============================================
Operator: LATTICE (4) -- the structure beneath every platform.

CK runs on anything with a processor. This module defines the
deployment matrix: 5 verified platforms, each with its own body,
BTQ constraints, and tick budget.

  Platform     CPU           RAM     Body         BTQ Domains
  --------     ---           ---     ----         -----------
  R16 PC       16c/5.8GHz    32GB    SimBody      memory, bio
  HP Tower     2c/3.2GHz     8GB     HPTower      memory, bio
  Old Phone    4c/1.2GHz     2GB     PhoneBody    memory, bio
  CK-Dog       2c/667MHz     512MB   DogBody      memory, bio, locomotion
  CKIS FPGA    2c/667MHz     512MB   FPGABody     memory, bio

Usage:
    from ck_sim.ck_deploy import get_deployment, list_deployments
    deploy = get_deployment('r16')
    engine = deploy.create_engine()
    engine.start()

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ck_sim.ck_body_interface import (
    PlatformSpec, Capability, BODY_REGISTRY, create_body, detect_platform
)


# ================================================================
#  DEPLOYMENT CONFIG
# ================================================================

@dataclass
class DeploymentConfig:
    """Complete deployment specification for one platform."""
    name: str = ""
    platform_key: str = "sim"
    description: str = ""

    # BTQ tuning
    btq_w_out: float = 0.5
    btq_w_in: float = 0.5
    btq_decision_hz: int = 5           # Decisions per second
    btq_candidates: int = 16           # Candidates per decision

    # Health monitor
    health_window: int = 100

    # Engine tick rate
    tick_hz: int = 50

    # Memory budget (max crystals, TL save interval)
    max_crystals: int = 1000
    tl_save_interval: int = 15000      # ticks

    # Audio settings
    audio_enabled: bool = True
    audio_sample_rate: int = 44100

    # Logging
    log_btq: bool = False
    log_file: str = ""

    def create_engine(self):
        """Create a CKSimEngine configured for this deployment."""
        from ck_sim.ck_sim_engine import CKSimEngine
        engine = CKSimEngine(platform=self.platform_key)

        # Apply BTQ weights
        engine.btq.q_block.w_out = self.btq_w_out
        engine.btq.q_block.w_in = self.btq_w_in

        # Apply health window
        engine.health.window_size = self.health_window

        return engine


# ================================================================
#  PLATFORM DEPLOYMENTS
# ================================================================

DEPLOYMENTS: Dict[str, DeploymentConfig] = {
    'r16': DeploymentConfig(
        name="R16 Gaming PC",
        platform_key="r16",
        description=(
            "Primary development platform. 16-core Ryzen, 32GB RAM, RTX GPU. "
            "Full Kivy visualization, speaker, mic. No motors."
        ),
        btq_w_out=0.5,
        btq_w_in=0.5,
        btq_candidates=16,
        health_window=100,
        tick_hz=50,
        max_crystals=10000,
        audio_sample_rate=44100,
    ),

    'hp': DeploymentConfig(
        name="HP 2-Core Tower",
        platform_key="hp",
        description=(
            "Older HP tower. 2-core Intel, 8GB RAM. "
            "Screen, speakers, mic, webcam. Tighter tick budget."
        ),
        btq_w_out=0.5,
        btq_w_in=0.5,
        btq_candidates=8,          # Fewer candidates for 2-core
        health_window=50,
        tick_hz=50,
        max_crystals=5000,
        audio_sample_rate=44100,
    ),

    'phone': DeploymentConfig(
        name="Old Android Phone",
        platform_key="phone",
        description=(
            "Budget Android phone via Kivy/Buildozer. 4-core ARM, 2GB RAM. "
            "Touch, accelerometer, mic, camera. Battery-conscious."
        ),
        btq_w_out=0.6,             # Favor safety (E_out) on constrained device
        btq_w_in=0.4,
        btq_candidates=8,
        btq_decision_hz=2,         # Slower decisions to save battery
        health_window=50,
        tick_hz=50,
        max_crystals=2000,
        audio_sample_rate=44100,
    ),

    'dog': DeploymentConfig(
        name="CK Quadruped Dog",
        platform_key="dog",
        description=(
            "Zynq-7020 quadruped. 2-core ARM + FPGA, 512MB. "
            "8 joints, IMU, speaker, mic. Locomotion domain active."
        ),
        btq_w_out=0.5,
        btq_w_in=0.5,
        btq_candidates=32,         # More candidates for motor safety
        health_window=100,
        tick_hz=50,
        max_crystals=1000,
        audio_sample_rate=48000,
        log_btq=True,
        log_file="ck_dog_btq.jsonl",
    ),

    'fpga': DeploymentConfig(
        name="CKIS FPGA Board",
        platform_key="fpga",
        description=(
            "Zynq-7020 standalone. 2-core ARM + FPGA fabric, 512MB. "
            "GPIO LEDs, DAC audio, I2S mic, UART. Pure CK machine."
        ),
        btq_w_out=0.5,
        btq_w_in=0.5,
        btq_candidates=16,
        health_window=100,
        tick_hz=50,
        max_crystals=1000,
        audio_sample_rate=48000,
    ),
}


# ================================================================
#  API
# ================================================================

def get_deployment(platform: str = None) -> DeploymentConfig:
    """Get deployment config. Auto-detects platform if not specified."""
    if platform is None:
        platform = detect_platform()

    key = platform.lower()
    if key not in DEPLOYMENTS:
        raise ValueError(
            f"Unknown deployment '{platform}'. "
            f"Available: {', '.join(DEPLOYMENTS.keys())}"
        )
    return DEPLOYMENTS[key]


def list_deployments() -> List[str]:
    """List all available deployment platform keys."""
    return list(DEPLOYMENTS.keys())


def deployment_matrix() -> str:
    """Pretty-print the deployment matrix."""
    lines = []
    lines.append(f"{'Platform':<12} {'Key':<6} {'Candidates':<12} "
                 f"{'Health Win':<12} {'Max Crystals':<14} {'Audio Hz'}")
    lines.append("-" * 80)

    for key, cfg in DEPLOYMENTS.items():
        lines.append(
            f"{cfg.name:<12} {key:<6} {cfg.btq_candidates:<12} "
            f"{cfg.health_window:<12} {cfg.max_crystals:<14} "
            f"{cfg.audio_sample_rate}"
        )

    # Platform capabilities
    lines.append("")
    lines.append("Capabilities:")
    for key in DEPLOYMENTS:
        body = create_body(key)
        lines.append(f"  {key}: {body.spec.capability_summary}")

    return "\n".join(lines)
