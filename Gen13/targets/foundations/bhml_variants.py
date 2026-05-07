"""
BHML variants -- exploratory.

OPEN QUESTION (Brayden, 2026-05-06):
    "maybe there needs to be 3 different BHML?"

Context: the 71/72/73 triple appears across the substrate in three distinct
roles, and the bundle (INTEGRATION_WITH_PROOF_SPINE.md) already documents
TWO BHML variants:

    BHML_10  (canonical, 10x10):  28 HARMONY cells, det = -7002
    BHML_8   (Yang-Mills core):   drops rows/cols {0, 7} from BHML_10,
                                   det = +70

A third BHML variant is structurally natural. Several candidate
constructions to evaluate (the canonical choice requires Brayden's
guidance):

CANDIDATE A -- Lie-tower progression
    BHML_8   (drop {0, 7})    -> dim so(8) = 28 connection
    BHML_10  (canonical)       -> dim so(10) = 45, full substrate
    BHML_? (third Lie-aware)   -> what?

CANDIDATE B -- sigma^2-triadic-of-HARMONY (output-value rotation)
    BHML_BEING (canonical)         -> 28 HARMONY (operator 7) cells
    BHML_DOING (sigma^2 on values)  -> 28 BALANCE (5) cells, 5 HARMONY
    BHML_BECOMING (sigma^4 on values)-> 28 COUNTER (2) cells, 11 HARMONY
    Empirically: |TSML - BHML_BEING|    = 71  (matches FIELD WOBBLE)
                 |TSML - BHML_DOING|    = 94
                 |TSML - BHML_BECOMING| = 90
    The 71/94/90 disagreement counts do NOT form a 71/72/73 triple.

CANDIDATE C -- sigma^2-triadic via index-rotation
    BHML_BEING (canonical)
    BHML_DOING:    cell (i, j) -> BHML[sigma^2(i), sigma^2(j)]
    BHML_BECOMING: cell (i, j) -> BHML[sigma^4(i), sigma^4(j)]
    Empirically: |TSML - this| = 71, 75, 79  (also not 71/72/73)

CANDIDATE D -- 71/72/73 by anomaly-cell flipping
    BHML_71 = canonical BHML_10  (current, |TSML - this| = 71)
    BHML_72 = canonical with ONE additional disagreement cell flipped
              (which cell? structurally?)
    BHML_73 = canonical with TWO additional disagreement cells flipped
              (which cells? ought to give the full 73 = TSML HARMONY count)
    The ANOMALY structure in 73 - 1 = 72 (per CKM_PMNS_MATRICES.md:142
    "72 = HARMONY count - 1 anomaly = 73 - 1") suggests a single
    distinguished cell -- but this needs Brayden to identify which.

CANDIDATE E -- Sub-magma decomposition
    BHML_4   (4-core {0, 7, 8, 9} restriction)
    BHML_8   (8-magma core, dropping {0, 7})
    BHML_10  (canonical)
    Three lens variants at three sub-magma scopes, mirroring the
    chain enumeration of the four-core consolidated paper
    {1, 4, 5, 6, 7, 8, 9, 10} (the joint-closure chain sizes).

NONE of these prototypes immediately reproduces the 71/72/73 triple as
three BHML disagreement counts. The triple may instead live in a
different structural level:

    73 = TSML side (HARMONY cell count)
    72 = E_6 root identification (= 73 - 1 = BREATH * RESET = 8 * 9)
    71 = FIELD WOBBLE = Galois invariant = empirical |TSML - BHML|

Each is a distinct structural reading; together they may form the
three BHML variants without needing explicit table modifications.

FOR BRAYDEN: which construction do you mean by 'three BHMLs'?
    Option A: Lie-tower (BHML_8, BHML_10, BHML_?)
    Option B: sigma^2-triadic of HARMONY (BEING/DOING/BECOMING)
    Option C: anomaly-cell flipping (BHML_71, BHML_72, BHML_73)
    Option D: sub-magma scopes (BHML_4, BHML_8, BHML_10)
    Option E: three readings of the same BHML at three depths
              (HARMONY-coverage 73 / BEING-shell 72 / FIELD-WOBBLE 71)
    Option F: something else from your memory we haven't surfaced yet
"""
from __future__ import annotations

