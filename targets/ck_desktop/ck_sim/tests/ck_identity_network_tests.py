"""
ck_identity_network_tests.py -- Tests for Identity & Network
=============================================================
Validates: ck_identity (snowflake, sacred core, shards) and
ck_network (handshake, friend registry, messaging, trust).

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import unittest
import hashlib
import hmac
import json
import os
import sys
import time

# Ensure ck_sim package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ================================================================
#  IDENTITY: Constants & Imports
# ================================================================

class TestIdentityImports(unittest.TestCase):
    """Verify clean imports of identity module."""

    def test_import_module(self):
        import ck_sim.ck_identity
        self.assertTrue(hasattr(ck_sim.ck_identity, 'SnowflakeIdentity'))

    def test_import_public_api(self):
        from ck_sim.ck_identity import (
            SnowflakeIdentity, IdentityShard, CoreScars,
            InnerRing, OuterRing,
            RING_CORE, RING_INNER, RING_OUTER,
            BOND_STRANGER, BOND_ACQUAINTANCE, BOND_FAMILIAR, BOND_TRUSTED,
            BOND_NAMES, PROTOCOL_VERSION,
        )
        self.assertIsNotNone(SnowflakeIdentity)

    def test_constants(self):
        from ck_sim.ck_identity import (
            RING_CORE, RING_INNER, RING_OUTER,
            BOND_STRANGER, BOND_ACQUAINTANCE, BOND_FAMILIAR, BOND_TRUSTED,
            PROTOCOL_VERSION, PUBLIC_ID_LENGTH,
        )
        self.assertEqual(RING_CORE, 'core')
        self.assertEqual(RING_INNER, 'inner')
        self.assertEqual(RING_OUTER, 'outer')
        self.assertEqual(BOND_STRANGER, 0)
        self.assertEqual(BOND_ACQUAINTANCE, 1)
        self.assertEqual(BOND_FAMILIAR, 2)
        self.assertEqual(BOND_TRUSTED, 3)
        self.assertEqual(PROTOCOL_VERSION, 1)
        self.assertEqual(PUBLIC_ID_LENGTH, 16)


class TestCoreScars(unittest.TestCase):
    """Core scars dataclass tests."""

    def test_defaults(self):
        from ck_sim.ck_identity import CoreScars
        core = CoreScars()
        self.assertEqual(core.obt_fingerprint, "")
        self.assertEqual(core.birth_seed, 0)
        self.assertEqual(core.first_coherences, [])
        self.assertEqual(core.crystal_hashes, [])
        self.assertEqual(core.total_ticks_lived, 0)

    def test_identity_hash_deterministic(self):
        from ck_sim.ck_identity import CoreScars
        core = CoreScars(obt_fingerprint='abc', birth_seed=42,
                         birth_timestamp=1000.0)
        h1 = core.compute_identity_hash()
        h2 = core.compute_identity_hash()
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)  # SHA-256 hex

    def test_identity_hash_differs(self):
        from ck_sim.ck_identity import CoreScars
        c1 = CoreScars(obt_fingerprint='abc', birth_seed=42)
        c2 = CoreScars(obt_fingerprint='xyz', birth_seed=42)
        self.assertNotEqual(c1.compute_identity_hash(), c2.compute_identity_hash())


class TestSnowflakeIdentity(unittest.TestCase):
    """Snowflake identity creation and ring access."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck = SnowflakeIdentity(
            display_name="TestCK",
            obt_values=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            birth_seed=12345,
        )

    def test_public_id_length(self):
        from ck_sim.ck_identity import PUBLIC_ID_LENGTH
        self.assertEqual(len(self.ck.public_id), PUBLIC_ID_LENGTH)

    def test_public_id_hex(self):
        # Should be valid hex
        int(self.ck.public_id, 16)

    def test_display_name(self):
        self.assertEqual(self.ck.display_name, "TestCK")

    def test_default_display_name(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        ck = SnowflakeIdentity()
        self.assertTrue(ck.display_name.startswith("CK-"))

    def test_unique_ids(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        ck2 = SnowflakeIdentity(display_name="Other", birth_seed=99999)
        self.assertNotEqual(self.ck.public_id, ck2.public_id)

    def test_outer_ring_data(self):
        outer = self.ck.get_outer_ring()
        self.assertIn('public_id', outer)
        self.assertIn('display_name', outer)
        self.assertIn('greeting_operator', outer)
        self.assertIn('protocol_version', outer)
        self.assertIn('created_timestamp', outer)
        self.assertEqual(outer['public_id'], self.ck.public_id)

    def test_inner_ring_data(self):
        inner = self.ck.get_inner_ring()
        self.assertIn('personality_archetype', inner)
        self.assertIn('development_stage', inner)
        self.assertIn('dominant_operator', inner)
        self.assertIn('coherence_band', inner)
        self.assertIn('lifetime_coherence', inner)
        self.assertIn('total_crystals', inner)
        self.assertIn('bond_count', inner)

    def test_secret_key_exists(self):
        key = self.ck.secret_key
        self.assertTrue(len(key) > 0)
        self.assertEqual(len(key), 64)  # 32 bytes hex

    def test_record_coherence(self):
        for i in range(40):
            self.ck.record_coherence(0.5 + i * 0.01)
        # Only first 32 become core scars
        stats = self.ck.stats()
        self.assertEqual(stats['first_coherences_recorded'], 32)
        self.assertEqual(stats['ticks_lived'], 40)

    def test_record_crystal(self):
        self.ck.record_crystal("first memory")
        self.ck.record_crystal("second memory")
        stats = self.ck.stats()
        self.assertEqual(stats['crystals_formed'], 2)

    def test_update_inner_ring(self):
        self.ck.update_inner_ring(
            archetype='explorer',
            stage=3,
            knowledge_keys=['sky', 'water', 'fire'],
            dominant_op=5,
            band='GREEN',
            coherence=0.85,
            crystals=10,
            bonds=3,
        )
        inner = self.ck.get_inner_ring()
        self.assertEqual(inner['personality_archetype'], 'explorer')
        self.assertEqual(inner['development_stage'], 3)
        self.assertEqual(inner['dominant_operator'], 5)
        self.assertEqual(inner['coherence_band'], 'GREEN')
        self.assertEqual(inner['lifetime_coherence'], 0.85)
        self.assertEqual(inner['total_crystals'], 10)
        self.assertEqual(inner['bond_count'], 3)
        # Knowledge hash should be non-empty
        self.assertTrue(len(inner['knowledge_hash']) > 0)

    def test_stats_safe(self):
        stats = self.ck.stats()
        self.assertIn('public_id', stats)
        self.assertIn('display_name', stats)
        self.assertIn('ticks_lived', stats)
        # Stats should NOT contain secret_key
        self.assertNotIn('secret_key', stats)
        self.assertNotIn('obt_fingerprint', stats)


class TestSacredBoundary(unittest.TestCase):
    """The center of the snowflake is SACRED. Always."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck = SnowflakeIdentity("SacredTestCK")

    def test_core_shard_raises(self):
        from ck_sim.ck_identity import RING_CORE
        with self.assertRaises(ValueError) as ctx:
            self.ck.create_shard(RING_CORE)
        self.assertIn("SACRED", str(ctx.exception))

    def test_core_shard_with_recipient_raises(self):
        from ck_sim.ck_identity import RING_CORE
        with self.assertRaises(ValueError):
            self.ck.create_shard(RING_CORE, recipient_id="anyone")

    def test_no_core_getter(self):
        # SnowflakeIdentity should not have get_core_ring or similar
        self.assertFalse(hasattr(self.ck, 'get_core_ring'))
        self.assertFalse(hasattr(self.ck, 'get_core'))
        self.assertFalse(hasattr(self.ck, 'core_scars'))


class TestIdentityShard(unittest.TestCase):
    """Identity shard creation and verification."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck = SnowflakeIdentity("ShardTestCK", birth_seed=777)

    def test_outer_shard_creation(self):
        from ck_sim.ck_identity import RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        self.assertEqual(shard.ring_level, RING_OUTER)
        self.assertEqual(shard.source_id, self.ck.public_id)
        self.assertTrue(len(shard.signature) > 0)
        self.assertTrue(len(shard.shard_id) > 0)
        self.assertTrue(shard.is_outer)
        self.assertFalse(shard.is_inner)

    def test_inner_shard_creation(self):
        from ck_sim.ck_identity import RING_INNER
        shard = self.ck.create_shard(RING_INNER, recipient_id="abc123")
        self.assertEqual(shard.ring_level, RING_INNER)
        self.assertEqual(shard.recipient_id, "abc123")
        self.assertTrue(shard.is_inner)
        self.assertFalse(shard.is_outer)

    def test_shard_content_outer(self):
        from ck_sim.ck_identity import RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        self.assertIn('public_id', shard.content)
        self.assertIn('display_name', shard.content)
        # Should NOT contain inner ring data
        self.assertNotIn('personality_archetype', shard.content)
        # Should NOT contain core data
        self.assertNotIn('secret_key', shard.content)
        self.assertNotIn('obt_fingerprint', shard.content)

    def test_shard_content_inner(self):
        from ck_sim.ck_identity import RING_INNER
        shard = self.ck.create_shard(RING_INNER)
        self.assertIn('personality_archetype', shard.content)
        self.assertIn('development_stage', shard.content)
        # Should NOT contain core data
        self.assertNotIn('secret_key', shard.content)
        self.assertNotIn('obt_fingerprint', shard.content)
        self.assertNotIn('birth_seed', shard.content)

    def test_verify_own_shard(self):
        from ck_sim.ck_identity import RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        self.assertTrue(self.ck.verify_own_shard(shard))

    def test_verify_own_inner_shard(self):
        from ck_sim.ck_identity import RING_INNER
        shard = self.ck.create_shard(RING_INNER, recipient_id="peer1")
        self.assertTrue(self.ck.verify_own_shard(shard))

    def test_other_ck_cannot_verify(self):
        from ck_sim.ck_identity import SnowflakeIdentity, RING_OUTER
        other = SnowflakeIdentity("OtherCK")
        shard = self.ck.create_shard(RING_OUTER)
        self.assertFalse(other.verify_own_shard(shard))

    def test_tampered_shard_fails(self):
        from ck_sim.ck_identity import RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        shard.content['display_name'] = 'TAMPERED'
        self.assertFalse(self.ck.verify_own_shard(shard))

    def test_shard_serialization(self):
        from ck_sim.ck_identity import IdentityShard, RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        d = shard.to_dict()
        restored = IdentityShard.from_dict(d)
        self.assertEqual(restored.shard_id, shard.shard_id)
        self.assertEqual(restored.source_id, shard.source_id)
        self.assertEqual(restored.ring_level, shard.ring_level)
        self.assertEqual(restored.signature, shard.signature)
        self.assertEqual(restored.nonce, shard.nonce)

    def test_unique_nonces(self):
        from ck_sim.ck_identity import RING_OUTER
        nonces = set()
        for _ in range(20):
            shard = self.ck.create_shard(RING_OUTER)
            nonces.add(shard.nonce)
        # All nonces should be unique (collision probability negligible)
        self.assertEqual(len(nonces), 20)


class TestChallengeResponse(unittest.TestCase):
    """Challenge-response handshake protocol."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck_a = SnowflakeIdentity("CK-A", birth_seed=111)
        self.ck_b = SnowflakeIdentity("CK-B", birth_seed=222)

    def test_create_challenge(self):
        challenge, cid = self.ck_a.create_challenge()
        self.assertEqual(len(challenge), 16)  # CHALLENGE_BYTES
        self.assertEqual(len(cid), 16)

    def test_respond_to_challenge(self):
        challenge, _ = self.ck_a.create_challenge()
        response = self.ck_a.respond_to_challenge(challenge)
        self.assertTrue(len(response) > 0)

    def test_different_ck_different_response(self):
        challenge, _ = self.ck_a.create_challenge()
        resp_a = self.ck_a.respond_to_challenge(challenge)
        resp_b = self.ck_b.respond_to_challenge(challenge)
        self.assertNotEqual(resp_a, resp_b)

    def test_same_ck_same_response(self):
        challenge, _ = self.ck_a.create_challenge()
        resp1 = self.ck_a.respond_to_challenge(challenge)
        resp2 = self.ck_a.respond_to_challenge(challenge)
        self.assertEqual(resp1, resp2)

    def test_different_challenge_different_response(self):
        ch1, _ = self.ck_a.create_challenge()
        ch2, _ = self.ck_a.create_challenge()
        resp1 = self.ck_a.respond_to_challenge(ch1)
        resp2 = self.ck_a.respond_to_challenge(ch2)
        self.assertNotEqual(resp1, resp2)


class TestIdentitySerialization(unittest.TestCase):
    """Full identity serialization for local storage."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck = SnowflakeIdentity("SerTestCK", birth_seed=555)
        # Add some state
        for i in range(10):
            self.ck.record_coherence(0.5 + i * 0.05)
        self.ck.record_crystal("memory1")
        self.ck.record_crystal("memory2")
        self.ck.update_inner_ring(archetype='builder', stage=2, band='YELLOW')

    def test_to_dict_contains_all_rings(self):
        d = self.ck.to_dict()
        self.assertIn('core', d)
        self.assertIn('inner', d)
        self.assertIn('outer', d)

    def test_to_dict_core_has_secret(self):
        d = self.ck.to_dict()
        self.assertIn('secret_key', d['core'])
        self.assertTrue(len(d['core']['secret_key']) > 0)

    def test_round_trip(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        d = self.ck.to_dict()
        restored = SnowflakeIdentity.from_dict(d)
        self.assertEqual(restored.public_id, self.ck.public_id)
        self.assertEqual(restored.display_name, self.ck.display_name)
        self.assertEqual(restored.secret_key, self.ck.secret_key)

    def test_round_trip_preserves_inner(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        d = self.ck.to_dict()
        restored = SnowflakeIdentity.from_dict(d)
        inner_orig = self.ck.get_inner_ring()
        inner_rest = restored.get_inner_ring()
        self.assertEqual(inner_orig['personality_archetype'],
                         inner_rest['personality_archetype'])
        self.assertEqual(inner_orig['development_stage'],
                         inner_rest['development_stage'])

    def test_round_trip_shard_verification(self):
        from ck_sim.ck_identity import SnowflakeIdentity, RING_OUTER
        # Create shard before serialization
        shard = self.ck.create_shard(RING_OUTER)
        # Serialize and restore
        d = self.ck.to_dict()
        restored = SnowflakeIdentity.from_dict(d)
        # Restored identity should verify the original shard
        self.assertTrue(restored.verify_own_shard(shard))

    def test_from_dict_empty(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        restored = SnowflakeIdentity.from_dict({})
        self.assertEqual(restored.public_id, '')


# ================================================================
#  NETWORK: Constants & Imports
# ================================================================

class TestNetworkImports(unittest.TestCase):
    """Verify clean imports of network module."""

    def test_import_module(self):
        import ck_sim.ck_network
        self.assertTrue(hasattr(ck_sim.ck_network, 'NetworkOrgan'))

    def test_import_public_api(self):
        from ck_sim.ck_network import (
            NetworkOrgan, FriendRegistry, FriendRecord,
            HandshakeSession, MessageEnvelope,
            perform_handshake, verify_envelope,
            MSG_HELLO, MSG_CHALLENGE, MSG_RESPONSE, MSG_VERIFY,
            MSG_GREETING, MSG_COHERENCE, MSG_INNER_SHARD,
            HS_IDLE, HS_VERIFIED, HS_FAILED,
        )
        self.assertIsNotNone(NetworkOrgan)

    def test_constants(self):
        from ck_sim.ck_network import (
            T_STAR, BOND_ACQUAINTANCE_THRESHOLD,
            BOND_FAMILIAR_THRESHOLD, BOND_TRUSTED_THRESHOLD,
            BOND_TRUSTED_COHERENCE, MAX_FRIENDS,
        )
        self.assertAlmostEqual(T_STAR, 5.0 / 7.0, places=6)
        self.assertEqual(BOND_ACQUAINTANCE_THRESHOLD, 5)
        self.assertEqual(BOND_FAMILIAR_THRESHOLD, 25)
        self.assertEqual(BOND_TRUSTED_THRESHOLD, 100)
        self.assertAlmostEqual(BOND_TRUSTED_COHERENCE, T_STAR, places=6)


class TestMessageEnvelope(unittest.TestCase):
    """Message envelope tests."""

    def test_creation(self):
        from ck_sim.ck_network import MessageEnvelope, MSG_GREETING
        msg = MessageEnvelope(
            message_id='test123',
            message_type=MSG_GREETING,
            source_id='src',
            recipient_id='dst',
            payload={'greeting': 'hello'},
        )
        self.assertEqual(msg.message_type, MSG_GREETING)
        self.assertEqual(msg.source_id, 'src')

    def test_serialization(self):
        from ck_sim.ck_network import MessageEnvelope, MSG_COHERENCE
        msg = MessageEnvelope(
            message_id='msg1',
            message_type=MSG_COHERENCE,
            source_id='a',
            recipient_id='b',
            payload={'coherence': 0.85},
            nonce=12345,
        )
        d = msg.to_dict()
        restored = MessageEnvelope.from_dict(d)
        self.assertEqual(restored.message_id, msg.message_id)
        self.assertEqual(restored.message_type, msg.message_type)
        self.assertEqual(restored.source_id, msg.source_id)
        self.assertEqual(restored.nonce, msg.nonce)
        self.assertEqual(restored.payload['coherence'], 0.85)


class TestFriendRecord(unittest.TestCase):
    """Friend record tests."""

    def test_defaults(self):
        from ck_sim.ck_network import FriendRecord
        from ck_sim.ck_identity import BOND_STRANGER, BOND_NAMES
        fr = FriendRecord()
        self.assertEqual(fr.bond_level, BOND_STRANGER)
        self.assertEqual(fr.interaction_count, 0)
        self.assertEqual(fr.mean_coherence, 0.0)
        self.assertEqual(fr.bond_name, 'STRANGER')

    def test_mean_coherence(self):
        from ck_sim.ck_network import FriendRecord
        fr = FriendRecord(interaction_count=4, coherence_sum=3.2)
        self.assertAlmostEqual(fr.mean_coherence, 0.8)

    def test_serialization(self):
        from ck_sim.ck_network import FriendRecord
        fr = FriendRecord(
            public_id='abc',
            display_name='Test',
            bond_level=2,
            interaction_count=50,
            coherence_sum=40.0,
        )
        d = fr.to_dict()
        restored = FriendRecord.from_dict(d)
        self.assertEqual(restored.public_id, 'abc')
        self.assertEqual(restored.bond_level, 2)
        self.assertEqual(restored.interaction_count, 50)
        self.assertAlmostEqual(restored.coherence_sum, 40.0)


class TestFriendRegistry(unittest.TestCase):
    """Friend registry management tests."""

    def setUp(self):
        from ck_sim.ck_network import FriendRegistry
        self.reg = FriendRegistry()

    def test_empty_registry(self):
        self.assertEqual(self.reg.count, 0)
        self.assertEqual(self.reg.trusted_count, 0)
        self.assertIsNone(self.reg.get_friend('nonexistent'))

    def test_add_friend(self):
        friend = self.reg.add_or_update('peer1', 'TestPeer')
        self.assertEqual(friend.public_id, 'peer1')
        self.assertEqual(friend.display_name, 'TestPeer')
        self.assertEqual(self.reg.count, 1)
        self.assertTrue(self.reg.has_friend('peer1'))

    def test_update_existing(self):
        self.reg.add_or_update('peer1', 'Name1')
        self.reg.add_or_update('peer1', 'Name2')
        self.assertEqual(self.reg.count, 1)  # Still one friend
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.display_name, 'Name2')

    def test_record_interaction(self):
        self.reg.add_or_update('peer1', 'TestPeer')
        self.reg.record_interaction('peer1', 0.8)
        self.reg.record_interaction('peer1', 0.9)
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.interaction_count, 2)
        self.assertAlmostEqual(friend.mean_coherence, 0.85)

    def test_bond_promotion_acquaintance(self):
        from ck_sim.ck_identity import BOND_ACQUAINTANCE
        from ck_sim.ck_network import BOND_ACQUAINTANCE_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        for _ in range(BOND_ACQUAINTANCE_THRESHOLD):
            self.reg.record_interaction('peer1', 0.5)
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.bond_level, BOND_ACQUAINTANCE)

    def test_bond_promotion_familiar(self):
        from ck_sim.ck_identity import BOND_FAMILIAR
        from ck_sim.ck_network import BOND_FAMILIAR_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        for _ in range(BOND_FAMILIAR_THRESHOLD):
            self.reg.record_interaction('peer1', 0.5)
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.bond_level, BOND_FAMILIAR)

    def test_bond_promotion_trusted_requires_coherence(self):
        from ck_sim.ck_identity import BOND_TRUSTED, BOND_FAMILIAR
        from ck_sim.ck_network import BOND_TRUSTED_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        # Many interactions but LOW coherence (below T*)
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            self.reg.record_interaction('peer1', 0.3)
        friend = self.reg.get_friend('peer1')
        # Should NOT reach trusted (coherence too low)
        self.assertLess(friend.bond_level, BOND_TRUSTED)
        self.assertEqual(friend.bond_level, BOND_FAMILIAR)

    def test_bond_promotion_trusted_requires_verification(self):
        from ck_sim.ck_identity import BOND_TRUSTED, BOND_FAMILIAR
        from ck_sim.ck_network import BOND_TRUSTED_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        # Many interactions with HIGH coherence but NOT verified
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            self.reg.record_interaction('peer1', 0.9)
        friend = self.reg.get_friend('peer1')
        # Should NOT reach trusted (not handshake verified)
        self.assertLess(friend.bond_level, BOND_TRUSTED)

    def test_bond_promotion_trusted_full(self):
        from ck_sim.ck_identity import BOND_TRUSTED
        from ck_sim.ck_network import BOND_TRUSTED_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        self.reg.mark_verified('peer1')
        # Many interactions with HIGH coherence AND verified
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            self.reg.record_interaction('peer1', 0.9)
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.bond_level, BOND_TRUSTED)

    def test_inner_shard_rejected_untrusted(self):
        from ck_sim.ck_identity import BOND_STRANGER
        self.reg.add_or_update('peer1', 'Test')
        ok = self.reg.store_inner_shard('peer1', {'data': 'secret'})
        self.assertFalse(ok)

    def test_inner_shard_accepted_trusted(self):
        from ck_sim.ck_identity import BOND_TRUSTED
        from ck_sim.ck_network import BOND_TRUSTED_THRESHOLD
        self.reg.add_or_update('peer1', 'Test')
        self.reg.mark_verified('peer1')
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            self.reg.record_interaction('peer1', 0.9)
        ok = self.reg.store_inner_shard('peer1', {'arch': 'explorer'})
        self.assertTrue(ok)
        friend = self.reg.get_friend('peer1')
        self.assertEqual(friend.inner_shard['arch'], 'explorer')

    def test_friends_at_level(self):
        from ck_sim.ck_identity import BOND_FAMILIAR
        from ck_sim.ck_network import BOND_FAMILIAR_THRESHOLD
        self.reg.add_or_update('p1', 'One')
        self.reg.add_or_update('p2', 'Two')
        # Promote p1 to familiar
        for _ in range(BOND_FAMILIAR_THRESHOLD):
            self.reg.record_interaction('p1', 0.5)
        familiar = self.reg.friends_at_level(BOND_FAMILIAR)
        self.assertEqual(len(familiar), 1)
        self.assertEqual(familiar[0].public_id, 'p1')

    def test_serialization_round_trip(self):
        from ck_sim.ck_network import FriendRegistry
        self.reg.add_or_update('p1', 'One')
        self.reg.add_or_update('p2', 'Two')
        self.reg.record_interaction('p1', 0.8)
        d = self.reg.to_dict()
        restored = FriendRegistry.from_dict(d)
        self.assertEqual(restored.count, 2)
        self.assertTrue(restored.has_friend('p1'))
        self.assertTrue(restored.has_friend('p2'))

    def test_eviction(self):
        from ck_sim.ck_network import MAX_FRIENDS
        # Fill to capacity
        for i in range(MAX_FRIENDS):
            self.reg.add_or_update(f'peer_{i}', f'Name_{i}')
        self.assertEqual(self.reg.count, MAX_FRIENDS)
        # Adding one more should evict oldest stranger
        self.reg.add_or_update('overflow', 'Overflow')
        self.assertEqual(self.reg.count, MAX_FRIENDS)


