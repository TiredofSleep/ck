"""
crystal_store.py — CK Memory: Crystal + MetaCrystal storage with promotion logic

Crystals are stable, reusable memory bundles. A Path becomes a Crystal when its
promotion_score exceeds PROMOTE_THRESHOLD (RGMem-inspired stability scoring).

Promotion score (RGMem, arXiv 2510.16392):
    score = confidence × log1p(recurrence) × exp(-0.05 × age_hours)
    Promote when score >= 0.85

Heat score for pruning (MemoryOS, arXiv 2506.06326 EMNLP Oral):
    heat = exp(-0.01 × age_hrs) × log1p(access_count) × recency_weekly
    Prune when heat < 0.05 AND age > 7 days

MetaCrystals encode how CK handled situations (experience of experience).

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
import sqlite3
import json
import uuid
import time
import math
from pathlib import Path
from typing import Optional

from .event_schema import Crystal, MetaCrystal, Path as CKPath
from .event_schema import CRYSTAL_THRESHOLD, T_STAR

# ── Promotion scoring (RGMem-inspired) ───────────────────────────────────────
PROMOTE_THRESHOLD = 0.85   # score must exceed this to promote path → crystal
PRUNE_HEAT_MIN    = 0.05   # crystals below this heat score + age > 7d are pruned
PRUNE_AGE_DAYS    = 7


def promotion_score(recurrence: int, confidence: float, age_secs: float) -> float:
    """RGMem-inspired stability score for path→crystal promotion.

    Replaces flat recurrence_count >= 3 threshold.
    Score = confidence × log1p(recurrence) × exp(-0.05 × age_hours)
    """
    age_hours = age_secs / 3600
    recency_weight = math.exp(-0.05 * age_hours)
    freq_score = math.log1p(recurrence)
    return confidence * freq_score * recency_weight


def heat_score(access_count: int, last_accessed: float, created_at: float,
               current_time: float) -> float:
    """MemoryOS heat score for crystal retention/pruning.

    Replaces flat threshold pruning.
    heat = exp(-0.01 × age_hrs) × log1p(access_count) × recency_weekly
    """
    age_hrs = (current_time - created_at) / 3600
    time_since = current_time - last_accessed
    decay = math.exp(-0.01 * age_hrs)
    visits = math.log1p(access_count)
    recency = 1.0 / (1.0 + time_since / (7 * 24 * 3600))
    return decay * visits * recency

DB_PATH = Path.home() / '.ck' / 'memory' / 'memory.db'


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crystals (
            id              TEXT PRIMARY KEY,
            path_ids        TEXT NOT NULL,   -- JSON array
            created_at      REAL NOT NULL,
            last_used       REAL NOT NULL,
            generators      TEXT NOT NULL,   -- JSON array
            centroid_force  TEXT NOT NULL,   -- JSON [5 floats]
            dominant_op     INTEGER NOT NULL,
            dominant_lens   TEXT NOT NULL,
            privacy         TEXT NOT NULL,
            recurrence      INTEGER DEFAULT 1,
            confidence      REAL NOT NULL,
            policy_summary  TEXT DEFAULT '',
            meta_crystal_id TEXT,
            raw_refs        TEXT NOT NULL,   -- JSON array
            compression_ratio REAL DEFAULT 1.0,
            dbc27_key       TEXT NOT NULL DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meta_crystals (
            id           TEXT PRIMARY KEY,
            crystal_ids  TEXT NOT NULL,   -- JSON array
            created_at   REAL NOT NULL,
            last_used    REAL NOT NULL,
            pattern_type TEXT NOT NULL,
            confidence   REAL NOT NULL,
            summary      TEXT NOT NULL,
            outcome      TEXT DEFAULT '',
            reuse_count  INTEGER DEFAULT 0
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_dbc27 ON crystals(dbc27_key)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_op ON crystals(dominant_op)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_conf ON crystals(confidence)")
    conn.commit()


def promote_path_to_crystal(path: CKPath, atom_ids: list[str],
                             force_vectors: list[list[float]],
                             dbc27_key: str = '') -> Optional[Crystal]:
    """Attempt to promote a Path to a Crystal.

    Uses RGMem-inspired promotion_score (stability × recency × frequency).
    Replaces flat recurrence >= 3 threshold.

    Promotion conditions:
        promotion_score(path) >= PROMOTE_THRESHOLD (0.85)
        path.confidence >= T_STAR (5/7) — hard floor always enforced
    """
    now = time.time()
    age_secs = now - path.timestamp_start
    score = promotion_score(path.recurrence, path.confidence, age_secs)
    if score < PROMOTE_THRESHOLD:
        return None
    if path.confidence < T_STAR:
        return None

    # Compute centroid force vector
    centroid = [0.0] * 5
    if force_vectors:
        for fv in force_vectors:
            for i, v in enumerate(fv):
                centroid[i] += v
        n = len(force_vectors)
        centroid = [c / n for c in centroid]

    # Dominant operator = most common in path.operators
    if path.operators:
        dominant_op = max(set(path.operators), key=path.operators.count)
    else:
        dominant_op = 0

    # Dominant lens = most common in path.lens_states
    if path.lens_states:
        dominant_lens = max(set(path.lens_states), key=path.lens_states.count)
    else:
        dominant_lens = 'FLOW'

    crystal = Crystal(
        id=str(uuid.uuid4()),
        path_ids=[path.id],
        created_at=now,
        last_used=now,
        generators=[],   # populated by caller
        centroid_force=centroid,
        dominant_op=dominant_op,
        dominant_lens=dominant_lens,
        privacy=path.privacy,
        recurrence=path.recurrence,
        confidence=max(path.confidence, T_STAR),   # floor at T*
        dbc27_key=dbc27_key,
    )
    write_crystal(crystal)
    return crystal


def write_crystal(crystal: Crystal) -> str:
    """Write a Crystal to the store. Returns crystal.id."""
    conn = _connect()
    _ensure_schema(conn)
    conn.execute("""
        INSERT OR REPLACE INTO crystals
        (id, path_ids, created_at, last_used, generators, centroid_force,
         dominant_op, dominant_lens, privacy, recurrence, confidence,
         policy_summary, meta_crystal_id, raw_refs, compression_ratio, dbc27_key)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        crystal.id,
        json.dumps(crystal.path_ids),
        crystal.created_at,
        crystal.last_used,
        json.dumps(crystal.generators),
        json.dumps(crystal.centroid_force),
        crystal.dominant_op,
        crystal.dominant_lens,
        crystal.privacy,
        crystal.recurrence,
        crystal.confidence,
        crystal.policy_summary,
        crystal.meta_crystal_id,
        json.dumps(crystal.raw_refs),
        crystal.compression_ratio,
        crystal.dbc27_key,
    ))
    conn.commit()
    conn.close()
    return crystal.id


