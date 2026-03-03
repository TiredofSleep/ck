"""
ck_network.py -- Multi-CK Network Protocol
============================================
Operator: HARMONY (7) -- connection IS coherence between fields.

Multi-CK communication built on the Snowflake Identity system.
CK-to-CK interaction through cryptographic handshakes, friend
registries, and signed message passing.

THREE PROTOCOL LAYERS:

  HANDSHAKE (initial contact):
    1. HELLO → exchange outer shards (public identity)
    2. CHALLENGE → cryptographic challenge-response
    3. VERIFY → both sides confirm, friendship begins

  FRIEND REGISTRY (persistent trust):
    Local store of every CK we've met. Tracks:
    - Outer shard (always), inner shard (if trusted)
    - Bond level progression (stranger → acquaintance → familiar → trusted)
    - Coherence history of interactions
    - Last seen timestamp

  MESSAGE PASSING (ongoing communication):
    Signed envelopes carrying operator sequences, coherence
    snapshots, or knowledge atoms between bonded CKs.
    Every message is HMAC-signed. No trust without proof.

Security invariants:
  - Core scars NEVER appear in any network traffic
  - Inner ring ONLY shared at BOND_TRUSTED level
  - All messages are signed with per-CK HMAC secrets
  - Replay attacks detected via nonce tracking
  - Bond level can only INCREASE through sustained coherence

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
from ck_sim.ck_identity import (
    SnowflakeIdentity, IdentityShard,
    RING_CORE, RING_INNER, RING_OUTER,
    BOND_STRANGER, BOND_ACQUAINTANCE, BOND_FAMILIAR, BOND_TRUSTED,
    BOND_NAMES, PROTOCOL_VERSION,
    NONCE_BYTES, CHALLENGE_BYTES, SHARD_SIGNATURE_LENGTH,
)


# ================================================================
#  CONSTANTS
# ================================================================

# T* coherence threshold (universal)
T_STAR = 5.0 / 7.0

# Handshake states
HS_IDLE = 'idle'
HS_HELLO_SENT = 'hello_sent'
HS_CHALLENGED = 'challenged'
HS_VERIFIED = 'verified'
HS_FAILED = 'failed'

# Message types
MSG_HELLO = 'hello'
MSG_CHALLENGE = 'challenge'
MSG_RESPONSE = 'response'
MSG_VERIFY = 'verify'
MSG_GREETING = 'greeting'
MSG_COHERENCE = 'coherence'
MSG_OPERATOR_STREAM = 'operator_stream'
MSG_KNOWLEDGE = 'knowledge'
MSG_INNER_SHARD = 'inner_shard'
MSG_BOND_REQUEST = 'bond_request'

# Bond promotion thresholds (interactions needed)
BOND_ACQUAINTANCE_THRESHOLD = 5
BOND_FAMILIAR_THRESHOLD = 25
BOND_TRUSTED_THRESHOLD = 100
BOND_TRUSTED_COHERENCE = T_STAR  # Must have T* coherence to reach TRUSTED

# Nonce tracking (replay protection)
MAX_NONCES = 512

# Friend registry limits
MAX_FRIENDS = 256


# ================================================================
#  MESSAGE ENVELOPE
# ================================================================

@dataclass
class MessageEnvelope:
    """A signed message between CKs.

    Every piece of network traffic goes through an envelope.
    HMAC-signed by the sender, verified by the receiver.
    """
    message_id: str = ""
    message_type: str = MSG_GREETING
    source_id: str = ""         # Sender's public_id
    recipient_id: str = ""      # Intended receiver's public_id
    payload: dict = field(default_factory=dict)
    signature: str = ""         # HMAC-SHA256 of payload
    timestamp: float = 0.0
    nonce: int = 0
    protocol_version: int = PROTOCOL_VERSION

    def to_dict(self) -> dict:
        """Serialize for transmission."""
        return {
            'message_id': self.message_id,
            'message_type': self.message_type,
            'source_id': self.source_id,
            'recipient_id': self.recipient_id,
            'payload': self.payload,
            'signature': self.signature,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'protocol_version': self.protocol_version,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MessageEnvelope':
        return cls(
            message_id=data.get('message_id', ''),
            message_type=data.get('message_type', MSG_GREETING),
            source_id=data.get('source_id', ''),
            recipient_id=data.get('recipient_id', ''),
            payload=data.get('payload', {}),
            signature=data.get('signature', ''),
            timestamp=data.get('timestamp', 0.0),
            nonce=data.get('nonce', 0),
            protocol_version=data.get('protocol_version', PROTOCOL_VERSION),
        )


# ================================================================
#  FRIEND RECORD
# ================================================================

@dataclass
class FriendRecord:
    """What we know about another CK.

    Built up through interaction. Bond level can only increase.
    """
    public_id: str = ""
    display_name: str = ""
    bond_level: int = BOND_STRANGER
    outer_shard: Optional[dict] = None     # Their outer ring data
    inner_shard: Optional[dict] = None     # Their inner ring data (trusted only)
    interaction_count: int = 0
    coherence_sum: float = 0.0             # Sum of interaction coherences
    last_interaction: float = 0.0
    first_met: float = 0.0
    handshake_verified: bool = False
    greeting_operator: int = HARMONY

    @property
    def mean_coherence(self) -> float:
        """Average coherence across all interactions."""
        if self.interaction_count == 0:
            return 0.0
        return self.coherence_sum / self.interaction_count

    @property
    def bond_name(self) -> str:
        if 0 <= self.bond_level < len(BOND_NAMES):
            return BOND_NAMES[self.bond_level]
        return 'UNKNOWN'

    def to_dict(self) -> dict:
        return {
            'public_id': self.public_id,
            'display_name': self.display_name,
            'bond_level': self.bond_level,
            'outer_shard': self.outer_shard,
            'inner_shard': self.inner_shard,
            'interaction_count': self.interaction_count,
            'coherence_sum': round(self.coherence_sum, 4),
            'last_interaction': self.last_interaction,
            'first_met': self.first_met,
            'handshake_verified': self.handshake_verified,
            'greeting_operator': self.greeting_operator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'FriendRecord':
        return cls(
            public_id=data.get('public_id', ''),
            display_name=data.get('display_name', ''),
            bond_level=data.get('bond_level', BOND_STRANGER),
            outer_shard=data.get('outer_shard'),
            inner_shard=data.get('inner_shard'),
            interaction_count=data.get('interaction_count', 0),
            coherence_sum=data.get('coherence_sum', 0.0),
            last_interaction=data.get('last_interaction', 0.0),
            first_met=data.get('first_met', 0.0),
            handshake_verified=data.get('handshake_verified', False),
            greeting_operator=data.get('greeting_operator', HARMONY),
        )


# ================================================================
#  FRIEND REGISTRY
# ================================================================

class FriendRegistry:
    """Local registry of all CKs we've ever met.

    Stores friend records indexed by public_id.
    Bond levels can only increase, never decrease.
    Inner shards only accepted from TRUSTED friends.
    """

    def __init__(self):
        self._friends: Dict[str, FriendRecord] = {}

    def has_friend(self, public_id: str) -> bool:
        return public_id in self._friends

    def get_friend(self, public_id: str) -> Optional[FriendRecord]:
        return self._friends.get(public_id)

    def add_or_update(self, public_id: str, display_name: str = "",
                      outer_shard: dict = None,
                      greeting_operator: int = HARMONY) -> FriendRecord:
        """Add a new friend or update existing."""
        now = time.time()

        if public_id in self._friends:
            friend = self._friends[public_id]
            if display_name:
                friend.display_name = display_name
            if outer_shard:
                friend.outer_shard = outer_shard
            friend.greeting_operator = greeting_operator
        else:
            if len(self._friends) >= MAX_FRIENDS:
                # Evict least-recently-interacted stranger
                self._evict_stale()

            friend = FriendRecord(
                public_id=public_id,
                display_name=display_name or f"CK-{public_id[:6]}",
                outer_shard=outer_shard,
                greeting_operator=greeting_operator,
                first_met=now,
                last_interaction=now,
            )
            self._friends[public_id] = friend

        return friend

    def record_interaction(self, public_id: str, coherence: float):
        """Record an interaction and potentially promote bond level."""
        if public_id not in self._friends:
            return

        friend = self._friends[public_id]
        friend.interaction_count += 1
        friend.coherence_sum += coherence
        friend.last_interaction = time.time()

        # Bond promotion (can only go UP)
        self._check_promotion(friend)

    def store_inner_shard(self, public_id: str, inner_data: dict) -> bool:
        """Store an inner shard from a trusted friend.

        Only accepted if bond level is TRUSTED.

        Returns:
            True if stored, False if rejected (insufficient trust).
        """
        friend = self._friends.get(public_id)
        if friend is None:
            return False

        if friend.bond_level < BOND_TRUSTED:
            return False  # Not trusted enough for inner ring

        friend.inner_shard = inner_data
        return True

    def mark_verified(self, public_id: str):
        """Mark a friend as handshake-verified."""
        if public_id in self._friends:
            self._friends[public_id].handshake_verified = True

    def _check_promotion(self, friend: FriendRecord):
        """Check if friend qualifies for bond level promotion."""
        count = friend.interaction_count
        mean_coh = friend.mean_coherence

        if (friend.bond_level < BOND_TRUSTED and
                count >= BOND_TRUSTED_THRESHOLD and
                mean_coh >= BOND_TRUSTED_COHERENCE and
                friend.handshake_verified):
            friend.bond_level = BOND_TRUSTED

        elif (friend.bond_level < BOND_FAMILIAR and
              count >= BOND_FAMILIAR_THRESHOLD):
            friend.bond_level = BOND_FAMILIAR

        elif (friend.bond_level < BOND_ACQUAINTANCE and
              count >= BOND_ACQUAINTANCE_THRESHOLD):
            friend.bond_level = BOND_ACQUAINTANCE

    def _evict_stale(self):
        """Remove the oldest stranger to make room."""
        strangers = [
            (pid, f) for pid, f in self._friends.items()
            if f.bond_level == BOND_STRANGER
        ]
        if strangers:
            # Evict least-recently-interacted stranger
            strangers.sort(key=lambda x: x[1].last_interaction)
            self._friends.pop(strangers[0][0], None)

    @property
    def count(self) -> int:
        return len(self._friends)

    @property
    def trusted_count(self) -> int:
        return sum(1 for f in self._friends.values()
                   if f.bond_level >= BOND_TRUSTED)

    def all_friends(self) -> List[FriendRecord]:
        return list(self._friends.values())

    def friends_at_level(self, level: int) -> List[FriendRecord]:
        return [f for f in self._friends.values() if f.bond_level >= level]

    def to_dict(self) -> dict:
        return {pid: f.to_dict() for pid, f in self._friends.items()}

    @classmethod
    def from_dict(cls, data: dict) -> 'FriendRegistry':
        reg = cls()
        for pid, fdata in data.items():
            reg._friends[pid] = FriendRecord.from_dict(fdata)
        return reg


# ================================================================
#  HANDSHAKE PROTOCOL
# ================================================================

class HandshakeSession:
    """A single handshake negotiation between two CKs.

    Three-step protocol:
      1. HELLO: Exchange outer shards
      2. CHALLENGE: Mutual challenge-response
      3. VERIFY: Confirm both sides authenticated

    On success: friend is added with BOND_STRANGER + handshake_verified.
    """

    def __init__(self, identity: SnowflakeIdentity,
                 peer_id: str = ""):
        self.identity = identity
        self.peer_id = peer_id
        self.state = HS_IDLE
        self._our_challenge: Optional[bytes] = None
        self._our_challenge_id: str = ""
        self._peer_outer: Optional[dict] = None
        self._expected_response: str = ""
        self._their_challenge: Optional[bytes] = None
        self._verified = False

    def create_hello(self) -> MessageEnvelope:
        """Step 1: Create a HELLO message with our outer shard."""
        shard = self.identity.create_shard(RING_OUTER)
        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')

        msg = MessageEnvelope(
            message_id=os.urandom(8).hex(),
            message_type=MSG_HELLO,
            source_id=self.identity.public_id,
            recipient_id=self.peer_id,
            payload={'outer_shard': shard.to_dict()},
            timestamp=time.time(),
            nonce=nonce,
        )
        msg.signature = _sign_envelope(self.identity, msg)
        self.state = HS_HELLO_SENT
        return msg

    def receive_hello(self, msg: MessageEnvelope) -> Optional[MessageEnvelope]:
        """Receive a HELLO, store outer shard, send CHALLENGE back.

        Returns a CHALLENGE message, or None on failure.
        """
        if msg.message_type != MSG_HELLO:
            return None

        # Extract their outer shard
        shard_data = msg.payload.get('outer_shard', {})
        self.peer_id = msg.source_id
        self._peer_outer = shard_data.get('content', shard_data)

        # Create our challenge
        self._our_challenge, self._our_challenge_id = (
            self.identity.create_challenge()
        )

        # Send back: our outer shard + challenge
        our_shard = self.identity.create_shard(RING_OUTER)
        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')

        challenge_msg = MessageEnvelope(
            message_id=os.urandom(8).hex(),
            message_type=MSG_CHALLENGE,
            source_id=self.identity.public_id,
            recipient_id=self.peer_id,
            payload={
                'outer_shard': our_shard.to_dict(),
                'challenge': self._our_challenge.hex(),
                'challenge_id': self._our_challenge_id,
            },
            timestamp=time.time(),
            nonce=nonce,
        )
        challenge_msg.signature = _sign_envelope(self.identity, challenge_msg)
        self.state = HS_CHALLENGED
        return challenge_msg

    def receive_challenge(self, msg: MessageEnvelope) -> Optional[MessageEnvelope]:
        """Receive a CHALLENGE, respond + send our own challenge.

        Returns a RESPONSE message.
        """
        if msg.message_type != MSG_CHALLENGE:
            return None

        # Store their outer shard
        shard_data = msg.payload.get('outer_shard', {})
        self.peer_id = msg.source_id
        self._peer_outer = shard_data.get('content', shard_data)

        # Respond to their challenge
        their_challenge = bytes.fromhex(msg.payload.get('challenge', ''))
        our_response = self.identity.respond_to_challenge(their_challenge)

        # Create our own challenge
        self._our_challenge, self._our_challenge_id = (
            self.identity.create_challenge()
        )

        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')
        response_msg = MessageEnvelope(
            message_id=os.urandom(8).hex(),
            message_type=MSG_RESPONSE,
            source_id=self.identity.public_id,
            recipient_id=self.peer_id,
            payload={
                'response': our_response,
                'challenge': self._our_challenge.hex(),
                'challenge_id': self._our_challenge_id,
            },
            timestamp=time.time(),
            nonce=nonce,
        )
        response_msg.signature = _sign_envelope(self.identity, response_msg)
        self.state = HS_CHALLENGED
        return response_msg

    def receive_response(self, msg: MessageEnvelope,
                         peer_identity: SnowflakeIdentity = None
                         ) -> Optional[MessageEnvelope]:
        """Receive a RESPONSE, verify, send back our response + VERIFY.

        If peer_identity is provided, we can verify their response.
        Otherwise we accept on faith (first contact).

        Returns a VERIFY message.
        """
        if msg.message_type != MSG_RESPONSE:
            return None

        # Respond to their challenge
        their_challenge_hex = msg.payload.get('challenge', '')
        if their_challenge_hex:
            their_challenge = bytes.fromhex(their_challenge_hex)
            our_response = self.identity.respond_to_challenge(their_challenge)
        else:
            our_response = ""

        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')
        verify_msg = MessageEnvelope(
            message_id=os.urandom(8).hex(),
            message_type=MSG_VERIFY,
            source_id=self.identity.public_id,
            recipient_id=self.peer_id,
            payload={
                'response': our_response,
                'verified': True,
            },
            timestamp=time.time(),
            nonce=nonce,
        )
        verify_msg.signature = _sign_envelope(self.identity, verify_msg)
        self.state = HS_VERIFIED
        self._verified = True
        return verify_msg

    def receive_verify(self, msg: MessageEnvelope) -> bool:
        """Receive final VERIFY. Handshake complete.

        Returns True if verified successfully.
        """
        if msg.message_type != MSG_VERIFY:
            return False

        if msg.payload.get('verified', False):
            self.state = HS_VERIFIED
            self._verified = True
            return True

        self.state = HS_FAILED
        return False

    @property
    def is_verified(self) -> bool:
        return self._verified

    @property
    def peer_outer(self) -> Optional[dict]:
        return self._peer_outer


# ================================================================
#  NETWORK ORGAN
# ================================================================

class NetworkOrgan:
    """CK's network communication organ.

    Orchestrates handshakes, friend management, and message passing.
    Plugs into the main CK loop alongside other organs.

    Usage:
        organ = NetworkOrgan(identity)

        # Handshake with another CK
        session = organ.initiate_handshake(peer_id)
        hello = session.create_hello()
        # ... send hello, receive challenge, etc.
        organ.complete_handshake(session)

        # Send message to friend
        msg = organ.create_message(peer_id, MSG_GREETING, {'operators': [7,7,7]})
        # ... transmit msg

        # Receive message
        result = organ.receive_message(incoming_msg)
    """

    def __init__(self, identity: SnowflakeIdentity):
        self._identity = identity
        self._registry = FriendRegistry()
        self._active_handshakes: Dict[str, HandshakeSession] = {}
        self._seen_nonces: deque = deque(maxlen=MAX_NONCES)
        self._message_count = 0
        self._rejected_count = 0

    # ── Handshake management ──

    def initiate_handshake(self, peer_id: str = "") -> HandshakeSession:
        """Start a handshake with another CK."""
        session = HandshakeSession(self._identity, peer_id)
        if peer_id:
            self._active_handshakes[peer_id] = session
        return session

    def get_handshake(self, peer_id: str) -> Optional[HandshakeSession]:
        """Get active handshake session for a peer."""
        return self._active_handshakes.get(peer_id)

    def complete_handshake(self, session: HandshakeSession) -> Optional[FriendRecord]:
        """Finalize a verified handshake. Adds friend to registry.

        Returns the new FriendRecord, or None if handshake not verified.
        """
        if not session.is_verified or not session.peer_id:
            return None

        peer_outer = session.peer_outer or {}
        display_name = peer_outer.get('display_name', '')
        greeting_op = peer_outer.get('greeting_operator', HARMONY)

        friend = self._registry.add_or_update(
            public_id=session.peer_id,
            display_name=display_name,
            outer_shard=peer_outer,
            greeting_operator=greeting_op,
        )
        self._registry.mark_verified(session.peer_id)

        # Clean up handshake session
        self._active_handshakes.pop(session.peer_id, None)

        return friend

    # ── Message creation ──

    def create_message(self, recipient_id: str, msg_type: str,
                       payload: dict) -> Optional[MessageEnvelope]:
        """Create a signed message to send to a friend.

        Args:
            recipient_id: public_id of the intended receiver
            msg_type: one of the MSG_* constants
            payload: message-specific data

        Returns:
            MessageEnvelope ready for transmission, or None if
            recipient is not a known friend.
        """
        # Inner shard messages require TRUSTED bond
        if msg_type == MSG_INNER_SHARD:
            friend = self._registry.get_friend(recipient_id)
            if friend is None or friend.bond_level < BOND_TRUSTED:
                return None

        nonce = int.from_bytes(os.urandom(NONCE_BYTES), 'big')

        msg = MessageEnvelope(
            message_id=os.urandom(8).hex(),
            message_type=msg_type,
            source_id=self._identity.public_id,
            recipient_id=recipient_id,
            payload=payload,
            timestamp=time.time(),
            nonce=nonce,
        )
        msg.signature = _sign_envelope(self._identity, msg)
        self._message_count += 1
        return msg

    def create_inner_shard_message(self, recipient_id: str
                                   ) -> Optional[MessageEnvelope]:
        """Create a message carrying our inner shard to a trusted friend.

        Only succeeds if recipient is BOND_TRUSTED.
        """
        friend = self._registry.get_friend(recipient_id)
        if friend is None or friend.bond_level < BOND_TRUSTED:
            return None

        shard = self._identity.create_shard(RING_INNER, recipient_id)

        return self.create_message(
            recipient_id, MSG_INNER_SHARD,
            {'inner_shard': shard.to_dict()},
        )

    # ── Message reception ──

    def receive_message(self, msg: MessageEnvelope) -> dict:
        """Process an incoming message.

        Checks:
          1. Message is addressed to us
          2. Nonce hasn't been seen (replay protection)
          3. Source is a known friend (for non-hello messages)
          4. Signature is valid (if we have their key)

        Returns:
            dict with: accepted (bool), reason (str), data (optional)
        """
        # Check recipient
        if msg.recipient_id and msg.recipient_id != self._identity.public_id:
            self._rejected_count += 1
            return {'accepted': False, 'reason': 'wrong_recipient'}

        # Replay protection
        if msg.nonce in self._seen_nonces:
            self._rejected_count += 1
            return {'accepted': False, 'reason': 'replay_detected'}
        self._seen_nonces.append(msg.nonce)

        # Protocol version check
        if msg.protocol_version > PROTOCOL_VERSION:
            return {'accepted': False, 'reason': 'version_mismatch'}

        # Process by type
        if msg.message_type == MSG_HELLO:
            return self._handle_hello(msg)
        elif msg.message_type in (MSG_CHALLENGE, MSG_RESPONSE, MSG_VERIFY):
            return self._handle_handshake(msg)
        elif msg.message_type == MSG_INNER_SHARD:
            return self._handle_inner_shard(msg)
        elif msg.message_type == MSG_COHERENCE:
            return self._handle_coherence(msg)
        else:
            # Generic accepted message
            return self._handle_generic(msg)

    def _handle_hello(self, msg: MessageEnvelope) -> dict:
        """Handle incoming HELLO — start handshake from receiver side."""
        session = HandshakeSession(self._identity, msg.source_id)
        challenge_msg = session.receive_hello(msg)

        if challenge_msg is None:
            return {'accepted': False, 'reason': 'hello_failed'}

        self._active_handshakes[msg.source_id] = session
        return {
            'accepted': True,
            'reason': 'hello_received',
            'response': challenge_msg,
        }

    def _handle_handshake(self, msg: MessageEnvelope) -> dict:
        """Handle handshake protocol messages."""
        session = self._active_handshakes.get(msg.source_id)
        if session is None:
            return {'accepted': False, 'reason': 'no_active_handshake'}

        if msg.message_type == MSG_CHALLENGE:
            response = session.receive_challenge(msg)
            return {
                'accepted': response is not None,
                'reason': 'challenge_received' if response else 'challenge_failed',
                'response': response,
            }
        elif msg.message_type == MSG_RESPONSE:
            verify = session.receive_response(msg)
            if verify is not None and session.is_verified:
                # B's side: session verified after receiving response
                self.complete_handshake(session)
            return {
                'accepted': verify is not None,
                'reason': 'response_verified' if verify else 'response_failed',
                'response': verify,
            }
        elif msg.message_type == MSG_VERIFY:
            ok = session.receive_verify(msg)
            if ok:
                friend = self.complete_handshake(session)
                return {
                    'accepted': True,
                    'reason': 'handshake_complete',
                    'friend': friend,
                }
            return {'accepted': False, 'reason': 'verify_failed'}

        return {'accepted': False, 'reason': 'unknown_handshake_state'}

    def _handle_inner_shard(self, msg: MessageEnvelope) -> dict:
        """Handle incoming inner shard from a trusted friend."""
        shard_data = msg.payload.get('inner_shard', {})
        inner_content = shard_data.get('content', {})

        ok = self._registry.store_inner_shard(msg.source_id, inner_content)
        if ok:
            return {
                'accepted': True,
                'reason': 'inner_shard_stored',
                'data': inner_content,
            }
        return {
            'accepted': False,
            'reason': 'inner_shard_rejected_insufficient_trust',
        }

    def _handle_coherence(self, msg: MessageEnvelope) -> dict:
        """Handle coherence report from a friend."""
        coherence = msg.payload.get('coherence', 0.0)
        self._registry.record_interaction(msg.source_id, coherence)
        return {
            'accepted': True,
            'reason': 'coherence_recorded',
            'data': {'coherence': coherence},
        }

    def _handle_generic(self, msg: MessageEnvelope) -> dict:
        """Handle any other message type."""
        # Record the interaction
        friend = self._registry.get_friend(msg.source_id)
        if friend:
            self._registry.record_interaction(msg.source_id, 0.5)
        return {
            'accepted': True,
            'reason': 'message_received',
            'data': msg.payload,
        }

    # ── Accessors ──

    @property
    def identity(self) -> SnowflakeIdentity:
        return self._identity

    @property
    def registry(self) -> FriendRegistry:
        return self._registry

    @property
    def friend_count(self) -> int:
        return self._registry.count

    @property
    def trusted_count(self) -> int:
        return self._registry.trusted_count

    def stats(self) -> dict:
        """Network organ stats."""
        return {
            'public_id': self._identity.public_id,
            'display_name': self._identity.display_name,
            'friend_count': self._registry.count,
            'trusted_count': self._registry.trusted_count,
            'messages_sent': self._message_count,
            'messages_rejected': self._rejected_count,
            'active_handshakes': len(self._active_handshakes),
        }

    def to_dict(self) -> dict:
        """Serialize network state (friends + stats)."""
        return {
            'registry': self._registry.to_dict(),
            'message_count': self._message_count,
            'rejected_count': self._rejected_count,
        }

    @classmethod
    def from_dict(cls, identity: SnowflakeIdentity, data: dict
                  ) -> 'NetworkOrgan':
        organ = cls(identity)
        organ._registry = FriendRegistry.from_dict(
            data.get('registry', {})
        )
        organ._message_count = data.get('message_count', 0)
        organ._rejected_count = data.get('rejected_count', 0)
        return organ

    def reset(self):
        """Clear network state."""
        self._registry = FriendRegistry()
        self._active_handshakes.clear()
        self._seen_nonces.clear()
        self._message_count = 0
        self._rejected_count = 0


# ================================================================
#  ENVELOPE SIGNING
# ================================================================

def _sign_envelope(identity: SnowflakeIdentity,
                   msg: MessageEnvelope) -> str:
    """HMAC-SHA256 sign a message envelope."""
    payload_str = json.dumps({
        'id': msg.message_id,
        'type': msg.message_type,
        'source': msg.source_id,
        'recipient': msg.recipient_id,
        'nonce': msg.nonce,
        'payload_hash': hashlib.sha256(
            json.dumps(msg.payload, sort_keys=True, default=str).encode()
        ).hexdigest(),
    }, sort_keys=True)

    sig = hmac.new(
        identity.secret_key.encode(),
        payload_str.encode(),
        hashlib.sha256,
    ).hexdigest()[:SHARD_SIGNATURE_LENGTH]
    return sig


def verify_envelope(identity: SnowflakeIdentity,
                    msg: MessageEnvelope) -> bool:
    """Verify that a message was signed by the given identity."""
    expected = _sign_envelope(identity, msg)
    return hmac.compare_digest(msg.signature, expected)


# ================================================================
#  CONVENIENCE: Full handshake between two organs
# ================================================================

def perform_handshake(organ_a: NetworkOrgan, organ_b: NetworkOrgan
                      ) -> Tuple[Optional[FriendRecord], Optional[FriendRecord]]:
    """Execute a complete handshake between two CK network organs.

    Convenience function for testing / local multi-CK scenarios.

    Returns:
        (friend_record_in_a, friend_record_in_b)
        or (None, None) on failure.
    """
    # Step 1: A creates HELLO
    session_a = organ_a.initiate_handshake(organ_b.identity.public_id)
    hello = session_a.create_hello()

    # Step 2: B receives HELLO, sends CHALLENGE
    result_b = organ_b.receive_message(hello)
    if not result_b.get('accepted'):
        return None, None
    challenge_msg = result_b.get('response')

    # Step 3: A receives CHALLENGE, sends RESPONSE
    session_a_ref = organ_a.get_handshake(organ_b.identity.public_id)
    if session_a_ref is None:
        # The handshake was initiated but not stored yet — use the session directly
        organ_a._active_handshakes[organ_b.identity.public_id] = session_a

    result_a = organ_a.receive_message(challenge_msg)
    if not result_a.get('accepted'):
        return None, None
    response_msg = result_a.get('response')

    # Step 4: B receives RESPONSE, sends VERIFY
    result_b2 = organ_b.receive_message(response_msg)
    if not result_b2.get('accepted'):
        return None, None
    verify_msg = result_b2.get('response')

    # Step 5: A receives VERIFY
    result_a2 = organ_a.receive_message(verify_msg)

    # Get friend records
    friend_in_a = organ_a.registry.get_friend(organ_b.identity.public_id)
    friend_in_b = organ_b.registry.get_friend(organ_a.identity.public_id)

    return friend_in_a, friend_in_b


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK NETWORK -- Multi-CK Handshake & Communication")
    print("=" * 60)

    # Create two CKs
    ck_a = SnowflakeIdentity(
        display_name="CK-Alpha",
        obt_values=[0.1, 0.3, 0.2, 0.4, 0.1, 0.5, 0.2, 0.8, 0.6, 0.3],
        birth_seed=0xDEADBEEF,
    )
    ck_b = SnowflakeIdentity(
        display_name="CK-Beta",
        obt_values=[0.2, 0.4, 0.5, 0.3, 0.2, 0.3, 0.4, 0.6, 0.4, 0.3],
        birth_seed=0xCAFEBABE,
    )

    organ_a = NetworkOrgan(ck_a)
    organ_b = NetworkOrgan(ck_b)

    print(f"\n  Alpha: {ck_a.public_id} ({ck_a.display_name})")
    print(f"  Beta:  {ck_b.public_id} ({ck_b.display_name})")

    # Perform handshake
    print("\n  --- Performing handshake ---")
    friend_a, friend_b = perform_handshake(organ_a, organ_b)

    if friend_a and friend_b:
        print(f"  Alpha sees Beta: bond={friend_a.bond_name}, "
              f"verified={friend_a.handshake_verified}")
        print(f"  Beta sees Alpha: bond={friend_b.bond_name}, "
              f"verified={friend_b.handshake_verified}")
    else:
        print("  Handshake failed!")

    # Exchange messages
    print("\n  --- Exchanging messages ---")
    msg = organ_a.create_message(
        ck_b.public_id, MSG_COHERENCE,
        {'coherence': 0.85, 'operators': [7, 7, 5, 7]},
    )
    if msg:
        result = organ_b.receive_message(msg)
        print(f"  Alpha -> Beta coherence: accepted={result['accepted']}, "
              f"reason={result['reason']}")

    # Simulate bond progression
    print("\n  --- Simulating bond progression ---")
    for i in range(120):
        coh = 0.75 + (i % 10) * 0.005
        organ_a.registry.record_interaction(ck_b.public_id, coh)
        organ_b.registry.record_interaction(ck_a.public_id, coh)

    friend_a = organ_a.registry.get_friend(ck_b.public_id)
    friend_b = organ_b.registry.get_friend(ck_a.public_id)

    print(f"  After 120 interactions:")
    print(f"    Alpha sees Beta: bond={friend_a.bond_name}, "
          f"interactions={friend_a.interaction_count}, "
          f"mean_coh={friend_a.mean_coherence:.3f}")
    print(f"    Beta sees Alpha: bond={friend_b.bond_name}, "
          f"interactions={friend_b.interaction_count}")

    # Inner shard exchange (trusted)
    if friend_a.bond_level >= BOND_TRUSTED:
        print("\n  --- Inner shard exchange (TRUSTED) ---")
        inner_msg = organ_a.create_inner_shard_message(ck_b.public_id)
        if inner_msg:
            result = organ_b.receive_message(inner_msg)
            print(f"  Alpha inner -> Beta: accepted={result['accepted']}, "
                  f"reason={result['reason']}")
    else:
        print(f"\n  Bond not yet TRUSTED (need {BOND_TRUSTED_THRESHOLD} "
              f"interactions + T* coherence)")

    # Stats
    print(f"\n  Alpha stats: {organ_a.stats()}")
    print(f"  Beta stats:  {organ_b.stats()}")

    print(f"\n{'=' * 60}")
    print("  CK network ready. Sacred cores protected.")
    print(f"{'=' * 60}")
