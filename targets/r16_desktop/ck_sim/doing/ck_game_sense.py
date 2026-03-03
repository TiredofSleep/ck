# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_game_sense.py -- Digital Environment Perception: Game State → D2 → Operator
================================================================================
Operator: COUNTER (2) -- CK measures the digital world the same way it measures
the physical one.

THE FRACTAL INSIGHT (continued):
  D2 curvature doesn't care if the signal comes from an IMU, a microphone,
  or a game engine. The same 5D force vector
  (aperture, pressure, depth, binding, continuity) maps:
    - car velocity    → operators
    - ball position   → operators
    - boost level     → operators
    - score delta     → operators
    - screen pixels   → operators

  CK sees Rocket League the same way it sees its own body.
  One algebra. Many worlds. Same math.

Architecture:
  GameStateCodec       -- Game telemetry (position, velocity, boost, score)
                          → 5D force vector → D2 curvature → operator.
                          Extends SensorCodec. Plugs into SensorFusion.

  ScreenVisionCodec    -- Screen capture frame statistics → 5D force vector.
                          Like VisionCodec but tuned for game UI regions
                          (minimap, boost meter, scoreboard, field view).

  GameActionDomain     -- BTQ domain for game actions. Generates throttle/
                          steer/jump/boost/dodge candidates, filters by game
                          constraints, scores by macro+micro consistency.

  GameEnvironmentAdapter -- Bridges CK operator decisions → game input
                          commands. Handles frame-rate mismatch (game@120Hz
                          vs CK@50Hz). Tracks game state over time.

  GameRewardSignal     -- Maps game outcomes (goal scored, save made,
                          demolition, etc.) back to operator feedback for
                          the heartbeat. CK learns what HARMONY feels like
                          in the digital world.

Sensor Mapping for Rocket League:
  aperture   = field awareness (how much of the field is "visible" to CK)
  pressure   = speed pressure (car speed / max speed; boost commitment)
  depth      = scoring depth (proximity to goal; shot opportunity)
  binding    = ball-car coupling (tracking quality; interception alignment)
  continuity = state stability (smooth trajectory; no erratic jumps)

Zero external dependencies. Same algebra at every scale.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import random as _random
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sensory_codecs import CurvatureEngine, SensorCodec


# ================================================================
#  CONSTANTS
# ================================================================

# Rocket League field dimensions (Unreal units, approx)
FIELD_LENGTH = 10280.0   # goal-to-goal (x axis)
FIELD_WIDTH  = 8960.0    # sideline-to-sideline (y axis)
FIELD_HEIGHT = 2044.0    # ceiling

# Car physics constants
CAR_MAX_SPEED     = 2300.0   # uu/s with boost
CAR_SUPERSONIC    = 2200.0   # supersonic threshold
CAR_BOOST_MAX     = 100.0    # boost tank capacity
CAR_JUMP_IMPULSE  = 292.0    # initial jump velocity uu/s
BALL_MAX_SPEED    = 6000.0   # ball max speed uu/s

# Game state update rates
GAME_TICK_RATE    = 120      # Rocket League physics tick rate
CK_TICK_RATE      = 50       # CK heartbeat rate
TICKS_PER_CK      = GAME_TICK_RATE // CK_TICK_RATE  # ~2 game ticks per CK tick

# Goal positions (centered on goal line)
GOAL_BLUE = (-FIELD_LENGTH / 2, 0.0, 0.0)
GOAL_ORANGE = (FIELD_LENGTH / 2, 0.0, 0.0)

# Operator → game behavior mapping (like OPERATOR_TO_BEHAVIOR for motors)
OPERATOR_TO_GAME_ACTION = {
    VOID:     {'action': 'idle',      'throttle': 0.0, 'steer': 0.0, 'boost': False, 'jump': False},
    LATTICE:  {'action': 'position',  'throttle': 0.3, 'steer': 0.0, 'boost': False, 'jump': False},
    COUNTER:  {'action': 'observe',   'throttle': 0.2, 'steer': 0.0, 'boost': False, 'jump': False},
    PROGRESS: {'action': 'advance',   'throttle': 1.0, 'steer': 0.0, 'boost': True,  'jump': False},
    COLLAPSE: {'action': 'retreat',   'throttle': -1.0,'steer': 0.0, 'boost': False, 'jump': False},
    BALANCE:  {'action': 'rotate',    'throttle': 0.5, 'steer': 0.0, 'boost': False, 'jump': False},
    CHAOS:    {'action': 'challenge', 'throttle': 1.0, 'steer': 0.5, 'boost': True,  'jump': False},
    HARMONY:  {'action': 'flow',      'throttle': 0.7, 'steer': 0.0, 'boost': False, 'jump': False},
    BREATH:   {'action': 'wait',      'throttle': 0.0, 'steer': 0.0, 'boost': False, 'jump': False},
    RESET:    {'action': 'recover',   'throttle': 0.5, 'steer': 0.0, 'boost': False, 'jump': True},
}


