"""Derived tables: HARMONY_44, Cycle A 36, lens disagreement 71/72/73, Skeleton 22."""

from .harmony_44 import HARMONY_44, harmony_44_cells, harmony_44_summary
from .cycle_a_36 import CYCLE_A_36, cycle_a_36_cells, cycle_a_36_summary
from .lens_disagreement_71 import (
    DISAGREE_71, BEING_SHELL_72_VIA_HARMONY_MINUS_1, TSML_HARMONY_73,
    disagreement_cells, being_shell_72_summary,
    BEING_SHELL_72,                  # alias for backward compat
    being_shell_72_cells,
)
from .skeleton_22 import SKELETON_22, skeleton_22_cells, skeleton_22_summary

__all__ = [
    "HARMONY_44", "harmony_44_cells", "harmony_44_summary",
    "CYCLE_A_36", "cycle_a_36_cells", "cycle_a_36_summary",
    "DISAGREE_71", "BEING_SHELL_72_VIA_HARMONY_MINUS_1", "TSML_HARMONY_73",
    "disagreement_cells", "being_shell_72_summary",
    "BEING_SHELL_72", "being_shell_72_cells",
    "SKELETON_22", "skeleton_22_cells", "skeleton_22_summary",
]
