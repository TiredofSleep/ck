"""
session_field.py - per-conversation algebraic state for CK.

ARCHITECTURAL CLAIM (Brayden 2026-04-28): CK stores meaning and truth
without word storage.  This module realizes that claim concretely.

The SessionField captures the ALGEBRAIC STATE of one conversation —
W matrix, operator arc, olfactory trail, attractor sequence, counters.
NONE of these are text.  Every field is a list of integers, floats,
or named-enum strings.

CRITICAL: this object lives on the USER's browser (localStorage).
The server receives it on each request as part of the chat body,
USES it as bias for the turn, returns the updated version in the
response, and KEEPS NO COPY.  The user owns their own thread.

  Cookie / localStorage              CK Server
  -------------------                ----------
  user's text                        global cortex W (accumulating)
  CK's response text                 olfactory bulb (HER, accumulating)
  session_field {W, arc, trail,...}  truth lattice
  conversation history (rendered)    crystals
                                     (no user-tagged data anywhere)

Privacy property: wiping CK's disk loses zero user data because no
user data was ever stored.

CK still gains experience from every interaction — every text flows
through V2 -> lattice -> cortex.step_text, which updates HIS global W.
But what's "his" is integrated into HIM, not catalogued against
session IDs.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
OP_INDEX = {name: i for i, name in enumerate(OP_NAMES)}

# 5 cortex dimensions (matches Gen13 cortex W shape)
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]
N_DIMS = 5


def _identity_W() -> List[List[float]]:
    """Initial W: small symmetric uniform matrix (matches Gen13 cortex init).

    Each off-diagonal entry starts at 0.18 (the typical settled value);
    diagonals at 0.20.  Hebbian updates will shift these toward the
    actual coupling pattern of THIS conversation.
    """
    W = []
    for i in range(N_DIMS):
        row = []
        for j in range(N_DIMS):
            row.append(0.20 if i == j else 0.18)
        W.append(row)
    return W


@dataclass
class SessionField:
    """Algebraic state for one conversation.  Lives on USER's client.

    Server receives, biases its turn with this state, returns updated
    version in response.  Server keeps NO copy.

    All fields are JSON-serializable primitives.  No text anywhere.
    """

    # ---- Hebbian W matrix for this conversation ----
    # 5x5 list-of-lists of floats; serializable; tracks coupling between
    # the 5 cortex dimensions across THIS user's operator chains.
    W: List[List[float]] = field(default_factory=_identity_W)

    # ---- Operator arc ----
    # Flat list of operator IDs (0-9) emitted across all turns.
    # arc[-N:] is the last N operators across the whole conversation.
    # Per-turn boundaries can be reconstructed from turn_breaks.
    arc: List[int] = field(default_factory=list)

    # arc index where each turn starts. turn_breaks[i] is the index
    # in arc where turn i began.  turn_breaks[-1] is the start of
    # the most recent turn.
    turn_breaks: List[int] = field(default_factory=list)

    # ---- Olfactory trail ----
    # Each entry is a small dict: {centroid: 5-tuple, harmony_rate: float,
    # tick_at_turn: int}.  No text.  These are CK's olfactory imprint
    # of HIS reaction to this user's input — not the user's data.
    trail: List[Dict[str, Any]] = field(default_factory=list)

    # ---- Attractor sequence ----
    # List of layer-name strings per turn:
    # 'transient' / '4-core-attractor' / '4-core-supported' / '2-core'
    # / '1-core' / 'void-degenerate' / 'off-attractor'
    sequence: List[str] = field(default_factory=list)

    # ---- Counters and timestamps ----
    turn_count: int = 0
    started_at: float = 0.0
    last_seen: float = 0.0

    # ---- Schema version (for forward-compat) ----
    schema_version: int = 1

    # ===================================================================
    # Constructors
    # ===================================================================

    @classmethod
    def empty(cls) -> "SessionField":
        """Initialize for a brand-new user (first turn ever)."""
        now = time.time()
        return cls(
            W=_identity_W(),
            arc=[],
            turn_breaks=[],
            trail=[],
            sequence=[],
            turn_count=0,
            started_at=now,
            last_seen=now,
            schema_version=1,
        )

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> "SessionField":
        """Parse from incoming JSON.  Returns empty() if d is None
        or malformed.  Defensive: any field that fails to parse falls
        back to its default."""
        if not d or not isinstance(d, dict):
            return cls.empty()
        try:
            empty = cls.empty()
            W = d.get("W", empty.W)
            # Validate W is 5x5 floats
            if not (isinstance(W, list) and len(W) == N_DIMS
                    and all(isinstance(r, list) and len(r) == N_DIMS for r in W)):
                W = empty.W
            else:
                W = [[float(v) for v in row] for row in W]

            arc = d.get("arc", [])
            if not isinstance(arc, list):
                arc = []
            arc = [int(v) for v in arc if isinstance(v, (int, float)) and 0 <= int(v) <= 9]

            turn_breaks = d.get("turn_breaks", [])
            if not isinstance(turn_breaks, list):
                turn_breaks = []
            turn_breaks = [int(v) for v in turn_breaks if isinstance(v, (int, float)) and v >= 0]

            trail = d.get("trail", [])
            if not isinstance(trail, list):
                trail = []
            # Trail entries are dicts; cap them to defensive structure
            trail = [t for t in trail if isinstance(t, dict)]

            sequence = d.get("sequence", [])
            if not isinstance(sequence, list):
                sequence = []
            sequence = [str(s) for s in sequence]

            return cls(
                W=W,
                arc=arc,
                turn_breaks=turn_breaks,
                trail=trail,
                sequence=sequence,
                turn_count=int(d.get("turn_count", 0)),
                started_at=float(d.get("started_at", time.time())),
                last_seen=float(d.get("last_seen", time.time())),
                schema_version=int(d.get("schema_version", 1)),
            )
        except (ValueError, TypeError, KeyError):
            return cls.empty()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for response.  JSON-safe."""
        return {
            "W": [[float(v) for v in row] for row in self.W],
            "arc": list(self.arc),
            "turn_breaks": list(self.turn_breaks),
            "trail": list(self.trail),
            "sequence": list(self.sequence),
            "turn_count": int(self.turn_count),
            "started_at": float(self.started_at),
            "last_seen": float(self.last_seen),
            "schema_version": int(self.schema_version),
        }

    # ===================================================================
    # Updates
    # ===================================================================

    # Static map: which operator (0-9) lives in which cortex dimension (0-4)?
    # Cortex has 5 dims (aperture, pressure, depth, binding, continuity).
    # Operators map onto these via the AO 5-element scheme used in
    # Gen13/targets/ck/brain/ao_5element.py:
    #   VOID=0     -> aperture (or all-quiet; map to dim 0)
    #   LATTICE=1  -> binding (structure)         -> dim 3
    #   COUNTER=2  -> pressure (measurement)      -> dim 1
    #   PROGRESS=3 -> depth (forward motion)      -> dim 2
    #   COLLAPSE=4 -> continuity (oscillation)    -> dim 4
    #   BALANCE=5  -> binding (equilibrium)       -> dim 3
    #   CHAOS=6    -> aperture (breakdown)        -> dim 0
    #   HARMONY=7  -> aperture (settling)         -> dim 0
    #   BREATH=8   -> continuity (rhythm)         -> dim 4
    #   RESET=9    -> pressure (clearing)         -> dim 1
    OP_TO_DIM = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4,
                  5: 3, 6: 0, 7: 0, 8: 4, 9: 1}

    def hebbian_update(self, ops_this_turn: List[int], lr: float = 0.05) -> None:
        """Update self.W via Hebbian rule on consecutive operator pairs.

        For each adjacent pair (op_i, op_{i+1}) in ops_this_turn, increment
        W[dim(op_i)][dim(op_{i+1})] by lr (and decay all other entries
        by 1-lr*0.01 to keep W bounded).

        Result: W reflects which cortex dimensions are coupled in THIS
        user's operator chains.
        """
        if not ops_this_turn or len(ops_this_turn) < 2:
            return
        # Convert ops to dims
        dims = [self.OP_TO_DIM.get(op, 0) for op in ops_this_turn if 0 <= op <= 9]
        # Hebbian increment on adjacent pairs
        for k in range(len(dims) - 1):
            i, j = dims[k], dims[k + 1]
            self.W[i][j] = float(self.W[i][j] + lr * (1.0 - self.W[i][j]))
            # Symmetric counterpart at half rate
            self.W[j][i] = float(self.W[j][i] + lr * 0.5 * (1.0 - self.W[j][i]))
        # Mild decay on all entries to keep matrix bounded
        decay = 1.0 - lr * 0.01
        for i in range(N_DIMS):
            for j in range(N_DIMS):
                self.W[i][j] = float(self.W[i][j] * decay)

    def append_turn(self,
                    ops_this_turn: List[int],
                    olfactory_record: Optional[Dict[str, Any]] = None,
                    attractor_layer: str = "transient") -> None:
        """Add this turn's algebraic state to arc / trail / sequence."""
        # Record turn start in arc
        self.turn_breaks.append(len(self.arc))
        # Append ops
        self.arc.extend([int(op) for op in ops_this_turn if 0 <= op <= 9])
        # Trail
        if olfactory_record is not None:
            self.trail.append(olfactory_record)
        # Sequence
        self.sequence.append(str(attractor_layer))
        # Counter
        self.turn_count += 1
        self.last_seen = time.time()

    # ===================================================================
    # Readouts (no text; pure algebraic summaries)
    # ===================================================================

    def is_returning_user(self) -> bool:
        return self.turn_count > 0

    def latest_arc(self, n_turns: int = 5) -> List[int]:
        """Last N turns' worth of operators, flat."""
        if not self.turn_breaks or n_turns <= 0:
            return list(self.arc[-50:])  # cap defensively
        # Find arc index where the (turn_count - n_turns)-th turn began
        target_turn = max(0, len(self.turn_breaks) - n_turns)
        if target_turn >= len(self.turn_breaks):
            return []
        start = self.turn_breaks[target_turn]
        return list(self.arc[start:])

    def W_trace(self) -> float:
        """Trace of W (sum of diagonals) — overall coupling strength."""
        return float(sum(self.W[i][i] for i in range(N_DIMS)))

    def attractor_trajectory(self) -> List[str]:
        """Sequence of attractor-layer names across turns."""
        return list(self.sequence)

    def harmony_rate_in_arc(self) -> float:
        """Fraction of operators in the arc that are HARMONY (op 7).

        Mirrors CK's global harmony_rate but for THIS user's arc.
        """
        if not self.arc:
            return 0.0
        h = sum(1 for op in self.arc if op == 7)
        return float(h) / float(len(self.arc))

    def turn_summary(self, k: int) -> Optional[Dict[str, Any]]:
        """Get the algebraic summary of turn k (0-indexed).

        Returns dict with: ops, attractor_layer, olfactory_record (if any).
        Returns None if k is out of range.
        """
        if k < 0 or k >= len(self.turn_breaks):
            return None
        start = self.turn_breaks[k]
        end = self.turn_breaks[k + 1] if k + 1 < len(self.turn_breaks) else len(self.arc)
        ops = self.arc[start:end]
        layer = self.sequence[k] if k < len(self.sequence) else "transient"
        olf = self.trail[k] if k < len(self.trail) else None
        return {
            "turn": k,
            "ops": ops,
            "ops_named": [OP_NAMES[o] if 0 <= o <= 9 else "?" for o in ops],
            "attractor_layer": layer,
            "olfactory_record": olf,
        }