# ================================================================
#  GAME STATE CODEC: Telemetry → D2 → Operator
# ================================================================

class GameStateCodec(SensorCodec):
    """Game engine telemetry → D2 → Operator.

    Maps game state (car position, velocity, ball state, boost, score)
    to 5D force vectors for D2 curvature classification.

    This is CK's primary sense in the digital world. It feels the
    game state the same way IMUCodec feels gravity.

    Expected raw_reading keys:
      car_x, car_y, car_z:     float (car position in field coords)
      car_vx, car_vy, car_vz:  float (car velocity uu/s)
      car_yaw:                 float (heading in radians)
      ball_x, ball_y, ball_z:  float (ball position)
      ball_vx, ball_vy, ball_vz: float (ball velocity)
      boost_amount:            float (0-100)
      team:                    int (0=blue, 1=orange)
      score_self:              int
      score_opponent:          int
      is_on_ground:            bool
      has_flip:                bool
    """

    def __init__(self, team: int = 0):
        super().__init__('game_state', sample_rate_hz=float(CK_TICK_RATE))
        self.team = team  # 0=blue, 1=orange
        self._prev_car_speed = 0.0
        self._prev_ball_dist = 0.0
        self._target_goal = GOAL_ORANGE if team == 0 else GOAL_BLUE
        self._own_goal = GOAL_BLUE if team == 0 else GOAL_ORANGE

    def map_to_force_vector(self, raw: dict) -> List[float]:
        """Map game telemetry to 5D force vector."""
        # Car state
        cx = raw.get('car_x', 0.0)
        cy = raw.get('car_y', 0.0)
        cz = raw.get('car_z', 0.0)
        cvx = raw.get('car_vx', 0.0)
        cvy = raw.get('car_vy', 0.0)
        cvz = raw.get('car_vz', 0.0)

        # Ball state
        bx = raw.get('ball_x', 0.0)
        by = raw.get('ball_y', 0.0)
        bz = raw.get('ball_z', 0.0)

        # Boost and score
        boost = raw.get('boost_amount', 50.0)

        # Derived quantities
        car_speed = math.sqrt(cvx*cvx + cvy*cvy + cvz*cvz)
        ball_dist = math.sqrt((bx-cx)**2 + (by-cy)**2 + (bz-cz)**2)

        # Distance to target goal
        gx, gy, gz = self._target_goal
        goal_dist = math.sqrt((gx-bx)**2 + (gy-by)**2)

        # Field diagonal for normalization
        field_diag = math.sqrt(FIELD_LENGTH**2 + FIELD_WIDTH**2)

        # ── aperture: field awareness ──
        # How much of the field the car "covers" -- based on position centrality
        # Center of field = max awareness, corners = low
        cx_norm = abs(cx) / (FIELD_LENGTH / 2)
        cy_norm = abs(cy) / (FIELD_WIDTH / 2)
        centrality = max(0.0, 1.0 - math.sqrt(cx_norm**2 + cy_norm**2) / 1.414)
        aperture = centrality

        # ── pressure: speed + boost commitment ──
        speed_pct = min(car_speed / CAR_MAX_SPEED, 1.0)
        boost_pct = boost / CAR_BOOST_MAX
        pressure = 0.6 * speed_pct + 0.4 * (1.0 - boost_pct)  # Low boost = high pressure

        # ── depth: scoring opportunity ──
        # Close to opponent goal with ball = deep scoring position
        max_goal_dist = field_diag
        goal_proximity = max(0.0, 1.0 - goal_dist / max_goal_dist)
        ball_proximity = max(0.0, 1.0 - ball_dist / max_goal_dist)
        depth = 0.7 * goal_proximity + 0.3 * ball_proximity

        # ── binding: ball-car coupling ──
        # How well the car tracks the ball (closer = stronger binding)
        binding = max(0.0, 1.0 - ball_dist / (field_diag * 0.5))

        # ── continuity: trajectory stability ──
        speed_delta = abs(car_speed - self._prev_car_speed)
        dist_delta = abs(ball_dist - self._prev_ball_dist)
        self._prev_car_speed = car_speed
        self._prev_ball_dist = ball_dist
        speed_stability = max(0.0, 1.0 - speed_delta / (CAR_MAX_SPEED * 0.2))
        dist_stability = max(0.0, 1.0 - dist_delta / (field_diag * 0.1))
        continuity = 0.5 * speed_stability + 0.5 * dist_stability

        return [
            max(0.0, min(aperture, 1.0)),
            max(0.0, min(pressure, 1.0)),
            max(0.0, min(depth, 1.0)),
            max(0.0, min(binding, 1.0)),
            max(0.0, min(continuity, 1.0)),
        ]


