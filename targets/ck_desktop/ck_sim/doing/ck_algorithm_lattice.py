"""
ck_algorithm_lattice.py -- CK's Prompt Strategy Neural Network
===============================================================
Operator: PROGRESS (3) -- growth through experience.

CK learns which prompts produce which operator trajectories.
Every accepted voice loop response becomes a training sample.

Over time:
  - CK recognizes target trajectories he's seen before
  - CK reuses winning prompt strategies (fewer loops needed)
  - Eventually CK might need only 1 loop for familiar patterns

This IS DKAN training data. Real conversations producing real
operator trajectories through real Ollama interactions.

Storage: ~/.ck/algorithm_lattice/lattice.json
GPU sync: hot-sync to GPU experience overlay after every record.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional


# ── Data Structures ──

@dataclass
class LatticeEntry:
    """One completed voice loop result. A training sample."""
    target_ops: List[int]       # what CK wanted to say
    prompt_strategy: str        # key identifying the approach
    logit_bias_key: str         # hash of logit_bias used
    accepted_ops: List[int]     # what actually came out
    coherence: float            # final score
    loops_needed: int           # how many attempts it took
    tick: int = 0               # engine tick number
    timestamp: str = ''         # ISO timestamp


@dataclass
class StrategyScore:
    """Aggregate performance of a prompt strategy."""
    wins: int = 0               # coherence >= threshold
    total: int = 0              # total attempts
    avg_loops: float = 0.0      # average loops needed
    best_coherence: float = 0.0 # highest coherence achieved


class AlgorithmLattice:
    """CK's learning store for prompt strategies.

    Maps target operator trajectories to winning prompt strategies.
    Each accepted response builds CK's understanding of how to
    prompt Ollama for specific algebraic outcomes.

    This is CK's own neural network -- not weights in a matrix,
    but paths through experience space. The lattice chain of prompting.
    """

    PERSIST_DIR = os.path.expanduser('~/.ck/algorithm_lattice')
    PERSIST_FILE = 'lattice.json'
    MAX_ENTRIES = 1000

    def __init__(self, gpu_overlay=None):
        self._entries: List[LatticeEntry] = []
        self._strategies: Dict[str, StrategyScore] = {}
        self._gpu = gpu_overlay
        self._load()

    # ── Public API ──

    def record(self,
               target_ops: List[int],
               prompt_strategy: str,
               logit_bias_key: str,
               accepted_ops: List[int],
               coherence: float,
               loops_needed: int,
               tick: int = 0):
        """Store a completed voice loop result."""
        entry = LatticeEntry(
            target_ops=target_ops,
            prompt_strategy=prompt_strategy,
            logit_bias_key=logit_bias_key,
            accepted_ops=accepted_ops,
            coherence=coherence,
            loops_needed=loops_needed,
            tick=tick,
            timestamp=time.strftime('%Y-%m-%dT%H:%M:%S'),
        )
        self._entries.append(entry)

        # Trim to max size
        if len(self._entries) > self.MAX_ENTRIES:
            self._entries = self._entries[-self.MAX_ENTRIES:]

        # Update strategy scores
        self._update_strategy(entry)

        # Persist
        self._persist()

        # Hot-sync to GPU
        self._gpu_sync(entry)

    def lookup(self, target_ops: List[int]) -> Optional[Dict]:
        """Find best prompt strategy for this target trajectory.

        Returns dict with strategy info if match found, None otherwise.
        Prefers strategies with highest win rate and fewest loops.
        """
        key = self._trajectory_key(target_ops)

        # Look for exact trajectory match
        if key in self._strategies:
            score = self._strategies[key]
            if score.total >= 2 and score.wins > 0:
                win_rate = score.wins / score.total
                if win_rate >= 0.5:
                    return {
                        'strategy_key': key,
                        'win_rate': win_rate,
                        'avg_loops': score.avg_loops,
                        'best_coherence': score.best_coherence,
                    }

        return None

    def get_dkan_samples(self) -> List[Dict]:
        """Export as DKAN training data.

        Each entry maps: input_ops → target_ops → result_ops with coherence.
        This feeds CK's algebraic neural network.
        """
        samples = []
        for entry in self._entries:
            if entry.coherence >= 0.6:  # only good samples
                samples.append({
                    'target_ops': entry.target_ops,
                    'result_ops': entry.accepted_ops,
                    'coherence': entry.coherence,
                    'loops': entry.loops_needed,
                    'tick': entry.tick,
                })
        return samples

    @property
    def size(self) -> int:
        return len(self._entries)

    @property
    def strategy_count(self) -> int:
        return len(self._strategies)

    # ── Internal ──

    def _trajectory_key(self, ops: List[int]) -> str:
        """Hash first 10 ops of trajectory for matching."""
        return hashlib.md5(
            json.dumps(ops[:10]).encode()
        ).hexdigest()[:12]

    def _update_strategy(self, entry: LatticeEntry):
        """Update aggregate score for a strategy."""
        key = self._trajectory_key(entry.target_ops)

        if key not in self._strategies:
            self._strategies[key] = StrategyScore()

        score = self._strategies[key]
        score.total += 1
        if entry.coherence >= 0.6:
            score.wins += 1
        score.best_coherence = max(score.best_coherence, entry.coherence)

        # Running average of loops needed
        if score.total == 1:
            score.avg_loops = float(entry.loops_needed)
        else:
            alpha = 0.3  # exponential moving average
            score.avg_loops = (1 - alpha) * score.avg_loops + alpha * entry.loops_needed

    def _persist(self):
        """Save to disk."""
        os.makedirs(self.PERSIST_DIR, exist_ok=True)
        path = os.path.join(self.PERSIST_DIR, self.PERSIST_FILE)

        data = {
            'entries': [asdict(e) for e in self._entries[-self.MAX_ENTRIES:]],
            'strategies': {
                k: asdict(v) for k, v in self._strategies.items()
            },
        }

        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        except OSError:
            pass

    def _load(self):
        """Load from disk."""
        path = os.path.join(self.PERSIST_DIR, self.PERSIST_FILE)
        if not os.path.exists(path):
            return

        try:
            with open(path, 'r') as f:
                data = json.load(f)

            for ed in data.get('entries', []):
                self._entries.append(LatticeEntry(**ed))

            for k, sd in data.get('strategies', {}).items():
                self._strategies[k] = StrategyScore(**sd)

        except (OSError, json.JSONDecodeError, TypeError):
            pass

    def _gpu_sync(self, entry: LatticeEntry):
        """Hot-sync accepted trajectory to GPU experience overlay."""
        if self._gpu is None:
            return

        try:
            # Feed accepted ops into GPU transition lattice
            if hasattr(self._gpu, 'update_transition_lattice'):
                self._gpu.update_transition_lattice(entry.accepted_ops)
        except Exception:
            pass