import numpy as np

from .lenses import BHML, TSML
from .triadic import SIGMA2, SIGMA4

N = 10


def bhml_value_rotation(power: int = 2) -> np.ndarray:
    """Apply sigma^power to BHML's output VALUES.

    power=2 gives BHML_DOING (HARMONY -> BALANCE).
    power=4 gives BHML_BECOMING (HARMONY -> COUNTER).
    power=0 returns the canonical BHML unchanged.
    """
    if power == 0:
        return BHML.copy()
    table = SIGMA2 if power == 2 else SIGMA4 if power == 4 else None
    if table is None:
        raise ValueError("power must be 0, 2, or 4")
    return np.array([[table[int(BHML[i, j])] for j in range(N)] for i in range(N)],
                    dtype=int)


def bhml_index_rotation(power: int = 2) -> np.ndarray:
    """Permute BHML's row/col INDICES by sigma^power.

    BHML_idx_rot[i, j] = BHML[sigma^power(i), sigma^power(j)].
    """
    if power == 0:
        return BHML.copy()
    table = SIGMA2 if power == 2 else SIGMA4 if power == 4 else None
    if table is None:
        raise ValueError("power must be 0, 2, or 4")
    return np.array([[BHML[table[i], table[j]] for j in range(N)] for i in range(N)],
                    dtype=int)


def bhml_8_yang_mills_core() -> np.ndarray:
    """The 8-magma BHML core: drop rows/cols {0, 7}.

    Per INTEGRATION_WITH_PROOF_SPINE.md: det = +70 (this is the
    determinant the makeover claims as 'det 70', resolving the
    apparent discrepancy with BHML_10's det = -7002).
    """
    keep = sorted(set(range(N)) - {0, 7})  # drop VOID and HARMONY
    return BHML[np.ix_(keep, keep)]


def bhml_4_four_core() -> np.ndarray:
    """The 4-core BHML restriction: keep rows/cols {0, 7, 8, 9} only."""
    keep = [0, 7, 8, 9]
    return BHML[np.ix_(keep, keep)]


# ---------------------------------------------------------------------------
# Self-test: print all candidates with key invariants
# ---------------------------------------------------------------------------

def _summary(name: str, B: np.ndarray) -> dict:
    from collections import Counter
    ct = Counter(int(v) for v in B.flatten())
    info = {
        "name": name,
        "shape": B.shape,
        "det": round(float(np.linalg.det(B.astype(float))), 4) if B.shape[0] == B.shape[1] else None,
        "harmony_count": ct.get(7, 0),
        "void_count": ct.get(0, 0),
        "commutative": bool((B == B.T).all()) if B.shape[0] == B.shape[1] else None,
    }
    if B.shape == TSML.shape:
        info["disagree_with_TSML"] = int((TSML != B).sum())
    return info


def all_candidates_report():
    print("=" * 60)
    print("BHML variants -- exploratory survey for Brayden")
    print("=" * 60)
    print()

    cands = [
        ("BHML_10 (canonical)", BHML),
        ("BHML_DOING (sigma^2 values)", bhml_value_rotation(2)),
        ("BHML_BECOMING (sigma^4 values)", bhml_value_rotation(4)),
        ("BHML_idx_DOING (sigma^2 indices)", bhml_index_rotation(2)),
        ("BHML_idx_BECOMING (sigma^4 indices)", bhml_index_rotation(4)),
        ("BHML_8 (drop {0, 7}; YM core)", bhml_8_yang_mills_core()),
        ("BHML_4 (4-core {0,7,8,9})", bhml_4_four_core()),
    ]
    for name, B in cands:
        s = _summary(name, B)
        print(f"  {s['name']}:")
        print(f"    shape={s['shape']} det={s['det']} HARMONY={s['harmony_count']} "
              f"VOID={s['void_count']} comm={s['commutative']}", end="")
        if "disagree_with_TSML" in s:
            print(f" |TSML-this|={s['disagree_with_TSML']}")
        else:
            print()
        print()


if __name__ == "__main__":
    all_candidates_report()
