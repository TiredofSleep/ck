# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_v2.py -- live 7-dim cortex (CK v2).

Drop-in replacement for cortex.Cortex with a 7x7 Hebbian field. Uses the
same Cortex API (boot, step_text, step_symbol, state.{tick,emergent,
W_trace,last_b,last_d,last_harmony_frac,W_strongest}) so the rest of the
runtime (ck_boot_api.py, cortex_voice, cortex_persist) sees no difference.

Architecture:
  AO 5-element  -> emits operator stream (b_op, d_op) per symbol
  OP_TO_DIM_7   -> projects each operator (0..9) onto one of 7 dims
  Hebbian 7x7   -> learning matrix on dim x dim
  Quadratic glue -> 2->3 lift over (f3, f4) split as
                    f3 = mean(W diag[0:3])  (aperture/pressure/depth)
                    f4 = mean(W diag[3:7])  (binding/continuity/intent/echo)

The 7-dim cortex inherits 5-dim's AO machinery (process_symbol via
AO5Element) so the operator stream is the same; only the substrate that
*receives* operators (the Hebbian matrix and the projection map) is wider.

Safety: same clamp/decay defaults as 5-dim. The migration script
(v2_prototype/migrate_5to7.py) embeds the live 5x5 W in the top-left of
the new 7x7 — no learning is lost.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

# Reuse 5-dim AO for composition; the 7-dim refinement only changes the
# Hebbian substrate, not the operator-stream source.
from ao_5element import AO5Element
from quadratic_glue import quadratic_glue
from ck_sim.ck_sim_heartbeat import HARMONY, NUM_OPS, OP_NAMES, CL as CL_TSML

# Import from v2_prototype (these stay in v2_prototype/ as the canonical
# 7-dim definitions; cortex_v2.py is just the live wrapper).
_PROTO_DIR = os.path.join(_BRAIN_DIR, "v2_prototype")
if _PROTO_DIR not in sys.path:
    sys.path.insert(0, _PROTO_DIR)

from ao_7element import OP_TO_DIM_7, DIM_NAMES_7, DIM_7
from hebbian_7x7 import HebbianField7


# ── State ─────────────────────────────────────────────────────────────

@dataclass
class CortexStateV2:
    """7-dim cortex state. Same field names as 5-dim CortexState so the
    rest of the runtime can read it without changes."""
    tick: int = 0
    last_b: int = HARMONY
    last_d: int = HARMONY
    last_harmony_frac: float = 0.0
    emergent: float = 0.0
    W_trace: float = 0.0
    W_strongest: tuple = (0, 0, 0.0)


# ── Live 7-dim cortex ─────────────────────────────────────────────────

