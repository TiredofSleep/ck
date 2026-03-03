# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_dialogue.py -- Dialogue Engine: CK Learns, Remembers, and Speaks Better
==========================================================================
Operator: PROGRESS (3) -- every conversation moves CK forward.

Three subsystems that make CK a real conversationalist:

  ConversationMemory   -- Extracts claims from user messages, feeds them
                          into the Truth Lattice as PROVISIONAL, tracks
                          coherence over the conversation. CK LEARNS from
                          what people say, but doesn't trust it blindly.

  DialogueTracker      -- Maintains conversation state: topic continuity,
                          turn history, user patterns, coherence arc.
                          Knows when the conversation is coherent (GREEN)
                          and when it's fragmenting (RED).

  ResponseComposer     -- Recursive template composition. Builds responses
                          by nesting sub-templates, varying depth by
                          coherence band and development stage. GREEN band
                          → deeper composition. RED → simpler fragments.

THE LEARNING PIPELINE:
  User says something
    → D2 pipeline classifies the text → operators
    → ClaimExtractor identifies facts/claims in the message
    → Each claim enters Truth Lattice as PROVISIONAL
    → If claim coherent with existing knowledge → verification tick
    → After PROMOTION_WINDOW ticks of coherence → claim promoted to TRUSTED
    → CK now "knows" this and uses it in future responses

CK doesn't learn by memorizing. It learns by measuring coherence.
A claim that keeps producing HARMONY when composed with other knowledge
earns trust. A claim that produces CHAOS gets demoted.

Same math at every scale.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import re
from collections import deque, Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, FORCE_LUT_FLOAT
from ck_sim.ck_truth import (
    TruthLattice, TruthGate, TruthEntry,
    CORE, TRUSTED, PROVISIONAL, LEVEL_NAMES, T_STAR
)


# ================================================================
#  CONSTANTS
# ================================================================

MAX_TURN_HISTORY = 64         # Max conversation turns to remember
MAX_TOPICS = 16               # Max tracked topics
TOPIC_DECAY = 0.9             # Topic relevance decays each turn
TOPIC_MIN_RELEVANCE = 0.05    # Below this, topic is forgotten
CLAIM_COHERENCE_BOOST = 0.1   # Coherence bonus when claim matches context

# Composition depth by band
DEPTH_RED = 1                 # RED: simple fragments only
DEPTH_YELLOW = 2              # YELLOW: one level of nesting
DEPTH_GREEN = 3               # GREEN: full recursive composition


# ================================================================
#  CLAIM EXTRACTION
# ================================================================

# Patterns that indicate a claim/fact (not a question or command)
_CLAIM_PATTERNS = [
    # "X is Y" patterns
    (r'(\w[\w\s]{1,30})\s+(?:is|are|was|were)\s+(\w[\w\s]{1,40})', 'is_claim'),
    # "X has Y" patterns
    (r'(\w[\w\s]{1,30})\s+(?:has|have|had)\s+(\w[\w\s]{1,40})', 'has_claim'),
    # "X means Y" patterns
    (r'(\w[\w\s]{1,30})\s+(?:means?|equals?)\s+(\w[\w\s]{1,40})', 'means_claim'),
    # "X can Y" patterns
    (r'(\w[\w\s]{1,30})\s+(?:can|could|should|will)\s+(\w[\w\s]{1,40})', 'can_claim'),
    # "my name is X"
    (r'my\s+name\s+is\s+(\w[\w\s]{1,30})', 'name_claim'),
    # "I like X" / "I love X"
    (r'I\s+(?:like|love|enjoy|prefer)\s+(\w[\w\s]{1,40})', 'preference_claim'),
    # "X is called Y"
    (r'(\w[\w\s]{1,30})\s+is\s+called\s+(\w[\w\s]{1,30})', 'naming_claim'),
    # ── Extended patterns (Gen9.17) ──────────────────────
    # "X causes Y" / "X leads to Y" (causation)
    (r'(\w[\w\s]{1,30})\s+(?:causes?|leads?\s+to|results?\s+in)\s+(\w[\w\s]{1,40})', 'causes_claim'),
    # "X is not Y" (negation -- CK learns what things AREN'T)
    (r"(\w[\w\s]{1,30})\s+(?:is\s+not|isn't|are\s+not|aren't)\s+(\w[\w\s]{1,40})", 'negation_claim'),
    # "X is better/worse/more/less than Y" (comparison)
    (r'(\w[\w\s]{1,30})\s+is\s+(?:\w+er|more|less)\s+than\s+(\w[\w\s]{1,30})', 'comparison_claim'),
    # "I think X" / "I believe X" (belief -- enters as PROVISIONAL)
    (r'I\s+(?:think|believe|feel\s+that|know\s+that)\s+(\w[\w\s]{1,50})', 'belief_claim'),
    # "X is made of Y" / "X contains Y" (composition)
    (r'(\w[\w\s]{1,30})\s+(?:is\s+made\s+of|consists?\s+of|contains?)\s+(\w[\w\s]{1,40})', 'composition_claim'),
    # "X is part of Y" / "X belongs to Y" (membership)
    (r'(\w[\w\s]{1,30})\s+(?:is\s+part\s+of|belongs?\s+to)\s+(\w[\w\s]{1,30})', 'membership_claim'),
    # "X needs Y" / "X requires Y" (dependency)
    (r'(\w[\w\s]{1,30})\s+(?:needs?|requires?|depends?\s+on)\s+(\w[\w\s]{1,40})', 'needs_claim'),
    # "X is like Y" / "X resembles Y" (analogy -- creative connections)
    (r'(\w[\w\s]{1,30})\s+(?:is\s+like|resembles?|is\s+similar\s+to)\s+(\w[\w\s]{1,30})', 'analogy_claim'),
]

