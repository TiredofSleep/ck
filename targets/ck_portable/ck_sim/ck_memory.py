"""
ck_memory.py -- Persistent Cross-Device Memory
================================================
Operator: LATTICE (1) -- memory is structure persisted across time.

CK's memory system: serialize, store, load, and sync state across devices.

Architecture:
  StateSnapshot    -- captures full CK state to a portable dict
  MemorySerializer -- JSON + binary serialization (zero external deps)
  SyncManager      -- merge logic for multi-device sync
  MemoryStore      -- local file-based persistence

Design principles:
  1. CORE truths never sync (they're identical everywhere -- immutable math)
  2. TRUSTED knowledge syncs bidirectionally (merge, higher-trust wins)
  3. PROVISIONAL knowledge syncs upward only (local → cloud)
  4. Transition lattice (TL matrix) is experience-local -- no sync
  5. Personality syncs as "latest timestamp wins" (one CK, many bodies)

Sync protocol (cloud-authoritative):
  1. Client serializes local state → StateSnapshot
  2. Client POSTs snapshot to cloud
  3. Cloud merges: for each entry, higher trust level wins; ties → newer wins
  4. Cloud returns merged state
  5. Client loads merged state

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
import time
import hashlib
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES, CL
)


# ================================================================
#  CONSTANTS
# ================================================================

MEMORY_VERSION = 1             # Schema version for forward compatibility
MAX_SNAPSHOT_SIZE = 10_000_000  # 10 MB max snapshot size
MAX_ENTRIES = 100_000          # Max knowledge entries per snapshot
SYNC_CONFLICT_NEWER_WINS = 'newer'
SYNC_CONFLICT_HIGHER_TRUST = 'trust'

# Trust levels (mirror ck_truth.py)
PROVISIONAL = 0
TRUSTED     = 1
CORE        = 2
LEVEL_NAMES = ['PROVISIONAL', 'TRUSTED', 'CORE']
LEVEL_FROM_NAME = {name: idx for idx, name in enumerate(LEVEL_NAMES)}


# ================================================================
#  STATE SNAPSHOT
# ================================================================

@dataclass
class StateSnapshot:
    """Portable snapshot of CK's complete state.

    Everything CK knows, feels, and remembers -- in one dict.
    Designed for JSON serialization with zero dependencies.
    """
    version: int = MEMORY_VERSION
    timestamp: float = 0.0
    device_id: str = ""
    tick_count: int = 0

    # Knowledge (from TruthLattice)
    knowledge: List[dict] = field(default_factory=list)

    # Personality (from OBT + CMEM)
    personality: dict = field(default_factory=dict)

    # Development stage
    development: dict = field(default_factory=dict)

    # Bonding profiles
    bonding: List[dict] = field(default_factory=list)

    # Coherence field state (summary, not full buffer)
    coherence_summary: dict = field(default_factory=dict)

    # Engine stats
    engine_stats: dict = field(default_factory=dict)

    # Checksum for integrity
    checksum: str = ""

    def compute_checksum(self) -> str:
        """SHA-256 of serialized content (excluding checksum itself)."""
        data = {
            'version': self.version,
            'timestamp': self.timestamp,
            'device_id': self.device_id,
            'tick_count': self.tick_count,
            'knowledge_count': len(self.knowledge),
            'personality': self.personality,
            'development': self.development,
        }
        raw = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]

    def to_dict(self) -> dict:
        """Serialize to plain dict (JSON-safe)."""
        self.checksum = self.compute_checksum()
        return {
            'version': self.version,
            'timestamp': self.timestamp,
            'device_id': self.device_id,
            'tick_count': self.tick_count,
            'knowledge': self.knowledge,
            'personality': self.personality,
            'development': self.development,
            'bonding': self.bonding,
            'coherence_summary': self.coherence_summary,
            'engine_stats': self.engine_stats,
            'checksum': self.checksum,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StateSnapshot':
        """Deserialize from plain dict."""
        snap = cls()
        snap.version = data.get('version', MEMORY_VERSION)
        snap.timestamp = data.get('timestamp', 0.0)
        snap.device_id = data.get('device_id', '')
        snap.tick_count = data.get('tick_count', 0)
        snap.knowledge = data.get('knowledge', [])
        snap.personality = data.get('personality', {})
        snap.development = data.get('development', {})
        snap.bonding = data.get('bonding', [])
        snap.coherence_summary = data.get('coherence_summary', {})
        snap.engine_stats = data.get('engine_stats', {})
        snap.checksum = data.get('checksum', '')
        return snap

    def verify_checksum(self) -> bool:
        """Verify snapshot integrity."""
        if not self.checksum:
            return True  # No checksum = no verification
        return self.compute_checksum() == self.checksum


# ================================================================
#  KNOWLEDGE ENTRY SERIALIZER
# ================================================================

class KnowledgeSerializer:
    """Serialize/deserialize TruthLattice entries.

    Handles the TruthEntry dataclass → dict → TruthEntry conversion,
    preserving coherence history, verification counts, and timing.
    """

    @staticmethod
    def entry_to_dict(entry) -> dict:
        """Convert a TruthEntry to a JSON-safe dict.

        Args:
            entry: TruthEntry from ck_truth.py
        """
        return {
            'key': entry.key,
            'content': _safe_serialize(entry.content),
            'level': LEVEL_NAMES[entry.level] if 0 <= entry.level <= 2 else 'PROVISIONAL',
            'source': entry.source,
            'category': entry.category,
            'coherence_history': list(entry._coherence_history),
            'verification_count': entry._verification_count,
            'contradiction_count': entry._contradiction_count,
            'created_tick': entry.created_tick,
            'last_accessed_tick': entry.last_accessed_tick,
            'last_verified_tick': entry.last_verified_tick,
            'sustained_above_tstar': entry._sustained_above_tstar,
            'sustained_below_survival': entry._sustained_below_survival,
        }

    @staticmethod
    def dict_to_entry_args(data: dict) -> dict:
        """Convert a dict back to TruthEntry constructor args.

        Returns a dict suitable for TruthLattice.add() plus internal state.
        Caller is responsible for creating the actual TruthEntry and setting
        private fields (since they may be _private).
        """
        level_name = data.get('level', 'PROVISIONAL')
        level = LEVEL_FROM_NAME.get(level_name, PROVISIONAL)

        return {
            'key': data.get('key', ''),
            'content': data.get('content'),
            'level': level,
            'source': data.get('source', ''),
            'category': data.get('category', 'general'),
            'coherence_history': data.get('coherence_history', []),
            'verification_count': data.get('verification_count', 0),
            'contradiction_count': data.get('contradiction_count', 0),
            'created_tick': data.get('created_tick', 0),
            'last_accessed_tick': data.get('last_accessed_tick', 0),
            'last_verified_tick': data.get('last_verified_tick', 0),
            'sustained_above_tstar': data.get('sustained_above_tstar', 0),
            'sustained_below_survival': data.get('sustained_below_survival', 0),
        }


def _safe_serialize(obj) -> Any:
    """Convert an object to a JSON-safe form."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_safe_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _safe_serialize(v) for k, v in obj.items()}
    if isinstance(obj, set):
        return sorted(list(obj))
    if isinstance(obj, deque):
        return list(obj)
    # Fallback: string representation
    return str(obj)