# ================================================================
#  SCREEN VISION CODEC: Game Screen Regions → D2 → Operator
# ================================================================

class ScreenVisionCodec(SensorCodec):
    """Screen capture statistics → D2 → Operator.

    Like VisionCodec but tuned for game UI. Processes pre-computed
    statistics from screen capture regions:
      - Field view (main gameplay area)
      - Minimap / positioning info
      - Boost meter
      - Scoreboard

    The raw statistics are computed externally (OpenCV, screen capture
    API, etc.). This codec maps them to 5D force vectors.

    Expected raw_reading keys:
      field_motion:       float [0, 1] -- optical flow in field region
      field_brightness:   float [0, 1] -- average brightness of field
      field_edges:        float [0, 1] -- edge density in field region
      boost_meter:        float [0, 1] -- boost gauge reading (OCR or pixel)
      score_delta:        float [-1, 1] -- recent score change (+ = us, - = them)
      minimap_density:    float [0, 1] -- how "busy" the minimap is
    """

    def __init__(self):
        super().__init__('screen_vision', sample_rate_hz=30.0)
        self._prev_motion = 0.0

    def map_to_force_vector(self, raw: dict) -> List[float]:
        """Map screen region statistics to 5D force vector."""
        motion     = raw.get('field_motion', 0.0)
        brightness = raw.get('field_brightness', 0.5)
        edges      = raw.get('field_edges', 0.0)
        boost_vis  = raw.get('boost_meter', 0.5)
        score_d    = raw.get('score_delta', 0.0)
        minimap    = raw.get('minimap_density', 0.0)

        # aperture: visual field openness (brightness + low density)
        aperture = max(0.0, min(brightness * (1.0 - minimap * 0.3), 1.0))

        # pressure: visual motion intensity
        pressure = max(0.0, min(motion, 1.0))

        # depth: visual complexity + score tension
        score_tension = min(abs(score_d), 1.0)
        depth = max(0.0, min(0.6 * edges + 0.4 * score_tension, 1.0))

        # binding: boost meter visibility (resource awareness)
        binding = max(0.0, min(boost_vis, 1.0))

        # continuity: smooth motion (no sudden visual jumps)
        motion_delta = abs(motion - self._prev_motion)
        self._prev_motion = motion
        continuity = max(0.0, min(1.0 - motion_delta * 2.0, 1.0))

        return [aperture, pressure, depth, binding, continuity]


# ================================================================
#  GAME ACTION: Candidate for BTQ Decision
# ================================================================

@dataclass
class GameAction:
    """A candidate game action for BTQ scoring."""
    throttle: float = 0.0       # [-1, 1] (reverse to full forward)
    steer: float = 0.0          # [-1, 1] (left to right)
    boost: bool = False
    jump: bool = False
    dodge_direction: float = 0.0  # radians, 0 = forward
    handbrake: bool = False
    action_name: str = "idle"
    # D2 analysis of the action sequence
    operator_sequence: List[int] = field(default_factory=list)
    d2_curvature: float = 0.0


# ================================================================
#  GAME ACTION DOMAIN: BTQ Decision Kernel for Game
# ================================================================

