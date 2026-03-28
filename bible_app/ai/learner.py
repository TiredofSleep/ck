"""
Learner — A lightweight neural net that learns from conversations.

Learns:
  - Which operator patterns → which verses actually help people
  - Which intents get engaged with (user responds positively)
  - Which corridor transitions happen (COL → BRT = someone felt better)

Uses a simple feedforward net trained on conversation pairs.
Stores weights to disk so learning persists across sessions.

No external dependencies — pure numpy-style math with Python stdlib.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import math
import os
import random
import time
from collections import defaultdict

from bible_app.algebra import NUM_OPS, OP_NAMES, HARMONY, T_STAR, coherence


# ── Paths ─────────────────────────────────────────────────────────
LEARN_DIR = os.path.expanduser('~/.ck/bible_learner')


class VerseLearner:
    """Learns which verses resonate with which operator patterns.

    Architecture: 10-input (operator distribution) → 20 hidden → 10 output
    (operator preference for next verse selection).

    Also maintains a "resonance memory" — which verses got positive engagement
    (user continued talking, corridor improved, coherence increased).
    """

    def __init__(self, save_dir=None):
        self._save_dir = save_dir or LEARN_DIR
        self._lr = 0.01  # Learning rate

        # Simple feedforward net: 10 → 20 → 10
        # Weights as nested lists (no numpy dependency)
        self._w1 = [[random.gauss(0, 0.3) for _ in range(NUM_OPS)]
                     for _ in range(20)]
        self._b1 = [0.0] * 20
        self._w2 = [[random.gauss(0, 0.3) for _ in range(20)]
                     for _ in range(NUM_OPS)]
        self._b2 = [0.0] * NUM_OPS

        # Resonance memory: {verse_ref: {score, count, last_corridor}}
        self._verse_scores = {}

        # Conversation memory: recent (input_ops, response_corridor, engagement)
        self._conversation_log = []

        # Stats
        self._total_learns = 0
        self._loaded = False

        self._load()

    def _sigmoid(self, x):
        if x > 500:
            return 1.0
        if x < -500:
            return 0.0
        return 1.0 / (1.0 + math.exp(-x))

    def _forward(self, input_dist):
        """Forward pass: operator distribution → verse operator preference."""
        # Hidden layer
        hidden = []
        for j in range(20):
            s = self._b1[j]
            for i in range(NUM_OPS):
                s += self._w1[j][i] * input_dist[i]
            hidden.append(self._sigmoid(s))

        # Output layer
        output = []
        for k in range(NUM_OPS):
            s = self._b2[k]
            for j in range(20):
                s += self._w2[k][j] * hidden[j]
            output.append(self._sigmoid(s))

        return output, hidden

    def predict_verse_ops(self, user_ops):
        """Predict which operator-type verses will resonate best.

        Returns a 10-element preference vector (higher = better match).
        """
        # Build operator distribution from user input
        dist = [0.0] * NUM_OPS
        for o in user_ops:
            dist[o % NUM_OPS] += 1.0
        total = sum(dist)
        if total > 0:
            dist = [d / total for d in dist]

        output, _ = self._forward(dist)
        return output

    def learn_from_conversation(self, user_ops, verse_ref, corridor_before,
                                 corridor_after, user_responded):
        """Learn from a conversation turn.

        Positive signal if:
          - User responded (continued engaging)
          - Corridor improved (moved toward PRE_LEAK/BRT from COL/CTR)
          - Coherence increased
        """
        corridor_rank = {
            'PRE_LEAK': 0, 'BRT': 1, 'CHA': 2,
            'BAL': 3, 'COL': 4, 'CTR': 5,
        }
        rank_before = corridor_rank.get(corridor_before, 3)
        rank_after = corridor_rank.get(corridor_after, 3)

        # Positive engagement signal
        engagement = 0.0
        if user_responded:
            engagement += 0.5
        if rank_after < rank_before:
            engagement += 0.5  # Corridor improved!
        elif rank_after > rank_before:
            engagement -= 0.3  # Got worse

        # Update verse score
        if verse_ref:
            if verse_ref not in self._verse_scores:
                self._verse_scores[verse_ref] = {
                    'score': 0.5, 'count': 0, 'corridors': [],
                }
            vs = self._verse_scores[verse_ref]
            vs['count'] += 1
            # Exponential moving average
            vs['score'] = 0.9 * vs['score'] + 0.1 * max(0.0, min(1.0, 0.5 + engagement))
            vs['corridors'].append(corridor_before)
            if len(vs['corridors']) > 20:
                vs['corridors'] = vs['corridors'][-20:]

        # Backprop-lite: adjust weights toward positive outcomes
        if abs(engagement) > 0.1:
            self._adjust_weights(user_ops, engagement)

        self._total_learns += 1

        # Auto-save every 20 learns
        if self._total_learns % 20 == 0:
            self._save()

    def _adjust_weights(self, user_ops, target_signal):
        """Simple gradient step: push output toward matching operators
        when engagement is positive, away when negative."""
        dist = [0.0] * NUM_OPS
        for o in user_ops:
            dist[o % NUM_OPS] += 1.0
        total = sum(dist)
        if total > 0:
            dist = [d / total for d in dist]

        output, hidden = self._forward(dist)

        # Target: if positive engagement, push output toward user's op distribution
        # If negative, push away
        for k in range(NUM_OPS):
            error = target_signal * (dist[k] - output[k])
            self._b2[k] += self._lr * error
            for j in range(20):
                self._w2[k][j] += self._lr * error * hidden[j]

    def get_verse_boost(self, verse_ref):
        """Get learned score boost for a verse (0.0 to 1.0).

        Higher = this verse has historically helped people.
        """
        vs = self._verse_scores.get(verse_ref)
        if vs is None or vs['count'] < 2:
            return 0.0  # Not enough data
        return vs['score'] - 0.5  # Center around 0

    def stats(self):
        return {
            'total_learns': self._total_learns,
            'verses_scored': len(self._verse_scores),
            'top_verses': sorted(
                [(ref, d['score'], d['count'])
                 for ref, d in self._verse_scores.items()
                 if d['count'] >= 3],
                key=lambda x: x[1], reverse=True
            )[:10],
        }

    def _save(self):
        os.makedirs(self._save_dir, exist_ok=True)
        data = {
            'w1': self._w1, 'b1': self._b1,
            'w2': self._w2, 'b2': self._b2,
            'verse_scores': self._verse_scores,
            'total_learns': self._total_learns,
            'saved_at': time.time(),
        }
        path = os.path.join(self._save_dir, 'weights.json')
        with open(path, 'w') as f:
            json.dump(data, f)

    def _load(self):
        path = os.path.join(self._save_dir, 'weights.json')
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            self._w1 = data['w1']
            self._b1 = data['b1']
            self._w2 = data['w2']
            self._b2 = data['b2']
            self._verse_scores = data.get('verse_scores', {})
            self._total_learns = data.get('total_learns', 0)
            self._loaded = True
        except Exception:
            pass  # Corrupted file, start fresh
