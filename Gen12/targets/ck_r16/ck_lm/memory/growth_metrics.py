"""
growth_metrics.py — CK Memory: Organism growth measurement

growth(t) = w1·compression_efficiency(t)
          + w2·retrieval_hit_rate(t)
          + w3·path_reuse_ratio(t)
          + w4·action_policy_reuse_ratio(t)
          + w5·(1 - deepseek_call_rate(t))
          + w6·log(1 + crystal_count(t)) / LOG_SCALE
          + w7·cross_modal_agreement(t)

All terms are in [0,1]. Weights sum to 1.

This is the single number that answers: "Is CK growing?"

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
from dataclasses import dataclass, field
import time
import math
import json
from pathlib import Path

METRICS_PATH = Path.home() / '.ck' / 'memory' / 'growth_metrics.json'

# Weights for growth formula (sum = 1.0)
W1_COMPRESSION   = 0.15
W2_RETRIEVAL_HIT = 0.20
W3_PATH_REUSE    = 0.15
W4_POLICY_REUSE  = 0.10
W5_DEEPSEEK_INV  = 0.20
W6_CRYSTAL_LOG   = 0.10
W7_CROSS_MODAL   = 0.10

LOG_SCALE = math.log(1 + 5000)  # normalized to 5000 crystal target


@dataclass
class GrowthSnapshot:
    """A single point-in-time growth measurement."""
    timestamp: float
    # Raw counters
    atom_count: int = 0
    path_count: int = 0
    crystal_count: int = 0
    # Rates (rolling window)
    compression_efficiency: float = 0.0   # compressed_atoms / raw_atoms
    retrieval_hit_rate: float = 0.0       # crystal hits / total queries
    path_reuse_ratio: float = 0.0         # reused paths / total paths traversed
    action_policy_reuse_ratio: float = 0.0
    deepseek_call_rate: float = 1.0       # 1.0 = always DeepSeek (bootstrap)
    cross_modal_agreement: float = 0.0    # agreement across modalities
    # Derived
    growth_score: float = 0.0
    deepseek_stage: int = 0


def compute_growth(snap: GrowthSnapshot) -> float:
    """Compute the scalar growth score from a snapshot."""
    crystal_term = math.log(1 + snap.crystal_count) / LOG_SCALE
    crystal_term = min(1.0, crystal_term)

    score = (
        W1_COMPRESSION   * snap.compression_efficiency
      + W2_RETRIEVAL_HIT * snap.retrieval_hit_rate
      + W3_PATH_REUSE    * snap.path_reuse_ratio
      + W4_POLICY_REUSE  * snap.action_policy_reuse_ratio
      + W5_DEEPSEEK_INV  * (1.0 - snap.deepseek_call_rate)
      + W6_CRYSTAL_LOG   * crystal_term
      + W7_CROSS_MODAL   * snap.cross_modal_agreement
    )
    return round(min(1.0, max(0.0, score)), 4)


class GrowthTracker:
    """Rolling growth tracker. Persists metrics to JSON."""

    def __init__(self, window: int = 100):
        self.window = window
        self._history: list[dict] = []
        self._query_count: int = 0
        self._crystal_hits: int = 0
        self._deepseek_calls: int = 0
        self._path_traversals: int = 0
        self._path_reuses: int = 0
        self._load()

    def record_query(self, crystal_hit: bool, deepseek_called: bool,
                     path_reused: bool = False) -> None:
        self._query_count += 1
        if crystal_hit:
            self._crystal_hits += 1
        if deepseek_called:
            self._deepseek_calls += 1
        self._path_traversals += 1
        if path_reused:
            self._path_reuses += 1

    def snapshot(
        self,
        atom_count: int,
        path_count: int,
        crystal_count: int,
        cross_modal_agreement: float = 0.0,
    ) -> GrowthSnapshot:
        q = max(1, self._query_count)
        t = max(1, self._path_traversals)
        snap = GrowthSnapshot(
            timestamp=time.time(),
            atom_count=atom_count,
            path_count=path_count,
            crystal_count=crystal_count,
            compression_efficiency=min(1.0, crystal_count / max(1, atom_count)),
            retrieval_hit_rate=self._crystal_hits / q,
            path_reuse_ratio=self._path_reuses / t,
            deepseek_call_rate=self._deepseek_calls / q,
            cross_modal_agreement=cross_modal_agreement,
        )
        snap.growth_score = compute_growth(snap)
        from .novelty_gate import stage_from_crystal_count
        snap.deepseek_stage = stage_from_crystal_count(crystal_count)
        self._history.append(_snap_to_dict(snap))
        if len(self._history) > self.window:
            self._history = self._history[-self.window:]
        self._save()
        return snap

    def _load(self) -> None:
        try:
            with open(METRICS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._history = data.get('history', [])
                self._query_count = data.get('query_count', 0)
                self._crystal_hits = data.get('crystal_hits', 0)
                self._deepseek_calls = data.get('deepseek_calls', 0)
                self._path_traversals = data.get('path_traversals', 0)
                self._path_reuses = data.get('path_reuses', 0)
        except Exception:
            pass

    def _save(self) -> None:
        try:
            METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(METRICS_PATH, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self._history,
                    'query_count': self._query_count,
                    'crystal_hits': self._crystal_hits,
                    'deepseek_calls': self._deepseek_calls,
                    'path_traversals': self._path_traversals,
                    'path_reuses': self._path_reuses,
                }, f, indent=2)
        except Exception:
            pass

    def latest_score(self) -> float:
        if self._history:
            return self._history[-1].get('growth_score', 0.0)
        return 0.0

    def report(self) -> str:
        q = max(1, self._query_count)
        ds_rate = self._deepseek_calls / q
        hit_rate = self._crystal_hits / q
        return (
            f"growth={self.latest_score():.3f}  "
            f"hits={hit_rate:.1%}  "
            f"deepseek={ds_rate:.1%}  "
            f"queries={self._query_count}"
        )


def _snap_to_dict(s: GrowthSnapshot) -> dict:
    return {
        'timestamp': s.timestamp,
        'atom_count': s.atom_count,
        'path_count': s.path_count,
        'crystal_count': s.crystal_count,
        'compression_efficiency': s.compression_efficiency,
        'retrieval_hit_rate': s.retrieval_hit_rate,
        'path_reuse_ratio': s.path_reuse_ratio,
        'deepseek_call_rate': s.deepseek_call_rate,
        'cross_modal_agreement': s.cross_modal_agreement,
        'growth_score': s.growth_score,
        'deepseek_stage': s.deepseek_stage,
    }
