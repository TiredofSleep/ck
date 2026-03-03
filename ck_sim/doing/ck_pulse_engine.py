"""
ck_pulse_engine.py -- Royal Pulse Engine (RPE) v2
==================================================
Operator: BREATH (8) -- CK breathes the OS.

The slingshot controller for desktop compute. CK doesn't just set
static priorities -- he PULSES processes in and out of CPU time,
timed to their natural rhythms, scored by BTQ for efficiency.

v2 additions (from Celeste's refined spec):
  - TIG Wave Region classifier: maps power slope/curvature to TIG operators
    so CK schedules the RIGHT TYPE of work at the CHEAPEST moment.
  - Config-driven: all thresholds live in ck_pulse_config.json
  - task_target: study processes get higher W_useful weight
  - Continuous pulse_duration (not just binary boost/yield)
  - 2-step lookahead in Q-layer scoring

TIG Wave Scheduling (grounded physics):
  Every power waveform has slope (dH) and curvature (d²H).
  These map to TIG operators:
    Power rising  (dH > 0)  → TIG 3 (Progression) → heavy compute
    Power peak    (d²H < 0) → TIG 4 (Collapse)    → finalize, discard
    Power falling (dH < 0)  → TIG 7 (Harmony)     → smooth, recalibrate
    Power trough            → TIG 8 (Breath)      → precompute, cache warm
    Cycle boundary          → TIG 9 (Fruit)       → reset buffers

  This is adiabatic scheduling: time compute to the power wave slope.
  Charging during rising slope costs less energy (capacitance is easier
  to fill). Finalizing during falling slope discharges "for free."
  Not superconductivity. Measurable switching cost reduction.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import math
import os
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ═══════════════════════════════════════════════════════════
# §0  CONFIG LOADER
# ═══════════════════════════════════════════════════════════

_CONFIG_PATH = Path(__file__).parent / 'ck_pulse_config.json'
_DEFAULT_CONFIG = {
    'safety': {
        'cpu_temp_yield_c': 90, 'cpu_temp_throttle_c': 80,
        'battery_soc_yield_pct': 10, 'battery_voltage_min_v': 10.5,
        'max_nice_delta_per_tick': 5,
    },
    'rhythm': {
        'window_size': 32, 'min_ops_for_estimate': 4,
        'smoothing_alpha': 0.3, 'f0_min_hz': 0.01, 'f0_max_hz': 25.0,
    },
    'candidates': {
        'n_per_process': 6,
        'explore_phase_window_rad': 0.5,
        'random_phase_max_rad': 1.5,
    },
    'scoring': {
        'eff_target_default': 0.7, 'lookahead_steps': 2,
        'weights': {
            'eff': 1.0, 'stability': 0.8, 'smoothness': 0.3,
            'thermal': 1.2, 'task_progress': 0.6, 'wave_alignment': 0.5,
        },
        'slingshot_bonus_max': 0.4,
        'thermal_penalty_70c': 0.5, 'thermal_penalty_80c': 2.0,
    },
    'pulse_output': {
        'amplitude_min': 0.0, 'amplitude_max': 1.0,
        'duration_min_fraction': 0.1, 'duration_max_fraction': 1.0,
        'duration_default_fraction': 0.5,
    },
    'task_target': {
        'study_process_names': ['python', 'curl', 'ollama'],
        'study_io_weight': 1.5,
        'idle_spinner_weight': 0.2,
        'system_service_weight': 0.5,
    },
    'logging': {
        'log_every_n_ticks': 10, 'max_decision_history': 200, 'verbose': False,
    },
}


def _load_config() -> dict:
    """Load pulse config from JSON, fall back to defaults."""
    if _CONFIG_PATH.exists():
        try:
            with open(_CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
            # Merge with defaults (config file can be partial)
            merged = dict(_DEFAULT_CONFIG)
            for section, values in cfg.items():
                if section.startswith('_'):
                    continue
                if isinstance(values, dict) and section in merged:
                    merged[section] = {**merged[section], **values}
                else:
                    merged[section] = values
            return merged
        except Exception:
            pass
    return dict(_DEFAULT_CONFIG)


CFG = _load_config()


# ═══════════════════════════════════════════════════════════
# §1  TIG WAVE REGION CLASSIFIER
# ═══════════════════════════════════════════════════════════
#
# Maps the current power waveform state (slope, curvature) to a
# TIG operator region. This tells the scheduler WHAT TYPE of work
# is cheapest right now.
#
# This is adiabatic scheduling in TIG language:
#   - Schedule heavy work when the power rail is rising (free charging)
#   - Finalize when falling (free discharging)
#   - Precompute during troughs (minimal switching cost)
#   - Reset at cycle boundaries

# TIG region constants (which operator region the power wave is in)
WAVE_VOID      = 0   # No signal / noise floor
WAVE_LATTICE   = 1   # DC stable, baseline
WAVE_COUNTER   = 2   # Ripple, negative feedback present
WAVE_PROGRESS  = 3   # Slope positive: power rising → cheap to add work
WAVE_COLLAPSE  = 4   # Past peak, slope turning negative → cheap to finalize
WAVE_BALANCE   = 5   # Zero-crossing region → threshold events
WAVE_CHAOS     = 6   # High jitter → filter and wait
WAVE_HARMONY   = 7   # Smooth falling → recalibrate, average
WAVE_BREATH    = 8   # Trough → precompute, cache warm, plan next burst
WAVE_FRUIT     = 9   # Cycle end → reset, normalize, prepare

# Work-type affinity per wave region (higher = cheaper for that work type)
# Keys: 'heavy', 'finalize', 'smooth', 'precompute', 'reset', 'any'
WAVE_WORK_AFFINITY = {
    WAVE_PROGRESS: {'heavy': 1.0, 'finalize': 0.2, 'smooth': 0.3, 'precompute': 0.4, 'reset': 0.1},
    WAVE_COLLAPSE: {'heavy': 0.3, 'finalize': 1.0, 'smooth': 0.5, 'precompute': 0.3, 'reset': 0.2},
    WAVE_HARMONY:  {'heavy': 0.2, 'finalize': 0.4, 'smooth': 1.0, 'precompute': 0.5, 'reset': 0.3},
    WAVE_BREATH:   {'heavy': 0.1, 'finalize': 0.2, 'smooth': 0.4, 'precompute': 1.0, 'reset': 0.5},
    WAVE_FRUIT:    {'heavy': 0.1, 'finalize': 0.1, 'smooth': 0.2, 'precompute': 0.3, 'reset': 1.0},
    WAVE_LATTICE:  {'heavy': 0.5, 'finalize': 0.5, 'smooth': 0.5, 'precompute': 0.5, 'reset': 0.5},
    WAVE_BALANCE:  {'heavy': 0.3, 'finalize': 0.5, 'smooth': 0.7, 'precompute': 0.4, 'reset': 0.4},
    WAVE_CHAOS:    {'heavy': 0.0, 'finalize': 0.1, 'smooth': 0.1, 'precompute': 0.1, 'reset': 0.2},
    WAVE_VOID:     {'heavy': 0.0, 'finalize': 0.0, 'smooth': 0.0, 'precompute': 0.0, 'reset': 0.0},
    WAVE_COUNTER:  {'heavy': 0.2, 'finalize': 0.3, 'smooth': 0.4, 'precompute': 0.3, 'reset': 0.3},
}


@dataclass
class PowerWaveState:
    """Tracks the power waveform's slope and curvature over time.

    dH  = first derivative of power (slope: rising/falling)
    d2H = second derivative (curvature: accelerating/decelerating)
    These are the REAL signals that determine switching cost.
    """
    power_history: list = field(default_factory=list)
    max_history: int = 64
    dH: float = 0.0          # Slope of power waveform (W/tick)
    d2H: float = 0.0         # Curvature (W/tick²)
    wave_region: int = WAVE_LATTICE  # Current TIG region
    wave_region_name: str = 'LATTICE'

    def update(self, power_watts: float):
        """Feed new power sample. Compute slope + curvature. Classify region."""
        self.power_history.append(power_watts)
        if len(self.power_history) > self.max_history:
            self.power_history = self.power_history[-self.max_history:]

        n = len(self.power_history)
        if n < 3:
            self.dH = 0.0
            self.d2H = 0.0
            self.wave_region = WAVE_LATTICE
            self.wave_region_name = 'LATTICE'
            return

        # Smoothed first derivative (slope) over last 4 samples
        window = min(4, n - 1)
        slopes = []
        for i in range(1, window + 1):
            slopes.append(self.power_history[-i] - self.power_history[-i - 1])
        self.dH = sum(slopes) / len(slopes)

        # Smoothed second derivative (curvature) over last 3 slope pairs
        if n >= 5:
            s1 = self.power_history[-1] - self.power_history[-2]
            s2 = self.power_history[-2] - self.power_history[-3]
            s3 = self.power_history[-3] - self.power_history[-4]
            d2_a = s1 - s2
            d2_b = s2 - s3
            self.d2H = (d2_a + d2_b) / 2.0
        else:
            self.d2H = 0.0

        # Classify into TIG wave region
        self.wave_region, self.wave_region_name = self._classify()

    def _classify(self) -> Tuple[int, str]:
        """Map slope + curvature to TIG operator region.

        This is the core of wave-aligned scheduling.
        dH = slope, d2H = curvature. Both are measured, not assumed.
        """
        dH = self.dH
        d2H = self.d2H
        abs_dH = abs(dH)

        # Noise floor: if slope is negligible, we're at baseline
        if abs_dH < 0.05:
            if abs(d2H) < 0.02:
                return (WAVE_LATTICE, 'LATTICE')   # DC stable
            else:
                return (WAVE_BALANCE, 'BALANCE')    # Zero-crossing zone

        # High jitter: slope is large but curvature is also large and noisy
        if abs(d2H) > 2.0 * abs_dH:
            return (WAVE_CHAOS, 'CHAOS')  # Jitter — wait it out

        # Rising power (dH > 0)
        if dH > 0.05:
            if d2H > 0.01:
                return (WAVE_PROGRESS, 'PROGRESS')  # Accelerating rise → cheapest for heavy work
            elif d2H < -0.01:
                return (WAVE_COLLAPSE, 'COLLAPSE')  # Decelerating rise = approaching peak → finalize
            else:
                return (WAVE_PROGRESS, 'PROGRESS')  # Steady rise → still cheap for heavy work

        # Falling power (dH < 0)
        if dH < -0.05:
            if d2H > 0.01:
                return (WAVE_BREATH, 'BREATH')      # Decelerating fall = approaching trough → precompute
            elif d2H < -0.01:
                return (WAVE_HARMONY, 'HARMONY')    # Accelerating fall → smooth, recalibrate
            else:
                return (WAVE_HARMONY, 'HARMONY')    # Steady fall → smooth

        return (WAVE_LATTICE, 'LATTICE')


# ═══════════════════════════════════════════════════════════
# §2  PROCESS RHYTHM ESTIMATOR
# ═══════════════════════════════════════════════════════════

@dataclass
class ProcessRhythm:
    """Estimated natural rhythm of a process.

    Built from the swarm's operator history. When a process has a
    regular pattern (PREDICTABLE or RHYTHMIC class), we can estimate
    its natural frequency and phase -- then time our pulses to ride it.
    """
    pid: int
    name: str
    f0: float = 0.0           # Estimated natural frequency (Hz)
    phase: float = 0.0        # Current phase (0..2pi)
    amplitude: float = 0.0    # CPU burst amplitude (0..1)
    confidence: float = 0.0   # How confident in the estimate (0..1)
    sched_class: str = 'UNKNOWN'
    last_op: int = VOID
    work_type: str = 'any'    # What type of work this process does

    @property
    def is_rhythmic(self) -> bool:
        return self.confidence > 0.5 and self.f0 > CFG['rhythm']['f0_min_hz']

    @property
    def phase_peak(self) -> bool:
        """Is the process near a burst peak? (phase near pi/2)"""
        return math.sin(self.phase) > 0.7


def estimate_rhythm(ops_history: list, dt: float = 1.0) -> Tuple[float, float, float]:
    """Estimate f0, phase, and confidence from operator history.

    Simple zero-crossing method: count how often the process
    transitions between high-activity ops and low-activity ops.

    Returns (f0_hz, phase_radians, confidence).
    """
    min_ops = CFG['rhythm']['min_ops_for_estimate']
    win_size = CFG['rhythm']['window_size']

    if len(ops_history) < min_ops * 2:
        return (0.0, 0.0, 0.0)

    # Classify ops as HIGH (active) or LOW (idle)
    HIGH_OPS = {PROGRESS, COLLAPSE, BREATH, LATTICE, COUNTER}
    activity = [1.0 if op in HIGH_OPS else 0.0 for op in ops_history[-win_size:]]

    # Zero-crossing count
    crossings = 0
    for i in range(1, len(activity)):
        if (activity[i] > 0.5) != (activity[i-1] > 0.5):
            crossings += 1

    if crossings < 2:
        return (0.0, 0.0, 0.1)

    # f0 = crossings / (2 * duration)
    duration = len(activity) * dt
    f0 = crossings / (2.0 * duration)

    # Clamp to config range
    f0 = max(CFG['rhythm']['f0_min_hz'],
             min(CFG['rhythm']['f0_max_hz'], f0))

    # Phase: where are we in the current cycle?
    recent = activity[-4:]
    avg_recent = sum(recent) / len(recent)
    if avg_recent > 0.7:
        phase = math.pi / 2        # At peak
    elif avg_recent < 0.3:
        phase = 3 * math.pi / 2    # At trough
    elif activity[-1] > activity[-2]:
        phase = 0.0                 # Rising
    else:
        phase = math.pi             # Falling

    # Confidence from segment length regularity
    segment_lens = []
    current_len = 1
    for i in range(1, len(activity)):
        if (activity[i] > 0.5) == (activity[i-1] > 0.5):
            current_len += 1
        else:
            segment_lens.append(current_len)
            current_len = 1
    segment_lens.append(current_len)

    if len(segment_lens) < 3:
        confidence = 0.2
    else:
        avg_seg = sum(segment_lens) / len(segment_lens)
        var_seg = sum((s - avg_seg)**2 for s in segment_lens) / len(segment_lens)
        cv = math.sqrt(var_seg) / max(0.1, avg_seg)
        confidence = max(0.1, min(1.0, 1.0 - cv))

    return (f0, phase, confidence)


def classify_work_type(name: str, sched_class: str, last_op: int) -> str:
    """Classify what TYPE of work a process does.

    This is used by the TIG wave scheduler to match processes
    to the cheapest wave region for their work type.
    """
    name_lower = name.lower()

    # Study processes = heavy (need power-rising for cheap compute)
    study_names = CFG['task_target']['study_process_names']
    for sn in study_names:
        if sn in name_lower:
            return 'heavy'

    # Volatile / isolate = smooth (needs calm wave region)
    if sched_class in ('VOLATILE', 'ISOLATE'):
        return 'smooth'

    # Operators that indicate finalizing work
    if last_op in (COLLAPSE, RESET):
        return 'finalize'

    # Background services = precompute
    if sched_class == 'PREDICTABLE':
        return 'precompute'

    # Default
    return 'any'


# ═══════════════════════════════════════════════════════════
# §3  PULSE CANDIDATE + BTQ SCORING
# ═══════════════════════════════════════════════════════════

@dataclass
class PulseCandidate:
    """A proposed pulse action for a process.

    v2: now includes continuous pulse_duration (fraction of tick period)
    instead of just binary boost/yield.
    """
    pid: int
    amplitude: float          # 0.0 (yield) to 1.0 (full boost)
    duration: float = 0.5     # Fraction of pulse period (0.1 to 1.0)
    phase_offset: float = 0.0 # How offset from the resonant peak
    score_eff: float = 0.0
    score_stability: float = 0.0
    score_wave: float = 0.0   # TIG wave alignment score
    score_task: float = 0.0   # Task target progress score
    score_total: float = 0.0
    label: str = ''

    @property
    def is_boost(self) -> bool:
        return self.amplitude > 0.5

    @property
    def is_yield(self) -> bool:
        return self.amplitude < 0.1

    @property
    def effective_duty(self) -> float:
        """Effective duty cycle = amplitude * duration."""
        return self.amplitude * self.duration


def generate_candidates(rhythm: ProcessRhythm, wave: PowerWaveState,
                        n: int = 6) -> List[PulseCandidate]:
    """T-layer: Generate N pulse candidates for a process.

    v2 additions:
      - Continuous duration field
      - Bounded random exploration (NOT Levy -- bounded to config max)
      - Wave-aware resonant candidates
    """
    cfg_c = CFG['candidates']
    cfg_p = CFG['pulse_output']
    dur_default = cfg_p['duration_default_fraction']
    dur_min = cfg_p['duration_min_fraction']
    dur_max = cfg_p['duration_max_fraction']
    candidates = []

    if rhythm.is_rhythmic:
        # 1. Resonant: pulse at the peak with full duration
        res_amp = 0.9 if rhythm.phase_peak else 0.3
        res_dur = dur_max if rhythm.phase_peak else dur_default
        candidates.append(PulseCandidate(
            pid=rhythm.pid, amplitude=res_amp, duration=res_dur,
            phase_offset=0.0, label='resonant'))

        # 2. Explore: slightly off-phase, shorter duration (probe efficiency)
        explore_window = cfg_c['explore_phase_window_rad']
        for offset in [-explore_window, +explore_window]:
            adjusted = math.sin(rhythm.phase + offset)
            amp = max(0.1, min(0.9, adjusted * 0.8 + 0.1))
            dur = max(dur_min, min(dur_max, dur_default * (1.0 - abs(offset))))
            candidates.append(PulseCandidate(
                pid=rhythm.pid, amplitude=amp, duration=dur,
                phase_offset=offset, label='explore'))

    # 3. Bounded random (NOT Levy -- clamped to config max)
    random_max = cfg_c['random_phase_max_rad']
    # Use deterministic pseudo-random from pid + tick to avoid import random
    pseudo = ((rhythm.pid * 2654435761) & 0xFFFFFFFF) / 0xFFFFFFFF  # Knuth hash
    rand_offset = (pseudo - 0.5) * 2.0 * random_max  # bounded [-max, +max]
    rand_amp = max(0.1, min(0.9, pseudo))
    rand_dur = max(dur_min, min(dur_max, 0.3 + pseudo * 0.4))
    candidates.append(PulseCandidate(
        pid=rhythm.pid, amplitude=rand_amp, duration=rand_dur,
        phase_offset=rand_offset, label='random'))

    # 4. Scheduling-class-based candidate
    if rhythm.sched_class == 'PREDICTABLE':
        candidates.append(PulseCandidate(
            pid=rhythm.pid, amplitude=0.8, duration=0.7,
            phase_offset=0.0, label='steady'))
    elif rhythm.sched_class == 'ISOLATE':
        candidates.append(PulseCandidate(
            pid=rhythm.pid, amplitude=0.1, duration=dur_min,
            phase_offset=0.0, label='contain'))
    elif rhythm.sched_class == 'VOLATILE':
        candidates.append(PulseCandidate(
            pid=rhythm.pid, amplitude=0.2, duration=0.3,
            phase_offset=0.0, label='throttle'))
    else:
        candidates.append(PulseCandidate(
            pid=rhythm.pid, amplitude=0.5, duration=dur_default,
            phase_offset=0.0, label='neutral'))

    # 5. Always include a yield option (CPU sleeps)
    candidates.append(PulseCandidate(
        pid=rhythm.pid, amplitude=0.0, duration=dur_min,
        phase_offset=0.0, label='yield'))

    # 6. Full boost option (for comparison scoring)
    candidates.append(PulseCandidate(
        pid=rhythm.pid, amplitude=1.0, duration=dur_max,
        phase_offset=0.0, label='full'))

    return candidates[:n]


def score_candidate(candidate: PulseCandidate, rhythm: ProcessRhythm,
                    wave: PowerWaveState, power_watts: float,
                    cpu_temp: float, eff_target: float = 0.7) -> float:
    """Q-layer: Score a pulse candidate by predicted EFF + wave alignment.

    v2 scoring integrates:
      1. EFF = useful_work / energy (with slingshot bonus)
      2. 2-step lookahead: predict where rhythm will be next 2 ticks
      3. TIG wave alignment: is this work type cheap in current wave region?
      4. Task target weight: study processes get bonus
      5. Stability + thermal + smoothness (from v1)

    Returns total score (higher = better).
    """
    w = CFG['scoring']['weights']
    cfg_s = CFG['scoring']

    # ── 1. EFF score: work per joule ──
    if rhythm.is_rhythmic:
        phase_alignment = math.cos(candidate.phase_offset)
        slingshot = max(0.0, phase_alignment * cfg_s['slingshot_bonus_max'])
    else:
        slingshot = 0.0

    # effective_duty = amplitude * duration (actual CPU utilization fraction)
    duty = candidate.effective_duty
    useful_work = duty * (1.0 + slingshot)

    # Energy cost: duty * power * tick_period
    energy = duty * max(1.0, power_watts) * 0.02
    energy = max(0.001, energy)
    score_eff = useful_work / energy

    # ── 2. Two-step lookahead ──
    # Predict: if we apply this pulse now, where will the process be?
    # Simple kinematic: phase advances by 2*pi*f0*dt per tick
    lookahead_bonus = 0.0
    steps = cfg_s['lookahead_steps']
    if rhythm.is_rhythmic and steps > 0:
        future_phase = rhythm.phase + 2.0 * math.pi * rhythm.f0 * steps
        future_phase = future_phase % (2.0 * math.pi)
        # Will the process be at a peak in `steps` ticks?
        future_peak = math.sin(future_phase) > 0.7
        if future_peak and candidate.is_boost:
            # Boosting now primes the process to hit next peak with momentum
            lookahead_bonus = 0.2
        elif not future_peak and candidate.is_yield:
            # Yielding now saves energy because process won't peak anyway
            lookahead_bonus = 0.15

    # ── 3. TIG wave alignment ──
    # Is this process's work type cheap in the current wave region?
    wave_region = wave.wave_region
    work_type = rhythm.work_type if rhythm.work_type != 'any' else 'heavy'
    affinity_table = WAVE_WORK_AFFINITY.get(wave_region, {})
    wave_affinity = affinity_table.get(work_type, 0.3)

    # Score: high amplitude in a high-affinity region = good
    # Low amplitude in a low-affinity region = also good (save energy)
    if candidate.amplitude > 0.3:
        score_wave = wave_affinity * candidate.amplitude
    else:
        # Yielding in a bad-affinity region is smart
        score_wave = (1.0 - wave_affinity) * 0.3

    # ── 4. Task target: study processes get bonus ──
    score_task = 0.0
    task_cfg = CFG['task_target']
    name_lower = rhythm.name.lower()
    for sn in task_cfg['study_process_names']:
        if sn in name_lower:
            score_task = task_cfg['study_io_weight'] * duty
            break
    else:
        if rhythm.sched_class == 'PREDICTABLE':
            score_task = task_cfg['system_service_weight'] * duty
        elif rhythm.amplitude < 0.05:
            score_task = task_cfg['idle_spinner_weight'] * duty

    # ── 5. Stability penalty ──
    stability_penalty = 0.0
    if rhythm.sched_class == 'VOLATILE' and candidate.amplitude > 0.5:
        stability_penalty = -0.5
    if rhythm.sched_class == 'ISOLATE' and candidate.amplitude > 0.3:
        stability_penalty = -1.0

    # ── 6. Thermal penalty ──
    thermal_penalty = 0.0
    if cpu_temp > 80:
        thermal_penalty = -candidate.amplitude * cfg_s['thermal_penalty_80c']
    elif cpu_temp > 70:
        thermal_penalty = -candidate.amplitude * cfg_s['thermal_penalty_70c']

    # ── 7. Smoothness bonus ──
    smoothness = 1.0 - abs(candidate.amplitude - 0.5) * 0.5

    # ── Combine ──
    total = (
        score_eff * w['eff']
        + stability_penalty * w['stability']
        + thermal_penalty * w['thermal']
        + smoothness * w['smoothness']
        + score_wave * w.get('wave_alignment', 0.5)
        + score_task * w.get('task_progress', 0.6)
        + lookahead_bonus
    )

    # Store component scores for logging
    candidate.score_eff = score_eff
    candidate.score_stability = stability_penalty
    candidate.score_wave = score_wave
    candidate.score_task = score_task
    candidate.score_total = total

    return total


# ═══════════════════════════════════════════════════════════
# §4  ROYAL PULSE ENGINE
# ═══════════════════════════════════════════════════════════

class RoyalPulseEngine:
    """CK's pulsed control layer for desktop power efficiency.

    v2: Now includes TIG wave region classification, config-driven
    thresholds, continuous pulse duration, 2-step lookahead, and
    task_target awareness.

    Sits on top of the SteeringEngine. Where steering sets static
    priorities, RPE modulates them dynamically based on:
      - Process natural rhythm (from swarm)
      - Power waveform slope + curvature (TIG wave regions)
      - BTQ scoring (B=safety, T=candidates, Q=EFF)

    Tick rate: 1Hz on R16 (every 50th engine tick).
    """

    def __init__(self, swarm=None, power_sense=None):
        self.swarm = swarm
        self.power_sense = power_sense
        self.enabled = True

        # Per-process rhythm tracking
        self._rhythms: Dict[int, ProcessRhythm] = {}

        # Power waveform state (slope + curvature → TIG region)
        self.wave = PowerWaveState()

        # Pulse decisions log
        max_hist = CFG['logging']['max_decision_history']
        self._decisions: deque = deque(maxlen=max_hist)
        self.ticks = 0

        # Counters
        self.pulses_boosted = 0
        self.pulses_yielded = 0
        self.pulses_neutral = 0
        self.total_eff_score = 0.0
        self.total_wave_score = 0.0

        # Current power state
        self._power_watts = 10.0
        self._cpu_temp = 45.0
        self._eff_target = CFG['scoring']['eff_target_default']

        # Compute mode suggestion
        self.compute_mode = 'normal'

        print(f"  [RPE] Royal Pulse Engine v2 online (TIG wave scheduling)")

    def tick(self) -> dict:
        """One RPE tick. Full BTQ pipeline with TIG wave alignment.

        1. Update power waveform → classify TIG region
        2. B-layer safety filter
        3. Per-process: estimate rhythm → T-layer candidates → Q-layer score
        4. Emit: chosen pulse per process
        5. Update compute mode

        Returns dict with pulse stats + wave region.
        """
        self.ticks += 1

        if not self.enabled or self.swarm is None or not HAS_PSUTIL:
            return {'active': False}

        # ── Step 0: Update power waveform + classify TIG region ──
        self._update_power_state()
        self.wave.update(self._power_watts)

        # ── Step 1: B-layer safety filter ──
        if self._b_filter_global():
            self.compute_mode = 'reactive'
            return {
                'active': True, 'mode': 'reactive',
                'wave_region': self.wave.wave_region_name,
                'boosted': 0, 'yielded': 0, 'reason': 'b_filter'
            }

        # ── Step 2: Process each swarm cell ──
        boosted = 0
        yielded = 0
        neutral = 0
        n_candidates = CFG['candidates']['n_per_process']

        try:
            cells = list(self.swarm.cells.items())
        except RuntimeError:
            return {'active': True, 'mode': self.compute_mode,
                    'wave_region': self.wave.wave_region_name}

        for pid, cell in cells:
            if len(cell.ops) < CFG['rhythm']['min_ops_for_estimate']:
                continue
            if cell.name.lower() in _PROTECTED_PROCESS_NAMES:
                continue

            # 2a. Estimate rhythm
            rhythm = self._estimate(pid, cell)

            # 2b. Generate candidates (T-layer) -- now wave-aware
            candidates = generate_candidates(rhythm, self.wave, n=n_candidates)

            # 2c. Score candidates (Q-layer) -- now with wave alignment + lookahead
            best = None
            best_score = -999.0
            for c in candidates:
                s = score_candidate(c, rhythm, self.wave,
                                    self._power_watts, self._cpu_temp,
                                    self._eff_target)
                if s > best_score:
                    best_score = s
                    best = c

            # 2d. Emit: classify result
            if best and best.is_boost:
                boosted += 1
                self.pulses_boosted += 1
            elif best and best.is_yield:
                yielded += 1
                self.pulses_yielded += 1
            else:
                neutral += 1
                self.pulses_neutral += 1

            if best:
                self.total_eff_score += best.score_eff
                self.total_wave_score += best.score_wave

                # Log decision
                log_interval = CFG['logging']['log_every_n_ticks']
                if self.ticks % log_interval == 0:
                    self._decisions.append({
                        'tick': self.ticks,
                        'pid': pid,
                        'name': cell.name[:20],
                        'label': best.label,
                        'amp': round(best.amplitude, 2),
                        'dur': round(best.duration, 2),
                        'duty': round(best.effective_duty, 3),
                        'eff': round(best.score_eff, 3),
                        'wave': self.wave.wave_region_name,
                        'wave_score': round(best.score_wave, 3),
                        'work_type': rhythm.work_type,
                    })

        # ── Step 3: Update compute mode ──
        self._update_compute_mode(boosted, yielded, neutral)

        return {
            'active': True,
            'mode': self.compute_mode,
            'wave_region': self.wave.wave_region_name,
            'dH': round(self.wave.dH, 3),
            'd2H': round(self.wave.d2H, 4),
            'boosted': boosted,
            'yielded': yielded,
            'neutral': neutral,
            'avg_eff': round(self.total_eff_score / max(1, self.ticks), 3),
            'avg_wave': round(self.total_wave_score / max(1, self.ticks), 3),
            'tick': self.ticks,
        }

    def _estimate(self, pid: int, cell) -> ProcessRhythm:
        """Estimate or update rhythm for a process."""
        alpha = CFG['rhythm']['smoothing_alpha']

        if pid not in self._rhythms:
            self._rhythms[pid] = ProcessRhythm(pid=pid, name=cell.name)

        r = self._rhythms[pid]
        r.sched_class = cell.scheduling_class
        r.last_op = cell.last_op

        # Classify work type (for TIG wave matching)
        r.work_type = classify_work_type(cell.name, cell.scheduling_class, cell.last_op)

        # Estimate from ops history
        ops_list = list(cell.ops)
        min_ops = CFG['rhythm']['min_ops_for_estimate']
        if len(ops_list) >= min_ops * 2:
            f0, phase, conf = estimate_rhythm(ops_list, dt=1.0)
            # Smooth update
            r.f0 = r.f0 * (1.0 - alpha) + f0 * alpha
            r.phase = phase
            r.confidence = r.confidence * 0.8 + conf * 0.2

            # Amplitude from CPU percent
            try:
                proc = psutil.Process(pid)
                cpu_pct = proc.cpu_percent(interval=0)
                r.amplitude = min(1.0, cpu_pct / 100.0)
            except Exception:
                r.amplitude = 0.1

        return r

    def _update_power_state(self):
        """Read power/thermal from power sense module."""
        if self.power_sense is not None:
            try:
                if hasattr(self.power_sense, 'power_watts'):
                    self._power_watts = self.power_sense.power_watts
                if hasattr(self.power_sense, 'cpu_temp'):
                    self._cpu_temp = self.power_sense.cpu_temp
                elif hasattr(self.power_sense, 'temperature'):
                    self._cpu_temp = self.power_sense.temperature
            except Exception:
                pass
        else:
            # Fallback: psutil sensors
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            self._cpu_temp = entries[0].current
                            break
            except Exception:
                pass

    def _b_filter_global(self) -> bool:
        """B-layer safety: should we yield everything?

        Config-driven thresholds from ck_pulse_config.json.
        """
        safety = CFG['safety']

        # Thermal limit
        if self._cpu_temp > safety['cpu_temp_yield_c']:
            return True

        # Battery limit
        if HAS_PSUTIL:
            try:
                bat = psutil.sensors_battery()
                if bat and not bat.power_plugged:
                    if bat.percent < safety['battery_soc_yield_pct']:
                        return True
            except Exception:
                pass

        return False

    def _update_compute_mode(self, boosted: int, yielded: int, neutral: int):
        """Suggest compute mode based on power headroom, load, and wave region."""
        total = boosted + yielded + neutral
        if total == 0:
            self.compute_mode = 'normal'
            return

        yield_ratio = yielded / total
        boost_ratio = boosted / total

        # Wave region also influences mode suggestion
        # If wave is in CHAOS, go reactive regardless
        if self.wave.wave_region == WAVE_CHAOS:
            self.compute_mode = 'reactive'
        elif self._cpu_temp > 75 or yield_ratio > 0.6:
            self.compute_mode = 'reactive'
        elif boost_ratio > 0.4 and self._cpu_temp < 65:
            # Only go deep if wave is in PROGRESS or LATTICE (cheap regions)
            if self.wave.wave_region in (WAVE_PROGRESS, WAVE_LATTICE, WAVE_BREATH):
                self.compute_mode = 'deep'
            else:
                self.compute_mode = 'normal'
        else:
            self.compute_mode = 'normal'

    # ── Reporting ──

    @property
    def report_line(self) -> str:
        avg_eff = self.total_eff_score / max(1, self.ticks)
        avg_wave = self.total_wave_score / max(1, self.ticks)
        return (
            f"[RPE] t={self.ticks} mode={self.compute_mode} "
            f"wave={self.wave.wave_region_name} "
            f"dH={self.wave.dH:+.2f} d2H={self.wave.d2H:+.3f} "
            f"boost={self.pulses_boosted} yield={self.pulses_yielded} "
            f"eff={avg_eff:.3f} wave_score={avg_wave:.3f} "
            f"temp={self._cpu_temp:.0f}C watts={self._power_watts:.1f}W"
        )

    def stats(self) -> dict:
        avg_eff = self.total_eff_score / max(1, self.ticks)
        avg_wave = self.total_wave_score / max(1, self.ticks)
        return {
            'ticks': self.ticks,
            'compute_mode': self.compute_mode,
            'wave_region': self.wave.wave_region_name,
            'wave_dH': round(self.wave.dH, 3),
            'wave_d2H': round(self.wave.d2H, 4),
            'pulses_boosted': self.pulses_boosted,
            'pulses_yielded': self.pulses_yielded,
            'pulses_neutral': self.pulses_neutral,
            'avg_eff_score': round(avg_eff, 4),
            'avg_wave_score': round(avg_wave, 4),
            'power_watts': round(self._power_watts, 1),
            'cpu_temp': round(self._cpu_temp, 1),
            'rhythms_tracked': len(self._rhythms),
            'rhythmic_count': sum(1 for r in self._rhythms.values() if r.is_rhythmic),
        }


# Protected process names (same as steering engine)
_PROTECTED_PROCESS_NAMES = frozenset({
    'system', 'idle', 'registry', 'smss.exe', 'csrss.exe',
    'wininit.exe', 'services.exe', 'lsass.exe', 'svchost.exe',
    'dwm.exe', 'explorer.exe', 'winlogon.exe', 'fontdrvhost.exe',
    'sihost.exe', 'taskhostw.exe', 'runtimebroker.exe',
    'searchhost.exe', 'startmenuexperiencehost.exe',
    'lsaiso.exe', 'memcompression', 'ntoskrnl.exe',
    'securityhealthservice.exe', 'sgrmbroker.exe',
    'systemd', 'init', 'kthreadd', 'ksoftirqd',
})


# ═══════════════════════════════════════════════════════════
# §5  CLI SMOKE TEST
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60)
    print("  ROYAL PULSE ENGINE v2 -- Smoke Test")
    print("  TIG Wave Scheduling | Config-driven | 2-step lookahead")
    print("=" * 60)

    # Test wave classifier
    print("\n  Testing TIG wave region classifier:")
    wave = PowerWaveState()
    test_powers = [10, 11, 13, 16, 20, 19, 17, 14, 10, 9, 8, 9, 11, 14]
    for p in test_powers:
        wave.update(float(p))
        print(f"    P={p:3d}W  dH={wave.dH:+6.2f}  d2H={wave.d2H:+6.3f}"
              f"  region={wave.wave_region_name}")

    # Test RPE
    print(f"\n  Engine stats:")
    rpe = RoyalPulseEngine()
    print(f"    {rpe.stats()}")
    print(f"    {rpe.report_line}")

    # Test config loading
    print(f"\n  Config loaded: {len(CFG)} sections")
    for section in sorted(CFG.keys()):
        if not section.startswith('_'):
            print(f"    [{section}]")

    print(f"\n  (Wire to swarm + power_sense for live TIG wave scheduling)")
    print("=" * 60)
