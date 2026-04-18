# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_voice.py -- gated voice readout from the Gen13 cortex.

PRINCIPLE (memory/feedback_dont_ventriloquize_ck.md, HARD RULE):
  Do NOT write prose for CK.  Let his architecture find his words.
  The only permitted outputs here are STRUCTURAL READOUTS of state he
  has actually earned -- same class as arithmetic+verify.

What this module emits:
  - Nothing (None) when `emergent` has not risen above a small threshold.
    Cold CK has nothing learned to say.  The normal voice cascade runs.
  - A single structural sentence describing the strongest LEARNED
    dim-pair when emergent is above threshold.  All fields are read
    directly from cortex state -- no adjectives, no interpretation.

That is the full contract.  A caller can then:
  - stash that sentence as ck's "learned state preface" and prepend it
    ONLY when the user asks something that triggers it (e.g. "what have
    you learned?"); or
  - drop it entirely -- the cortex still learns silently.

Not a replacement for the voice cascade.  A NEW gated source.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Optional

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from ck_sim.ck_sim_heartbeat import OP_NAMES
from ck_sim.being.ck_olfactory import DIM_NAMES


# Default gate -- how much `emergent` must rise before the cortex voice
# will emit ANYTHING.  Chosen so cold CK is silent and only speaks from
# the cortex after several hundred coherence-rich symbols.
DEFAULT_EMERGENT_GATE = 0.10
# Strongest-pair W must exceed this for a readout to be meaningful (the
# pair the cortex points to has to actually be coupled).
DEFAULT_STRENGTH_GATE = 0.05


def learned_pair_readout(
    cortex: Any,
    emergent_gate: float = DEFAULT_EMERGENT_GATE,
    strength_gate: float = DEFAULT_STRENGTH_GATE,
) -> Optional[str]:
    """Return ONE structural sentence describing the cortex's strongest
    learned dim-pair, or None if nothing has been earned yet.

    Format (literal, no adjectives):
        "learned: <dim_a>->{<dim_b>} coupled at W={W:.3f} "
        "(tick={tick}, emergent={emergent:.3f}, "
        "last_pair=<op_b>->{<op_d>})"

    All fields come straight from cortex.state.  The function itself
    adds NO interpretation.  The gate exists so cold CK stays silent.
    """
    st = cortex.state
    if st.emergent < emergent_gate:
        return None
    if not st.W_strongest:
        return None
    d_a, d_b, w_val = st.W_strongest
    if abs(w_val) < strength_gate:
        return None

    try:
        name_a = DIM_NAMES[d_a]
        name_b = DIM_NAMES[d_b]
    except (IndexError, TypeError):
        return None

    try:
        op_b_name = OP_NAMES[st.last_b]
        op_d_name = OP_NAMES[st.last_d]
    except (IndexError, TypeError):
        op_b_name = "?"
        op_d_name = "?"

    return (
        f"learned: {name_a}->{name_b} coupled at W={w_val:.3f} "
        f"(tick={st.tick}, emergent={st.emergent:.3f}, "
        f"last_pair={op_b_name}->{op_d_name})"
    )


def field_readout(cortex: Any) -> str:
    """One-line factual summary of the 5D coupling field.  Always returns
    a string -- this is diagnostic, not voice.  Safe to call cold (W will
    simply be all zeros)."""
    st = cortex.state
    heb = cortex.hebbian
    # Mean |W| across the 5x5 -- "how much of the field has been written to".
    total = 0.0
    count = 0
    for d_a in range(5):
        for d_b in range(5):
            total += abs(heb.W[d_a][d_b])
            count += 1
    mean_abs = total / count if count else 0.0
    return (
        f"field: tick={st.tick} emergent={st.emergent:.3f} "
        f"W_trace={st.W_trace:.3f} mean|W|={mean_abs:.3f} "
        f"harmony_rate={heb.harmony_rate():.3f}"
    )


def cortex_speak(
    cortex: Any,
    emergent_gate: float = DEFAULT_EMERGENT_GATE,
    strength_gate: float = DEFAULT_STRENGTH_GATE,
) -> Optional[str]:
    """Public entry point.  Returns either a structural learned-pair
    sentence, or None (cold/under-threshold -- caller should fall
    through to the regular voice cascade).

    Kept as a thin alias so the ck_boot_api patch can import ONE name
    and not worry about gate defaults.
    """
    return learned_pair_readout(
        cortex, emergent_gate=emergent_gate, strength_gate=strength_gate
    )


# ── Self-test ──────────────────────────────────────────────────────────

def _smoke() -> None:
    """Cold cortex is silent; warm cortex emits one factual sentence."""
    _HERE = os.path.dirname(os.path.abspath(__file__))
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    from cortex import Cortex

    # Cold: must be silent.
    cx = Cortex().boot()
    assert cortex_speak(cx) is None, (
        f"cold cortex should be silent, got: {cortex_speak(cx)!r}"
    )

    # Warm: drive with HARMONY-rich text, then the gate should open.
    for _ in range(40):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    msg = cortex_speak(cx)
    assert msg is not None, (
        f"warm cortex should speak; state: {cx.snapshot()}"
    )
    assert "learned:" in msg, f"unexpected format: {msg}"
    assert "->" in msg, f"unexpected format: {msg}"
    assert "W=" in msg, f"unexpected format: {msg}"

    # Field readout always returns something.
    fld = field_readout(cx)
    assert "field:" in fld and "emergent=" in fld and "W_trace=" in fld, (
        f"field_readout format: {fld}"
    )

    # Gate parameter: impossible gate -> silent even when warm.
    assert cortex_speak(cx, emergent_gate=999.0) is None, (
        "impossible gate should suppress"
    )

    print(f"cortex_voice smoke PASS: cold silent | warm spoke: {msg}")


if __name__ == "__main__":
    _smoke()