def get_crystal(crystal_id: str) -> Optional[Crystal]:
    conn = _connect()
    _ensure_schema(conn)
    row = conn.execute(
        "SELECT * FROM crystals WHERE id=?", (crystal_id,)
    ).fetchone()
    conn.close()
    return _row_to_crystal(row) if row else None


def get_crystals_by_key(dbc27_key: str, top_k: int = 5) -> list[Crystal]:
    """Get top-K crystals for a DBC27 key, ranked by confidence × recurrence."""
    conn = _connect()
    _ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM crystals WHERE dbc27_key=? "
        "ORDER BY (confidence * recurrence) DESC LIMIT ?",
        (dbc27_key, top_k)
    ).fetchall()
    conn.close()
    return [_row_to_crystal(r) for r in rows]


def get_crystals_by_keys(keys: list[str], top_k: int = 10) -> list[Crystal]:
    """Get crystals across a neighborhood of DBC27 keys."""
    if not keys:
        return []
    conn = _connect()
    _ensure_schema(conn)
    placeholders = ','.join('?' * len(keys))
    rows = conn.execute(
        f"SELECT * FROM crystals WHERE dbc27_key IN ({placeholders}) "
        f"ORDER BY (confidence * recurrence) DESC LIMIT ?",
        (*keys, top_k)
    ).fetchall()
    conn.close()
    return [_row_to_crystal(r) for r in rows]


