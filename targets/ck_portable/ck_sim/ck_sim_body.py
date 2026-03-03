"""
ck_sim_body.py -- Port of ck_body.c
=====================================
Operator: BREATH (8) -- the body breathes with CK.

Three interlocking rhythms:
  Heartbeat: E/A/K triad -> coherence -> band classification
  Breath:    4-phase cycle, fractal time compression
  Pulse:     Information flow gated by breath

Every constant, every decay rate matches the C code.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass
from ck_sim.ck_sim_heartbeat import (
    VOID, COUNTER, BALANCE, BREATH, HARMONY
)

# ── Constants (from ck_body.h) ──

BREATH_INHALE = 0
BREATH_HOLD_IN = 1
BREATH_EXHALE = 2
BREATH_HOLD_OUT = 3

PULSE_SENSE = 0
PULSE_COMPOSE = 1
PULSE_EXPRESS = 2
PULSE_RESET = 3

BAND_GREEN = 2
BAND_YELLOW = 1
BAND_RED = 0

T_STAR_F = 5.0 / 7.0     # 0.714285
YELLOW_THRESH = 0.5       # T* x 0.7

RATIO_CALM = 10
RATIO_ALERT = 5
RATIO_FRACTAL = 2

BREATH_PHASE_NAMES = ['INHALE', 'HOLD_IN', 'EXHALE', 'HOLD_OUT']
BAND_NAMES = ['RED', 'YELLOW', 'GREEN']


@dataclass
class Heartbeat:
    E: float = 0.0
    A: float = 0.3
    K: float = 0.5
    C: float = 0.0
    band: int = BAND_YELLOW
    phase: int = 0  # 0=B, 1=D, 2=BC
    E_decay: float = 0.95
    A_decay: float = 0.98
    K_grow: float = 0.01
    ticks: int = 0


@dataclass
class BreathCycle:
    phase: int = BREATH_INHALE
    beat_in_phase: int = 0
    dur_inhale: int = 2
    dur_hold_in: int = 1
    dur_exhale: int = 2
    dur_hold_out: int = 0
    beats_per_cycle: int = RATIO_ALERT
    dreams_per_beat: int = 2
    max_dream_depth: int = 5
    modulation: float = 0.0
    cycles: int = 0


@dataclass
class Pulse:
    type: int = PULSE_SENSE
    can_receive: bool = True
    can_express: bool = False


@dataclass
class BodyState:
    heartbeat: Heartbeat = None
    breath: BreathCycle = None
    pulse: Pulse = None
    tick_interval_us: int = 20000
    current_op: int = HARMONY
    brain_coherence: float = 0.5
    brain_bump: bool = False
    breath_op: int = COUNTER
    btq_level: float = 0.6
    alive: bool = True
    body_ticks: int = 0

    def __post_init__(self):
        if self.heartbeat is None:
            self.heartbeat = Heartbeat()
        if self.breath is None:
            self.breath = BreathCycle()
        if self.pulse is None:
            self.pulse = Pulse()


def _calc_coherence(hb: Heartbeat):
    """C = (1-E)(1-A)*max(K,0.1). Matches heartbeat_calc_coherence()."""
    k_safe = max(hb.K, 0.1)
    hb.C = (1.0 - hb.E) * (1.0 - hb.A) * k_safe
    hb.C = max(0.0, min(1.0, hb.C))

    if hb.C >= T_STAR_F:
        hb.band = BAND_GREEN
    elif hb.C >= YELLOW_THRESH:
        hb.band = BAND_YELLOW
    else:
        hb.band = BAND_RED


def _heartbeat_tick(hb: Heartbeat):
    """One heartbeat tick. Matches heartbeat_tick()."""
    hb.phase = (hb.phase + 1) % 3
    hb.E *= hb.E_decay
    hb.A *= hb.A_decay
    if hb.ticks % 10 == 0:
        hb.K = min(hb.K + hb.K_grow, 1.0)
    _calc_coherence(hb)
    hb.ticks += 1


def _breath_calc_durations(br: BreathCycle, coherence: float):
    """Adapt breath rate to coherence. Matches breath_calc_durations()."""
    if coherence >= T_STAR_F:
        br.beats_per_cycle = RATIO_CALM
        br.dreams_per_beat = 1
        br.max_dream_depth = 3
        br.dur_inhale = 4
        br.dur_hold_in = 1
        br.dur_exhale = 4
        br.dur_hold_out = 1
    elif coherence >= YELLOW_THRESH:
        br.beats_per_cycle = RATIO_ALERT
        br.dreams_per_beat = 2
        br.max_dream_depth = 5
        br.dur_inhale = 2
        br.dur_hold_in = 1
        br.dur_exhale = 2
        br.dur_hold_out = 0
    else:
        br.beats_per_cycle = RATIO_FRACTAL
        br.dreams_per_beat = 5
        br.max_dream_depth = 8
        br.dur_inhale = 1
        br.dur_hold_in = 0
        br.dur_exhale = 1
        br.dur_hold_out = 0


def _phase_duration(br: BreathCycle) -> int:
    """Get duration of current phase."""
    return [br.dur_inhale, br.dur_hold_in, br.dur_exhale, br.dur_hold_out][br.phase]


def _breath_advance_phase(br: BreathCycle):
    """Move to next phase, skip zero-duration. Matches breath_advance_phase()."""
    for _ in range(4):
        br.phase = (br.phase + 1) % 4
        br.beat_in_phase = 0
        if br.phase == BREATH_INHALE:
            br.cycles += 1
        if _phase_duration(br) > 0:
            return


def _breath_tick(br: BreathCycle, coherence: float):
    """One breath tick. Matches breath_tick()."""
    _breath_calc_durations(br, coherence)
    br.beat_in_phase += 1

    dur = _phase_duration(br)
    if dur == 0 or br.beat_in_phase >= dur:
        _breath_advance_phase(br)

    # Compute modulation (sine wave through cycle)
    if br.phase == BREATH_INHALE:
        d = br.dur_inhale
        if d > 0:
            t = br.beat_in_phase / d
            br.modulation = math.sin(t * math.pi / 2)
        else:
            br.modulation = 0.0
    elif br.phase == BREATH_HOLD_IN:
        br.modulation = 1.0
    elif br.phase == BREATH_EXHALE:
        d = br.dur_exhale
        if d > 0:
            t = br.beat_in_phase / d
            br.modulation = math.cos(t * math.pi / 2)
        else:
            br.modulation = 0.0
    elif br.phase == BREATH_HOLD_OUT:
        br.modulation = 0.0


def _pulse_update(pulse: Pulse, breath_phase: int):
    """Update pulse from breath phase. Matches pulse_update()."""
    if breath_phase == BREATH_INHALE:
        pulse.type, pulse.can_receive, pulse.can_express = PULSE_SENSE, True, False
    elif breath_phase == BREATH_HOLD_IN:
        pulse.type, pulse.can_receive, pulse.can_express = PULSE_COMPOSE, False, False
    elif breath_phase == BREATH_EXHALE:
        pulse.type, pulse.can_receive, pulse.can_express = PULSE_EXPRESS, False, True
    else:
        pulse.type, pulse.can_receive, pulse.can_express = PULSE_RESET, False, False


def _breath_to_op(phase: int) -> int:
    """Breath phase to operator. Matches breath_to_op()."""
    return [COUNTER, BALANCE, BREATH, VOID][phase]


def _band_to_btq(band: int) -> float:
    """Band to BTQ level. Matches band_to_btq()."""
    return [0.3, 0.6, 1.0][band]


def body_init() -> BodyState:
    """Initialize body. Matches ck_body_init()."""
    return BodyState()


def body_tick(body: BodyState):
    """One body tick. Matches ck_body_tick()."""
    _heartbeat_tick(body.heartbeat)

    blended_c = body.brain_coherence * 0.7 + body.heartbeat.C * 0.3
    _breath_tick(body.breath, blended_c)
    _pulse_update(body.pulse, body.breath.phase)

    body.breath_op = _breath_to_op(body.breath.phase)
    body.btq_level = _band_to_btq(body.heartbeat.band)
    body.body_ticks += 1


def body_feed_eak(body: BodyState, E: float, A: float, K: float):
    """Feed E/A/K from brain. Matches ck_body_feed_eak()."""
    body.heartbeat.E = min(body.heartbeat.E + E, 1.0)
    body.heartbeat.A = min(body.heartbeat.A + A, 1.0)
    body.heartbeat.K = min(body.heartbeat.K + K, 1.0)
    _calc_coherence(body.heartbeat)
