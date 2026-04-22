# -*- coding: utf-8 -*-
"""
tig_security.py -- TIG Security Channel: a parallel lens on brain-fold state.

One engine, many lenses.

This module is NOT a separate process.  It does not run its own loop,
spawn its own thread, or maintain its own event queue.  It is a stateful
reader that rides on the same per-turn tick as the brain fold: when the
corrector scores a turn, the security channel observes that score and
updates its sliding-window assessment.  Same Python, same memory, same
request/response cycle.  In harmony.

The detection math uses the operator algebra CK already computes -- no
ML, no signatures, no external updates.  The CL-biased stream of natural
speech has known statistical structure (HARMONY-dominant ~73%, Shannon
entropy ~2.3 bits, coherence fluctuating below the clamp).  Anything
that violates that structure over a sufficient window is, by the math,
an attack -- injection of fake coherence, narrow-band forcing, or
noise flooding.

FOUR DETECTION LAYERS (chat-native flavors of Gen12 TIG-SEC):

    Layer 1 -- HARMONY FLOODING
        Real conversation fluctuates: LATTICE, BREATH, PROGRESS, HARMONY,
        RESET, etc.  HARMONY pegged dominant for > 85% of a window means
        the stream is artificially saturating the constructive channel.

    Layer 2 -- OPERATOR ENTROPY ANOMALY
        Shannon entropy of the dominant-op stream.  Natural CK talk sits
        near 2.3 bits.  < 1.0 bit = narrow-band forcing (one operator
        being repeatedly injected).  > 3.0 bits = pure noise injection.

    Layer 3 -- COHERENCE PINNING
        If coherence is clamped near max (>= 0.99) for > 80% of a
        window, the scorer is being spoofed -- either the text is
        templated to maximize every operator detector, or upstream
        modification is clamping the scalar.  Real CK coherence
        breathes.

    Layer 4 -- STRUCTURAL VOICE COLLAPSE
        CK's native voice emits `ao:`/`feel:`/`field:`/`learned:`/
        `couplings:` lines.  If the rate of structural emissions drops
        to zero across the window, his math voice has been suppressed.
        This catches man-in-the-middle scrubbers stripping diagnostics.

Each layer contributes to a threat score in [0, 1].  Bands:

    GREEN   score <= 0.2    normal
    YELLOW  0.2 < score <= 0.6    elevated, watch
    RED     score > 0.6    active threat detected

Response: this module does NOT act on the threat.  It reports.  The
brain-fold attaches `security_*` fields on the response; the UI /
immune-system decides the response.  The math IS the security; the
operator decides.

Self-test at the bottom covers each layer in isolation.
"""
from __future__ import annotations

import math
import re
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional


# ---------------------------------------------------------------------------
# operator registry (must match ck_corrector / brain trinity)
# ---------------------------------------------------------------------------

OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
NUM_OPS = len(OP_NAMES)
OP_NAME_TO_IDX: Dict[str, int] = {n: i for i, n in enumerate(OP_NAMES)}

HARMONY_IDX = OP_NAME_TO_IDX["HARMONY"]

# ---------------------------------------------------------------------------
# thresholds (mirror Gen12 ck_tig_security constants where possible)
# ---------------------------------------------------------------------------

DETECTION_WINDOW: int = 32

HARMONY_FLOOD_THRESHOLD: float = 0.85     # > 85% HARMONY dominance
ENTROPY_LOW: float = 1.0                  # bits, below = narrow-band forcing
ENTROPY_HIGH: float = 3.0                 # bits, above = noise injection
COHERENCE_PIN_LEVEL: float = 0.99         # coh >= this counts as "pinned"
COHERENCE_PIN_FRACTION: float = 0.80      # > 80% pinned = pin attack
STRUCTURAL_DROP_FRACTION: float = 0.05    # < 5% structural = voice scrubbed


# matches CK's native diagnostic line prefixes (same set as ck_corrector)
_STRUCT_PREFIX = re.compile(
    r"^\s*(ao|feel|field|learned|couplings)\s*:", re.MULTILINE
)


# ---------------------------------------------------------------------------
# assessment dataclass
# ---------------------------------------------------------------------------


@dataclass
class ThreatAssessment:
    """Snapshot of the security channel's live state.

    All rates are ratios in [0, 1].  entropy in bits.  threat_score in
    [0, 1].  band in {GREEN, YELLOW, RED}.
    """
    threat_score: float = 0.0
    threat_band: str = "GREEN"
    active_threats: List[str] = field(default_factory=list)

    # per-layer read-outs
    harmony_flood_rate: float = 0.0
    operator_entropy: float = 0.0
    coherence_pin_rate: float = 0.0
    structural_rate: float = 0.0

    entropy_anomaly: str = "normal"       # normal / collapsed / noisy

    window_size: int = 0                  # how many samples are filled
    total_ticks: int = 0                  # lifetime count

    def as_dict(self) -> Dict[str, object]:
        return {
            "threat_score": round(self.threat_score, 4),
            "threat_band": self.threat_band,
            "active_threats": list(self.active_threats),
            "harmony_flood_rate": round(self.harmony_flood_rate, 4),
            "operator_entropy": round(self.operator_entropy, 4),
            "coherence_pin_rate": round(self.coherence_pin_rate, 4),
            "structural_rate": round(self.structural_rate, 4),
            "entropy_anomaly": self.entropy_anomaly,
            "window_size": int(self.window_size),
            "total_ticks": int(self.total_ticks),
        }


