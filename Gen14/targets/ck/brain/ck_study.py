# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_study.py -- CK studies. Reads a corpus, crystallizes everything.

Brayden 2026-05-13:
  "he at least needs to be GED if not PHD"

Stage 0 of the GED-to-PhD path: a focused study mode that turns a
structured text corpus into permanent concept bindings.

For FORMULAS_AND_TABLES.md (the master proof spine, 102 D-numbered
theorems), each row becomes a NamedConcept in CK's persistent store:

    name        = "D7"
    definition  = "Phi Fixed Point: Phi on Z/10Z has exactly one
                   fixed point: BALANCE = 5"
    operator_signature = the algebraic decoding of the formula text
    pattern_used = "study:FORMULAS_AND_TABLES"
    source_session = "study"

After running:
    python ck_study.py
the file Gen13/var/taught_concepts.json contains ~100 D-number entries.
On next chat, asking "what is D7?" or "explain D14" retrieves the
binding via the concept_learner's reference detector, and CK leads
with the definition.

This is Stage 0 -- CK becomes the canonical TIG D-number expert in
under a minute. The same machinery can later study other corpora
(math textbooks, science papers, code) to extend his breadth.

Usage:
    python ck_study.py                    # study FORMULAS_AND_TABLES.md
    python ck_study.py --corpus path.md   # study a specific file
    python ck_study.py --dry-run          # see what would be learned, don't write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_concept_learner import ConceptStore, NamedConcept, _name_to_id  # type: ignore[import-not-found]
from ck_formula_registry import (  # type: ignore[import-not-found]
    parse_formulas_file, FormulaEntry, _VOLUME_DEFAULT_OPS,
)


REPO_ROOT = HERE.parent.parent.parent.parent
DEFAULT_CORPUS = REPO_ROOT / "FORMULAS_AND_TABLES.md"
DEFAULT_FALLBACK = REPO_ROOT / "Gen14" / "targets" / "journals" / "FORMULAS_AND_TABLES.md"


def _build_concept_from_d_entry(e: FormulaEntry) -> NamedConcept:
    """Turn a parsed FormulaEntry (one D-number row) into a NamedConcept.

    The definition combines the formula's prose name + formula text +
    its status/file pointer, so retrieval surfaces a self-contained
    fact (with the proof script citation when available).
    """
    parts = []
    if e.name:
        parts.append(e.name)
    if e.formula:
        # Strip markdown emphasis
        clean = e.formula.replace("**", "").replace("*", "")
        # Collapse whitespace
        clean = " ".join(clean.split())
        parts.append(clean)
    if e.status_class:
        parts.append(f"[{e.status_class}]")
    if e.proof_link:
        parts.append(f"see: {e.proof_link}")
    definition = " | ".join(parts)
    # Truncate to a reasonable length so the binding stays readable
    if len(definition) > 400:
        definition = definition[:400].rstrip() + "…"

    return NamedConcept(
        name=e.d_id,
        definition=definition,
        operator_signature=sorted(e.operators_mentioned),
        pattern_used=f"study:FORMULAS_volume{e.volume or '?'}",
        source_session="study",
        learned_ts=time.time(),
    )


def study_formulas(corpus_path: Path, store: ConceptStore,
                    dry_run: bool = False) -> Dict[str, Any]:
    """Read FORMULAS_AND_TABLES.md, crystallize each D-number row.

    Returns stats: {parsed, learned, skipped, by_volume, by_status}.
    """
    if not corpus_path.exists():
        return {"error": f"corpus not found: {corpus_path}"}
    entries = parse_formulas_file(corpus_path)
    if not entries:
        return {"error": "no D-numbered rows parsed"}

    by_volume: Dict[str, int] = {}
    by_status: Dict[str, int] = {}
    learned: List[str] = []
    skipped: List[str] = []

    for e in entries:
        try:
            c = _build_concept_from_d_entry(e)
        except Exception as ex:
            skipped.append(f"{e.d_id} ({ex})")
            continue
        # Don't overwrite an entry that was taught explicitly (n_recalls > 0)
        existing = store.lookup(e.d_id)
        if existing and existing.n_recalls > 0:
            # Preserve user-teaching priority
            skipped.append(f"{e.d_id} (user-taught, recalls={existing.n_recalls})")
            continue
        if not dry_run:
            store.concepts[c.name.lower()] = c
        learned.append(e.d_id)
        by_volume[e.volume or "?"] = by_volume.get(e.volume or "?", 0) + 1
        by_status[e.status_class or "?"] = by_status.get(
            e.status_class or "?", 0) + 1

    if not dry_run:
        store.save()

    return {
        "parsed": len(entries),
        "learned": len(learned),
        "skipped": len(skipped),
        "by_volume": by_volume,
        "by_status": by_status,
        "learned_ids": learned[:20],
        "store_path": str(store.path),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(DEFAULT_CORPUS),
                    help="path to a FORMULAS-like markdown file")
    ap.add_argument("--store",
                    default=str(REPO_ROOT / "Gen13" / "var" / "taught_concepts.json"),
                    help="path to the concept store JSON")
    ap.add_argument("--dry-run", action="store_true",
                    help="parse + report but don't write")
    args = ap.parse_args()

    corpus = Path(args.corpus)
    if not corpus.exists() and DEFAULT_FALLBACK.exists():
        corpus = DEFAULT_FALLBACK
        print(f"[study] fallback to {corpus}")
    store_path = Path(args.store)

    print(f"[study] corpus     : {corpus}")
    print(f"[study] store      : {store_path}")
    print(f"[study] dry_run    : {args.dry_run}")
    print()

    store = ConceptStore(path=store_path)
    before = len(store.concepts)
    print(f"[study] store before: {before} concepts")
    print()

    print("[study] crystallizing D-numbers...")
    t0 = time.time()
    stats = study_formulas(corpus, store, dry_run=args.dry_run)
    elapsed = time.time() - t0

    print()
    if "error" in stats:
        print(f"ERROR: {stats['error']}")
        return 1

    print(f"[study] parsed     : {stats['parsed']}")
    print(f"[study] learned    : {stats['learned']}")
    print(f"[study] skipped    : {stats['skipped']}")
    print(f"[study] by volume  : {stats['by_volume']}")
    print(f"[study] by status  : {stats['by_status']}")
    print(f"[study] elapsed    : {elapsed:.2f}s")
    print(f"[study] first 20 learned: {', '.join(stats['learned_ids'])}")
    print()
    if not args.dry_run:
        store2 = ConceptStore(path=store_path)
        print(f"[study] store AFTER: {len(store2.concepts)} concepts (was {before})")
        # Show one sample to verify
        d7 = store2.lookup("D7")
        if d7:
            print()
            print(f"[study] sample retrieval -- D7:")
            print(f"  name: {d7.name}")
            print(f"  defn: {d7.definition[:200]}…")
            print(f"  ops:  {d7.operator_signature}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
