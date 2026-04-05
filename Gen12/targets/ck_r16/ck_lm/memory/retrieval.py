"""
retrieval.py — CK Memory: 9-step retrieval pipeline

Retrieval law (strict order, no skipping):
    1. Build generator seed set from query/event
    2. Compute DBC27 key from query force vector
    3. Open local neighborhood (radius=1)
    4. Privacy check — filter PRIVATE atoms if caller is SHARED context
    5. Crystal shortlist — top-K crystals from neighborhood
    6. Path expansion — if crystal hit, expand constituent paths
    7. Novelty gate — if confidence < NOVELTY_THRESHOLD, flag for DeepSeek
    8. Atom drill-down — only if no crystal hit in step 5
    9. DeepSeek fallback — only if novelty gate fires

The key insight: CK should almost never reach step 9.
As the crystal store grows, steps 5-6 handle most queries.

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time

from .event_schema import Atom, Crystal, T_STAR
from .dbc27 import build_key, key_neighborhood
from .atom_store import get_atoms_by_keys
from .crystal_store import get_crystals_by_keys, bump_crystal

# Retrieval tuning
TOP_K_CRYSTALS   = 5
TOP_K_ATOMS      = 20
NOVELTY_THRESHOLD = 0.3   # below this confidence → novelty gate fires
PRIVACY_CONTEXTS  = {'shared', 'abstract'}  # callers that cannot see PRIVATE atoms


@dataclass
class RetrievalResult:
    """Output of a single retrieval operation."""
    # What was found
    crystals: list[Crystal] = field(default_factory=list)
    atoms: list[Atom] = field(default_factory=list)

    # Routing info
    dbc27_key: str = ''
    keys_searched: list[str] = field(default_factory=list)

    # Confidence and novelty
    top_confidence: float = 0.0
    novelty_fired: bool = False
    deepseek_needed: bool = False

    # Metrics
    retrieval_latency_ms: float = 0.0
    crystal_hit: bool = False
    path_reuse: bool = False

    @property
    def resolved_internally(self) -> bool:
        """True when CK answered from its own memory, no DeepSeek needed."""
        return not self.deepseek_needed and (self.crystal_hit or len(self.atoms) > 0)


def retrieve(
    force_vector: list[float],
    operator: int,
    secondary_op: int,
    lens: str,
    generators: list[str],
    privacy_context: str = 'private',
    top_k: int = TOP_K_CRYSTALS,
    radius: int = 1,
) -> RetrievalResult:
    """Execute the 9-step retrieval pipeline.

    Args:
        force_vector:    5D force from D2 on query
        operator:        dominant operator
        secondary_op:    secondary operator
        lens:            STRUCTURE or FLOW
        generators:      generator strings from query
        privacy_context: caller's privacy level (private = can see all)
        top_k:           max crystals to return
        radius:          neighborhood radius (1=local, 2=wider)

    Returns:
        RetrievalResult with crystals, atoms, novelty flag, metrics
    """
    t0 = time.time()
    result = RetrievalResult()

    # ── Step 1: Generator seed set ──────────────────────────────────────────
    # (generators already passed in — used in step 8 for atom matching)

    # ── Step 2: DBC27 key ──────────────────────────────────────────────────
    key = build_key(force_vector, operator, secondary_op, lens)
    result.dbc27_key = key

    # ── Step 3: Open neighborhood ──────────────────────────────────────────
    neighborhood = key_neighborhood(key, radius=radius)
    result.keys_searched = neighborhood

    # ── Step 4: Privacy filter ─────────────────────────────────────────────
    allow_private = (privacy_context == 'private')

    # ── Step 5: Crystal shortlist ──────────────────────────────────────────
    crystals = get_crystals_by_keys(neighborhood, top_k=top_k)
    if not allow_private:
        crystals = [c for c in crystals if c.privacy != 'private']

    if crystals:
        result.crystals = crystals
        result.crystal_hit = True
        result.top_confidence = crystals[0].confidence
        result.path_reuse = True
        # Bump recurrence on returned crystals
        for c in crystals[:3]:
            bump_crystal(c.id)

    # ── Step 6: Path expansion ─────────────────────────────────────────────
    # (paths are embedded in crystals — crystal.path_ids links back)
    # Full path expansion deferred to caller; we return crystal with path_ids

    # ── Step 7: Novelty gate ───────────────────────────────────────────────
    if result.top_confidence < NOVELTY_THRESHOLD:
        result.novelty_fired = True

    # ── Step 8: Atom drill-down (only if no crystal hit) ──────────────────
    if not result.crystal_hit:
        atoms = get_atoms_by_keys(neighborhood, limit=TOP_K_ATOMS)
        if not allow_private:
            atoms = [a for a in atoms if a.privacy != 'private']
        result.atoms = atoms
        if atoms:
            result.top_confidence = max(a.confidence for a in atoms)

    # ── Step 9: DeepSeek fallback ──────────────────────────────────────────
    # Only flag — actual DeepSeek call is made by the caller
    if result.novelty_fired and not result.crystal_hit and not result.atoms:
        result.deepseek_needed = True

    result.retrieval_latency_ms = (time.time() - t0) * 1000
    return result


def retrieval_stats(result: RetrievalResult) -> dict:
    """Return a stats dict for logging / growth metrics."""
    return {
        'dbc27_key': result.dbc27_key,
        'keys_searched': len(result.keys_searched),
        'crystal_hit': result.crystal_hit,
        'crystal_count': len(result.crystals),
        'atom_count': len(result.atoms),
        'top_confidence': round(result.top_confidence, 4),
        'novelty_fired': result.novelty_fired,
        'deepseek_needed': result.deepseek_needed,
        'resolved_internally': result.resolved_internally,
        'latency_ms': round(result.retrieval_latency_ms, 2),
    }