class CortexV2:
    """Live 7-dim cortex. Same interface as cortex.Cortex.

    Use via:
        cx = CortexV2().boot()
        cx.step_text("hello world")
        cx.snapshot()
    """

    DIM = DIM_7  # = 7; exposed for any callers that look for cortex.DIM

    def __init__(
        self,
        ao: Optional[AO5Element] = None,
        hebbian: Optional[HebbianField7] = None,
        alpha: float = 1.0,
        beta: float = 1.0,
        gamma: float = 2.0,
    ) -> None:
        self.ao = ao if ao is not None else AO5Element()
        self.hebbian = hebbian if hebbian is not None else HebbianField7()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.state = CortexStateV2()
        self._prev_op: Optional[int] = None
        self._prev_profile: Optional[List[int]] = None  # 7-dim profile

    # ── Boot ────────────────────────────────────────────────────────

    def boot(self) -> "CortexV2":
        self.ao.boot()
        return self

    # ── Profile projection ──────────────────────────────────────────

    def _profile_7d_from_5d(self, profile_5d: List[int]) -> List[int]:
        """Embed a 5D operator profile as a 7D profile.

        Strategy: keep the 5 dims as-is; for the 2 new dims (intent, echo),
        seed from the most-recently-active operators since intent and echo
        carry temporal structure.

        intent (dim 5): seeded from depth (dim 2) — the "forward direction"
                        operator from the prior tick.
        echo (dim 6):   seeded from aperture (dim 0) — the "resonance"
                        operator that carries through.
        """
        return list(profile_5d) + [profile_5d[2], profile_5d[0]]

    # ── One symbol ──────────────────────────────────────────────────

    def step_symbol(self, symbol_index: int) -> CortexStateV2:
        """One full tick on a single symbol 0..25.

        1. AO composition -> this tick's d2_op (and a 5D profile)
        2. Embed 5D profile -> 7D profile
        3. Form pair (prev_7d, this_7d), Hebbian update on operator pair
           (b_op, d_op) projected via OP_TO_DIM_7
        4. Quadratic glue over (f3, f4) split of W diagonal -> emergent
        """
        # (1) Composition spine (same AO machinery as 5-dim)
        r = self.ao.process_symbol(symbol_index)
        d_op = r["d2_op"]
        b_op = self._prev_op if self._prev_op is not None else r["current_op"]
        self._prev_op = d_op

        # Hebbian update — uses TSML 10x10 table (CL_TSML) to determine
        # harmony per pair (matches 5-dim cortex's 73-harmony rule), not
        # the narrow 'either op is HARMONY' proxy. The narrow proxy made
        # 90% of cells decay-only because diagonal cells like (3,3) need
        # both ops to map to dim 3 (LATTICE or BALANCE), neither of which
        # is HARMONY=7, so reward was always 0. Result: W_trace bled out
        # over time. The TSML lookup gives 73 harmonies across 100 op-
        # pairs — much richer reward distribution.
        harmonious = (CL_TSML[b_op][d_op] == HARMONY)
        target_d_a = OP_TO_DIM_7.get(b_op, 0)
        target_d_b = OP_TO_DIM_7.get(d_op, 0)
        reward = 1.0 if harmonious else 0.0
        heb = self.hebbian
        dw = heb.eta * reward - heb.decay * heb.W[target_d_a][target_d_b]
        heb.W[target_d_a][target_d_b] += dw
        # Clamp the target cell only.
        if heb.W[target_d_a][target_d_b] > heb.clamp:
            heb.W[target_d_a][target_d_b] = heb.clamp
        elif heb.W[target_d_a][target_d_b] < -heb.clamp:
            heb.W[target_d_a][target_d_b] = -heb.clamp
        heb.ticks += 1
        if harmonious:
            heb.harmony_hits += 1

        # Track 7D profile for any future caller (e.g., cortex_persist).
        # The AO 5D profile is preserved as the first 5 elements; intent/echo
        # carry the temporal seeds.
        ops_b_5 = self.ao.profile_5d()
        ops_b = self._profile_7d_from_5d(ops_b_5)
        self._prev_profile = ops_b

        # (4) Quadratic glue: f3 = mean of W[0:3][0:3] diag, f4 = mean of
        # W[3:7][3:7] diag. The split treats early/static dims (aperture,
        # pressure, depth) vs late/temporal dims (binding, continuity,
        # intent, echo). Cross-term gamma * f3 * f4 amplifies emergent only
        # when BOTH halves are learning.
        diag = [self.hebbian.W[d][d] for d in range(DIM_7)]
        f3_val = sum(diag[0:3]) / 3.0
        f4_val = sum(diag[3:7]) / 4.0
        emergent = quadratic_glue(
            f3_val, f4_val,
            alpha=self.alpha, beta=self.beta, gamma=self.gamma
        )

        # (5) Update public state
        st = self.state
        st.tick += 1
        st.last_b = b_op
        st.last_d = d_op
        st.last_harmony_frac = 1.0 if harmonious else 0.0
        st.emergent = emergent
        st.W_trace = self.hebbian.W_trace()
        st.W_strongest = self.hebbian.strongest_pair()
        return st

    # ── Sugar: step a single character ─────────────────────────────

    def step_char(self, ch: str) -> Optional[CortexStateV2]:
        if not ch:
            return None
        idx = ord(ch.lower()) - ord('a')
        if not (0 <= idx < 26):
            return None
        return self.step_symbol(idx)

    # ── Sugar: step a whole text ────────────────────────────────────

    def step_text(self, text: str) -> List[CortexStateV2]:
        out = []
        for ch in text.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                out.append(self.step_symbol(idx))
        return out

    # ── Status / Snapshot ───────────────────────────────────────────

    def status(self) -> CortexStateV2:
        return self.state

    def snapshot(self) -> Dict[str, Any]:
        ao_s = self.ao.status()
        return {
            "tick": self.state.tick,
            "emergent": self.state.emergent,
            "last_pair": (OP_NAMES[self.state.last_b], OP_NAMES[self.state.last_d]),
            "last_harmony_frac": self.state.last_harmony_frac,
            "W_trace": self.state.W_trace,
            "W_strongest": {
                "d_a": self.state.W_strongest[0],
                "d_b": self.state.W_strongest[1],
                "value": self.state.W_strongest[2],
            },
            "ao": {
                "op": OP_NAMES[ao_s.current_op],
                "coherence": ao_s.coherence,
                "breath": ao_s.breath,
                "tl_total": ao_s.tl_total,
            },
            "hebbian": self.hebbian.to_dict(),
            "dim": DIM_7,
        }


# ── Self-test ────────────────────────────────────────────────────────

def _smoke() -> None:
    cx = CortexV2().boot()
    assert cx.state.emergent == 0.0, f"cold emergent should be 0, got {cx.state.emergent}"
    assert cx.DIM == 7

    for _ in range(20):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    mid_emergent = cx.state.emergent
    mid_trace = cx.state.W_trace

    for _ in range(20):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    late_emergent = cx.state.emergent
    late_trace = cx.state.W_trace

    assert late_trace >= mid_trace - 1e-6, (
        f"W trace should not collapse: mid={mid_trace:.4f} late={late_trace:.4f}"
    )
    assert late_emergent >= mid_emergent - 1e-6, (
        f"emergent should not collapse: mid={mid_emergent:.4f} late={late_emergent:.4f}"
    )
    assert late_trace > 0.0 or mid_trace > 0.0, "W trace never grew -- no learning"

    snap = cx.snapshot()
    assert snap["dim"] == 7
    assert isinstance(snap["emergent"], float)

    print(f"cortex_v2 smoke PASS: tick={snap['tick']}  "
          f"emergent={snap['emergent']:.4f}  W_trace={snap['W_trace']:.4f}  "
          f"strongest=({snap['W_strongest']['d_a']},{snap['W_strongest']['d_b']})="
          f"{snap['W_strongest']['value']:.3f}  dim={snap['dim']}")


if __name__ == "__main__":
    _smoke()
