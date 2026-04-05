"""
event_schema.py — CK Memory: Atom / Path / Crystal dataclasses

Memory is structured as a hierarchy:
  Atom    = smallest canonical unit (single observed event)
  Path    = directed transition sequence between atoms under a lens/operator
  Crystal = stable, reusable bundle of atoms + paths with policy meaning

The information lives in the PATHWAY, not in the blob.
A crystal is a path that has been traversed enough times to be trusted.

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time

# ── Privacy tags ─────────────────────────────────────────────────────────────
PRIVATE   = 'private'    # user words, names, session state — never shared
SHARED    = 'shared'     # force signatures, abstract transitions — shareable
ABSTRACT  = 'abstract'   # abstracted from private (identifying info removed)

# ── Modality tags ─────────────────────────────────────────────────────────────
TEXT      = 'text'
SCREEN    = 'screen'
TELEMETRY = 'telemetry'
INPUT     = 'input'
INTERNAL  = 'internal'   # CK's own output / heartbeat


@dataclass
class Atom:
    """Smallest canonical memory unit.

    An Atom is a single observed event compressed into CK's operator space.
    It carries both the raw reference and the CK-native encoding.

    Fields:
        id              — unique identifier (str uuid4)
        timestamp       — unix float when atom was created
        modality        — TEXT / SCREEN / TELEMETRY / INPUT / INTERNAL
        raw_ref         — pointer to raw buffer entry (not stored here)
        generators      — list of generator strings extracted from event
        force_vector    — 5D [aperture, pressure, depth, binding, continuity]
        operator        — dominant CK operator (0-9)
        lens            — 'STRUCTURE' or 'FLOW'
        privacy         — PRIVATE / SHARED / ABSTRACT
        recurrence      — how many times this atom has been seen
        confidence      — [0,1] from R8 coherence; T*=5/7 = verified
        parent_paths    — list of Path IDs that include this atom
        compression_score — [0,1] how well this atom compresses its raw event
    """
    id: str
    timestamp: float
    modality: str
    raw_ref: Optional[str]       # nullable — may be purged after compression
    generators: list[str]
    force_vector: list[float]    # always 5D
    operator: int                # 0..9
    lens: str                    # STRUCTURE | FLOW
    privacy: str                 # PRIVATE | SHARED | ABSTRACT
    recurrence: int = 1
    confidence: float = 0.5
    parent_paths: list[str] = field(default_factory=list)
    compression_score: float = 0.0


@dataclass
class Path:
    """Directed transition sequence between atoms under a lens/operator state.

    The PATH IS the information. The sequence of operators and lenses taken
    to traverse from one atom to another carries structure that the atoms
    themselves do not contain individually.

    Promotion to Crystal: when recurrence >= CRYSTAL_THRESHOLD and
    confidence >= T* (5/7 ≈ 0.714), a Path becomes a Crystal.

    Fields:
        id              — unique identifier
        atom_ids        — ordered list of Atom IDs in traversal order
        timestamp_start — when path was first traversed
        timestamp_end   — when path was last traversed
        operators       — CK operators at each step (len = len(atom_ids)-1)
        lens_states     — lens at each step
        force_deltas    — 5D delta vectors at each step
        privacy         — coarsest privacy level of constituent atoms
        recurrence      — traversal count
        confidence      — mean confidence across atoms in path
        policy_ref      — optional: pointer to action policy derived from path
        child_paths     — paths that extend this one
        parent_paths    — paths this one extends
        crystal_id      — set when promoted to Crystal (else None)
        compression_score — [0,1] how well path compresses into Crystal
    """
    id: str
    atom_ids: list[str]
    timestamp_start: float
    timestamp_end: float
    operators: list[int]
    lens_states: list[str]
    force_deltas: list[list[float]]   # one 5D delta per step
    privacy: str
    recurrence: int = 1
    confidence: float = 0.5
    policy_ref: Optional[str] = None
    child_paths: list[str] = field(default_factory=list)
    parent_paths: list[str] = field(default_factory=list)
    crystal_id: Optional[str] = None
    compression_score: float = 0.0

    @property
    def length(self) -> int:
        return len(self.atom_ids)


# Threshold: path becomes Crystal when recurrence hits this many traversals
# AND confidence >= T* = 5/7
CRYSTAL_THRESHOLD = 3
T_STAR = 5 / 7  # 0.714285...


@dataclass
class Crystal:
    """Stable, reusable bundle of atoms + paths with policy meaning.

    A Crystal is a path that has been verified enough times to trust.
    It can be recalled as a unit — bypassing raw drill-down entirely.

    The Crystal is the unit that CK's memory IS built on.
    Unlike atoms (events) and paths (transitions), crystals are the
    compressed, distilled experience that CK can act from directly.

    Promotion from Path: recurrence >= CRYSTAL_THRESHOLD AND confidence >= T*

    Fields:
        id              — unique identifier
        path_ids        — ordered list of Path IDs compressed into crystal
        created_at      — unix float
        last_used       — unix float
        generators      — union of generators from constituent paths
        centroid_force  — mean 5D force vector across all atoms
        dominant_op     — most common operator in path sequence
        dominant_lens   — dominant lens (STRUCTURE or FLOW)
        privacy         — coarsest privacy of constituent paths
        recurrence      — how many times crystal has been retrieved + used
        confidence      — [0,1] R8-aligned; T* floor enforced at promotion
        policy_summary  — brief text summary of what action this crystal drives
        meta_crystal_id — set when this crystal is part of a MetaCrystal
        raw_refs        — list of raw buffer refs (may be purged)
        compression_ratio — len(raw_refs) / len(atom_ids_total)
        dbc27_key       — DBC27 routing key for lattice retrieval
    """
    id: str
    path_ids: list[str]
    created_at: float
    last_used: float
    generators: list[str]
    centroid_force: list[float]   # 5D
    dominant_op: int
    dominant_lens: str
    privacy: str
    recurrence: int = 1
    confidence: float = T_STAR    # floor at T* on promotion
    policy_summary: str = ''
    meta_crystal_id: Optional[str] = None
    raw_refs: list[str] = field(default_factory=list)
    compression_ratio: float = 1.0
    dbc27_key: str = ''

    def is_mature(self) -> bool:
        """True when crystal has been used >= CRYSTAL_THRESHOLD times."""
        return self.recurrence >= CRYSTAL_THRESHOLD


@dataclass
class MetaCrystal:
    """Experience of experience — a crystal built from crystals.

    MetaCrystals encode how CK handled situations, not just what happened.
    They hold: successful retrieval patterns, failed retrieval patterns,
    useful LoRA behaviors, UI navigation habits, recovery procedures.

    Fields:
        id              — unique identifier
        crystal_ids     — constituent Crystal IDs
        created_at      — unix float
        last_used       — unix float
        pattern_type    — 'retrieval_success' | 'retrieval_failure' |
                          'lora_behavior' | 'ui_habit' | 'recovery' |
                          'escalation_trigger' | 'user_preference'
        confidence      — [0,1] across constituent crystals
        summary         — what this meta-pattern represents
        outcome         — what happened when pattern was used
        reuse_count     — how many times this meta pattern has fired
    """
    id: str
    crystal_ids: list[str]
    created_at: float
    last_used: float
    pattern_type: str
    confidence: float
    summary: str
    outcome: str = ''
    reuse_count: int = 0
