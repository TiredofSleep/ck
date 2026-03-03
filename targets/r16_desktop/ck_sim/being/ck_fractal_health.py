# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_fractal_health.py -- Fractal Health Diagnostics
====================================================
Operator: BALANCE (5) -- equilibrium across domains.

Consumes E_out/E_in decision scores from any BTQ domain and produces
per-domain health assessments:

  - Running mean/std/trend on E_out, E_in, E_total
  - Band distribution (% GREEN / YELLOW / RED) over sliding window
  - Drift detection via linear regression slope
  - Crystal health metrics (formation rate, fuse stability)
  - System-level GREEN/YELLOW/RED flag (worst-domain rule)

Every organ of CK -- motion, language, memory, bio -- gets its own
health monitor. If any domain drifts RED, the system knows.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import deque

from ck_sim.ck_sim_heartbeat import HARMONY


# ================================================================
#  RUNNING STATISTICS (Welford's online algorithm)
# ================================================================

@dataclass
class RunningStats:
    """Efficient online mean/variance using Welford's algorithm.
    Plus linear regression slope for trend detection.
    """
    count: int = 0
    mean: float = 0.0
    _m2: float = 0.0
    min_val: float = float('inf')
    max_val: float = float('-inf')
    _window: deque = field(default_factory=lambda: deque(maxlen=200))

    def update(self, value: float):
        """Feed one value."""
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self._m2 += delta * delta2
        self.min_val = min(self.min_val, value)
        self.max_val = max(self.max_val, value)
        self._window.append(value)

    @property
    def variance(self) -> float:
        if self.count < 2:
            return 0.0
        return self._m2 / (self.count - 1)

    @property
    def std(self) -> float:
        return math.sqrt(self.variance)

    @property
    def trend_slope(self) -> float:
        """Linear regression slope over the window.
        Positive = values increasing (degrading).
        Negative = values decreasing (improving).
        """
        vals = list(self._window)
        n = len(vals)
        if n < 5:
            return 0.0

        # Simple linear regression: y = a + b*x
        sum_x = n * (n - 1) / 2.0
        sum_x2 = n * (n - 1) * (2 * n - 1) / 6.0
        sum_y = sum(vals)
        sum_xy = sum(i * v for i, v in enumerate(vals))

        denom = n * sum_x2 - sum_x * sum_x
        if abs(denom) < 1e-12:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denom
        return slope


# ================================================================
#  CRYSTAL HEALTH
# ================================================================

@dataclass
class CrystalHealth:
    """Crystal formation and stability metrics."""
    formation_count: int = 0
    harmony_fuse_count: int = 0
    total_confidence: float = 0.0
    _total_fed: int = 0

    @property
    def formation_rate(self) -> float:
        """Crystals formed per N feeds."""
        return self.formation_count / max(self._total_fed, 1)

    @property
    def fuse_stability(self) -> float:
        """Fraction of fuses that produce HARMONY."""
        return self.harmony_fuse_count / max(self.formation_count, 1)

    @property
    def avg_confidence(self) -> float:
        return self.total_confidence / max(self.formation_count, 1)

    def feed(self, fuse_result: int, confidence: float):
        self.formation_count += 1
        self._total_fed += 1
        self.total_confidence += confidence
        if fuse_result == HARMONY:
            self.harmony_fuse_count += 1


# ================================================================
#  DOMAIN HEALTH
# ================================================================

@dataclass
class DomainHealth:
    """Health report for one domain."""
    domain: str = ""
    band: str = "RED"
    e_out_stats: RunningStats = field(default_factory=RunningStats)
    e_in_stats: RunningStats = field(default_factory=RunningStats)
    e_total_stats: RunningStats = field(default_factory=RunningStats)
    band_distribution: Dict[str, float] = field(
        default_factory=lambda: {"GREEN": 0.0, "YELLOW": 0.0, "RED": 0.0})
    drift_direction: str = "stable"
    drift_magnitude: float = 0.0
    crystal_health: CrystalHealth = field(default_factory=CrystalHealth)
    decision_count: int = 0


# ================================================================
#  HEALTH MONITOR
# ================================================================

class HealthMonitor:
    """Per-domain health tracking with configurable windows."""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self._domains: Dict[str, DomainHealth] = {}
        self._band_history: Dict[str, deque] = {}

    def _ensure_domain(self, domain: str):
        if domain not in self._domains:
            self._domains[domain] = DomainHealth(domain=domain)
            self._band_history[domain] = deque(maxlen=self.window_size)

    def feed(self, domain: str, score):
        """Feed one decision score into the monitor.

        `score` is a CandidateScore (or any object with e_out, e_in, e_total, band).
        """
        self._ensure_domain(domain)
        dh = self._domains[domain]

        dh.e_out_stats.update(score.e_out)
        dh.e_in_stats.update(score.e_in)
        dh.e_total_stats.update(score.e_total)
        dh.decision_count += 1

        self._band_history[domain].append(score.band)

        # Update band distribution
        hist = self._band_history[domain]
        n = len(hist)
        if n > 0:
            dh.band_distribution = {
                "GREEN": sum(1 for b in hist if b == "GREEN") / n,
                "YELLOW": sum(1 for b in hist if b == "YELLOW") / n,
                "RED": sum(1 for b in hist if b == "RED") / n,
            }

        # Update drift
        direction, magnitude = self.detect_drift(domain)
        dh.drift_direction = direction
        dh.drift_magnitude = magnitude

        # Update overall band
        dh.band = self._classify_domain_band(domain)

    def feed_crystal(self, domain: str, fuse_result: int, confidence: float):
        """Feed crystal formation event."""
        self._ensure_domain(domain)
        self._domains[domain].crystal_health.feed(fuse_result, confidence)

    def detect_drift(self, domain: str) -> Tuple[str, float]:
        """Detect if E_total is trending up (degrading) or down (improving).

        Returns (direction, slope).
        """
        self._ensure_domain(domain)
        slope = self._domains[domain].e_total_stats.trend_slope

        if abs(slope) < 0.001:
            return "stable", slope
        elif slope > 0:
            return "degrading", slope
        else:
            return "improving", slope

    def _classify_domain_band(self, domain: str) -> str:
        """Classify domain health based on recent band distribution."""
        dh = self._domains[domain]
        dist = dh.band_distribution

        if dist["GREEN"] >= 0.6:
            return "GREEN"
        elif dist["RED"] >= 0.4:
            return "RED"
        else:
            return "YELLOW"

    def get_health(self, domain: str) -> DomainHealth:
        """Get current health assessment for a domain."""
        self._ensure_domain(domain)
        return self._domains[domain]

    def get_system_health(self) -> Dict[str, DomainHealth]:
        """Get health for all domains."""
        return dict(self._domains)

    def classify_system_band(self) -> str:
        """Overall system health: worst-domain rule.

        If ANY domain is RED, system is RED.
        If all GREEN, system is GREEN. Otherwise YELLOW.
        """
        if not self._domains:
            return "RED"

        bands = [dh.band for dh in self._domains.values()]

        if any(b == "RED" for b in bands):
            return "RED"
        if all(b == "GREEN" for b in bands):
            return "GREEN"
        return "YELLOW"

    def summary(self) -> str:
        """One-line system health summary."""
        sys_band = self.classify_system_band()
        parts = [f"SYSTEM: {sys_band}"]
        for name, dh in self._domains.items():
            parts.append(
                f"  {name}: {dh.band} "
                f"(E_total={dh.e_total_stats.mean:.3f} "
                f"drift={dh.drift_direction} "
                f"decisions={dh.decision_count})"
            )
        return "\n".join(parts)
