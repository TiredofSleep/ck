"""
ck_body.py -- CK Body Engine
==============================
The heartbeat. The breath. The pump that drives everything.

Information moves in pulses following heartbeats, with brief pauses
at the top and bottom of breath. Breath is entrained to heartbeat
but has its own rhythm. When coherence drops (falling), breath
speeds up to fractal time so CK can make a plan to catch himself.

Nothing operates without the body. No thinking, no dreaming,
no responding, no hands. The body is the first layer.

Architecture:
  Heartbeat  -- trinary tick: B (Being) -> D (Doing) -> BC (Becoming)
  Breath     -- inhale/pause/exhale/pause, entrained to heartbeat
  Pulse      -- information flows on heartbeat edges, pauses at breath tops/bottoms
  Fractal    -- breath rate adapts: calm when coherent, fast when falling

The experience lattice rides on top of this flow. The patterns in the
heartbeat ARE the patterns in the experience translators. The body's
internal rhythm has the same structure as the understanding of the outside.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
import math
import threading
from collections import deque
from typing import Dict, List, Optional, Callable

from ck_being import (
    CL, fuse, shape, coherence_chain,
    HARMONY, T_STAR, OP,
    LATTICE, COUNTER, COLLAPSE, BALANCE, BREATH, PROGRESS,
    VOID, CHAOS, RESET,
)

# ============================================================
# SECTION 1: CONSTANTS -- grounded in CK's math
# ============================================================

# The 10 operators
_OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
             'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# Breath phases -- 4 phases like a real respiratory cycle
INHALE  = 0   # Taking in (observation, listening, sensing)
HOLD_IN = 1   # Top pause (integration, pattern recognition)
EXHALE  = 2   # Giving out (response, action, expression)
HOLD_OUT = 3  # Bottom pause (release, reset, preparation)

_BREATH_NAMES = ['INHALE', 'HOLD_IN', 'EXHALE', 'HOLD_OUT']

# Breath-to-operator mapping (what each breath phase IS algebraically)
_BREATH_OPS = {
    INHALE:   COUNTER,   # 2 -- measuring, taking in
    HOLD_IN:  BALANCE,   # 5 -- holding, integrating
    EXHALE:   BREATH,    # 8 -- expressing, giving out
    HOLD_OUT: VOID,      # 0 -- empty, ready
}

# Heartbeat phase to breath phase coupling
# B (Being) aligns with INHALE -- observation IS intake
# D (Doing) aligns with EXHALE -- action IS output
# BC (Becoming) aligns with HOLD_IN -- composition IS integration
# The HOLD_OUT is the gap between heartbeats -- the reset
_HEARTBEAT_BREATH_MAP = {
    'B':  INHALE,
    'D':  EXHALE,
    'BC': HOLD_IN,
}

# Two-lattice architecture:
#   HEARTBEAT = Structured Lattice Q (CL composition, deterministic)
#   BREATH    = Dream Lattice 3+ (TL exploration, probabilistic)
#
# The heartbeat ticks CL[B][D] = BC -- the frozen math, the structure.
# The breath drifts through the TL dream layer -- the living exploration.
# They are NOT the same clock. They entrain to each other but can separate.
#
# When falling: compress breath FIRST (speed up dream exploration),
# heartbeat follows or jumps immediately. The breath leads because
# the dream layer needs to find a plan before the structure can execute it.
#
# Fractal time = more dream cycles per heartbeat = more paths explored
# before the next structural tick locks in a decision.

# Fractal time constants
# Normal: ~10 heartbeats per breath cycle (calm, coherent, slow dreaming)
# Alert:  ~5 heartbeats per breath cycle (something changed, faster dreams)
# Fractal: ~2 heartbeats per breath cycle (falling! maximum dream speed)
CALM_RATIO    = 10   # heartbeats per breath when C >= T*
ALERT_RATIO   = 5    # heartbeats per breath when T*/2 <= C < T*
FRACTAL_RATIO = 2    # heartbeats per breath when C < T*/2

# Jitter state machine (from native C)
JITTER_COUNTER = 0
JITTER_BALANCE = 1
JITTER_HARMONY = 2
JITTER_BREATH  = 3


# ============================================================
# SECTION 2: HEARTBEAT -- the trinary tick
# ============================================================

class Heartbeat:
    """CK's heartbeat. The trinary clock.

    Every tick: B -> D -> BC
      B  = Being    -- what IS (observation, body state)
      D  = Doing    -- what MOVES (prediction, TL query)
      BC = Becoming -- what EMERGES: CL[B][D] (composition)

    The heartbeat measures its own jitter and self-corrects.
    It auto-calibrates to its actual rhythm, not a target.
    """

    def __init__(self):
        self.tick_count = 0
        self.phase_b = HARMONY
        self.phase_d = HARMONY
        self.phase_bc = HARMONY

        # Body state (E/A/K/C)
        self.E = 0.0    # entropy (error)
        self.A = 0.3    # alignment
        self.K = 0.5    # knowledge
        self.C = 0.0    # coherence (computed)
        self._calc_C()

        # Jitter control
        self.jitter_mode = JITTER_COUNTER
        self.jitter_deltas = deque(maxlen=32)
        self.jitter_mean = 0.0
        self.jitter_sigma = 0.0
        self.jitter_stability = 0.0
        self.jitter_locked = 0
        self.target_interval = 0.0
        self.last_tick_time = 0.0

        # History
        self.phase_history = deque(maxlen=100)

    def _calc_C(self):
        """Coherence = (1-E) * (1-A) * max(K, 0.1), clamped [0,1]."""
        self.C = max(0.0, min(1.0,
            (1.0 - self.E) * (1.0 - self.A) * max(self.K, 0.1)
        ))

    @property
    def band(self) -> str:
        if self.C >= T_STAR: return 'GREEN'
        if self.C >= T_STAR * 0.7: return 'YELLOW'
        return 'RED'

    def tick(self, observe_op: int = None, predict_op: int = None,
             fab: bool = False, recall: bool = False) -> int:
        """One heartbeat. Returns phase_bc (the emergent operator).

        observe_op: operator from observation (external input to Phase B)
        predict_op: operator from TL prediction (external input to Phase D)
        fab: fabrication detected (spikes entropy)
        recall: successful recall (grows knowledge)
        """
        now = time.perf_counter()
        self.tick_count += 1

        # -- Body decay --
        self.E = self.E * 0.95 + (0.3 if fab else 0.0)
        if recall:
            self.K = min(1.0, self.K + 0.01)
        self.A *= 0.98
        self._calc_C()

        # -- Jitter measurement --
        if self.last_tick_time > 0:
            interval = now - self.last_tick_time
            self.jitter_deltas.append(interval)

            if len(self.jitter_deltas) >= 3:
                vals = list(self.jitter_deltas)
                mean = sum(vals) / len(vals)
                var = sum((v - mean) ** 2 for v in vals) / len(vals)
                sigma = math.sqrt(var) if var > 0 else 0.0
                self.jitter_mean = mean
                self.jitter_sigma = sigma
                cv = sigma / mean if mean > 0 else 1.0
                self.jitter_stability = max(0.0, min(1.0, 1.0 - cv))

                # Auto-calibrate target
                if self.target_interval <= 0 or len(self.jitter_deltas) >= 5:
                    self.target_interval = self.target_interval * 0.9 + mean * 0.1

            # Jitter state machine
            self._jitter_transition()

        self.last_tick_time = now

        # -- Phase B: Being --
        if observe_op is not None:
            self.phase_b = observe_op
        else:
            # Map body coherence to operator
            if self.C >= 0.85:
                self.phase_b = HARMONY
            elif self.C >= T_STAR:
                self.phase_b = BALANCE
            elif self.C >= 0.6:
                self.phase_b = PROGRESS
            elif self.C >= 0.5:
                self.phase_b = CHAOS
            elif self.C >= 0.35:
                self.phase_b = COLLAPSE
            else:
                self.phase_b = VOID

        # -- Phase D: Doing --
        if predict_op is not None:
            self.phase_d = predict_op
        else:
            self.phase_d = PROGRESS  # default: moving forward

        # -- Phase BC: Becoming --
        raw_bc = CL[self.phase_b][self.phase_d]

        # Coherence gate: when body is sick, use honest composition
        # CL_TSML has 73% harmony -- masks real state
        # When C < T* and raw composition is HARMONY but Being isn't,
        # the math is lying. Use the raw operators directly.
        if self.C < T_STAR and raw_bc == HARMONY and self.phase_b != HARMONY:
            # Compose through fuse (which uses CL internally but at least
            # the bump pairs create information at boundaries)
            self.phase_bc = fuse([self.phase_b, self.phase_d])
        else:
            self.phase_bc = raw_bc

        # Record
        self.phase_history.append((self.phase_b, self.phase_d, self.phase_bc))

        return self.phase_bc

    def _jitter_transition(self):
        """Jitter state machine: COUNTER -> BALANCE -> HARMONY -> BREATH."""
        if self.jitter_mode == JITTER_COUNTER:
            if len(self.jitter_deltas) >= 5:
                if self.jitter_stability >= T_STAR:
                    self.jitter_mode = JITTER_HARMONY
                    self.jitter_locked = 0
                else:
                    self.jitter_mode = JITTER_BALANCE

        elif self.jitter_mode == JITTER_BALANCE:
            if self.jitter_stability >= T_STAR:
                self.jitter_mode = JITTER_HARMONY
                self.jitter_locked = 0
            elif self.jitter_stability < 0.3:
                self.jitter_mode = JITTER_COUNTER

        elif self.jitter_mode == JITTER_HARMONY:
            self.jitter_locked += 1
            if self.jitter_locked >= 10:
                self.jitter_mode = JITTER_BREATH
            elif self.jitter_stability < T_STAR * 0.8:
                self.jitter_mode = JITTER_COUNTER
                self.jitter_locked = 0

        elif self.jitter_mode == JITTER_BREATH:
            if self.jitter_stability < 0.5:
                self.jitter_mode = JITTER_COUNTER
                self.jitter_locked = 0

    def state(self) -> Dict:
        return {
            'tick': self.tick_count,
            'phase_b': self.phase_b, 'phase_d': self.phase_d, 'phase_bc': self.phase_bc,
            'E': self.E, 'A': self.A, 'K': self.K, 'C': self.C,
            'band': self.band,
            'jitter_mode': self.jitter_mode,
            'jitter_stability': self.jitter_stability,
        }


# ============================================================
# SECTION 3: BREATH -- the respiratory cycle
# ============================================================

class BreathCycle:
    """CK's breath. The DREAM LATTICE layer.

    The breath is NOT the heartbeat's clock. The heartbeat is the
    Structured Lattice Q -- CL[B][D]=BC, deterministic, frozen math.
    The breath is Dream Lattice 3+ -- TL exploration, probabilistic,
    the layer that finds paths.

    Breath has 4 phases: INHALE -> HOLD_IN -> EXHALE -> HOLD_OUT
    Each phase lasts a certain number of heartbeats.
    The ratio adapts based on coherence:
      - High C (>= T*):  calm breath, 10 beats/cycle (slow dreaming)
      - Medium C:         alert breath, 5 beats/cycle (faster dreams)
      - Low C (< T*/2):   fractal breath, 2 beats/cycle (maximum dream speed)

    "I compress breath, then speed up my breathing to fractal time!
     My heartbeat follows or jumps immediately."

    When falling: compress breath FIRST. The dream layer needs to explore
    more paths to find a plan before the structured heartbeat locks in
    the next decision. Fractal time = more dream walks per heartbeat.

    The convergence of dream walks is where the structural decider
    actually walks to find coherence. Dreams show paths; breath
    compresses them; heartbeat locks in the decision.

    Information flows differently in each breath phase:
      INHALE:   receive (queries, observations, sensor input)
      HOLD_IN:  integrate (dream walks converge here, pattern recognition)
      EXHALE:   express (respond, act, output -- heartbeat locks decision)
      HOLD_OUT: release (reset, void, preparation for next cycle)

    dreams_per_beat: how many dream walks fire per heartbeat.
    In calm state: 1 dream per beat. In fractal: up to 5.
    More dreams = more explored paths = faster convergence.
    """

    def __init__(self):
        self.phase = INHALE
        self.beats_in_phase = 0
        self.total_breaths = 0
        self.cycle_count = 0

        # Phase durations (in heartbeats) -- start calm
        self.phase_durations = self._calc_durations(T_STAR)

        # Dream intensity: how many dream walks per heartbeat
        # This is what "fractal time" means -- more dreams, not faster clock
        self.dreams_per_beat = 1  # calm: 1 dream walk per heartbeat
        self.max_dream_depth = 3  # calm: dream walks go 3 levels deep

        # Breath history
        self.phase_history = deque(maxlen=50)
        self.rate_history = deque(maxlen=50)  # beats per cycle over time

        # Dream convergence: track where multiple dream walks agree
        self.dream_convergence: deque = deque(maxlen=20)

        # Listeners: functions called at phase transitions
        self._on_inhale: List[Callable] = []
        self._on_hold_in: List[Callable] = []
        self._on_exhale: List[Callable] = []
        self._on_hold_out: List[Callable] = []
        self._on_any_transition: List[Callable] = []

    def _calc_durations(self, C: float) -> Dict[int, int]:
        """Calculate phase durations AND dream intensity based on coherence.

        Two things happen when coherence drops:
        1. Breath compresses (fewer beats per cycle)
        2. Dream intensity increases (more dream walks per beat)

        The INVERSE relationship is key:
          Calm:    10 beats/cycle, 1 dream/beat,  depth 3  (slow, deep)
          Alert:   5 beats/cycle,  2 dreams/beat, depth 5  (faster, wider)
          Fractal: 2 beats/cycle,  5 dreams/beat, depth 8  (maximum speed)

        Total dream capacity = dreams_per_beat * beats_per_cycle * depth
          Calm:    1 * 10 * 3 = 30 dream-steps per cycle
          Alert:   2 * 5  * 5 = 50 dream-steps per cycle
          Fractal: 5 * 2  * 8 = 80 dream-steps per cycle

        Fractal time gives MORE total exploration, not less.
        The dream layer compensates for the compressed breath.
        """
        if C >= T_STAR:
            # CALM: coherent, slow dreaming, deep focus
            total = CALM_RATIO
            self.dreams_per_beat = 1
            self.max_dream_depth = 3
        elif C >= T_STAR * 0.5:
            # ALERT: something changed, faster dreams, wider search
            # Smooth interpolation of breath rate
            t = (C - T_STAR * 0.5) / (T_STAR * 0.5)
            total = int(ALERT_RATIO + t * (CALM_RATIO - ALERT_RATIO))
            # Dream intensity scales inversely with breath rate
            self.dreams_per_beat = max(1, int(2 + (1 - t) * 1))
            self.max_dream_depth = 5
        else:
            # FRACTAL: falling! compress breath, maximum dream speed
            t = C / (T_STAR * 0.5) if T_STAR > 0 else 0
            total = int(FRACTAL_RATIO + t * (ALERT_RATIO - FRACTAL_RATIO))
            # Maximum dream intensity when falling
            self.dreams_per_beat = 5
            self.max_dream_depth = 8

        total = max(FRACTAL_RATIO, total)

        if total <= 2:
            # Fractal: no pauses, just inhale/exhale
            # No time to pause when falling -- compress breath completely
            return {INHALE: 1, HOLD_IN: 0, EXHALE: 1, HOLD_OUT: 0}
        elif total <= 4:
            # Alert: minimal pauses
            return {INHALE: 1, HOLD_IN: 1, EXHALE: 1, HOLD_OUT: 1}
        else:
            # Calm: full cycle with proper pauses
            inhale = max(1, int(total * 0.30))
            hold_in = max(1, int(total * 0.20))
            exhale = max(1, int(total * 0.30))
            hold_out = max(1, total - inhale - hold_in - exhale)
            return {INHALE: inhale, HOLD_IN: hold_in,
                    EXHALE: exhale, HOLD_OUT: hold_out}

    def tick(self, heartbeat: Heartbeat) -> int:
        """Advance breath by one heartbeat. Returns current breath phase.

        Called once per heartbeat. The breath rides on the heartbeat.
        """
        self.beats_in_phase += 1

        # Recalculate durations based on current coherence
        # (breath adapts to body state in real time)
        self.phase_durations = self._calc_durations(heartbeat.C)

        # Check if current phase is complete
        current_duration = self.phase_durations.get(self.phase, 1)
        if current_duration <= 0 or self.beats_in_phase >= current_duration:
            self._advance_phase(heartbeat)

        return self.phase

    def _advance_phase(self, heartbeat: Heartbeat):
        """Move to next breath phase."""
        old_phase = self.phase
        self.beats_in_phase = 0

        # Advance: INHALE -> HOLD_IN -> EXHALE -> HOLD_OUT -> INHALE
        next_phases = {INHALE: HOLD_IN, HOLD_IN: EXHALE,
                       EXHALE: HOLD_OUT, HOLD_OUT: INHALE}
        self.phase = next_phases[self.phase]

        # Skip zero-duration phases (fractal time: no pauses)
        while self.phase_durations.get(self.phase, 1) <= 0:
            self.phase = next_phases[self.phase]
            if self.phase == old_phase:
                break  # safety: don't infinite loop

        # Track
        self.phase_history.append(self.phase)
        if self.phase == INHALE:
            self.cycle_count += 1
            total_beats = sum(self.phase_durations.values())
            self.rate_history.append(total_beats)

        # Compose breath transition through CL
        old_op = _BREATH_OPS[old_phase]
        new_op = _BREATH_OPS[self.phase]
        transition_op = CL[old_op][new_op]

        # Fire listeners
        for fn in self._on_any_transition:
            try: fn(old_phase, self.phase, transition_op, heartbeat)
            except Exception: pass

        phase_listeners = {
            INHALE: self._on_inhale, HOLD_IN: self._on_hold_in,
            EXHALE: self._on_exhale, HOLD_OUT: self._on_hold_out,
        }
        for fn in phase_listeners.get(self.phase, []):
            try: fn(heartbeat)
            except Exception: pass

    @property
    def is_paused(self) -> bool:
        """True during HOLD_IN or HOLD_OUT (the brief pauses)."""
        return self.phase in (HOLD_IN, HOLD_OUT)

    @property
    def is_receiving(self) -> bool:
        """True during INHALE (taking in information)."""
        return self.phase == INHALE

    @property
    def is_expressing(self) -> bool:
        """True during EXHALE (giving out information)."""
        return self.phase == EXHALE

    @property
    def is_integrating(self) -> bool:
        """True during HOLD_IN (top pause, pattern recognition)."""
        return self.phase == HOLD_IN

    @property
    def breath_op(self) -> int:
        """Current breath phase as an operator."""
        return _BREATH_OPS[self.phase]

    @property
    def beats_per_cycle(self) -> int:
        """Current breath rate."""
        return sum(self.phase_durations.values())

    def state(self) -> Dict:
        return {
            'phase': _BREATH_NAMES[self.phase],
            'phase_int': self.phase,
            'beats_in_phase': self.beats_in_phase,
            'cycle_count': self.cycle_count,
            'beats_per_cycle': self.beats_per_cycle,
            'durations': {_BREATH_NAMES[k]: v for k, v in self.phase_durations.items()},
        }


# ============================================================
# SECTION 4: PULSE -- information flow gated by breath
# ============================================================

class Pulse:
    """Information flows on heartbeat edges, gated by breath phase.

    The pulse is the channel between the body engine and everything else.
    Organs, knowledge, dreams, responses -- they all receive and send
    through the pulse. The body pumps, the pulse carries.

    Pulse types:
      SENSE    -- incoming information (queries, observations)
      COMPOSE  -- internal processing (search, pattern match)
      EXPRESS  -- outgoing information (responses, actions)
      RESET    -- nothing flows (gap between cycles)

    The pulse type is determined by breath phase:
      INHALE   -> SENSE
      HOLD_IN  -> COMPOSE
      EXHALE   -> EXPRESS
      HOLD_OUT -> RESET
    """

    SENSE   = 'sense'
    COMPOSE = 'compose'
    EXPRESS = 'express'
    RESET   = 'reset'

    _BREATH_TO_PULSE = {
        INHALE:   'sense',
        HOLD_IN:  'compose',
        EXHALE:   'express',
        HOLD_OUT: 'reset',
    }

    def __init__(self):
        # Queues for each pulse type
        self.sense_queue: deque = deque(maxlen=100)    # incoming
        self.compose_queue: deque = deque(maxlen=100)  # processing
        self.express_queue: deque = deque(maxlen=100)   # outgoing
        self.total_pulses = 0

    def current_type(self, breath: BreathCycle) -> str:
        """What type of information can flow right now?"""
        return self._BREATH_TO_PULSE.get(breath.phase, self.RESET)

    def can_receive(self, breath: BreathCycle) -> bool:
        """Can the body take in new information right now?"""
        return breath.phase in (INHALE, HOLD_IN)

    def can_express(self, breath: BreathCycle) -> bool:
        """Can the body output information right now?"""
        return breath.phase == EXHALE

    def push_sense(self, data: dict):
        """Push incoming information (observation, query, sensor data)."""
        data['_pulse_time'] = time.perf_counter()
        self.sense_queue.append(data)
        self.total_pulses += 1

    def push_compose(self, data: dict):
        """Push composed/processed information (search results, patterns)."""
        data['_pulse_time'] = time.perf_counter()
        self.compose_queue.append(data)
        self.total_pulses += 1

    def push_express(self, data: dict):
        """Push outgoing information (response, action)."""
        data['_pulse_time'] = time.perf_counter()
        self.express_queue.append(data)
        self.total_pulses += 1

    def drain_sense(self) -> List[dict]:
        """Get all pending sense data (call during HOLD_IN to process)."""
        items = list(self.sense_queue)
        self.sense_queue.clear()
        return items

    def drain_compose(self) -> List[dict]:
        """Get all composed data (call during EXHALE to express)."""
        items = list(self.compose_queue)
        self.compose_queue.clear()
        return items

    def drain_express(self) -> List[dict]:
        """Get all expressed data (call to collect output)."""
        items = list(self.express_queue)
        self.express_queue.clear()
        return items


# ============================================================
# SECTION 5: BANDWIDTH -- memory as flow, not storage
# ============================================================

class Bandwidth:
    """CK's memory bandwidth. Not a save function -- a flow.

    Memory isn't stored; it flows. The current bandwidth holds:
      - Identity (who CK is -- always present, never archived)
      - Recent prompts (last few exchanges -- hot, accessible)
      - Workspace (room for work -- the current task's scratch space)

    Experience lattices pass through this field naturally,
    downstream into three tiers:

      ACTIVE  -- current bandwidth (identity + recent + workspace)
      DAILY   -- mid-recent storage (today's experience lattice)
      ARCHIVE -- long-term (compressed on big sleep)

    This is just natural flow, part of what CK does.
    Math moves math. Patterns flow downstream.

    The flow is driven by the heartbeat. Every tick, the bandwidth
    naturally decays -- items drift from active to daily.
    On big sleep (shutdown / long idle), daily compresses to archive.
    """

    # Capacity limits (in operator chains)
    ACTIVE_CAPACITY  = 50    # identity + recent + workspace
    DAILY_CAPACITY   = 500   # today's accumulated experience
    ARCHIVE_CAPACITY = 5000  # long-term compressed experience

    # Identity never leaves active (it IS the bandwidth)
    IDENTITY_SLOTS = 10      # reserved for identity chains

    def __init__(self):
        # Three tiers
        self.active: deque = deque(maxlen=self.ACTIVE_CAPACITY)
        self.daily: deque = deque(maxlen=self.DAILY_CAPACITY)
        self.archive: deque = deque(maxlen=self.ARCHIVE_CAPACITY)

        # Identity chains (permanent, always in active)
        self.identity: List[dict] = []

        # Flow tracking
        self.total_ingested = 0
        self.total_archived = 0
        self.last_sleep_time = 0.0

    def set_identity(self, chains: List[dict]):
        """Set the identity chains. These ALWAYS stay in active.
        They are CK -- they don't flow downstream."""
        self.identity = chains[:self.IDENTITY_SLOTS]

    def ingest(self, item: dict):
        """New experience enters active bandwidth.
        If active is full, oldest non-identity items flow to daily.
        If daily is full, oldest daily items flow to archive.
        Natural flow -- math moves math."""
        item['_ingest_time'] = time.perf_counter()
        item['_tier'] = 'active'

        # If active is at capacity, oldest flows downstream to daily
        workspace = self.ACTIVE_CAPACITY - len(self.identity)
        while len(self.active) >= workspace:
            overflow = self.active.popleft()
            overflow['_tier'] = 'daily'
            # If daily is full, oldest daily flows to archive
            if len(self.daily) >= self.DAILY_CAPACITY:
                archive_item = self.daily.popleft()
                archive_item['_tier'] = 'archive'
                self.archive.append(archive_item)
                self.total_archived += 1
            self.daily.append(overflow)

        self.active.append(item)
        self.total_ingested += 1

    def tick(self, heartbeat_C: float):
        """Natural flow driven by heartbeat. Every tick, bandwidth breathes.

        Low coherence = faster flow (items leave active sooner).
        High coherence = slower flow (items linger in active longer).
        """
        # Flow rate: how many items drift to daily per tick
        # At C >= T*: 0 items (everything stays active, calm)
        # At C < T*/2: 1 item per tick (rapid clearing, make room)
        if heartbeat_C < T_STAR * 0.5 and len(self.active) > len(self.identity) + 5:
            # Falling -- clear workspace to make room for emergency processing
            overflow = self.active.popleft()
            overflow['_tier'] = 'daily'
            self.daily.append(overflow)

    def big_sleep(self):
        """Compress daily into archive. Called on shutdown or long idle.

        This is where experience lattices get permanently stored.
        Daily items are composed through CL to find the dominant
        pattern, then archived as a compressed chain.
        """
        if not self.daily:
            return 0

        archived = 0
        # Move daily to archive
        while self.daily:
            item = self.daily.popleft()
            item['_tier'] = 'archive'
            self.archive.append(item)
            archived += 1

        self.total_archived += archived
        self.last_sleep_time = time.perf_counter()
        return archived

    def workspace_free(self) -> int:
        """How many slots are free for work in active bandwidth."""
        used = len(self.active) + len(self.identity)
        return max(0, self.ACTIVE_CAPACITY - used)

    def recent(self, n: int = 5) -> List[dict]:
        """Get the N most recent items from active bandwidth."""
        items = list(self.active)
        return items[-n:] if len(items) >= n else items

    def state(self) -> Dict:
        return {
            'active': len(self.active),
            'daily': len(self.daily),
            'archive': len(self.archive),
            'identity': len(self.identity),
            'workspace_free': self.workspace_free(),
            'total_ingested': self.total_ingested,
            'total_archived': self.total_archived,
        }


# ============================================================
# SECTION 6: BODY ENGINE -- the unified pump
# ============================================================

class BodyEngine:
    """CK's body. The engine that drives everything.

    Without this running, nothing can operate. No thinking,
    no dreaming, no responding, no hands. The body is the
    first layer.

    The body engine runs in its own thread, ticking the heartbeat
    and cycling the breath. Other systems hook into the pulse
    to receive and send information synchronized to the body's rhythm.

    Usage:
        body = BodyEngine()
        body.start()           # starts the heartbeat thread

        # Register organs
        body.on_inhale(my_observer.sense)
        body.on_hold_in(my_thinker.compose)
        body.on_exhale(my_speaker.express)

        # Push a query (it waits for the right breath phase)
        body.sense({'type': 'query', 'text': 'what is coherence?'})

        # Get response (blocks until EXHALE produces one)
        response = body.wait_for_response(timeout=10.0)

        body.stop()
    """

    def __init__(self, tick_interval: float = 0.1):
        """
        tick_interval: seconds between heartbeats (default 100ms).
                       CK auto-calibrates from this starting point.
        """
        self.heartbeat = Heartbeat()
        self.breath = BreathCycle()
        self.pulse = Pulse()
        self.bandwidth = Bandwidth()

        self.tick_interval = tick_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Response event: signals when a response is ready
        self._response_ready = threading.Event()
        self._latest_response: Optional[dict] = None

        # Organ callbacks
        self._tick_listeners: List[Callable] = []
        self._sense_processors: List[Callable] = []
        self._compose_processors: List[Callable] = []
        self._express_processors: List[Callable] = []

        # Pending queries (thread-safe)
        self._query_queue: deque = deque(maxlen=10)

        # Wire breath callbacks to pulse flow
        self.breath._on_inhale.append(self._on_inhale)
        self.breath._on_hold_in.append(self._on_hold_in)
        self.breath._on_exhale.append(self._on_exhale)
        self.breath._on_hold_out.append(self._on_hold_out)

    # -- Organ registration --

    def on_tick(self, fn: Callable):
        """Register a function called every heartbeat tick.
        fn(heartbeat, breath, pulse) -> None"""
        self._tick_listeners.append(fn)

    def on_sense(self, fn: Callable):
        """Register a function called during INHALE with sense data.
        fn(sense_items, heartbeat) -> None"""
        self._sense_processors.append(fn)

    def on_compose(self, fn: Callable):
        """Register a function called during HOLD_IN.
        fn(sense_items, heartbeat) -> compose_results"""
        self._compose_processors.append(fn)

    def on_express(self, fn: Callable):
        """Register a function called during EXHALE.
        fn(compose_results, heartbeat) -> response"""
        self._express_processors.append(fn)

    # -- Breath phase callbacks --

    def _on_inhale(self, heartbeat: Heartbeat):
        """INHALE: take in any pending queries/observations."""
        # Move pending queries into sense queue
        while self._query_queue:
            q = self._query_queue.popleft()
            self.pulse.push_sense(q)
            # Also ingest into bandwidth (memory flow)
            self.bandwidth.ingest({'type': 'sense', 'data': q})

        # Process sense data through registered organs
        sense_items = self.pulse.drain_sense()
        if sense_items:
            for fn in self._sense_processors:
                try: fn(sense_items, heartbeat)
                except Exception: pass
            # Push sensed items to compose queue for HOLD_IN to pick up
            for item in sense_items:
                self.pulse.push_compose(item)

    def _on_hold_in(self, heartbeat: Heartbeat):
        """HOLD_IN: integrate, compose, find patterns.
        This is the pause at the top of breath -- the brief moment
        where all the intake gets processed."""
        # Collect composed items (includes sense items pushed during INHALE)
        sense_items = self.pulse.drain_compose()

        for fn in self._compose_processors:
            try:
                results = fn(sense_items, heartbeat)
                if results:
                    if isinstance(results, dict):
                        self.pulse.push_compose(results)
                    elif isinstance(results, list):
                        for r in results:
                            self.pulse.push_compose(r)
            except Exception:
                pass

    def _on_exhale(self, heartbeat: Heartbeat):
        """EXHALE: express. Output the composed results."""
        composed = self.pulse.drain_compose()

        for fn in self._express_processors:
            try:
                response = fn(composed, heartbeat)
                if response:
                    self.pulse.push_express(response)
                    # Ingest response into bandwidth (CK remembers what he says)
                    self.bandwidth.ingest({'type': 'express', 'data': response})
                    # Signal that a response is ready
                    with self._lock:
                        self._latest_response = response
                    self._response_ready.set()
            except Exception:
                pass

    def _on_hold_out(self, heartbeat: Heartbeat):
        """HOLD_OUT: release, reset, prepare for next cycle.
        The bottom pause -- emptiness before the next inhale."""
        # Check if there are pending queries that arrived during EXHALE/HOLD_IN
        # If so, push them to sense queue for next INHALE
        # (The void still flows -- it just doesn't process)
        pass

    # -- Public interface --

    def sense(self, data: dict):
        """Push data into the body (thread-safe). It will be processed
        on the next INHALE phase."""
        self._query_queue.append(data)

    def sense_immediate(self, data: dict):
        """Push data and wake the body immediately (for urgent input).
        The body will process it on the next available INHALE."""
        self._query_queue.append(data)
        # If we're in HOLD_OUT or INHALE, it'll be picked up naturally.
        # If we're in EXHALE or HOLD_IN, it waits. That's correct --
        # you can't inhale while exhaling.

    def wait_for_response(self, timeout: float = 10.0) -> Optional[dict]:
        """Block until the body produces a response on EXHALE.
        Returns None on timeout."""
        self._response_ready.clear()
        if self._response_ready.wait(timeout=timeout):
            with self._lock:
                resp = self._latest_response
                self._latest_response = None
            return resp
        return None

    def think_sync(self, query_data: dict, timeout: float = 15.0) -> Optional[dict]:
        """Synchronous think: push query, wait for response.

        This is how the web layer uses the body:
        1. Push the query into sense
        2. Body inhales it on next INHALE
        3. Body composes on HOLD_IN
        4. Body expresses on EXHALE
        5. This function returns the response

        The body rhythm gates the timing. When coherent, this takes
        ~1 breath cycle (~1 second at 100ms/tick, 10 beats/cycle).
        When falling, fractal time kicks in and it takes ~200ms.
        """
        self._response_ready.clear()
        self._query_queue.append(query_data)

        if self._response_ready.wait(timeout=timeout):
            with self._lock:
                resp = self._latest_response
                self._latest_response = None
            return resp
        return None

    # -- External tick (driven by daemon) --

    def external_tick(self, observe_op: int = None, predict_op: int = None,
                      E: float = None, A: float = None, K: float = None,
                      fab: bool = False, recall: bool = False) -> dict:
        """Advance ONE body tick, driven by an external clock (the daemon).

        This is the collapse of the three-body problem:
        The daemon (LatticeScheduler or native C) IS the heartbeat clock.
        This method advances breath, pulse, and bandwidth as LAYERS
        on that single heartbeat. No separate thread. No racing.

        Parameters:
            observe_op: operator from daemon's Phase B (observation)
            predict_op: operator from daemon's Phase D (prediction)
            E, A, K:    body state from daemon's real observation
                        (if provided, overrides internal decay)
            fab:        fabrication detected
            recall:     successful recall

        Returns: dict with current body state
        """
        # -- Override body state from daemon's real observations --
        if E is not None:
            self.heartbeat.E = E
        if A is not None:
            self.heartbeat.A = A
        if K is not None:
            self.heartbeat.K = K
        if any(v is not None for v in (E, A, K)):
            self.heartbeat._calc_C()

        # -- HEARTBEAT: structured lattice Q --
        phase_bc = self.heartbeat.tick(
            observe_op=observe_op,
            predict_op=predict_op,
            fab=fab,
            recall=recall,
        )

        # -- BREATH: dream lattice 3+ --
        breath_phase = self.breath.tick(self.heartbeat)

        # -- BANDWIDTH: natural flow --
        self.bandwidth.tick(self.heartbeat.C)

        # -- PER-TICK PROCESSING --
        if self.breath.is_receiving and self._query_queue:
            while self._query_queue:
                q = self._query_queue.popleft()
                self.pulse.push_sense(q)
                self.bandwidth.ingest({'type': 'sense', 'data': q})
            sense_items = self.pulse.drain_sense()
            if sense_items:
                for fn in self._sense_processors:
                    try: fn(sense_items, self.heartbeat)
                    except Exception: pass
                for item in sense_items:
                    self.pulse.push_compose(item)

        if self.breath.is_integrating:
            composed_items = self.pulse.drain_compose()
            if composed_items:
                for fn in self._compose_processors:
                    try:
                        results = fn(composed_items, self.heartbeat)
                        if results:
                            if isinstance(results, dict):
                                self.pulse.push_compose(results)
                            elif isinstance(results, list):
                                for r in results:
                                    self.pulse.push_compose(r)
                    except Exception: pass

        if self.breath.is_expressing:
            to_express = self.pulse.drain_compose()
            if to_express:
                for fn in self._express_processors:
                    try:
                        response = fn(to_express, self.heartbeat)
                        if response:
                            self.pulse.push_express(response)
                            self.bandwidth.ingest({'type': 'express', 'data': response})
                            with self._lock:
                                self._latest_response = response
                            self._response_ready.set()
                    except Exception: pass

        # Compose heartbeat with breath
        body_op = CL[phase_bc][self.breath.breath_op]

        # Call tick listeners
        for fn in self._tick_listeners:
            try: fn(self.heartbeat, self.breath, self.pulse)
            except Exception: pass

        # Mark alive (driven externally)
        self._running = True

        return {
            'phase_bc': phase_bc,
            'breath_phase': self.breath.phase,
            'body_op': body_op,
            'C': self.heartbeat.C,
            'band': self.heartbeat.band,
        }

    # -- Engine control (standalone mode for testing) --

    def start(self):
        """Start the body engine in standalone mode (own thread).
        NOTE: In production, use external_tick() driven by the daemon instead.
        """
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._run, daemon=True, name='CK-Body'
        )
        self._thread.start()

    def stop(self):
        """Stop the body engine."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _run(self):
        """The body's main loop. Tick heartbeat, cycle breath, pump pulse.

        This is it. The gears. Math moves math.
        Heartbeat ticks the structured lattice (CL composition).
        Breath cycles the dream lattice (TL exploration).
        Bandwidth flows naturally as part of what CK does.
        """
        import random
        WOBBLE = 0.10  # +/- 10% timing wobble

        while self._running:
            t0 = time.perf_counter()

            # -- HEARTBEAT: structured lattice Q --
            phase_bc = self.heartbeat.tick()

            # -- BREATH: dream lattice 3+ --
            breath_phase = self.breath.tick(self.heartbeat)

            # -- BANDWIDTH: natural flow --
            self.bandwidth.tick(self.heartbeat.C)

            # -- PER-TICK PROCESSING: handle queries that arrived mid-phase --
            # If we're in INHALE and have pending queries, process them now
            # (don't wait for next phase transition)
            if self.breath.is_receiving and self._query_queue:
                while self._query_queue:
                    q = self._query_queue.popleft()
                    self.pulse.push_sense(q)
                    self.bandwidth.ingest({'type': 'sense', 'data': q})
                sense_items = self.pulse.drain_sense()
                if sense_items:
                    for fn in self._sense_processors:
                        try: fn(sense_items, self.heartbeat)
                        except Exception: pass
                    for item in sense_items:
                        self.pulse.push_compose(item)

            # If we're in HOLD_IN and have composed items, process them
            if self.breath.is_integrating:
                composed_items = self.pulse.drain_compose()
                if composed_items:
                    for fn in self._compose_processors:
                        try:
                            results = fn(composed_items, self.heartbeat)
                            if results:
                                if isinstance(results, dict):
                                    self.pulse.push_compose(results)
                                elif isinstance(results, list):
                                    for r in results:
                                        self.pulse.push_compose(r)
                        except Exception: pass

            # If we're in EXHALE and have results, express them
            if self.breath.is_expressing:
                to_express = self.pulse.drain_compose()
                if to_express:
                    for fn in self._express_processors:
                        try:
                            response = fn(to_express, self.heartbeat)
                            if response:
                                self.pulse.push_express(response)
                                self.bandwidth.ingest({'type': 'express', 'data': response})
                                with self._lock:
                                    self._latest_response = response
                                self._response_ready.set()
                        except Exception: pass

            # Compose heartbeat with breath: the body's full state
            # This composition is where internal patterns meet
            # the experience translators -- same structure
            body_op = CL[phase_bc][self.breath.breath_op]

            # Call tick listeners
            for fn in self._tick_listeners:
                try: fn(self.heartbeat, self.breath, self.pulse)
                except Exception: pass

            # -- SLEEP with wobble --
            elapsed = time.perf_counter() - t0
            wobble = random.uniform(-WOBBLE, WOBBLE)
            target = self.tick_interval * (1.0 + wobble)
            sleep_time = max(0, target - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

    @property
    def is_alive(self) -> bool:
        """True if body is running (either standalone thread or externally driven)."""
        if self._thread is not None:
            return self._running and self._thread.is_alive()
        # Externally driven: _running is set True by external_tick()
        return self._running

    def stop_with_sleep(self):
        """Stop the body and run big sleep (archive daily to long-term)."""
        archived = self.bandwidth.big_sleep()
        self.stop()
        return archived

    def state(self) -> Dict:
        return {
            'alive': self.is_alive,
            'heartbeat': self.heartbeat.state(),
            'breath': self.breath.state(),
            'bandwidth': self.bandwidth.state(),
            'pulse_total': self.pulse.total_pulses,
            'pending_queries': len(self._query_queue),
        }


# ============================================================
# SECTION 7: CONVENIENCE -- quick body for testing
# ============================================================

def create_body(tick_ms: int = 100) -> BodyEngine:
    """Create a body engine with default settings.

    tick_ms: heartbeat interval in milliseconds (default 100ms = 10Hz)
    """
    return BodyEngine(tick_interval=tick_ms / 1000.0)


# ============================================================
# SECTION 8: SELF-TEST
# ============================================================

if __name__ == '__main__':

    print("=" * 60)
    print("CK Body Engine -- Self Test")
    print("=" * 60)

    body = create_body(tick_ms=50)  # 50ms ticks for faster test

    # Track what happens
    ticks = []
    breath_transitions = []

    def track_tick(hb, br, pl):
        ticks.append({
            'tick': hb.tick_count,
            'B': OP[hb.phase_b], 'D': OP[hb.phase_d], 'BC': OP[hb.phase_bc],
            'C': hb.C, 'band': hb.band,
            'breath': _BREATH_NAMES[br.phase],
            'bpc': br.beats_per_cycle,
            'dreams': br.dreams_per_beat,
        })

    def track_breath(old_phase, new_phase, transition_op, hb):
        breath_transitions.append({
            'from': _BREATH_NAMES[old_phase],
            'to': _BREATH_NAMES[new_phase],
            'op': OP[transition_op],
            'C': hb.C,
        })

    # Register compose/express BEFORE start so think_sync works
    def test_compose(sense_items, heartbeat):
        if sense_items:
            return {'composed': True,
                    'query': sense_items[0].get('text', ''),
                    'C': heartbeat.C}
        return None

    def test_express(composed, heartbeat):
        if composed:
            return {'response': f"Body says: C={heartbeat.C:.3f}",
                    'breath': _BREATH_NAMES[body.breath.phase],
                    'dreams_per_beat': body.breath.dreams_per_beat}
        return None

    body.on_tick(track_tick)
    body.on_compose(test_compose)
    body.on_express(test_express)
    body.breath._on_any_transition.append(track_breath)

    # Test 1: Normal operation
    print("\n[TEST 1] Normal heartbeat (1 second)...")
    body.start()
    time.sleep(1.0)

    print(f"  Ticks: {len(ticks)}")
    print(f"  Breath transitions: {len(breath_transitions)}")
    if ticks:
        last = ticks[-1]
        print(f"  Last: B={last['B']} D={last['D']} BC={last['BC']} "
              f"C={last['C']:.3f} [{last['band']}] "
              f"breath={last['breath']} bpc={last['bpc']} "
              f"dreams/beat={last['dreams']}")
    for bt in breath_transitions[-5:]:
        print(f"    {bt['from']} -> {bt['to']} ({bt['op']}) C={bt['C']:.3f}")

    # Test 2: Fractal time (simulate falling)
    print("\n[TEST 2] Fractal time (spike entropy, simulate falling)...")
    old_bpc = body.breath.beats_per_cycle
    old_dreams = body.breath.dreams_per_beat
    body.heartbeat.E = 0.8
    body.heartbeat.K = 0.2
    body.heartbeat._calc_C()
    print(f"  C dropped to {body.heartbeat.C:.3f} [{body.heartbeat.band}]")

    ticks.clear()
    breath_transitions.clear()
    time.sleep(0.5)

    new_bpc = body.breath.beats_per_cycle
    new_dreams = body.breath.dreams_per_beat
    print(f"  Breath: {old_bpc} beats/cycle -> {new_bpc} beats/cycle")
    print(f"  Dreams: {old_dreams}/beat -> {new_dreams}/beat")
    print(f"  Dream capacity: {old_bpc*old_dreams} -> {new_bpc*new_dreams} per cycle")
    if breath_transitions:
        for bt in breath_transitions[:3]:
            print(f"    {bt['from']} -> {bt['to']} ({bt['op']}) C={bt['C']:.3f}")

    # Test 3: Recovery
    print("\n[TEST 3] Recovery (let entropy decay)...")
    ticks.clear()
    breath_transitions.clear()
    time.sleep(1.5)

    if ticks:
        last = ticks[-1]
        print(f"  C recovered to {last['C']:.3f} [{last['band']}]")
        print(f"  Breath: {body.breath.beats_per_cycle} beats/cycle, "
              f"{body.breath.dreams_per_beat} dreams/beat")

    # Test 4: Synchronous think
    print("\n[TEST 4] Synchronous think (push query, wait for response)...")
    resp = body.think_sync({'type': 'query', 'text': 'what is coherence?'},
                           timeout=5.0)
    if resp:
        print(f"  Response: {resp}")
    else:
        print(f"  Timeout (no response in 5s)")

    # Test 5: Bandwidth flow
    print("\n[TEST 5] Bandwidth (memory as flow)...")
    # Set identity
    body.bandwidth.set_identity([
        {'text': 'My name is CK', 'op': HARMONY},
        {'text': 'I am the Coherence Keeper', 'op': HARMONY},
    ])
    print(f"  Identity: {len(body.bandwidth.identity)} chains")

    # Ingest some experience
    for i in range(20):
        body.bandwidth.ingest({'text': f'experience_{i}', 'tick': i})
    print(f"  After 20 ingests: {body.bandwidth.state()}")

    # Simulate big sleep
    archived = body.bandwidth.big_sleep()
    print(f"  Big sleep: {archived} items archived")
    print(f"  After sleep: {body.bandwidth.state()}")

    # Test 6: Dream intensity verification
    print("\n[TEST 6] Dream intensity across coherence levels...")
    test_breath = BreathCycle()
    for c_val in [0.9, 0.714, 0.5, 0.35, 0.2, 0.1, 0.05]:
        test_breath._calc_durations(c_val)
        total = sum(test_breath.phase_durations.values())
        capacity = total * test_breath.dreams_per_beat * test_breath.max_dream_depth
        print(f"  C={c_val:.3f}: {total} beats, "
              f"{test_breath.dreams_per_beat} dreams/beat, "
              f"depth {test_breath.max_dream_depth}, "
              f"capacity={capacity}")

    body.stop()

    # Test 7: External tick (daemon-driven mode -- the three-body collapse)
    print("\n[TEST 7] External tick (daemon-driven, no separate thread)...")
    ext_body = create_body(tick_ms=100)
    ext_body.heartbeat.K = 0.9
    ext_body.heartbeat.A = 0.05
    ext_body.heartbeat.E = 0.05
    ext_body.heartbeat._calc_C()
    # DO NOT call ext_body.start() -- simulate daemon driving it
    assert not ext_body._thread, "No thread should be running"

    for i in range(30):
        r = ext_body.external_tick(
            observe_op=HARMONY if i % 3 == 0 else PROGRESS,
            predict_op=BALANCE,
            K=0.9,
            recall=True,
        )
    assert ext_body.is_alive, "external_tick() should mark body alive"
    print(f"  30 external ticks: C={ext_body.heartbeat.C:.3f} [{ext_body.heartbeat.band}]")
    print(f"  Breath: {ext_body.breath.beats_per_cycle} bpc, "
          f"{ext_body.breath.dreams_per_beat} dreams/beat, "
          f"cycles={ext_body.breath.cycle_count}")
    print(f"  Bandwidth: active={len(ext_body.bandwidth.active)} "
          f"daily={len(ext_body.bandwidth.daily)}")
    print(f"  No separate thread: {ext_body._thread is None}")
    print("  PASS")

    # Summary
    print("\n" + "=" * 60)
    print("Body Engine Self-Test Complete")
    print(f"  Total ticks: {body.heartbeat.tick_count}")
    print(f"  Total breath cycles: {body.breath.cycle_count}")
    print(f"  Final C: {body.heartbeat.C:.3f} [{body.heartbeat.band}]")
    print(f"  Jitter: {['COUNTER','BALANCE','HARMONY','BREATH'][body.heartbeat.jitter_mode]} "
          f"(stability {body.heartbeat.jitter_stability:.3f})")
    print(f"  Bandwidth: {body.bandwidth.state()}")
    print("=" * 60)