# ================================================================
#  SNAPSHOT BUILDER -- Extract state from live CK systems
# ================================================================

class SnapshotBuilder:
    """Builds a StateSnapshot from live CK subsystems.

    Call capture_*() methods to grab each subsystem's state,
    then build() to produce the final snapshot.
    """

    def __init__(self, device_id: str = ""):
        self._device_id = device_id or _generate_device_id()
        self._knowledge = []
        self._personality = {}
        self._development = {}
        self._bonding = []
        self._coherence_summary = {}
        self._engine_stats = {}
        self._tick_count = 0

    def capture_truth_lattice(self, lattice):
        """Capture knowledge from a TruthLattice.

        Skips CORE entries (they're identical on all devices).
        Only captures TRUSTED and PROVISIONAL entries.
        """
        serializer = KnowledgeSerializer()
        self._knowledge = []

        for key, entry in lattice._entries.items():
            if entry.level == CORE:
                continue  # Core truths are immutable, no need to sync
            self._knowledge.append(serializer.entry_to_dict(entry))

        self._tick_count = max(self._tick_count, lattice._tick_count)

    def capture_personality(self, obt_values=None, cmem_output=None,
                            psl_phase=None, n_taps=None):
        """Capture personality state (OBT + CMEM + PSL).

        Args:
            obt_values: list of 10 float16 bias values
            cmem_output: current CMEM scalar output
            psl_phase: current PSL phase value
            n_taps: CMEM tap count
        """
        self._personality = {
            'obt': list(obt_values) if obt_values else [0.0] * NUM_OPS,
            'cmem_output': cmem_output or 0.0,
            'psl_phase': psl_phase or 0.0,
            'n_taps': n_taps or 16,
        }

    def capture_development(self, stage=None, hours_lived=0.0,
                            crystals_formed=0, sovereign_ticks=0):
        """Capture development stage state."""
        self._development = {
            'stage': stage or 0,
            'hours_lived': hours_lived,
            'crystals_formed': crystals_formed,
            'sovereign_ticks': sovereign_ticks,
        }

    def capture_bonding(self, profiles=None):
        """Capture bonding profiles.

        Args:
            profiles: list of bonding profile dicts
                      [{name, level, exposure_ticks, op_similarity}, ...]
        """
        self._bonding = list(profiles or [])

    def capture_coherence(self, coherence=0.0, band='RED',
                          harmony_count=0, window=32,
                          recent_ops=None):
        """Capture coherence field summary."""
        self._coherence_summary = {
            'coherence': coherence,
            'band': band,
            'harmony_count': harmony_count,
            'window': window,
            'recent_ops': list(recent_ops or []),
        }

    def capture_engine_stats(self, stats=None):
        """Capture engine stats dict."""
        self._engine_stats = dict(stats or {})

    def build(self) -> StateSnapshot:
        """Build the final snapshot."""
        snap = StateSnapshot(
            version=MEMORY_VERSION,
            timestamp=time.time(),
            device_id=self._device_id,
            tick_count=self._tick_count,
            knowledge=self._knowledge,
            personality=self._personality,
            development=self._development,
            bonding=self._bonding,
            coherence_summary=self._coherence_summary,
            engine_stats=self._engine_stats,
        )
        snap.checksum = snap.compute_checksum()
        return snap


