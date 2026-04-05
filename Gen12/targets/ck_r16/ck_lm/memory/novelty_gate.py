"""
novelty_gate.py — CK Memory: Novelty gate for DeepSeek escalation

The novelty gate is the gatekeeper between CK's own memory and external reasoning.

A query is NOVEL when:
    - No crystal was found (retrieval.crystal_hit = False)
    - Top confidence < NOVELTY_THRESHOLD (0.3)
    - The generator set has no overlap with known generators

A query is KNOWN when:
    - At least one crystal was found with confidence >= T* (5/7)
    - Path reuse rate is high

Stage progression (DeepSeek reduction):
    Stage 0: DeepSeek always called (bootstrap)
    Stage 1: Retrieval-first; DeepSeek only if no crystal
    Stage 2: Novelty-gated; DeepSeek only if gate fires
    Stage 3: Policy reuse dominant; DeepSeek rarely
    Stage 4: DeepSeek fallback only for truly novel/high-uncertainty

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import time

from .event_schema import T_STAR
from .retrieval import RetrievalResult

# Gate thresholds
NOVELTY_THRESHOLD = 0.3
CONFIDENCE_FLOOR  = T_STAR          # crystals below this are unreliable
GENERATOR_OVERLAP_MIN = 0.2         # min fraction of generators that must match

# Current stage (0-4). Move through stages as crystal count grows.
# Stage is tracked externally in growth_metrics; gate reads it here.
_current_stage: int = 1             # default: retrieval-first


@dataclass
class GateDecision:
    """Decision from the novelty gate."""
    escalate: bool                  # True → call DeepSeek
    reason: str                     # why
    stage: int                      # which stage decision was made in
    confidence: float               # top confidence at decision time
    crystal_count: int              # crystals found
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


def set_stage(stage: int) -> None:
    """Update the gate's operating stage (0-4)."""
    global _current_stage
    _current_stage = max(0, min(4, stage))


def evaluate(
    retrieval: RetrievalResult,
    query_generators: list[str],
    known_generators: list[str],
    stage: Optional[int] = None,
) -> GateDecision:
    """Evaluate whether to escalate to DeepSeek.

    Args:
        retrieval:        result from retrieval.retrieve()
        query_generators: generators extracted from this query
        known_generators: all generators CK has seen before
        stage:            override operating stage (else use _current_stage)

    Returns:
        GateDecision with escalate flag + reason
    """
    s = stage if stage is not None else _current_stage
    conf = retrieval.top_confidence
    n_crystals = len(retrieval.crystals)

    # Stage 0: always escalate (bootstrap)
    if s == 0:
        return GateDecision(
            escalate=True, reason='stage0_bootstrap',
            stage=s, confidence=conf, crystal_count=n_crystals
        )

    # Stage 4: only escalate if truly no memory + low confidence
    if s == 4:
        if not retrieval.crystal_hit and conf < NOVELTY_THRESHOLD:
            return GateDecision(
                escalate=True, reason='stage4_genuine_novelty',
                stage=s, confidence=conf, crystal_count=n_crystals
            )
        return GateDecision(
            escalate=False, reason='stage4_internal_sufficient',
            stage=s, confidence=conf, crystal_count=n_crystals
        )

    # Stage 1-3: retrieval-first gating
    # Rule 1: crystal hit with high confidence → internal
    if retrieval.crystal_hit and conf >= CONFIDENCE_FLOOR:
        return GateDecision(
            escalate=False, reason='crystal_hit_high_confidence',
            stage=s, confidence=conf, crystal_count=n_crystals
        )

    # Rule 2: no crystal, no atoms, stage 1+ → escalate
    if not retrieval.crystal_hit and not retrieval.atoms:
        return GateDecision(
            escalate=True, reason='no_memory_found',
            stage=s, confidence=conf, crystal_count=n_crystals
        )

    # Rule 3: generator overlap check (stage 2+)
    if s >= 2 and query_generators and known_generators:
        known_set = set(known_generators)
        overlap = sum(1 for g in query_generators if g in known_set)
        overlap_frac = overlap / len(query_generators) if query_generators else 0
        if overlap_frac < GENERATOR_OVERLAP_MIN:
            return GateDecision(
                escalate=True, reason=f'low_generator_overlap_{overlap_frac:.2f}',
                stage=s, confidence=conf, crystal_count=n_crystals
            )

    # Rule 4: confidence too low even with atoms
    if conf < NOVELTY_THRESHOLD:
        if s <= 2:
            return GateDecision(
                escalate=True, reason=f'low_confidence_{conf:.3f}',
                stage=s, confidence=conf, crystal_count=n_crystals
            )

    # Default: use internal memory
    return GateDecision(
        escalate=False, reason='internal_sufficient',
        stage=s, confidence=conf, crystal_count=n_crystals
    )


def stage_from_crystal_count(n_crystals: int) -> int:
    """Suggest operating stage based on crystal store size.

    Stage migration thresholds:
        0 →  1: crystal_count >= 10    (retrieval-first possible)
        1 →  2: crystal_count >= 100   (novelty gate reliable)
        2 →  3: crystal_count >= 1000  (policy reuse available)
        3 →  4: crystal_count >= 5000  (full autonomy)
    """
    if n_crystals < 10:
        return 0
    if n_crystals < 100:
        return 1
    if n_crystals < 1000:
        return 2
    if n_crystals < 5000:
        return 3
    return 4
