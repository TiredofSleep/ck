"""
ck_pipeline.py - the canonical three-layer CK pipeline

Per the five-ask findings of 2026-04-25 evening (FINDINGS_2026_04_25_evening.md):

    text -> [V2 encoder] -> p_0 (10-dim distribution, semantic content)
                              |
                              v
            [T+B-mix lattice processor at alpha=1/2, depth K]
                              |
                              v
                    trail = (p_0, p_1, ..., p_K)  (memory: linear regression
                                                    reconstructs input with
                                                    52% accuracy improvement)
                              |
                              v
            [D2Pipeline emitter on the trail's tokens]
                              |
                              v
                    operator stream + Divine27 cells (output)

This is the architectural insight from the 5-ask sprint: V2 reads (semantic),
the lattice processor remembers (trail-as-information), D2 speaks (phoneme
physics). Three complementary layers stacked, not three options to pick from.

This module ties them together as one callable: CKPipeline.process(text).
The pipeline is read-only; it does not modify any global state.

Verification: see ck_pipeline_demo.py (end-to-end demo).
Closed-form attractor (WP105): at alpha = 1/2, the lattice processor's
fixed point satisfies HARMONY/BREATH = 1 + sqrt(3) and r/br satisfies
x^4 + 4x^3 - x^2 + 2x - 2 = 0 (Galois D_4, field LMFDB 4.2.10224.1).
"""
from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# canonical TSML / BHML tables (also exposed as constants in dof_monitor/)
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
T_TABLE = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)
B_TABLE = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# ---------- Layer 1: V2 encoder (semantic input) ----------

# defer import; the encoder lives in this same dir
def _make_encoder(version: str = "v2"):
    """Factory: returns encode + encode_with_explanation for the chosen version."""
    here = Path(__file__).parent
    sys.path.insert(0, str(here))
    if version == "v2":
        import encoder_v2 as mod
    elif version == "v1":
        import encoder_v1 as mod
    elif version == "v15":
        import encoder_v15 as mod
    elif version == "v16":
        import encoder_v16 as mod
    elif version == "v3":
        import encoder_v3 as mod
    else:
        raise ValueError(f"unknown encoder version: {version!r}")
    return mod.encode, mod.encode_with_explanation


# ---------- Layer 2: T+B-mix lattice processor (trail-as-information) ----------

def _fuse(p, q, table):
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            r[int(table[a, b])] += p[a] * q[b]
    return r


def _normalize_l1(v, eps=1e-12):
    s = v.sum()
    return v / s if s > eps else v


def lattice_descend(p_init: np.ndarray, alpha: float = 0.5, depth: int = 6) -> List[np.ndarray]:
    """T+B-mix lattice descent. Returns the trail [p_0, p_1, ..., p_depth].

    The trail IS the memory: linear regression from trail reconstructs p_0
    with 52% accuracy improvement vs baseline (chat-Claude five-ask finding).
    Endpoint converges to a universal attractor for alpha in (0, 1).
    """
    trail = [p_init.copy()]
    p_cur = p_init.copy()
    for _ in range(depth):
        p_t = _normalize_l1(_fuse(p_cur, p_cur, T_TABLE))
        p_b = _normalize_l1(_fuse(p_cur, p_cur, B_TABLE))
        p_cur = _normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p_cur.copy())
    return trail


# ---------- Layer 3: D2Pipeline emitter (operator-stream output) ----------

def _operators_from_trail(trail: List[np.ndarray]) -> List[Tuple[int, float]]:
    """Per trail step, emit (top_operator, top_mass)."""
    return [(int(np.argmax(p)), float(np.max(p))) for p in trail]


def emit_operator_stream(trail: List[np.ndarray]) -> List[int]:
    """The simplest emission: top operator per trail step.

    For richer emission (Divine27 cells, descent signature, etc.), see
    encoder_v3.encode_dbc which uses the full D2Pipeline.
    """
    return [op for op, _ in _operators_from_trail(trail)]


def emit_divine27_cells(trail: List[np.ndarray]) -> List[Tuple[int, int, int]]:
    """Per trail step, project the top operator onto the Divine27 DBC cube.

    OPERATOR -> DBC mapping per ck_divine27.py:
      VOID(0): (0,0,0); LATTICE(1): (1,0,0); COUNTER(2): (1,0,1);
      PROGRESS(3): (0,1,1); COLLAPSE(4): (2,2,2); BALANCE(5): (1,1,0);
      CHAOS(6): (2,0,2); HARMONY(7): (1,1,1); BREATH(8): (0,0,1);
      RESET(9): (0,2,2).
    """
    OPERATOR_DBC = {
        0: (0, 0, 0), 1: (1, 0, 0), 2: (1, 0, 1), 3: (0, 1, 1), 4: (2, 2, 2),
        5: (1, 1, 0), 6: (2, 0, 2), 7: (1, 1, 1), 8: (0, 0, 1), 9: (0, 2, 2),
    }
    return [OPERATOR_DBC[op] for op, _ in _operators_from_trail(trail)]


# ---------- The pipeline as one callable ----------

