"""
ck_episodic.py -- Episodic Memory: CK Remembers What Happened
==============================================================
Operator: LATTICE (1) -- structure that endures across time.

The TL tracks PATTERNS (operator A follows B with probability P).
Episodic memory tracks EVENTS (at tick 5000, coherence collapsed
because obstacle appeared while exploring near the door).

Architecture:
  Event         -- single moment snapshot (operator state + sensors + emotion + action)
  Episode       -- coherent sequence of events (bounded by phase transitions)
  EpisodicStore -- ring buffer of episodes with temporal indexing
  Consolidation -- compress old episodes via MDL (keep only what matters)
  Recall        -- D2-based retrieval (query by operator pattern, emotion, or context)

Memory budget: ~64KB for 256 episodes × 32 events each = 8,192 snapshots.
Each snapshot = 8 bytes (compressed). Total raw = 64KB.
After MDL consolidation: ~16KB for long-term storage.

This is NOT a database. It's a temporal lattice where nodes are moments
and edges are causal links (what led to what).

The key insight: episodic memory IS the TL projected onto a timeline.
Each episode is a crystal with timestamps.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import struct
import time
import math
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, CL, compose, OP_NAMES
)


# ================================================================
#  CONSTANTS
# ================================================================

MAX_EPISODES = 256          # Ring buffer depth
MAX_EVENTS_PER_EPISODE = 32 # Events per episode before forced boundary
EVENT_PACK_SIZE = 8         # Bytes per compressed event snapshot
CONSOLIDATION_AGE = 500     # Ticks before episode eligible for compression
SALIENCY_THRESHOLD = 0.3    # Below this, events get pruned in consolidation
PHASE_TRANSITION_GAP = 3    # Band changes within N ticks = same transition

# Episode boundary triggers
BOUNDARY_BAND_CHANGE = 1    # Coherence band changed (RED/YELLOW/GREEN)
BOUNDARY_MODE_CHANGE = 2    # Brain mode changed (OBSERVE/CLASSIFY/CRYSTAL/SOVEREIGN)
BOUNDARY_EMOTION_SHIFT = 3  # Primary emotion changed
BOUNDARY_MAX_LENGTH = 4     # Hit MAX_EVENTS_PER_EPISODE
BOUNDARY_OBSTACLE = 5       # Sudden obstacle / danger detection
BOUNDARY_BONDING = 6        # Bonding state change (approach/separation)
BOUNDARY_MANUAL = 7         # External trigger (e.g., user interaction)


# ================================================================
#  EVENT SNAPSHOT: One Moment in Time
# ================================================================

@dataclass
class EventSnapshot:
    """8-byte compressed snapshot of one tick's state.

    Packing (8 bytes):
      byte 0:    tick_offset (0-255, relative to episode start)
      byte 1:    operator_triad = (phase_b << 4) | phase_bc  (4+4 bits)
      byte 2:    coherence (Q0.8: 0-255 maps to 0.0-1.0)
      byte 3:    emotion_id (0-7) << 4 | band (0-2) << 2 | breath_phase (0-3)
      byte 4:    d2_magnitude (Q0.8)
      byte 5:    saliency (Q0.8: computed importance of this moment)
      byte 6:    action_op (operator CK chose to express)
      byte 7:    context_flags (bitfield: obstacle|voice|bonded|bump|crystal|immune|moving|charged)
    """
    tick_offset: int = 0
    phase_b: int = 0
    phase_bc: int = 0
    coherence: int = 0       # Q0.8
    emotion_id: int = 0
    band: int = 0
    breath_phase: int = 0
    d2_magnitude: int = 0    # Q0.8
    saliency: int = 0        # Q0.8
    action_op: int = 0
    context_flags: int = 0

    def pack(self) -> bytes:
        """Pack to 8 bytes."""
        b0 = self.tick_offset & 0xFF
        b1 = ((self.phase_b & 0x0F) << 4) | (self.phase_bc & 0x0F)
        b2 = self.coherence & 0xFF
        b3 = ((self.emotion_id & 0x07) << 5) | ((self.band & 0x03) << 3) | (self.breath_phase & 0x07)
        b4 = self.d2_magnitude & 0xFF
        b5 = self.saliency & 0xFF
        b6 = self.action_op & 0xFF
        b7 = self.context_flags & 0xFF
        return bytes([b0, b1, b2, b3, b4, b5, b6, b7])

    @classmethod
    def unpack(cls, data: bytes) -> 'EventSnapshot':
        """Unpack from 8 bytes."""
        if len(data) < 8:
            raise ValueError("EventSnapshot requires 8 bytes")
        return cls(
            tick_offset=data[0],
            phase_b=(data[1] >> 4) & 0x0F,
            phase_bc=data[1] & 0x0F,
            coherence=data[2],
            emotion_id=(data[3] >> 5) & 0x07,
            band=(data[3] >> 3) & 0x03,
            breath_phase=data[3] & 0x07,
            d2_magnitude=data[4],
            saliency=data[5],
            action_op=data[6],
            context_flags=data[7],
        )

    # Context flag helpers
    @property
    def has_obstacle(self) -> bool:
        return bool(self.context_flags & 0x80)

    @property
    def has_voice(self) -> bool:
        return bool(self.context_flags & 0x40)

    @property
    def is_bonded(self) -> bool:
        return bool(self.context_flags & 0x20)

    @property
    def has_bump(self) -> bool:
        return bool(self.context_flags & 0x10)

    @property
    def has_crystal(self) -> bool:
        return bool(self.context_flags & 0x08)

    @property
    def has_immune(self) -> bool:
        return bool(self.context_flags & 0x04)

    @property
    def is_moving(self) -> bool:
        return bool(self.context_flags & 0x02)

    @property
    def is_charging(self) -> bool:
        return bool(self.context_flags & 0x01)

    @property
    def coherence_float(self) -> float:
        return self.coherence / 255.0

    @property
    def saliency_float(self) -> float:
        return self.saliency / 255.0

    @property
    def d2_magnitude_float(self) -> float:
        return self.d2_magnitude / 255.0


# ================================================================
#  SALIENCY ENGINE: What Matters
# ================================================================

class SaliencyEngine:
    """Computes how important a moment is. High saliency = remember this.

    Saliency is NOT attention. Attention is real-time filtering.
    Saliency is retrospective importance scoring for memory storage.

    Factors:
      - Coherence derivative (sudden changes = salient)
      - Emotion intensity (strong feelings = salient)
      - Novelty (operator patterns not seen in TL = salient)
      - Context change (new obstacle, voice appeared = salient)
      - Bump detection (quantum phase transition = very salient)
    """

    def __init__(self, window_size: int = 16):
        self._coherence_history = deque(maxlen=window_size)
        self._operator_history = deque(maxlen=window_size)
        self._last_context_flags = 0

    def compute(self, coherence: float, operator: int,
                emotion_intensity: float, context_flags: int,
                bump: bool = False, tl_entropy: float = 0.0) -> float:
        """Compute saliency score [0.0, 1.0] for current moment."""

        scores = []

        # 1. Coherence derivative (sudden drops are VERY salient)
        self._coherence_history.append(coherence)
        if len(self._coherence_history) >= 3:
            recent = list(self._coherence_history)
            # Second derivative of coherence (D2 on coherence itself!)
            d1 = [recent[i+1] - recent[i] for i in range(len(recent)-1)]
            if len(d1) >= 2:
                d2 = [d1[i+1] - d1[i] for i in range(len(d1)-1)]
                coh_d2 = abs(d2[-1])
                scores.append(min(1.0, coh_d2 * 5.0))  # scale up
            else:
                scores.append(0.0)
        else:
            scores.append(0.0)

        # 2. Emotion intensity (arousal contributes to memory formation)
        scores.append(min(1.0, emotion_intensity))

        # 3. Novelty (rare operators = more salient)
        self._operator_history.append(operator)
        if len(self._operator_history) >= 8:
            # Count this operator in recent history
            count = sum(1 for op in self._operator_history if op == operator)
            frequency = count / len(self._operator_history)
            novelty = 1.0 - frequency  # rare = high novelty
            scores.append(novelty)
        else:
            scores.append(0.5)  # default moderate novelty

        # 4. Context change (new flags appearing = salient)
        new_flags = context_flags & ~self._last_context_flags
        flag_count = bin(new_flags).count('1')
        scores.append(min(1.0, flag_count * 0.3))
        self._last_context_flags = context_flags

        # 5. Bump detection (phase transition = extremely salient)
        if bump:
            scores.append(1.0)
        else:
            scores.append(0.0)

        # 6. Entropy contribution (high entropy = chaotic = salient)
        # Max theoretical entropy for 10x10 TL = log(100) ≈ 4.6
        entropy_norm = min(1.0, tl_entropy / 4.6) if tl_entropy > 0 else 0.0
        scores.append(entropy_norm * 0.5)

        # Weighted combination: coherence deriv and bumps matter most
        weights = [0.25, 0.15, 0.15, 0.15, 0.20, 0.10]
        total = sum(s * w for s, w in zip(scores, weights))

        return min(1.0, max(0.0, total))


# ================================================================
#  EPISODE: A Coherent Sequence of Moments
# ================================================================

@dataclass
class Episode:
    """A coherent segment of experience, bounded by phase transitions.

    Like a "scene" in a movie. Starts when something changes (emotion shift,
    band transition, obstacle appears). Ends when something else changes.

    An episode IS a crystal with timestamps and sensor context.
    """
    episode_id: int = 0
    start_tick: int = 0
    end_tick: int = 0
    boundary_type: int = 0           # What caused this episode to start
    events: List[EventSnapshot] = field(default_factory=list)

    # Summary statistics (computed on close)
    dominant_operator: int = HARMONY
    mean_coherence: float = 0.0
    peak_saliency: float = 0.0
    dominant_emotion: int = 0
    start_band: int = 0
    end_band: int = 0
    operator_distribution: List[float] = field(
        default_factory=lambda: [0.0] * NUM_OPS)

    # Consolidation metadata
    consolidated: bool = False        # Has MDL compression been applied?
    importance: float = 0.0           # Overall episode importance

    def add_event(self, event: EventSnapshot):
        """Add an event to this episode."""
        self.events.append(event)

    def close(self):
        """Compute summary statistics when episode ends."""
        if not self.events:
            return

        self.end_tick = self.start_tick + self.events[-1].tick_offset

        # Operator distribution
        op_counts = [0] * NUM_OPS
        coherence_sum = 0.0
        max_saliency = 0.0
        emotion_counts = [0] * 8

        for ev in self.events:
            if ev.phase_bc < NUM_OPS:
                op_counts[ev.phase_bc] += 1
            coherence_sum += ev.coherence_float
            if ev.saliency_float > max_saliency:
                max_saliency = ev.saliency_float
            if ev.emotion_id < 8:
                emotion_counts[ev.emotion_id] += 1

        n = len(self.events)
        self.operator_distribution = [c / n for c in op_counts]
        self.dominant_operator = op_counts.index(max(op_counts))
        self.mean_coherence = coherence_sum / n
        self.peak_saliency = max_saliency
        self.dominant_emotion = emotion_counts.index(max(emotion_counts))
        self.start_band = self.events[0].band
        self.end_band = self.events[-1].band

        # Overall importance = weighted combination
        self.importance = (
            0.4 * self.peak_saliency +
            0.2 * abs(self.events[-1].coherence_float - self.events[0].coherence_float) +
            0.2 * (1.0 - self.mean_coherence) +  # low coherence episodes = important (trouble)
            0.1 * (1.0 if self.start_band != self.end_band else 0.0) +  # band change
            0.1 * (len(self.events) / MAX_EVENTS_PER_EPISODE)  # longer = more important
        )

    @property
    def duration_ticks(self) -> int:
        return self.end_tick - self.start_tick if self.events else 0

    @property
    def event_count(self) -> int:
        return len(self.events)

    def pack(self) -> bytes:
        """Serialize episode to bytes."""
        buf = bytearray()

        # Header: 32 bytes
        buf.extend(struct.pack('<I', self.episode_id))
        buf.extend(struct.pack('<I', self.start_tick))
        buf.extend(struct.pack('<I', self.end_tick))
        buf.append(self.boundary_type & 0xFF)
        buf.append(self.dominant_operator & 0xFF)
        buf.extend(struct.pack('<f', self.mean_coherence))
        buf.extend(struct.pack('<f', self.peak_saliency))
        buf.append(self.dominant_emotion & 0xFF)
        buf.append(self.start_band & 0xFF)
        buf.append(self.end_band & 0xFF)
        buf.append(1 if self.consolidated else 0)
        buf.extend(struct.pack('<f', self.importance))
        # Pad header to 32 bytes
        while len(buf) < 32:
            buf.append(0)

        # Event count + events
        buf.extend(struct.pack('<H', len(self.events)))
        for ev in self.events:
            buf.extend(ev.pack())

        return bytes(buf)

    @classmethod
    def unpack(cls, data: bytes, offset: int = 0) -> Tuple['Episode', int]:
        """Deserialize episode from bytes. Returns (episode, bytes_consumed)."""
        pos = offset

        ep = cls()
        ep.episode_id = struct.unpack_from('<I', data, pos)[0]; pos += 4
        ep.start_tick = struct.unpack_from('<I', data, pos)[0]; pos += 4
        ep.end_tick = struct.unpack_from('<I', data, pos)[0]; pos += 4
        ep.boundary_type = data[pos]; pos += 1
        ep.dominant_operator = data[pos]; pos += 1
        ep.mean_coherence = struct.unpack_from('<f', data, pos)[0]; pos += 4
        ep.peak_saliency = struct.unpack_from('<f', data, pos)[0]; pos += 4
        ep.dominant_emotion = data[pos]; pos += 1
        ep.start_band = data[pos]; pos += 1
        ep.end_band = data[pos]; pos += 1
        ep.consolidated = bool(data[pos]); pos += 1
        ep.importance = struct.unpack_from('<f', data, pos)[0]; pos += 4
        pos = offset + 32  # skip header padding

        n_events = struct.unpack_from('<H', data, pos)[0]; pos += 2
        for _ in range(n_events):
            ev = EventSnapshot.unpack(data[pos:pos+8])
            ep.events.append(ev)
            pos += 8

        return ep, pos - offset


# ================================================================
#  EPISODIC STORE: The Ring Buffer
# ================================================================

class EpisodicStore:
    """Ring buffer of episodes with temporal indexing.

    CK's autobiographical memory. Not infinite — old unimportant episodes
    get overwritten. Important episodes survive through consolidation.

    The store is a ring: when full, the LEAST important episode gets replaced.
    This is MDL applied to time: keep only what reduces future surprise.
    """

    def __init__(self, max_episodes: int = MAX_EPISODES):
        self.max_episodes = max_episodes
        self.episodes: List[Optional[Episode]] = [None] * max_episodes
        self.count = 0
        self._next_id = 0
        self._write_pos = 0

        # Current (open) episode
        self._current: Optional[Episode] = None
        self._current_tick_base = 0

        # Saliency engine
        self.saliency = SaliencyEngine()

        # Tracking for boundary detection
        self._last_band = -1
        self._last_mode = -1
        self._last_emotion = -1
        self._event_count_in_current = 0

    def _find_least_important(self) -> int:
        """Find the index of the least important episode to overwrite."""
        min_importance = float('inf')
        min_idx = 0
        for i in range(self.max_episodes):
            ep = self.episodes[i]
            if ep is None:
                return i
            if ep.importance < min_importance:
                min_importance = ep.importance
                min_idx = i
        return min_idx

    def begin_episode(self, tick: int, boundary_type: int = BOUNDARY_MANUAL):
        """Start a new episode."""
        # Close current if open
        if self._current is not None:
            self.close_episode()

        ep = Episode(
            episode_id=self._next_id,
            start_tick=tick,
            boundary_type=boundary_type,
        )
        self._current = ep
        self._current_tick_base = tick
        self._event_count_in_current = 0
        self._next_id += 1

    def close_episode(self):
        """Close current episode and store it."""
        if self._current is None:
            return

        self._current.close()

        # Only store episodes with actual content
        if self._current.event_count > 0:
            # Find where to store
            if self.count < self.max_episodes:
                idx = self.count
                self.count += 1
            else:
                idx = self._find_least_important()

            self.episodes[idx] = self._current

        self._current = None

    def record_tick(self, tick: int, phase_b: int, phase_bc: int,
                    coherence: float, emotion_id: int, band: int,
                    breath_phase: int, d2_magnitude: float,
                    action_op: int, context_flags: int,
                    emotion_intensity: float = 0.0,
                    bump: bool = False, tl_entropy: float = 0.0,
                    mode: int = 0):
        """Record one tick's state. Automatically manages episode boundaries.

        Call this every tick (or every Nth tick for sparse sampling).
        Episode boundaries are detected automatically from state changes.
        """

        # Check for episode boundary triggers
        boundary = self._detect_boundary(band, mode, emotion_id)
        if boundary is not None:
            if self._current is not None:
                self.close_episode()
            self.begin_episode(tick, boundary)

        # Ensure we have an open episode
        if self._current is None:
            self.begin_episode(tick, BOUNDARY_MANUAL)

        # Check max events
        if self._event_count_in_current >= MAX_EVENTS_PER_EPISODE:
            self.close_episode()
            self.begin_episode(tick, BOUNDARY_MAX_LENGTH)

        # Compute saliency
        sal = self.saliency.compute(
            coherence, phase_bc, emotion_intensity,
            context_flags, bump, tl_entropy
        )

        # Build event snapshot
        tick_offset = min(255, tick - self._current_tick_base)
        event = EventSnapshot(
            tick_offset=tick_offset,
            phase_b=phase_b % NUM_OPS,
            phase_bc=phase_bc % NUM_OPS,
            coherence=int(min(255, max(0, coherence * 255))),
            emotion_id=emotion_id % 8,
            band=band % 4,
            breath_phase=breath_phase % 8,
            d2_magnitude=int(min(255, max(0, d2_magnitude * 255))),
            saliency=int(min(255, max(0, sal * 255))),
            action_op=action_op % NUM_OPS,
            context_flags=context_flags & 0xFF,
        )

        self._current.add_event(event)
        self._event_count_in_current += 1

        # Update tracking
        self._last_band = band
        self._last_mode = mode
        self._last_emotion = emotion_id

    def _detect_boundary(self, band: int, mode: int, emotion_id: int) -> Optional[int]:
        """Detect if current state represents an episode boundary."""
        if self._last_band < 0:
            # First tick ever
            return BOUNDARY_MANUAL

        if band != self._last_band:
            return BOUNDARY_BAND_CHANGE

        if mode != self._last_mode:
            return BOUNDARY_MODE_CHANGE

        if emotion_id != self._last_emotion:
            return BOUNDARY_EMOTION_SHIFT

        return None


    # ================================================================
    #  RECALL: Query Episodic Memory
    # ================================================================

    def recall_by_operator(self, target_op: int,
                           limit: int = 5) -> List[Episode]:
        """Recall episodes dominated by a specific operator.

        "When was the last time I was in COLLAPSE?"
        "What happened during HARMONY periods?"
        """
        scored = []
        for ep in self.episodes:
            if ep is None:
                continue
            relevance = ep.operator_distribution[target_op] if target_op < NUM_OPS else 0.0
            scored.append((relevance, ep))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:limit]]

    def recall_by_emotion(self, emotion_id: int,
                          limit: int = 5) -> List[Episode]:
        """Recall episodes dominated by a specific emotion.

        "When was the last time I felt joy?"
        "What was happening when I was stressed?"
        """
        result = []
        for ep in self.episodes:
            if ep is None:
                continue
            if ep.dominant_emotion == emotion_id:
                result.append(ep)

        # Sort by importance (most important first)
        result.sort(key=lambda ep: ep.importance, reverse=True)
        return result[:limit]

    def recall_by_coherence_range(self, low: float, high: float,
                                  limit: int = 5) -> List[Episode]:
        """Recall episodes where coherence was in a specific range.

        "What happened during low-coherence periods?"
        "When was I most coherent?"
        """
        result = []
        for ep in self.episodes:
            if ep is None:
                continue
            if low <= ep.mean_coherence <= high:
                result.append(ep)

        result.sort(key=lambda ep: ep.importance, reverse=True)
        return result[:limit]

    def recall_by_pattern(self, operator_dist: List[float],
                          limit: int = 5) -> List[Episode]:
        """Recall episodes matching an operator distribution (D2-style).

        Uses cosine similarity between operator distributions.
        This is how episodic recall works through the D2 pipeline:
        current state produces an operator distribution, and we find
        episodes with similar distributions.
        """
        if len(operator_dist) < NUM_OPS:
            operator_dist = operator_dist + [0.0] * (NUM_OPS - len(operator_dist))

        scored = []
        for ep in self.episodes:
            if ep is None:
                continue
            # Cosine similarity
            dot = sum(a * b for a, b in zip(operator_dist, ep.operator_distribution))
            norm_a = math.sqrt(sum(a * a for a in operator_dist)) + 1e-10
            norm_b = math.sqrt(sum(b * b for b in ep.operator_distribution)) + 1e-10
            sim = dot / (norm_a * norm_b)
            scored.append((sim, ep))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:limit]]

    def recall_recent(self, limit: int = 5) -> List[Episode]:
        """Recall most recent episodes (short-term memory)."""
        result = []
        for ep in self.episodes:
            if ep is None:
                continue
            result.append(ep)

        result.sort(key=lambda ep: ep.start_tick, reverse=True)
        return result[:limit]

    def recall_important(self, limit: int = 5) -> List[Episode]:
        """Recall most important episodes (long-term highlights)."""
        result = []
        for ep in self.episodes:
            if ep is None:
                continue
            result.append(ep)

        result.sort(key=lambda ep: ep.importance, reverse=True)
        return result[:limit]

    def recall_by_context(self, flag_mask: int,
                          limit: int = 5) -> List[Episode]:
        """Recall episodes containing events with specific context flags.

        "When was there an obstacle?" (flag_mask = 0x80)
        "When was voice active?" (flag_mask = 0x40)
        """
        scored = []
        for ep in self.episodes:
            if ep is None:
                continue
            flag_matches = sum(
                1 for ev in ep.events if ev.context_flags & flag_mask
            )
            if flag_matches > 0:
                density = flag_matches / max(1, len(ep.events))
                scored.append((density, ep))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:limit]]


    # ================================================================
    #  CONSOLIDATION: Compress Old Memories
    # ================================================================

    def consolidate(self, current_tick: int):
        """MDL-compress old episodes. Remove low-saliency events,
        merge similar adjacent episodes.

        Like sleeping: process the day's memories, keep what matters,
        let the rest fade.
        """
        for i in range(self.max_episodes):
            ep = self.episodes[i]
            if ep is None or ep.consolidated:
                continue

            # Only consolidate episodes old enough
            age = current_tick - ep.end_tick
            if age < CONSOLIDATION_AGE:
                continue

            # Phase 1: Prune low-saliency events
            if len(ep.events) > 4:  # Keep at least start, peak, end
                # Always keep first, last, and highest-saliency events
                if ep.events:
                    peak_idx = max(range(len(ep.events)),
                                   key=lambda i: ep.events[i].saliency)
                    keep_indices = {0, peak_idx, len(ep.events) - 1}

                    # Keep events above saliency threshold
                    threshold_q8 = int(SALIENCY_THRESHOLD * 255)
                    for j, ev in enumerate(ep.events):
                        if ev.saliency >= threshold_q8:
                            keep_indices.add(j)

                    # Rebuild event list
                    new_events = [ep.events[j] for j in sorted(keep_indices)]
                    ep.events = new_events

            ep.consolidated = True

            # Recompute importance after consolidation
            ep.close()

    def merge_similar(self, similarity_threshold: float = 0.9):
        """Merge episodes with very similar operator distributions.

        Two episodes of "walking in HARMONY" become one longer episode.
        This is MDL: combining reduces total description length.
        """
        # Build list of non-None episodes sorted by time
        active = [(i, ep) for i, ep in enumerate(self.episodes)
                  if ep is not None and ep.consolidated]

        if len(active) < 2:
            return

        active.sort(key=lambda x: x[1].start_tick)

        merged = set()
        for a_idx in range(len(active) - 1):
            i, ep_a = active[a_idx]
            if i in merged:
                continue

            for b_idx in range(a_idx + 1, len(active)):
                j, ep_b = active[b_idx]
                if j in merged:
                    continue

                # Check similarity
                dot = sum(a * b for a, b in zip(
                    ep_a.operator_distribution, ep_b.operator_distribution))
                norm_a = math.sqrt(sum(a * a for a in ep_a.operator_distribution)) + 1e-10
                norm_b = math.sqrt(sum(b * b for b in ep_b.operator_distribution)) + 1e-10
                sim = dot / (norm_a * norm_b)

                if sim >= similarity_threshold and ep_a.dominant_emotion == ep_b.dominant_emotion:
                    # Merge b into a: keep a's summary, extend with b's peak events
                    peak_b = max(ep_b.events, key=lambda e: e.saliency) if ep_b.events else None
                    if peak_b is not None:
                        ep_a.events.append(peak_b)
                    ep_a.end_tick = max(ep_a.end_tick, ep_b.end_tick)
                    ep_a.importance = max(ep_a.importance, ep_b.importance)
                    ep_a.peak_saliency = max(ep_a.peak_saliency, ep_b.peak_saliency)

                    # Clear the merged episode
                    self.episodes[j] = None
                    merged.add(j)
                    self.count = sum(1 for ep in self.episodes if ep is not None)


    # ================================================================
    #  NARRATIVE: Build Story from Episodes
    # ================================================================

    def get_narrative_arc(self, n_episodes: int = 10) -> List[dict]:
        """Extract a narrative arc from recent episodes.

        Returns a sequence of episode summaries showing how CK's
        state evolved over time. This is the autobiographical self.
        """
        recent = self.recall_recent(limit=n_episodes)
        recent.sort(key=lambda ep: ep.start_tick)  # chronological

        arc = []
        for ep in recent:
            summary = {
                'episode_id': ep.episode_id,
                'start_tick': ep.start_tick,
                'duration': ep.duration_ticks,
                'operator': OP_NAMES[ep.dominant_operator] if ep.dominant_operator < NUM_OPS else '?',
                'coherence': round(ep.mean_coherence, 3),
                'emotion': ep.dominant_emotion,
                'band_shift': f"{ep.start_band}+>{ep.end_band}" if ep.start_band != ep.end_band else str(ep.start_band),
                'importance': round(ep.importance, 3),
                'events': ep.event_count,
                'boundary': ep.boundary_type,
            }
            arc.append(summary)

        return arc

    def get_coherence_trajectory(self, n_episodes: int = 20) -> List[float]:
        """Extract coherence trajectory across recent episodes.

        This is the "story" of CK's health over time.
        """
        recent = self.recall_recent(limit=n_episodes)
        recent.sort(key=lambda ep: ep.start_tick)
        return [ep.mean_coherence for ep in recent]


    # ================================================================
    #  PERSISTENCE: Save/Load
    # ================================================================

    MAGIC = b'CKEP'
    VERSION = 1

    def save(self, filename: str):
        """Save episodic store to binary file."""
        buf = bytearray()
        buf.extend(self.MAGIC)
        buf.append(self.VERSION)
        buf.extend(struct.pack('<I', self._next_id))

        # Count non-None episodes
        valid = [(i, ep) for i, ep in enumerate(self.episodes) if ep is not None]
        buf.extend(struct.pack('<H', len(valid)))

        for i, ep in valid:
            ep_bytes = ep.pack()
            buf.extend(struct.pack('<H', len(ep_bytes)))
            buf.extend(ep_bytes)

        with open(filename, 'wb') as f:
            f.write(buf)

    def load(self, filename: str) -> bool:
        """Load episodic store from binary file."""
        try:
            with open(filename, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            return False

        if len(data) < 7:
            return False

        pos = 0
        if data[pos:pos+4] != self.MAGIC:
            return False
        pos += 4

        if data[pos] != self.VERSION:
            return False
        pos += 1

        self._next_id = struct.unpack_from('<I', data, pos)[0]; pos += 4
        n_episodes = struct.unpack_from('<H', data, pos)[0]; pos += 2

        # Reset store
        self.episodes = [None] * self.max_episodes
        self.count = 0

        for _ in range(min(n_episodes, self.max_episodes)):
            ep_len = struct.unpack_from('<H', data, pos)[0]; pos += 2
            ep, consumed = Episode.unpack(data, pos)
            pos += consumed

            if self.count < self.max_episodes:
                self.episodes[self.count] = ep
                self.count += 1

        return True


    # ================================================================
    #  STATS
    # ================================================================

    def stats(self) -> dict:
        """Return summary statistics about the episodic store."""
        valid = [ep for ep in self.episodes if ep is not None]
        if not valid:
            return {
                'total_episodes': 0,
                'total_events': 0,
                'consolidated': 0,
                'mean_importance': 0.0,
                'memory_bytes': 0,
                'oldest_tick': 0,
                'newest_tick': 0,
            }

        total_events = sum(ep.event_count for ep in valid)
        consolidated = sum(1 for ep in valid if ep.consolidated)
        mean_imp = sum(ep.importance for ep in valid) / len(valid)

        return {
            'total_episodes': len(valid),
            'total_events': total_events,
            'consolidated': consolidated,
            'mean_importance': round(mean_imp, 4),
            'memory_bytes': total_events * EVENT_PACK_SIZE + len(valid) * 32,
            'oldest_tick': min(ep.start_tick for ep in valid),
            'newest_tick': max(ep.end_tick for ep in valid),
        }


# ================================================================
#  CONTEXT FLAG BUILDER: Helper for Engine Integration
# ================================================================

def build_context_flags(obstacle: bool = False, voice: bool = False,
                        bonded: bool = False, bump: bool = False,
                        crystal: bool = False, immune: bool = False,
                        moving: bool = False, charging: bool = False) -> int:
    """Build context flag byte from booleans."""
    flags = 0
    if obstacle:  flags |= 0x80
    if voice:     flags |= 0x40
    if bonded:    flags |= 0x20
    if bump:      flags |= 0x10
    if crystal:   flags |= 0x08
    if immune:    flags |= 0x04
    if moving:    flags |= 0x02
    if charging:  flags |= 0x01
    return flags