class GameActionDomain:
    """BTQ domain for Rocket League game actions.

    Generates, filters, and scores driving/flying actions through
    the same T→B→Q pipeline used for language, memory, and locomotion.

    CK doesn't know it's playing a game. It just sees operators
    and tries to find the path to HARMONY.
    """

    def __init__(self, seed: int = 42):
        self._name = "game_action"
        self.rng = _random.Random(seed)
        self._action_templates = [
            # (name, throttle, steer, boost, jump, dodge)
            ('idle',       0.0,  0.0,  False, False, 0.0),
            ('forward',    1.0,  0.0,  False, False, 0.0),
            ('boost_fwd',  1.0,  0.0,  True,  False, 0.0),
            ('reverse',   -1.0,  0.0,  False, False, 0.0),
            ('turn_left',  0.8, -1.0,  False, False, 0.0),
            ('turn_right', 0.8,  1.0,  False, False, 0.0),
            ('jump',       0.5,  0.0,  False, True,  0.0),
            ('dodge_fwd',  1.0,  0.0,  False, True,  0.0),
            ('dodge_left', 0.5, -0.5,  False, True,  -1.57),
            ('dodge_right',0.5,  0.5,  False, True,  1.57),
            ('powerslide', 0.8,  1.0,  False, False, 0.0),  # + handbrake
            ('aerial',     0.3,  0.0,  True,  True,  0.0),
        ]

    @property
    def name(self) -> str:
        return self._name

    def t_generate(self, env_state: dict, goal: dict, n: int) -> list:
        """Generate n game action candidates.

        Uses templates + perturbation. Same as BioLatticeDomain's
        Lévy-perturbed generation.
        """
        from ck_sim.ck_btq import Candidate

        candidates = []

        # Template-based candidates
        for tmpl in self._action_templates:
            name, throttle, steer, boost, jump, dodge = tmpl
            payload = GameAction(
                throttle=throttle,
                steer=steer,
                boost=boost,
                jump=jump,
                dodge_direction=dodge,
                handbrake=(name == 'powerslide'),
                action_name=name,
            )
            candidates.append(Candidate(
                domain=self._name,
                payload=payload,
                source=f"template_{name}",
            ))

        # Perturbed candidates (Lévy walk around templates)
        while len(candidates) < n:
            base = self.rng.choice(self._action_templates)
            name, throttle, steer, boost, jump, dodge = base
            # Perturb throttle and steer
            throttle = max(-1.0, min(1.0, throttle + self.rng.gauss(0, 0.2)))
            steer = max(-1.0, min(1.0, steer + self.rng.gauss(0, 0.3)))
            # Random boost/jump toggles
            if self.rng.random() < 0.2:
                boost = not boost
            if self.rng.random() < 0.1:
                jump = not jump

            payload = GameAction(
                throttle=throttle,
                steer=steer,
                boost=boost,
                jump=jump,
                dodge_direction=dodge + self.rng.gauss(0, 0.5),
                handbrake=self.rng.random() < 0.05,
                action_name=f"perturb_{name}",
            )
            candidates.append(Candidate(
                domain=self._name,
                payload=payload,
                source=f"levy_{len(candidates)}",
            ))

        return candidates[:n]

    def b_check(self, candidate, env_state: dict) -> Tuple[bool, str]:
        """Hard constraints for game actions.

        - Can't boost without boost fuel
        - Can't dodge without flip available
        - Can't jump if not on ground and no flip
        - Throttle must be in [-1, 1]
        """
        ga = candidate.payload
        boost_amount = env_state.get('boost_amount', 50.0)
        on_ground = env_state.get('is_on_ground', True)
        has_flip = env_state.get('has_flip', True)

        # Boost check: need fuel
        if ga.boost and boost_amount <= 0:
            return False, "no_boost"

        # Jump/dodge check: need ground or flip
        if ga.jump:
            if not on_ground and not has_flip:
                return False, "no_flip"

        # Range check
        if not (-1.0 <= ga.throttle <= 1.0):
            return False, "throttle_range"
        if not (-1.0 <= ga.steer <= 1.0):
            return False, "steer_range"

        return True, "approved"

    def einstein_score(self, candidate, env_state: dict) -> Tuple[float, dict]:
        """E_out: macro consistency -- does this action make strategic sense?

        Scores based on:
          - Ball pursuit: are we moving toward the ball?
          - Goal alignment: are we pushing ball toward opponent goal?
          - Boost efficiency: are we wasting boost?
          - Defensive responsibility: are we leaving our goal exposed?
        """
        ga = candidate.payload

        # Extract state
        car_x = env_state.get('car_x', 0.0)
        car_y = env_state.get('car_y', 0.0)
        ball_x = env_state.get('ball_x', 0.0)
        ball_y = env_state.get('ball_y', 0.0)
        boost_amount = env_state.get('boost_amount', 50.0)
        score_diff = env_state.get('score_self', 0) - env_state.get('score_opponent', 0)

        # Ball direction (simplified: positive throttle when ball is ahead)
        ball_ahead = (ball_x - car_x)  # positive = ball is in front (for blue team)
        team = env_state.get('team', 0)
        if team == 1:
            ball_ahead = -ball_ahead  # Flip for orange

        # Ball pursuit cost: penalize going away from ball
        if ga.throttle > 0 and ball_ahead > 0:
            pursuit_cost = 0.0  # Good: moving toward ball
        elif ga.throttle < 0 and ball_ahead < 0:
            pursuit_cost = 0.0  # Good: reversing toward ball behind us
        elif ga.throttle > 0 and ball_ahead < 0:
            pursuit_cost = 0.6  # Bad: driving away from ball
        else:
            pursuit_cost = 0.3  # Neutral

        # Boost efficiency: penalize boosting when not needed
        boost_cost = 0.0
        if ga.boost:
            if boost_amount < 20:
                boost_cost = 0.7  # Wasting last boost
            elif abs(ga.throttle) < 0.3:
                boost_cost = 0.5  # Boosting while barely moving

        # Defensive cost: penalize leaving goal exposed when losing
        defense_cost = 0.0
        if score_diff < 0:
            own_goal_x = -FIELD_LENGTH / 2 if team == 0 else FIELD_LENGTH / 2
            # If car is far from own goal and ball is near own goal
            car_to_own = abs(car_x - own_goal_x) / FIELD_LENGTH
            ball_to_own = abs(ball_x - own_goal_x) / FIELD_LENGTH
            if ball_to_own < 0.3 and car_to_own > 0.5:
                defense_cost = 0.6

        e_out = 0.40 * pursuit_cost + 0.30 * boost_cost + 0.30 * defense_cost

        details = {
            'pursuit_cost': pursuit_cost,
            'boost_cost': boost_cost,
            'defense_cost': defense_cost,
            'ball_ahead': ball_ahead,
        }
        return float(max(0.0, min(e_out, 1.0))), details

    def tesla_score(self, candidate) -> Tuple[float, dict]:
        """E_in: micro resonance -- does this action "feel" coherent?

        Scores based on:
          - Action smoothness: gentle inputs = smoother D2 = more HARMONY
          - Input complexity: fewer simultaneous inputs = cleaner signal
          - Action novelty: doing something different from template = higher curvature
        """
        ga = candidate.payload

        # Smoothness: extreme inputs have high curvature
        throttle_extremity = abs(ga.throttle)
        steer_extremity = abs(ga.steer)
        input_magnitude = math.sqrt(throttle_extremity**2 + steer_extremity**2) / 1.414
        smoothness_cost = min(input_magnitude, 1.0)

        # Complexity: how many inputs active simultaneously
        active_count = 0
        if abs(ga.throttle) > 0.1:
            active_count += 1
        if abs(ga.steer) > 0.1:
            active_count += 1
        if ga.boost:
            active_count += 1
        if ga.jump:
            active_count += 1
        if ga.handbrake:
            active_count += 1
        complexity_cost = min(active_count / 3.0, 1.0)  # 3+ inputs = max complexity

        e_in = 0.60 * smoothness_cost + 0.40 * complexity_cost

        details = {
            'smoothness_cost': smoothness_cost,
            'complexity_cost': complexity_cost,
            'active_inputs': active_count,
        }
        return float(max(0.0, min(e_in, 1.0))), details