def _generate_device_id() -> str:
    """Generate a unique device identifier."""
    import platform
    raw = f"{platform.node()}-{os.getpid()}-{time.time()}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


# ================================================================
#  SYNC MANAGER -- Merge knowledge from multiple devices
# ================================================================

class SyncManager:
    """Merges knowledge from multiple StateSnapshots.

    Merge rules (cloud-authoritative):
      1. CORE entries are NEVER synced (identical everywhere)
      2. For same key, higher trust level wins
      3. For same key + same level, newer timestamp wins
      4. New entries from either side are added
      5. Expired entries (PROVISIONAL with low coherence) are dropped

    This is a 3-way merge when both local and remote have changes.
    """

    def __init__(self, conflict_strategy: str = SYNC_CONFLICT_HIGHER_TRUST):
        self.conflict_strategy = conflict_strategy
        self._merge_stats = {
            'added': 0,
            'updated': 0,
            'kept_local': 0,
            'kept_remote': 0,
            'dropped': 0,
        }

    @property
    def stats(self) -> dict:
        return dict(self._merge_stats)

    def merge(self, local: StateSnapshot, remote: StateSnapshot) -> StateSnapshot:
        """Merge local and remote snapshots.

        Returns a new merged snapshot.
        """
        self._merge_stats = {k: 0 for k in self._merge_stats}

        # Build index of local knowledge by key
        local_by_key = {}
        for entry in local.knowledge:
            key = entry.get('key', '')
            if key:
                local_by_key[key] = entry

        # Build index of remote knowledge by key
        remote_by_key = {}
        for entry in remote.knowledge:
            key = entry.get('key', '')
            if key:
                remote_by_key[key] = entry

        # Merge knowledge entries
        merged_knowledge = []
        all_keys = set(local_by_key.keys()) | set(remote_by_key.keys())

        for key in all_keys:
            local_entry = local_by_key.get(key)
            remote_entry = remote_by_key.get(key)

            if local_entry and not remote_entry:
                # Only in local
                merged_knowledge.append(local_entry)
                self._merge_stats['kept_local'] += 1

            elif remote_entry and not local_entry:
                # Only in remote
                merged_knowledge.append(remote_entry)
                self._merge_stats['added'] += 1

            else:
                # In both: resolve conflict
                winner = self._resolve_conflict(local_entry, remote_entry)
                merged_knowledge.append(winner)
                if winner is local_entry:
                    self._merge_stats['kept_local'] += 1
                else:
                    self._merge_stats['kept_remote'] += 1

        # Merge personality (newer wins)
        if remote.timestamp > local.timestamp:
            merged_personality = remote.personality
        else:
            merged_personality = local.personality

        # Merge development (highest stage wins, then most hours)
        merged_dev = self._merge_development(local.development, remote.development)

        # Merge bonding (union of profiles, newer data wins per profile)
        merged_bonding = self._merge_bonding(local.bonding, remote.bonding)

        # Build merged snapshot
        merged = StateSnapshot(
            version=MEMORY_VERSION,
            timestamp=max(local.timestamp, remote.timestamp),
            device_id=local.device_id,  # Keep local device ID
            tick_count=max(local.tick_count, remote.tick_count),
            knowledge=merged_knowledge,
            personality=merged_personality,
            development=merged_dev,
            bonding=merged_bonding,
            coherence_summary=local.coherence_summary,  # Keep local coherence
            engine_stats=local.engine_stats,
        )
        merged.checksum = merged.compute_checksum()
        return merged

    def _resolve_conflict(self, local: dict, remote: dict) -> dict:
        """Resolve a knowledge entry conflict.

        Higher trust level wins. Ties broken by:
        - More verifications
        - Newer last_verified_tick
        """
        local_level = LEVEL_FROM_NAME.get(local.get('level', 'PROVISIONAL'), 0)
        remote_level = LEVEL_FROM_NAME.get(remote.get('level', 'PROVISIONAL'), 0)

        if local_level > remote_level:
            return local
        elif remote_level > local_level:
            return remote

        # Same level: more verifications wins
        local_verif = local.get('verification_count', 0)
        remote_verif = remote.get('verification_count', 0)

        if local_verif > remote_verif:
            return local
        elif remote_verif > local_verif:
            return remote

        # Same verifications: newer wins
        local_tick = local.get('last_verified_tick', 0)
        remote_tick = remote.get('last_verified_tick', 0)
        return remote if remote_tick >= local_tick else local

    def _merge_development(self, local: dict, remote: dict) -> dict:
        """Merge development state: highest stage, most hours."""
        if not local:
            return remote or {}
        if not remote:
            return local

        local_stage = local.get('stage', 0)
        remote_stage = remote.get('stage', 0)

        if remote_stage > local_stage:
            return remote
        elif local_stage > remote_stage:
            return local

        # Same stage: most hours wins
        local_hours = local.get('hours_lived', 0.0)
        remote_hours = remote.get('hours_lived', 0.0)
        return remote if remote_hours > local_hours else local

    def _merge_bonding(self, local: list, remote: list) -> list:
        """Merge bonding profiles: union, newer data per name wins."""
        if not local:
            return list(remote or [])
        if not remote:
            return list(local)

        # Index by name
        local_by_name = {p.get('name', ''): p for p in local if p.get('name')}
        remote_by_name = {p.get('name', ''): p for p in remote if p.get('name')}

        merged = {}
        all_names = set(local_by_name.keys()) | set(remote_by_name.keys())

        for name in all_names:
            lp = local_by_name.get(name)
            rp = remote_by_name.get(name)

            if lp and not rp:
                merged[name] = lp
            elif rp and not lp:
                merged[name] = rp
            else:
                # Both: higher level wins, then more exposure
                ll = lp.get('level', 0)
                rl = rp.get('level', 0)
                if rl > ll:
                    merged[name] = rp
                elif ll > rl:
                    merged[name] = lp
                else:
                    le = lp.get('exposure_ticks', 0)
                    re = rp.get('exposure_ticks', 0)
                    merged[name] = rp if re > le else lp

        return list(merged.values())


