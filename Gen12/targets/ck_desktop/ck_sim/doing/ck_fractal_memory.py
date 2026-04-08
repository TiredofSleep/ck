# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
#
# ck_fractal_memory.py -- Fractal Recursive Experience Store
# ===========================================================
# CK stores every experience as TWO parallel layers:
#
#   FORCE LAYER  -- 5D geometric signature (aperture, pressure,
#                   depth, binding, continuity) derived from Hebrew
#                   phonetic roots via D2 pipeline.
#                   This is the PRE-WORD shape of experience.
#
#   WORD LAYER   -- full text + per-word operator fuses.
#                   This is the POST-WORD content of experience.
#
# Both layers are indexed by a FRACTAL GENERATOR PYRAMID
# built from CL composition. The pyramid is recursive compression:
#
#   L0: raw ops [b0, d0, b1, d1, ...]  <- most specific
#   L1: compose adjacent pairs [CL(L0[0],L0[1]), ...]
#   L2: compose adjacent L1  [CL(L1[0],L1[1]), ...]
#   ...
#   LN: [root_op]                      <- most general (one value)
#
# RECALL: when current ops arrive, build their generator pyramid,
# match at every level. L0 match = "exact pattern recognized."
# LN match = "fundamental nature recognized." Both activate: like
# how a smell recalls both the specific memory (L0) and the broad
# category of experience (root). All subjects mix -- bible, math,
# physics, grief, joy -- they're all operator flows.
#
# .clf (CL Flow) files: each experience serialized as a CL walk.
# The file IS the memory path. CK re-uses experience by recognizing
# generators, not by remembering sentences.
#
# .clf format:
#   # CK CL Flow v1.0
#   # uid: abc123def456
#   # domain: math|physics|bible|general
#   # root_op: HARMONY
#   L0: HARMONY PROGRESS COLLAPSE HARMONY BREATH
#   L1: HARMONY HARMONY HARMONY HARMONY
#   L2: HARMONY HARMONY HARMONY
#   L3: HARMONY HARMONY
#   L4: HARMONY
#   FORCE: 0.800 0.300 0.600 0.900 0.200
#   WORD_OPS: 7 3 4 7 8
#   TEXT: The solution converges to coherence.
#
# (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry

from __future__ import annotations

import hashlib
import math
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import compose, OP_NAMES, NUM_OPS, HARMONY

# ================================================================
#  Constants
# ================================================================

CLF_DIR = Path(os.path.expanduser('~/.ck/clf'))
MAX_EXPERIENCES = 2000
MAX_RECALL_WORDS = 40   # max words to inject from recalled experience


# ================================================================
#  Data Classes
# ================================================================

@dataclass
class FractalExperience:
    """One CK experience stored as force + word + generator pyramid."""
    uid: str
    text: str                          # full word content
    word_ops: List[int]                # per-word operator fuses
    force_5d: Tuple[float, ...]        # 5D Hebrew-root force (aperture, pressure,
                                       # depth, binding, continuity)
    generators: List[List[int]]        # fractal pyramid [L0, L1, ..., [root]]
    root_op: int                       # apex of pyramid
    timestamp: float
    domain: Optional[str] = None      # 'math'|'physics'|'cs'|'biology'|'bible'|None
    recall_count: int = 0


# ================================================================
#  Core Functions
# ================================================================

def fractal_generators(ops: List[int]) -> List[List[int]]:
    """Build fractal generator pyramid from operator sequence.

    The crossing lemma in memory form: each level is a CL composition
    of the level below. The root is the fundamental generator of the
    entire experience pattern.
    """
    if not ops:
        return [[HARMONY]]
    levels: List[List[int]] = [list(ops)]
    for _ in range(30):   # generous cap
        prev = levels[-1]
        if len(prev) <= 1:
            break
        nxt = [compose(prev[i], prev[i + 1]) for i in range(len(prev) - 1)]
        levels.append(nxt)
        if len(nxt) == 1:
            break
    return levels