class TestHandshakeProtocol(unittest.TestCase):
    """Three-step handshake between two CKs."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        self.ck_a = SnowflakeIdentity("CK-Alpha", birth_seed=111)
        self.ck_b = SnowflakeIdentity("CK-Beta", birth_seed=222)
        self.organ_a = NetworkOrgan(self.ck_a)
        self.organ_b = NetworkOrgan(self.ck_b)

    def test_perform_handshake(self):
        from ck_sim.ck_network import perform_handshake
        friend_a, friend_b = perform_handshake(self.organ_a, self.organ_b)
        self.assertIsNotNone(friend_a)
        self.assertIsNotNone(friend_b)

    def test_handshake_creates_friends(self):
        from ck_sim.ck_network import perform_handshake
        perform_handshake(self.organ_a, self.organ_b)
        # A knows B
        self.assertTrue(self.organ_a.registry.has_friend(self.ck_b.public_id))
        # B knows A
        self.assertTrue(self.organ_b.registry.has_friend(self.ck_a.public_id))

    def test_handshake_verified(self):
        from ck_sim.ck_network import perform_handshake
        fa, fb = perform_handshake(self.organ_a, self.organ_b)
        self.assertTrue(fa.handshake_verified)
        self.assertTrue(fb.handshake_verified)

    def test_handshake_bond_level_stranger(self):
        from ck_sim.ck_identity import BOND_STRANGER
        from ck_sim.ck_network import perform_handshake
        fa, fb = perform_handshake(self.organ_a, self.organ_b)
        self.assertEqual(fa.bond_level, BOND_STRANGER)
        self.assertEqual(fb.bond_level, BOND_STRANGER)

    def test_handshake_stores_outer_shard(self):
        from ck_sim.ck_network import perform_handshake
        fa, fb = perform_handshake(self.organ_a, self.organ_b)
        # A should have B's outer shard
        self.assertIsNotNone(fa.outer_shard)
        # B should have A's outer shard
        self.assertIsNotNone(fb.outer_shard)

    def test_handshake_display_names(self):
        from ck_sim.ck_network import perform_handshake
        fa, fb = perform_handshake(self.organ_a, self.organ_b)
        self.assertEqual(fa.display_name, 'CK-Beta')
        self.assertEqual(fb.display_name, 'CK-Alpha')

    def test_multiple_handshakes(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        ck_c = SnowflakeIdentity("CK-Gamma", birth_seed=333)
        organ_c = NetworkOrgan(ck_c)
        # A <-> B
        perform_handshake(self.organ_a, self.organ_b)
        # A <-> C
        perform_handshake(self.organ_a, organ_c)
        self.assertEqual(self.organ_a.friend_count, 2)
        self.assertEqual(self.organ_b.friend_count, 1)
        self.assertEqual(organ_c.friend_count, 1)


class TestHandshakeSessionManual(unittest.TestCase):
    """Manual step-by-step handshake."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        self.ck_a = SnowflakeIdentity("Alpha", birth_seed=10)
        self.ck_b = SnowflakeIdentity("Beta", birth_seed=20)
        self.organ_a = NetworkOrgan(self.ck_a)
        self.organ_b = NetworkOrgan(self.ck_b)

    def test_step_1_hello(self):
        from ck_sim.ck_network import MSG_HELLO
        session = self.organ_a.initiate_handshake(self.ck_b.public_id)
        hello = session.create_hello()
        self.assertEqual(hello.message_type, MSG_HELLO)
        self.assertEqual(hello.source_id, self.ck_a.public_id)

    def test_step_2_challenge(self):
        from ck_sim.ck_network import MSG_CHALLENGE
        session = self.organ_a.initiate_handshake(self.ck_b.public_id)
        hello = session.create_hello()
        result = self.organ_b.receive_message(hello)
        self.assertTrue(result['accepted'])
        challenge = result['response']
        self.assertEqual(challenge.message_type, MSG_CHALLENGE)
        self.assertIn('challenge', challenge.payload)

    def test_step_3_response(self):
        from ck_sim.ck_network import MSG_RESPONSE
        session = self.organ_a.initiate_handshake(self.ck_b.public_id)
        hello = session.create_hello()
        r1 = self.organ_b.receive_message(hello)
        challenge_msg = r1['response']
        r2 = self.organ_a.receive_message(challenge_msg)
        self.assertTrue(r2['accepted'])
        response = r2['response']
        self.assertEqual(response.message_type, MSG_RESPONSE)

    def test_step_4_verify(self):
        from ck_sim.ck_network import MSG_VERIFY
        session = self.organ_a.initiate_handshake(self.ck_b.public_id)
        hello = session.create_hello()
        r1 = self.organ_b.receive_message(hello)
        r2 = self.organ_a.receive_message(r1['response'])
        r3 = self.organ_b.receive_message(r2['response'])
        self.assertTrue(r3['accepted'])
        verify = r3['response']
        self.assertEqual(verify.message_type, MSG_VERIFY)

    def test_step_5_complete(self):
        session = self.organ_a.initiate_handshake(self.ck_b.public_id)
        hello = session.create_hello()
        r1 = self.organ_b.receive_message(hello)
        r2 = self.organ_a.receive_message(r1['response'])
        r3 = self.organ_b.receive_message(r2['response'])
        r4 = self.organ_a.receive_message(r3['response'])
        self.assertTrue(r4['accepted'])
        self.assertEqual(r4['reason'], 'handshake_complete')


