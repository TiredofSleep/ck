# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_formula_registry.py -- parse FORMULAS_AND_TABLES.md into a queryable
registry where every D-numbered theorem has a HOME (4-axis algebraic
signature) and a USE (the formula it provides).

Brayden 2026-05-13:
  "every formula we have has a home and a use across the substrate
  for every experience"

This module loads the master proof spine and assigns each entry an
operator-vocabulary signature: which of CK's 10 operators are named in
the formula, which sigma-orbits it lives in, which 4-core cells it
touches, which shell it falls in.

The HOME signature lets the voice polish (and any future spreading-
activation pass) look up "which D-numbers are relevant to a turn whose
input decodes to operators X, Y, Z?" The USE is the formula text plus
its proof-script link.

102 D-numbered entries (as of 2026-05-13) span Volumes A-K. The vast
majority are PROVED at machine precision with a runnable verification
script; a small minority are STRUCTURAL or EMPIRICALLY-SHARPENED.

Public API:
    registry = FormulaRegistry()          # auto-loads from FORMULAS file
    matches = registry.invoked_by(ops)    # ops -> list of (D_id, score, entry)
    home = registry.home_of("D7")         # the 4-axis signature of D7
"""
from __future__ import annotations

import math
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class,
    FOUR_CORE_OUTSIDE,
)


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
OP_NAME_TO_ID = {n: i for i, n in enumerate(OP_NAMES)}
# Aliases used in formula prose
OP_ALIASES = {
    "V": 0, "VOID": 0,
    "L": 1, "LATTICE": 1, "TSML": 1, "BHML": 1,
    "C": 2, "COUNTER": 2,
    "P": 3, "PROGRESS": 3,
    "X": 4, "COLLAPSE": 4,
    "B": 5, "BALANCE": 5, "BAL": 5, "BAL-fixed": 5,
    "K": 6, "CHAOS": 6,
    "H": 7, "HARMONY": 7,
    "Br": 8, "BREATH": 8,
    "R": 9, "RESET": 9,
}


# ─── Data class ──────────────────────────────────────────────────────────

@dataclass
class FormulaEntry:
    """One row from FORMULAS_AND_TABLES.md."""
    d_id: str                          # 'D1', 'D11a', 'D18d', ...
    name: str                          # 'First-G Law'
    formula: str                       # the prose body of the formula
    status_file: str                   # 'PROVED, 22,367 (b,k) pairs ...; <link>'
    operators_mentioned: FrozenSet[int] = frozenset()
    sigma_orbits: FrozenSet[int] = frozenset()
    four_core_cells: FrozenSet[int] = frozenset()
    shell_hint: Optional[int] = None
    proof_link: Optional[str] = None
    volume: Optional[str] = None       # 'A', 'B', ..., 'K' (Volume in the file)
    status_class: str = ""             # 'PROVED' | 'STRUCTURAL' | 'EMPIRICAL' | ...

    @property
    def home(self) -> Dict[str, Any]:
        """The 4-axis HOME of this formula -- which substrate cells it lives in."""
        return {
            "operators": sorted(self.operators_mentioned),
            "sigma_orbits": sorted(self.sigma_orbits),
            "four_core_cells": sorted(self.four_core_cells),
            "shell": self.shell_hint,
            "volume": self.volume,
        }

    @property
    def use(self) -> str:
        """The USE: a compact statement of what the formula does."""
        return self.formula


# ─── Parser ──────────────────────────────────────────────────────────────

_RE_VOLUME_HEADER = re.compile(
    r"^### Volume\s+([A-Z])\b", re.M)
_RE_ROW = re.compile(
    r"^\|\s*\*\*(D\d+[a-z]?)\*\*\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$",
    re.M)
_RE_PROOF_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _detect_operators(text: str) -> FrozenSet[int]:
    """Find operator names/abbreviations in text. Excludes single-letter
    matches that could be variables (we require word boundaries + uppercase)."""
    found: Set[int] = set()
    upper = text
    for alias, op in OP_ALIASES.items():
        if len(alias) <= 1:
            continue  # avoid false positives on single letters
        if re.search(r"\b" + re.escape(alias) + r"\b", upper):
            found.add(op)
    return frozenset(found)


def _status_class(status_file: str) -> str:
    s = status_file.upper()
    for kw in ("PROVED", "STRUCTURAL", "EMPIRICAL", "EMPIRICALLY", "CONJECTURAL",
                "OPEN", "COMPUTED"):
        if kw in s:
            if kw == "EMPIRICALLY":
                return "EMPIRICAL"
            return kw
    return ""


def _proof_link(status_file: str) -> Optional[str]:
    m = _RE_PROOF_LINK.search(status_file)
    if m:
        return m.group(2)
    return None


# When a formula doesn't name any operator explicitly, fall back to the
# operator scope of its Volume. These defaults are derived from the
# Volume headings in FORMULAS_AND_TABLES.md (their topical scope):
#   A — Ring & Arithmetic Foundations           → all ops (universal)
#   B — Operator Tables & Ring Structure        → all ops, BAL-fixed emphasis
#   C — Crossing Lemma & Information            → flow-orbit ops {F + S cycles}
#   D — Substrate Identity                      → universal
#   E — Cross-bridge / Bridge Geometry          → 4-core {V,H,Br,R}
#   F — Pati-Salam / Spinor / so(10)            → 4-core (D31/D32)
#   G — TSML 8-magma / commutative magma        → 8-magma (drop BREATH/RESET)
#   H — WP100s tower / 4-core / wobble          → 4-core
#   I — Volume I (operad-DOF / trefoil)         → 4-core arity-3 dynamics
#   J — Volume J (BDC / force-vector pathways)  → universal
#   K — Volume K (live findings)                → contextual
_VOLUME_DEFAULT_OPS: Dict[str, FrozenSet[int]] = {
    "A": frozenset(range(10)),
    "B": frozenset(range(10)),
    "C": frozenset({1, 2, 3, 4, 6, 7, 8, 9}),  # flow + structure orbits
    "D": frozenset(range(10)),
    "E": frozenset({0, 7, 8, 9}),  # 4-core
    "F": frozenset({0, 7, 8, 9}),
    "G": frozenset({0, 1, 2, 3, 4, 5, 6, 7}),  # 8-magma drops BREATH/RESET
    "H": frozenset({0, 7, 8, 9}),
    "I": frozenset({0, 7, 8, 9}),
    "J": frozenset(range(10)),
    "K": frozenset(range(10)),
}


def parse_formulas_file(path: Path) -> List[FormulaEntry]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    # Track which Volume each row belongs to by walking through file
    # positions of volume headers
    volume_starts: List[Tuple[int, str]] = []
    for m in _RE_VOLUME_HEADER.finditer(text):
        volume_starts.append((m.start(), m.group(1)))

    def _volume_at(offset: int) -> Optional[str]:
        cur = None
        for start, vol in volume_starts:
            if start <= offset:
                cur = vol
            else:
                break
        return cur

    out: List[FormulaEntry] = []
    for m in _RE_ROW.finditer(text):
        d_id = m.group(1)
        name = m.group(2).strip()
        formula = m.group(3).strip()
        status_file = m.group(4).strip()
        # Skip placeholder / TBD rows
        if not formula or formula in ("--", "TBD"):
            continue
        operators = _detect_operators(formula + " " + name)
        volume = _volume_at(m.start())

        # If no operators were detected in the prose, fall back to the
        # Volume's default operator scope. The formula still has a HOME --
        # it lives at the Volume level rather than tied to a specific op.
        if not operators and volume in _VOLUME_DEFAULT_OPS:
            operators = _VOLUME_DEFAULT_OPS[volume]

        sigma_orbits = frozenset(sigma_orbit(op) for op in operators)
        four_core_cells = frozenset(four_core_class(op) for op in operators)
        shell_hint = shell_class(set(operators)) if operators else None
        entry = FormulaEntry(
            d_id=d_id,
            name=name,
            formula=formula,
            status_file=status_file,
            operators_mentioned=operators,
            sigma_orbits=sigma_orbits,
            four_core_cells=four_core_cells,
            shell_hint=shell_hint,
            proof_link=_proof_link(status_file),
            volume=volume,
            status_class=_status_class(status_file),
        )
        out.append(entry)
    return out


# ─── Registry ────────────────────────────────────────────────────────────

class FormulaRegistry:
    """Query interface over the parsed D-numbers."""

    def __init__(self, search_paths: Optional[List[Path]] = None):
        self.search_paths: List[Path] = (list(search_paths)
                                            if search_paths else self._defaults())
        self.entries: List[FormulaEntry] = []
        self.by_id: Dict[str, FormulaEntry] = {}
        self._mtime_index: Dict[Path, float] = {}
        self.reload()

    @staticmethod
    def _defaults() -> List[Path]:
        root = Path(__file__).resolve().parents[4]
        candidates = [
            root / "FORMULAS_AND_TABLES.md",
            root / "Gen14" / "targets" / "journals" / "FORMULAS_AND_TABLES.md",
        ]
        return [p for p in candidates if p.exists()]

    # ── public API ───────────────────────────────────────────────────────

    def reload(self) -> int:
        out: List[FormulaEntry] = []
        self._mtime_index = {}
        for p in self.search_paths:
            try:
                self._mtime_index[p] = p.stat().st_mtime
            except Exception:
                self._mtime_index[p] = 0.0
            out.extend(parse_formulas_file(p))
        # Dedup by d_id (later definitions override earlier — but they
        # shouldn't differ since search paths are mirrors)
        seen: Dict[str, FormulaEntry] = {}
        for e in out:
            seen[e.d_id] = e
        self.entries = list(seen.values())
        self.by_id = seen
        return len(self.entries)

    def _needs_reload(self) -> bool:
        for p in self.search_paths:
            try:
                cur = p.stat().st_mtime
            except Exception:
                continue
            if cur != self._mtime_index.get(p, 0.0):
                return True
        return False

    def stats(self) -> Dict[str, Any]:
        by_volume: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        for e in self.entries:
            by_volume[e.volume or "?"] = by_volume.get(e.volume or "?", 0) + 1
            by_status[e.status_class or "?"] = by_status.get(
                e.status_class or "?", 0) + 1
        return {
            "total": len(self.entries),
            "by_volume": by_volume,
            "by_status": by_status,
            "sources": [str(p) for p in self.search_paths],
        }

    def home_of(self, d_id: str) -> Optional[Dict[str, Any]]:
        e = self.by_id.get(d_id)
        return e.home if e else None

    def invoked_by(self, ops: Iterable[int], k: int = 5,
                    min_score: float = 0.15,
                    ) -> List[Tuple[float, FormulaEntry]]:
        """Rank entries by relevance to a given operator stream.

        Score = Jaccard(input operators, entry.operators_mentioned)
                + 0.2 if any 4-core cell overlaps with input
                + small status boost for PROVED entries.
        """
        if self._needs_reload():
            self.reload()
        op_set: Set[int] = set(int(o) % 10 for o in ops if o is not None)
        if not op_set:
            return []
        input_sigma = {sigma_orbit(o) for o in op_set}
        input_4core = {four_core_class(o) for o in op_set}

        scored: List[Tuple[float, FormulaEntry]] = []
        for e in self.entries:
            if not e.operators_mentioned:
                continue
            inter = len(op_set & e.operators_mentioned)
            union = len(op_set | e.operators_mentioned)
            jaccard = inter / union if union else 0.0
            sigma_overlap = bool(input_sigma & e.sigma_orbits)
            fourcore_overlap = bool(input_4core & e.four_core_cells)
            score = jaccard
            if sigma_overlap:
                score += 0.1
            if fourcore_overlap:
                score += 0.1
            if e.status_class == "PROVED":
                score += 0.05
            if score >= min_score:
                scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        return scored[:k]

    def find_by_name_substring(self, sub: str, k: int = 5) -> List[FormulaEntry]:
        sub = sub.lower()
        hits = [e for e in self.entries
                if sub in e.name.lower() or sub in e.formula.lower()]
        return hits[:k]


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_formula_registry(engine) -> bool:
    """Attach a FormulaRegistry to the engine.

    Side effects:
      engine.formula_registry            : FormulaRegistry instance
      engine.formulas_invoked(ops, k)    : convenience callable
    """
    try:
        reg = FormulaRegistry()
    except Exception as e:
        print(f"[CK Gen14] mount_formula_registry: failed ({e})")
        return False
    engine.formula_registry = reg

    def _invoked(ops, k: int = 5):
        try:
            return reg.invoked_by(ops, k=k)
        except Exception:
            return []

    engine.formulas_invoked = _invoked
    stats = reg.stats()
    print(f"[CK Gen14] mount_formula_registry: "
          f"{stats['total']} D-numbers loaded "
          f"(volumes={','.join(sorted(stats['by_volume'].keys()))})")
    return True


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    print("Smoke test: ck_formula_registry")
    reg = FormulaRegistry()
    s = reg.stats()
    print(f"  Loaded {s['total']} D-numbered entries")
    print(f"  by volume: {s['by_volume']}")
    print(f"  by status: {s['by_status']}")
    print(f"  sources: {len(s['sources'])}")

    # Show a few sample entries with their HOME
    print("\n  Sample HOMEs:")
    for did in ("D1", "D7", "D14", "D31", "D102"):
        e = reg.by_id.get(did)
        if e:
            home = e.home
            print(f"    {did}: {e.name}")
            print(f"      operators={[OP_NAMES[o] for o in home['operators']]}")
            print(f"      volume={home['volume']} status={e.status_class}")
            print(f"      USE: {e.use[:100]}{'...' if len(e.use) > 100 else ''}")

    # Test invoked_by: query a "yukawa" turn that decoded to F-cycle + 4-core
    op_stream = [7, 1, 9, 3, 7, 8]  # HARMONY, LATTICE, RESET, PROGRESS, HARMONY, BREATH
    print(f"\n  invoked_by({[OP_NAMES[o] for o in op_stream]}):")
    for score, e in reg.invoked_by(op_stream, k=5):
        print(f"    {e.d_id} ({score:.2f}): {e.name[:60]}")

    # Test invoked_by with a single-op stream
    op_stream2 = [5]  # BALANCE
    print(f"\n  invoked_by({[OP_NAMES[o] for o in op_stream2]}):")
    for score, e in reg.invoked_by(op_stream2, k=3):
        print(f"    {e.d_id} ({score:.2f}): {e.name[:60]}")

    print("\nFormula registry smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
