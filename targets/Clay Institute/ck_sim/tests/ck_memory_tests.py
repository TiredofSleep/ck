"""
ck_memory_tests.py -- Tests for Persistent Cross-Device Memory
===============================================================
Validates: StateSnapshot, KnowledgeSerializer, SnapshotBuilder,
SyncManager, MemoryStore, SnapshotLoader, SnapshotDiff,
plus full round-trip and merge integration.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import json
import os
import sys
import time
import tempfile
import shutil

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  CONSTANTS TESTS
# ================================================================

class TestMemoryConstants(unittest.TestCase):
    """Validate memory module constants and level mappings."""

    def test_memory_version_positive(self):
        from ck_sim.ck_memory import MEMORY_VERSION
        self.assertGreater(MEMORY_VERSION, 0)
        self.assertEqual(MEMORY_VERSION, 1)

    def test_max_snapshot_size(self):
        from ck_sim.ck_memory import MAX_SNAPSHOT_SIZE
        self.assertEqual(MAX_SNAPSHOT_SIZE, 10_000_000)

    def test_max_entries(self):
        from ck_sim.ck_memory import MAX_ENTRIES
        self.assertEqual(MAX_ENTRIES, 100_000)

    def test_level_values(self):
        from ck_sim.ck_memory import PROVISIONAL, TRUSTED, CORE
        self.assertEqual(PROVISIONAL, 0)
        self.assertEqual(TRUSTED, 1)
        self.assertEqual(CORE, 2)

    def test_level_names(self):
        from ck_sim.ck_memory import LEVEL_NAMES
        self.assertEqual(LEVEL_NAMES[0], 'PROVISIONAL')
        self.assertEqual(LEVEL_NAMES[1], 'TRUSTED')
        self.assertEqual(LEVEL_NAMES[2], 'CORE')

    def test_level_from_name_round_trip(self):
        from ck_sim.ck_memory import LEVEL_NAMES, LEVEL_FROM_NAME
        for idx, name in enumerate(LEVEL_NAMES):
            self.assertEqual(LEVEL_FROM_NAME[name], idx)

    def test_conflict_strategy_constants(self):
        from ck_sim.ck_memory import SYNC_CONFLICT_NEWER_WINS, SYNC_CONFLICT_HIGHER_TRUST
        self.assertEqual(SYNC_CONFLICT_NEWER_WINS, 'newer')
        self.assertEqual(SYNC_CONFLICT_HIGHER_TRUST, 'trust')

    def test_levels_match_truth_module(self):
        """Memory level integers must match ck_truth.py."""
        from ck_sim.ck_memory import PROVISIONAL, TRUSTED, CORE
        from ck_sim.ck_truth import PROVISIONAL as T_PROV, TRUSTED as T_TRUST, CORE as T_CORE
        self.assertEqual(PROVISIONAL, T_PROV)
        self.assertEqual(TRUSTED, T_TRUST)
        self.assertEqual(CORE, T_CORE)


# ================================================================
#  STATE SNAPSHOT TESTS
# ================================================================

class TestStateSnapshot(unittest.TestCase):
    """Validate StateSnapshot creation, serialization, checksum."""

    def test_default_construction(self):
        from ck_sim.ck_memory import StateSnapshot, MEMORY_VERSION
        snap = StateSnapshot()
        self.assertEqual(snap.version, MEMORY_VERSION)
        self.assertEqual(snap.timestamp, 0.0)
        self.assertEqual(snap.device_id, "")
        self.assertEqual(snap.knowledge, [])
        self.assertEqual(snap.personality, {})
        self.assertEqual(snap.development, {})
        self.assertEqual(snap.bonding, [])
        self.assertEqual(snap.coherence_summary, {})
        self.assertEqual(snap.engine_stats, {})
        self.assertEqual(snap.checksum, "")

    def test_checksum_is_hex_string(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=100.0, device_id='test')
        cs = snap.compute_checksum()
        self.assertEqual(len(cs), 16)  # Truncated SHA-256
        # All hex chars
        for c in cs:
            self.assertIn(c, '0123456789abcdef')

    def test_checksum_deterministic(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=42.0, device_id='dev1', tick_count=100)
        cs1 = snap.compute_checksum()
        cs2 = snap.compute_checksum()
        self.assertEqual(cs1, cs2)

    def test_checksum_changes_with_data(self):
        from ck_sim.ck_memory import StateSnapshot
        s1 = StateSnapshot(timestamp=1.0, device_id='a')
        s2 = StateSnapshot(timestamp=2.0, device_id='a')
        self.assertNotEqual(s1.compute_checksum(), s2.compute_checksum())

    def test_to_dict_sets_checksum(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=50.0, device_id='d1')
        d = snap.to_dict()
        self.assertIn('checksum', d)
        self.assertTrue(len(d['checksum']) > 0)

    def test_to_dict_has_all_fields(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=1.0, device_id='test')
        d = snap.to_dict()
        required_keys = [
            'version', 'timestamp', 'device_id', 'tick_count',
            'knowledge', 'personality', 'development', 'bonding',
            'coherence_summary', 'engine_stats', 'checksum',
        ]
        for key in required_keys:
            self.assertIn(key, d, f"Missing key: {key}")

    def test_to_dict_is_json_safe(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(
            timestamp=1.0, device_id='x',
            knowledge=[{'key': 'test', 'level': 'PROVISIONAL'}],
            personality={'obt': [0.1] * 10},
        )
        d = snap.to_dict()
        raw = json.dumps(d, default=str)
        self.assertIsInstance(raw, str)
        self.assertGreater(len(raw), 10)

    def test_from_dict_round_trip(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(
            timestamp=99.9, device_id='dev42', tick_count=500,
            knowledge=[{'key': 'k1', 'level': 'TRUSTED'}],
            personality={'obt': [0.5] * 10},
            development={'stage': 3},
            bonding=[{'name': 'Alice', 'level': 2}],
            coherence_summary={'coherence': 0.8},
            engine_stats={'ticks': 500},
        )
        d = snap.to_dict()
        snap2 = StateSnapshot.from_dict(d)
        self.assertAlmostEqual(snap2.timestamp, 99.9)
        self.assertEqual(snap2.device_id, 'dev42')
        self.assertEqual(snap2.tick_count, 500)
        self.assertEqual(len(snap2.knowledge), 1)
        self.assertEqual(snap2.knowledge[0]['key'], 'k1')
        self.assertEqual(snap2.personality['obt'], [0.5] * 10)
        self.assertEqual(snap2.development['stage'], 3)
        self.assertEqual(snap2.bonding[0]['name'], 'Alice')

    def test_verify_checksum_pass(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=1.0, device_id='t')
        snap.checksum = snap.compute_checksum()
        self.assertTrue(snap.verify_checksum())

    def test_verify_checksum_fail_on_tamper(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot(timestamp=1.0, device_id='t')
        snap.checksum = snap.compute_checksum()
        snap.timestamp = 999.0  # Tamper
        self.assertFalse(snap.verify_checksum())

    def test_verify_checksum_empty_passes(self):
        """No checksum = no verification (acceptable for new snapshots)."""
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot()
        self.assertTrue(snap.verify_checksum())

    def test_from_dict_missing_fields_defaults(self):
        from ck_sim.ck_memory import StateSnapshot
        snap = StateSnapshot.from_dict({})
        self.assertEqual(snap.knowledge, [])
        self.assertEqual(snap.personality, {})
        self.assertEqual(snap.device_id, '')


# ================================================================
#  SAFE SERIALIZE TESTS
# ================================================================

class TestSafeSerialize(unittest.TestCase):
    """Validate _safe_serialize handles various types."""

    def test_primitives(self):
        from ck_sim.ck_memory import _safe_serialize
        self.assertEqual(_safe_serialize("hello"), "hello")
        self.assertEqual(_safe_serialize(42), 42)
        self.assertAlmostEqual(_safe_serialize(3.14), 3.14)
        self.assertEqual(_safe_serialize(True), True)
        self.assertIsNone(_safe_serialize(None))

    def test_list(self):
        from ck_sim.ck_memory import _safe_serialize
        self.assertEqual(_safe_serialize([1, 2, 3]), [1, 2, 3])

    def test_tuple_becomes_list(self):
        from ck_sim.ck_memory import _safe_serialize
        self.assertEqual(_safe_serialize((1, 2)), [1, 2])

    def test_dict(self):
        from ck_sim.ck_memory import _safe_serialize
        result = _safe_serialize({'a': 1, 'b': [2, 3]})
        self.assertEqual(result, {'a': 1, 'b': [2, 3]})

    def test_set_becomes_sorted_list(self):
        from ck_sim.ck_memory import _safe_serialize
        result = _safe_serialize({3, 1, 2})
        self.assertEqual(result, [1, 2, 3])

    def test_deque_becomes_list(self):
        from collections import deque
        from ck_sim.ck_memory import _safe_serialize
        result = _safe_serialize(deque([10, 20, 30]))
        self.assertEqual(result, [10, 20, 30])

    def test_custom_object_becomes_string(self):
        from ck_sim.ck_memory import _safe_serialize

        class Foo:
            def __str__(self):
                return "foo_obj"

        result = _safe_serialize(Foo())
        self.assertEqual(result, "foo_obj")


# ================================================================
#  KNOWLEDGE SERIALIZER TESTS
# ================================================================

class TestKnowledgeSerializer(unittest.TestCase):
    """Validate TruthEntry <-> dict round-trip."""

    def _make_entry(self):
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL
        entry = TruthEntry(
            key='test_key',
            content='test_content',
            level=PROVISIONAL,
            source='test',
            category='general',
            created_tick=10,
            last_accessed_tick=20,
            last_verified_tick=15,
        )
        entry._verification_count = 5
        entry._contradiction_count = 1
        entry._sustained_above_tstar = 12
        entry._sustained_below_survival = 0
        entry._coherence_history.append(0.8)
        entry._coherence_history.append(0.75)
        return entry

    def test_entry_to_dict_has_key(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        entry = self._make_entry()
        d = KnowledgeSerializer.entry_to_dict(entry)
        self.assertEqual(d['key'], 'test_key')

    def test_entry_to_dict_has_level_name(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        entry = self._make_entry()
        d = KnowledgeSerializer.entry_to_dict(entry)
        self.assertEqual(d['level'], 'PROVISIONAL')

    def test_entry_to_dict_preserves_counts(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        entry = self._make_entry()
        d = KnowledgeSerializer.entry_to_dict(entry)
        self.assertEqual(d['verification_count'], 5)
        self.assertEqual(d['contradiction_count'], 1)
        self.assertEqual(d['sustained_above_tstar'], 12)

    def test_entry_to_dict_preserves_coherence_history(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        entry = self._make_entry()
        d = KnowledgeSerializer.entry_to_dict(entry)
        self.assertEqual(len(d['coherence_history']), 2)
        self.assertAlmostEqual(d['coherence_history'][0], 0.8)

    def test_dict_to_entry_args_round_trip(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        entry = self._make_entry()
        d = KnowledgeSerializer.entry_to_dict(entry)
        args = KnowledgeSerializer.dict_to_entry_args(d)
        self.assertEqual(args['key'], 'test_key')
        self.assertEqual(args['level'], 0)  # PROVISIONAL = 0
        self.assertEqual(args['verification_count'], 5)
        self.assertEqual(args['created_tick'], 10)

    def test_dict_to_entry_args_defaults(self):
        from ck_sim.ck_memory import KnowledgeSerializer
        args = KnowledgeSerializer.dict_to_entry_args({})
        self.assertEqual(args['key'], '')
        self.assertEqual(args['level'], 0)
        self.assertEqual(args['verification_count'], 0)

    def test_trusted_level_round_trip(self):
        from ck_sim.ck_memory import KnowledgeSerializer, TRUSTED
        from ck_sim.ck_truth import TruthEntry
        entry = TruthEntry(key='trusted_k', level=TRUSTED)
        d = KnowledgeSerializer.entry_to_dict(entry)
        self.assertEqual(d['level'], 'TRUSTED')
        args = KnowledgeSerializer.dict_to_entry_args(d)
        self.assertEqual(args['level'], TRUSTED)


# ================================================================
#  SNAPSHOT BUILDER TESTS
# ================================================================

class TestSnapshotBuilder(unittest.TestCase):
    """Validate SnapshotBuilder captures CK subsystem state."""

    def test_build_empty(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder(device_id='test-dev')
        snap = builder.build()
        self.assertEqual(snap.device_id, 'test-dev')
        self.assertEqual(snap.knowledge, [])
        self.assertGreater(snap.timestamp, 0.0)

    def test_build_has_checksum(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder(device_id='d')
        snap = builder.build()
        self.assertTrue(len(snap.checksum) > 0)
        self.assertTrue(snap.verify_checksum())

    def test_auto_device_id(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder()  # No device_id
        snap = builder.build()
        self.assertTrue(len(snap.device_id) > 0)

    def test_capture_personality(self):
        from ck_sim.ck_memory import SnapshotBuilder, NUM_OPS
        builder = SnapshotBuilder(device_id='p')
        builder.capture_personality(
            obt_values=[0.1] * NUM_OPS,
            cmem_output=0.5,
            psl_phase=0.2,
            n_taps=16,
        )
        snap = builder.build()
        self.assertEqual(snap.personality['cmem_output'], 0.5)
        self.assertEqual(snap.personality['psl_phase'], 0.2)
        self.assertEqual(snap.personality['n_taps'], 16)
        self.assertEqual(len(snap.personality['obt']), NUM_OPS)

    def test_capture_development(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder(device_id='d')
        builder.capture_development(stage=4, hours_lived=24.0,
                                     crystals_formed=100, sovereign_ticks=50)
        snap = builder.build()
        self.assertEqual(snap.development['stage'], 4)
        self.assertAlmostEqual(snap.development['hours_lived'], 24.0)
        self.assertEqual(snap.development['crystals_formed'], 100)
        self.assertEqual(snap.development['sovereign_ticks'], 50)

    def test_capture_bonding(self):
        from ck_sim.ck_memory import SnapshotBuilder
        profiles = [
            {'name': 'Alice', 'level': 2, 'exposure_ticks': 100},
            {'name': 'Bob', 'level': 1, 'exposure_ticks': 50},
        ]
        builder = SnapshotBuilder(device_id='b')
        builder.capture_bonding(profiles)
        snap = builder.build()
        self.assertEqual(len(snap.bonding), 2)
        self.assertEqual(snap.bonding[0]['name'], 'Alice')

    def test_capture_coherence(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder(device_id='c')
        builder.capture_coherence(
            coherence=0.8, band='GREEN',
            harmony_count=25, window=32,
            recent_ops=[7, 7, 3, 5],
        )
        snap = builder.build()
        self.assertAlmostEqual(snap.coherence_summary['coherence'], 0.8)
        self.assertEqual(snap.coherence_summary['band'], 'GREEN')
        self.assertEqual(snap.coherence_summary['harmony_count'], 25)
        self.assertEqual(snap.coherence_summary['recent_ops'], [7, 7, 3, 5])

    def test_capture_engine_stats(self):
        from ck_sim.ck_memory import SnapshotBuilder
        builder = SnapshotBuilder(device_id='e')
        builder.capture_engine_stats({'ticks': 1000, 'uptime': 60.0})
        snap = builder.build()
        self.assertEqual(snap.engine_stats['ticks'], 1000)
        self.assertAlmostEqual(snap.engine_stats['uptime'], 60.0)

    def test_capture_truth_lattice_skips_core(self):
        """Builder should skip CORE entries (they never sync)."""
        from ck_sim.ck_memory import SnapshotBuilder, CORE
        from ck_sim.ck_truth import TruthLattice

        lattice = TruthLattice()
        # TruthLattice seeds ~50 core truths at construction
        core_count = len([e for e in lattice._entries.values() if e.level == CORE])
        self.assertGreater(core_count, 0)

        # Add one provisional entry
        lattice.add('user_fact', 'sky is blue', source='obs', category='world')

        builder = SnapshotBuilder(device_id='tl')
        builder.capture_truth_lattice(lattice)
        snap = builder.build()

        # Only the provisional entry should be captured, not core truths
        self.assertEqual(len(snap.knowledge), 1)
        self.assertEqual(snap.knowledge[0]['key'], 'user_fact')

    def test_capture_truth_lattice_includes_trusted(self):
        """Builder captures TRUSTED entries."""
        from ck_sim.ck_memory import SnapshotBuilder, TRUSTED
        from ck_sim.ck_truth import TruthLattice

        lattice = TruthLattice()
        lattice.add('learned_fact', 'cats purr', source='obs',
                     category='world', level=TRUSTED)

        builder = SnapshotBuilder(device_id='tl2')
        builder.capture_truth_lattice(lattice)
        snap = builder.build()

        # Should capture the trusted entry
        trusted_entries = [e for e in snap.knowledge if e['level'] == 'TRUSTED']
        self.assertGreaterEqual(len(trusted_entries), 1)


# ================================================================
#  SYNC MANAGER TESTS
# ================================================================

class TestSyncManager(unittest.TestCase):
    """Validate merge logic for multi-device sync."""

    def _make_snap(self, timestamp=1.0, device='local',
                   knowledge=None, personality=None,
                   development=None, bonding=None, tick_count=0):
        from ck_sim.ck_memory import StateSnapshot
        return StateSnapshot(
            timestamp=timestamp,
            device_id=device,
            tick_count=tick_count,
            knowledge=knowledge or [],
            personality=personality or {},
            development=development or {},
            bonding=bonding or [],
        )

    def test_merge_empty_snapshots(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap()
        remote = self._make_snap()
        merged = mgr.merge(local, remote)
        self.assertEqual(len(merged.knowledge), 0)

    def test_merge_local_only_entries(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[
            {'key': 'k1', 'level': 'PROVISIONAL', 'verification_count': 1},
        ])
        remote = self._make_snap()
        merged = mgr.merge(local, remote)
        self.assertEqual(len(merged.knowledge), 1)
        self.assertEqual(merged.knowledge[0]['key'], 'k1')
        self.assertEqual(mgr.stats['kept_local'], 1)

    def test_merge_remote_only_entries(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap()
        remote = self._make_snap(knowledge=[
            {'key': 'r1', 'level': 'TRUSTED', 'verification_count': 5},
        ])
        merged = mgr.merge(local, remote)
        self.assertEqual(len(merged.knowledge), 1)
        self.assertEqual(merged.knowledge[0]['key'], 'r1')
        self.assertEqual(mgr.stats['added'], 1)

    def test_merge_union_disjoint(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[
            {'key': 'a', 'level': 'PROVISIONAL'},
        ])
        remote = self._make_snap(knowledge=[
            {'key': 'b', 'level': 'TRUSTED'},
        ])
        merged = mgr.merge(local, remote)
        keys = {e['key'] for e in merged.knowledge}
        self.assertEqual(keys, {'a', 'b'})

    def test_merge_higher_trust_wins(self):
        """Same key, different trust: higher level wins."""
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[
            {'key': 'fact', 'level': 'PROVISIONAL', 'verification_count': 2,
             'last_verified_tick': 10},
        ])
        remote = self._make_snap(knowledge=[
            {'key': 'fact', 'level': 'TRUSTED', 'verification_count': 5,
             'last_verified_tick': 20},
        ])
        merged = mgr.merge(local, remote)
        self.assertEqual(len(merged.knowledge), 1)
        self.assertEqual(merged.knowledge[0]['level'], 'TRUSTED')
        self.assertEqual(mgr.stats['kept_remote'], 1)

    def test_merge_same_level_more_verifications_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[
            {'key': 'x', 'level': 'TRUSTED', 'verification_count': 10,
             'last_verified_tick': 5},
        ])
        remote = self._make_snap(knowledge=[
            {'key': 'x', 'level': 'TRUSTED', 'verification_count': 3,
             'last_verified_tick': 50},
        ])
        merged = mgr.merge(local, remote)
        # Local has more verifications
        self.assertEqual(merged.knowledge[0]['verification_count'], 10)

    def test_merge_same_level_same_verifs_newer_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[
            {'key': 'y', 'level': 'TRUSTED', 'verification_count': 5,
             'last_verified_tick': 10},
        ])
        remote = self._make_snap(knowledge=[
            {'key': 'y', 'level': 'TRUSTED', 'verification_count': 5,
             'last_verified_tick': 50},
        ])
        merged = mgr.merge(local, remote)
        # Remote is newer
        self.assertEqual(merged.knowledge[0]['last_verified_tick'], 50)

    def test_merge_personality_newer_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(
            timestamp=10.0,
            personality={'obt': [0.1] * 10, 'cmem_output': 0.3},
        )
        remote = self._make_snap(
            timestamp=20.0,
            personality={'obt': [0.9] * 10, 'cmem_output': 0.8},
        )
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.personality['cmem_output'], 0.8)

    def test_merge_personality_local_wins_if_newer(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(
            timestamp=30.0,
            personality={'obt': [0.5] * 10, 'cmem_output': 0.5},
        )
        remote = self._make_snap(
            timestamp=10.0,
            personality={'obt': [0.1] * 10, 'cmem_output': 0.1},
        )
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.personality['cmem_output'], 0.5)

    def test_merge_development_higher_stage_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(
            development={'stage': 2, 'hours_lived': 5.0},
        )
        remote = self._make_snap(
            development={'stage': 4, 'hours_lived': 20.0},
        )
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.development['stage'], 4)

    def test_merge_development_same_stage_more_hours_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(
            development={'stage': 3, 'hours_lived': 50.0},
        )
        remote = self._make_snap(
            development={'stage': 3, 'hours_lived': 10.0},
        )
        merged = mgr.merge(local, remote)
        self.assertAlmostEqual(merged.development['hours_lived'], 50.0)

    def test_merge_development_empty_local(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(development={})
        remote = self._make_snap(development={'stage': 2})
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.development['stage'], 2)

    def test_merge_bonding_union(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(bonding=[
            {'name': 'Alice', 'level': 2, 'exposure_ticks': 100},
        ])
        remote = self._make_snap(bonding=[
            {'name': 'Bob', 'level': 1, 'exposure_ticks': 50},
        ])
        merged = mgr.merge(local, remote)
        names = {p['name'] for p in merged.bonding}
        self.assertEqual(names, {'Alice', 'Bob'})

    def test_merge_bonding_overlap_higher_level_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(bonding=[
            {'name': 'Alice', 'level': 1, 'exposure_ticks': 100},
        ])
        remote = self._make_snap(bonding=[
            {'name': 'Alice', 'level': 3, 'exposure_ticks': 50},
        ])
        merged = mgr.merge(local, remote)
        alice = [p for p in merged.bonding if p['name'] == 'Alice'][0]
        self.assertEqual(alice['level'], 3)

    def test_merge_bonding_same_level_more_exposure_wins(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(bonding=[
            {'name': 'Alice', 'level': 2, 'exposure_ticks': 200},
        ])
        remote = self._make_snap(bonding=[
            {'name': 'Alice', 'level': 2, 'exposure_ticks': 50},
        ])
        merged = mgr.merge(local, remote)
        alice = [p for p in merged.bonding if p['name'] == 'Alice'][0]
        self.assertEqual(alice['exposure_ticks'], 200)

    def test_merge_timestamp_takes_max(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(timestamp=10.0)
        remote = self._make_snap(timestamp=30.0)
        merged = mgr.merge(local, remote)
        self.assertAlmostEqual(merged.timestamp, 30.0)

    def test_merge_tick_count_takes_max(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(tick_count=100)
        remote = self._make_snap(tick_count=300)
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.tick_count, 300)

    def test_merge_keeps_local_device_id(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(device='local-phone')
        remote = self._make_snap(device='cloud-server')
        merged = mgr.merge(local, remote)
        self.assertEqual(merged.device_id, 'local-phone')

    def test_merge_stats_reset_each_call(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[{'key': 'a', 'level': 'PROVISIONAL'}])
        remote = self._make_snap()
        mgr.merge(local, remote)
        self.assertEqual(mgr.stats['kept_local'], 1)
        # Second call should reset
        mgr.merge(self._make_snap(), self._make_snap())
        self.assertEqual(mgr.stats['kept_local'], 0)

    def test_merged_snapshot_has_valid_checksum(self):
        from ck_sim.ck_memory import SyncManager
        mgr = SyncManager()
        local = self._make_snap(knowledge=[{'key': 'a', 'level': 'PROVISIONAL'}])
        remote = self._make_snap(knowledge=[{'key': 'b', 'level': 'TRUSTED'}])
        merged = mgr.merge(local, remote)
        self.assertTrue(merged.verify_checksum())


# ================================================================
#  MEMORY STORE TESTS (temp dir)
# ================================================================

class TestMemoryStore(unittest.TestCase):
    """Validate local file-based persistence."""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp(prefix='ck_memory_test_')

    def tearDown(self):
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _make_snap(self, ts=None, device='test'):
        from ck_sim.ck_memory import StateSnapshot
        return StateSnapshot(
            timestamp=ts or time.time(),
            device_id=device,
            tick_count=100,
            knowledge=[{'key': 'k1', 'level': 'PROVISIONAL'}],
            personality={'obt': [0.1] * 10},
            development={'stage': 2},
        )

    def test_save_creates_current_json(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap()
        path = store.save(snap)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith('current.json'))

    def test_save_creates_history(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=12345.678)
        store.save(snap)
        history_dir = os.path.join(self._tmpdir, 'snapshots')
        self.assertTrue(os.path.isdir(history_dir))
        files = os.listdir(history_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('.json'))

    def test_save_no_history(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap()
        store.save(snap, keep_history=False)
        history_dir = os.path.join(self._tmpdir, 'snapshots')
        if os.path.isdir(history_dir):
            self.assertEqual(len(os.listdir(history_dir)), 0)

    def test_load_round_trip(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=999.0)
        store.save(snap)
        loaded = store.load()
        self.assertIsNotNone(loaded)
        self.assertAlmostEqual(loaded.timestamp, 999.0)
        self.assertEqual(loaded.device_id, 'test')
        self.assertEqual(len(loaded.knowledge), 1)

    def test_load_returns_none_if_no_file(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        self.assertIsNone(store.load())

    def test_load_returns_none_on_corrupt_json(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        os.makedirs(self._tmpdir, exist_ok=True)
        with open(os.path.join(self._tmpdir, 'current.json'), 'w') as f:
            f.write("not valid json{{{")
        self.assertIsNone(store.load())

    def test_load_returns_none_on_bad_checksum(self):
        from ck_sim.ck_memory import MemoryStore, StateSnapshot
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=50.0)
        d = snap.to_dict()
        d['checksum'] = 'badhash1234abcde'  # Wrong checksum
        os.makedirs(self._tmpdir, exist_ok=True)
        with open(os.path.join(self._tmpdir, 'current.json'), 'w') as f:
            json.dump(d, f)
        self.assertIsNone(store.load())

    def test_list_snapshots_empty(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        self.assertEqual(store.list_snapshots(), [])

    def test_list_snapshots_multiple(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        for ts in [100.0, 200.0, 300.0]:
            snap = self._make_snap(ts=ts)
            store.save(snap)
        snaps = store.list_snapshots()
        self.assertEqual(len(snaps), 3)
        # Should be sorted newest first
        self.assertGreater(snaps[0]['timestamp_ms'], snaps[1]['timestamp_ms'])

    def test_load_snapshot_by_timestamp(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=42000.0)
        store.save(snap)
        snaps = store.list_snapshots()
        ts_ms = snaps[0]['timestamp_ms']
        loaded = store.load_snapshot(ts_ms)
        self.assertIsNotNone(loaded)
        self.assertAlmostEqual(loaded.timestamp, 42000.0)

    def test_load_snapshot_nonexistent(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        self.assertIsNone(store.load_snapshot(99999999))

    def test_prune_keeps_n_newest(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        # Save 5 snapshots with distinct timestamps
        for i in range(5):
            snap = self._make_snap(ts=1000.0 + i * 100)
            store.save(snap)

        deleted = store.prune(keep_count=2)
        self.assertEqual(deleted, 3)
        remaining = store.list_snapshots()
        self.assertEqual(len(remaining), 2)

    def test_prune_no_op_if_few_snapshots(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=1.0)
        store.save(snap)
        deleted = store.prune(keep_count=10)
        self.assertEqual(deleted, 0)

    def test_stats(self):
        from ck_sim.ck_memory import MemoryStore
        store = MemoryStore(base_dir=self._tmpdir)
        snap = self._make_snap(ts=500.0)
        store.save(snap)
        stats = store.stats()
        self.assertEqual(stats['snapshot_count'], 1)
        self.assertEqual(stats['base_dir'], self._tmpdir)
        self.assertGreater(stats['total_size_bytes'], 0)
        self.assertGreater(stats['current_size_bytes'], 0)

    def test_save_too_large_raises(self):
        from ck_sim.ck_memory import MemoryStore, StateSnapshot, MAX_SNAPSHOT_SIZE
        store = MemoryStore(base_dir=self._tmpdir)
        # Create an absurdly large snapshot
        huge_knowledge = [{'key': f'k_{i}', 'data': 'x' * 1000}
                          for i in range(15000)]
        snap = StateSnapshot(
            timestamp=1.0, device_id='big',
            knowledge=huge_knowledge,
        )
        with self.assertRaises(ValueError):
            store.save(snap)


# ================================================================
#  SNAPSHOT LOADER TESTS
# ================================================================

class TestSnapshotLoader(unittest.TestCase):
    """Validate restoring state from snapshots into live CK systems."""

    def test_restore_truth_lattice_basic(self):
        from ck_sim.ck_memory import (
            SnapshotBuilder, SnapshotLoader, StateSnapshot,
        )
        from ck_sim.ck_truth import TruthLattice

        # Build a lattice with one user fact
        src = TruthLattice()
        src.add('test_fact', 'hello', source='user', category='social')

        # Capture to snapshot
        builder = SnapshotBuilder(device_id='src')
        builder.capture_truth_lattice(src)
        snap = builder.build()

        # Restore into fresh lattice
        dst = TruthLattice()
        count = SnapshotLoader.restore_truth_lattice(snap, dst)
        self.assertEqual(count, 1)
        entry = dst.get('test_fact')
        self.assertIsNotNone(entry)
        self.assertEqual(entry.content, 'hello')

    def test_restore_skips_core(self):
        """Restoration should never overwrite CORE truths."""
        from ck_sim.ck_memory import (
            SnapshotLoader, StateSnapshot, CORE,
        )
        from ck_sim.ck_truth import TruthLattice

        # Create snapshot with a CORE-level entry (shouldn't happen but test defense)
        snap = StateSnapshot(
            knowledge=[{
                'key': 'op_count',  # This is a CORE truth
                'content': 999,     # Wrong value!
                'level': 'CORE',
                'source': 'hacker',
                'category': 'math',
                'coherence_history': [],
                'verification_count': 0,
                'contradiction_count': 0,
                'created_tick': 0,
                'last_accessed_tick': 0,
                'last_verified_tick': 0,
                'sustained_above_tstar': 0,
                'sustained_below_survival': 0,
            }],
        )

        dst = TruthLattice()
        count = SnapshotLoader.restore_truth_lattice(snap, dst)
        self.assertEqual(count, 0)  # Should not restore
        # Core truth should still be correct
        entry = dst.get('op_count')
        self.assertIsNotNone(entry)
        self.assertEqual(entry.content, 10)  # NUM_OPS = 10

    def test_restore_preserves_internal_state(self):
        from ck_sim.ck_memory import (
            SnapshotBuilder, SnapshotLoader,
        )
        from ck_sim.ck_truth import TruthLattice

        src = TruthLattice()
        entry = src.add('fact_a', True, source='obs')
        # Simulate some coherence history
        for i in range(5):
            src.record_coherence('fact_a', 0.8, tick=i)

        builder = SnapshotBuilder(device_id='s')
        builder.capture_truth_lattice(src)
        snap = builder.build()

        dst = TruthLattice()
        SnapshotLoader.restore_truth_lattice(snap, dst)
        restored = dst.get('fact_a')
        self.assertIsNotNone(restored)
        self.assertEqual(restored._verification_count, 5)
        self.assertEqual(len(restored._coherence_history), 5)

    def test_get_personality(self):
        from ck_sim.ck_memory import SnapshotLoader, StateSnapshot
        snap = StateSnapshot(
            personality={'obt': [0.5] * 10, 'cmem_output': 0.3},
        )
        p = SnapshotLoader.get_personality(snap)
        self.assertEqual(p['cmem_output'], 0.3)
        self.assertEqual(len(p['obt']), 10)

    def test_get_development(self):
        from ck_sim.ck_memory import SnapshotLoader, StateSnapshot
        snap = StateSnapshot(
            development={'stage': 4, 'hours_lived': 100.0},
        )
        d = SnapshotLoader.get_development(snap)
        self.assertEqual(d['stage'], 4)

    def test_get_bonding(self):
        from ck_sim.ck_memory import SnapshotLoader, StateSnapshot
        snap = StateSnapshot(
            bonding=[{'name': 'A', 'level': 2}],
        )
        b = SnapshotLoader.get_bonding(snap)
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0]['name'], 'A')

    def test_get_returns_copy(self):
        """Modifications to returned data shouldn't affect snapshot."""
        from ck_sim.ck_memory import SnapshotLoader, StateSnapshot
        snap = StateSnapshot(
            personality={'obt': [0.5] * 10},
            development={'stage': 3},
            bonding=[{'name': 'X'}],
        )
        p = SnapshotLoader.get_personality(snap)
        p['obt'] = [0.0] * 10
        self.assertEqual(snap.personality['obt'], [0.5] * 10)

        d = SnapshotLoader.get_development(snap)
        d['stage'] = 999
        self.assertEqual(snap.development['stage'], 3)