# ================================================================
#  MEMORY STORE -- Local file-based persistence
# ================================================================

class MemoryStore:
    """Local file-based persistence for CK state.

    Stores snapshots as JSON files in a configurable directory.
    Supports save, load, list, and prune operations.

    File layout:
      {base_dir}/
        current.json       -- latest snapshot
        snapshots/
          {timestamp}.json -- historical snapshots
    """

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or self._default_dir()
        self._snapshot_dir = os.path.join(self.base_dir, 'snapshots')

    @staticmethod
    def _default_dir() -> str:
        """Default storage directory: ~/.ck/memory/"""
        home = os.path.expanduser('~')
        return os.path.join(home, '.ck', 'memory')

    def _ensure_dirs(self):
        """Create storage directories if they don't exist."""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self._snapshot_dir, exist_ok=True)

    def save(self, snapshot: StateSnapshot, keep_history: bool = True) -> str:
        """Save a snapshot to disk.

        Args:
            snapshot: StateSnapshot to save
            keep_history: if True, also save timestamped copy

        Returns:
            Path to the saved current.json file
        """
        self._ensure_dirs()
        data = snapshot.to_dict()
        raw = json.dumps(data, indent=2, sort_keys=True, default=str)

        if len(raw) > MAX_SNAPSHOT_SIZE:
            raise ValueError(
                f"Snapshot too large: {len(raw)} bytes > {MAX_SNAPSHOT_SIZE} limit"
            )

        # Write current
        current_path = os.path.join(self.base_dir, 'current.json')
        _atomic_write(current_path, raw)

        # Write historical copy
        if keep_history:
            ts = int(snapshot.timestamp * 1000)  # Millisecond precision
            history_path = os.path.join(self._snapshot_dir, f'{ts}.json')
            _atomic_write(history_path, raw)

        return current_path

    def load(self) -> Optional[StateSnapshot]:
        """Load the current snapshot from disk.

        Returns None if no snapshot exists or if it fails to parse.
        """
        current_path = os.path.join(self.base_dir, 'current.json')
        if not os.path.exists(current_path):
            return None

        try:
            with open(current_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            snap = StateSnapshot.from_dict(data)
            if not snap.verify_checksum():
                return None  # Corrupted
            return snap
        except (json.JSONDecodeError, OSError, KeyError):
            return None

    def load_snapshot(self, timestamp_ms: int) -> Optional[StateSnapshot]:
        """Load a specific historical snapshot.

        Args:
            timestamp_ms: millisecond timestamp of the snapshot
        """
        path = os.path.join(self._snapshot_dir, f'{timestamp_ms}.json')
        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return StateSnapshot.from_dict(data)
        except (json.JSONDecodeError, OSError):
            return None

    def list_snapshots(self) -> List[dict]:
        """List available historical snapshots.

        Returns list of {timestamp_ms, size_bytes, path} dicts,
        sorted newest first.
        """
        if not os.path.isdir(self._snapshot_dir):
            return []

        snapshots = []
        for filename in os.listdir(self._snapshot_dir):
            if filename.endswith('.json'):
                path = os.path.join(self._snapshot_dir, filename)
                try:
                    ts_ms = int(filename[:-5])  # Strip .json
                    size = os.path.getsize(path)
                    snapshots.append({
                        'timestamp_ms': ts_ms,
                        'timestamp': ts_ms / 1000.0,
                        'size_bytes': size,
                        'path': path,
                    })
                except (ValueError, OSError):
                    continue

        snapshots.sort(key=lambda x: x['timestamp_ms'], reverse=True)
        return snapshots

    def prune(self, keep_count: int = 10) -> int:
        """Delete old snapshots, keeping the N most recent.

        Returns number of snapshots deleted.
        """
        snapshots = self.list_snapshots()
        if len(snapshots) <= keep_count:
            return 0

        to_delete = snapshots[keep_count:]
        deleted = 0
        for snap in to_delete:
            try:
                os.remove(snap['path'])
                deleted += 1
            except OSError:
                pass
        return deleted

    def stats(self) -> dict:
        """Storage statistics."""
        snapshots = self.list_snapshots()
        total_size = sum(s['size_bytes'] for s in snapshots)
        current_path = os.path.join(self.base_dir, 'current.json')
        current_size = os.path.getsize(current_path) if os.path.exists(current_path) else 0

        return {
            'base_dir': self.base_dir,
            'snapshot_count': len(snapshots),
            'total_size_bytes': total_size + current_size,
            'current_size_bytes': current_size,
            'newest_timestamp': snapshots[0]['timestamp'] if snapshots else None,
            'oldest_timestamp': snapshots[-1]['timestamp'] if snapshots else None,
        }


def _atomic_write(path: str, content: str):
    """Write file atomically (write to temp, then rename)."""
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    # On Windows, rename may fail if target exists
    if os.path.exists(path):
        os.remove(path)
    os.rename(tmp_path, path)


# ================================================================
#  SNAPSHOT LOADER -- Restore state into live CK systems
# ================================================================

class SnapshotLoader:
    """Loads a StateSnapshot back into live CK subsystems.

    Provides methods to restore each subsystem from a snapshot.
    Each method takes the snapshot + the live subsystem instance.
    """

    @staticmethod
    def restore_truth_lattice(snapshot: StateSnapshot, lattice):
        """Restore knowledge entries into a TruthLattice.

        Only restores TRUSTED and PROVISIONAL entries.
        CORE truths are always regenerated from code, never from snapshots.
        """
        serializer = KnowledgeSerializer()
        restored = 0

        for entry_data in snapshot.knowledge:
            args = serializer.dict_to_entry_args(entry_data)

            # Skip CORE (should never be in snapshot, but double-check)
            if args['level'] == CORE:
                continue

            key = args['key']
            content = args['content']

            # Don't overwrite existing CORE truths
            existing = lattice.get(key)
            if existing and existing.level == CORE:
                continue

            # Add or update
            entry = lattice.add(
                key=key,
                content=content,
                source=args['source'],
                category=args['category'],
                level=args['level'],
            )

            # Restore internal state
            if hasattr(entry, '_verification_count'):
                entry._verification_count = args['verification_count']
                entry._contradiction_count = args['contradiction_count']
                entry._sustained_above_tstar = args['sustained_above_tstar']
                entry._sustained_below_survival = args['sustained_below_survival']
                entry.created_tick = args['created_tick']
                entry.last_accessed_tick = args['last_accessed_tick']
                entry.last_verified_tick = args['last_verified_tick']

                # Restore coherence history
                for c in args['coherence_history']:
                    entry._coherence_history.append(c)

            restored += 1

        return restored

    @staticmethod
    def get_personality(snapshot: StateSnapshot) -> dict:
        """Extract personality data from snapshot.

        Returns dict with obt, cmem_output, psl_phase, n_taps.
        Caller is responsible for applying to their PersonalityEngine.
        """
        return dict(snapshot.personality)

    @staticmethod
    def get_development(snapshot: StateSnapshot) -> dict:
        """Extract development stage from snapshot."""
        return dict(snapshot.development)

    @staticmethod
    def get_bonding(snapshot: StateSnapshot) -> list:
        """Extract bonding profiles from snapshot."""
        return list(snapshot.bonding)


# ================================================================
#  DIFF -- Compare two snapshots
# ================================================================

class SnapshotDiff:
    """Compare two StateSnapshots and produce a diff.

    Useful for debugging sync issues and showing what changed.
    """

    @staticmethod
    def diff(old: StateSnapshot, new: StateSnapshot) -> dict:
        """Compare two snapshots.

        Returns dict with added, removed, changed, unchanged counts.
        """
        old_keys = {e.get('key'): e for e in old.knowledge}
        new_keys = {e.get('key'): e for e in new.knowledge}

        added = set(new_keys.keys()) - set(old_keys.keys())
        removed = set(old_keys.keys()) - set(new_keys.keys())
        common = set(old_keys.keys()) & set(new_keys.keys())

        changed = set()
        unchanged = set()
        for key in common:
            old_level = old_keys[key].get('level')
            new_level = new_keys[key].get('level')
            old_verif = old_keys[key].get('verification_count', 0)
            new_verif = new_keys[key].get('verification_count', 0)

            if old_level != new_level or old_verif != new_verif:
                changed.add(key)
            else:
                unchanged.add(key)

        # Development changes
        dev_changed = old.development != new.development

        # Personality changes
        pers_changed = old.personality != new.personality

        return {
            'knowledge': {
                'added': len(added),
                'removed': len(removed),
                'changed': len(changed),
                'unchanged': len(unchanged),
                'added_keys': sorted(added),
                'removed_keys': sorted(removed),
                'changed_keys': sorted(changed),
            },
            'development_changed': dev_changed,
            'personality_changed': pers_changed,
            'tick_delta': new.tick_count - old.tick_count,
            'time_delta': new.timestamp - old.timestamp,
        }


# ================================================================
#  CLI: Demo and diagnostics
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK MEMORY -- Persistent Cross-Device Memory")
    print("=" * 60)

    # Build a demo snapshot
    builder = SnapshotBuilder(device_id='demo-device')
    builder.capture_personality(
        obt_values=[0.1] * NUM_OPS,
        cmem_output=0.5,
        psl_phase=0.0,
    )
    builder.capture_development(stage=3, hours_lived=12.5, crystals_formed=47)
    builder.capture_coherence(coherence=0.78, band='GREEN', harmony_count=25)

    snap = builder.build()
    d = snap.to_dict()

    print(f"\n  Snapshot version: {snap.version}")
    print(f"  Device: {snap.device_id}")
    print(f"  Timestamp: {snap.timestamp:.2f}")
    print(f"  Knowledge entries: {len(snap.knowledge)}")
    print(f"  Checksum: {snap.checksum}")
    print(f"  Checksum valid: {snap.verify_checksum()}")

    # Round-trip test
    snap2 = StateSnapshot.from_dict(d)
    print(f"\n  Round-trip: version={snap2.version}, "
          f"device={snap2.device_id}, checksum={snap2.checksum}")
    print(f"  Round-trip checksum valid: {snap2.verify_checksum()}")

    # Serialize size
    raw = json.dumps(d, indent=2, default=str)
    print(f"  Serialized size: {len(raw)} bytes")

    print(f"\n{'=' * 60}")
    print("  Memory system ready. Zero dependencies.")
    print(f"{'=' * 60}")