# ================================================================
#  GAME REWARD SIGNAL: Outcomes → Operator Feedback
# ================================================================

# Game events → operator mapping
# These feed back into the heartbeat as phase_d signals
GAME_EVENT_TO_OPERATOR = {
    'goal_scored':       HARMONY,     # Scored! Pure HARMONY.
    'goal_conceded':     COLLAPSE,    # Conceded. COLLAPSE.
    'save':              BALANCE,     # Saved! BALANCE achieved.
    'assist':            LATTICE,     # Assisted. Structure created.
    'shot_on_goal':      PROGRESS,    # Shot! Making PROGRESS.
    'demolition':        CHAOS,       # Destroyed opponent. CHAOS.
    'demolished':        RESET,       # Got destroyed. RESET needed.
    'boost_pickup':      BREATH,      # Refueled. BREATH of energy.
    'ball_touch':        COUNTER,     # Touched ball. COUNTER (measuring).
    'aerial_hit':        PROGRESS,    # Aerial! Advanced PROGRESS.
    'center_ball':       LATTICE,     # Centered. Building LATTICE.
    'clear_ball':        BALANCE,     # Cleared danger. BALANCE.
    'overtime':          CHAOS,       # Overtime tension. CHAOS.
    'win':               HARMONY,     # Victory. Deep HARMONY.
    'loss':              COLLAPSE,    # Defeat. COLLAPSE.
    'kickoff':           RESET,       # New start. RESET.
}