# ================================================================
#  SNAPSHOT DIFF TESTS
# ================================================================

class TestSnapshotDiff(unittest.TestCase):
    """Validate diff between two snapshots."""

    def _make_snap(self, knowledge=None, dev=None, pers=None,
                   tick=0, ts=0.0):
        from ck_sim.ck_memory import StateSnapshot
        return StateSnapshot(
            timestamp=ts,
            tick_count=tick,
            knowledge=knowledge or [],
            development=dev or {},
            personality=pers or {},
        )

    def test_diff_identical(self):
        from ck_sim.ck_memory import SnapshotDiff
        snap = self._make_snap(knowledge=[
            {'key': 'a', 'level': 'TRUSTED', 'verification_count': 3},
        ])
        result = SnapshotDiff.diff(snap, snap)
        self.assertEqual(result['knowledge']['added'], 0)
        self.assertEqual(result['knowledge']['removed'], 0)
        self.assertEqual(result['knowledge']['changed'], 0)
        self.assertEqual(result['knowledge']['unchanged'], 1)

    def test_diff_added(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(knowledge=[])
        new = self._make_snap(knowledge=[
            {'key': 'new_fact', 'level': 'PROVISIONAL', 'verification_count': 0},
        ])
        result = SnapshotDiff.diff(old, new)
        self.assertEqual(result['knowledge']['added'], 1)
        self.assertIn('new_fact', result['knowledge']['added_keys'])

    def test_diff_removed(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(knowledge=[
            {'key': 'old_fact', 'level': 'PROVISIONAL', 'verification_count': 0},
        ])
        new = self._make_snap(knowledge=[])
        result = SnapshotDiff.diff(old, new)
        self.assertEqual(result['knowledge']['removed'], 1)
        self.assertIn('old_fact', result['knowledge']['removed_keys'])

    def test_diff_changed_level(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(knowledge=[
            {'key': 'f', 'level': 'PROVISIONAL', 'verification_count': 0},
        ])
        new = self._make_snap(knowledge=[
            {'key': 'f', 'level': 'TRUSTED', 'verification_count': 0},
        ])
        result = SnapshotDiff.diff(old, new)
        self.assertEqual(result['knowledge']['changed'], 1)
        self.assertIn('f', result['knowledge']['changed_keys'])

    def test_diff_changed_verifications(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(knowledge=[
            {'key': 'f', 'level': 'TRUSTED', 'verification_count': 3},
        ])
        new = self._make_snap(knowledge=[
            {'key': 'f', 'level': 'TRUSTED', 'verification_count': 10},
        ])
        result = SnapshotDiff.diff(old, new)
        self.assertEqual(result['knowledge']['changed'], 1)

    def test_diff_development_changed(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(dev={'stage': 2})
        new = self._make_snap(dev={'stage': 4})
        result = SnapshotDiff.diff(old, new)
        self.assertTrue(result['development_changed'])

    def test_diff_personality_changed(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(pers={'obt': [0.1] * 10})
        new = self._make_snap(pers={'obt': [0.9] * 10})
        result = SnapshotDiff.diff(old, new)
        self.assertTrue(result['personality_changed'])

    def test_diff_tick_delta(self):
        from ck_sim.ck_memory import SnapshotDiff
        old = self._make_snap(tick=10, ts=1.0)
        new = self._make_snap(tick=50, ts=5.0)
        result = SnapshotDiff.diff(old, new)
        self.assertEqual(result['tick_delta'], 40)
        self.assertAlmostEqual(result['time_delta'], 4.0)


# ================================================================
#  FULL INTEGRATION: BUILD → SAVE → LOAD → MERGE → RESTORE
# ================================================================

class TestFullIntegration(unittest.TestCase):
    """End-to-end: build snapshot, save to disk, load, merge, restore."""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp(prefix='ck_mem_integ_')

    def tearDown(self):
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def test_full_round_trip(self):
        from ck_sim.ck_memory import (
            SnapshotBuilder, MemoryStore, SnapshotLoader,
        )
        from ck_sim.ck_truth import TruthLattice
        from ck_sim.ck_sim_heartbeat import NUM_OPS

        # 1. Build a CK state
        lattice = TruthLattice()
        lattice.add('user_name', 'Brayden', source='conversation', category='social')
        lattice.add('sky_color', 'blue', source='observation', category='world')

        builder = SnapshotBuilder(device_id='phone-1')
        builder.capture_truth_lattice(lattice)
        builder.capture_personality(
            obt_values=[0.3] * NUM_OPS, cmem_output=0.4, psl_phase=0.1,
        )
        builder.capture_development(stage=3, hours_lived=48.0)
        builder.capture_bonding([{'name': 'Brayden', 'level': 3, 'exposure_ticks': 5000}])
        builder.capture_coherence(coherence=0.82, band='GREEN', harmony_count=26)
        snap = builder.build()

        # 2. Save to disk
        store = MemoryStore(base_dir=self._tmpdir)
        store.save(snap)

        # 3. Load from disk
        loaded = store.load()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.device_id, 'phone-1')
        self.assertEqual(len(loaded.knowledge), 2)
        self.assertTrue(loaded.verify_checksum())

        # 4. Restore into fresh lattice
        dst_lattice = TruthLattice()
        count = SnapshotLoader.restore_truth_lattice(loaded, dst_lattice)
        self.assertEqual(count, 2)
        self.assertEqual(dst_lattice.get('user_name').content, 'Brayden')
        self.assertEqual(dst_lattice.get('sky_color').content, 'blue')

        # 5. Verify personality / dev / bonding extraction
        p = SnapshotLoader.get_personality(loaded)
        self.assertAlmostEqual(p['cmem_output'], 0.4)
        d = SnapshotLoader.get_development(loaded)
        self.assertEqual(d['stage'], 3)
        b = SnapshotLoader.get_bonding(loaded)
        self.assertEqual(b[0]['name'], 'Brayden')

    def test_multi_device_merge_cycle(self):
        """Simulate phone and desktop CKs syncing via cloud."""
        from ck_sim.ck_memory import (
            SnapshotBuilder, SyncManager, SnapshotDiff,
        )
        from ck_sim.ck_truth import TruthLattice

        # Phone CK: knows user name + sky color
        phone_lattice = TruthLattice()
        phone_lattice.add('user_name', 'Brayden', source='voice')
        phone_lattice.add('sky_color', 'blue', source='camera')

        phone_builder = SnapshotBuilder(device_id='phone')
        phone_builder.capture_truth_lattice(phone_lattice)
        phone_builder.capture_development(stage=3, hours_lived=20.0)
        phone_snap = phone_builder.build()

        # Desktop CK: knows user name (TRUSTED) + keyboard preference
        desktop_lattice = TruthLattice()
        entry = desktop_lattice.add('user_name', 'Brayden', source='keyboard',
                                     level=1)  # TRUSTED
        desktop_lattice.add('keyboard_pref', 'mechanical', source='obs')

        desktop_builder = SnapshotBuilder(device_id='desktop')
        desktop_builder.capture_truth_lattice(desktop_lattice)
        desktop_builder.capture_development(stage=4, hours_lived=100.0)
        desktop_snap = desktop_builder.build()

        # Merge
        mgr = SyncManager()
        merged = mgr.merge(phone_snap, desktop_snap)

        # Should have all 3 entries
        keys = {e['key'] for e in merged.knowledge}
        self.assertIn('user_name', keys)
        self.assertIn('sky_color', keys)
        self.assertIn('keyboard_pref', keys)

        # user_name: desktop's TRUSTED version should win over phone's PROVISIONAL
        user_entry = [e for e in merged.knowledge if e['key'] == 'user_name'][0]
        self.assertEqual(user_entry['level'], 'TRUSTED')

        # Development: desktop stage 4 > phone stage 3
        self.assertEqual(merged.development['stage'], 4)

        # Diff
        diff = SnapshotDiff.diff(phone_snap, merged)
        self.assertGreater(diff['knowledge']['added'], 0)  # keyboard_pref is new
        self.assertTrue(diff['development_changed'])

    def test_save_and_prune_history(self):
        from ck_sim.ck_memory import MemoryStore, StateSnapshot
        store = MemoryStore(base_dir=self._tmpdir)

        # Save 10 snapshots
        for i in range(10):
            snap = StateSnapshot(
                timestamp=1000.0 + i * 10,
                device_id='pruner',
                tick_count=i * 50,
            )
            store.save(snap)

        self.assertEqual(len(store.list_snapshots()), 10)

        # Prune to 3
        deleted = store.prune(keep_count=3)
        self.assertEqual(deleted, 7)
        self.assertEqual(len(store.list_snapshots()), 3)

        # Current should still load
        loaded = store.load()
        self.assertIsNotNone(loaded)


# ================================================================
#  EDGE CASES
# ================================================================

class TestEdgeCases(unittest.TestCase):
    """Edge cases and defensive behavior."""

    def test_snapshot_with_special_content_types(self):
        """Content can be various types -- all must serialize cleanly."""
        from ck_sim.ck_memory import KnowledgeSerializer
        from ck_sim.ck_truth import TruthEntry, PROVISIONAL

        for content in [42, 3.14, True, None, "text",
                        [1, 2, 3], {'a': 'b'}, (5, 6)]:
            entry = TruthEntry(key='test', content=content, level=PROVISIONAL)
            d = KnowledgeSerializer.entry_to_dict(entry)
            raw = json.dumps(d, default=str)
            self.assertIsInstance(raw, str)

    def test_merge_with_empty_keys_ignored(self):
        from ck_sim.ck_memory import SyncManager, StateSnapshot
        mgr = SyncManager()
        local = StateSnapshot(knowledge=[{'key': '', 'level': 'PROVISIONAL'}])
        remote = StateSnapshot(knowledge=[{'key': 'real', 'level': 'TRUSTED'}])
        merged = mgr.merge(local, remote)
        # Empty key should be ignored, only 'real' kept
        keys = {e['key'] for e in merged.knowledge}
        self.assertIn('real', keys)
        self.assertNotIn('', keys)

    def test_bonding_merge_empty_name_ignored(self):
        from ck_sim.ck_memory import SyncManager, StateSnapshot
        mgr = SyncManager()
        local = StateSnapshot(bonding=[{'name': '', 'level': 1}])
        remote = StateSnapshot(bonding=[{'name': 'Alice', 'level': 2}])
        merged = mgr.merge(local, remote)
        names = {p['name'] for p in merged.bonding}
        self.assertIn('Alice', names)
        self.assertNotIn('', names)

    def test_generate_device_id_is_string(self):
        from ck_sim.ck_memory import _generate_device_id
        did = _generate_device_id()
        self.assertIsInstance(did, str)
        self.assertEqual(len(did), 12)

    def test_atomic_write_creates_file(self):
        from ck_sim.ck_memory import _atomic_write
        path = os.path.join(tempfile.mkdtemp(), 'test_atomic.txt')
        _atomic_write(path, 'hello world')
        with open(path, 'r') as f:
            self.assertEqual(f.read(), 'hello world')
        # Clean up
        os.remove(path)
        os.rmdir(os.path.dirname(path))

    def test_overwrite_existing_file(self):
        from ck_sim.ck_memory import _atomic_write
        tmpdir = tempfile.mkdtemp()
        path = os.path.join(tmpdir, 'test.txt')
        _atomic_write(path, 'first')
        _atomic_write(path, 'second')
        with open(path, 'r') as f:
            self.assertEqual(f.read(), 'second')
        os.remove(path)
        os.rmdir(tmpdir)


# ================================================================
#  IMPORT TESTS
# ================================================================

class TestImports(unittest.TestCase):
    """Verify clean imports."""

    def test_import_module(self):
        import ck_sim.ck_memory
        self.assertTrue(hasattr(ck_sim.ck_memory, 'StateSnapshot'))

    def test_import_all_public_classes(self):
        from ck_sim.ck_memory import (
            StateSnapshot, KnowledgeSerializer, SnapshotBuilder,
            SyncManager, MemoryStore, SnapshotLoader, SnapshotDiff,
        )
        self.assertIsNotNone(StateSnapshot)
        self.assertIsNotNone(KnowledgeSerializer)
        self.assertIsNotNone(SnapshotBuilder)
        self.assertIsNotNone(SyncManager)
        self.assertIsNotNone(MemoryStore)
        self.assertIsNotNone(SnapshotLoader)
        self.assertIsNotNone(SnapshotDiff)

    def test_import_constants(self):
        from ck_sim.ck_memory import (
            MEMORY_VERSION, MAX_SNAPSHOT_SIZE, MAX_ENTRIES,
            PROVISIONAL, TRUSTED, CORE, LEVEL_NAMES, LEVEL_FROM_NAME,
        )
        self.assertEqual(len(LEVEL_NAMES), 3)


# ================================================================
#  RUN
# ================================================================

if __name__ == '__main__':
    unittest.main()
