"""
ck_lm/memory — CK organism memory stack

Hierarchy:
    Atom     → smallest canonical unit (single compressed event)
    Path     → directed transition between atoms under operator/lens
    Crystal  → stable reusable bundle (Path promoted when recurrence >= 3, confidence >= T*)
    MetaCrystal → experience of experience (Crystal patterns)

Routing:
    DBC27 key = "{dbc_sym}::{cl_fused}::{lens}"
    Retrieval opens local neighborhood only — not all memory at once.

Growth:
    growth(t) = weighted sum of 7 metrics
    Stage 0→4: DeepSeek dependency decreases as crystal store grows

"""
from .event_schema import Atom, Path, Crystal, MetaCrystal, T_STAR, CRYSTAL_THRESHOLD
from .dbc27 import build_key, key_neighborhood
from .atom_store import write_atom, get_atom, get_atoms_by_keys, bump_recurrence
from .crystal_store import write_crystal, get_crystals_by_keys, promote_path_to_crystal, bump_crystal
from .retrieval import retrieve, RetrievalResult, retrieval_stats
from .novelty_gate import evaluate as gate_evaluate, GateDecision, set_stage, stage_from_crystal_count
from .growth_metrics import GrowthTracker, GrowthSnapshot, compute_growth

__all__ = [
    'Atom', 'Path', 'Crystal', 'MetaCrystal', 'T_STAR', 'CRYSTAL_THRESHOLD',
    'build_key', 'key_neighborhood',
    'write_atom', 'get_atom', 'get_atoms_by_keys', 'bump_recurrence',
    'write_crystal', 'get_crystals_by_keys', 'promote_path_to_crystal', 'bump_crystal',
    'retrieve', 'RetrievalResult', 'retrieval_stats',
    'gate_evaluate', 'GateDecision', 'set_stage', 'stage_from_crystal_count',
    'GrowthTracker', 'GrowthSnapshot', 'compute_growth',
]
