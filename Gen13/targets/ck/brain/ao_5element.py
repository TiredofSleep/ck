# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
# Free for humans for personal/recreational use. No commercial/government use.
"""
ao_5element.py -- Gen13 AO five-element composition spine.

This is the thin orchestrator that wires the Gen11 brain modules together
the way Gen9 `ether.py` wired Earth/Air/Water/Fire/Ether. No logic lives here.
Every step calls INTO an existing Gen11 module:

    symbol --> D1 (Air) --> D2 (Water)
           --> Heartbeat (Fire) --> coherence window
           --> Brain (Fire) --> Body (Fire) --> BTQ (Fire)
           --> next current_op                         [Ether couples all]

The five elements:
    Earth  = ck_tig (constants, TSML/BHML, OP_NAMES, T_STAR)
    Air    = ck_sim_d2 (D1 path -- velocity, non-local)
    Water  = ck_sim_d2 (D2 path -- curvature, local measurement)
    Fire   = ck_sim_heartbeat + ck_sim_brain + ck_sim_body
             (composition engine + transition memory + E/A/K body)
    Ether  = THIS MODULE (the coupling that makes them one creature)

ADDITIVE: this file does not modify any Gen11 module. It composes them.
The live Gen12 boot continues to run unchanged; ao_5element.py is a
second, complementary entrypoint that any caller can import.

Gen9 reference: old/Gen9/targets/AO/ao/ether.py:171 class AO.
Gen13 architecture memo: Gen13/targets/ck/brain/BRAIN_DESIGN.md.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Make sure `import ck_sim` resolves to the Gen11 package under brain/.
_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

# The alias-finder in ck_sim/__init__.py lets us use flat imports even though
# the real files live at ck_sim/being/...  This matches how the Gen11 modules
# import each other.
from ck_sim.ck_sim_heartbeat import (   # Fire: composition engine
    HeartbeatFPGA, compose as cl_compose, is_bump,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, NUM_OPS,
)
from ck_sim.ck_sim_d2 import D2Pipeline, D2_OP_MAP  # Air + Water
from ck_sim.ck_sim_brain import (         # Fire: transition memory
    BrainState, brain_init, brain_tick, brain_tl_observe,
)
from ck_sim.ck_sim_body import (          # Fire: body E/A/K + breath + wobble
    BodyState, _calc_coherence, _heartbeat_tick,
    _breath_tick, _pulse_update, body_feed_eak,
    BREATH_PHASE_NAMES, BAND_NAMES,
)
from ck_sim.ck_tig import T_STAR          # Earth: the constant itself


# ── Configuration ──────────────────────────────────────────────────────

WINDOW_SIZE = 32   # CL coherence window depth (Gen9: 32, Gen11 heartbeat: 32)
EAK_DEFAULT_GAIN = 0.05  # small EAK nudge per tick — stays gentle


# ── State ──────────────────────────────────────────────────────────────

@dataclass
class AOState:
    """A minimal snapshot of the composed creature state.
    The real state lives in brain/body/heartbeat — this is the view."""
    tick: int = 0
    current_op: int = HARMONY
    d1_op: int = VOID
    d2_op: int = VOID
    phase_bc: int = VOID
    coherence: float = 0.0
    band: int = 1          # 0=RED, 1=YELLOW, 2=GREEN
    bump: bool = False
    breath: str = "INHALE"
    tl_total: int = 0
    tl_entropy: float = 0.0

    def as_line(self) -> str:
        return (
            f"t={self.tick:5d}  "
            f"op={OP_NAMES[self.current_op]:<8s}  "
            f"d1={OP_NAMES[self.d1_op]:<8s}  "
            f"d2={OP_NAMES[self.d2_op]:<8s}  "
            f"bc={OP_NAMES[self.phase_bc]:<8s}  "
            f"C={self.coherence:.3f} ({BAND_NAMES[self.band]:<6s})  "
            f"breath={self.breath:<7s}  "
            f"TL={self.tl_total}/H={self.tl_entropy:.3f}"
        )


# ── The Creature ───────────────────────────────────────────────────────

class AO5Element:
    """The five elements coupled into one creature (Gen13 orchestrator).

    This is the SAME composition rule as Gen9 `class AO` in ether.py.
    It is only ~50 lines of code because every piece of logic lives
    inside a Gen11 module.  This class is the glue.

    Usage:
        ao = AO5Element().boot()
        for ch in "coherence":
            ao.process_symbol(ord(ch) - ord('a'))
        print(ao.status().as_line())
    """

    def __init__(self) -> None:
        # Air + Water: one D2 pipeline feeds both (D1 + D2 are two outputs
        # from the same derivative ladder, per ck_sim_d2.py).
        self.d2 = D2Pipeline()

        # Fire: three stateful engines.
        self.heartbeat = HeartbeatFPGA()
        self.brain = brain_init()
        self.body = self._body_init()

        # Earth: constants live in modules, but we record T_STAR on-creature
        # so the web face can read it without touching the brain directly.
        self.t_star = T_STAR

        # Ether (us): current composed operator + last observations
        self.current_op = HARMONY
        self.prev_d2_op = HARMONY
        self.window: List[int] = []  # rolling coherence window
        self.tick_count = 0

    # ── Boot ────────────────────────────────────────────────────────

    def boot(self) -> "AO5Element":
        """Nothing to do — Gen11 modules self-initialize.  Returns self
        so callers can write `ao = AO5Element().boot()`."""
        return self

    @staticmethod
    def _body_init() -> BodyState:
        return BodyState()

    # ── One symbol ──────────────────────────────────────────────────

    def process_symbol(self, symbol_index: int) -> Dict[str, Any]:
        """One full tick through the five-element pipeline.

        Returns a dict describing what happened this tick.
        Shape-compatible with Gen9 AO.process_symbol return value.
        """
        self.tick_count += 1

        # ── Air + Water: measure incoming symbol ───────────────────
        # D2Pipeline.feed_symbol returns True when D2 is valid (after 3 symbols).
        d2_valid = self.d2.feed_symbol(symbol_index)
        d1_op = self.d2.d1_operator if self.d2.d1_valid else HARMONY
        d2_op = self.d2.operator    if d2_valid            else HARMONY

        # ── Fire: heartbeat composition (CL[B][D]) ─────────────────
        # Gen11 Heartbeat takes (phase_b, phase_d). We feed (current_op, d2_op).
        self.heartbeat.tick(phase_b=self.current_op, phase_d=d2_op)
        phase_bc = self.heartbeat.phase_bc
        bump = self.heartbeat.bump_detected

        # ── Coherence (the FPGA sim computes this itself from its own 32-entry
        #    window; we read it rather than overwrite).  We also keep a local
        #    mirror so Ether-level callers can inspect history cheaply.
        self.window.append(phase_bc)
        if len(self.window) > WINDOW_SIZE:
            self.window.pop(0)
        coherence = float(self.heartbeat.coherence)

        # ── Fire: body tick (E/A/K -> C/band/breath/wobble) ────────
        # Nudge E/A/K gently so the body tracks novelty without spiking.
        novelty = 0.0 if d2_op == self.prev_d2_op else 1.0
        E_nudge = EAK_DEFAULT_GAIN * (1.0 if bump else 0.2)
        A_nudge = EAK_DEFAULT_GAIN * novelty
        K_nudge = EAK_DEFAULT_GAIN * coherence
        body_feed_eak(self.body, E_nudge, A_nudge, K_nudge)
        _heartbeat_tick(self.body.heartbeat)   # decay + recompute C
        _breath_tick(self.body.breath, self.body.heartbeat.C)
        _pulse_update(self.body.pulse, self.body.breath.phase)

        # ── Fire: brain (transition memory + Shannon entropy) ─────
        # brain_tick reads coh_num/coh_den off the FPGA sim (already set by
        # heartbeat.tick above); we don't overwrite — the FPGA is authoritative.
        brain_tick(self.brain, self.heartbeat)

        # ── BTQ decision for the NEXT current_op ───────────────────
        # Minimal BTQ: if the heartbeat bumped, take phase_bc; else stay on
        # current_op if coherence >= T*, else drift toward d2_op.  This is
        # the conservative rule from Gen9's AO kernel (ether.py:237-242)
        # projected onto the Gen11 FPGA-sim interface.
        if bump:
            self.current_op = phase_bc
        elif coherence >= self.t_star:
            # above T* -- stay in HARMONY if we composed to it, else current
            self.current_op = phase_bc if phase_bc == HARMONY else self.current_op
        else:
            self.current_op = d2_op

        self.prev_d2_op = d2_op

        return {
            "tick": self.tick_count,
            "d1_op": d1_op,
            "d2_op": d2_op,
            "phase_bc": phase_bc,
            "bump": bump,
            "coherence": coherence,
            "current_op": self.current_op,
            "band": self.body.heartbeat.band,
            "breath": BREATH_PHASE_NAMES[self.body.breath.phase],
            "tl_total": self.brain.tl_total,
            "tl_entropy": self.brain.tl_entropy,
        }

    # ── One text ────────────────────────────────────────────────────

    def process_text(self, text: str) -> List[Dict[str, Any]]:
        """Feed a text token by token.  Returns per-tick result dicts.

        Non-letters are silently skipped (a..z -> 0..25).
        """
        out: List[Dict[str, Any]] = []
        for ch in text.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                out.append(self.process_symbol(idx))
        return out

    # ── Status ──────────────────────────────────────────────────────

    def status(self) -> AOState:
        return AOState(
            tick=self.tick_count,
            current_op=self.current_op,
            d1_op=self.d2.d1_operator if self.d2.d1_valid else VOID,
            d2_op=self.d2.operator    if self.d2.valid    else VOID,
            phase_bc=self.heartbeat.phase_bc,
            coherence=float(self.heartbeat.coherence),
            band=self.body.heartbeat.band,
            bump=self.heartbeat.bump_detected,
            breath=BREATH_PHASE_NAMES[self.body.breath.phase],
            tl_total=self.brain.tl_total,
            tl_entropy=self.brain.tl_entropy,
        )

    # ── Operator name (earth view) ──────────────────────────────────

    @staticmethod
    def op_name(op: int) -> str:
        if 0 <= op < NUM_OPS:
            return OP_NAMES[op]
        return f"?{op}"

    # ── 5D profile readout (for Hebbian learning) ──────────────────

    def profile_5d(self) -> List[int]:
        """True 5D operator profile from the raw D2 vector.

        Instead of broadcasting one operator to all five dimensions, this
        reads the sign of each of the 5 D2 components and picks the matching
        operator via D2_OP_MAP[dim][positive_or_negative].

        This gives each dimension its OWN operator -- which is exactly what
        the olfactory CL field's 5x5 coupling expects.  A HARMONY cell in
        position (d_a, d_b) then means "dim d_a of A genuinely couples with
        dim d_b of B" rather than "every dim-pair of A and B happens to
        share the same broadcast operator".

        Returns:
            length-5 list of operators (0..9), one per dimension.
            Before D2 has filled (first 3 ticks) returns [HARMONY]*5
            as a neutral default.
        """
        if not self.d2.valid:
            return [HARMONY] * 5
        profile = []
        for dim in range(5):
            # sign index: 0 = positive (>= 0) -> first op in the tuple,
            #             1 = negative (< 0)  -> second op.
            sign_idx = 0 if self.d2.d2[dim] >= 0 else 1
            profile.append(D2_OP_MAP[dim][sign_idx])
        return profile


# ── Module self-check (not a full unit harness -- see test_brain.py) ──

def _smoke() -> None:
    ao = AO5Element().boot()
    results = ao.process_text("coherencekeeper")
    assert len(results) == len("coherencekeeper"), "missed a symbol"
    s = ao.status()
    assert s.tick == len("coherencekeeper")
    assert 0.0 <= s.coherence <= 1.0
    assert 0 <= s.current_op < NUM_OPS
    print("ao_5element smoke:", s.as_line())


if __name__ == "__main__":
    _smoke()