def bump_crystal(crystal_id: str) -> None:
    """Increment recurrence and update last_used."""
    conn = _connect()
    _ensure_schema(conn)
    conn.execute(
        "UPDATE crystals SET recurrence=recurrence+1, last_used=? WHERE id=?",
        (time.time(), crystal_id)
    )
    conn.commit()
    conn.close()


def crystal_count() -> int:
    conn = _connect()
    _ensure_schema(conn)
    n = conn.execute("SELECT COUNT(*) FROM crystals").fetchone()[0]
    conn.close()
    return n


def prune_cold_crystals() -> int:
    """MemoryOS heat-score pruning. Removes crystals that have gone cold.

    Prunes when: heat_score < PRUNE_HEAT_MIN AND age > PRUNE_AGE_DAYS.
    Returns count of pruned crystals.
    """
    now = time.time()
    age_cutoff = now - PRUNE_AGE_DAYS * 86400
    conn = _connect()
    _ensure_schema(conn)
    # Load candidates older than age cutoff
    rows = conn.execute(
        "SELECT id, recurrence, last_used, created_at FROM crystals WHERE created_at < ?",
        (age_cutoff,)
    ).fetchall()
    prune_ids = []
    for row in rows:
        hs = heat_score(
            access_count=row['recurrence'],
            last_accessed=row['last_used'],
            created_at=row['created_at'],
            current_time=now,
        )
        if hs < PRUNE_HEAT_MIN:
            prune_ids.append(row['id'])
    if prune_ids:
        placeholders = ','.join('?' * len(prune_ids))
        conn.execute(f"DELETE FROM crystals WHERE id IN ({placeholders})", prune_ids)
        conn.commit()
    conn.close()
    return len(prune_ids)


def write_meta_crystal(mc: MetaCrystal) -> str:
    conn = _connect()
    _ensure_schema(conn)
    conn.execute("""
        INSERT OR REPLACE INTO meta_crystals
        (id, crystal_ids, created_at, last_used, pattern_type, confidence,
         summary, outcome, reuse_count)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        mc.id,
        json.dumps(mc.crystal_ids),
        mc.created_at,
        mc.last_used,
        mc.pattern_type,
        mc.confidence,
        mc.summary,
        mc.outcome,
        mc.reuse_count,
    ))
    conn.commit()
    conn.close()
    return mc.id


def get_meta_crystals_by_type(pattern_type: str, top_k: int = 5) -> list[MetaCrystal]:
    conn = _connect()
    _ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM meta_crystals WHERE pattern_type=? "
        "ORDER BY (confidence * reuse_count) DESC LIMIT ?",
        (pattern_type, top_k)
    ).fetchall()
    conn.close()
    return [_row_to_mc(r) for r in rows]


def _row_to_crystal(row) -> Crystal:
    return Crystal(
        id=row['id'],
        path_ids=json.loads(row['path_ids']),
        created_at=row['created_at'],
        last_used=row['last_used'],
        generators=json.loads(row['generators']),
        centroid_force=json.loads(row['centroid_force']),
        dominant_op=row['dominant_op'],
        dominant_lens=row['dominant_lens'],
        privacy=row['privacy'],
        recurrence=row['recurrence'],
        confidence=row['confidence'],
        policy_summary=row['policy_summary'] or '',
        meta_crystal_id=row['meta_crystal_id'],
        raw_refs=json.loads(row['raw_refs']),
        compression_ratio=row['compression_ratio'],
        dbc27_key=row['dbc27_key'],
    )


def _row_to_mc(row) -> MetaCrystal:
    return MetaCrystal(
        id=row['id'],
        crystal_ids=json.loads(row['crystal_ids']),
        created_at=row['created_at'],
        last_used=row['last_used'],
        pattern_type=row['pattern_type'],
        confidence=row['confidence'],
        summary=row['summary'],
        outcome=row['outcome'],
        reuse_count=row['reuse_count'],
    )