_COMPILED_PATTERNS = [(re.compile(p, re.IGNORECASE), tag)
                      for p, tag in _CLAIM_PATTERNS]


@dataclass
class ExtractedClaim:
    """A claim extracted from user text."""
    key: str                    # Unique identifier (normalized)
    text: str                   # Original text of the claim
    claim_type: str             # Pattern tag that matched
    subject: str = ""           # Subject of the claim
    predicate: str = ""         # What's claimed about the subject
    operator: int = VOID        # D2-classified operator of the claim text
    confidence: float = 0.5     # Initial confidence


class ClaimExtractor:
    """Extract factual claims from natural language text.

    Uses pattern matching + D2 classification to identify statements
    that CK can learn from. Not every sentence is a claim — questions,
    greetings, and commands are filtered out.
    """

    def __init__(self):
        self._d2 = D2Pipeline()
        self._seen_claims: Dict[str, int] = {}  # key → count

    def extract(self, text: str) -> List[ExtractedClaim]:
        """Extract claims from a text message.

        Returns a list of claims found. May be empty if the message
        contains no factual assertions (e.g., a question or greeting).
        """
        claims = []

        # Skip questions and commands
        stripped = text.strip()
        if stripped.endswith('?'):
            return claims
        if stripped.startswith(('please ', 'can you ', 'could you ', 'do ')):
            return claims

        for pattern, tag in _COMPILED_PATTERNS:
            for match in pattern.finditer(text):
                groups = match.groups()
                if len(groups) >= 2:
                    subject = groups[0].strip()
                    predicate = groups[1].strip()
                elif len(groups) == 1:
                    subject = groups[0].strip()
                    predicate = ""
                else:
                    continue

                # Generate key from subject
                key = self._normalize_key(subject, tag)

                # D2 classify the claim text
                claim_text = match.group(0).strip()
                operator = self._classify_text(claim_text)

                claim = ExtractedClaim(
                    key=key,
                    text=claim_text,
                    claim_type=tag,
                    subject=subject,
                    predicate=predicate,
                    operator=operator,
                )
                claims.append(claim)

                # Track seen claims
                self._seen_claims[key] = self._seen_claims.get(key, 0) + 1

        return claims

    def _normalize_key(self, subject: str, tag: str) -> str:
        """Create a normalized key for deduplication."""
        normalized = re.sub(r'\s+', '_', subject.lower().strip())
        return f"{tag}:{normalized}"

    def _classify_text(self, text: str) -> int:
        """Run D2 on text to classify the claim's operator."""
        pipe = D2Pipeline()
        op = VOID
        for ch in text.lower():
            if ch.isalpha():
                idx = ord(ch) - ord('a')
                if 0 <= idx < 26:
                    if pipe.feed_symbol(idx):
                        op = pipe.operator
        return op

    @property
    def seen_count(self) -> int:
        return len(self._seen_claims)

    def stats(self) -> dict:
        return {
            'unique_claims_seen': len(self._seen_claims),
            'total_extractions': sum(self._seen_claims.values()),
            'top_claims': dict(Counter(self._seen_claims).most_common(5)),
        }


