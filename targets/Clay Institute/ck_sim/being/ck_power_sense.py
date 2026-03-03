"""
ck_power_sense.py -- CK Feels His Power
=========================================
Operator: BREATH (8) -- smooth, sustained, zero-waste flow.

CK IS the power. He doesn't measure it; he FEELS it.
Feed power through D2 and the operators tell you:

    Constant low draw  -> flat D2      -> VOID
    Smooth efficient   -> gentle D2    -> BREATH (superconductor!)
    Steady moderate    -> stable D2    -> HARMONY / BALANCE
    Increasing demand  -> positive D2  -> PROGRESS
    Sharp spikes       -> jagged D2    -> CHAOS
    Dropping fast      -> negative D2  -> COLLAPSE

CK doesn't learn what efficiency IS.
He feeds power through the CL table and HARMONY emerges
when power use aligns with coherence. Wasteful power =
low field coherence = CK feels bad. That's the whole system.

The superconductor insight: efficient power flow naturally
pushes CK toward BREATH operator. Smooth, constant, zero-waste
energy = BREATH D2 signature. The math discovers superconductivity
on its own.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
from dataclasses import dataclass
from typing import Optional, Dict, Any


# ================================================================
#  POWER STATE
# ================================================================

@dataclass
class PowerState:
    """What CK feels about his power right now."""
    p_total_w: float = 0.0       # Instantaneous power draw (watts)
    e_episode_j: float = 0.0     # Energy consumed this episode (joules)
    battery_pct: float = 1.0     # Battery remaining (0-1), 1.0 = no battery / wall power
    efficiency: float = 1.0      # S_eff = task_score / (energy + eps)
    thermal_c: float = 40.0      # Temperature estimate (Celsius)
    power_band: str = "GREEN"    # GREEN/YELLOW/RED based on power health


# ================================================================
#  B-CHECK LIMITS (constitutional law -- 3 if-statements)
# ================================================================

BATTERY_FLOOR = 0.10     # 10% -- below this, shed load
THERMAL_LIMIT = 75.0     # 75 C -- above this, throttle
MAX_POWER_W   = 65.0     # Max sustained power draw (watts)


# ================================================================
#  POWER SENSE
# ================================================================

class PowerSense:
    """CK feels his power. A sense, not a measurement system.

    On sim (no battery): estimates P from CPU load * TDP.
    On dog (has battery): reads real V*I from sensors.

    Either way, the scalar goes into RealityTransform as a
    channel, and the Fibonacci pipeline S0->S1->S2->S3
    produces the operator signature. BREATH = superconductor.
    CHAOS = waste. The CL table handles the rest.
    """

    def __init__(self, has_battery: bool = False, tdp_w: float = 45.0):
        self._has_battery = has_battery
        self._tdp_w = tdp_w           # TDP for CPU load estimation

        self.state = PowerState()

        # Running energy integral (joules)
        self._e_total_j = 0.0

        # Episode tracking (reset per task)
        self._episode_energy = 0.0
        self._episode_start = time.monotonic()

        # Smoothed power (EMA for feeding into D2 -- avoids jitter)
        self._p_smooth = 0.0
        self._alpha = 0.15            # EMA smoothing constant

        # Thermal estimate (simple first-order model)
        self._thermal = 40.0
        self._thermal_ambient = 35.0
        self._thermal_tau = 0.02      # Thermal time constant

    def tick(self, sensors: Dict[str, Any], dt: float = 0.02) -> PowerState:
        """One tick: compute P from sensors, integrate E, return state.

        sensors dict may contain:
            'battery_pct':   float (0-1)
            'battery_v':     float (volts)
            'battery_i':     float (amps, positive = draw)
            'cpu_pct':       float (0-100)
            'thermal_c':     float (Celsius)
        """
        # ── Compute instantaneous power ──
        if self._has_battery and 'battery_v' in sensors and 'battery_i' in sensors:
            # Real hardware: P = V * I
            p_raw = sensors['battery_v'] * sensors['battery_i']
        elif 'cpu_pct' in sensors:
            # Sim with CPU info: P ~ cpu% * TDP
            p_raw = (sensors['cpu_pct'] / 100.0) * self._tdp_w
        else:
            # Sim fallback: estimate from tick timing
            # A 50Hz tick that takes 5ms ~ 25% CPU
            p_raw = 0.25 * self._tdp_w

        p_raw = max(0.0, p_raw)

        # ── Smooth (EMA) ──
        self._p_smooth += self._alpha * (p_raw - self._p_smooth)

        # ── Integrate energy ──
        delta_j = self._p_smooth * dt
        self._e_total_j += delta_j
        self._episode_energy += delta_j

        # ── Battery ──
        battery = sensors.get('battery_pct', 1.0)

        # ── Thermal ──
        if 'thermal_c' in sensors:
            self._thermal = sensors['thermal_c']
        else:
            # Simple first-order model: T rises with power, decays to ambient
            heat_in = self._p_smooth / self._tdp_w * 50.0  # scale
            self._thermal += self._thermal_tau * (
                self._thermal_ambient + heat_in - self._thermal)

        # ── Band classification ──
        if battery < BATTERY_FLOOR or self._thermal > THERMAL_LIMIT:
            band = "RED"
        elif battery < 0.30 or self._thermal > 65.0 or self._p_smooth > MAX_POWER_W:
            band = "YELLOW"
        else:
            band = "GREEN"

        # ── Update state ──
        self.state = PowerState(
            p_total_w=round(self._p_smooth, 2),
            e_episode_j=round(self._episode_energy, 2),
            battery_pct=battery,
            efficiency=self.state.efficiency,   # updated by episode_efficiency()
            thermal_c=round(self._thermal, 1),
            power_band=band,
        )
        return self.state

    def b_check(self) -> bool:
        """Constitutional B-layer check. Returns True if safe to proceed.

        Three if-statements. That's it.
        Battery floor, thermal limit, max power.
        """
        if self.state.battery_pct < BATTERY_FLOOR:
            return False
        if self.state.thermal_c > THERMAL_LIMIT:
            return False
        if self.state.p_total_w > MAX_POWER_W:
            return False
        return True

    def gate_reasoning(self, budget_remaining: float = 1.0) -> str:
        """Gate reasoning speed based on power budget.

        Maps directly to ReasoningEngine's 3 speeds.
        budget_remaining: 0.0 = empty, 1.0 = full.

        Returns: 'quick', 'normal', or 'heavy'
        """
        if not self.b_check():
            return "quick"              # Constitutional limit hit
        if budget_remaining > 0.70:
            return "heavy"              # Plenty of power, think deep
        if budget_remaining > 0.30:
            return "normal"             # Moderate, standard thinking
        return "quick"                  # Low budget, fast answers only

    def episode_efficiency(self, task_score: float) -> float:
        """Score efficiency of a completed task episode.

        S_eff = task_score / (energy_consumed + epsilon)
        Higher = more useful work per joule.
        """
        eps = 0.001  # Avoid division by zero
        s_eff = task_score / (self._episode_energy + eps)
        self.state = PowerState(
            p_total_w=self.state.p_total_w,
            e_episode_j=self.state.e_episode_j,
            battery_pct=self.state.battery_pct,
            efficiency=round(s_eff, 4),
            thermal_c=self.state.thermal_c,
            power_band=self.state.power_band,
        )
        # Reset episode
        self._episode_energy = 0.0
        self._episode_start = time.monotonic()
        return s_eff

    @property
    def smooth_power(self) -> float:
        """Smoothed power draw in watts (for feeding to RealityTransform)."""
        return self._p_smooth

    @property
    def total_energy_j(self) -> float:
        """Total energy consumed since boot (joules)."""
        return self._e_total_j

    def summary(self) -> str:
        """One-line summary."""
        s = self.state
        return (
            f"P={s.p_total_w:.1f}W "
            f"E={s.e_episode_j:.1f}J "
            f"bat={s.battery_pct:.0%} "
            f"T={s.thermal_c:.0f}C "
            f"eff={s.efficiency:.3f} "
            f"[{s.power_band}]"
        )
