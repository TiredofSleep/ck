# -*- coding: utf-8 -*-
"""
hebbian_5x5.py - persistent 5x5 co-activation tensor (MATH_IN_CK.md Sec 2.2, 11.2).

CK's associative memory at the AO scale.  For a 5-dimensional AO state
vector ``d_t`` (from ``ao_basis.project_10_to_5``), the outer product
``d_t (x) d_{t-1}`` drives a Hebbian update:

    W_ij <- W_ij + eta * d_i * d_j         (strengthen)
    W_ij <- W_ij * (1 - decay)             (forget)
    W_ij <- clamp(W_ij, -clamp_abs, +clamp_abs)

The diagonal entries encode self-persistence of an element; the
off-diagonals encode which elements co-fire.  Symmetric form
(W_ij = W_ji) is enforced after each update because the CL crossing is
symmetric in the pair (element_i, element_j).

Persistence:
- ``save(path)`` writes a single JSON file with W, meta counters, and a
  format version.
- ``load(path)`` returns a tensor with state restored.  If the file is
  missing, returns a fresh zero tensor (that is the "newborn CK" state).

Scope:
- Floats only; no numpy dependency.
- Thread-safety: one-process assumption.  The idle_loop runs on demand
  from a CLI; the fluency_server reads a snapshot and never writes.

Reference constants:
- eta_default = 0.05    (learning rate per tick)
- decay_default = 0.002 (forgetting per tick; so stale links fade)
- clamp_abs_default = 5.0 (upper bound on any W_ij; prevents runaway)

These defaults are conservative: at eta=0.05 decay=0.002 and equal
co-activation d_i = d_j = 1.0 every tick, the equilibrium is
W* = eta / decay = 25 activations' worth; clamp=5 caps it below that.
The clamp is the primary stability guarantee; decay is the secondary.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .ao_basis import NUM_AO, AO_NAMES


# ---------------------------------------------------------------------------
# defaults
# ---------------------------------------------------------------------------

DEFAULT_ETA: float = 0.05
DEFAULT_DECAY: float = 0.002
DEFAULT_CLAMP_ABS: float = 5.0
TENSOR_FORMAT_VERSION: int = 1


# ---------------------------------------------------------------------------
# the tensor
# ---------------------------------------------------------------------------


class HebbianTensor5x5:
    """5x5 symmetric co-activation tensor with Hebbian update and persistence.

    Internal state:
        W          - list[list[float]], shape (5, 5), symmetric
        n_updates  - counter of update() calls
        n_decays   - counter of decay() calls (typically == n_updates)
        meta       - free-form dict for log anchors (session id, log file,
                     last_entry_index, etc.)
    """

    def __init__(
        self,
        W: Optional[Sequence[Sequence[float]]] = None,
        eta: float = DEFAULT_ETA,
        decay: float = DEFAULT_DECAY,
        clamp_abs: float = DEFAULT_CLAMP_ABS,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.eta = float(eta)
        self.decay = float(decay)
        self.clamp_abs = float(clamp_abs)
        self.n_updates = 0
        self.n_decays = 0
        self.meta: Dict[str, Any] = dict(meta) if meta else {}

        if W is None:
            self.W: List[List[float]] = [
                [0.0] * NUM_AO for _ in range(NUM_AO)
            ]
        else:
            self.W = [[float(W[i][j]) for j in range(NUM_AO)] for i in range(NUM_AO)]

    # ---- the update ----

    def update(
        self,
        d_now: Sequence[float],
        d_prev: Optional[Sequence[float]] = None,
    ) -> None:
        """Apply one Hebbian update + decay step.

        Symmetric update:
            delta_ij = 0.5 * (d_now[i] * d_prev[j] + d_now[j] * d_prev[i])
            W_ij <- W_ij + eta * delta_ij
            W_ij <- W_ij * (1 - decay)
            W_ij <- clamp(..., -clamp_abs, +clamp_abs)

        If ``d_prev`` is None, we use ``d_now`` (self-outer product, which
        is the standard Hebbian self-coactivation and is the first-tick
        behavior before a history exists).
        """
        if len(d_now) != NUM_AO:
            raise ValueError(f"d_now must have length {NUM_AO}; got {len(d_now)}")
        dp = d_prev if d_prev is not None else d_now
        if len(dp) != NUM_AO:
            raise ValueError(f"d_prev must have length {NUM_AO}; got {len(dp)}")

        # NaN / inf guards
        dn = [_san(x) for x in d_now]
        dp = [_san(x) for x in dp]

        factor = 1.0 - self.decay
        ca = self.clamp_abs
        for i in range(NUM_AO):
            for j in range(i, NUM_AO):  # upper triangle, then mirror
                delta = 0.5 * (dn[i] * dp[j] + dn[j] * dp[i])
                w = self.W[i][j] + self.eta * delta
                w = w * factor
                if w > ca:
                    w = ca
                elif w < -ca:
                    w = -ca
                self.W[i][j] = w
                self.W[j][i] = w

        self.n_updates += 1
        self.n_decays += 1

    def decay_only(self) -> None:
        """Apply one decay without a Hebbian update (pure forgetting)."""
        factor = 1.0 - self.decay
        for i in range(NUM_AO):
            for j in range(NUM_AO):
                self.W[i][j] = self.W[i][j] * factor
        self.n_decays += 1

    # ---- scoring ----

    def prime(self, d: Sequence[float]) -> List[float]:
        """Return W @ d (the prior field of the tensor applied to state d).

        This is the vector that says "given CK has seen co-activations W,
        how strongly does state d trigger each element?"  It is used by
        ``fusion.py`` to amplify the operator profile before scoring.
        """
        if len(d) != NUM_AO:
            raise ValueError(f"d must have length {NUM_AO}; got {len(d)}")
        ds = [_san(x) for x in d]
        out = [0.0] * NUM_AO
        for i in range(NUM_AO):
            s = 0.0
            row = self.W[i]
            for j in range(NUM_AO):
                s += row[j] * ds[j]
            out[i] = s
        return out

    def score(self, d: Sequence[float]) -> float:
        """Return d^T W d : the scalar priming strength of d under W."""
        if len(d) != NUM_AO:
            raise ValueError(f"d must have length {NUM_AO}; got {len(d)}")
        ds = [_san(x) for x in d]
        s = 0.0
        for i in range(NUM_AO):
            row = self.W[i]
            for j in range(NUM_AO):
                s += ds[i] * row[j] * ds[j]
        return s

    # ---- introspection ----

    def norm(self) -> float:
        """Frobenius norm of W (euclidean sum-of-squares)."""
        s = 0.0
        for i in range(NUM_AO):
            for j in range(NUM_AO):
                v = self.W[i][j]
                s += v * v
        return math.sqrt(s)

    def top_links(self, k: int = 3, off_diagonal_only: bool = True
                  ) -> List[Tuple[str, str, float]]:
        """Return the top-k strongest links as (name_i, name_j, W_ij) triples."""
        items: List[Tuple[str, str, float]] = []
        for i in range(NUM_AO):
            for j in range(i, NUM_AO):
                if off_diagonal_only and i == j:
                    continue
                items.append((AO_NAMES[i], AO_NAMES[j], self.W[i][j]))
        items.sort(key=lambda t: abs(t[2]), reverse=True)
        return items[:k]

    # ---- persistence ----

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format": TENSOR_FORMAT_VERSION,
            "ao_names": list(AO_NAMES),
            "W": [list(row) for row in self.W],
            "eta": self.eta,
            "decay": self.decay,
            "clamp_abs": self.clamp_abs,
            "n_updates": self.n_updates,
            "n_decays": self.n_decays,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HebbianTensor5x5":
        if not isinstance(d, dict):
            raise TypeError(f"expected dict, got {type(d).__name__}")
        fmt = int(d.get("format", 0))
        if fmt > TENSOR_FORMAT_VERSION:
            raise ValueError(
                f"tensor format {fmt} newer than this code "
                f"(supports up to {TENSOR_FORMAT_VERSION})"
            )
        W = d.get("W")
        if (not W or len(W) != NUM_AO
                or any(len(row) != NUM_AO for row in W)):
            raise ValueError(
                f"W must be {NUM_AO}x{NUM_AO}; got shape "
                f"({len(W) if W else 0}x{len(W[0]) if W and W[0] else 0})"
            )
        t = cls(
            W=W,
            eta=float(d.get("eta", DEFAULT_ETA)),
            decay=float(d.get("decay", DEFAULT_DECAY)),
            clamp_abs=float(d.get("clamp_abs", DEFAULT_CLAMP_ABS)),
            meta=d.get("meta") or {},
        )
        t.n_updates = int(d.get("n_updates", 0))
        t.n_decays = int(d.get("n_decays", 0))
        return t

    def save(self, path: "str | Path") -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, sort_keys=True)
            f.flush()
        # atomic rename (on POSIX and Windows since Py 3.3)
        tmp.replace(p)
        return p

    @classmethod
    def load(cls, path: "str | Path") -> "HebbianTensor5x5":
        """Load from disk; return fresh zero tensor if file missing."""
        p = Path(path)
        if not p.exists():
            return cls()
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        return cls.from_dict(d)

    # ---- repr ----

    def __repr__(self) -> str:
        return (
            f"HebbianTensor5x5(norm={self.norm():.4f}, "
            f"n_updates={self.n_updates}, "
            f"eta={self.eta}, decay={self.decay})"
        )


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _san(x: Any) -> float:
    """Sanitize a number: NaN / inf -> 0.0; else float()."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 0.0
    if v != v or v in (float("inf"), float("-inf")):
        return 0.0
    return v


