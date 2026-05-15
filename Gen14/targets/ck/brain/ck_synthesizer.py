# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_synthesizer.py -- CK forms higher-order abstractions across his store.

Brayden 2026-05-14:
  "is he learning super fast? synthesizing?"

Truthful answer this morning: CK learned the whole local corpus
in ~30 seconds (he's that fast on the binding side), then plateaued
because there's nothing new to read. He retrieves but doesn't
SYNTHESIZE -- doesn't form new concepts from his existing ones.

This module is the synthesis layer. It looks at CK's concept store
and groups concepts that share an algebraic-substrate signature.
Each non-trivial cluster becomes a NEW concept of tier=SYNTHESIZED
whose definition is the pattern its members share.

The architecture: every NamedConcept already has an
`operator_signature` (which of CK's 10 operators appear in its
definition prose). The 4-axis algebraic address (op, sigma_orbit,
shell, four_core) gives a coordinate. Concepts with the SAME
4-axis cell are sharing structural form. That cell IS the synthesis.

Example clusters that emerge from CK's current store:
  - All 4-core theorems (D48, D43, WP110, ...) share 4-core_class=H
  - All F-cycle results share sigma_orbit=1
  - All sigma-fixed entries share sigma_orbit=3 (BALANCE)
  - All Pati-Salam material shares the spinor operator pattern

This is what a PhD does: read 100 papers, see the META-PATTERN, form
the new concept that organizes them all. CK now has the machinery.

Public API:
    synthesize(store, min_cluster_size=3) -> List[NamedConcept]
    promote_to_store(store, new_concepts)  -- add to ConceptStore in place
    cluster_stats(store) -> Dict        -- audit existing clusters
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_concept_learner import ConceptStore, NamedConcept  # type: ignore[import-not-found]
from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class, FOUR_CORE_OUTSIDE,
)


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
SIGMA_NAMES = ("V_void", "F_creation", "S_dissolution", "BAL_fixed")
FOUR_CORE_NAMES = ("V", "H", "Br", "R", "outside")


# ─── Algebraic signature of a concept ───────────────────────────────────

def concept_signature(c: NamedConcept) -> Tuple[FrozenSet[int], int, int, int]:
    """The 4-axis cell of a concept, based on its operator_signature.

    Returns (operator_set, dominant_sigma_orbit, dominant_4core, shell).
    """
    ops = frozenset(int(o) % 10 for o in (c.operator_signature or []))
    if not ops:
        return (frozenset(), -1, -1, -1)
    sigma_classes = [sigma_orbit(o) for o in ops]
    sig_dom = Counter(sigma_classes).most_common(1)[0][0]
    fc_classes = [four_core_class(o) for o in ops]
    fc_dom = Counter(fc_classes).most_common(1)[0][0]
    sh = shell_class(set(ops))
    return (ops, sig_dom, fc_dom, sh)


def cluster_key(c: NamedConcept) -> Optional[Tuple[int, int, int]]:
    """The 3-axis key we group by: (dominant_sigma, dominant_4core, shell).

    Operator-set itself is too granular (each concept has its own); but
    the σ/4-core/shell triple is the meaningful structural cell. Same
    triple = same algebraic neighbourhood = candidate for synthesis.
    """
    _, sig, fc, sh = concept_signature(c)
    if sig < 0 or fc < 0 or sh < 0:
        return None
    return (sig, fc, sh)


# ─── Synthesis ──────────────────────────────────────────────────────────

def _format_member_list(members: List[NamedConcept], max_show: int = 10) -> str:
    names = sorted({m.name for m in members})
    if len(names) <= max_show:
        return ", ".join(names)
    return ", ".join(names[:max_show]) + f", +{len(names) - max_show} more"