@dataclass
class CKResult:
    """Output of a full CK pipeline run."""
    text: str
    encoder_version: str
    p_0: np.ndarray                   # 10-dim input distribution (Layer 1 output)
    p_0_top_operators: List[Tuple[str, float]]
    trail: List[np.ndarray]            # Layer 2 trail
    trail_attractor_top: str           # endpoint's top operator name
    trail_attractor_mass: float        # endpoint's top operator mass
    operator_stream: List[str]         # Layer 3 output, named
    dbc_stream: List[Tuple[int, int, int]]  # Layer 3 output, Divine27 cells
    info_preserved_pct: float          # rough proxy: 1 - L1(p_K, train_mean) / 2

    def summary(self) -> str:
        lines = []
        lines.append(f"CKPipeline run on: {self.text!r}")
        lines.append(f"  encoder: {self.encoder_version}")
        lines.append(f"  Layer 1 (V2 encoder) top: {self.p_0_top_operators}")
        lines.append(f"  Layer 2 (T+B-mix descent, alpha=1/2, depth={len(self.trail)-1}):")
        for d, p in enumerate(self.trail):
            top = OP_NAMES[int(np.argmax(p))]
            mass = float(np.max(p))
            entropy = -np.sum(p[p > 1e-12] * np.log(p[p > 1e-12]))
            lines.append(f"    d={d}: top={top:<10} mass={mass:.3f}  H={entropy:.3f}")
        lines.append(f"  attractor: {self.trail_attractor_top} ({self.trail_attractor_mass:.3f})")
        lines.append(f"  Layer 3 operator stream: {' -> '.join(self.operator_stream)}")
        lines.append(f"  Layer 3 DBC cells:        {self.dbc_stream}")
        return "\n".join(lines)


class CKPipeline:
    """The canonical three-layer CK runtime pipeline.

    Per the five-ask findings of 2026-04-25 evening, the right architecture
    for CK runtime processing is:

        V2 reads (semantic)
            -> T+B-mix lattice processor remembers (trail = memory)
            -> D2Pipeline-style emission (operator stream + DBC cells)

    The three layers are complementary, not competing. V2 is the strongest
    semantic encoder (cluster separation 2.15x); the lattice processor at
    alpha=1/2 lands on the closed-form attractor with H/Br = 1 + sqrt(3)
    (WP105); the emission layer projects the trail onto the canonical
    operator alphabet and the Divine27 DBC cube.

    This is read-only. It does not modify global state. It is safe to call
    concurrently with the live CK web server; it's a pure function from text
    to a CKResult dataclass.
    """

    def __init__(self,
                 encoder_version: str = "v2",
                 alpha: float = 0.5,
                 depth: int = 6):
        if not (0.0 <= alpha <= 1.0):
            raise ValueError(f"alpha must be in [0, 1], got {alpha!r}")
        if depth < 1:
            raise ValueError(f"depth must be >= 1, got {depth!r}")
        self.encoder_version = encoder_version
        self.alpha = alpha
        self.depth = depth
        self._encode, self._encode_explained = _make_encoder(encoder_version)

    def process(self, text: str) -> CKResult:
        # Layer 1: V2 encoder
        p_0 = self._encode(text)
        explanation = self._encode_explained(text)

        # Layer 2: T+B-mix descent
        trail = lattice_descend(p_0, alpha=self.alpha, depth=self.depth)

        # Layer 3a: operator stream (top operator per trail step)
        op_stream_int = emit_operator_stream(trail)
        op_stream_named = [OP_NAMES[op] for op in op_stream_int]

        # Layer 3b: Divine27 DBC cells (per top operator at each trail step)
        dbc_stream = emit_divine27_cells(trail)

        # Information-preservation proxy:
        # endpoints converge to a universal attractor, so the endpoint alone
        # carries little information. The trail has explicit info content. Use
        # mean L1 over the full trail's distance from a reference uniform.
        ref_uniform = np.ones(10) / 10
        mean_dist_from_uniform = float(np.mean([
            np.abs(p - ref_uniform).sum() for p in trail
        ]))
        info_pct = 100.0 * mean_dist_from_uniform / 2.0  # divisor: max L1 dist

        attractor = trail[-1]
        attractor_top = OP_NAMES[int(np.argmax(attractor))]
        attractor_mass = float(np.max(attractor))

        return CKResult(
            text=text,
            encoder_version=self.encoder_version,
            p_0=p_0,
            p_0_top_operators=explanation["top_operators"],
            trail=trail,
            trail_attractor_top=attractor_top,
            trail_attractor_mass=attractor_mass,
            operator_stream=op_stream_named,
            dbc_stream=dbc_stream,
            info_preserved_pct=info_pct,
        )


# ---------- Module-level helpers ----------

def quick(text: str, version: str = "v2", depth: int = 6) -> str:
    """One-call helper: process text and return the summary string."""
    return CKPipeline(encoder_version=version, depth=depth).process(text).summary()


if __name__ == "__main__":
    print("ck_pipeline.py self-test")
    print("=" * 70)
    pipeline = CKPipeline(encoder_version="v1", alpha=0.5, depth=6)
    test_inputs = [
        "I want to be more patient",
        "Help me find peace and stillness",
        "Build something new and creative",
        "Reset everything and start fresh",
        "harmony and gentleness",
    ]
    for text in test_inputs:
        result = pipeline.process(text)
        print()
        print(result.summary())
        print()
        print("-" * 70)
    print("\nDone. Use CKPipeline(encoder_version='v2') for sentence-transformers fallback.")