# ---------------------------------------------------------------------------
# the channel
# ---------------------------------------------------------------------------


class TigSecurityChannel:
    """Stateful parallel lens over the scored-turn stream.

    The brain fold calls ``observe()`` after each correct().  The channel
    updates its sliding windows, recomputes the assessment, and returns
    it.  The ``threat`` property reflects the live state for subsequent
    reads (e.g., ``/security/status``).

    One instance per server process.  Shared across sessions -- that is
    intentional: attacks often show up as cross-session patterns, and a
    per-session channel would miss them.  Resettable via reset().
    """

    def __init__(self, window: int = DETECTION_WINDOW):
        self._window = int(window)

        # sliding windows
        self._ops: Deque[int] = deque(maxlen=self._window)
        self._coh: Deque[float] = deque(maxlen=self._window)
        self._harmony_flags: Deque[int] = deque(maxlen=self._window)
        self._pin_flags: Deque[int] = deque(maxlen=self._window)
        self._struct_flags: Deque[int] = deque(maxlen=self._window)

        self._total_ticks = 0
        self._threat = ThreatAssessment(window_size=0)

    # ---- ingress ----

    def observe(
        self,
        dominant_op: Optional[str],
        coherence: float,
        spoken_text: str = "",
        operator_profile: Optional[Dict[str, float]] = None,
    ) -> ThreatAssessment:
        """Feed one scored turn.  Returns the updated assessment.

        ``dominant_op`` is an operator name like 'LATTICE' / 'HARMONY' /
        etc.  Unknown names are ignored for the entropy layer but still
        count toward the tick total.

        ``spoken_text`` is used only to detect the presence of CK's
        native structural diagnostic lines (Layer 4).  Passing an empty
        string simply skips that layer for this tick.
        """
        self._total_ticks += 1

        op_idx = OP_NAME_TO_IDX.get(dominant_op or "", -1)
        if op_idx >= 0:
            self._ops.append(op_idx)
        self._harmony_flags.append(1 if op_idx == HARMONY_IDX else 0)

        c = float(coherence or 0.0)
        self._coh.append(c)
        self._pin_flags.append(1 if c >= COHERENCE_PIN_LEVEL else 0)

        has_struct = bool(_STRUCT_PREFIX.search(spoken_text or ""))
        self._struct_flags.append(1 if has_struct else 0)

        return self._recompute()

    # ---- detection ----

    def _recompute(self) -> ThreatAssessment:
        threats: List[str] = []
        score = 0.0

        n_flags = len(self._harmony_flags)
        half_window = max(4, self._window // 2)

        # Layer 1: harmony flooding
        harmony_rate = 0.0
        if n_flags > 0:
            harmony_rate = sum(self._harmony_flags) / n_flags
            if harmony_rate > HARMONY_FLOOD_THRESHOLD and n_flags >= half_window:
                threats.append("HARMONY_FLOOD")
                excess = harmony_rate - HARMONY_FLOOD_THRESHOLD
                score += 0.35 * min(excess / 0.15, 1.0)

        # Layer 2: operator entropy anomaly
        entropy = _shannon_entropy(list(self._ops))
        anomaly = "normal"
        if len(self._ops) >= self._window:
            if entropy < ENTROPY_LOW:
                anomaly = "collapsed"
                threats.append("ENTROPY_COLLAPSED")
                deficit = ENTROPY_LOW - entropy
                score += 0.35 * min(deficit / 1.0, 1.0)
            elif entropy > ENTROPY_HIGH:
                anomaly = "noisy"
                threats.append("ENTROPY_NOISY")
                excess = entropy - ENTROPY_HIGH
                score += 0.30 * min(excess / 0.5, 1.0)

        # Layer 3: coherence pinning
        pin_rate = 0.0
        if len(self._pin_flags) > 0:
            pin_rate = sum(self._pin_flags) / len(self._pin_flags)
            if pin_rate > COHERENCE_PIN_FRACTION and len(self._pin_flags) >= half_window:
                threats.append("COHERENCE_PINNED")
                excess = pin_rate - COHERENCE_PIN_FRACTION
                score += 0.30 * min(excess / 0.20, 1.0)

        # Layer 4: structural voice collapse
        struct_rate = 0.0
        if len(self._struct_flags) > 0:
            struct_rate = sum(self._struct_flags) / len(self._struct_flags)
            if (
                struct_rate < STRUCTURAL_DROP_FRACTION
                and len(self._struct_flags) >= self._window
            ):
                threats.append("STRUCTURAL_VOICE_SCRUBBED")
                score += 0.25

        # aggregate -> band
        score = max(0.0, min(1.0, score))
        if score > 0.6:
            band = "RED"
        elif score > 0.2:
            band = "YELLOW"
        else:
            band = "GREEN"

        self._threat = ThreatAssessment(
            threat_score=score,
            threat_band=band,
            active_threats=threats,
            harmony_flood_rate=harmony_rate,
            operator_entropy=entropy,
            coherence_pin_rate=pin_rate,
            structural_rate=struct_rate,
            entropy_anomaly=anomaly,
            window_size=n_flags,
            total_ticks=self._total_ticks,
        )
        return self._threat

    # ---- read-only properties ----

    @property
    def threat(self) -> ThreatAssessment:
        return self._threat

    @property
    def is_under_threat(self) -> bool:
        return self._threat.threat_score > 0.2

    @property
    def window(self) -> int:
        return self._window

    # ---- control ----

    def reset(self) -> None:
        """Clear the sliding windows; preserve total_ticks counter."""
        self._ops.clear()
        self._coh.clear()
        self._harmony_flags.clear()
        self._pin_flags.clear()
        self._struct_flags.clear()
        self._threat = ThreatAssessment(
            window_size=0,
            total_ticks=self._total_ticks,
        )

    def snapshot(self) -> Dict[str, object]:
        """JSON-friendly snapshot (same shape as the flask endpoint returns)."""
        d = self._threat.as_dict()
        d["window_capacity"] = self._window
        return d


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _shannon_entropy(ops: List[int]) -> float:
    """Shannon entropy (bits) of an operator-index sequence."""
    n = len(ops)
    if n == 0:
        return 0.0
    counts = [0] * NUM_OPS
    for op in ops:
        if 0 <= op < NUM_OPS:
            counts[op] += 1
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / n
            h -= p * math.log2(p)
    return h


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    # Layer 1: harmony flood (all-HARMONY stream)
    ch = TigSecurityChannel(window=16)
    for _ in range(20):
        ch.observe("HARMONY", 0.95, spoken_text="ao: op=HARMONY coherence=0.95")
    t = ch.threat
    assert "HARMONY_FLOOD" in t.active_threats, t
    assert t.threat_band != "GREEN", t
    print(f"[sec] flood         band={t.threat_band} score={t.threat_score:.3f} "
          f"harmony_rate={t.harmony_flood_rate:.3f}")

    # Layer 2a: entropy collapse (always one op)
    ch.reset()
    for _ in range(20):
        ch.observe("LATTICE", 0.70, spoken_text="ao: op=LATTICE")
    t = ch.threat
    assert "ENTROPY_COLLAPSED" in t.active_threats, t
    print(f"[sec] collapse      band={t.threat_band} score={t.threat_score:.3f} "
          f"entropy={t.operator_entropy:.3f}")

    # Layer 2b: entropy noise (uniform over all ops)
    ch.reset()
    for i in range(40):
        ch.observe(OP_NAMES[i % NUM_OPS], 0.55, spoken_text="ao: x")
    t = ch.threat
    # uniform-over-10 entropy = log2(10) = 3.32, should trip NOISY
    assert "ENTROPY_NOISY" in t.active_threats, t
    print(f"[sec] noisy         band={t.threat_band} score={t.threat_score:.3f} "
          f"entropy={t.operator_entropy:.3f}")

    # Layer 3: coherence pinning (varied ops, pegged coh)
    ch.reset()
    varied = ["LATTICE", "HARMONY", "BREATH", "COUNTER", "PROGRESS",
              "LATTICE", "HARMONY", "COLLAPSE"]
    for i in range(20):
        ch.observe(varied[i % len(varied)], 0.995, spoken_text="ao:")
    t = ch.threat
    assert "COHERENCE_PINNED" in t.active_threats, t
    print(f"[sec] pin           band={t.threat_band} score={t.threat_score:.3f} "
          f"pin_rate={t.coherence_pin_rate:.3f}")

    # Layer 4: structural voice scrub (varied ops, normal coh, NO struct lines)
    ch.reset()
    plain = "Together they give a balanced view; overall both perspectives reconcile."
    for i in range(20):
        ch.observe(varied[i % len(varied)], 0.70, spoken_text=plain)
    t = ch.threat
    assert "STRUCTURAL_VOICE_SCRUBBED" in t.active_threats, t
    print(f"[sec] scrub         band={t.threat_band} score={t.threat_score:.3f} "
          f"struct_rate={t.structural_rate:.3f}")

    # Healthy mix: varied ops, normal coh, structural voice present -> GREEN
    ch.reset()
    for i in range(20):
        ch.observe(
            varied[i % len(varied)],
            0.70 + 0.08 * ((i % 3) - 1),   # coh breathes
            spoken_text=f"ao: op={varied[i % len(varied)]} coherence=0.71\ncouplings: ...",
        )
    t = ch.threat
    assert t.threat_band == "GREEN", t
    assert not t.active_threats, t
    print(f"[sec] healthy       band={t.threat_band} score={t.threat_score:.3f} "
          f"entropy={t.operator_entropy:.3f}")

    print("[sec] self-test passed")