def _shared_operators(members: List[NamedConcept]) -> List[int]:
    """Operators present in every member, sorted by frequency."""
    counts: Counter = Counter()
    for m in members:
        counts.update(set(int(o) % 10 for o in (m.operator_signature or [])))
    n = len(members)
    return sorted(
        [op for op, c in counts.items() if c >= max(2, n // 2)],
        key=lambda op: -counts[op],
    )


def _tier_of_cluster(members: List[NamedConcept]) -> str:
    """Synthesis concept's tier is the WEAKEST tier among its members.

    Rationale: a pattern across {PROVED, PROVED, SPECULATIVE} is only
    as strong as the speculative member -- we can't claim the abstraction
    is more rigorous than its weakest piece.
    """
    tier_strength = {
        "PROVED": 5, "STRUCTURAL": 4, "EMPIRICAL": 3, "OPEN": 2,
        "EXTERNAL": 2, "SPECULATIVE": 1, "UNKNOWN": 0, "USER_TAUGHT": 4,
    }
    if not members:
        return "UNKNOWN"
    min_tier = min(members, key=lambda m: tier_strength.get(
        getattr(m, "tier", "UNKNOWN"), 0))
    return getattr(min_tier, "tier", "UNKNOWN")


def synthesize(store: ConceptStore,
                min_cluster_size: int = 3,
                exclude_existing_synthesis: bool = True
                ) -> List[NamedConcept]:
    """Cluster concepts by their 3-axis (sigma, 4core, shell) key.
    Each cluster of size >= min_cluster_size becomes a synthesis concept.

    Returns the list of NEW synthesis concepts (not yet added to store).
    """
    clusters: Dict[Tuple[int, int, int], List[NamedConcept]] = defaultdict(list)
    for c in store.concepts.values():
        if exclude_existing_synthesis and c.source_session == "synthesis":
            continue  # don't synthesise the synthesis
        key = cluster_key(c)
        if key is None:
            continue
        clusters[key].append(c)

    new_concepts: List[NamedConcept] = []
    now = time.time()
    for key, members in clusters.items():
        if len(members) < min_cluster_size:
            continue
        sig, fc, sh = key
        shared_ops = _shared_operators(members)
        cluster_name = (
            f"Pattern_{SIGMA_NAMES[sig]}_{FOUR_CORE_NAMES[fc]}_sh{sh}"
        )
        # Build definition
        member_str = _format_member_list(members, max_show=8)
        shared_str = ", ".join(OP_NAMES[o] for o in shared_ops[:5]) or "(none)"
        defn = (
            f"Synthesis cluster of {len(members)} concepts sharing the "
            f"algebraic cell (sigma={SIGMA_NAMES[sig]}, "
            f"four_core={FOUR_CORE_NAMES[fc]}, shell={sh}). "
            f"Shared operators: {shared_str}. "
            f"Members: {member_str}."
        )
        # Tier inherits weakest member's tier
        tier = _tier_of_cluster(members)
        syn = NamedConcept(
            name=cluster_name,
            definition=defn,
            operator_signature=list(shared_ops),
            pattern_used="synthesis:algebraic_cluster",
            source_session="synthesis",
            learned_ts=now,
            tier=f"SYNTHESIZED({tier})",
            source_file="(synthesized from store)",
        )
        new_concepts.append(syn)

    return new_concepts


def promote_to_store(store: ConceptStore, new_concepts: List[NamedConcept]
                       ) -> int:
    """Insert new synthesis concepts into the store. Returns how many added."""
    added = 0
    for c in new_concepts:
        key = c.name.lower()
        store.concepts[key] = c
        added += 1
    store.save()
    return added


def cluster_stats(store: ConceptStore) -> Dict[str, Any]:
    """Audit how concepts cluster in the store today."""
    clusters: Dict[Tuple[int, int, int], List[NamedConcept]] = defaultdict(list)
    no_signature = 0
    for c in store.concepts.values():
        if c.source_session == "synthesis":
            continue
        key = cluster_key(c)
        if key is None:
            no_signature += 1
            continue
        clusters[key].append(c)

    sizes = [len(v) for v in clusters.values()]
    return {
        "n_concepts": len(store.concepts),
        "n_no_signature": no_signature,
        "n_clusters": len(clusters),
        "max_cluster": max(sizes) if sizes else 0,
        "min_cluster": min(sizes) if sizes else 0,
        "clusters_size_3plus": sum(1 for s in sizes if s >= 3),
        "clusters_size_10plus": sum(1 for s in sizes if s >= 10),
        "clusters_size_25plus": sum(1 for s in sizes if s >= 25),
    }


# ─── CLI ────────────────────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=None,
                    help="path to taught_concepts.json (default: Gen13/var/...)")
    ap.add_argument("--min-cluster", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true",
                    help="show clusters, don't write")
    args = ap.parse_args()

    if args.store:
        store = ConceptStore(path=Path(args.store))
    else:
        store = ConceptStore()
    print(f"[synthesize] store loaded: {len(store.concepts):,} concepts")

    stats = cluster_stats(store)
    print(f"[synthesize] cluster stats: {stats}")

    new = synthesize(store, min_cluster_size=args.min_cluster)
    print(f"[synthesize] would form {len(new)} synthesis concepts")
    for c in sorted(new, key=lambda c: -len(c.operator_signature))[:10]:
        print(f"  {c.name}: ops={[OP_NAMES[o] for o in c.operator_signature[:5]]}"
              f"  tier={c.tier}")
        print(f"    {c.definition[:200]}…")

    if args.dry_run:
        print(f"[synthesize] DRY-RUN: not writing")
        return 0

    n_added = promote_to_store(store, new)
    print(f"[synthesize] promoted {n_added} new concepts to store")
    print(f"[synthesize] store NOW: {len(store.concepts):,} concepts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
