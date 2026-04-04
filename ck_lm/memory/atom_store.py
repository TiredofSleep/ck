"""
atom_store.py — CK Memory: SQLite-backed Atom storage

Atoms are the smallest memory unit. This module handles:
- Writing atoms to SQLite
- Reading atoms by ID or DBC27 key neighborhood
- Recurrence tracking (bump count on re-observation)
- Compression: prune low-confidence atoms after they've been superseded

Schema lives in memory.db, table: atoms

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
import sqlite3
import json
import uuid
import time
from pathlib import Path
from typing import Optional

from .event_schema import Atom, PRIVATE, SHARED, ABSTRACT

DB_PATH = Path.home() / '.ck' / 'memory' / 'memory.db'
PRUNE_CONFIDENCE = 0.2   # atoms below this after 10+ ticks get pruned
PRUNE_AGE_SECS   = 86400 # 24 hours before low-confidence atoms expire


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS atoms (
            id              TEXT PRIMARY KEY,
            timestamp       REAL NOT NULL,
            modality        TEXT NOT NULL,
            raw_ref         TEXT,
            generators      TEXT NOT NULL,   -- JSON array
            force_vector    TEXT NOT NULL,   -- JSON array [5 floats]
            operator        INTEGER NOT NULL,
            lens            TEXT NOT NULL,
            privacy         TEXT NOT NULL,
            recurrence      INTEGER DEFAULT 1,
            confidence      REAL DEFAULT 0.5,
            parent_paths    TEXT NOT NULL,   -- JSON array of path IDs
            compression_score REAL DEFAULT 0.0,
            dbc27_key       TEXT NOT NULL DEFAULT ''
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_atoms_dbc27 ON atoms(dbc27_key)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_atoms_operator ON atoms(operator)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_atoms_lens ON atoms(lens)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_atoms_privacy ON atoms(privacy)")
    conn.commit()


def write_atom(atom: Atom, dbc27_key: str = '') -> str:
    """Write an Atom to the store. Returns atom.id."""
    conn = _connect()
    _ensure_schema(conn)
    conn.execute("""
        INSERT OR REPLACE INTO atoms
        (id, timestamp, modality, raw_ref, generators, force_vector,
         operator, lens, privacy, recurrence, confidence, parent_paths,
         compression_score, dbc27_key)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        atom.id,
        atom.timestamp,
        atom.modality,
        atom.raw_ref,
        json.dumps(atom.generators),
        json.dumps(atom.force_vector),
        atom.operator,
        atom.lens,
        atom.privacy,
        atom.recurrence,
        atom.confidence,
        json.dumps(atom.parent_paths),
        atom.compression_score,
        dbc27_key,
    ))
    conn.commit()
    conn.close()
    return atom.id


def get_atom(atom_id: str) -> Optional[Atom]:
    """Retrieve a single Atom by ID."""
    conn = _connect()
    _ensure_schema(conn)
    row = conn.execute(
        "SELECT * FROM atoms WHERE id=?", (atom_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_atom(row)


def get_atoms_by_key(dbc27_key: str, limit: int = 20) -> list[Atom]:
    """Retrieve Atoms matching a DBC27 key (exact)."""
    conn = _connect()
    _ensure_schema(conn)
    rows = conn.execute(
        "SELECT * FROM atoms WHERE dbc27_key=? ORDER BY confidence DESC, recurrence DESC LIMIT ?",
        (dbc27_key, limit)
    ).fetchall()
    conn.close()
    return [_row_to_atom(r) for r in rows]


def get_atoms_by_keys(keys: list[str], limit: int = 50) -> list[Atom]:
    """Retrieve Atoms across a neighborhood of DBC27 keys."""
    if not keys:
        return []
    conn = _connect()
    _ensure_schema(conn)
    placeholders = ','.join('?' * len(keys))
    rows = conn.execute(
        f"SELECT * FROM atoms WHERE dbc27_key IN ({placeholders}) "
        f"ORDER BY confidence DESC, recurrence DESC LIMIT ?",
        (*keys, limit)
    ).fetchall()
    conn.close()
    return [_row_to_atom(r) for r in rows]


def bump_recurrence(atom_id: str) -> None:
    """Increment recurrence count for an atom."""
    conn = _connect()
    _ensure_schema(conn)
    conn.execute(
        "UPDATE atoms SET recurrence = recurrence + 1 WHERE id=?",
        (atom_id,)
    )
    conn.commit()
    conn.close()


def prune_expired_atoms() -> int:
    """Remove low-confidence, old atoms that have been superseded.

    Returns count of pruned atoms.
    """
    cutoff_time = time.time() - PRUNE_AGE_SECS
    conn = _connect()
    _ensure_schema(conn)
    result = conn.execute(
        "DELETE FROM atoms WHERE confidence < ? AND timestamp < ? AND recurrence < 2",
        (PRUNE_CONFIDENCE, cutoff_time)
    )
    count = result.rowcount
    conn.commit()
    conn.close()
    return count


def atom_count() -> int:
    conn = _connect()
    _ensure_schema(conn)
    n = conn.execute("SELECT COUNT(*) FROM atoms").fetchone()[0]
    conn.close()
    return n


def _row_to_atom(row) -> Atom:
    return Atom(
        id=row['id'],
        timestamp=row['timestamp'],
        modality=row['modality'],
        raw_ref=row['raw_ref'],
        generators=json.loads(row['generators']),
        force_vector=json.loads(row['force_vector']),
        operator=row['operator'],
        lens=row['lens'],
        privacy=row['privacy'],
        recurrence=row['recurrence'],
        confidence=row['confidence'],
        parent_paths=json.loads(row['parent_paths']),
        compression_score=row['compression_score'],
    )
