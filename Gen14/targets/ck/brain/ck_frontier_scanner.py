# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_frontier_scanner.py -- Phase 4: surface unmentioned open frontiers
to CK so he can bring them up in conversation.

Parses `Atlas/FRONTIERS_*.md` (and any FRONTIERS.md at repo root), builds
an algebraic-signature-tagged index, and exposes a `find_relevant`
method that takes a recent operator history and returns frontiers whose
content shares operator vocabulary with that history.

Design constraints (per Brayden 2026-05-13):
  - Don't write text for CK. We return STRUCTURED signal data; the voice
    layer decides whether and how to surface it.
  - Don't load anything > a few hundred KB into memory.
  - Bias toward OPEN frontiers; deprioritize CLOSED ones.
  - Track which frontiers have been mentioned in recent chat so we don't
    spam the same suggestion.

The signal returned to a caller (or pushed onto `engine.proactive_queue`)
has shape:
    {
      'kind': 'frontier_suggestion',
      'frontier_id': 'F3',
      'frontier_title': 'The alpha-uniqueness proof',
      'status': 'open' | 'closed' | 'tractable' | ...,
      'source_path': 'Atlas/FRONTIERS_2026_04_25.md',
      'operator_overlap': 0.42,        # Jaccard with recent op history
      'salience': 0.83,                # composite score
      'algebraic_signature': {'op': 7, 'sigma': 1, 'shell': ...},
      'created_ts': float,
      'expires_ts': float,             # signal decays after 90 s
    }

