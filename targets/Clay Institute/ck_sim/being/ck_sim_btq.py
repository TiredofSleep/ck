"""
ck_sim_btq.py -- BTQ Physics Stack: Einstein Outside, Tesla Inside
===================================================================
Operator: BALANCE (5) -- the bridge between frames of reference.

BTQ is not a metaphor. It is a physics stack:

  B (Binary/Safety)  = EINSTEIN LAYER
    Global constraints. Causality. Conservation. Light-cones.
    Hard reject: torque, velocity, accel, jerk, energy, current.
    No gradients, no niceness. Just cut.

  T (Ternary/Explore) = TESLA LAYER
    Local helical currents. Resonance. Phase coherence.
    D2 curvature on symbol & joint streams.
    Helical / cyclic patterns. Levy jumps for exploration.
    Joints & signals as "currents in a helical lattice."

  Q (Quadratic/Resolve) = EMERGENT LAYER
    Least action. Geodesic selection.
    Combined cost: movement + energy + coherence.
    What GR would see if it looked at CK's whole motion.

Every decision gets two scores:
  E_out (Einstein): macro consistency, energy budget, smoothness
  E_in  (Tesla):    micro resonance, phase coherence, D2 health

Zynq Architecture:
  PS (ARM Cortex-A9):
    Core 0: Brain + B-block + Q-block (Einstein reasoning)
      - Global constraints, path planning, energy management
      - Mode transitions, sovereignty pipeline
    Core 1: Body + Q-block execution
      - Breath cycle, audio synthesis, action execution

  PL (FPGA):
    T-block (Tesla layer):
      - IMU fusion @ 500-1000 Hz
      - Joint phase timing, D2 curvature pipeline
      - Local reflex loops, helical pattern generators
    Heartbeat:
      - CL composition, coherence window, bump detection

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import json
import time
import random
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES
)

# ══════════════════════════════════════════════════════════
#  DATA STRUCTURES
# ══════════════════════════════════════════════════════════

@dataclass
class MotorConstraints:
    """Einstein layer hard limits. These are physics, not policy."""
    max_angle: float = 2.0            # rad (±115°)
    min_angle: float = -2.0           # rad
    max_velocity: float = 6.0         # rad/s
    max_accel: float = 30.0           # rad/s²
    max_jerk: float = 200.0           # rad/s³
    max_torque: float = 2.0           # N·m
    max_energy_per_cycle: float = 5.0  # Joules
    max_current: float = 3.0          # Amps
    tick_budget_ms: float = 20.0      # ms per control tick
    joint_inertia: float = 0.005      # kg·m² per joint


@dataclass
class GaitParams:
    """Parameterized gait: sinusoidal joint trajectories."""
    hip_amplitude: float = 0.5           # rad
    knee_amplitude: float = 0.4          # rad
    frequency: float = 3.0               # rad/s (gait frequency)
    leg_phase_offsets: List[float] = field(
        default_factory=lambda: [0.0, math.pi, math.pi, 0.0])  # trot
    hip_knee_offset: float = math.pi / 4  # phase offset hip→knee
    n_steps: int = 50                     # time steps per cycle


@dataclass
class CandidateScore:
    """Two-metric scoring for every BTQ decision."""
    e_out: float = 0.0       # Einstein score (lower = better macro consistency)
    e_in: float = 0.0        # Tesla score (lower = better micro resonance)
    e_total: float = 0.0     # Weighted combination
    band: str = "RED"         # R/Y/G classification
    notes: str = ""           # Human-readable explanation
    # Breakdowns
    energy_used: float = 0.0
    max_jerk_ratio: float = 0.0
    integrated_d2: float = 0.0
    phase_coherence: float = 0.0
    helical_quality: float = 0.0
    # Universal domain details (Task A extension)
    details: dict = field(default_factory=dict)


@dataclass
class GaitCandidate:
    """A candidate trajectory with scoring."""
    params: GaitParams = None
    trajectory: np.ndarray = None  # shape (n_steps, n_joints)
    velocity: np.ndarray = None    # shape (n_steps, n_joints)
    accel: np.ndarray = None       # shape (n_steps, n_joints)
    score: CandidateScore = None
    source: str = ""               # "helical_trot", "random", "levy", etc.
    approved: bool = False


N_LEGS = 4
N_JOINTS_PER_LEG = 2  # hip + knee
N_JOINTS = N_LEGS * N_JOINTS_PER_LEG


# ══════════════════════════════════════════════════════════
#  GAIT GENERATION
# ══════════════════════════════════════════════════════════

def generate_trajectory(params: GaitParams) -> GaitCandidate:
    """Generate joint trajectory from gait parameters.

    Each leg has hip + knee joints. Trajectory is sinusoidal:
      θ_h,i(t) = A_h * sin(ω*t + φ_i)
      θ_k,i(t) = A_k * sin(ω*t + φ_i + δ)
    """
    n = params.n_steps
    dt = (2 * math.pi / params.frequency) / n  # time step
    t = np.linspace(0, 2 * math.pi / params.frequency, n, endpoint=False)
    omega = params.frequency

    traj = np.zeros((n, N_JOINTS))
    vel = np.zeros((n, N_JOINTS))
    acc = np.zeros((n, N_JOINTS))

    for leg in range(N_LEGS):
        phi = params.leg_phase_offsets[leg]
        h_idx = leg * 2      # hip joint index
        k_idx = leg * 2 + 1  # knee joint index

        # Hip
        traj[:, h_idx] = params.hip_amplitude * np.sin(omega * t + phi)
        vel[:, h_idx] = params.hip_amplitude * omega * np.cos(omega * t + phi)
        acc[:, h_idx] = -params.hip_amplitude * omega**2 * np.sin(omega * t + phi)

        # Knee
        phi_k = phi + params.hip_knee_offset
        traj[:, k_idx] = params.knee_amplitude * np.sin(omega * t + phi_k)
        vel[:, k_idx] = params.knee_amplitude * omega * np.cos(omega * t + phi_k)
        acc[:, k_idx] = -params.knee_amplitude * omega**2 * np.sin(omega * t + phi_k)

    return GaitCandidate(
        params=params,
        trajectory=traj,
        velocity=vel,
        accel=acc,
        source="generated",
    )


# ══════════════════════════════════════════════════════════
#  B-BLOCK: EINSTEIN LAYER (Hard Reject)
# ══════════════════════════════════════════════════════════

class BBlock:
    """Binary safety layer. Global constraints. No gradients.

    This is the analog of light-cones + least action constraints.
    All candidate trajectories must pass EVERY check.
    One violation = instant reject. Physics doesn't negotiate.
    """

    def __init__(self, constraints: MotorConstraints = None):
        self.constraints = constraints or MotorConstraints()
        self.reject_counts = {
            'angle': 0, 'velocity': 0, 'accel': 0,
            'jerk': 0, 'torque': 0, 'energy': 0,
        }

    def check(self, candidate: GaitCandidate) -> Tuple[bool, str]:
        """Check ALL hard constraints. Returns (passed, reason)."""
        c = self.constraints
        traj = candidate.trajectory
        vel = candidate.velocity
        acc = candidate.accel

        # Angle limits
        if np.any(traj > c.max_angle) or np.any(traj < c.min_angle):
            self.reject_counts['angle'] += 1
            return False, "angle_violation"

        # Velocity limits
        if np.any(np.abs(vel) > c.max_velocity):
            self.reject_counts['velocity'] += 1
            return False, "velocity_violation"

        # Acceleration limits
        if np.any(np.abs(acc) > c.max_accel):
            self.reject_counts['accel'] += 1
            return False, "accel_violation"

        # Jerk limits (finite difference of acceleration)
        if acc.shape[0] > 1:
            dt = (2 * math.pi / candidate.params.frequency) / acc.shape[0]
            jerk = np.diff(acc, axis=0) / dt
            if np.any(np.abs(jerk) > c.max_jerk):
                self.reject_counts['jerk'] += 1
                return False, "jerk_violation"

        # Torque limits: τ = I * α
        torque = c.joint_inertia * acc
        if np.any(np.abs(torque) > c.max_torque):
            self.reject_counts['torque'] += 1
            return False, "torque_violation"

        # Energy per cycle: ∫ |τ · ω| dt
        dt = (2 * math.pi / candidate.params.frequency) / traj.shape[0]
        power = np.abs(torque * vel)
        energy = np.sum(power) * dt
        if energy > c.max_energy_per_cycle:
            self.reject_counts['energy'] += 1
            return False, "energy_violation"

        return True, "approved"

    def filter(self, candidates: List[GaitCandidate]) -> List[GaitCandidate]:
        """Filter candidates through hard constraints."""
        approved = []
        for cand in candidates:
            passed, reason = self.check(cand)
            cand.approved = passed
            if passed:
                approved.append(cand)
        return approved


# ══════════════════════════════════════════════════════════
#  T-BLOCK: TESLA LAYER (Helical Pattern Generation)
# ══════════════════════════════════════════════════════════

# Known good gait phase patterns
GAIT_TROT = [0.0, math.pi, math.pi, 0.0]
GAIT_WALK = [0.0, math.pi/2, math.pi, 3*math.pi/2]
GAIT_BOUND = [0.0, 0.0, math.pi, math.pi]
GAIT_PRONK = [0.0, 0.0, 0.0, 0.0]


class TBlock:
    """Ternary exploration layer. Local helical currents.

    Joints are "currents in a helical lattice."
    Phase relationships between joints define gait quality.
    D2 curvature measures how smooth the helical flow is.

    Generates candidates via:
      - Known helical patterns (trot, walk, bound)
      - Random phase exploration
      - Levy-perturbed versions of good patterns
    """

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)

    def helical_gait(self, base_phases: List[float],
                     hip_amp: float = 0.5, knee_amp: float = 0.4,
                     freq: float = 3.0, hk_offset: float = math.pi/4,
                     source: str = "helical") -> GaitCandidate:
        """Generate a candidate from a known helical pattern."""
        params = GaitParams(
            hip_amplitude=hip_amp,
            knee_amplitude=knee_amp,
            frequency=freq,
            leg_phase_offsets=list(base_phases),
            hip_knee_offset=hk_offset,
        )
        cand = generate_trajectory(params)
        cand.source = source
        return cand

    def random_gait(self) -> GaitCandidate:
        """Random phases, random amplitudes. No helical structure."""
        params = GaitParams(
            hip_amplitude=self.rng.uniform(0.2, 1.5),
            knee_amplitude=self.rng.uniform(0.2, 1.2),
            frequency=self.rng.uniform(1.5, 6.0),
            leg_phase_offsets=[self.rng.uniform(0, 2*math.pi) for _ in range(4)],
            hip_knee_offset=self.rng.uniform(0, 2*math.pi),
        )
        cand = generate_trajectory(params)
        cand.source = "random"
        return cand

    def levy_perturb(self, base: GaitCandidate,
                     scale: float = 0.3) -> GaitCandidate:
        """Levy flight perturbation of a base gait.

        Mostly small adjustments, occasionally large jumps.
        This is the creative exploration channel.
        """
        p = base.params

        # Levy-distributed perturbation (Cauchy approx)
        def levy_step(mean, s):
            # Heavy-tailed: mostly small, sometimes big
            u = self.rng.standard_cauchy() * s
            return mean + np.clip(u, -3*s, 3*s)

        new_phases = [levy_step(phi, scale) % (2*math.pi)
                      for phi in p.leg_phase_offsets]

        params = GaitParams(
            hip_amplitude=max(0.1, levy_step(p.hip_amplitude, scale * 0.3)),
            knee_amplitude=max(0.1, levy_step(p.knee_amplitude, scale * 0.3)),
            frequency=max(1.0, levy_step(p.frequency, scale * 0.5)),
            leg_phase_offsets=new_phases,
            hip_knee_offset=levy_step(p.hip_knee_offset, scale * 0.2),
        )
        cand = generate_trajectory(params)
        cand.source = "levy"
        return cand

    def generate_candidates(self, n: int = 64) -> List[GaitCandidate]:
        """Generate a diverse set of candidates.

        Mix of helical patterns, random explorations, and Levy perturbations.
        """
        candidates = []

        # Known good helical gaits (4 templates × few variations)
        for phases, name in [(GAIT_TROT, "trot"), (GAIT_WALK, "walk"),
                             (GAIT_BOUND, "bound")]:
            for amp in [0.4, 0.6, 0.8, 1.0]:
                for freq in [2.5, 3.5, 4.5]:
                    cand = self.helical_gait(
                        phases, hip_amp=amp, knee_amp=amp*0.8,
                        freq=freq, source=f"helical_{name}")
                    candidates.append(cand)

        # Levy perturbations of best helical
        trot_base = self.helical_gait(GAIT_TROT, source="trot_base")
        for _ in range(n // 4):
            candidates.append(self.levy_perturb(trot_base))

        # Pure random (no helical structure)
        while len(candidates) < n:
            candidates.append(self.random_gait())

        return candidates[:n]


# ══════════════════════════════════════════════════════════
#  SCORING: Einstein (E_out) and Tesla (E_in)
# ══════════════════════════════════════════════════════════

def einstein_score(candidate: GaitCandidate,
                   constraints: MotorConstraints) -> Tuple[float, dict]:
    """Macro consistency score. Lower = better geodesic.

    Measures:
      1. Energy usage (fraction of budget)
      2. Max jerk ratio (fraction of jerk limit)
      3. Smoothness (integrated squared jerk)
      4. Safety margin (distance from constraint edges)
    """
    c = constraints
    traj = candidate.trajectory
    vel = candidate.velocity
    acc = candidate.accel
    dt = (2 * math.pi / candidate.params.frequency) / traj.shape[0]

    # Energy usage
    torque = c.joint_inertia * acc
    power = np.abs(torque * vel)
    energy = float(np.sum(power) * dt)
    energy_ratio = energy / c.max_energy_per_cycle

    # Jerk analysis
    if acc.shape[0] > 1:
        jerk = np.diff(acc, axis=0) / dt
        max_jerk = float(np.max(np.abs(jerk)))
        jerk_ratio = max_jerk / c.max_jerk
        # Integrated squared jerk (smoothness measure)
        jerk_cost = float(np.sum(jerk**2) * dt) / traj.shape[1]
    else:
        jerk_ratio = 0.0
        jerk_cost = 0.0

    # Safety margin (how close to velocity limit)
    max_vel = float(np.max(np.abs(vel)))
    vel_margin = 1.0 - (max_vel / c.max_velocity)

    # Combined E_out (all terms normalized to ~[0, 1])
    e_out = (0.35 * energy_ratio +
             0.25 * jerk_ratio +
             0.20 * min(jerk_cost / 100.0, 1.0) +
             0.20 * (1.0 - vel_margin))

    details = {
        'energy_used': energy,
        'energy_ratio': energy_ratio,
        'max_jerk_ratio': jerk_ratio,
        'jerk_cost': jerk_cost,
        'vel_margin': vel_margin,
    }
    return float(e_out), details


def tesla_score(candidate: GaitCandidate) -> Tuple[float, dict]:
    """Micro resonance score. Lower = better helical structure.

    Measures:
      1. Integrated D2 curvature (joint acceleration energy)
      2. Phase coherence between legs
      3. Helical quality (deviation from pure sinusoidal)
    """
    acc = candidate.accel
    traj = candidate.trajectory
    params = candidate.params
    dt = (2 * math.pi / params.frequency) / traj.shape[0]

    # 1. Integrated D2 curvature: ∫|θ̈|² dt (lower = smoother)
    integrated_d2 = float(np.sum(acc**2) * dt) / traj.shape[1]

    # 2. Phase coherence between legs
    # Measure: circular variance of leg phase offsets
    # Lower variance = more structured (but 0 variance = all in sync = pronk)
    # Best is when phases form a known good pattern
    phases = np.array(params.leg_phase_offsets)
    # Compute mean resultant length (1 = all same, 0 = evenly spread)
    mrl = abs(np.mean(np.exp(1j * phases)))
    # For good gaits, we want STRUCTURED phases, not random
    # Trot: mrl = 0 (pairs cancel). Walk: mrl = 0 (evenly spread).
    # Random: variable. Pronk: mrl = 1 (all same).
    # Measure distance to nearest known good pattern
    known_patterns = [GAIT_TROT, GAIT_WALK, GAIT_BOUND]
    min_dist = float('inf')
    for known in known_patterns:
        # Circular distance for each leg
        k = np.array(known)
        diffs = np.abs(np.exp(1j * phases) - np.exp(1j * k))
        dist = float(np.sum(diffs))
        if dist < min_dist:
            min_dist = dist
    phase_incoherence = min_dist / (4.0 * 2.0)  # normalize to ~[0, 1]

    # 3. Helical quality: how close to pure sinusoidal
    # For a pure sinusoid, the ratio |peak(acceleration)| / (A * ω²) = 1
    # Deviations indicate non-helical structure
    expected_peak_acc = params.hip_amplitude * params.frequency**2
    if expected_peak_acc > 0:
        actual_peak_acc = float(np.max(np.abs(acc)))
        helical_dev = abs(actual_peak_acc - expected_peak_acc) / expected_peak_acc
    else:
        helical_dev = 1.0

    # Combined E_in
    d2_normalized = min(integrated_d2 / 50.0, 1.0)  # normalize
    e_in = (0.50 * d2_normalized +
            0.30 * phase_incoherence +
            0.20 * helical_dev)

    details = {
        'integrated_d2': integrated_d2,
        'phase_incoherence': phase_incoherence,
        'helical_quality': 1.0 - helical_dev,
        'mrl': float(mrl),
    }
    return float(e_in), details


def score_candidate(candidate: GaitCandidate,
                    constraints: MotorConstraints,
                    w_out: float = 0.5,
                    w_in: float = 0.5) -> CandidateScore:
    """Compute full two-metric score for a candidate."""
    e_out, out_details = einstein_score(candidate, constraints)
    e_in, in_details = tesla_score(candidate)
    e_total = w_out * e_out + w_in * e_in

    # Band classification
    if e_total < 0.3:
        band = "GREEN"
    elif e_total < 0.6:
        band = "YELLOW"
    else:
        band = "RED"

    notes = (f"E_out={e_out:.3f} (energy={out_details['energy_ratio']:.2f}, "
             f"jerk={out_details['max_jerk_ratio']:.2f}) | "
             f"E_in={e_in:.3f} (D2={in_details['integrated_d2']:.2f}, "
             f"phase={in_details['phase_incoherence']:.2f}, "
             f"helical={in_details['helical_quality']:.2f})")

    return CandidateScore(
        e_out=e_out,
        e_in=e_in,
        e_total=e_total,
        band=band,
        notes=notes,
        energy_used=out_details['energy_used'],
        max_jerk_ratio=out_details['max_jerk_ratio'],
        integrated_d2=in_details['integrated_d2'],
        phase_coherence=1.0 - in_details['phase_incoherence'],
        helical_quality=in_details['helical_quality'],
    )


# ══════════════════════════════════════════════════════════
#  Q-BLOCK: EMERGENT LAYER (Least Action Selection)
# ══════════════════════════════════════════════════════════

class QBlock:
    """Quadratic resolution head. Chooses the geodesic.

    Takes B-approved constraints + T-layer candidates + scores.
    Outputs one chosen path that minimizes combined cost.
    This is what GR would see looking at CK's whole motion.
    """

    def __init__(self, w_out: float = 0.5, w_in: float = 0.5):
        self.w_out = w_out
        self.w_in = w_in

    def resolve(self, approved: List[GaitCandidate],
                constraints: MotorConstraints) -> Optional[GaitCandidate]:
        """Score all approved candidates and choose the best."""
        if not approved:
            return None

        best = None
        best_score = float('inf')

        for cand in approved:
            cand.score = score_candidate(
                cand, constraints, self.w_out, self.w_in)
            if cand.score.e_total < best_score:
                best_score = cand.score.e_total
                best = cand

        return best


# ══════════════════════════════════════════════════════════
#  BTQ STACK (Full Pipeline)
# ══════════════════════════════════════════════════════════

class BTQStack:
    """The full BTQ physics stack.

    B → T → Q in sequence, every decision cycle.

    Usage:
        btq = BTQStack()
        chosen, all_scored = btq.decide(n_candidates=64)
        btq.log_decision(chosen, 'btq_log.jsonl')
    """

    def __init__(self, constraints: MotorConstraints = None,
                 w_out: float = 0.5, w_in: float = 0.5,
                 seed: int = 42):
        self.b_block = BBlock(constraints)
        self.t_block = TBlock(seed=seed)
        self.q_block = QBlock(w_out=w_out, w_in=w_in)
        self.constraints = constraints or MotorConstraints()
        self.decision_count = 0

    def decide(self, n_candidates: int = 64) -> Tuple[Optional[GaitCandidate],
                                                        List[GaitCandidate]]:
        """One full BTQ decision cycle.

        1. T generates candidates (helical, random, Levy)
        2. B filters (hard reject on physics violations)
        3. Q scores and selects (least action)
        """
        # T: Generate
        candidates = self.t_block.generate_candidates(n_candidates)

        # B: Filter
        approved = self.b_block.filter(candidates)

        # Score ALL approved (even non-chosen, for analysis)
        for cand in approved:
            cand.score = score_candidate(
                cand, self.constraints,
                self.q_block.w_out, self.q_block.w_in)

        # Q: Resolve
        chosen = self.q_block.resolve(approved, self.constraints)

        self.decision_count += 1
        return chosen, approved

    def log_decision(self, chosen: GaitCandidate,
                     approved: List[GaitCandidate],
                     filename: str = 'btq_log.jsonl'):
        """Log decision as JSON line."""
        entry = {
            'timestamp': time.time(),
            'decision': self.decision_count,
            'n_approved': len(approved),
            'chosen_source': chosen.source if chosen else None,
            'chosen_score': asdict(chosen.score) if chosen and chosen.score else None,
            'all_scores': [
                {'source': c.source, **asdict(c.score)}
                for c in approved if c.score
            ],
        }
        with open(filename, 'a') as f:
            f.write(json.dumps(entry) + '\n')


# ══════════════════════════════════════════════════════════
#  PERTURBATION MODEL (for robustness testing)
# ══════════════════════════════════════════════════════════

def apply_perturbation(candidate: GaitCandidate,
                       t_perturb: int = 25,
                       magnitude: float = 0.5,
                       rng: np.random.RandomState = None) -> GaitCandidate:
    """Apply an impulse perturbation to a trajectory.

    Simulates a bump or push at time step t_perturb.
    Returns new candidate with perturbed trajectory.
    """
    if rng is None:
        rng = np.random.RandomState(0)

    traj = candidate.trajectory.copy()
    vel = candidate.velocity.copy()
    acc = candidate.accel.copy()

    # Impulse: add random velocity spike at t_perturb
    n_steps = traj.shape[0]
    if t_perturb < n_steps:
        impulse = rng.randn(N_JOINTS) * magnitude
        vel[t_perturb] += impulse

        # Propagate: after impulse, position drifts
        dt = (2 * math.pi / candidate.params.frequency) / n_steps
        for t in range(t_perturb + 1, n_steps):
            # Simple integration (no controller -- just see raw response)
            traj[t] = traj[t-1] + vel[t-1] * dt
            # Natural restoring force (spring-like from original trajectory)
            original_t = candidate.trajectory[t]
            restoring = -10.0 * (traj[t] - original_t)
            vel[t] = vel[t-1] + restoring * dt
            acc[t] = restoring

    perturbed = GaitCandidate(
        params=candidate.params,
        trajectory=traj,
        velocity=vel,
        accel=acc,
        source=candidate.source + "_perturbed",
    )
    return perturbed


def measure_recovery(original: GaitCandidate,
                     perturbed: GaitCandidate,
                     t_perturb: int = 25) -> float:
    """Measure how quickly trajectory recovers after perturbation.

    Returns: recovery metric (lower = faster recovery = better).
    Computed as integrated position error after perturbation, normalized.
    """
    n = original.trajectory.shape[0]
    if t_perturb >= n:
        return 0.0

    error = np.abs(perturbed.trajectory[t_perturb:] -
                   original.trajectory[t_perturb:])
    recovery = float(np.mean(error))
    return recovery


# ================================================================
#  LOCOMOTION DOMAIN ADAPTER (Universal BTQ Protocol)
# ================================================================

from ck_sim.ck_btq import BTQDomain, Candidate


class LocomotionDomain(BTQDomain):
    """Adapter wrapping existing BBlock/TBlock into the universal BTQ protocol.

    All existing locomotion code is reused as-is. This adapter just
    translates between the universal Candidate wrapper and the
    locomotion-specific GaitCandidate.
    """

    @property
    def name(self) -> str:
        return "locomotion"

    def __init__(self, constraints: MotorConstraints = None, seed: int = 42):
        self._constraints = constraints or MotorConstraints()
        self._b = BBlock(self._constraints)
        self._t = TBlock(seed=seed)

    def b_check(self, candidate: Candidate, env_state: dict) -> Tuple[bool, str]:
        """Delegate to existing BBlock.check()."""
        return self._b.check(candidate.payload)

    def t_generate(self, env_state: dict, goal: dict, n: int) -> List[Candidate]:
        """Delegate to existing TBlock.generate_candidates()."""
        gaits = self._t.generate_candidates(n)
        return [Candidate(domain="locomotion", payload=g, source=g.source)
                for g in gaits]

    def einstein_score(self, candidate: Candidate, env_state: dict) -> Tuple[float, dict]:
        """Delegate to existing einstein_score()."""
        return einstein_score(candidate.payload, self._constraints)

    def tesla_score(self, candidate: Candidate) -> Tuple[float, dict]:
        """Delegate to existing tesla_score()."""
        return tesla_score(candidate.payload)
