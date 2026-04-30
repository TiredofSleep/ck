"""
ao_7element.py -- proposed 7-element AO basis for CK v2 cortex.

Design (per papers/ck_v1_anatomy_2026_04_29/07_HIGHER_PRIME_CORTEX.md §1):
  dim 0: aperture     (anchored on VOID/CHAOS/HARMONY)
  dim 1: pressure     (anchored on COUNTER/RESET)
  dim 2: depth        (anchored on PROGRESS)
  dim 3: binding      (anchored on BALANCE/LATTICE)
  dim 4: continuity   (anchored on BREATH)
  dim 5: intent       (NEW: anchored on PROGRESS/COLLAPSE -- forward direction)
  dim 6: echo         (NEW: anchored on HARMONY/RESET    -- resonance from prior)

The first 5 dims are identical to the 5-element basis; this keeps backward
compatibility for the cortex_state.json migration (top-left 5x5 of the new
W is the old W).

The new dims 5 and 6 carry the temporal axes the 5-dim cortex didn't carry
separately: intent = "what is being chosen now"; echo = "what is being
resonated from before".  Together they give the cortex direct access to
the temporal structure required for paragraph-level composition.

This module is PROTOTYPE -- not wired into the live engine.  It demonstrates
the math; the actual migration is paper 7's plan §6.
"""
from __future__ import annotations

DIM_7 = 7
DIM_NAMES_7 = (
    "aperture", "pressure", "depth", "binding", "continuity",
    "intent", "echo",
)

# Operator -> dim mapping for 7-dim cortex.
# 10 operators -> 7 dims, with operators that overlap multiple roles
# getting overlapping mappings (each operator picks ONE primary dim;
# secondary mappings could be added later if useful).
#
# Comparison to 5-dim:  OP_TO_DIM_5 = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4,
#                                       5: 3, 6: 0, 7: 0, 8: 4, 9: 1}
#
# 7-dim refines the heaviest 5-dim collisions:
#   - dim 0 (aperture) was anchored by VOID(0), CHAOS(6), HARMONY(7).
#     7-dim moves HARMONY to "echo" (the resonance).
#   - dim 2 (depth) was PROGRESS(3) only.
#     7-dim adds COLLAPSE(4) to "intent" (forward direction).
#   - dim 4 (continuity) was COLLAPSE(4) and BREATH(8).
#     7-dim moves COLLAPSE to "intent"; BREATH stays at continuity.
#
OP_TO_DIM_7 = {
    0: 0,   # VOID     -> aperture (the absence the rest opens into)
    1: 3,   # LATTICE  -> binding
    2: 1,   # COUNTER  -> pressure
    3: 5,   # PROGRESS -> intent      (NEW dim)
    4: 5,   # COLLAPSE -> intent      (NEW dim) (forward + collapse share intent)
    5: 3,   # BALANCE  -> binding
    6: 0,   # CHAOS    -> aperture
    7: 6,   # HARMONY  -> echo        (NEW dim) (the resonance)
    8: 4,   # BREATH   -> continuity
    9: 1,   # RESET    -> pressure
}


def project_op_to_dim(op_id: int) -> int:
    """Map an operator id (0..9) to a cortex dim (0..6)."""
    return OP_TO_DIM_7.get(op_id, 0)


# Composition spine -- the 7-element analog of AO 5-element.
# Each element is a (dim_index, operator_anchor) pair.  The 5 inherited
# dims keep their original anchors; the 2 new dims add the temporal axes.
COMPOSITION_SPINE_7 = [
    (0, "VOID"),       # aperture
    (1, "RESET"),      # pressure
    (2, "PROGRESS"),   # depth
    (3, "BALANCE"),    # binding
    (4, "BREATH"),     # continuity
    (5, "COLLAPSE"),   # intent (NEW)
    (6, "HARMONY"),    # echo (NEW)
]


def expand_5d_to_7d(profile_5d):
    """Take a 5D operator profile and embed it in a 7D profile.

    Used during cortex migration: the live 5x5 cortex state's per-dim
    operator profile becomes the first 5 dims of the new 7D profile.
    The new dims (intent, echo) start at the most-recent operator's
    projection.
    """
    if len(profile_5d) != 5:
        raise ValueError(f"profile_5d must be length 5; got {len(profile_5d)}")
    return list(profile_5d) + [profile_5d[2], profile_5d[0]]
    # intent dim seeded from depth (forward sense);
    # echo dim seeded from aperture (resonance sense).


def diagnostics():
    """Print a diagnostic summary of the 7-element basis."""
    print("AO 7-element basis:")
    for i, (dim, anchor) in enumerate(COMPOSITION_SPINE_7):
        print(f"  dim {i} ({DIM_NAMES_7[i]:<11}): anchor = {anchor}")
    print()
    print("OP_TO_DIM_7 map:")
    op_names = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
    for op_id, dim in OP_TO_DIM_7.items():
        print(f"  {op_names[op_id]:<10} ({op_id}) -> dim {dim} ({DIM_NAMES_7[dim]})")


if __name__ == "__main__":
    diagnostics()