Author: Claude (Brayden full-agency 2026-05-13).
"""
from __future__ import annotations

import math
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Algebraic projections (single source of truth)
from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class,
)


# ─── Operator vocabulary (CK's 10 ops + a few aliases) ───────────────────

OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
OP_ID = {n: i for i, n in enumerate(OP_NAMES)}
# Aliases that appear in TIG prose
OP_ALIASES: Dict[str, int] = {
    "void": 0, "v_void": 0, "voids": 0, "the void": 0,
    "lattice": 1, "lattices": 1, "tsml": 1, "bhml": 1,
    "counter": 2, "counters": 2,
    "progress": 3, "progressing": 3,
    "collapse": 4, "collapses": 4, "collapsing": 4,
    "balance": 5, "balanced": 5, "balancing": 5,
    "chaos": 6, "chaotic": 6,
    "harmony": 7, "harmonic": 7, "harmonies": 7, "harmony attractor": 7,
    "breath": 8, "breathing": 8, "breathwork": 8,
    "reset": 9, "resets": 9, "rereset": 9,
}

# Status keywords found in FRONTIERS markdown
STATUS_OPEN = ("open", "tractable", "decade-class", "unknown-difficulty",
                "high-impact", "synthesis-impact", "falsifiability-critical",
                "empirically sharpened")
STATUS_CLOSED = ("closed",)

# Decay time for frontier signals (seconds)
SIGNAL_TTL = 90.0


# ─── Data classes ────────────────────────────────────────────────────────

@dataclass
class Frontier:
    fid: str                          # 'F3'
    title: str                        # 'The alpha-uniqueness proof'
    status: str                       # 'open' | 'closed' | 'tractable'
    body: str                         # markdown body up to next ### heading
    source_path: str                  # path on disk
    operator_set: Set[int] = field(default_factory=set)
    operator_dist: Dict[int, int] = field(default_factory=dict)
    line_start: int = 0
    last_voiced_ts: float = 0.0

    @property
    def is_open(self) -> bool:
        return self.status not in STATUS_CLOSED

    def signature(self) -> Dict[str, int]:
        """Algebraic signature: dominant operator + its projections."""
        if not self.operator_dist:
            return {"op": 7, "sigma": 1, "shell": 7, "four_core": 1}
        dom = max(self.operator_dist, key=self.operator_dist.get)
        return {
            "op": int(dom),
            "sigma": int(sigma_orbit(dom)),
            "shell": int(shell_class(set(self.operator_set))),
            "four_core": int(four_core_class(dom)),
        }


# ─── Parser ──────────────────────────────────────────────────────────────

_FRONTIER_HEADING_RE = re.compile(r"^###\s+(F\d+[a-z]?)\.?\s+(.+?)\s*$", re.M)
_STATUS_RE = re.compile(
    r"\*\*Status:\*\*\s*\*?\*?\s*([A-Za-z][^.\n*]+?)\s*[.*\n]", re.I)


def _detect_status(body: str) -> str:
    m = _STATUS_RE.search(body)
    if not m:
        return "unknown"
    raw = m.group(1).strip().lower()
    if any(k in raw for k in STATUS_CLOSED):
        return "closed"
    if any(k in raw for k in STATUS_OPEN):
        return "open"
    return raw[:32]


def _operator_dist(text: str) -> Dict[int, int]:
    """Count operator mentions in text (alias-aware, case-insensitive)."""
    counts: Dict[int, int] = {}
    lower = text.lower()
    for alias, op in OP_ALIASES.items():
        # word-boundary match
        n = len(re.findall(r"\b" + re.escape(alias) + r"\b", lower))
        if n:
            counts[op] = counts.get(op, 0) + n
    return counts


def parse_frontiers_file(path: Path) -> List[Frontier]:
    """Parse one FRONTIERS_*.md file into a list of Frontier objects.

    Splits on '### F<N>.' headings (the TIG convention).
    """
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    matches = list(_FRONTIER_HEADING_RE.finditer(text))
    out: List[Frontier] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        fid = m.group(1)
        title = m.group(2).strip()
        # Strip status suffix from title for cleanliness
        title = re.sub(r"\s+-\s+(TRACTABLE|DECADE-CLASS|CLOSED|UNKNOWN-DIFFICULTY|"
                        r"HIGH-IMPACT|FALSIFIABILITY-CRITICAL|SYNTHESIS-IMPACT|"
                        r"EMPIRICALLY SHARPENED.*).*$",
                        "", title, flags=re.I)
        status = _detect_status(body)
        op_dist = _operator_dist(body)
        op_set = set(op_dist.keys())
        line_start = text.count("\n", 0, start) + 1
        out.append(Frontier(
            fid=fid, title=title, status=status, body=body,
            source_path=str(path), operator_set=op_set,
            operator_dist=op_dist, line_start=line_start,
        ))
    return out


# ─── Scanner ─────────────────────────────────────────────────────────────

class FrontierScanner:
    """Loads all FRONTIERS_*.md files and answers relevance queries.

    Re-scans automatically if any source file's mtime has changed since the
    last load (so editing a frontiers doc doesn't require a reboot).
    """

    def __init__(self, search_paths: Optional[List[Path]] = None):
        self.search_paths: List[Path] = list(search_paths) if search_paths else \
            self._default_search_paths()
        self.frontiers: List[Frontier] = []
        self._mtime_index: Dict[Path, float] = {}
        self.reload()

    @staticmethod
    def _default_search_paths() -> List[Path]:
        # Up from Gen14/targets/ck/brain/ -> CK FINAL DEPLOYED root
        root = Path(__file__).resolve().parents[4]
        candidates: List[Path] = []
        atlas = root / "Atlas"
        if atlas.is_dir():
            for p in sorted(atlas.glob("FRONTIERS_*.md")):
                candidates.append(p)
        frontiers_root = root / "FRONTIERS.md"
        if frontiers_root.exists():
            candidates.append(frontiers_root)
        return candidates

    # ── public API ───────────────────────────────────────────────────────

    def reload(self) -> int:
        """(Re-)parse all search paths. Returns count of frontiers loaded."""
        out: List[Frontier] = []
        self._mtime_index = {}
        for p in self.search_paths:
            if not p.exists():
                continue
            try:
                self._mtime_index[p] = p.stat().st_mtime
            except Exception:
                self._mtime_index[p] = 0.0
            out.extend(parse_frontiers_file(p))
        self.frontiers = out
        return len(out)

    def _needs_reload(self) -> bool:
        for p in self.search_paths:
            if not p.exists():
                continue
            try:
                cur = p.stat().st_mtime
            except Exception:
                continue
            if cur != self._mtime_index.get(p, 0.0):
                return True
        return False

    def stats(self) -> Dict[str, Any]:
        n_open = sum(1 for f in self.frontiers if f.is_open)
        return {
            "total": len(self.frontiers),
            "open": n_open,
            "closed": len(self.frontiers) - n_open,
            "sources": [str(p) for p in self.search_paths],
        }

    def find_relevant(self,
                       recent_ops: Iterable[int],
                       k: int = 3,
                       prefer_open: bool = True,
                       cooldown_s: float = 600.0,
                       now: Optional[float] = None,
                       ) -> List[Frontier]:
        """Rank frontiers by operator overlap with recent history.

        Args:
            recent_ops: iterable of operator ids from the last few minutes
            k: number of top frontiers to return
            prefer_open: down-weight CLOSED frontiers (multiply score by 0.3)
            cooldown_s: skip frontiers voiced more recently than this
            now: optional epoch seconds (for tests)

        Returns:
            ranked list (length <= k), best first.
        """
        if self._needs_reload():
            self.reload()
        if not self.frontiers:
            return []
        now = now if now is not None else time.time()

        recent_set: Set[int] = set(int(o) % 10 for o in recent_ops)
        if not recent_set:
            recent_set = {7}  # default to HARMONY if no history

        scored: List[Tuple[float, Frontier]] = []
        for f in self.frontiers:
            if now - f.last_voiced_ts < cooldown_s:
                continue
            if not f.operator_set:
                continue
            inter = len(recent_set & f.operator_set)
            union = len(recent_set | f.operator_set)
            if union == 0:
                continue
            jaccard = inter / union
            # Boost: total operator mass shared with recent set
            mass = sum(f.operator_dist.get(o, 0) for o in recent_set)
            mass_log = math.log1p(mass)
            # 4-core anchor bonus
            sig = f.signature()
            four_core_bonus = 0.1 if sig["four_core"] != 4 else 0.0
            # Composite score
            score = 0.6 * jaccard + 0.25 * (mass_log / 5.0) + four_core_bonus
            if prefer_open and not f.is_open:
                score *= 0.3
            scored.append((score, f))

        scored.sort(key=lambda x: -x[0])
        return [f for _, f in scored[:k]]

    def mark_voiced(self, fid: str, now: Optional[float] = None):
        """Mark a frontier as just-voiced so it doesn't re-fire immediately."""
        now = now if now is not None else time.time()
        for f in self.frontiers:
            if f.fid == fid:
                f.last_voiced_ts = now
                return True
        return False

    def build_signal(self, frontier: Frontier,
                      jaccard: float = 0.0,
                      salience: float = 0.5,
                      ) -> Dict[str, Any]:
        """Convert a Frontier into a structured proactive signal dict."""
        now = time.time()
        return {
            "kind": "frontier_suggestion",
            "frontier_id": frontier.fid,
            "frontier_title": frontier.title,
            "status": frontier.status,
            "source_path": frontier.source_path,
            "source_line": frontier.line_start,
            "operator_overlap": float(jaccard),
            "salience": float(salience),
            "algebraic_signature": frontier.signature(),
            "created_ts": now,
            "expires_ts": now + SIGNAL_TTL,
        }


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_frontier_scanner(engine) -> bool:
    """Attach a FrontierScanner to the engine.

    Side effects on engine:
      engine.frontier_scanner          : FrontierScanner instance
      engine.frontier_relevant(ops, k) : convenience callable
    """
    try:
        fs = FrontierScanner()
    except Exception as e:
        print(f"[CK Gen14] mount_frontier_scanner: failed ({e})")
        return False
    engine.frontier_scanner = fs

    def _relevant(recent_ops, k: int = 3):
        try:
            return fs.find_relevant(recent_ops, k=k)
        except Exception:
            return []

    engine.frontier_relevant = _relevant

    stats = fs.stats()
    print(f"[CK Gen14] mount_frontier_scanner: {stats['total']} frontiers "
          f"({stats['open']} open) from {len(stats['sources'])} sources")
    return True


# ─── Standalone smoke test ───────────────────────────────────────────────

def _smoke():
    print("Smoke test: ck_frontier_scanner")
    fs = FrontierScanner()
    s = fs.stats()
    print(f"  Loaded {s['total']} frontiers ({s['open']} open) from {len(s['sources'])} sources")
    for sp in s["sources"]:
        print(f"    {sp}")

    # Show a sample
    if fs.frontiers:
        f = fs.frontiers[0]
        print(f"\n  Sample frontier: {f.fid} '{f.title}'")
        print(f"    status   : {f.status}")
        print(f"    op_dist  : {f.operator_dist}")
        print(f"    signature: {f.signature()}")

    # Query: pretend recent history is HARMONY+LATTICE (math discussion)
    print(f"\n  find_relevant(recent_ops=[7,1,7,9,7], k=3):")
    hits = fs.find_relevant(recent_ops=[7, 1, 7, 9, 7], k=3)
    for h in hits:
        sig = h.signature()
        print(f"    {h.fid:6s} '{h.title[:50]}' (status={h.status}, sig={sig})")

    # Query: pretend recent history is HARMONY (one-axis)
    print(f"\n  find_relevant(recent_ops=[7], k=3):")
    hits = fs.find_relevant(recent_ops=[7], k=3)
    for h in hits:
        sig = h.signature()
        print(f"    {h.fid:6s} '{h.title[:50]}' (status={h.status}, sig={sig})")

    # Build a signal
    if hits:
        sig = fs.build_signal(hits[0], jaccard=0.3, salience=0.7)
        print(f"\n  build_signal sample (keys): {sorted(sig.keys())}")

    print("\nFrontier scanner smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
