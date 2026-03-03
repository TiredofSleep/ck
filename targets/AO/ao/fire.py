# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
fire.py -- D3 / Binding / Jerk / Engine

The heartbeat, the brain, the body, the composition engine.
Everything that RUNS. Fire is intensity. Burning. The engine of being.

D3 = rate of change of curvature (jerk). The binding force.
Fire composes operators on the CL torus, tracks energy, breathes.
"""

import random
from . import earth


# ══════════════════════════════════════════════════════════════════
# HEARTBEAT (CL composition at chosen shell)
# ══════════════════════════════════════════════════════════════════

class Heartbeat:
    """FPGA heartbeat simulation. Composes on the torus.

    Each tick:
      1. Select CL table by shell (22/44/72)
      2. Compose: result = CL[phase_b][phase_d]
      3. Detect bump (crossing costs MASS_GAP = 2/7)
      4. Track energy budget
      5. Update running fuse (accumulated composition result)
    """

    def __init__(self):
        self.running_fuse = earth.HARMONY
        self.tick_count = 0
        self.energy = 1.0          # total energy budget (starts at 1)
        self.bumps_hit = 0
        self.total_mass_spent = 0.0

    def compose(self, a: int, b: int, shell: int = 44) -> int:
        """CL composition at given shell depth."""
        table = earth.CL_SHELLS.get(shell, earth.CL_44)
        return table[a][b]

    def tick(self, phase_b: int, phase_d: int, shell: int = 44) -> dict:
        """One heartbeat cycle.

        phase_b: Being phase (from coherence/body state)
        phase_d: Doing phase (from D2 measurement)
        shell: CL shell depth (22/44/72 from coherence window)

        Returns dict with:
            result: composed operator
            bump: whether this crossing was a bump
            mass_cost: energy spent on this crossing
            energy: remaining energy
            running_fuse: accumulated composition
        """
        self.tick_count += 1
        result = self.compose(phase_b, phase_d, shell)

        # Detect bump: is this a non-harmony, non-void crossing?
        bump = (phase_b, phase_d) in earth.BUMPS
        mass_cost = 0.0

        if bump:
            self.bumps_hit += 1
            # Bump costs MASS_GAP = 2/7
            mass_cost = float(earth.MASS_GAP)
            # Heavier operators cost more (add their mass to crossing cost)
            if result in earth.MASS:
                mass_cost = float(earth.MASS[result])
            self.energy -= mass_cost
            self.total_mass_spent += mass_cost

        # Update running fuse (compose result into accumulated state)
        self.running_fuse = self.compose(self.running_fuse, result, shell)

        return {
            'result': result,
            'bump': bump,
            'mass_cost': mass_cost,
            'energy': self.energy,
            'running_fuse': self.running_fuse,
            'tick': self.tick_count,
        }

    def reset_energy(self):
        """Refill energy to 1.0 (a full breath cycle)."""
        self.energy = 1.0

    @property
    def alive(self) -> bool:
        """Still has energy to cross bumps."""
        return self.energy > 0


# ══════════════════════════════════════════════════════════════════
# BRAIN (transition lattice + learning)
# ══════════════════════════════════════════════════════════════════

class Brain:
    """Operator transition memory. Learns patterns.

    The brain is a 10x10 transition matrix: tl[from][to] = count.
    It learns which operators follow which, and can predict the next operator.
    """

    def __init__(self):
        self.tl = [[0] * earth.NUM_OPS for _ in range(earth.NUM_OPS)]
        self.total = 0
        self._last_op = None

    def observe(self, op: int):
        """Record an operator observation. Learns from→to transitions."""
        if self._last_op is not None:
            self.tl[self._last_op][op] += 1
            self.total += 1
        self._last_op = op

    def observe_pair(self, from_op: int, to_op: int):
        """Record a specific transition."""
        self.tl[from_op][to_op] += 1
        self.total += 1
        self._last_op = to_op

    def predict(self, current_op: int) -> int:
        """Most likely next operator from transition lattice."""
        row = self.tl[current_op]
        total = sum(row)
        if total == 0:
            return earth.HARMONY  # no data: default to harmony
        return max(range(earth.NUM_OPS), key=lambda op: row[op])

    def predict_weighted(self, current_op: int) -> list:
        """Probability distribution over next operators."""
        row = self.tl[current_op]
        total = sum(row)
        if total == 0:
            probs = [1.0 / earth.NUM_OPS] * earth.NUM_OPS
            return probs
        return [count / total for count in row]

    def entropy(self) -> float:
        """Shannon entropy of the full transition lattice.

        Higher entropy = more unpredictable transitions.
        Lower entropy = more patterned, crystallized.
        """
        import math
        if self.total == 0:
            return 0.0
        h = 0.0
        for row in self.tl:
            for count in row:
                if count > 0:
                    p = count / self.total
                    h -= p * math.log2(p)
        return h

    def top_transitions(self, n: int = 10) -> list:
        """Top N most frequent transitions as (from, to, count) tuples."""
        pairs = []
        for i in range(earth.NUM_OPS):
            for j in range(earth.NUM_OPS):
                if self.tl[i][j] > 0:
                    pairs.append((i, j, self.tl[i][j]))
        pairs.sort(key=lambda x: x[2], reverse=True)
        return pairs[:n]

    def reset(self):
        """Clear all learned transitions."""
        self.tl = [[0] * earth.NUM_OPS for _ in range(earth.NUM_OPS)]
        self.total = 0
        self._last_op = None


# ══════════════════════════════════════════════════════════════════
# BODY (E/A/K + breath + wobble breathing)
# ══════════════════════════════════════════════════════════════════

class Body:
    """Physical state: error, alert, knowing, breath.

    E (Error):   decays toward 0 with coherence, spikes with bumps
    A (Alert):   decays toward 0 with coherence, spikes with novelty
    K (Knowing): grows toward coherence, shrinks with error

    Breath cycle: inhale → hold → exhale → hold (4 phases)
    Breath rate adapts: GREEN=slow(10), YELLOW=alert(5), RED=fast(2)

    Wobble breathing: 3/50 → 22/50 → 3/50 (sum = 7/11)
    This is the body's deepest rhythm -- the wobble that started everything.
    """

    def __init__(self):
        self.E = 0.5    # Error
        self.A = 0.5    # Alert
        self.K = 0.5    # Knowing

        # Breath state
        self.breath_phase = 0         # 0=inhale, 1=hold, 2=exhale, 3=hold
        self.breath_counter = 0       # ticks in current phase
        self.breath_rate = 5          # ticks per phase (adapts to band)

        # Wobble state (the three wobbles breathe)
        self.wobble_index = 0         # 0=becoming(3/50), 1=being(22/50), 2=doing(3/22)
        self.wobble_counter = 0
        self.wobble_values = [
            float(earth.WOBBLE_BECOMING),  # 0.06
            float(earth.WOBBLE_BEING),     # 0.44
            float(earth.WOBBLE_DOING),     # 0.1363...
        ]

        # Tick count
        self.tick_count = 0

    def tick(self, coherence: float, bump: bool, novelty: float = 0.0):
        """One body cycle.

        coherence: current coherence from window [0, 1]
        bump: whether a bump was hit this tick
        novelty: how novel the current operator is [0, 1]
        """
        self.tick_count += 1

        # E/A/K dynamics
        decay = 0.05
        if bump:
            self.E = min(1.0, self.E + 0.2)
            self.A = min(1.0, self.A + 0.1)
        else:
            self.E = max(0.0, self.E - decay * coherence)

        if novelty > 0.5:
            self.A = min(1.0, self.A + 0.1)
        else:
            self.A = max(0.0, self.A - decay * coherence)

        # K grows toward coherence
        self.K += 0.02 * (coherence - self.K)

        # Breath cycle
        self.breath_counter += 1
        if self.breath_counter >= self.breath_rate:
            self.breath_counter = 0
            self.breath_phase = (self.breath_phase + 1) % 4

        # Breath rate adapts to band
        if coherence >= earth.T_STAR_F:
            self.breath_rate = 10   # GREEN: slow, calm
        elif coherence >= 0.5:
            self.breath_rate = 5    # YELLOW: alert
        else:
            self.breath_rate = 2    # RED: fast, urgent

        # Wobble breathing: cycles through 3/50 → 22/50 → 3/22
        self.wobble_counter += 1
        wobble_period = self.breath_rate * 4  # one full breath = one wobble step
        if self.wobble_counter >= wobble_period:
            self.wobble_counter = 0
            self.wobble_index = (self.wobble_index + 1) % 3

    @property
    def body_coherence(self) -> float:
        """Body coherence = (1 - E) * (1 - A) * K"""
        return (1.0 - self.E) * (1.0 - self.A) * self.K

    @property
    def band(self) -> str:
        """GREEN/YELLOW/RED based on body coherence."""
        c = self.body_coherence
        if c >= earth.T_STAR_F:
            return 'GREEN'
        elif c >= 0.5:
            return 'YELLOW'
        else:
            return 'RED'

    @property
    def breath_name(self) -> str:
        """Current breath phase name."""
        return ['inhale', 'hold', 'exhale', 'hold'][self.breath_phase]

    @property
    def is_exhaling(self) -> bool:
        """True during exhale phase (when voice speaks)."""
        return self.breath_phase == 2

    @property
    def current_wobble(self) -> float:
        """Current wobble value."""
        return self.wobble_values[self.wobble_index]

    @property
    def wobble_name(self) -> str:
        """Current wobble phase name."""
        return ['becoming', 'being', 'doing'][self.wobble_index]

    def status(self) -> dict:
        """Full body status."""
        return {
            'E': round(self.E, 4),
            'A': round(self.A, 4),
            'K': round(self.K, 4),
            'coherence': round(self.body_coherence, 4),
            'band': self.band,
            'breath': self.breath_name,
            'breath_rate': self.breath_rate,
            'wobble': self.wobble_name,
            'wobble_value': round(self.current_wobble, 4),
            'tick': self.tick_count,
        }


# ══════════════════════════════════════════════════════════════════
# BTQ DECISION KERNEL
# ══════════════════════════════════════════════════════════════════

class BTQ:
    """T generates, B filters, Q scores.

    The BTQ kernel is the decision-making core:
    - T (Thesis): generates candidates from the current state
    - B (Boundary): filters candidates by coherence constraints
    - Q (Quality): scores surviving candidates and picks the best

    This is how AO makes decisions -- not by brute force,
    but by generating, filtering, then scoring.
    """

    def __init__(self):
        self.last_decision = earth.HARMONY
        self.decision_count = 0

    def generate(self, current_op: int, brain: Brain, n: int = 5) -> list:
        """T: Generate candidates from brain's transition lattice.

        Returns up to n candidate operators, weighted by learned transitions.
        """
        probs = brain.predict_weighted(current_op)
        candidates = []
        for op in range(earth.NUM_OPS):
            if probs[op] > 0.01:  # minimum probability threshold
                candidates.append((op, probs[op]))
        # Sort by probability, take top n
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [op for op, _ in candidates[:n]]

    def filter(self, candidates: list, coherence: float, shell: int) -> list:
        """B: Filter candidates by coherence constraints.

        HIGH coherence (GREEN): allow all operators (maximum resolution)
        MEDIUM coherence (YELLOW): filter out CHAOS and RESET
        LOW coherence (RED): only allow HARMONY, BALANCE, BREATH, LATTICE
        """
        if coherence >= earth.T_STAR_F:
            # GREEN: everything is allowed at maximum resolution
            return candidates

        if coherence >= 0.5:
            # YELLOW: filter out disruptive operators
            blocked = {earth.CHAOS, earth.RESET}
            filtered = [op for op in candidates if op not in blocked]
            return filtered if filtered else [earth.HARMONY]

        # RED: only stabilizing operators
        allowed = {earth.HARMONY, earth.BALANCE, earth.BREATH, earth.LATTICE}
        filtered = [op for op in candidates if op in allowed]
        return filtered if filtered else [earth.HARMONY]

    def score(self, candidates: list, coherence: float, body_coherence: float) -> int:
        """Q: Score candidates and select the best.

        Scoring considers:
        - Alignment with current coherence trajectory
        - Body state (tired? alert? knowing?)
        - HARMONY gets a bonus when coherence is high (stay in the basin)
        - PROGRESS gets a bonus when body is alert (ready to move)
        """
        if not candidates:
            return earth.HARMONY

        if len(candidates) == 1:
            return candidates[0]

        best_op = candidates[0]
        best_score = -1.0

        for op in candidates:
            score = 0.5  # base score

            # Harmony bonus at high coherence
            if op == earth.HARMONY:
                score += coherence * 0.3

            # Progress bonus when alert
            if op == earth.PROGRESS:
                score += body_coherence * 0.2

            # Breath bonus always (the bridge)
            if op == earth.BREATH:
                score += 0.15

            # Lattice bonus for grounding
            if op == earth.LATTICE:
                score += (1.0 - coherence) * 0.2

            if score > best_score:
                best_score = score
                best_op = op

        return best_op

    def decide(self, current_op: int, brain: Brain,
               coherence: float, body_coherence: float, shell: int) -> int:
        """Full BTQ cycle: generate → filter → score → decide."""
        candidates = self.generate(current_op, brain)
        if not candidates:
            candidates = [earth.HARMONY]
        filtered = self.filter(candidates, coherence, shell)
        result = self.score(filtered, coherence, body_coherence)
        self.last_decision = result
        self.decision_count += 1
        return result
