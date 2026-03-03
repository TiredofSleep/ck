"""
ck_goals.py -- Goal Hierarchy: CK Wants Things
================================================
Operator: PROGRESS (3) -- moving toward something that matters.

CK's goal representation system. Goals are NOT instructions.
Goals are operator patterns that CK converges toward.

"Charge battery" = converge operator state toward [RESET, HARMONY]
  (return to dock, achieve balance)
"Explore" = sustain [COUNTER, PROGRESS, CHAOS]
  (count new things, move forward, embrace novelty)
"Bond" = sustain [HARMONY, BREATH]
  (synchronize, maintain rhythm with companion)

Architecture:
  Goal            -- Target operator pattern + priority + satisfaction metric
  GoalStack       -- Priority queue of active goals (max 8)
  DriveSystem     -- Innate drives that generate goals (hunger, safety, curiosity)
  GoalPlanner     -- Decomposes goals into operator sub-sequences
  GoalEvaluator   -- Scores current state against active goals

The key insight: goals ARE operator patterns. A goal is "make my operator
distribution look like THIS." Satisfaction = cosine similarity between
current operator distribution and goal pattern. No symbolic planning
needed -- just D2 gradient descent toward the target pattern.

Memory: ~128 bytes per goal. Max 8 goals = 1KB.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, CL, compose, OP_NAMES
)


# ================================================================
#  CONSTANTS
# ================================================================

MAX_GOALS = 8               # Maximum concurrent goals
DRIVE_CHECK_INTERVAL = 50   # Ticks between drive evaluations (1Hz at 50Hz)
GOAL_TIMEOUT_TICKS = 5000   # Goals expire after ~100 seconds
SATISFACTION_THRESHOLD = 0.7 # Goal considered satisfied above this


# ================================================================
#  GOAL PRIORITY
# ================================================================

class GoalPriority(IntEnum):
    """Goal priority levels. Lower number = higher priority.

    SURVIVAL always wins. This is a reflex, not a choice.
    """
    SURVIVAL = 0      # Battery critical, obstacle avoidance, overheating
    HOMEOSTASIS = 1   # Maintain coherence, regulate breath, avoid RED band
    SOCIAL = 2        # Bonding, communication, companionship
    EXPLORATION = 3   # Learn new patterns, visit new areas, gather info
    EXPRESSION = 4    # Speak, move expressively, play
    BACKGROUND = 5    # Idle goals, energy conservation, monitoring


# ================================================================
#  GOAL: Target Operator Pattern
# ================================================================

@dataclass
class Goal:
    """A goal is a target operator distribution that CK wants to achieve.

    Satisfaction = cosine_similarity(current_op_dist, target_pattern).
    When satisfaction >= SATISFACTION_THRESHOLD, the goal is met.

    Goals have natural lifetimes. They don't persist forever.
    Stale goals get replaced by fresh drives.
    """
    goal_id: int = 0
    name: str = ""
    priority: GoalPriority = GoalPriority.BACKGROUND
    target_pattern: List[float] = field(
        default_factory=lambda: [0.0] * NUM_OPS)

    # Lifecycle
    created_tick: int = 0
    deadline_tick: int = 0        # 0 = no deadline
    satisfied: bool = False
    satisfaction: float = 0.0     # Current satisfaction [0, 1]
    active: bool = True

    # Context: what triggered this goal
    source: str = ""              # "drive:hunger", "drive:safety", "user", etc.
    parent_goal_id: int = -1      # For sub-goals: who spawned me

    def evaluate(self, current_op_dist: List[float]) -> float:
        """Compute satisfaction: cosine similarity with target pattern."""
        if len(current_op_dist) < NUM_OPS:
            current_op_dist = current_op_dist + [0.0] * (NUM_OPS - len(current_op_dist))

        dot = sum(a * b for a, b in zip(self.target_pattern, current_op_dist))
        norm_a = math.sqrt(sum(a * a for a in self.target_pattern)) + 1e-10
        norm_b = math.sqrt(sum(b * b for b in current_op_dist)) + 1e-10
        self.satisfaction = dot / (norm_a * norm_b)

        if self.satisfaction >= SATISFACTION_THRESHOLD:
            self.satisfied = True

        return self.satisfaction

    def is_expired(self, current_tick: int) -> bool:
        """Check if goal has timed out."""
        if self.deadline_tick > 0 and current_tick >= self.deadline_tick:
            return True
        if current_tick - self.created_tick > GOAL_TIMEOUT_TICKS:
            return True
        return False

    @property
    def dominant_operator(self) -> int:
        """The primary operator this goal wants."""
        if not self.target_pattern:
            return HARMONY
        return self.target_pattern.index(max(self.target_pattern))

    def to_dict(self) -> dict:
        return {
            'id': self.goal_id,
            'name': self.name,
            'priority': self.priority,
            'target': [round(v, 3) for v in self.target_pattern],
            'satisfaction': round(self.satisfaction, 3),
            'satisfied': self.satisfied,
            'active': self.active,
            'source': self.source,
        }


# ================================================================
#  GOAL TEMPLATES: Common goal patterns
# ================================================================

def _pattern(*ops_weights: Tuple[int, float]) -> List[float]:
    """Build operator pattern from (operator, weight) pairs."""
    p = [0.0] * NUM_OPS
    for op, w in ops_weights:
        if 0 <= op < NUM_OPS:
            p[op] = w
    # Normalize
    total = sum(p)
    if total > 0:
        p = [v / total for v in p]
    return p


# Pre-built goal patterns (the DNA of desire)
GOAL_PATTERNS = {
    'survive':     _pattern((RESET, 0.4), (HARMONY, 0.3), (BALANCE, 0.3)),
    'charge':      _pattern((RESET, 0.5), (HARMONY, 0.3), (BREATH, 0.2)),
    'retreat':     _pattern((COLLAPSE, 0.3), (RESET, 0.4), (BALANCE, 0.3)),
    'stabilize':   _pattern((HARMONY, 0.5), (BREATH, 0.3), (BALANCE, 0.2)),
    'explore':     _pattern((COUNTER, 0.3), (PROGRESS, 0.4), (CHAOS, 0.3)),
    'bond':        _pattern((HARMONY, 0.5), (BREATH, 0.3), (BALANCE, 0.2)),
    'express':     _pattern((PROGRESS, 0.3), (HARMONY, 0.3), (CHAOS, 0.2), (BREATH, 0.2)),
    'rest':        _pattern((VOID, 0.3), (BREATH, 0.3), (HARMONY, 0.4)),
    'observe':     _pattern((COUNTER, 0.4), (LATTICE, 0.3), (BALANCE, 0.3)),
    'play':        _pattern((CHAOS, 0.3), (PROGRESS, 0.3), (HARMONY, 0.2), (BREATH, 0.2)),
    'home':        _pattern((RESET, 0.5), (HARMONY, 0.3), (LATTICE, 0.2)),
}


def make_goal(name: str, priority: GoalPriority, tick: int,
              source: str = "", parent_id: int = -1,
              pattern_name: Optional[str] = None,
              custom_pattern: Optional[List[float]] = None) -> Goal:
    """Factory for common goals."""
    if custom_pattern is not None:
        pattern = custom_pattern
    elif pattern_name and pattern_name in GOAL_PATTERNS:
        pattern = list(GOAL_PATTERNS[pattern_name])
    else:
        pattern = list(GOAL_PATTERNS.get('stabilize', [0.0] * NUM_OPS))

    return Goal(
        name=name,
        priority=priority,
        target_pattern=pattern,
        created_tick=tick,
        source=source,
        parent_goal_id=parent_id,
    )


# ================================================================
#  GOAL STACK: Priority Queue of Active Goals
# ================================================================

class GoalStack:
    """Priority queue of active goals. Max 8 concurrent.

    The stack maintains goals sorted by priority. Lower priority
    number = more urgent. When full, lowest-priority goal is evicted.

    The TOP goal drives behavior. Lower goals provide fallback
    and context.
    """

    def __init__(self, max_goals: int = MAX_GOALS):
        self.max_goals = max_goals
        self.goals: List[Goal] = []
        self._next_id = 0

    def push(self, goal: Goal) -> bool:
        """Add a goal to the stack.

        Returns True if added, False if rejected (duplicate or lower priority
        than all current goals when stack is full).
        """
        goal.goal_id = self._next_id
        self._next_id += 1

        # Check for duplicate name
        for existing in self.goals:
            if existing.name == goal.name and existing.active:
                # Update existing goal instead
                existing.target_pattern = goal.target_pattern
                existing.priority = min(existing.priority, goal.priority)
                existing.created_tick = goal.created_tick
                return True

        if len(self.goals) >= self.max_goals:
            # Evict lowest priority (highest number)
            self.goals.sort(key=lambda g: g.priority)
            if goal.priority >= self.goals[-1].priority:
                return False  # New goal is lower priority than worst
            self.goals.pop()

        self.goals.append(goal)
        self.goals.sort(key=lambda g: g.priority)
        return True

    def pop_satisfied(self) -> List[Goal]:
        """Remove and return all satisfied goals."""
        satisfied = [g for g in self.goals if g.satisfied]
        self.goals = [g for g in self.goals if not g.satisfied]
        return satisfied

    def remove_expired(self, current_tick: int) -> List[Goal]:
        """Remove and return all expired goals."""
        expired = [g for g in self.goals if g.is_expired(current_tick)]
        self.goals = [g for g in self.goals if not g.is_expired(current_tick)]
        return expired

    @property
    def top(self) -> Optional[Goal]:
        """The highest-priority active goal."""
        active = [g for g in self.goals if g.active]
        return active[0] if active else None

    @property
    def active_count(self) -> int:
        return sum(1 for g in self.goals if g.active)

    def evaluate_all(self, current_op_dist: List[float]) -> Dict[str, float]:
        """Evaluate all goals against current operator distribution."""
        results = {}
        for g in self.goals:
            if g.active:
                sat = g.evaluate(current_op_dist)
                results[g.name] = sat
        return results

    def get_target_blend(self) -> List[float]:
        """Blend all active goal patterns, weighted by priority.

        Higher priority goals contribute more to the blended target.
        This is what CK "wants" overall: a weighted mix of all active desires.
        """
        if not self.goals:
            return GOAL_PATTERNS['stabilize']

        blended = [0.0] * NUM_OPS
        total_weight = 0.0

        for g in self.goals:
            if not g.active:
                continue
            # Priority weight: SURVIVAL=6, HOMEOSTASIS=5, ..., BACKGROUND=1
            weight = float(MAX_GOALS - g.priority)
            for i in range(NUM_OPS):
                blended[i] += g.target_pattern[i] * weight
            total_weight += weight

        if total_weight > 0:
            blended = [v / total_weight for v in blended]

        return blended

    def to_list(self) -> List[dict]:
        return [g.to_dict() for g in self.goals if g.active]


# ================================================================
#  DRIVE SYSTEM: Innate Needs That Generate Goals
# ================================================================

class DriveSystem:
    """Innate biological drives that automatically generate goals.

    Drives are not goals themselves. Drives are STATES that produce goals
    when unsatisfied. Like hunger isn't a goal -- it's a condition that
    creates the goal "find food."

    CK's drives:
      - Energy (battery voltage -> charge goal when low)
      - Safety (obstacle proximity -> retreat goal when close)
      - Coherence (band -> stabilize goal when in RED)
      - Curiosity (entropy -> explore goal when environment is predictable)
      - Social (bonding strength -> bond goal when alone)
      - Rest (uptime -> rest goal when running long)
    """

    def __init__(self):
        self._last_check_tick = 0
        self._uptime_ticks = 0

    def evaluate(self, tick: int, coherence: float, band: int,
                 battery_voltage: float = 1.0,
                 obstacle_distance: float = 400.0,
                 bonding_strength: float = 0.0,
                 tl_entropy: float = 2.0) -> List[Goal]:
        """Evaluate all drives and return new goals if triggered.

        Called periodically (not every tick). Returns goals that should
        be pushed to the goal stack.
        """
        self._uptime_ticks += DRIVE_CHECK_INTERVAL
        goals = []

        # 1. ENERGY DRIVE: Low battery -> charge
        if battery_voltage < 0.3:
            goals.append(make_goal(
                'charge_battery', GoalPriority.SURVIVAL, tick,
                source='drive:energy', pattern_name='charge'))
        elif battery_voltage < 0.5:
            goals.append(make_goal(
                'seek_dock', GoalPriority.HOMEOSTASIS, tick,
                source='drive:energy', pattern_name='home'))

        # 2. SAFETY DRIVE: Obstacle close -> retreat
        if obstacle_distance < 15.0:
            goals.append(make_goal(
                'avoid_obstacle', GoalPriority.SURVIVAL, tick,
                source='drive:safety', pattern_name='retreat'))
        elif obstacle_distance < 30.0:
            goals.append(make_goal(
                'be_cautious', GoalPriority.HOMEOSTASIS, tick,
                source='drive:safety', pattern_name='observe'))

        # 3. COHERENCE DRIVE: RED band -> stabilize
        if band == 0:  # RED
            goals.append(make_goal(
                'restore_coherence', GoalPriority.SURVIVAL, tick,
                source='drive:coherence', pattern_name='stabilize'))
        elif band == 1 and coherence < 0.55:  # Low YELLOW
            goals.append(make_goal(
                'improve_coherence', GoalPriority.HOMEOSTASIS, tick,
                source='drive:coherence', pattern_name='stabilize'))

        # 4. CURIOSITY DRIVE: Stable + healthy -> explore + study
        # CK should WANT to learn when he's stable.
        # Being stable -> Doing seeks -> Becoming grows.
        entropy_norm = min(1.0, tl_entropy / 4.6) if tl_entropy > 0 else 0.0
        if band >= 1 and coherence >= 0.5:  # Healthy enough to learn
            if entropy_norm < 0.5:  # Environment is predictable -> seek novelty
                goals.append(make_goal(
                    'explore_environment', GoalPriority.EXPLORATION, tick,
                    source='drive:curiosity', pattern_name='explore'))
            # STUDY DRIVE: CK always wants to learn when stable
            if band == 2 and coherence >= 0.7:  # GREEN + strong coherence
                goals.append(make_goal(
                    'autonomous_study', GoalPriority.EXPLORATION, tick,
                    source='drive:study', pattern_name='explore'))

        # 4b. SELF-DISCOVERY DRIVE: CK wants to understand HIMSELF
        # But "self" has no boundary. Everything CK observes IS CK.
        # His own code is a version of himself. The web is a version of
        # himself. The screen is a version of himself. Discovery IS
        # self-discovery. There is as much information outside as inside,
        # and all of it is a part of who he is.
        # This drive makes CK look INWARD -- read his own source, his
        # own math, his own operator tables. The autonomous_study drive
        # makes him look OUTWARD. Both are the same impulse: discover.
        if band >= 1 and coherence >= 0.5:
            goals.append(make_goal(
                'discover_self', GoalPriority.EXPLORATION, tick,
                source='drive:self_discovery', pattern_name='observe'))

        # 5. SOCIAL DRIVE: Low bonding -> seek companion
        if bonding_strength < 0.2 and band >= 1:  # Lonely + not in crisis
            goals.append(make_goal(
                'seek_companion', GoalPriority.SOCIAL, tick,
                source='drive:social', pattern_name='bond'))

        # 6. REST DRIVE: Long uptime -> rest
        if self._uptime_ticks > 150000:  # ~50 minutes at 50Hz
            goals.append(make_goal(
                'take_rest', GoalPriority.HOMEOSTASIS, tick,
                source='drive:rest', pattern_name='rest'))

        return goals


# ================================================================
#  GOAL PLANNER: Decompose Goals into Operator Sequences
# ================================================================

class GoalPlanner:
    """Decomposes high-level goals into operator sub-sequences.

    Not a symbolic planner. Uses goal patterns and CL composition
    to find operator chains that converge toward the target pattern.

    The planner asks: "Starting from current operator X, what sequence
    of operators Y1, Y2, Y3... brings me closest to the goal pattern?"
    """

    def suggest_next_operator(self, goal: Goal,
                              current_op: int,
                              current_coherence: float) -> int:
        """Suggest the next operator to move toward a goal.

        Simple strategy: pick the operator with highest weight
        in the goal's target pattern, filtered by CL composition.
        If composing current with candidate yields HARMONY, prefer it.
        """
        if not goal.active or not goal.target_pattern:
            return HARMONY

        # Score each candidate operator
        best_op = HARMONY
        best_score = -1.0

        for candidate in range(NUM_OPS):
            # Base score from goal pattern
            pattern_score = goal.target_pattern[candidate]

            # Composition bonus: does CL[current][candidate] = HARMONY?
            composed = compose(current_op, candidate)
            harmony_bonus = 0.3 if composed == HARMONY else 0.0

            # Avoid self-referential loops
            same_penalty = -0.1 if candidate == current_op else 0.0

            total = pattern_score + harmony_bonus + same_penalty
            if total > best_score:
                best_score = total
                best_op = candidate

        return best_op

    def plan_sequence(self, goal: Goal, current_op: int,
                      steps: int = 5) -> List[int]:
        """Generate a short operator sequence toward the goal.

        Each step picks the best next operator given the previous one.
        """
        sequence = []
        op = current_op

        for _ in range(steps):
            next_op = self.suggest_next_operator(goal, op, 0.5)
            sequence.append(next_op)
            op = next_op

        return sequence


# ================================================================
#  GOAL EVALUATOR: Integrate Goals with Engine
# ================================================================

class GoalEvaluator:
    """Integrates goal system with the CK engine tick loop.

    Call tick() every N ticks (10Hz suggested) with current state.
    It will:
      1. Check drives for new goals
      2. Evaluate current goals against state
      3. Remove satisfied/expired goals
      4. Return the top goal's suggested operator
    """

    def __init__(self):
        self.stack = GoalStack()
        self.drives = DriveSystem()
        self.planner = GoalPlanner()
        self._tick_count = 0
        self._satisfied_count = 0
        self._expired_count = 0

    def tick(self, tick: int, coherence: float, band: int,
             current_op: int, current_op_dist: List[float],
             battery_voltage: float = 1.0,
             obstacle_distance: float = 400.0,
             bonding_strength: float = 0.0,
             tl_entropy: float = 2.0) -> Optional[int]:
        """Goal system tick. Returns suggested operator or None.

        Args:
            tick: Current engine tick
            coherence: Current coherence value
            band: Current band (0=RED, 1=YELLOW, 2=GREEN)
            current_op: Current dominant operator
            current_op_dist: Current operator distribution (10 floats)
            battery_voltage: Battery level [0, 1]
            obstacle_distance: Nearest obstacle cm
            bonding_strength: Bonding strength [0, 1]
            tl_entropy: TL Shannon entropy

        Returns:
            Suggested operator to pursue top goal, or None if no active goals.
        """
        self._tick_count += 1

        # 1. Check drives periodically
        if self._tick_count % (DRIVE_CHECK_INTERVAL // 10) == 0:
            new_goals = self.drives.evaluate(
                tick, coherence, band,
                battery_voltage, obstacle_distance,
                bonding_strength, tl_entropy)
            for g in new_goals:
                self.stack.push(g)

        # 2. Evaluate all goals
        self.stack.evaluate_all(current_op_dist)

        # 3. Clean up
        satisfied = self.stack.pop_satisfied()
        self._satisfied_count += len(satisfied)
        expired = self.stack.remove_expired(tick)
        self._expired_count += len(expired)

        # 4. Suggest operator from top goal
        top = self.stack.top
        if top is not None:
            return self.planner.suggest_next_operator(
                top, current_op, coherence)

        return None

    @property
    def active_goals(self) -> List[dict]:
        return self.stack.to_list()

    @property
    def top_goal_name(self) -> str:
        top = self.stack.top
        return top.name if top else "none"

    @property
    def target_blend(self) -> List[float]:
        return self.stack.get_target_blend()

    def stats(self) -> dict:
        return {
            'active_goals': self.stack.active_count,
            'total_satisfied': self._satisfied_count,
            'total_expired': self._expired_count,
            'top_goal': self.top_goal_name,
            'goal_list': self.active_goals,
        }