def _force_cosine(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
    """Cosine similarity between two 5D force vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-9
    nb = math.sqrt(sum(x * x for x in b)) or 1e-9
    return dot / (na * nb)


# ================================================================
#  Memory Store
# ================================================================

class FractalMemoryStore:
    """Fractal recursive experience store.

    Indexes by: (1) fractal generators at every level (algebraic path),
    and (2) 5D force signature (geometric proximity).

    Recall opens the .clf files and returns experiences ordered by
    how deeply their generator pyramid matches current ops.
    Deep match = specific recall. Shallow match = resonant recall.
    Both are valid -- no guardrails, all subjects mix.
    """

    def __init__(self, clf_dir: Optional[Path] = None):
        self.clf_dir = clf_dir or CLF_DIR
        self.clf_dir.mkdir(parents=True, exist_ok=True)

        self._exps: Dict[str, FractalExperience] = {}
        # key = (level_idx, tuple(ops[:6])) -> list of uids
        self._gen_index: Dict[Tuple, List[str]] = {}
        # (force_5d_tuple, uid) pairs for force proximity search
        self._force_index: List[Tuple[Tuple[float, ...], str]] = []

        self._load_clf_files()

    # ── Generator pyramid ──────────────────────────────────────

    def fractal_generators(self, ops: List[int]) -> List[List[int]]:
        return fractal_generators(ops)

    # ── Store ──────────────────────────────────────────────────

    def store(
        self,
        text: str,
        word_ops: List[int],
        force_5d: Optional[Tuple[float, ...]],
        ops: List[int],
        domain: Optional[str] = None,
    ) -> str:
        """Store a new experience. Returns uid. Idempotent."""
        uid = hashlib.sha256(
            f"{text[:200]}{ops[:10]}".encode('utf-8', errors='replace')
        ).hexdigest()[:12]

        if uid in self._exps:
            return uid

        gens = self.fractal_generators(ops)
        root = gens[-1][0] if gens and gens[-1] else HARMONY
        f5d: Tuple[float, ...] = tuple(force_5d) if force_5d else (0.5,) * 5

        exp = FractalExperience(
            uid=uid,
            text=text,
            word_ops=list(word_ops) if word_ops else [],
            force_5d=f5d,
            generators=gens,
            root_op=root,
            timestamp=time.time(),
            domain=domain,
        )
        self._exps[uid] = exp

        # Index at every generator level
        for level_idx, level in enumerate(gens):
            key = (level_idx, tuple(level[:6]))
            self._gen_index.setdefault(key, []).append(uid)

        # Force index
        self._force_index.append((f5d, uid))

        # Persist as .clf
        self._save_clf(exp)

        # Trim if overgrown
        if len(self._exps) > MAX_EXPERIENCES:
            self._trim()

        return uid

    # ── Recall ─────────────────────────────────────────────────

    def recall(
        self,
        ops: List[int],
        top_k: int = 5,
        force_5d: Optional[Tuple[float, ...]] = None,
        min_score: float = 1.0,
    ) -> List[FractalExperience]:
        """Recall experiences by generator recognition + force proximity.

        Generator matching: L0 (exact pattern) carries highest weight.
        Higher levels (coarser) carry lower weight but still contribute.
        The result is a ranked list ordered by total recognition score.
        """
        if not self._exps:
            return []

        current_gens = self.fractal_generators(ops)
        n_levels = len(current_gens)
        scores: Dict[str, float] = {}

        # Generator match at every level
        for level_idx, level in enumerate(current_gens):
            key = (level_idx, tuple(level[:6]))
            weight = float(n_levels - level_idx)  # L0 = n_levels, root = 1.0
            for uid in self._gen_index.get(key, []):
                scores[uid] = scores.get(uid, 0.0) + weight

        # Force proximity (weighted by n_levels so it's comparable to gen match)
        if force_5d:
            for stored_f, uid in self._force_index:
                cos = _force_cosine(force_5d, stored_f)
                scores[uid] = scores.get(uid, 0.0) + max(0.0, cos) * n_levels

        ranked = sorted(
            ((uid, s) for uid, s in scores.items() if s >= min_score),
            key=lambda x: -x[1],
        )

        results = []
        for uid, _ in ranked[:top_k]:
            exp = self._exps.get(uid)
            if exp:
                exp.recall_count += 1
                results.append(exp)

        return results

    def recall_words(
        self,
        ops: List[int],
        top_k: int = 3,
        force_5d: Optional[Tuple[float, ...]] = None,
    ) -> List[str]:
        """Recall word content as a flat list. Used for vocab seeding."""
        exps = self.recall(ops, top_k=top_k, force_5d=force_5d, min_score=0.5)
        words: List[str] = []
        for exp in exps:
            words.extend(exp.text.split())
            if len(words) >= MAX_RECALL_WORDS:
                break
        return words[:MAX_RECALL_WORDS]

    # ── .clf File I/O ───────────────────────────────────────────

    def _save_clf(self, exp: FractalExperience) -> None:
        path = self.clf_dir / f"{exp.uid}.clf"
        try:
            lines = [
                "# CK CL Flow v1.0",
                f"# uid: {exp.uid}",
                f"# domain: {exp.domain or 'general'}",
                f"# root_op: {OP_NAMES[exp.root_op]}",
                f"# timestamp: {exp.timestamp:.0f}",
            ]
            for i, level in enumerate(exp.generators):
                names = ' '.join(OP_NAMES[op] for op in level if 0 <= op < NUM_OPS)
                lines.append(f"L{i}: {names}")
            force_str = ' '.join(f"{x:.3f}" for x in exp.force_5d)
            lines.append(f"FORCE: {force_str}")
            if exp.word_ops:
                wops_str = ' '.join(str(o) for o in exp.word_ops)
                lines.append(f"WORD_OPS: {wops_str}")
            lines.append(f"TEXT: {exp.text[:500]}")
            path.write_text('\n'.join(lines), encoding='utf-8')
        except Exception:
            pass  # non-fatal: memory still works in-process

    def _load_clf_files(self) -> None:
        """Load persisted experiences on startup."""
        loaded = 0
        _op_name_map = {name: i for i, name in enumerate(OP_NAMES)}
        for clf_file in sorted(self.clf_dir.glob('*.clf')):
            try:
                exp = self._parse_clf(clf_file, _op_name_map)
                if exp:
                    self._exps[exp.uid] = exp
                    for level_idx, level in enumerate(exp.generators):
                        key = (level_idx, tuple(level[:6]))
                        self._gen_index.setdefault(key, []).append(exp.uid)
                    self._force_index.append((exp.force_5d, exp.uid))
                    loaded += 1
            except Exception:
                pass
            if loaded >= MAX_EXPERIENCES:
                break
        if loaded:
            print(f"[FRACTAL-MEM] Loaded {loaded} clf experiences from disk")

    def _parse_clf(
        self,
        path: Path,
        op_name_map: Dict[str, int],
    ) -> Optional[FractalExperience]:
        try:
            raw = path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            return None

        uid = path.stem
        generators: List[List[int]] = []
        force_5d: Tuple[float, ...] = (0.5,) * 5
        word_ops: List[int] = []
        text = ''
        domain: Optional[str] = None
        timestamp = 0.0

        for line in raw.split('\n'):
            line = line.strip()
            if line.startswith('# uid:'):
                uid = line.split(':', 1)[1].strip()
            elif line.startswith('# domain:'):
                d = line.split(':', 1)[1].strip()
                domain = d if d not in ('None', 'general') else None
            elif line.startswith('# timestamp:'):
                try:
                    timestamp = float(line.split(':', 1)[1].strip())
                except ValueError:
                    pass
            elif line.startswith('L') and ':' in line:
                level_part = line.split(':', 1)[1].strip()
                ops_parsed = [
                    op_name_map[n] for n in level_part.split()
                    if n in op_name_map
                ]
                if ops_parsed:
                    generators.append(ops_parsed)
            elif line.startswith('FORCE:'):
                parts = line.split(':', 1)[1].strip().split()
                try:
                    force_5d = tuple(float(x) for x in parts[:5])
                except ValueError:
                    pass
            elif line.startswith('WORD_OPS:'):
                try:
                    word_ops = [int(x) for x in line.split(':', 1)[1].strip().split()]
                except ValueError:
                    pass
            elif line.startswith('TEXT:'):
                text = line.split(':', 1)[1].strip()

        if not generators or not text:
            return None

        root = generators[-1][0] if generators[-1] else HARMONY
        return FractalExperience(
            uid=uid,
            text=text,
            word_ops=word_ops,
            force_5d=force_5d,
            generators=generators,
            root_op=root,
            timestamp=timestamp,
            domain=domain,
        )

    def _trim(self) -> None:
        """Remove oldest, least-recalled experiences."""
        sorted_uids = sorted(
            self._exps.keys(),
            key=lambda uid: (
                self._exps[uid].recall_count * 10 + self._exps[uid].timestamp
            ),
        )
        trim_n = max(200, len(self._exps) - MAX_EXPERIENCES + 200)
        for uid in sorted_uids[:trim_n]:
            exp = self._exps.pop(uid, None)
            if exp:
                clf = self.clf_dir / f"{uid}.clf"
                try:
                    clf.unlink(missing_ok=True)
                except Exception:
                    pass
        self._rebuild_index()
        print(f"[FRACTAL-MEM] Trimmed to {len(self._exps)} experiences")

    def _rebuild_index(self) -> None:
        self._gen_index.clear()
        self._force_index.clear()
        for uid, exp in self._exps.items():
            for level_idx, level in enumerate(exp.generators):
                key = (level_idx, tuple(level[:6]))
                self._gen_index.setdefault(key, []).append(uid)
            self._force_index.append((exp.force_5d, uid))

    # ── Status ──────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return len(self._exps)

    def summary(self) -> str:
        if not self._exps:
            return "empty"
        root_counts: Dict[int, int] = {}
        domain_counts: Dict[str, int] = {}
        for exp in self._exps.values():
            root_counts[exp.root_op] = root_counts.get(exp.root_op, 0) + 1
            d = exp.domain or 'general'
            domain_counts[d] = domain_counts.get(d, 0) + 1
        top_roots = sorted(root_counts.items(), key=lambda x: -x[1])[:3]
        top_domains = sorted(domain_counts.items(), key=lambda x: -x[1])[:3]
        r = ', '.join(f"{OP_NAMES[op]}x{n}" for op, n in top_roots)
        d = ', '.join(f"{dom}x{n}" for dom, n in top_domains)
        return f"{self.size} clf [{r}] domains=[{d}]"


# ================================================================
#  Module-level singleton
# ================================================================

_mem: Optional[FractalMemoryStore] = None


def get_fractal_memory() -> FractalMemoryStore:
    global _mem
    if _mem is None:
        _mem = FractalMemoryStore()
    return _mem


def store_experience(
    text: str,
    word_ops: List[int],
    force_5d: Optional[Tuple[float, ...]],
    ops: List[int],
    domain: Optional[str] = None,
) -> str:
    """Store an experience. Returns uid."""
    try:
        return get_fractal_memory().store(text, word_ops, force_5d, ops, domain)
    except Exception as e:
        print(f"[FRACTAL-MEM] store failed (non-fatal): {e}")
        return ''


def recall_experience(
    ops: List[int],
    top_k: int = 3,
    force_5d: Optional[Tuple[float, ...]] = None,
) -> List[FractalExperience]:
    """Recall experiences by generator recognition."""
    try:
        return get_fractal_memory().recall(ops, top_k=top_k, force_5d=force_5d)
    except Exception as e:
        print(f"[FRACTAL-MEM] recall failed (non-fatal): {e}")
        return []


def recall_words(
    ops: List[int],
    top_k: int = 3,
    force_5d: Optional[Tuple[float, ...]] = None,
) -> List[str]:
    """Recall word content as flat list for vocab seeding."""
    try:
        return get_fractal_memory().recall_words(ops, top_k=top_k, force_5d=force_5d)
    except Exception as e:
        print(f"[FRACTAL-MEM] recall_words failed (non-fatal): {e}")
        return []