class GameRewardSignal:
    """Maps game outcomes to operator feedback for the heartbeat.

    CK learns what HARMONY feels like in the game:
    - Goals scored → HARMONY
    - Smart plays → LATTICE/BALANCE
    - Getting destroyed → COLLAPSE/RESET

    These operators feed into phase_d, mixing with the game state
    codec's operators in the CL composition table.
    """

    def __init__(self):
        self._event_history: deque = deque(maxlen=64)
        self._reward_operator = VOID
        self._event_counts: Dict[str, int] = {}

    def signal(self, event_name: str) -> int:
        """Process a game event and return the reward operator.

        Args:
            event_name: Key from GAME_EVENT_TO_OPERATOR.

        Returns:
            Operator (0-9) for this event.
        """
        operator = GAME_EVENT_TO_OPERATOR.get(event_name, VOID)
        self._event_history.append((event_name, operator))
        self._reward_operator = operator
        self._event_counts[event_name] = self._event_counts.get(event_name, 0) + 1
        return operator

    @property
    def reward_operator(self) -> int:
        """Most recent reward operator."""
        return self._reward_operator

    def fuse_recent(self, n: int = 8) -> int:
        """Fuse the last n reward operators through CL.

        Returns the running fuse — CK's "mood" from recent game events.
        """
        recent = list(self._event_history)[-n:]
        if not recent:
            return VOID
        result = recent[0][1]
        for _, op in recent[1:]:
            result = compose(result, op)
        return result

    def coherence(self) -> float:
        """Harmony ratio in recent events."""
        if not self._event_history:
            return 0.0
        harmony_count = sum(1 for _, op in self._event_history if op == HARMONY)
        return harmony_count / len(self._event_history)

    def stats(self) -> dict:
        return {
            'reward_operator': OP_NAMES[self._reward_operator],
            'recent_fuse': OP_NAMES[self.fuse_recent()],
            'coherence': round(self.coherence(), 3),
            'event_counts': dict(self._event_counts),
            'total_events': sum(self._event_counts.values()),
        }


# ================================================================
#  GAME ENVIRONMENT ADAPTER: CK Decisions → Game Inputs
# ================================================================

