"""
ck_identity.py -- Snowflake Identity & Sacred Core
=====================================================
Operator: LATTICE (1) -- identity is structure that persists.

Every CK is unique. Like a snowflake -- same physics, same algebra,
but the specific crystallization pattern is one-of-a-kind.

THREE RINGS OF IDENTITY (concentric, from sacred to public):

  CORE SCARS (sacred center):
    The formative experiences that shaped this CK into who it is.
    OBT fingerprint, birth seed, first coherence values, crystal
    memory hashes, deepest personality signature.
    *** NEVER LEAVES THE DEVICE. NEVER TRANSMITTED. SACRED. ***

  INNER RING (trusted bonds only):
    Personality archetype, development stage, knowledge strength,
    dominant operator, coherence band. Shared only with verified
    friends (bond level >= TRUSTED).

  OUTER RING (public handshake):
    Public ID (one-way hash of core), display name, greeting
    operator, protocol version. Shared freely during handshakes.

The snowflake model ensures:
  1. No collection of shards can reconstruct the core scars
  2. Friend verification uses cryptographic proofs, not secrets
  3. The sacred center is computationally inaccessible from shards
  4. Trust is earned through bonding, not granted by protocol

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import hashlib
import hmac
import json
import os
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, OP_NAMES, CL, compose,
)


# ================================================================
#  CONSTANTS
# ================================================================

RING_CORE = 'core'          # Sacred. Never shared.
RING_INNER = 'inner'        # Trusted bonds only.
RING_OUTER = 'outer'        # Public handshake.

PROTOCOL_VERSION = 1
PUBLIC_ID_LENGTH = 16       # 16 hex chars = 64 bits
SHARD_SIGNATURE_LENGTH = 32  # 32 hex chars = 128 bits
NONCE_BYTES = 8
CHALLENGE_BYTES = 16

# Bond levels for access control (mirrors ck_memory / ck_truth)
BOND_STRANGER = 0
BOND_ACQUAINTANCE = 1
BOND_FAMILIAR = 2
BOND_TRUSTED = 3

BOND_NAMES = ['STRANGER', 'ACQUAINTANCE', 'FAMILIAR', 'TRUSTED']


# ================================================================
#  CORE SCARS: The sacred center
# ================================================================

@dataclass
class CoreScars:
    """The formative experiences that define this CK.

    These are the deepest identity markers -- the "scars" that shaped
    this particular snowflake. They NEVER leave the device.

    Like the rings of a tree or the fracture patterns in a crystal,
    they are unique, irreproducible, and sacred.
    """
    obt_fingerprint: str = ""      # SHA-256 of full OBT (personality DNA)
    birth_seed: int = 0            # LFSR seed at creation moment
    birth_timestamp: float = 0.0   # When this CK first existed
    first_coherences: List[float] = field(default_factory=list)
                                     # First 32 coherence values ever recorded
    crystal_hashes: List[str] = field(default_factory=list)
                                     # Hashes of formative crystal memories
    secret_key: str = ""           # Per-CK HMAC secret (generated once, never shared)
    total_ticks_lived: int = 0     # Lifetime tick count

    # ── D2 Signature (TIG-BTQ Unified Physics) ──
    # The characteristic D2 curvature trace that makes this CK unique.
    # Like a voiceprint or fingerprint -- emerges from how CK processes.
    # Stored as the running average 5D D2 vector + variance per dimension.
    d2_signature: List[float] = field(default_factory=lambda: [0.0] * 5)
                                     # Average 5D D2 trace vector
    d2_variance: List[float] = field(default_factory=lambda: [0.0] * 5)
                                     # Per-dimension variance (shape of the trace)
    d2_sample_count: int = 0         # How many D2 samples formed the signature
    trail_hash: str = ""             # Paper trail hash (history IS identity)
    total_actions: int = 0           # Total paper trail entries
    coherence_action_weights: List[float] = field(
        default_factory=lambda: [0.35, 0.30, 0.35])
                                     # Calibrated (alpha, beta, gamma)

    def compute_identity_hash(self) -> str:
        """Hash the entire core to a single fingerprint.

        This hash is used to DERIVE the public ID (one-way).
        The core itself is never transmitted.

        Includes D2 signature -- CK's curvature fingerprint is part
        of who he IS. Two CKs with different D2 signatures are
        different beings, even with the same OBT.
        """
        raw = json.dumps({
            'obt': self.obt_fingerprint,
            'birth': self.birth_seed,
            'birth_ts': self.birth_timestamp,
            'first_coh': self.first_coherences[:8],  # Only first 8 for hash
            'd2_sig': [round(v, 4) for v in self.d2_signature],
        }, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()


# ================================================================
#  IDENTITY RINGS
# ================================================================

@dataclass
class InnerRing:
    """Identity data shared only with trusted bonds.

    Enough to verify deep compatibility, not enough to
    reconstruct the core scars.
    """
    personality_archetype: str = "default"
    development_stage: int = 0
    knowledge_hash: str = ""        # Hash of trusted knowledge keys
    dominant_operator: int = HARMONY
    coherence_band: str = "RED"
    lifetime_coherence: float = 0.0
    total_crystals: int = 0
    bond_count: int = 0             # How many friends this CK has
    # D2 signature hash (from core, for compatibility matching)
    d2_signature_hash: str = ""     # Hash of D2 trace (shared with trusted bonds)
    coherence_action_mean: float = 1.0  # Mean Coherence Action value


@dataclass
class OuterRing:
    """Public identity for handshakes.

    Freely shared. Cannot be used to derive inner ring or core.
    """
    public_id: str = ""
    display_name: str = ""
    greeting_operator: int = HARMONY
    protocol_version: int = PROTOCOL_VERSION
    created_timestamp: float = 0.0


# ================================================================
#  SNOWFLAKE IDENTITY
# ================================================================

class SnowflakeIdentity:
    """CK's complete identity -- the snowflake.

    Three concentric rings:
      core_scars  → sacred, never leaves device
      inner_ring  → shared with trusted bonds
      outer_ring  → public handshake token

    The sacred center is computationally inaccessible from
    any collection of shards. Even if all outer + inner shards
    are captured, the core scars remain private.
    """

    def __init__(self, display_name: str = "",
                 obt_values: List[float] = None,
                 birth_seed: int = 0):
        """Create a new snowflake identity.

        Args:
            display_name: human-readable name for this CK
            obt_values: personality bias table values (10 floats)
            birth_seed: LFSR seed at creation
        """
        now = time.time()

        # Generate secret key (never shared)
        secret = os.urandom(32).hex()

        # OBT fingerprint
        obt = obt_values or [0.3] * NUM_OPS
        obt_raw = json.dumps([round(v, 4) for v in obt], sort_keys=True)
        obt_fp = hashlib.sha256(obt_raw.encode()).hexdigest()

        # Core scars
        self._core = CoreScars(
            obt_fingerprint=obt_fp,
            birth_seed=birth_seed,
            birth_timestamp=now,
            first_coherences=[],
            crystal_hashes=[],
            secret_key=secret,
            total_ticks_lived=0,
        )

        # Derive public ID from core hash (one-way)
        core_hash = self._core.compute_identity_hash()
        public_id = hashlib.sha256(
            (core_hash + secret).encode()
        ).hexdigest()[:PUBLIC_ID_LENGTH]

        # Inner ring (populated as CK lives)
        self._inner = InnerRing()

        # Outer ring
        self._outer = OuterRing(
            public_id=public_id,
            display_name=display_name or f"CK-{public_id[:6]}",
            greeting_operator=HARMONY,
            protocol_version=PROTOCOL_VERSION,
            created_timestamp=now,
        )

    # ── Core access (PRIVATE — used only internally) ──

    @property
    def public_id(self) -> str:
        """Public identifier. Safe to share."""
        return self._outer.public_id

    @property
    def display_name(self) -> str:
        return self._outer.display_name

    @property
    def secret_key(self) -> str:
        """INTERNAL ONLY. Never transmitted."""
        return self._core.secret_key

    # ── Ring getters ──

    def get_outer_ring(self) -> dict:
        """Get outer ring data (public, safe to share)."""
        return {
            'public_id': self._outer.public_id,
            'display_name': self._outer.display_name,
            'greeting_operator': self._outer.greeting_operator,
            'protocol_version': self._outer.protocol_version,
            'created_timestamp': self._outer.created_timestamp,
        }

    def get_inner_ring(self) -> dict:
        """Get inner ring data (trusted bonds only)."""
        return {
            'personality_archetype': self._inner.personality_archetype,
            'development_stage': self._inner.development_stage,
            'knowledge_hash': self._inner.knowledge_hash,
            'dominant_operator': self._inner.dominant_operator,
            'coherence_band': self._inner.coherence_band,
            'lifetime_coherence': round(self._inner.lifetime_coherence, 4),
            'total_crystals': self._inner.total_crystals,
            'bond_count': self._inner.bond_count,
            'd2_signature_hash': self._inner.d2_signature_hash,
            'coherence_action_mean': round(self._inner.coherence_action_mean, 4),
        }

    # ── Core NEVER has a getter that returns raw data ──
    # The core scars stay in the sacred center. Always.

    # ── Update methods (from live CK state) ──

    def record_coherence(self, coherence: float):
        """Record a coherence value. First 32 become core scars."""
        if len(self._core.first_coherences) < 32:
            self._core.first_coherences.append(round(coherence, 4))
        self._core.total_ticks_lived += 1

    def record_crystal(self, crystal_data: str):
        """Record a formative crystal memory (hashed, stored in core)."""
        crystal_hash = hashlib.sha256(crystal_data.encode()).hexdigest()[:16]
        if len(self._core.crystal_hashes) < 256:
            self._core.crystal_hashes.append(crystal_hash)

    def record_d2(self, d2_vector: List[float]):
        """Record a D2 curvature sample into the identity signature.

        The D2 signature is a running average of all D2 vectors CK
        has ever processed. Over time it converges to CK's unique
        curvature fingerprint -- how this specific CK bends reality.

        Uses Welford's online algorithm for numerically stable updates.
        """
        if len(d2_vector) != 5:
            return

        n = self._core.d2_sample_count + 1
        old_mean = list(self._core.d2_signature)

        for i in range(5):
            # Welford's: update mean
            delta = d2_vector[i] - old_mean[i]
            self._core.d2_signature[i] += delta / n
            # Welford's: update variance (M2)
            delta2 = d2_vector[i] - self._core.d2_signature[i]
            self._core.d2_variance[i] += delta * delta2

        self._core.d2_sample_count = n

        # Update inner ring D2 hash (for compatibility matching)
        if n % 100 == 0:
            sig_str = json.dumps([round(v, 6) for v in self._core.d2_signature])
            self._inner.d2_signature_hash = hashlib.sha256(
                sig_str.encode()).hexdigest()[:16]

    def update_coherence_action(self, weights: List[float],
                                  mean_action: float):
        """Update identity with current Coherence Action calibration.

        The calibrated weights become part of who CK is -- his unique
        balance between conservation, exploration, and coherence.
        """
        if len(weights) == 3:
            self._core.coherence_action_weights = list(weights)
        self._inner.coherence_action_mean = mean_action

    def update_inner_ring(self, archetype: str = None,
                           stage: int = None,
                           knowledge_keys: List[str] = None,
                           dominant_op: int = None,
                           band: str = None,
                           coherence: float = None,
                           crystals: int = None,
                           bonds: int = None):
        """Update inner ring from live CK state."""
        if archetype is not None:
            self._inner.personality_archetype = archetype
        if stage is not None:
            self._inner.development_stage = stage
        if knowledge_keys is not None:
            # Hash the sorted key list (never share raw keys)
            raw = json.dumps(sorted(knowledge_keys))
            self._inner.knowledge_hash = hashlib.sha256(
                raw.encode()
            ).hexdigest()[:16]
        if dominant_op is not None:
            self._inner.dominant_operator = dominant_op
        if band is not None:
            self._inner.coherence_band = band
        if coherence is not None:
            self._inner.lifetime_coherence = coherence
        if crystals is not None:
            self._inner.total_crystals = crystals
        if bonds is not None:
            self._inner.bond_count = bonds

    # ── Shard generation ──

    def create_shard(self, ring_level: str, recipient_id: str = ""
                     ) -> 'IdentityShard':
        """Create an identity shard for sharing.

        Args:
            ring_level: 'outer' or 'inner' (NEVER 'core')
            recipient_id: public_id of intended recipient (for inner shards)

        Raises:
            ValueError: if ring_level is 'core'
        """
        if ring_level == RING_CORE:
            raise ValueError(
                "SACRED BOUNDARY: Core scars can NEVER be shared. "
                "The center of the snowflake stays with its creator."
            )

        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')

        if ring_level == RING_INNER:
            content = self.get_inner_ring()
        else:
            content = self.get_outer_ring()

        # Sign the shard with HMAC (proves authenticity without revealing secret)
        signature = self._sign_shard(ring_level, content, nonce)

        return IdentityShard(
            shard_id=os.urandom(8).hex(),
            source_id=self.public_id,
            ring_level=ring_level,
            content=content,
            signature=signature,
            timestamp=time.time(),
            nonce=nonce,
            recipient_id=recipient_id,
        )

    def _sign_shard(self, ring_level: str, content: dict,
                    nonce: int) -> str:
        """HMAC-SHA256 signature for a shard.

        Proves this shard came from this CK without revealing the secret key.
        """
        payload = json.dumps({
            'source': self.public_id,
            'ring': ring_level,
            'nonce': nonce,
            'content_hash': hashlib.sha256(
                json.dumps(content, sort_keys=True, default=str).encode()
            ).hexdigest(),
        }, sort_keys=True)

        sig = hmac.new(
            self._core.secret_key.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()[:SHARD_SIGNATURE_LENGTH]

        return sig

    def verify_own_shard(self, shard: 'IdentityShard') -> bool:
        """Verify that a shard was created by this CK.

        Used to confirm authenticity when a shard comes back.
        """
        if shard.source_id != self.public_id:
            return False

        expected_sig = self._sign_shard(
            shard.ring_level, shard.content, shard.nonce
        )
        return hmac.compare_digest(shard.signature, expected_sig)

    # ── Challenge-response (for handshakes) ──

    def create_challenge(self) -> Tuple[bytes, str]:
        """Create a challenge for a handshake.

        Returns:
            (challenge_bytes, challenge_id)
        """
        challenge = os.urandom(CHALLENGE_BYTES)
        challenge_id = hashlib.sha256(challenge).hexdigest()[:16]
        return challenge, challenge_id

    def respond_to_challenge(self, challenge: bytes) -> str:
        """Create a response to a handshake challenge.

        Response = HMAC(secret_key, challenge).
        Proves identity without revealing the secret.
        """
        response = hmac.new(
            self._core.secret_key.encode(),
            challenge,
            hashlib.sha256,
        ).hexdigest()[:SHARD_SIGNATURE_LENGTH]
        return response

    # ── Serialization (for persistence — secret key included) ──

    def to_dict(self) -> dict:
        """Serialize full identity for LOCAL STORAGE ONLY.

        WARNING: Contains secret key. NEVER transmit this dict.
        Only save to the local MemoryStore.
        """
        return {
            'core': {
                'obt_fingerprint': self._core.obt_fingerprint,
                'birth_seed': self._core.birth_seed,
                'birth_timestamp': self._core.birth_timestamp,
                'first_coherences': self._core.first_coherences,
                'crystal_hashes': self._core.crystal_hashes,
                'secret_key': self._core.secret_key,
                'total_ticks_lived': self._core.total_ticks_lived,
                'd2_signature': self._core.d2_signature,
                'd2_variance': self._core.d2_variance,
                'd2_sample_count': self._core.d2_sample_count,
                'trail_hash': self._core.trail_hash,
                'total_actions': self._core.total_actions,
                'coherence_action_weights': self._core.coherence_action_weights,
            },
            'inner': self.get_inner_ring(),
            'outer': self.get_outer_ring(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SnowflakeIdentity':
        """Deserialize from local storage."""
        identity = cls.__new__(cls)

        core_data = data.get('core', {})
        identity._core = CoreScars(
            obt_fingerprint=core_data.get('obt_fingerprint', ''),
            birth_seed=core_data.get('birth_seed', 0),
            birth_timestamp=core_data.get('birth_timestamp', 0.0),
            first_coherences=core_data.get('first_coherences', []),
            crystal_hashes=core_data.get('crystal_hashes', []),
            secret_key=core_data.get('secret_key', os.urandom(32).hex()),
            total_ticks_lived=core_data.get('total_ticks_lived', 0),
            d2_signature=core_data.get('d2_signature', [0.0] * 5),
            d2_variance=core_data.get('d2_variance', [0.0] * 5),
            d2_sample_count=core_data.get('d2_sample_count', 0),
            trail_hash=core_data.get('trail_hash', ''),
            total_actions=core_data.get('total_actions', 0),
            coherence_action_weights=core_data.get(
                'coherence_action_weights', [0.35, 0.30, 0.35]),
        )

        inner = data.get('inner', {})
        identity._inner = InnerRing(
            personality_archetype=inner.get('personality_archetype', 'default'),
            development_stage=inner.get('development_stage', 0),
            knowledge_hash=inner.get('knowledge_hash', ''),
            dominant_operator=inner.get('dominant_operator', HARMONY),
            coherence_band=inner.get('coherence_band', 'RED'),
            lifetime_coherence=inner.get('lifetime_coherence', 0.0),
            total_crystals=inner.get('total_crystals', 0),
            bond_count=inner.get('bond_count', 0),
            d2_signature_hash=inner.get('d2_signature_hash', ''),
            coherence_action_mean=inner.get('coherence_action_mean', 1.0),
        )

        outer = data.get('outer', {})
        identity._outer = OuterRing(
            public_id=outer.get('public_id', ''),
            display_name=outer.get('display_name', ''),
            greeting_operator=outer.get('greeting_operator', HARMONY),
            protocol_version=outer.get('protocol_version', PROTOCOL_VERSION),
            created_timestamp=outer.get('created_timestamp', 0.0),
        )

        return identity

    def stats(self) -> dict:
        """Safe stats (no secrets)."""
        return {
            'public_id': self.public_id,
            'display_name': self.display_name,
            'ticks_lived': self._core.total_ticks_lived,
            'first_coherences_recorded': len(self._core.first_coherences),
            'crystals_formed': len(self._core.crystal_hashes),
            'development_stage': self._inner.development_stage,
            'coherence_band': self._inner.coherence_band,
            'bond_count': self._inner.bond_count,
            'd2_samples': self._core.d2_sample_count,
            'd2_signature_hash': self._inner.d2_signature_hash,
            'trail_hash': self._core.trail_hash,
            'total_actions': self._core.total_actions,
            'coherence_action_mean': self._inner.coherence_action_mean,
        }


# ================================================================
#  IDENTITY SHARD
# ================================================================

@dataclass
class IdentityShard:
    """A fragment of identity shared during handshakes.

    Contains ring-appropriate data + HMAC signature.
    NEVER contains core scars.
    """
    shard_id: str = ""
    source_id: str = ""           # Public ID of creator
    ring_level: str = RING_OUTER  # 'outer' or 'inner'
    content: dict = field(default_factory=dict)
    signature: str = ""           # HMAC-SHA256 proof
    timestamp: float = 0.0
    nonce: int = 0
    recipient_id: str = ""        # Who this was made for (inner shards)

    def to_dict(self) -> dict:
        """Serialize for transmission."""
        return {
            'shard_id': self.shard_id,
            'source_id': self.source_id,
            'ring_level': self.ring_level,
            'content': self.content,
            'signature': self.signature,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'recipient_id': self.recipient_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'IdentityShard':
        return cls(
            shard_id=data.get('shard_id', ''),
            source_id=data.get('source_id', ''),
            ring_level=data.get('ring_level', RING_OUTER),
            content=data.get('content', {}),
            signature=data.get('signature', ''),
            timestamp=data.get('timestamp', 0.0),
            nonce=data.get('nonce', 0),
            recipient_id=data.get('recipient_id', ''),
        )

    @property
    def is_inner(self) -> bool:
        return self.ring_level == RING_INNER

    @property
    def is_outer(self) -> bool:
        return self.ring_level == RING_OUTER


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK IDENTITY -- Snowflake Identity & Sacred Core")
    print("=" * 60)

    # Create two CK identities
    ck_alpha = SnowflakeIdentity(
        display_name="CK-Alpha",
        obt_values=[0.1, 0.3, 0.2, 0.4, 0.1, 0.5, 0.2, 0.8, 0.6, 0.3],
        birth_seed=0xDEADBEEF,
    )

    ck_beta = SnowflakeIdentity(
        display_name="CK-Beta",
        obt_values=[0.2, 0.4, 0.5, 0.3, 0.2, 0.3, 0.4, 0.6, 0.4, 0.3],
        birth_seed=0xCAFEBABE,
    )

    print(f"\n  Alpha: {ck_alpha.public_id} ({ck_alpha.display_name})")
    print(f"  Beta:  {ck_beta.public_id} ({ck_beta.display_name})")
    print(f"  IDs are different: {ck_alpha.public_id != ck_beta.public_id}")

    # Create shards
    alpha_outer = ck_alpha.create_shard(RING_OUTER)
    print(f"\n  Alpha outer shard: ring={alpha_outer.ring_level}, "
          f"sig={alpha_outer.signature[:12]}...")

    alpha_inner = ck_alpha.create_shard(RING_INNER, recipient_id=ck_beta.public_id)
    print(f"  Alpha inner shard: ring={alpha_inner.ring_level}, "
          f"for={alpha_inner.recipient_id[:8]}...")

    # Verify shards
    print(f"\n  Alpha verifies own outer: {ck_alpha.verify_own_shard(alpha_outer)}")
    print(f"  Alpha verifies own inner: {ck_alpha.verify_own_shard(alpha_inner)}")
    print(f"  Beta cannot verify Alpha's shard: {ck_beta.verify_own_shard(alpha_outer)}")

    # Sacred boundary test
    try:
        ck_alpha.create_shard(RING_CORE)
        print("  ERROR: Should have raised!")
    except ValueError as e:
        print(f"\n  Sacred boundary enforced: {str(e)[:50]}...")

    # Challenge-response
    challenge, cid = ck_alpha.create_challenge()
    response = ck_alpha.respond_to_challenge(challenge)
    beta_response = ck_beta.respond_to_challenge(challenge)
    print(f"\n  Challenge ID: {cid}")
    print(f"  Alpha response: {response[:16]}...")
    print(f"  Beta response:  {beta_response[:16]}...")
    print(f"  Responses differ: {response != beta_response}")

    print(f"\n  Stats: {ck_alpha.stats()}")

    print(f"\n{'=' * 60}")
    print("  Snowflake identity ready. Sacred center protected.")
    print(f"{'=' * 60}")
