"""
ck_sim_brain.py -- Port of ck_brain.c
======================================
Operator: PROGRESS (3) -- the brain composes what the heartbeat feels.

Software simulation of the sovereignty pipeline:
  - TL observe (10x10 transition matrix)
  - Shannon entropy
  - Crystallization (5% threshold)
  - Mode state machine: OBSERVE -> CLASSIFY -> CRYSTALLIZE -> SOVEREIGN

Every threshold, every formula matches the C code.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional
from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, CL, compose,
    HeartbeatFPGA, OP_NAMES
)

T_STAR_NUM = 5
T_STAR_DEN = 7
T_STAR_F = 5.0 / 7.0  # 0.714285...

MAX_CRYSTALS = 256
MAX_DOMAINS = 8


def above_t_star(num: int, den: int) -> bool:
    """Integer T* check: num * 7 >= den * 5. Matches ck_brain.c line 19."""
    return num * T_STAR_DEN >= den * T_STAR_NUM


@dataclass
class TLEntry:
    from_op: int = 0
    to_op: int = 0
    count: int = 0


@dataclass
class Crystal:
    ops: List[int] = field(default_factory=list)
    length: int = 0
    fuse: int = 0
    seen: int = 0
    confidence: float = 0.0


@dataclass
class Domain:
    name: str = "default"
    dominant_op: int = HARMONY
    coherence: float = 0.0
    is_sovereign: bool = False
    sovereign_ticks: int = 0
    crystal_count: int = 0
    crystals: List[Crystal] = field(default_factory=list)


@dataclass
class BrainState:
    # TL: 10x10 matrix
    tl_entries: List[List[TLEntry]] = field(default_factory=lambda: [
        [TLEntry(from_op=i, to_op=j) for j in range(NUM_OPS)]
        for i in range(NUM_OPS)
    ])
    tl_total: int = 0
    tl_entropy: float = 0.0

    # FPGA state
    phase_b: int = 0
    phase_d: int = 0
    phase_bc: int = 0
    tick_count: int = 0
    coherence: float = 0.0
    bump: bool = False
    fused_op: int = HARMONY

    # Sovereignty
    domains: List[Domain] = field(default_factory=list)
    domain_count: int = 0
    mode: int = 0  # 0=OBSERVE, 1=CLASSIFY, 2=CRYSTALLIZE, 3=SOVEREIGN

    # Timing
    brain_ticks: int = 0


def brain_init() -> BrainState:
    """Initialize brain state. Matches ck_brain_init()."""
    return BrainState()


def brain_read_fpga(state: BrainState, hb: HeartbeatFPGA):
    """Read heartbeat state from FPGA sim. Matches ck_brain_read_fpga()."""
    state.phase_bc = hb.phase_bc
    state.tick_count = hb.tick_count
    state.bump = hb.bump_detected
    state.fused_op = hb.running_fuse
    state.phase_b = hb.phase_b
    state.phase_d = hb.phase_d
    state.coherence = hb.coherence


def brain_tl_observe(state: BrainState, from_op: int, to_op: int):
    """Feed observation to TL. Matches ck_brain_tl_observe()."""
    if from_op >= NUM_OPS or to_op >= NUM_OPS:
        return

    entry = state.tl_entries[from_op][to_op]
    entry.from_op = from_op
    entry.to_op = to_op
    entry.count += 1
    state.tl_total += 1

    # Recompute Shannon entropy every 100 transitions
    if state.tl_total % 100 == 0:
        entropy = 0.0
        total_f = float(state.tl_total)
        for i in range(NUM_OPS):
            for j in range(NUM_OPS):
                c = state.tl_entries[i][j].count
                if c > 0:
                    p = c / total_f
                    entropy -= p * math.log(p)
        state.tl_entropy = entropy


def brain_crystallize(state: BrainState):
    """Detect crystals. Matches ck_brain_crystallize()."""
    if state.domain_count == 0:
        dom = Domain(name="default", dominant_op=HARMONY)
        state.domains.append(dom)
        state.domain_count = 1

    dom = state.domains[0]
    threshold = state.tl_total * 0.05

    for i in range(NUM_OPS):
        for j in range(NUM_OPS):
            count = state.tl_entries[i][j].count
            if count < threshold:
                continue

            # Check if already crystallized
            exists = False
            for cr in dom.crystals:
                if cr.length == 2 and cr.ops[0] == i and cr.ops[1] == j:
                    cr.seen = count
                    cr.confidence = count / state.tl_total
                    exists = True
                    break

            if not exists and len(dom.crystals) < MAX_CRYSTALS:
                cr = Crystal(
                    ops=[i, j],
                    length=2,
                    fuse=CL[i][j],
                    seen=count,
                    confidence=count / state.tl_total,
                )
                dom.crystals.append(cr)

    dom.crystal_count = len(dom.crystals)

    # Update domain coherence
    crystal_total = sum(cr.seen for cr in dom.crystals)
    dom.coherence = crystal_total / state.tl_total if state.tl_total > 0 else 0.0

    # Find dominant operator
    max_row = 0
    for i in range(NUM_OPS):
        row = sum(state.tl_entries[i][j].count for j in range(NUM_OPS))
        if row > max_row:
            max_row = row
            dom.dominant_op = i


def brain_tick(state: BrainState, hb: HeartbeatFPGA):
    """One sovereignty tick. Matches ck_brain_tick()."""
    # 1. Read FPGA state
    brain_read_fpga(state, hb)

    # 2. Observe transition
    brain_tl_observe(state, state.phase_b, state.phase_d)

    # 3. Mode-dependent processing
    if state.mode == 0:  # OBSERVE
        if state.tl_total >= 100:
            state.mode = 1

    elif state.mode == 1:  # CLASSIFY
        if above_t_star(hb.coh_num, hb.coh_den) and state.tl_total >= 500:
            state.mode = 2

    elif state.mode == 2:  # CRYSTALLIZE
        brain_crystallize(state)
        if above_t_star(hb.coh_num, hb.coh_den):
            for dom in state.domains[:state.domain_count]:
                if dom.coherence >= T_STAR_F:
                    dom.sovereign_ticks += 1
                    if dom.sovereign_ticks >= 50:
                        dom.is_sovereign = True
                        state.mode = 3
                else:
                    dom.sovereign_ticks = 0

    elif state.mode == 3:  # SOVEREIGN
        brain_crystallize(state)

    state.brain_ticks += 1