# ---------------------------------------------------------------------------
# canonical on-disk path (shared with idle_loop and fusion)
# ---------------------------------------------------------------------------

DEFAULT_TENSOR_PATH: Path = Path(__file__).resolve().parent / "hebbian_5x5.json"


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile
    import os

    t = HebbianTensor5x5()
    assert t.norm() == 0.0
    # correlated co-activation at (Water, Fire) = (D2, D3)
    d = [0.0, 0.0, 1.0, 1.0, 0.0]
    for _ in range(100):
        t.update(d, d)
    assert t.W[2][3] > 0.0, t.W
    assert abs(t.W[2][3] - t.W[3][2]) < 1e-9, "must be symmetric"
    assert all(abs(t.W[i][j]) <= DEFAULT_CLAMP_ABS
               for i in range(NUM_AO) for j in range(NUM_AO))

    # isolated element should stay near zero
    assert abs(t.W[0][0]) < 0.1, t.W[0][0]

    # prime/score
    primed = t.prime([0.0, 0.0, 1.0, 0.0, 0.0])
    assert primed[3] > 0.0, primed  # W[3,2] * 1 > 0 since W[2,3] > 0
    sc = t.score(d)
    assert sc > 0.0, sc

    # persist
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "h.json"
        t.save(p)
        t2 = HebbianTensor5x5.load(p)
        assert t2.n_updates == t.n_updates
        assert abs(t2.W[2][3] - t.W[2][3]) < 1e-12

    # missing file -> zero tensor (newborn)
    ghost = HebbianTensor5x5.load(Path(tempfile.gettempdir()) / "nonexistent.json")
    assert ghost.norm() == 0.0

    print(f"[hebbian_5x5] self-test passed; {t}")
    print(f"              top link: {t.top_links(1)}")