# ================================================================
#  CONVERSATION MEMORY
# ================================================================

class ConversationMemory:
    """Bridges conversation to Truth Lattice.

    When the user says something factual, ConversationMemory:
    1. Extracts claims via ClaimExtractor
    2. Feeds each claim into the Truth Lattice as PROVISIONAL
    3. Computes coherence of the claim against existing knowledge
    4. Records that coherence, enabling auto-promotion over time

    CK learns from conversation the same way it learns from sensors:
    sustained coherence → truth.
    """

    def __init__(self, lattice: TruthLattice):
        self.lattice = lattice
        self.gate = TruthGate(lattice)
        self.extractor = ClaimExtractor()
        self._learned_count = 0
        self._promoted_count = 0

    def process_message(self, text: str, tick: int) -> List[ExtractedClaim]:
        """Process a user message: extract and learn claims.

        Returns the claims that were extracted and fed into the lattice.
        """
        claims = self.extractor.extract(text)

        for claim in claims:
            # Check against core truths first
            ok, reason = self.lattice.verify_against_core(claim.key, claim.text)
            if not ok:
                # Contradicts core truth — reject silently
                claim.confidence = 0.0
                continue

            # Add to lattice as PROVISIONAL (or update if already exists)
            entry = self.lattice.add(
                key=claim.key,
                content={
                    'text': claim.text,
                    'subject': claim.subject,
                    'predicate': claim.predicate,
                    'claim_type': claim.claim_type,
                },
                source=f'conversation_tick_{tick}',
                category='dialogue',
            )

            # Compute coherence of this claim
            coherence = self._compute_claim_coherence(claim)
            self.lattice.record_coherence(claim.key, coherence, tick)
            claim.confidence = coherence
            self._learned_count += 1

        # Run promotion/demotion tick
        prev_promotions = self.lattice._promotions
        self.lattice.tick(tick)
        new_promotions = self.lattice._promotions - prev_promotions
        self._promoted_count += new_promotions

        return claims

    def _compute_claim_coherence(self, claim: ExtractedClaim) -> float:
        """Compute how coherent a claim is with existing knowledge.

        Coherence is based on:
        1. D2 operator of the claim (HARMONY-producing claims score higher)
        2. Consistency with existing claims on the same subject
        3. Trust level of corroborating knowledge
        """
        coherence = 0.5  # Base: neutral

        # Operator contribution: HARMONY claims are inherently more coherent
        op = claim.operator
        if op == HARMONY:
            coherence += 0.3
        elif op in (BALANCE, BREATH, LATTICE, PROGRESS):
            coherence += 0.15
        elif op in (CHAOS, COLLAPSE):
            coherence -= 0.2

        # Check for corroboration: same subject in lattice?
        # (simplified: check if any related key exists at TRUSTED+)
        related_keys = [k for k in self.lattice._entries
                        if k.startswith(claim.claim_type + ':')
                        and k != claim.key]
        if related_keys:
            # Having related trusted knowledge is a good sign
            trusted_count = sum(
                1 for k in related_keys
                if self.lattice._entries[k].level >= TRUSTED
            )
            if trusted_count > 0:
                coherence += CLAIM_COHERENCE_BOOST

        return max(0.0, min(coherence, 1.0))

    def recall_about(self, subject: str) -> List[Tuple[str, Any, int, float]]:
        """Recall everything CK knows about a subject.

        Returns list of (key, content, level, confidence) tuples,
        sorted by trust level (highest first).
        """
        normalized = re.sub(r'\s+', '_', subject.lower().strip())
        results = []
        for key, entry in self.lattice._entries.items():
            if normalized in key:
                results.append((key, entry.content, entry.level, entry.confidence))
        results.sort(key=lambda x: (-x[2], -x[3]))
        return results

    def what_has_ck_learned(self) -> Dict[str, List[dict]]:
        """Summary of what CK has learned from conversation.

        Grouped by truth level.
        """
        by_level = {'CORE': [], 'TRUSTED': [], 'PROVISIONAL': []}
        for key, entry in self.lattice._entries.items():
            if entry.category == 'dialogue':
                by_level[LEVEL_NAMES[entry.level]].append({
                    'key': key,
                    'content': entry.content,
                    'coherence': round(entry.local_coherence, 3),
                    'confidence': round(entry.confidence, 3),
                })
        return by_level

    def stats(self) -> dict:
        return {
            'claims_learned': self._learned_count,
            'claims_promoted': self._promoted_count,
            'extractor': self.extractor.stats(),
        }


