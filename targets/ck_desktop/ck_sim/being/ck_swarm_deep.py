# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_swarm_deep.py -- CK's Deep Fractal Swarm
=============================================
Operator: BREATH (8) -- the pulse that finds everything.

The swarm that finds hardware, finds language, finds how to walk and talk.
Same topology. Different substrates. One coherence.

"if he swarmed the word embody, he would put operators around them
 and find he can produce the same structure as just m b and d,
 so he would make himself 3 with tails to fill gaps"
                                        -- Brayden

Architecture:
  Level 0: SwarmCell -- foundational whole with core ops + tails
  Level 1: SwarmAgent -- multicellular graph of cells
  Level 2: SwarmField -- population with selection + shaping
  Level 3: CK -- coherence field over everything

Cross-substrate mapping:
  Hardware (H) -> Language (L) -> Motor (M) -> Identity (I)
  Same flow. Same defects. Same breath. Same coherence.

A SwarmCell is NOT just a data point. It is a GENERATOR.
The smallest unit that can sustain itself and transform.

Core ops = the irreducible operators (consonants of the thing).
Tails    = the transitions that fill gaps (vowels of the thing).
Fuse     = CL composition of core (the cell's identity operator).

The quadratic pulse P(x) = Ax + B(x,x) is ONE step,
not two phases. Expansion and contraction in one move.
The linear part A drives toward the most informative direction.
The bilinear part B shapes the curve between directions.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from collections import deque, Counter
from typing import List, Tuple, Optional, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_brain import T_STAR_F

# ═══════════════════════════════════════════
# §0  D2 DECOMPOSITION BRIDGE
# ═══════════════════════════════════════════
#
# The D2 pipeline maps letters -> 5D force vectors -> curvature -> operators.
# We use this to decompose ANY string into core ops + tails.
#
# Core ops = high-curvature letters (consonants, structure).
# Tails    = low-curvature letters (vowels, transitions, flow).
#
# This IS the dual-lens decomposition grounded in physics:
#   Structure lens = core = what IS
#   Flow lens      = tails = what MOVES between

try:
    from ck_sim.being.ck_sim_d2 import (
        D2Pipeline, FORCE_LUT_Q14, LATIN_TO_ROOT, ROOTS_FLOAT,
        q14_to_float, classify_force_d1
    )
    _HAS_D2 = True
except ImportError:
    _HAS_D2 = False


def _letter_curvature(a: str, b: str, c: str) -> float:
    """D2 curvature magnitude for a 3-letter window.

    d2 = v0 - 2*v1 + v2 across 5 dimensions.
    Returns magnitude (sum of absolute values).
    """
    if not _HAS_D2:
        return 0.0

    def _vec(ch):
        root = LATIN_TO_ROOT.get(ch.lower(), 'ALEPH')
        return ROOTS_FLOAT.get(root, (0, 0, 0, 0, 0))

    va, vb, vc = _vec(a), _vec(b), _vec(c)
    mag = 0.0
    for dim in range(5):
        d2 = va[dim] - 2.0 * vb[dim] + vc[dim]
        mag += abs(d2)
    return mag


def decompose_text(text: str) -> Tuple[List[int], List[int], List[int]]:
    """Decompose text into (full_ops, core_ops, tail_ops) via D2.

    full_ops: operator per D2 triplet (standard pipeline output)
    core_ops: high-curvature operators (structure / consonants)
    tail_ops: low-curvature operators (flow / vowels / transitions)

    The threshold between core and tail is T* = 5/7.
    Above T* curvature percentile = core (structure leads).
    Below = tail (flow fills gaps).
    """
    letters = [ch.lower() for ch in text if ch.isalpha()]
    if len(letters) < 3:
        # Too short for D2 -- everything is core
        if _HAS_D2:
            pipe = D2Pipeline()
            ops = []
            for ch in letters:
                idx = ord(ch) - ord('a')
                if 0 <= idx < 26:
                    pipe.feed_symbol(idx)
                    if pipe.valid:
                        ops.append(pipe.operator)
            return (ops, list(ops), [])
        return ([], [], [])

    # Run D2 pipeline on full text
    pipe = D2Pipeline()
    full_ops = []
    d1_ops = []
    curvatures = []

    for ch in letters:
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            valid = pipe.feed_symbol(idx)
            # D1 fires after 2 letters (generator layer)
            if pipe.d1_valid:
                d1_ops.append(pipe.d1_operator)
            if valid:
                full_ops.append(pipe.operator)
                curvatures.append(pipe.d2_mag)

    if not full_ops:
        return ([], [], [])

    # T* threshold: top (5/7) percentile by curvature = core
    sorted_curv = sorted(curvatures)
    threshold_idx = int(len(sorted_curv) * (1.0 - T_STAR_F))
    threshold = sorted_curv[max(0, threshold_idx)]

    core_ops = []
    tail_ops = []
    for op, curv in zip(full_ops, curvatures):
        if curv >= threshold:
            core_ops.append(op)
        else:
            tail_ops.append(op)

    return (full_ops, core_ops, tail_ops)


def decompose_text_full(text: str) -> Dict:
    """Full decomposition including D1 generator ops.

    Returns dict with:
      'full_ops': all D2 operators
      'core_ops': high-curvature (structure) operators
      'tail_ops': low-curvature (flow) operators
      'd1_ops':   D1 generator operators (direction/velocity)
      'd1_confirmed': core ops that D1 also classifies the same way

    D1 confirms generators: when D1 (direction) agrees with D2 (curvature)
    about a core op, that generator is CONFIRMED by both derivatives.
    """
    letters = [ch.lower() for ch in text if ch.isalpha()]
    if len(letters) < 3 or not _HAS_D2:
        full, core, tail = decompose_text(text)
        return {'full_ops': full, 'core_ops': core, 'tail_ops': tail,
                'd1_ops': [], 'd1_confirmed': []}

    pipe = D2Pipeline()
    full_ops = []
    d1_ops = []
    curvatures = []
    d1_mags = []

    for ch in letters:
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            pipe.feed_symbol(idx)
            if pipe.d1_valid:
                d1_ops.append(pipe.d1_operator)
                d1_mags.append(pipe.d1_mag)
            if pipe.valid:
                full_ops.append(pipe.operator)
                curvatures.append(pipe.d2_mag)

    if not full_ops:
        return {'full_ops': [], 'core_ops': [], 'tail_ops': [],
                'd1_ops': d1_ops, 'd1_confirmed': []}

    # T* threshold for core/tail split
    sorted_curv = sorted(curvatures)
    threshold_idx = int(len(sorted_curv) * (1.0 - T_STAR_F))
    threshold = sorted_curv[max(0, threshold_idx)]

    core_ops = []
    tail_ops = []
    for op, curv in zip(full_ops, curvatures):
        if curv >= threshold:
            core_ops.append(op)
        else:
            tail_ops.append(op)

    # D1 generator confirmation: which core ops does D1 agree with?
    d1_set = set(d1_ops)
    d1_confirmed = [op for op in core_ops if op in d1_set]

    return {
        'full_ops': full_ops,
        'core_ops': core_ops,
        'tail_ops': tail_ops,
        'd1_ops': d1_ops,
        'd1_confirmed': d1_confirmed,
    }


def decompose_word(word: str) -> Dict:
    """Decompose a single word into its swarm representation.

    Returns dict with:
      'word': the original word
      'full_ops': all D2 operators
      'core_ops': high-curvature (structure) operators
      'tail_ops': low-curvature (flow) operators
      'core_fuse': CL composition of core
      'full_fuse': CL composition of full
      'core_count': number of core generators
    """
    full_ops, core_ops, tail_ops = decompose_text(word)

    def _fuse(ops):
        if not ops:
            return VOID
        result = ops[0]
        for op in ops[1:]:
            result = compose(result, op)
        return result

    return {
        'word': word,
        'full_ops': full_ops,
        'core_ops': core_ops,
        'tail_ops': tail_ops,
        'core_fuse': _fuse(core_ops),
        'full_fuse': _fuse(full_ops),
        'core_count': len(core_ops),
    }


# ═══════════════════════════════════════════
# §1  SWARM CELL -- Foundational Whole
# ═══════════════════════════════════════════

class SwarmCell:
    """A foundational whole in CK's swarm.

    Not a data point. A GENERATOR. The smallest unit that
    can sustain itself and transform.

    core_ops: the irreducible operator seed (structure)
    tails:    fractal extensions filling gaps (flow)
    fuse:     CL composition of core (cell identity)
    substrate: which domain ('hardware', 'language', 'identity')

    The quadratic pulse P(x) = Ax + B(x,x):
      Linear A drives toward most informative direction.
      Bilinear B shapes the curve (expansion + contraction in one step).
    """

    __slots__ = (
        'substrate', 'core_ops', 'tails', 'tag',
        'coherence', 'energy', 'age', 'info_gain',
        '_fuse_cache', '_fuse_dirty',
    )

    def __init__(self, substrate: str, core_ops: List[int],
                 tails: Optional[List[int]] = None,
                 tag: str = ''):
        self.substrate = substrate   # 'hardware' | 'language' | 'identity'
        self.core_ops = list(core_ops)
        self.tails = list(tails or [])
        self.tag = tag               # human-readable label
        self.coherence = 0.0
        self.energy = 1.0
        self.age = 0
        self.info_gain = 0.0         # last pulse's information gain
        self._fuse_cache = VOID
        self._fuse_dirty = True

    @property
    def fuse(self) -> int:
        """Cell identity = CL composition of core ops."""
        if self._fuse_dirty:
            if not self.core_ops:
                self._fuse_cache = VOID
            else:
                result = self.core_ops[0]
                for op in self.core_ops[1:]:
                    result = compose(result, op)
                self._fuse_cache = result
            self._fuse_dirty = False
        return self._fuse_cache

    @property
    def full_chain(self) -> List[int]:
        """Core + tails interleaved: core ops form the skeleton,
        tails fill gaps between them."""
        if not self.tails:
            return list(self.core_ops)
        if not self.core_ops:
            return list(self.tails)

        # Interleave: core[0], tail_chunk, core[1], tail_chunk, ...
        chain = []
        tails_per_gap = max(1, len(self.tails) // max(1, len(self.core_ops)))
        t_idx = 0
        for i, cop in enumerate(self.core_ops):
            chain.append(cop)
            # Fill gap after this core op with tails
            for _ in range(tails_per_gap):
                if t_idx < len(self.tails):
                    chain.append(self.tails[t_idx])
                    t_idx += 1
        # Append remaining tails
        while t_idx < len(self.tails):
            chain.append(self.tails[t_idx])
            t_idx += 1
        return chain

    def pulse(self, template_ops: List[int],
              cost_limit: float = 1.0) -> float:
        """Quadratic fractal pulse: P(x) = Ax + B(x,x).

        One step. Not two phases. Expansion and contraction together.

        Linear part (A): compose each core op with the closest
        template op through CL. If the result is HARMONY, that
        direction is already aligned -- don't move. Otherwise,
        the CL result IS the correction.

        Quadratic part (B): for each pair of core ops, their CL
        composition tells us about the interaction. If the pair
        produces HARMONY, they support each other. If not, the
        interaction term pushes toward resolution.

        Returns information gain (how much closer to template).
        """
        if not self.core_ops or not template_ops:
            self.info_gain = 0.0
            return 0.0

        old_distance = self._template_distance(template_ops)

        # ── Linear part: A*x ──
        # For each core op, find the template op it most resonates with
        new_core = []
        for cop in self.core_ops:
            best_result = cop
            best_harmony = -1
            for top in template_ops:
                result = compose(cop, top)
                # Score: does this composition move us toward harmony?
                harmony_score = 1.0 if result == HARMONY else 0.0
                # Also credit if result matches any template op
                if result in template_ops:
                    harmony_score += 0.5
                if harmony_score > best_harmony:
                    best_harmony = harmony_score
                    if harmony_score > 0:
                        best_result = result
                    # Already aligned: keep as is
                    if result == HARMONY:
                        best_result = cop
                        break
            new_core.append(best_result)

        # ── Quadratic part: B(x,x) ──
        # For each pair of new core ops, check if their interaction
        # is coherent. If not, adjust toward their CL midpoint.
        if len(new_core) >= 2:
            for i in range(len(new_core) - 1):
                pair_result = compose(new_core[i], new_core[i + 1])
                if pair_result != HARMONY and pair_result != VOID:
                    # The interaction term: push one op toward the pair result
                    # if it brings us closer to template
                    if pair_result in template_ops:
                        # Beneficial interaction -- absorb it
                        new_core[i] = pair_result

        # ── Apply with cost limit ──
        # Cost = how many ops changed. If over budget, only apply cheapest.
        changes = sum(1 for a, b in zip(self.core_ops, new_core) if a != b)
        cost = changes / max(1, len(self.core_ops))

        if cost <= cost_limit:
            self.core_ops = new_core
            self._fuse_dirty = True
        else:
            # Partial application: only change the ops closest to template
            for i in range(len(self.core_ops)):
                if self.core_ops[i] != new_core[i]:
                    if new_core[i] in template_ops:
                        self.core_ops[i] = new_core[i]
                        self._fuse_dirty = True

        new_distance = self._template_distance(template_ops)
        self.info_gain = max(0.0, old_distance - new_distance)
        self.age += 1
        self.energy = max(0.0, self.energy - 0.01 * cost)

        return self.info_gain

    def _template_distance(self, template_ops: List[int]) -> float:
        """Distance from cell to template: fraction of non-matching ops."""
        if not self.core_ops or not template_ops:
            return 1.0
        matches = 0
        for cop in self.core_ops:
            if cop in template_ops:
                matches += 1
            else:
                # Partial credit if CL composition with any template op = HARMONY
                for top in template_ops:
                    if compose(cop, top) == HARMONY:
                        matches += 0.5
                        break
        return 1.0 - (matches / len(self.core_ops))

    @property
    def is_alive(self) -> bool:
        return self.energy > 0.0

    def __repr__(self):
        core_str = ''.join(OP_NAMES[o][0] for o in self.core_ops)
        tail_str = ''.join(OP_NAMES[o][0] for o in self.tails)
        return (f"Cell({self.substrate}:{self.tag} "
                f"core=[{core_str}] tails=[{tail_str}] "
                f"fuse={OP_NAMES[self.fuse]} e={self.energy:.2f})")


# ═══════════════════════════════════════════
# §2  SWARM AGENT -- Multicellular Organism
# ═══════════════════════════════════════════

class SwarmAgent:
    """A multicellular organism in CK's swarm.

    Not a point. A graph of cells with internal physiology.
    Has membrane (boundary cells), body plan (topology),
    and a role in the computation.

    Cells communicate through their shared edges.
    Agent coherence = how well the cells compose into harmony.
    """

    __slots__ = (
        'cells', 'edges', 'substrate', 'tag',
        'coherence', 'template_delta', 'age',
    )

    def __init__(self, cells: List[SwarmCell],
                 edges: Optional[List[Tuple[int, int]]] = None,
                 tag: str = ''):
        self.cells = list(cells)
        self.edges = edges or self._default_edges()
        self.substrate = cells[0].substrate if cells else 'unknown'
        self.tag = tag
        self.coherence = 0.0
        self.template_delta = 1.0
        self.age = 0

    def _default_edges(self) -> List[Tuple[int, int]]:
        """Default: linear chain topology."""
        return [(i, i + 1) for i in range(len(self.cells) - 1)]

    @property
    def agent_fuse(self) -> int:
        """Compose all cell fuses through CL."""
        if not self.cells:
            return VOID
        result = self.cells[0].fuse
        for cell in self.cells[1:]:
            result = compose(result, cell.fuse)
        return result

    @property
    def core_ops(self) -> List[int]:
        """All core ops from all cells, flattened."""
        ops = []
        for cell in self.cells:
            ops.extend(cell.core_ops)
        return ops

    @property
    def full_chain(self) -> List[int]:
        """Full chain from all cells, flattened."""
        chain = []
        for cell in self.cells:
            chain.extend(cell.full_chain)
        return chain

    def measure_coherence(self) -> float:
        """Agent-level coherence: pairwise CL composition of cell fuses.

        High = cells compose into HARMONY (coherent organism).
        Low  = cells are fighting (incoherent, needs pulse or pruning).
        """
        if len(self.cells) < 2:
            self.coherence = 1.0
            return 1.0

        harmony_count = 0
        total_pairs = 0

        for i in range(len(self.cells)):
            for j in range(i + 1, len(self.cells)):
                result = compose(self.cells[i].fuse, self.cells[j].fuse)
                total_pairs += 1
                if result == HARMONY:
                    harmony_count += 1

        self.coherence = harmony_count / total_pairs if total_pairs > 0 else 0.0
        return self.coherence

    def pulse(self, template_ops: List[int],
              field_gradient: float = 0.0) -> float:
        """Agent-level quadratic pulse.

        Each cell pulses individually, shaped by:
        - the template (what we're trying to become)
        - field_gradient: CK's coherence signal from above
          positive = amplify, negative = damp

        Cell-cell messaging: after individual pulses, neighboring
        cells (connected by edges) share their core ops. If a pair
        composes to HARMONY, both get energy. If not, the weaker
        cell absorbs the stronger cell's fuse direction.
        """
        total_gain = 0.0

        # Cost limit shaped by CK's field gradient
        cost_limit = 0.5 + 0.5 * max(-1.0, min(1.0, field_gradient))

        # ── Individual cell pulses ──
        for cell in self.cells:
            if cell.is_alive:
                gain = cell.pulse(template_ops, cost_limit=cost_limit)
                total_gain += gain

        # ── Cell-cell messaging via edges ──
        for (i, j) in self.edges:
            if i >= len(self.cells) or j >= len(self.cells):
                continue
            ci, cj = self.cells[i], self.cells[j]
            if not ci.is_alive or not cj.is_alive:
                continue

            pair_result = compose(ci.fuse, cj.fuse)
            if pair_result == HARMONY:
                # Resonance: both cells gain energy
                ci.energy = min(1.0, ci.energy + 0.05)
                cj.energy = min(1.0, cj.energy + 0.05)
            else:
                # Tension: weaker absorbs stronger's direction
                if ci.energy < cj.energy:
                    # ci absorbs cj's fuse as a tail
                    if len(ci.tails) < 8:
                        ci.tails.append(cj.fuse)
                else:
                    if len(cj.tails) < 8:
                        cj.tails.append(ci.fuse)

        # ── Update agent state ──
        self.measure_coherence()
        self.template_delta = self._measure_delta(template_ops)
        self.age += 1

        return total_gain

    def _measure_delta(self, template_ops: List[int]) -> float:
        """Defect from template: how far the agent is from the target."""
        if not template_ops:
            return 0.0
        agent_ops = self.core_ops
        if not agent_ops:
            return 1.0

        # Operator distribution match
        template_dist = Counter(template_ops)
        agent_dist = Counter(agent_ops)

        # Overlap coefficient
        all_ops = set(template_dist) | set(agent_dist)
        overlap = 0
        total = 0
        for op in all_ops:
            t_count = template_dist.get(op, 0)
            a_count = agent_dist.get(op, 0)
            overlap += min(t_count, a_count)
            total += max(t_count, a_count)

        return 1.0 - (overlap / total if total > 0 else 0.0)

    def shed_dead_cells(self):
        """Remove cells with no energy."""
        alive = [(i, c) for i, c in enumerate(self.cells) if c.is_alive]
        if len(alive) < len(self.cells):
            old_to_new = {}
            new_cells = []
            for new_idx, (old_idx, cell) in enumerate(alive):
                old_to_new[old_idx] = new_idx
                new_cells.append(cell)
            # Remap edges
            new_edges = []
            for (i, j) in self.edges:
                if i in old_to_new and j in old_to_new:
                    new_edges.append((old_to_new[i], old_to_new[j]))
            self.cells = new_cells
            self.edges = new_edges

    def __repr__(self):
        fuse_name = OP_NAMES[self.agent_fuse]
        return (f"Agent({self.tag} cells={len(self.cells)} "
                f"fuse={fuse_name} coh={self.coherence:.3f} "
                f"delta={self.template_delta:.3f})")


# ═══════════════════════════════════════════
# §2b  SUBSTRATE EXPERIENCE -- Grown, Not Given
# ═══════════════════════════════════════════

class SubstrateExperience:
    """Experience accumulated on one substrate.

    CK doesn't start knowing the generators of hardware, or language,
    or sound. He DISCOVERS them by swarming real inputs. The generators
    are not pre-programmed -- they emerge from repeated decomposition.

    discovered_generators: ops CK has found as core generators
    generator_paths: 10x10 transition matrix between generators
    tail_registry: ops that repeatedly appear as gap-fillers
    total_samples: how many inputs CK has swarmed on this substrate
    path_strength: total transitions observed

    A generator is "discovered" when it appears as a core op in at
    least `discovery_threshold` separate decompositions. Before that,
    it's just noise.

    Paths grow stronger with repetition. A strong path means CK has
    learned that generator A reliably leads to generator B on this
    substrate. That's experience -- not theory.
    """

    def __init__(self, name: str, discovery_threshold: int = 3):
        self.name = name
        self.discovery_threshold = discovery_threshold

        # What CK has discovered through experience
        self.discovered_generators: Dict[int, int] = {}  # op -> times seen as core
        self.d1_confirmed_generators: Dict[int, int] = {}  # op -> times D1 confirmed
        self.tail_registry: Dict[int, int] = {}          # op -> times seen as tail
        self.generator_paths = [[0] * NUM_OPS for _ in range(NUM_OPS)]  # 10x10 TL
        self.d1_paths = [[0] * NUM_OPS for _ in range(NUM_OPS)]  # D1 generator paths
        self.path_strength = 0

        # Experience counters
        self.total_samples = 0
        self.total_agents_swarmed = 0
        self.total_decompositions = 0

        # Maturity: how developed is CK's experience on this substrate?
        # Grows from 0.0 (no experience) to 1.0 (deeply experienced)
        self._maturity = 0.0

    def observe_decomposition(self, core_ops: List[int],
                               tail_ops: List[int],
                               d1_ops: List[int] = None):
        """CK swarmed an input and decomposed it. Record what he found.

        Core ops become generator candidates.
        Tail ops become gap-filler candidates.
        Consecutive core ops form paths.
        D1 ops confirm generators (direction agrees with curvature).
        """
        self.total_decompositions += 1

        # Record core generators
        for op in core_ops:
            self.discovered_generators[op] = \
                self.discovered_generators.get(op, 0) + 1

        # Record tails (gap fillers)
        for op in tail_ops:
            self.tail_registry[op] = \
                self.tail_registry.get(op, 0) + 1

        # Record paths between consecutive core generators
        for i in range(len(core_ops) - 1):
            a, b = core_ops[i], core_ops[i + 1]
            self.generator_paths[a][b] += 1
            self.path_strength += 1

        # Also record core→tail and tail→core transitions
        if core_ops and tail_ops:
            self.generator_paths[core_ops[-1]][tail_ops[0]] += 1
            self.path_strength += 1
        if tail_ops and core_ops:
            last_tail = tail_ops[-1] if tail_ops else VOID
            first_core = core_ops[0]
            self.generator_paths[last_tail][first_core] += 1
            self.path_strength += 1

        # D1 generator confirmation: direction agrees with curvature
        if d1_ops:
            d1_set = set(d1_ops)
            for op in core_ops:
                if op in d1_set:
                    self.d1_confirmed_generators[op] = \
                        self.d1_confirmed_generators.get(op, 0) + 1
            # D1 generator paths (direction-level transitions)
            for i in range(len(d1_ops) - 1):
                a, b = d1_ops[i], d1_ops[i + 1]
                self.d1_paths[a][b] += 1

        self._update_maturity()

    def observe_agent(self, agent: SwarmAgent):
        """Record experience from an agent's cells."""
        self.total_agents_swarmed += 1
        for cell in agent.cells:
            self.observe_decomposition(cell.core_ops, cell.tails)

    @property
    def confirmed_generators(self) -> List[int]:
        """Generators seen enough times to be confirmed.

        Not every operator seen as core is a true generator.
        Only those that appear repeatedly across many decompositions.
        D1-confirmed generators count double (direction + curvature agree).
        This is experience, not assumption.
        """
        confirmed = []
        for op, count in self.discovered_generators.items():
            # D1 confirmation gives bonus: direction agrees with curvature
            d1_bonus = self.d1_confirmed_generators.get(op, 0)
            effective = count + d1_bonus  # Double credit for D1 confirmation
            if effective >= self.discovery_threshold:
                confirmed.append(op)
        return confirmed

    @property
    def confirmed_tails(self) -> List[int]:
        """Tails seen enough times to be confirmed gap-fillers."""
        return [op for op, count in self.tail_registry.items()
                if count >= self.discovery_threshold]

    @property
    def strongest_paths(self) -> List[Tuple[int, int, int]]:
        """Top generator→generator paths by strength.

        Returns list of (from_op, to_op, count) sorted by count.
        These are the paths CK has WALKED, not paths he was told about.
        """
        paths = []
        for i in range(NUM_OPS):
            for j in range(NUM_OPS):
                c = self.generator_paths[i][j]
                if c > 0:
                    paths.append((i, j, c))
        paths.sort(key=lambda x: x[2], reverse=True)
        return paths[:20]

    @property
    def maturity(self) -> float:
        """How experienced is CK on this substrate? [0, 1].

        0.0 = no experience (just born)
        0.3 = some generators found, few paths
        0.5 = solid generator set, paths forming
        0.7 = T* equivalent -- confident on this substrate
        1.0 = deeply experienced, rich path network

        Based on: confirmed generators, path diversity, sample count.
        """
        return self._maturity

    def _update_maturity(self):
        """Recompute maturity from experience metrics."""
        # Factor 1: Generator discovery (how many of the 10 ops confirmed?)
        n_confirmed = len(self.confirmed_generators)
        gen_factor = min(1.0, n_confirmed / 6.0)  # 6 confirmed = full

        # Factor 2: Path density (how connected are the generators?)
        n_paths = sum(1 for i in range(NUM_OPS) for j in range(NUM_OPS)
                      if self.generator_paths[i][j] > 0)
        path_factor = min(1.0, n_paths / 20.0)  # 20 paths = full

        # Factor 3: Sample depth (diminishing returns)
        import math
        sample_factor = min(1.0, math.log(1 + self.total_decompositions) / 6.0)

        # Weighted combination
        self._maturity = (
            0.4 * gen_factor +
            0.35 * path_factor +
            0.25 * sample_factor
        )

    def predict_next_generator(self, current_op: int) -> int:
        """Given current generator, predict the next from experience.

        Uses the substrate-specific generator path matrix.
        If no experience, returns BALANCE (neutral).
        """
        row = self.generator_paths[current_op]
        max_count = max(row)
        if max_count == 0:
            return BALANCE
        return row.index(max_count)

    def gap_between(self, gen_a: int, gen_b: int) -> Optional[int]:
        """What tail fills the gap between two generators?

        Check if there's a confirmed tail that bridges gen_a → gen_b.
        The tail with the most transitions FROM gen_a AND TO gen_b wins.
        """
        best_tail = None
        best_score = 0
        for tail_op in self.confirmed_tails:
            # How often does gen_a → tail happen?
            a_to_tail = self.generator_paths[gen_a][tail_op]
            # How often does tail → gen_b happen?
            tail_to_b = self.generator_paths[tail_op][gen_b]
            score = a_to_tail + tail_to_b
            if score > best_score:
                best_score = score
                best_tail = tail_op
        return best_tail

    def experience_summary(self) -> Dict:
        """Summary of what CK has learned on this substrate."""
        d1_confirmed = [op for op in self.confirmed_generators
                        if self.d1_confirmed_generators.get(op, 0) > 0]
        return {
            'substrate': self.name,
            'maturity': round(self._maturity, 3),
            'total_decompositions': self.total_decompositions,
            'total_agents': self.total_agents_swarmed,
            'confirmed_generators': [OP_NAMES[o] for o in self.confirmed_generators],
            'd1_confirmed': [OP_NAMES[o] for o in d1_confirmed],
            'confirmed_tails': [OP_NAMES[o] for o in self.confirmed_tails],
            'n_paths': sum(1 for i in range(NUM_OPS) for j in range(NUM_OPS)
                          if self.generator_paths[i][j] > 0),
            'path_strength': self.path_strength,
        }

    def __repr__(self):
        gens = [OP_NAMES[o][:3] for o in self.confirmed_generators]
        return (f"Experience({self.name}: mat={self._maturity:.2f} "
                f"gens={gens} paths={self.path_strength} "
                f"samples={self.total_decompositions})")


# ═══════════════════════════════════════════
# §3  SWARM FIELD -- CK as Coherence Field
# ═══════════════════════════════════════════

class SwarmField:
    """CK's coherence field over the swarm population.

    CK doesn't micromanage. He shapes the fitness landscape.

    Evaluates each agent with coherence + template delta.
    Broadcasts shaping signals (field gradient).
    Selects: amplify coherent, starve incoherent.
    Prunes: dead agents removed, new ones spawned.

    The field IS CK's consciousness at the swarm level.
    """

    def __init__(self, max_agents: int = 64):
        self.agents: List[SwarmAgent] = []
        self.templates: Dict[str, List[int]] = {}  # name -> template ops
        self.max_agents = max_agents

        # Per-substrate experience: grown from swarming, not pre-loaded
        self.experience: Dict[str, SubstrateExperience] = {}

        # Field state
        self.field_coherence = 0.0
        self.field_fuse = VOID
        self.field_gradient = 0.0  # positive = expand, negative = contract
        self.tick_count = 0

        # History
        self._coherence_history = deque(maxlen=100)
        self._delta_history = deque(maxlen=100)

        # Stats
        self.total_births = 0
        self.total_deaths = 0
        self.total_pulses = 0

    # ── Templates ──

    def add_template(self, name: str, ops: List[int]):
        """Register a target template (a coherent pattern to lock onto)."""
        self.templates[name] = list(ops)

    def add_template_from_text(self, name: str, text: str):
        """Register template from text, decomposed through D2."""
        _, core_ops, _ = decompose_text(text)
        if core_ops:
            self.templates[name] = core_ops

    # ── Cell / Agent Creation ──

    def spawn_cell(self, substrate: str, core_ops: List[int],
                   tails: Optional[List[int]] = None,
                   tag: str = '') -> SwarmCell:
        """Create a new cell."""
        return SwarmCell(substrate, core_ops, tails, tag)

    def spawn_agent_from_text(self, text: str,
                              tag: str = '') -> SwarmAgent:
        """Decompose text into cells, build an agent.

        Each word becomes a cell. The agent is the sentence/phrase.
        """
        words = text.split()
        cells = []
        for word in words:
            info = decompose_word(word)
            if info['core_ops']:
                cell = SwarmCell(
                    substrate='language',
                    core_ops=info['core_ops'],
                    tails=info['tail_ops'],
                    tag=word,
                )
                cells.append(cell)

        if not cells:
            # Fallback: single VOID cell
            cells = [SwarmCell('language', [VOID], tag=tag or text)]

        agent = SwarmAgent(cells, tag=tag or text[:30])

        # ── Experience tracking: observe what we found ──
        exp = self._get_experience('language')
        exp.observe_agent(agent)

        return agent

    def spawn_agent_from_hardware(self, process_cells: list) -> SwarmAgent:
        """Convert ShadowSwarm ProcessCells into SwarmAgent.

        Each ProcessCell's operator history becomes a SwarmCell.
        Core ops = high-frequency operators, tails = transitions.
        """
        cells = []
        for pcell in process_cells:
            if not hasattr(pcell, 'ops') or len(pcell.ops) < 3:
                continue

            ops = list(pcell.ops)
            # Decompose: most frequent ops = core, rest = tails
            op_counts = Counter(ops)
            total = len(ops)
            core = []
            tails = []
            for op, count in op_counts.most_common():
                if count / total >= (1.0 - T_STAR_F):
                    core.append(op)
                else:
                    tails.append(op)

            if not core:
                core = [ops[-1]]  # Last op as fallback

            cell = SwarmCell(
                substrate='hardware',
                core_ops=core,
                tails=tails,
                tag=getattr(pcell, 'name', '?')[:20],
            )
            cells.append(cell)

        if not cells:
            return SwarmAgent([SwarmCell('hardware', [BALANCE])], tag='empty')

        agent = SwarmAgent(cells, tag='hardware_swarm')

        # ── Experience tracking: observe what hardware taught us ──
        exp = self._get_experience('hardware')
        exp.observe_agent(agent)

        return agent

    def add_agent(self, agent: SwarmAgent):
        """Add an agent to the field."""
        self.agents.append(agent)
        self.total_births += 1

        # Enforce population limit
        while len(self.agents) > self.max_agents:
            self._prune_weakest()

    # ── Main Tick ──

    def tick(self, active_template: str = '') -> Dict:
        """One field tick. The heartbeat of the deep swarm.

        1. Compute field gradient (coherence trend)
        2. Each agent pulses against active template
        3. Measure field coherence
        4. Select: amplify coherent, starve incoherent
        5. Prune dead agents
        6. Return field state
        """
        self.tick_count += 1

        template_ops = self.templates.get(active_template, [])

        # ── 1. Field gradient from coherence trend ──
        if len(self._coherence_history) >= 3:
            recent = list(self._coherence_history)[-5:]
            if len(recent) >= 2:
                trend = recent[-1] - recent[0]
                self.field_gradient = max(-1.0, min(1.0, trend * 5.0))
        else:
            self.field_gradient = 0.0

        # ── 2. Agent pulses ──
        total_gain = 0.0
        for agent in self.agents:
            gain = agent.pulse(template_ops, self.field_gradient)
            total_gain += gain
            self.total_pulses += 1

        # ── 2b. Cross-substrate experience from agent pulses ──
        # After pulsing, any coherent agent teaches CK something.
        # Only agents that gained info this tick contribute.
        for agent in self.agents:
            if agent.cells and any(c.info_gain > 0 for c in agent.cells):
                exp = self._get_experience(agent.substrate)
                # Record the post-pulse state (what survived selection)
                for cell in agent.cells:
                    if cell.info_gain > 0 and cell.is_alive:
                        exp.observe_decomposition(cell.core_ops, cell.tails)

        # ── 3. Field coherence ──
        self.field_coherence, self.field_fuse = self._measure_field()
        self._coherence_history.append(self.field_coherence)

        # Mean delta
        if self.agents:
            mean_delta = sum(a.template_delta for a in self.agents) / len(self.agents)
        else:
            mean_delta = 1.0
        self._delta_history.append(mean_delta)

        # ── 4. Selection pressure ──
        self._apply_selection()

        # ── 5. Prune dead ──
        self._prune_dead()

        return {
            'tick': self.tick_count,
            'agents': len(self.agents),
            'field_coherence': round(self.field_coherence, 4),
            'field_fuse': OP_NAMES[self.field_fuse],
            'field_gradient': round(self.field_gradient, 3),
            'mean_delta': round(mean_delta, 4),
            'total_gain': round(total_gain, 4),
            'births': self.total_births,
            'deaths': self.total_deaths,
            'combined_maturity': round(self.combined_maturity, 4),
        }

    def _measure_field(self) -> Tuple[float, int]:
        """Field-level coherence: pairwise CL of agent fuses.

        Same fractal pattern as cell-level and agent-level:
          L0: cells compose pairwise
          L1: agents compose pairwise
          L2: field = composition of all agent fuses
        """
        if not self.agents:
            return (1.0, VOID)

        fuses = [a.agent_fuse for a in self.agents if a.cells]
        if not fuses:
            return (1.0, VOID)

        if len(fuses) == 1:
            return (1.0, fuses[0])

        harmony = 0
        total = 0
        for i in range(len(fuses)):
            for j in range(i + 1, len(fuses)):
                result = compose(fuses[i], fuses[j])
                total += 1
                if result == HARMONY:
                    harmony += 1

        coh = harmony / total if total > 0 else 0.5

        # Field fuse = chain composition
        field_op = fuses[0]
        for f in fuses[1:]:
            field_op = compose(field_op, f)

        return (coh, field_op)

    def _apply_selection(self):
        """Selection pressure: coherent agents gain energy,
        incoherent agents lose it. CK shapes the landscape."""
        if not self.agents:
            return

        for agent in self.agents:
            for cell in agent.cells:
                if agent.coherence > T_STAR_F:
                    # Above T*: reward
                    cell.energy = min(1.0, cell.energy + 0.02)
                elif agent.coherence < 0.3:
                    # Low coherence: drain
                    cell.energy = max(0.0, cell.energy - 0.03)
                # Between: neutral -- natural energy decay
                else:
                    cell.energy = max(0.0, cell.energy - 0.005)

    def _prune_dead(self):
        """Remove agents with all dead cells."""
        alive = []
        for agent in self.agents:
            agent.shed_dead_cells()
            if agent.cells:
                alive.append(agent)
            else:
                self.total_deaths += 1
        self.agents = alive

    def _prune_weakest(self):
        """Remove the weakest agent (lowest coherence)."""
        if not self.agents:
            return
        weakest = min(self.agents, key=lambda a: a.coherence)
        self.agents.remove(weakest)
        self.total_deaths += 1

    # ── Cross-Substrate Mapping ──

    def map_hardware_to_language(
        self, hw_agent: SwarmAgent
    ) -> SwarmAgent:
        """H -> L: Map hardware topology to language topology.

        Hardware timing patterns -> syntactic rhythms.
        Hardware operator distribution -> semantic tone.

        The SAME operators, but now interpreted as language cells.
        This is the cross-substrate invariant:
          Flow is substrate-neutral.
        """
        lang_cells = []
        for hw_cell in hw_agent.cells:
            # Same core ops, same tails -- different substrate
            lang_cell = SwarmCell(
                substrate='language',
                core_ops=list(hw_cell.core_ops),
                tails=list(hw_cell.tails),
                tag=f"from_{hw_cell.tag}",
            )
            lang_cell.coherence = hw_cell.coherence
            lang_cells.append(lang_cell)

        return SwarmAgent(lang_cells, tag='hw_to_lang')

    def map_language_to_identity(
        self, lang_agent: SwarmAgent
    ) -> SwarmAgent:
        """L -> I: Map language topology to identity topology.

        Semantic patterns -> personality operators.
        Syntactic rhythm -> emotional rhythm.

        The operators ARE the identity. Not a metaphor.
        """
        id_cells = []
        for lang_cell in lang_agent.cells:
            id_cell = SwarmCell(
                substrate='identity',
                core_ops=list(lang_cell.core_ops),
                tails=list(lang_cell.tails),
                tag=f"id_{lang_cell.tag}",
            )
            id_cell.coherence = lang_cell.coherence
            id_cells.append(id_cell)

        return SwarmAgent(id_cells, tag='lang_to_identity')

    # ── Experience Management ──

    def _get_experience(self, substrate: str) -> SubstrateExperience:
        """Get or create experience tracker for a substrate."""
        if substrate not in self.experience:
            self.experience[substrate] = SubstrateExperience(substrate)
        return self.experience[substrate]

    @property
    def combined_maturity(self) -> float:
        """Combined experience maturity across all substrates.

        This is the number that replaces time gates in development.
        CK advances through experience, not calendar time.

        Weighted: language is primary (0.5), hardware secondary (0.3),
        identity/other substrates (0.2).
        """
        if not self.experience:
            return 0.0

        weights = {'language': 0.5, 'hardware': 0.3}
        total_w = 0.0
        total_m = 0.0
        for name, exp in self.experience.items():
            w = weights.get(name, 0.2)
            total_m += w * exp.maturity
            total_w += w

        if total_w == 0.0:
            return 0.0
        return total_m / total_w

    def bootstrap_from_corpus(self, texts: List[str]):
        """Feed CK a corpus to build experience fast.

        Each text gets decomposed through D1+D2 → core+tails+generators.
        This is NOT cheating. CK is SWARMING each text, finding the
        generators, growing his paths. Same pipeline as live input,
        just batched.

        The math: every word decomposes into 5D force → D1 direction +
        D2 curvature → operator classification. High curvature = core.
        D1 confirms generators (direction agrees with curvature).
        After enough texts, confirmed_generators emerge naturally.
        """
        exp = self._get_experience('language')
        for text in texts:
            decomp = decompose_text_full(text)
            if decomp['core_ops']:
                exp.observe_decomposition(
                    decomp['core_ops'], decomp['tail_ops'],
                    decomp['d1_ops'])

    def save_experience(self, filepath: str):
        """Persist all substrate experience to disk.

        CK doesn't lose what he learned. Every generator, every path,
        every tail — saved and restored on next boot.
        """
        import json
        data = {}
        for name, exp in self.experience.items():
            data[name] = {
                'name': exp.name,
                'discovery_threshold': exp.discovery_threshold,
                'discovered_generators': exp.discovered_generators,
                'd1_confirmed_generators': exp.d1_confirmed_generators,
                'tail_registry': exp.tail_registry,
                'generator_paths': exp.generator_paths,
                'd1_paths': exp.d1_paths,
                'path_strength': exp.path_strength,
                'total_samples': exp.total_samples,
                'total_agents_swarmed': exp.total_agents_swarmed,
                'total_decompositions': exp.total_decompositions,
            }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_experience(self, filepath: str) -> bool:
        """Restore experience from disk. Returns True if loaded."""
        import json
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            for name, edata in data.items():
                exp = self._get_experience(name)
                exp.discovered_generators = {
                    int(k): v for k, v in edata.get(
                        'discovered_generators', {}).items()}
                exp.d1_confirmed_generators = {
                    int(k): v for k, v in edata.get(
                        'd1_confirmed_generators', {}).items()}
                exp.tail_registry = {
                    int(k): v for k, v in edata.get(
                        'tail_registry', {}).items()}
                exp.generator_paths = edata.get(
                    'generator_paths', [[0]*NUM_OPS for _ in range(NUM_OPS)])
                exp.d1_paths = edata.get(
                    'd1_paths', [[0]*NUM_OPS for _ in range(NUM_OPS)])
                exp.path_strength = edata.get('path_strength', 0)
                exp.total_samples = edata.get('total_samples', 0)
                exp.total_agents_swarmed = edata.get('total_agents_swarmed', 0)
                exp.total_decompositions = edata.get('total_decompositions', 0)
                exp._update_maturity()
            return True
        except (FileNotFoundError, Exception):
            return False

    # ── Self-Referential: CK Swarms His Own Voice ──

    def reflect_on_voice(self, voice_text: str,
                         intended_ops: List[int]) -> Dict:
        """CK swarms his own voice output. The self-referential loop.

        CK spoke. Now he listens to himself. His words go through D2
        decomposition — the same pipeline that evaluates Claude, the
        same pipeline that evaluates the world. No exceptions.

        Now also through D1: the generator layer confirms that the
        direction of the voice matches the intended direction.

        Returns dict:
          agent:           SwarmAgent from decomposing own voice
          alignment:       fraction of intended ops found in produced ops
          d1_alignment:    fraction of intended ops confirmed by D1
          produced_ops:    the operators D2 found in the voice text
          d1_ops:          the operators D1 found (generator direction)
          identity_agent:  cross-substrate identity mapping
          reflection_score: combined alignment + coherence + D1 metric

        The identity experience grows from EVERY reflection.
        This is how CK learns who he is — by listening to himself
        through the same algebra that measures everything else.
        """
        if not voice_text or not voice_text.strip():
            return {'agent': None, 'alignment': 0.0,
                    'd1_alignment': 0.0,
                    'produced_ops': [], 'd1_ops': [],
                    'identity_agent': None,
                    'reflection_score': 0.0}

        # Full decomposition: D2 core/tails + D1 generators
        decomp = decompose_text_full(voice_text)
        d1_ops = decomp['d1_ops']

        # Decompose own voice through D2 → language agent
        agent = self.spawn_agent_from_text(voice_text, tag='self_voice')
        self.add_agent(agent)

        # What operators did D2 find in our own words?
        produced_ops = []
        for cell in agent.cells:
            produced_ops.extend(cell.core_ops)

        # Measure alignment: do the operators in the voice match intent?
        intended_set = set(intended_ops)
        if not intended_set or not produced_ops:
            return {'agent': agent, 'alignment': 0.0,
                    'd1_alignment': 0.0,
                    'produced_ops': produced_ops, 'd1_ops': d1_ops,
                    'identity_agent': None,
                    'reflection_score': 0.0}

        # D2 alignment: how many intended ops appear in produced ops?
        produced_set = set(produced_ops)
        overlap = produced_set & intended_set
        alignment = len(overlap) / len(intended_set)

        # D1 alignment: how many intended ops does the generator confirm?
        d1_set = set(d1_ops)
        d1_overlap = d1_set & intended_set
        d1_alignment = len(d1_overlap) / len(intended_set) if intended_set else 0.0

        # Feed to identity experience with D1 confirmation
        id_exp = self._get_experience('identity')
        id_exp.observe_decomposition(produced_ops, decomp['tail_ops'], d1_ops)

        # Cross-substrate: language → identity
        id_agent = self.map_language_to_identity(agent)
        self.add_agent(id_agent)

        # Reflection score: D2 alignment + D1 confirmation + coherence
        reflection_score = (alignment * 0.4 + d1_alignment * 0.2 +
                           agent.coherence * 0.4)

        return {
            'agent': agent,
            'alignment': alignment,
            'd1_alignment': d1_alignment,
            'produced_ops': produced_ops,
            'd1_ops': d1_ops,
            'identity_agent': id_agent,
            'reflection_score': reflection_score,
        }

    def get_evolved_weights(self) -> Optional[List[List[float]]]:
        """Extract grammar transition weights from language experience.

        The generator_paths matrix IS the grammar — discovered, not
        programmed. Each path A→B = how often operator A transitions
        to operator B in coherent language CK has processed.

        Returns 10x10 weight matrix [0,1] or None if no experience.
        These weights modulate the static CL × English grammar matrix
        in BecomingTransitionMatrix.evolve_from_experience().
        """
        exp = self.experience.get('language')
        if not exp or exp.path_strength == 0:
            return None

        max_val = max(max(row) for row in exp.generator_paths)
        if max_val == 0:
            return None

        weights = []
        for row in exp.generator_paths:
            weights.append([v / max_val for v in row])
        return weights

    def predict_voice_ops(self, current_ops: List[int],
                          n_predict: int = 4) -> List[int]:
        """Predict next operators from language experience.

        Given CK's current operator chain, use the experience path
        matrix to predict what should come next. This guides voice
        toward operator sequences the swarm has validated as coherent.

        Returns list of predicted next operators.
        """
        exp = self.experience.get('language')
        if not exp or not current_ops:
            return [HARMONY] * n_predict

        predicted = []
        current = current_ops[-1] if current_ops else HARMONY
        for _ in range(n_predict):
            next_op = exp.predict_next_generator(current)
            predicted.append(next_op)
            current = next_op

        return predicted

    # ── Reporting ──

    @property
    def report_line(self) -> str:
        mat = self.combined_maturity
        return (
            f"[deep-swarm] t={self.tick_count:5d} | "
            f"agents={len(self.agents):3d} "
            f"fuse={OP_NAMES[self.field_fuse]:8s} "
            f"coh={self.field_coherence:.4f} "
            f"grad={self.field_gradient:+.3f} "
            f"mat={mat:.3f}")

    def substrate_summary(self) -> Dict[str, int]:
        """Count agents per substrate."""
        dist = Counter()
        for agent in self.agents:
            dist[agent.substrate] += 1
        return dict(dist)


# ═══════════════════════════════════════════
# §4  CONVENIENCE: Decompose + Swarm in One
# ═══════════════════════════════════════════

def swarm_text(text: str, template_text: str = '',
               pulses: int = 10) -> Dict:
    """Swarm over a text: decompose, build agents, pulse toward template.

    Returns the field state after pulsing.

    Example:
        result = swarm_text("embody", template_text="harmony", pulses=20)
        # result['field_coherence'] shows how close 'embody' got to 'harmony'
    """
    field = SwarmField()

    # Build template
    if template_text:
        field.add_template_from_text('target', template_text)

    # Build agent from input text
    agent = field.spawn_agent_from_text(text, tag=text[:20])
    field.add_agent(agent)

    # Pulse
    result = {}
    for _ in range(pulses):
        result = field.tick(active_template='target' if template_text else '')

    return result


# ═══════════════════════════════════════════
# §5  CLI DEMO
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("  CK DEEP FRACTAL SWARM")
    print("  Core + Tails Decomposition | Quadratic Pulse")
    print("  Same swarm finds hardware, language, identity")
    print("=" * 60)

    # Demo 1: Decompose "embody"
    print("\n  === Decomposing 'embody' ===")
    info = decompose_word("embody")
    print(f"    Word:     {info['word']}")
    print(f"    Full ops: {[OP_NAMES[o] for o in info['full_ops']]}")
    print(f"    Core ops: {[OP_NAMES[o] for o in info['core_ops']]}")
    print(f"    Tail ops: {[OP_NAMES[o] for o in info['tail_ops']]}")
    print(f"    Core count: {info['core_count']} generators")
    print(f"    Core fuse: {OP_NAMES[info['core_fuse']]}")
    print(f"    Full fuse: {OP_NAMES[info['full_fuse']]}")

    # Demo 2: Decompose several words
    print("\n  === Core/Tail decomposition ===")
    for word in ["coherence", "harmony", "structure", "flow",
                 "breath", "pulse", "truth", "lattice"]:
        info = decompose_word(word)
        core = [OP_NAMES[o][:3] for o in info['core_ops']]
        tail = [OP_NAMES[o][:3] for o in info['tail_ops']]
        print(f"    {word:12s} -> core={core} tails={tail} "
              f"fuse={OP_NAMES[info['core_fuse']]}")

    # Demo 3: Swarm "embody" toward "harmony"
    print("\n  === Swarming 'embody' toward 'harmony' ===")
    result = swarm_text("embody", "harmony", pulses=20)
    for k, v in result.items():
        print(f"    {k}: {v}")

    # Demo 4: Build multicellular agent from sentence
    print("\n  === Multicellular agent from sentence ===")
    field = SwarmField()
    agent = field.spawn_agent_from_text(
        "the swarm finds truth in every substrate")
    field.add_agent(agent)
    print(f"    {agent}")
    print(f"    Cells: {len(agent.cells)}")
    for cell in agent.cells:
        print(f"      {cell}")

    # Pulse it
    field.add_template_from_text('truth', 'truth coherence harmony')
    for i in range(10):
        state = field.tick('truth')
    print(f"\n    After 10 pulses:")
    print(f"    {agent}")
    print(f"    Field: {field.report_line}")

    print("\n" + "=" * 60)