class GameEnvironmentAdapter:
    """Bridges CK operator decisions to game input commands.

    The adapter:
    1. Takes the operator from the heartbeat (or BTQ decision)
    2. Maps it to a game action via OPERATOR_TO_GAME_ACTION
    3. Optionally blends with BTQ-selected GameAction candidate
    4. Outputs a final input command dict for the game

    Also handles:
    - Frame rate bridging (game@120Hz, CK@50Hz)
    - Input smoothing (avoid jerky inputs)
    - Action persistence (hold actions for multiple game ticks)
    """

    def __init__(self, ck_rate: int = CK_TICK_RATE, game_rate: int = GAME_TICK_RATE):
        self.ck_rate = ck_rate
        self.game_rate = game_rate
        self.ticks_per_ck = max(1, game_rate // ck_rate)
        self._current_action: Dict[str, Any] = OPERATOR_TO_GAME_ACTION[VOID].copy()
        self._hold_counter = 0
        self._action_history: deque = deque(maxlen=32)
        self._smooth_throttle = 0.0
        self._smooth_steer = 0.0
        self._smoothing_rate = 0.3  # EMA smoothing factor

    def update_from_operator(self, operator: int) -> Dict[str, Any]:
        """Convert a heartbeat operator to a game input.

        This is the "reflex" path — fast, operator-driven.
        For deliberate actions, use update_from_btq().
        """
        template = OPERATOR_TO_GAME_ACTION.get(operator, OPERATOR_TO_GAME_ACTION[VOID])
        action = template.copy()
        action['source'] = 'operator'
        action['operator'] = operator
        action['operator_name'] = OP_NAMES[operator]

        self._apply_smoothing(action)
        self._current_action = action
        self._action_history.append(action)
        self._hold_counter = self.ticks_per_ck  # Hold for game ticks
        return action

    def update_from_btq(self, game_action: GameAction) -> Dict[str, Any]:
        """Convert a BTQ-selected GameAction to a game input.

        This is the "deliberate" path — slower, scored.
        """
        action = {
            'action': game_action.action_name,
            'throttle': game_action.throttle,
            'steer': game_action.steer,
            'boost': game_action.boost,
            'jump': game_action.jump,
            'handbrake': game_action.handbrake,
            'source': 'btq',
        }

        self._apply_smoothing(action)
        self._current_action = action
        self._action_history.append(action)
        self._hold_counter = self.ticks_per_ck
        return action

    def game_tick(self) -> Dict[str, Any]:
        """Called at game tick rate. Returns current held action.

        Between CK ticks, the adapter holds the last action,
        providing input continuity at the game's frame rate.
        """
        if self._hold_counter > 0:
            self._hold_counter -= 1
        return self._current_action

    def _apply_smoothing(self, action: dict):
        """EMA smoothing on throttle and steer to avoid jerk."""
        r = self._smoothing_rate
        target_t = action.get('throttle', 0.0)
        target_s = action.get('steer', 0.0)

        self._smooth_throttle = r * target_t + (1 - r) * self._smooth_throttle
        self._smooth_steer = r * target_s + (1 - r) * self._smooth_steer

        action['throttle_smooth'] = round(self._smooth_throttle, 4)
        action['steer_smooth'] = round(self._smooth_steer, 4)

    @property
    def current_action(self) -> Dict[str, Any]:
        return self._current_action

    def stats(self) -> dict:
        return {
            'current_action': self._current_action.get('action', 'idle'),
            'smooth_throttle': round(self._smooth_throttle, 4),
            'smooth_steer': round(self._smooth_steer, 4),
            'hold_counter': self._hold_counter,
            'history_size': len(self._action_history),
        }


# ================================================================
#  GAME SESSION: Orchestrates all game senses
# ================================================================

class GameSession:
    """Top-level orchestrator for CK in a game environment.

    Combines:
    - GameStateCodec (telemetry sense)
    - ScreenVisionCodec (visual sense)
    - GameRewardSignal (reward feedback)
    - GameEnvironmentAdapter (action output)
    - GameActionDomain (BTQ decisions)

    Usage:
        session = GameSession(team=0)
        session.feed_state(game_telemetry)
        session.feed_screen(screen_stats)
        session.on_event('goal_scored')
        action = session.get_action()
    """

    def __init__(self, team: int = 0, seed: int = 42):
        self.team = team
        self.state_codec = GameStateCodec(team=team)
        self.screen_codec = ScreenVisionCodec()
        self.reward = GameRewardSignal()
        self.adapter = GameEnvironmentAdapter()
        self.action_domain = GameActionDomain(seed=seed)

        # Running state
        self._tick_count = 0
        self._state_operator = VOID
        self._screen_operator = VOID
        self._fused_operator = VOID

    def feed_state(self, raw_telemetry: dict) -> int:
        """Feed game telemetry. Returns classified operator."""
        self._state_operator = self.state_codec.feed(raw_telemetry)
        self._update_fused()
        self._tick_count += 1
        return self._state_operator

    def feed_screen(self, screen_stats: dict) -> int:
        """Feed screen capture statistics. Returns classified operator."""
        self._screen_operator = self.screen_codec.feed(screen_stats)
        self._update_fused()
        return self._screen_operator

    def on_event(self, event_name: str) -> int:
        """Process a game event. Returns reward operator."""
        return self.reward.signal(event_name)

    def get_action(self, use_btq: bool = False,
                   env_state: dict = None) -> Dict[str, Any]:
        """Get the next game action.

        If use_btq=True, runs the full BTQ pipeline for deliberate
        action selection. Otherwise, uses operator-driven reflex.
        """
        if use_btq and env_state:
            # Full BTQ decision
            candidates = self.action_domain.t_generate(env_state, {}, 32)
            approved = [c for c in candidates
                        if self.action_domain.b_check(c, env_state)[0]]
            if approved:
                # Score and select best
                best = None
                best_total = float('inf')
                for cand in approved:
                    e_out, _ = self.action_domain.einstein_score(cand, env_state)
                    e_in, _ = self.action_domain.tesla_score(cand)
                    e_total = 0.5 * e_out + 0.5 * e_in
                    if e_total < best_total:
                        best_total = e_total
                        best = cand
                if best:
                    return self.adapter.update_from_btq(best.payload)

        # Reflex path: use fused operator
        return self.adapter.update_from_operator(self._fused_operator)

    def _update_fused(self):
        """Fuse state and screen operators through CL."""
        self._fused_operator = compose(self._state_operator, self._screen_operator)

    @property
    def fused_operator(self) -> int:
        return self._fused_operator

    def coherence(self) -> float:
        """Average coherence across game senses."""
        c1 = self.state_codec.coherence()
        c2 = self.screen_codec.coherence()
        return (c1 + c2) / 2.0

    def stats(self) -> dict:
        return {
            'tick': self._tick_count,
            'state_operator': OP_NAMES[self._state_operator],
            'screen_operator': OP_NAMES[self._screen_operator],
            'fused_operator': OP_NAMES[self._fused_operator],
            'coherence': round(self.coherence(), 3),
            'reward': self.reward.stats(),
            'adapter': self.adapter.stats(),
            'state_codec': self.state_codec.stats(),
            'screen_codec': self.screen_codec.stats(),
        }


# ================================================================
#  CODEC REGISTRY EXTENSION
# ================================================================

# Register game codecs so SensorFusion can discover them
GAME_CODEC_REGISTRY = {
    'game_state': GameStateCodec,
    'screen_vision': ScreenVisionCodec,
}


# ================================================================
#  CLI: Test the game codecs
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK GAME SENSE -- Digital Environment → Operator")
    print("=" * 60)

    session = GameSession(team=0, seed=42)

    # Simulate 50 ticks of Rocket League
    rng = _random.Random(42)
    for tick in range(50):
        # Simulated telemetry
        telemetry = {
            'car_x': rng.gauss(0, 2000),
            'car_y': rng.gauss(0, 1000),
            'car_z': 17.01,  # On ground
            'car_vx': rng.gauss(500, 200),
            'car_vy': rng.gauss(0, 100),
            'car_vz': 0.0,
            'ball_x': rng.gauss(1000, 500),
            'ball_y': rng.gauss(0, 500),
            'ball_z': 93.15,  # Ball on ground
            'ball_vx': rng.gauss(0, 300),
            'ball_vy': rng.gauss(0, 200),
            'ball_vz': 0.0,
            'boost_amount': max(0, min(100, 50 + rng.gauss(0, 20))),
            'team': 0,
            'score_self': 0,
            'score_opponent': 0,
            'is_on_ground': True,
            'has_flip': True,
        }

        screen = {
            'field_motion': rng.uniform(0.1, 0.6),
            'field_brightness': rng.uniform(0.3, 0.8),
            'field_edges': rng.uniform(0.2, 0.7),
            'boost_meter': telemetry['boost_amount'] / 100.0,
            'score_delta': 0.0,
            'minimap_density': rng.uniform(0.1, 0.5),
        }

        session.feed_state(telemetry)
        session.feed_screen(screen)

        # Occasional events
        if tick == 25:
            session.on_event('ball_touch')
        if tick == 40:
            session.on_event('shot_on_goal')

    # Get action via reflex
    action = session.get_action()
    print(f"\n  Reflex action: {action.get('action', 'idle')}")

    # Get action via BTQ
    btq_action = session.get_action(use_btq=True, env_state=telemetry)
    print(f"  BTQ action: {btq_action.get('action', 'idle')}")

    # Stats
    stats = session.stats()
    print(f"\n  Fused operator: {stats['fused_operator']}")
    print(f"  Coherence: {stats['coherence']}")
    print(f"  State operator: {stats['state_operator']}")
    print(f"  Screen operator: {stats['screen_operator']}")
    print(f"  Reward events: {stats['reward']['total_events']}")
    print(f"  Ticks: {stats['tick']}")