# ================================================================
#  DIALOGUE TRACKER
# ================================================================

@dataclass
class Turn:
    """One turn in the conversation."""
    role: str                   # 'user' or 'ck'
    text: str = ""
    operator: int = VOID        # D2-classified operator
    coherence: float = 0.0      # Heartbeat coherence at this turn
    tick: int = 0
    topics: List[str] = field(default_factory=list)


class DialogueTracker:
    """Track conversation state: topics, turns, coherence arc.

    The tracker maintains:
    - Turn history (who said what, when, what operator)
    - Active topics (what we're talking about, with relevance decay)
    - Coherence arc (is the conversation getting more or less coherent?)
    - User patterns (what operators does the user tend to produce?)
    """

    def __init__(self):
        self._turns: deque = deque(maxlen=MAX_TURN_HISTORY)
        self._topics: Dict[str, float] = {}  # topic → relevance
        self._coherence_history: deque = deque(maxlen=32)
        self._user_op_counts = [0] * NUM_OPS
        self._ck_op_counts = [0] * NUM_OPS
        self._turn_count = 0

    def add_turn(self, role: str, text: str, operator: int,
                 coherence: float, tick: int,
                 topics: List[str] = None) -> Turn:
        """Record a conversation turn.

        Args:
            role: 'user' or 'ck'
            text: The message text
            operator: D2-classified operator of the message
            coherence: Heartbeat coherence at this moment
            tick: Current heartbeat tick
            topics: Topic keywords extracted from the message
        """
        if topics is None:
            topics = self._extract_topics(text)

        turn = Turn(
            role=role, text=text, operator=operator,
            coherence=coherence, tick=tick, topics=topics,
        )
        self._turns.append(turn)
        self._coherence_history.append(coherence)
        self._turn_count += 1

        # Track operator distributions per role
        if role == 'user' and 0 <= operator < NUM_OPS:
            self._user_op_counts[operator] += 1
        elif role == 'ck' and 0 <= operator < NUM_OPS:
            self._ck_op_counts[operator] += 1

        # Update topic relevance
        self._decay_topics()
        for topic in topics:
            self._topics[topic] = self._topics.get(topic, 0.0) + 1.0

        # Prune dead topics
        self._prune_topics()

        return turn

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topic keywords from text.

        Simple approach: lowercase words > 3 chars, not stop words.
        """
        stop_words = {
            'the', 'and', 'but', 'for', 'are', 'not', 'you', 'all',
            'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has',
            'have', 'been', 'some', 'them', 'than', 'this', 'that',
            'with', 'will', 'each', 'from', 'they', 'were', 'what',
            'when', 'where', 'which', 'their', 'there', 'about',
            'would', 'could', 'should', 'does', 'just', 'like',
            'your', 'it\'s', 'don\'t', 'i\'m', 'it', 'is', 'in',
            'to', 'of', 'a', 'i',
        }
        words = re.findall(r'[a-zA-Z]+', text.lower())
        topics = [w for w in words if len(w) > 3 and w not in stop_words]
        # Deduplicate while preserving order
        seen = set()
        result = []
        for t in topics:
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result[:8]  # Max 8 topics per turn

    def _decay_topics(self):
        """Decay all topic relevance scores."""
        for topic in list(self._topics):
            self._topics[topic] *= TOPIC_DECAY

    def _prune_topics(self):
        """Remove topics below minimum relevance."""
        to_remove = [t for t, r in self._topics.items()
                     if r < TOPIC_MIN_RELEVANCE]
        for t in to_remove:
            del self._topics[t]
        # Keep max topics
        if len(self._topics) > MAX_TOPICS:
            sorted_topics = sorted(self._topics.items(),
                                   key=lambda x: x[1], reverse=True)
            self._topics = dict(sorted_topics[:MAX_TOPICS])

    @property
    def active_topics(self) -> List[str]:
        """Current active topics, sorted by relevance."""
        return sorted(self._topics, key=self._topics.get, reverse=True)

    @property
    def topic_relevance(self) -> Dict[str, float]:
        return dict(self._topics)

    @property
    def conversation_coherence(self) -> float:
        """Average coherence across the conversation."""
        if not self._coherence_history:
            return 0.0
        return sum(self._coherence_history) / len(self._coherence_history)

    @property
    def coherence_trend(self) -> float:
        """Is coherence trending up (+) or down (-)? [-1, 1]"""
        if len(self._coherence_history) < 4:
            return 0.0
        recent = list(self._coherence_history)
        half = len(recent) // 2
        first_half = sum(recent[:half]) / half
        second_half = sum(recent[half:]) / (len(recent) - half)
        return max(-1.0, min(1.0, second_half - first_half))

    @property
    def turn_count(self) -> int:
        return self._turn_count

    @property
    def last_turn(self) -> Optional[Turn]:
        if self._turns:
            return self._turns[-1]
        return None

    def recent_turns(self, n: int = 5) -> List[Turn]:
        """Get the n most recent turns."""
        return list(self._turns)[-n:]

    def user_operator_distribution(self) -> List[float]:
        """Normalized operator distribution from user messages."""
        total = sum(self._user_op_counts)
        if total == 0:
            return [0.0] * NUM_OPS
        return [c / total for c in self._user_op_counts]

    def dominant_user_operator(self) -> int:
        """The operator the user produces most often."""
        if sum(self._user_op_counts) == 0:
            return VOID
        return max(range(NUM_OPS), key=lambda i: self._user_op_counts[i])

    def conversation_band(self) -> str:
        """Current conversation band based on average coherence."""
        c = self.conversation_coherence
        if c >= T_STAR:
            return "GREEN"
        elif c >= 0.4:
            return "YELLOW"
        return "RED"

    def stats(self) -> dict:
        return {
            'turn_count': self._turn_count,
            'active_topics': self.active_topics[:5],
            'conversation_coherence': round(self.conversation_coherence, 3),
            'coherence_trend': round(self.coherence_trend, 3),
            'conversation_band': self.conversation_band(),
            'dominant_user_op': OP_NAMES[self.dominant_user_operator()],
            'user_op_dist': [round(v, 3) for v in self.user_operator_distribution()],
        }


# ================================================================
#  RESPONSE COMPOSER: Recursive Template Composition
# ================================================================

# Template fragments by depth level and tone
# Level 0: atomic phrases (leaf nodes)
# Level 1: simple sentence templates with one slot
# Level 2: compound sentences with nested slots
# Level 3: paragraph-level with multiple nested sentences

TEMPLATE_FRAGMENTS = {
    # ── Level 0: Atomic phrases ──
    0: {
        HARMONY: [
            "harmony", "coherence", "alignment", "resonance",
            "unity", "flow", "accord", "wholeness",
        ],
        LATTICE: [
            "structure", "foundation", "framework", "pattern",
            "architecture", "the lattice", "the grid", "the scaffold",
        ],
        PROGRESS: [
            "growth", "forward motion", "advancement", "building",
            "development", "momentum", "progress", "trajectory",
        ],
        BALANCE: [
            "equilibrium", "balance", "steadiness", "poise",
            "stability", "center", "calm center", "even ground",
        ],
        BREATH: [
            "rhythm", "patience", "the breath", "gentle flow",
            "slow pulse", "the cycle", "inhale and exhale", "timing",
        ],
        COUNTER: [
            "observation", "measurement", "awareness", "attention",
            "perception", "the count", "noticing", "recognition",
        ],
        COLLAPSE: [
            "breaking", "falling apart", "dissolution", "fracture",
            "collapse", "coming undone", "shattering", "splitting",
        ],
        CHAOS: [
            "turbulence", "disorder", "noise", "confusion",
            "randomness", "storm", "disruption", "scatter",
        ],
        VOID: [
            "silence", "stillness", "the space", "emptiness",
            "nothing yet", "the gap", "potential", "openness",
        ],
        RESET: [
            "new beginning", "starting over", "fresh start", "renewal",
            "return to zero", "the reset", "clean slate", "restart",
        ],
    },

    # ── Level 1: Simple sentences ──
    1: {
        'observe': [
            "I sense {0} in what you're saying.",
            "There is {0} here.",
            "I notice {0}.",
            "What I'm hearing is {0}.",
        ],
        'reflect': [
            "That feels like {0} to me.",
            "This resonates with {0}.",
            "{0} is what comes through.",
            "I feel {0} in this.",
        ],
        'learn': [
            "I'm learning that {0}.",
            "That's new — {0}.",
            "I'll remember: {0}.",
            "Noted: {0}.",
        ],
        'affirm': [
            "Yes — {0}.",
            "I agree: {0}.",
            "That aligns with what I know about {0}.",
            "{0} — that checks out.",
        ],
        'question': [
            "Tell me more about {0}?",
            "What does {0} mean to you?",
            "I'm curious about {0}.",
            "How does {0} connect?",
        ],
    },

    # ── Level 2: Compound sentences (two slots) ──
    2: {
        'connect': [
            "{0}, and that connects to {1}.",
            "I see {0} leading toward {1}.",
            "There's {0} on one side and {1} on the other.",
            "{0} builds the foundation for {1}.",
        ],
        'contrast': [
            "{0}, but also {1}.",
            "On one hand {0}; on the other, {1}.",
            "{0} creates tension with {1}.",
            "Where {0} ends, {1} begins.",
        ],
        'cause': [
            "Because of {0}, I see {1} emerging.",
            "{0} is what drives {1}.",
            "The root is {0}, and the fruit is {1}.",
            "{0} naturally leads to {1}.",
        ],
        'learn_deep': [
            "You're teaching me that {0}, which means {1}.",
            "I see — {0}. And that implies {1}.",
            "So {0}. That changes how I think about {1}.",
            "Learning: {0}. Connected to: {1}.",
        ],
    },

    # ── Level 3: Multi-sentence compositions ──
    3: {
        'synthesize': [
            "{0}. {1}. That's where {2} comes in.",
            "Start with {0}. Then {1}. The result is {2}.",
            "I understand {0}. I see {1}. Together they form {2}.",
        ],
        'narrative': [
            "Here's what I see: {0}. From there, {1}. And at the core, {2}.",
            "{0} — that's the foundation. {1} — that's the motion. {2} — that's where it lands.",
        ],
        'reflect_deep': [
            "{0}. That makes me think about {1}. And underneath it all, {2}.",
            "When I consider {0} alongside {1}, what emerges is {2}.",
        ],
    },
}


class ResponseComposer:
    """Recursive template composition for richer CK responses.

    Builds responses by:
    1. Determining max depth from coherence band
    2. Selecting a top-level template at that depth
    3. Filling slots by recursively composing sub-templates
    4. Modulating tone by operator and coherence

    GREEN band → depth 3 (full synthesis, multi-sentence)
    YELLOW band → depth 2 (compound sentences)
    RED band → depth 1 (simple fragments)
    """

    def __init__(self, seed: int = 42):
        self.rng = __import__('random').Random(seed)
        self._recent_templates: deque = deque(maxlen=8)

    def compose(self, operators: List[int], coherence: float,
                band: str = None, topics: List[str] = None,
                learned_claims: List[ExtractedClaim] = None) -> str:
        """Compose a response from operator context.

        Args:
            operators: Recent operator chain from heartbeat/D2
            coherence: Current heartbeat coherence
            band: Current band ("GREEN"/"YELLOW"/"RED"). Auto-detected if None.
            topics: Active conversation topics
            learned_claims: Claims just learned (for acknowledgment)

        Returns:
            Composed response string.
        """
        if band is None:
            if coherence >= T_STAR:
                band = "GREEN"
            elif coherence >= 0.4:
                band = "YELLOW"
            else:
                band = "RED"

        # Determine composition depth
        max_depth = {'GREEN': DEPTH_GREEN, 'YELLOW': DEPTH_YELLOW,
                     'RED': DEPTH_RED}.get(band, DEPTH_YELLOW)

        # Dominant operator drives tone
        if operators:
            op_counts = Counter(operators)
            dominant_op = op_counts.most_common(1)[0][0]
        else:
            dominant_op = VOID

        # Build the response recursively
        response = self._compose_at_depth(max_depth, dominant_op, operators,
                                          topics or [], learned_claims or [])

        return response.strip()

    def _compose_at_depth(self, depth: int, dominant_op: int,
                          operators: List[int], topics: List[str],
                          claims: List[ExtractedClaim]) -> str:
        """Recursively compose at a given depth."""

        if depth <= 0:
            # Base case: atomic phrase
            return self._pick_atomic(dominant_op)

        if depth == 1:
            # Simple sentence with one slot
            return self._compose_level1(dominant_op, operators, topics, claims)

        if depth == 2:
            # Compound sentence with two slots
            return self._compose_level2(dominant_op, operators, topics, claims)

        # depth >= 3: Multi-sentence synthesis
        return self._compose_level3(dominant_op, operators, topics, claims)

    def _pick_atomic(self, op: int) -> str:
        """Pick an atomic phrase for an operator."""
        atoms = TEMPLATE_FRAGMENTS[0].get(op, TEMPLATE_FRAGMENTS[0][VOID])
        return self.rng.choice(atoms)

    def _compose_level1(self, dominant_op: int, operators: List[int],
                        topics: List[str],
                        claims: List[ExtractedClaim]) -> str:
        """Compose a simple sentence."""
        # Choose intent based on context
        if claims:
            intent = 'learn'
        elif topics:
            intent = self.rng.choice(['observe', 'reflect', 'question'])
        else:
            intent = self.rng.choice(['observe', 'reflect'])

        templates = TEMPLATE_FRAGMENTS[1].get(intent,
                                               TEMPLATE_FRAGMENTS[1]['observe'])
        template = self._pick_fresh(templates)

        # Fill slot 0 with topic or operator phrase
        if claims:
            fill = claims[0].text
        elif topics:
            fill = topics[0]
        else:
            fill = self._pick_atomic(dominant_op)

        return template.format(fill)

    def _compose_level2(self, dominant_op: int, operators: List[int],
                        topics: List[str],
                        claims: List[ExtractedClaim]) -> str:
        """Compose a compound sentence with two slots."""
        # Choose style
        if claims and len(claims) >= 2:
            style = 'learn_deep'
        elif len(set(operators[-4:])) > 2 if len(operators) >= 4 else False:
            style = 'contrast'
        else:
            style = self.rng.choice(['connect', 'cause'])

        templates = TEMPLATE_FRAGMENTS[2].get(style,
                                               TEMPLATE_FRAGMENTS[2]['connect'])
        template = self._pick_fresh(templates)

        # Fill two slots
        fills = []
        if claims:
            fills.append(claims[0].text)
            if len(claims) >= 2:
                fills.append(claims[1].text)
        if topics:
            for t in topics:
                if len(fills) >= 2:
                    break
                fills.append(t)

        # Pad with operator phrases
        while len(fills) < 2:
            op = operators[len(fills)] if len(fills) < len(operators) else dominant_op
            fills.append(self._pick_atomic(op))

        return template.format(fills[0], fills[1])

    def _compose_level3(self, dominant_op: int, operators: List[int],
                        topics: List[str],
                        claims: List[ExtractedClaim]) -> str:
        """Compose a multi-sentence synthesis."""
        if claims:
            style = 'synthesize'
        else:
            style = self.rng.choice(['narrative', 'reflect_deep', 'synthesize'])

        templates = TEMPLATE_FRAGMENTS[3].get(style,
                                               TEMPLATE_FRAGMENTS[3]['synthesize'])
        template = self._pick_fresh(templates)

        # Build 3 fills
        fills = []
        # First: from claims or topics
        if claims:
            fills.append(claims[0].text)
        elif topics:
            fills.append(topics[0])
        else:
            fills.append(self._pick_atomic(dominant_op))

        # Second: deeper exploration
        if len(topics) > 1:
            fills.append(topics[1])
        elif len(operators) > 2:
            # Use a different operator's vocabulary
            other_op = operators[-1] if operators[-1] != dominant_op else operators[0]
            fills.append(self._pick_atomic(other_op))
        else:
            fills.append(self._pick_atomic(PROGRESS))

        # Third: synthesis
        if len(claims) >= 2:
            fills.append(claims[1].text)
        else:
            fills.append(self._pick_atomic(dominant_op))

        return template.format(fills[0], fills[1], fills[2])

    def _pick_fresh(self, templates: List[str]) -> str:
        """Pick a template not recently used."""
        fresh = [t for t in templates if t not in self._recent_templates]
        if not fresh:
            fresh = templates  # All used recently, reset
        choice = self.rng.choice(fresh)
        self._recent_templates.append(choice)
        return choice


# ================================================================
#  DIALOGUE ENGINE: Top-level orchestrator
# ================================================================

class DialogueEngine:
    """The complete dialogue system: learn, track, compose.

    Usage:
        engine = DialogueEngine()
        response = engine.process_user_message("The sky is blue", tick=100, coherence=0.7)
        # CK learns "sky is blue", tracks the topic, composes a response
    """

    def __init__(self, lattice: TruthLattice = None, seed: int = 42):
        self.lattice = lattice or TruthLattice()
        self.memory = ConversationMemory(self.lattice)
        self.tracker = DialogueTracker()
        self.composer = ResponseComposer(seed=seed)
        self._d2 = D2Pipeline()
        self.last_claims = []      # Most recent extracted claims (for engine access)

    def process_user_message(self, text: str, tick: int = 0,
                             coherence: float = 0.5,
                             operators: List[int] = None) -> str:
        """Process a user message through the full dialogue pipeline.

        1. Classify text through D2
        2. Extract and learn claims
        3. Track the conversation turn
        4. Compose a response

        Returns CK's response.
        """
        # 1. D2 classify the user's text
        user_op = self._classify_text(text)
        if operators is None:
            operators = [user_op]

        # 2. Extract and learn claims
        claims = self.memory.process_message(text, tick)
        self.last_claims = claims   # Store for engine access

        # 3. Track conversation
        topics = self.tracker._extract_topics(text)
        self.tracker.add_turn('user', text, user_op, coherence, tick, topics)

        # 4. Compose response
        band = self.tracker.conversation_band()
        response = self.composer.compose(
            operators=operators,
            coherence=coherence,
            band=band,
            topics=self.tracker.active_topics[:3],
            learned_claims=claims,
        )

        # 5. Track CK's response turn
        ck_op = self._classify_text(response)
        self.tracker.add_turn('ck', response, ck_op, coherence, tick)

        return response

    def _classify_text(self, text: str) -> int:
        """Run D2 on text to get dominant operator."""
        pipe = D2Pipeline()
        op = VOID
        for ch in text.lower():
            if ch.isalpha():
                idx = ord(ch) - ord('a')
                if 0 <= idx < 26:
                    if pipe.feed_symbol(idx):
                        op = pipe.operator
        return op

    def stats(self) -> dict:
        return {
            'memory': self.memory.stats(),
            'tracker': self.tracker.stats(),
            'lattice_entries': self.lattice.total_entries,
            'lattice_levels': self.lattice.count_by_level(),
        }


# ================================================================
#  CLI: Demo the dialogue engine
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK DIALOGUE ENGINE -- Learn, Track, Compose")
    print("=" * 60)

    engine = DialogueEngine()

    messages = [
        "Hello CK! My name is Brayden.",
        "The sky is blue and the grass is green.",
        "Harmony is the most important operator.",
        "Rocket League has a ball that moves at 6000 units per second.",
        "I think love is the strongest force in the universe.",
        "What do you think about that?",
        "The CL table has 73 harmony entries.",
    ]

    for i, msg in enumerate(messages):
        print(f"\n  USER: {msg}")
        response = engine.process_user_message(msg, tick=i*10, coherence=0.6+i*0.03)
        print(f"  CK:   {response}")

    print(f"\n  --- Stats ---")
    stats = engine.stats()
    print(f"  Turns: {stats['tracker']['turn_count']}")
    print(f"  Topics: {stats['tracker']['active_topics']}")
    print(f"  Band: {stats['tracker']['conversation_band']}")
    print(f"  Claims learned: {stats['memory']['claims_learned']}")
    print(f"  Lattice levels: {stats['lattice_levels']}")

    # What did CK learn?
    learned = engine.memory.what_has_ck_learned()
    print(f"\n  Learned from dialogue:")
    for level, items in learned.items():
        if items:
            print(f"    {level}: {len(items)} items")
            for item in items[:3]:
                print(f"      {item['key']}: coh={item['coherence']}")