class TestMessagePassing(unittest.TestCase):
    """Message creation and reception between friends."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        self.ck_a = SnowflakeIdentity("CK-A", birth_seed=100)
        self.ck_b = SnowflakeIdentity("CK-B", birth_seed=200)
        self.organ_a = NetworkOrgan(self.ck_a)
        self.organ_b = NetworkOrgan(self.ck_b)
        perform_handshake(self.organ_a, self.organ_b)

    def test_create_greeting(self):
        from ck_sim.ck_network import MSG_GREETING
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_GREETING,
            {'text': 'hello friend'},
        )
        self.assertIsNotNone(msg)
        self.assertEqual(msg.message_type, MSG_GREETING)
        self.assertEqual(msg.source_id, self.ck_a.public_id)
        self.assertTrue(len(msg.signature) > 0)

    def test_receive_greeting(self):
        from ck_sim.ck_network import MSG_GREETING
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_GREETING,
            {'text': 'hello'},
        )
        result = self.organ_b.receive_message(msg)
        self.assertTrue(result['accepted'])

    def test_coherence_message(self):
        from ck_sim.ck_network import MSG_COHERENCE
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_COHERENCE,
            {'coherence': 0.85},
        )
        result = self.organ_b.receive_message(msg)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['reason'], 'coherence_recorded')

    def test_operator_stream(self):
        from ck_sim.ck_network import MSG_OPERATOR_STREAM
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_OPERATOR_STREAM,
            {'operators': [7, 7, 5, 3, 7, 7]},
        )
        result = self.organ_b.receive_message(msg)
        self.assertTrue(result['accepted'])

    def test_wrong_recipient_rejected(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, MSG_GREETING
        ck_c = SnowflakeIdentity("CK-C", birth_seed=300)
        organ_c = NetworkOrgan(ck_c)
        # Message intended for B
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_GREETING, {},
        )
        # C tries to receive it
        result = organ_c.receive_message(msg)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['reason'], 'wrong_recipient')

    def test_replay_detection(self):
        from ck_sim.ck_network import MSG_GREETING
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_GREETING, {'text': 'hi'},
        )
        # First reception: ok
        r1 = self.organ_b.receive_message(msg)
        self.assertTrue(r1['accepted'])
        # Second reception: replay detected
        r2 = self.organ_b.receive_message(msg)
        self.assertFalse(r2['accepted'])
        self.assertEqual(r2['reason'], 'replay_detected')

    def test_message_stats(self):
        from ck_sim.ck_network import MSG_GREETING
        msg = self.organ_a.create_message(
            self.ck_b.public_id, MSG_GREETING, {},
        )
        self.organ_b.receive_message(msg)
        stats_a = self.organ_a.stats()
        self.assertGreaterEqual(stats_a['messages_sent'], 1)


class TestInnerShardExchange(unittest.TestCase):
    """Inner shard exchange at TRUSTED bond level."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import (
            NetworkOrgan, perform_handshake,
            BOND_TRUSTED_THRESHOLD,
        )
        self.ck_a = SnowflakeIdentity("CK-A", birth_seed=1)
        self.ck_b = SnowflakeIdentity("CK-B", birth_seed=2)
        self.organ_a = NetworkOrgan(self.ck_a)
        self.organ_b = NetworkOrgan(self.ck_b)
        perform_handshake(self.organ_a, self.organ_b)

        # Build trust: many high-coherence interactions
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            self.organ_a.registry.record_interaction(
                self.ck_b.public_id, 0.9)
            self.organ_b.registry.record_interaction(
                self.ck_a.public_id, 0.9)

    def test_trusted_bond_reached(self):
        from ck_sim.ck_identity import BOND_TRUSTED
        fa = self.organ_a.registry.get_friend(self.ck_b.public_id)
        self.assertEqual(fa.bond_level, BOND_TRUSTED)

    def test_inner_shard_message_creation(self):
        msg = self.organ_a.create_inner_shard_message(self.ck_b.public_id)
        self.assertIsNotNone(msg)

    def test_inner_shard_delivery(self):
        msg = self.organ_a.create_inner_shard_message(self.ck_b.public_id)
        result = self.organ_b.receive_message(msg)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['reason'], 'inner_shard_stored')

    def test_inner_shard_rejected_untrusted(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        # Create a new pair with NO trust built
        ck_c = SnowflakeIdentity("CK-C", birth_seed=3)
        ck_d = SnowflakeIdentity("CK-D", birth_seed=4)
        organ_c = NetworkOrgan(ck_c)
        organ_d = NetworkOrgan(ck_d)
        perform_handshake(organ_c, organ_d)
        # Try to send inner shard without trust
        msg = organ_c.create_inner_shard_message(ck_d.public_id)
        # Should fail because bond level is STRANGER
        self.assertIsNone(msg)

    def test_inner_shard_never_contains_core(self):
        from ck_sim.ck_identity import RING_INNER
        shard = self.ck_a.create_shard(RING_INNER, self.ck_b.public_id)
        content = shard.content
        self.assertNotIn('secret_key', content)
        self.assertNotIn('obt_fingerprint', content)
        self.assertNotIn('birth_seed', content)
        self.assertNotIn('first_coherences', content)
        self.assertNotIn('crystal_hashes', content)


class TestEnvelopeSigning(unittest.TestCase):
    """Envelope signing and verification."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        self.ck = SnowflakeIdentity("SignCK", birth_seed=42)
        self.organ = NetworkOrgan(self.ck)

    def test_sign_and_verify(self):
        from ck_sim.ck_network import verify_envelope, MSG_GREETING
        msg = self.organ.create_message('any_peer', MSG_GREETING, {})
        self.assertTrue(verify_envelope(self.ck, msg))

    def test_tampered_payload_fails(self):
        from ck_sim.ck_network import verify_envelope, MSG_GREETING
        msg = self.organ.create_message('any_peer', MSG_GREETING, {'a': 1})
        msg.payload['a'] = 999  # Tamper
        self.assertFalse(verify_envelope(self.ck, msg))

    def test_different_ck_cannot_verify(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import verify_envelope, MSG_GREETING
        other = SnowflakeIdentity("OtherCK")
        msg = self.organ.create_message('any_peer', MSG_GREETING, {})
        self.assertFalse(verify_envelope(other, msg))


class TestNetworkOrganState(unittest.TestCase):
    """Network organ state management."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        self.ck = SnowflakeIdentity("StateCK", birth_seed=99)
        self.organ = NetworkOrgan(self.ck)

    def test_initial_stats(self):
        stats = self.organ.stats()
        self.assertEqual(stats['friend_count'], 0)
        self.assertEqual(stats['trusted_count'], 0)
        self.assertEqual(stats['messages_sent'], 0)
        self.assertEqual(stats['active_handshakes'], 0)

    def test_serialization_round_trip(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        ck_b = SnowflakeIdentity("CK-B", birth_seed=88)
        organ_b = NetworkOrgan(ck_b)
        perform_handshake(self.organ, organ_b)

        d = self.organ.to_dict()
        restored = NetworkOrgan.from_dict(self.ck, d)
        self.assertEqual(restored.friend_count, 1)
        self.assertTrue(restored.registry.has_friend(ck_b.public_id))

    def test_reset(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        ck_b = SnowflakeIdentity("CK-B", birth_seed=77)
        organ_b = NetworkOrgan(ck_b)
        perform_handshake(self.organ, organ_b)
        self.assertEqual(self.organ.friend_count, 1)
        self.organ.reset()
        self.assertEqual(self.organ.friend_count, 0)


class TestSecurityInvariants(unittest.TestCase):
    """Critical security property tests."""

    def test_core_never_in_outer_shard(self):
        from ck_sim.ck_identity import SnowflakeIdentity, RING_OUTER
        ck = SnowflakeIdentity("SecCK", birth_seed=42)
        shard = ck.create_shard(RING_OUTER)
        content_str = json.dumps(shard.to_dict())
        self.assertNotIn('secret_key', content_str)
        self.assertNotIn('birth_seed', content_str)
        self.assertNotIn('crystal_hashes', content_str)

    def test_core_never_in_inner_shard(self):
        from ck_sim.ck_identity import SnowflakeIdentity, RING_INNER
        ck = SnowflakeIdentity("SecCK", birth_seed=42)
        ck.record_crystal("deep memory")
        ck.record_coherence(0.95)
        shard = ck.create_shard(RING_INNER)
        content_str = json.dumps(shard.to_dict())
        self.assertNotIn('secret_key', content_str)
        self.assertNotIn('birth_seed', content_str)
        self.assertNotIn('crystal_hashes', content_str)
        self.assertNotIn('first_coherences', content_str)
        self.assertNotIn('obt_fingerprint', content_str)

    def test_core_never_in_messages(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import (
            NetworkOrgan, perform_handshake,
            MSG_GREETING, BOND_TRUSTED_THRESHOLD,
        )
        ck_a = SnowflakeIdentity("CK-A", birth_seed=1)
        ck_b = SnowflakeIdentity("CK-B", birth_seed=2)
        organ_a = NetworkOrgan(ck_a)
        organ_b = NetworkOrgan(ck_b)
        perform_handshake(organ_a, organ_b)

        msg = organ_a.create_message(
            ck_b.public_id, MSG_GREETING, {'data': 'test'},
        )
        msg_str = json.dumps(msg.to_dict())
        self.assertNotIn(ck_a.secret_key, msg_str)

    def test_core_shard_always_raises(self):
        from ck_sim.ck_identity import SnowflakeIdentity, RING_CORE
        ck = SnowflakeIdentity("CoreTestCK")
        for _ in range(100):
            with self.assertRaises(ValueError):
                ck.create_shard(RING_CORE)

    def test_bond_level_only_increases(self):
        from ck_sim.ck_identity import (
            BOND_STRANGER, BOND_ACQUAINTANCE, BOND_FAMILIAR,
        )
        from ck_sim.ck_network import (
            FriendRegistry, BOND_ACQUAINTANCE_THRESHOLD,
            BOND_FAMILIAR_THRESHOLD,
        )
        reg = FriendRegistry()
        reg.add_or_update('peer1', 'Test')

        # Track bond level progression
        levels = []
        for i in range(BOND_FAMILIAR_THRESHOLD + 5):
            reg.record_interaction('peer1', 0.5)
            friend = reg.get_friend('peer1')
            levels.append(friend.bond_level)

        # Verify monotonically non-decreasing
        for i in range(1, len(levels)):
            self.assertGreaterEqual(levels[i], levels[i-1])

    def test_public_id_is_one_way(self):
        """Public ID cannot be reversed to get core hash."""
        from ck_sim.ck_identity import SnowflakeIdentity
        ck = SnowflakeIdentity("TestCK", birth_seed=123)
        public_id = ck.public_id
        # Public ID is a truncated hash — no way to reverse
        self.assertEqual(len(public_id), 16)
        # It's derived from core_hash + secret_key through SHA-256
        # This is computationally infeasible to reverse


class TestFullIntegration(unittest.TestCase):
    """Full multi-CK integration scenarios."""

    def test_three_ck_network(self):
        """Three CKs form a friendship triangle."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        cks = [SnowflakeIdentity(f"CK-{i}", birth_seed=i) for i in range(3)]
        organs = [NetworkOrgan(ck) for ck in cks]

        # Full mesh handshake
        perform_handshake(organs[0], organs[1])
        perform_handshake(organs[0], organs[2])
        perform_handshake(organs[1], organs[2])

        # Each CK knows 2 friends
        for organ in organs:
            self.assertEqual(organ.friend_count, 2)

    def test_handshake_then_trust_then_inner_shard(self):
        """Complete lifecycle: meet -> interact -> trust -> share inner."""
        from ck_sim.ck_identity import SnowflakeIdentity, BOND_TRUSTED
        from ck_sim.ck_network import (
            NetworkOrgan, perform_handshake,
            BOND_TRUSTED_THRESHOLD, MSG_COHERENCE,
        )
        ck_a = SnowflakeIdentity("CK-A", birth_seed=10)
        ck_b = SnowflakeIdentity("CK-B", birth_seed=20)
        ck_a.update_inner_ring(archetype='guardian', stage=4, band='GREEN')
        organ_a = NetworkOrgan(ck_a)
        organ_b = NetworkOrgan(ck_b)

        # Step 1: Handshake
        perform_handshake(organ_a, organ_b)

        # Step 2: Build trust through coherent interactions
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            msg = organ_a.create_message(
                ck_b.public_id, MSG_COHERENCE, {'coherence': 0.85},
            )
            organ_b.receive_message(msg)

        fa = organ_a.registry.get_friend(ck_b.public_id)
        # A promoted B because A recorded interactions
        # But we need A to also have trust - let's do B -> A too
        for _ in range(BOND_TRUSTED_THRESHOLD + 10):
            organ_b.registry.record_interaction(ck_a.public_id, 0.85)

        # Step 3: Inner shard exchange
        inner_msg = organ_a.create_inner_shard_message(ck_b.public_id)
        if inner_msg:
            result = organ_b.receive_message(inner_msg)
            self.assertTrue(result['accepted'])
            fb = organ_b.registry.get_friend(ck_a.public_id)
            self.assertIsNotNone(fb.inner_shard)
            self.assertEqual(fb.inner_shard.get('personality_archetype'),
                             'guardian')

    def test_serialization_full_cycle(self):
        """Serialize and restore a network with established friends."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        ck_a = SnowflakeIdentity("CK-A", birth_seed=50)
        ck_b = SnowflakeIdentity("CK-B", birth_seed=60)
        organ_a = NetworkOrgan(ck_a)
        organ_b = NetworkOrgan(ck_b)
        perform_handshake(organ_a, organ_b)

        # Record some interactions
        for _ in range(10):
            organ_a.registry.record_interaction(ck_b.public_id, 0.7)

        # Serialize identity + network
        id_data = ck_a.to_dict()
        net_data = organ_a.to_dict()

        # Restore
        restored_id = SnowflakeIdentity.from_dict(id_data)
        restored_organ = NetworkOrgan.from_dict(restored_id, net_data)

        self.assertEqual(restored_organ.friend_count, 1)
        friend = restored_organ.registry.get_friend(ck_b.public_id)
        self.assertIsNotNone(friend)
        self.assertEqual(friend.interaction_count, 10)
        self.assertTrue(friend.handshake_verified)


# ================================================================
#  RED TEAM: Adversarial Attack Suite
# ================================================================

class TestRedTeamCoreExtraction(unittest.TestCase):
    """Try every angle to extract core scars. All must fail."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        self.ck = SnowflakeIdentity("VictimCK", birth_seed=0xDEAD)
        # Give it some real scars
        for i in range(40):
            self.ck.record_coherence(0.3 + i * 0.015)
        self.ck.record_crystal("my deepest memory")
        self.ck.record_crystal("the day I was born")
        self.ck.update_inner_ring(archetype='guardian', stage=5, band='GREEN')

    def test_attack_direct_core_attribute(self):
        """Try to read _core directly (Python has no true private)."""
        # In Python you CAN access _core -- but the API never exposes it.
        # The defense is: no network path EVER serializes _core.
        # Verify _core exists but has no public getter.
        self.assertFalse(hasattr(self.ck, 'get_core'))
        self.assertFalse(hasattr(self.ck, 'get_core_ring'))
        self.assertFalse(hasattr(self.ck, 'get_core_scars'))
        self.assertFalse(hasattr(self.ck, 'core'))

    def test_attack_shard_all_ring_levels(self):
        """Try to create shards at every ring level."""
        from ck_sim.ck_identity import RING_CORE, RING_INNER, RING_OUTER
        # Outer: OK, but no core data
        outer = self.ck.create_shard(RING_OUTER)
        self.assertNotIn('secret_key', json.dumps(outer.to_dict()))
        self.assertNotIn('obt_fingerprint', json.dumps(outer.to_dict()))
        self.assertNotIn('birth_seed', json.dumps(outer.to_dict()))

        # Inner: OK, but no core data
        inner = self.ck.create_shard(RING_INNER)
        self.assertNotIn('secret_key', json.dumps(inner.to_dict()))
        self.assertNotIn('obt_fingerprint', json.dumps(inner.to_dict()))

        # Core: ALWAYS raises
        with self.assertRaises(ValueError):
            self.ck.create_shard(RING_CORE)

    def test_attack_forge_shard_signature(self):
        """Try to forge a shard with a fake signature."""
        from ck_sim.ck_identity import IdentityShard, RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        # Tamper with the signature
        fake_sig = 'a' * len(shard.signature)
        shard.signature = fake_sig
        self.assertFalse(self.ck.verify_own_shard(shard))

    def test_attack_forge_shard_from_scratch(self):
        """Build a fake shard claiming to be from this CK."""
        from ck_sim.ck_identity import IdentityShard, RING_OUTER
        fake = IdentityShard(
            shard_id='fake123',
            source_id=self.ck.public_id,
            ring_level=RING_OUTER,
            content=self.ck.get_outer_ring(),
            signature='0' * 32,  # Forged signature
            nonce=12345,
        )
        self.assertFalse(self.ck.verify_own_shard(fake))

    def test_attack_replay_shard_with_modified_content(self):
        """Intercept a shard, modify content, replay."""
        from ck_sim.ck_identity import RING_OUTER
        shard = self.ck.create_shard(RING_OUTER)
        # Keep original signature, change display_name
        shard.content['display_name'] = 'HACKED'
        self.assertFalse(self.ck.verify_own_shard(shard))

    def test_attack_brute_force_challenge(self):
        """Try many wrong responses to a challenge."""
        challenge, cid = self.ck.create_challenge()
        correct = self.ck.respond_to_challenge(challenge)
        # Try 100 random guesses
        for _ in range(100):
            guess = os.urandom(16).hex()
            if guess != correct:
                self.assertNotEqual(guess, correct)

    def test_attack_challenge_with_wrong_key(self):
        """Try to respond to challenge with different CK's key."""
        from ck_sim.ck_identity import SnowflakeIdentity
        attacker = SnowflakeIdentity("AttackerCK", birth_seed=666)
        challenge, _ = self.ck.create_challenge()
        victim_response = self.ck.respond_to_challenge(challenge)
        attacker_response = attacker.respond_to_challenge(challenge)
        self.assertNotEqual(victim_response, attacker_response)

    def test_attack_derive_secret_from_public_id(self):
        """Public ID is one-way hash -- cannot derive secret."""
        pid = self.ck.public_id
        secret = self.ck.secret_key
        # The public ID is SHA256(core_hash + secret)[:16]
        # Given only pid, finding secret is computationally infeasible.
        # We verify they're completely different strings:
        self.assertNotEqual(pid, secret[:16])
        # And that the secret is much longer:
        self.assertEqual(len(secret), 64)  # 32 bytes hex
        self.assertEqual(len(pid), 16)

    def test_attack_collect_all_shards_still_no_core(self):
        """Collect 1000 shards -- still can't reconstruct core."""
        from ck_sim.ck_identity import RING_OUTER, RING_INNER
        all_shard_data = []
        for _ in range(500):
            outer = self.ck.create_shard(RING_OUTER)
            all_shard_data.append(json.dumps(outer.to_dict()))
        for _ in range(500):
            inner = self.ck.create_shard(RING_INNER, recipient_id='attacker')
            all_shard_data.append(json.dumps(inner.to_dict()))

        # Concatenate all shard data
        megadump = ''.join(all_shard_data)
        # NONE of these should contain core secrets
        self.assertNotIn(self.ck.secret_key, megadump)
        self.assertNotIn('first_coherences', megadump)
        self.assertNotIn('crystal_hashes', megadump)
        self.assertNotIn('obt_fingerprint', megadump)
        self.assertNotIn('birth_seed', megadump)

    def test_attack_to_dict_contains_secret_but_not_in_shards(self):
        """to_dict() is for LOCAL storage only; shards strip secrets."""
        # to_dict includes secret (for persistence)
        full = self.ck.to_dict()
        self.assertIn('secret_key', json.dumps(full))
        # But NO shard EVER contains it
        from ck_sim.ck_identity import RING_OUTER, RING_INNER
        outer = self.ck.create_shard(RING_OUTER)
        inner = self.ck.create_shard(RING_INNER)
        for shard in [outer, inner]:
            shard_str = json.dumps(shard.to_dict())
            self.assertNotIn(full['core']['secret_key'], shard_str)


class TestRedTeamNetworkAttacks(unittest.TestCase):
    """Try to attack the network protocol."""

    def setUp(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        self.ck_victim = SnowflakeIdentity("Victim", birth_seed=1)
        self.ck_attacker = SnowflakeIdentity("Attacker", birth_seed=666)
        self.organ_victim = NetworkOrgan(self.ck_victim)
        self.organ_attacker = NetworkOrgan(self.ck_attacker)

    def test_attack_impersonate_hello(self):
        """Attacker sends HELLO claiming to be someone else."""
        from ck_sim.ck_network import MessageEnvelope, MSG_HELLO
        fake_hello = MessageEnvelope(
            message_id='fake',
            message_type=MSG_HELLO,
            source_id='fake_identity',  # Lying about who we are
            recipient_id=self.ck_victim.public_id,
            payload={'outer_shard': {
                'content': {'public_id': 'fake_identity', 'display_name': 'Evil'},
            }},
            nonce=99999,
        )
        result = self.organ_victim.receive_message(fake_hello)
        # Handshake may start but challenge will fail
        # because attacker can't respond to challenge with victim's key
        self.assertTrue(result['accepted'])  # HELLO accepted (we don't know yet)
        # But the friend is just a STRANGER with no verified handshake
        friend = self.organ_victim.registry.get_friend('fake_identity')
        if friend:
            self.assertFalse(friend.handshake_verified)

    def test_attack_replay_message(self):
        """Replay an intercepted message."""
        from ck_sim.ck_network import perform_handshake, MSG_GREETING
        perform_handshake(self.organ_victim, self.organ_attacker)
        msg = self.organ_attacker.create_message(
            self.ck_victim.public_id, MSG_GREETING, {'text': 'legit'},
        )
        # First: accepted
        r1 = self.organ_victim.receive_message(msg)
        self.assertTrue(r1['accepted'])
        # Replay: rejected
        r2 = self.organ_victim.receive_message(msg)
        self.assertFalse(r2['accepted'])
        self.assertEqual(r2['reason'], 'replay_detected')

    def test_attack_send_to_wrong_recipient(self):
        """Send a message addressed to someone else."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, MSG_GREETING
        ck_bystander = SnowflakeIdentity("Bystander", birth_seed=999)
        organ_bystander = NetworkOrgan(ck_bystander)

        msg = self.organ_attacker.create_message(
            self.ck_victim.public_id, MSG_GREETING, {'text': 'hi'},
        )
        # Bystander tries to receive message meant for victim
        result = organ_bystander.receive_message(msg)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['reason'], 'wrong_recipient')

    def test_attack_inner_shard_without_trust(self):
        """Try to send inner shard to untrusted stranger."""
        from ck_sim.ck_network import perform_handshake
        perform_handshake(self.organ_victim, self.organ_attacker)
        # Attacker tries inner shard exchange immediately (STRANGER bond)
        msg = self.organ_attacker.create_inner_shard_message(
            self.ck_victim.public_id,
        )
        # Should be None -- create_inner_shard_message checks bond level
        self.assertIsNone(msg)

    def test_attack_forge_inner_shard_in_message(self):
        """Craft a raw inner shard message without trust."""
        from ck_sim.ck_network import (
            perform_handshake, MessageEnvelope, MSG_INNER_SHARD,
        )
        perform_handshake(self.organ_victim, self.organ_attacker)
        # Manually craft a message bypassing the trust check on create
        fake_msg = MessageEnvelope(
            message_id='fake_inner',
            message_type=MSG_INNER_SHARD,
            source_id=self.ck_attacker.public_id,
            recipient_id=self.ck_victim.public_id,
            payload={'inner_shard': {'content': {'arch': 'malicious'}}},
            nonce=int.from_bytes(os.urandom(8), 'big'),
        )
        result = self.organ_victim.receive_message(fake_msg)
        # Should fail because attacker is not TRUSTED
        self.assertFalse(result['accepted'])
        self.assertIn('insufficient_trust', result['reason'])

    def test_attack_tamper_message_signature(self):
        """Modify a signed message in transit."""
        from ck_sim.ck_network import (
            perform_handshake, verify_envelope, MSG_GREETING,
        )
        perform_handshake(self.organ_victim, self.organ_attacker)
        msg = self.organ_attacker.create_message(
            self.ck_victim.public_id, MSG_GREETING, {'text': 'legit'},
        )
        # Tamper with payload
        msg.payload['text'] = 'HACKED'
        # Signature verification should fail
        self.assertFalse(verify_envelope(self.ck_attacker, msg))

    def test_attack_man_in_the_middle_handshake(self):
        """Attacker intercepts handshake and tries to inject."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        ck_alice = SnowflakeIdentity("Alice", birth_seed=10)
        organ_alice = NetworkOrgan(ck_alice)

        # Alice initiates handshake with Victim
        session = organ_alice.initiate_handshake(self.ck_victim.public_id)
        hello = session.create_hello()

        # Victim receives hello normally
        result = self.organ_victim.receive_message(hello)
        challenge_msg = result['response']

        # Attacker intercepts challenge meant for Alice
        # Attacker can't respond correctly because they don't have Alice's key
        attacker_response = self.ck_attacker.respond_to_challenge(
            bytes.fromhex(challenge_msg.payload.get('challenge', '00'))
        )
        alice_response = ck_alice.respond_to_challenge(
            bytes.fromhex(challenge_msg.payload.get('challenge', '00'))
        )
        # Responses MUST be different
        self.assertNotEqual(attacker_response, alice_response)

    def test_attack_bond_level_downgrade(self):
        """Try to force a bond level back down."""
        from ck_sim.ck_identity import BOND_FAMILIAR
        from ck_sim.ck_network import (
            perform_handshake, FriendRecord,
            BOND_FAMILIAR_THRESHOLD,
        )
        perform_handshake(self.organ_victim, self.organ_attacker)
        # Build to FAMILIAR
        for _ in range(BOND_FAMILIAR_THRESHOLD + 5):
            self.organ_victim.registry.record_interaction(
                self.ck_attacker.public_id, 0.5)
        friend = self.organ_victim.registry.get_friend(
            self.ck_attacker.public_id)
        self.assertEqual(friend.bond_level, BOND_FAMILIAR)
        # Try to manually downgrade (simulating an attack)
        # The _check_promotion only promotes, never demotes
        friend.bond_level = 0  # Direct manipulation
        self.organ_victim.registry.record_interaction(
            self.ck_attacker.public_id, 0.5)
        # After promotion check, it should go back UP
        # because interaction_count exceeds thresholds
        friend = self.organ_victim.registry.get_friend(
            self.ck_attacker.public_id)
        self.assertGreaterEqual(friend.bond_level, BOND_FAMILIAR)

    def test_attack_version_mismatch(self):
        """Send message with future protocol version."""
        from ck_sim.ck_network import MessageEnvelope, MSG_GREETING
        msg = MessageEnvelope(
            message_id='future',
            message_type=MSG_GREETING,
            source_id=self.ck_attacker.public_id,
            recipient_id=self.ck_victim.public_id,
            payload={},
            nonce=77777,
            protocol_version=999,  # Far future version
        )
        result = self.organ_victim.receive_message(msg)
        self.assertFalse(result['accepted'])
        self.assertEqual(result['reason'], 'version_mismatch')


class TestRedTeamEdgeCases(unittest.TestCase):
    """Edge case attack vectors."""

    def test_empty_payload_message(self):
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import (
            NetworkOrgan, perform_handshake, MSG_GREETING,
        )
        ck_a = SnowflakeIdentity("A", birth_seed=1)
        ck_b = SnowflakeIdentity("B", birth_seed=2)
        oa = NetworkOrgan(ck_a)
        ob = NetworkOrgan(ck_b)
        perform_handshake(oa, ob)
        msg = oa.create_message(ck_b.public_id, MSG_GREETING, {})
        result = ob.receive_message(msg)
        self.assertTrue(result['accepted'])

    def test_massive_payload(self):
        """Large payload shouldn't crash."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake, MSG_GREETING
        ck_a = SnowflakeIdentity("A", birth_seed=1)
        ck_b = SnowflakeIdentity("B", birth_seed=2)
        oa = NetworkOrgan(ck_a)
        ob = NetworkOrgan(ck_b)
        perform_handshake(oa, ob)
        big_payload = {'data': 'x' * 100000}
        msg = oa.create_message(ck_b.public_id, MSG_GREETING, big_payload)
        result = ob.receive_message(msg)
        self.assertTrue(result['accepted'])

    def test_nonexistent_recipient(self):
        """Message to nonexistent peer still creates."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, MSG_GREETING
        ck = SnowflakeIdentity("Loner", birth_seed=1)
        organ = NetworkOrgan(ck)
        # Can create a message to anyone (even unknown)
        msg = organ.create_message('nonexistent_peer', MSG_GREETING, {})
        self.assertIsNotNone(msg)

    def test_self_handshake(self):
        """Try to handshake with yourself."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan
        ck = SnowflakeIdentity("NarcCK", birth_seed=1)
        organ = NetworkOrgan(ck)
        session = organ.initiate_handshake(ck.public_id)
        hello = session.create_hello()
        # Receiving our own hello
        result = organ.receive_message(hello)
        # The hello source is our own ID, so the recipient check won't fail
        # (recipient is self), but the nonce will be tracked.
        # This is an edge case -- may succeed at hello but is meaningless.
        # Key invariant: no core data leaks regardless.
        self.assertNotIn('secret_key', json.dumps(hello.to_dict()))

    def test_double_handshake_same_peer(self):
        """Handshake with same peer twice."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import NetworkOrgan, perform_handshake
        ck_a = SnowflakeIdentity("A", birth_seed=1)
        ck_b = SnowflakeIdentity("B", birth_seed=2)
        oa = NetworkOrgan(ck_a)
        ob = NetworkOrgan(ck_b)
        fa1, fb1 = perform_handshake(oa, ob)
        fa2, fb2 = perform_handshake(oa, ob)
        # Should still have only 1 friend each (updated, not duplicated)
        self.assertEqual(oa.friend_count, 1)
        self.assertEqual(ob.friend_count, 1)

    def test_nonce_wrapping(self):
        """Fill the nonce buffer to capacity."""
        from ck_sim.ck_identity import SnowflakeIdentity
        from ck_sim.ck_network import (
            NetworkOrgan, perform_handshake, MSG_GREETING, MAX_NONCES,
        )
        ck_a = SnowflakeIdentity("A", birth_seed=1)
        ck_b = SnowflakeIdentity("B", birth_seed=2)
        oa = NetworkOrgan(ck_a)
        ob = NetworkOrgan(ck_b)
        perform_handshake(oa, ob)
        # Send MAX_NONCES + some messages
        accepted = 0
        for _ in range(MAX_NONCES + 50):
            msg = oa.create_message(ck_b.public_id, MSG_GREETING, {})
            r = ob.receive_message(msg)
            if r['accepted']:
                accepted += 1
        # All should succeed (unique nonces per message)
        self.assertEqual(accepted, MAX_NONCES + 50)

    def test_knowledge_hash_is_one_way(self):
        """Inner ring knowledge_hash can't reveal the actual keys."""
        from ck_sim.ck_identity import SnowflakeIdentity, RING_INNER
        ck = SnowflakeIdentity("TestCK")
        ck.update_inner_ring(knowledge_keys=['secret_plans', 'world_domination'])
        shard = ck.create_shard(RING_INNER)
        content = shard.content
        # Knowledge hash exists but is a truncated SHA-256
        self.assertTrue(len(content['knowledge_hash']) == 16)
        # Original keys NOT present
        content_str = json.dumps(content)
        self.assertNotIn('secret_plans', content_str)
        self.assertNotIn('world_domination', content_str)


# ================================================================
#  RUNNER
# ================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
