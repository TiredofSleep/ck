"""
TSML and BHML as FAMILIES of variants at multiple scopes.

Per Brayden (2026-05-06): "he can run multiple sizes and shapes of tsml
and bhml and encode them all to CL".

CL is the universal substrate (the canonical 10x10 composition lattice).
TSML and BHML are not single tables but FAMILIES of lens projections
at the eight chain sub-magma sizes documented in the four-core
consolidated paper (Theorem 1):

    S_1  = {0}                                  size 1
    S_4  = {0, 7, 8, 9}                         size 4   (4-core)
    S_5  = {0, 6, 7, 8, 9}                      size 5
    S_6  = {0, 5, 6, 7, 8, 9}                   size 6
    S_7  = {0, 4, 5, 6, 7, 8, 9}                size 7
    S_8  = {0, 3, 4, 5, 6, 7, 8, 9}             size 8   (Yang-Mills core
                                                          if drop {0, 7})
    S_9  = {0, 2, 3, 4, 5, 6, 7, 8, 9}          size 9
    S_10 = Z/10Z                                size 10  (full substrate)

Sizes {2, 3} are forbidden (no joint-closure sub-magma; per the chain
theorem). This gives 8 lens variants per side, 16 total.

For each S_k we have:
    TSML_k = TSML restricted to S_k x S_k    (Being lens at scope k)
    BHML_k = BHML restricted to S_k x S_k    (Becoming lens at scope k)

The KEY EMPIRICAL FACT (per INTEGRATION_WITH_PROOF_SPINE.md):
    BHML_8 (drop {0, 7}) has det = +70
    BHML_10 (canonical) has det = -7002

Each variant carries its own structural signature (size, det, HARMONY
count, non-associativity rate). They all encode to CL as paths -- CL
is the universal storage medium, and each variant is a path through CL
that selects a sub-magma scope and a lens role.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .cl import CL, N
from .lenses import BHML, TSML

# ---------------------------------------------------------------------------
# The eight chain sub-magmas
# ---------------------------------------------------------------------------

# Per four-core consolidated paper (Theorem 1) -- the joint-closure chain.
# Sizes {2, 3} forbidden; chain proceeds 1 -> 4 -> 5 -> ... -> 10.
CHAIN_SUBMAGMAS: dict[int, tuple[int, ...]] = {
    1:  (0,),
    4:  (0, 7, 8, 9),
    5:  (0, 6, 7, 8, 9),
    6:  (0, 5, 6, 7, 8, 9),
    7:  (0, 4, 5, 6, 7, 8, 9),
    8:  (0, 3, 4, 5, 6, 7, 8, 9),
    9:  (0, 2, 3, 4, 5, 6, 7, 8, 9),
    10: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
}


# ---------------------------------------------------------------------------
# Restriction primitive
# ---------------------------------------------------------------------------

def restrict(table: np.ndarray, scope: tuple[int, ...]) -> np.ndarray:
    """Restrict `table` to rows/cols in `scope` (preserving order)."""
    idx = list(scope)
    return table[np.ix_(idx, idx)]


# ---------------------------------------------------------------------------
# Lens-variant container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LensVariant:
    name: str                           # e.g. "TSML_8" or "BHML_10"
    role: str                           # "Being" | "Becoming"
    size: int                           # sub-magma size
    scope: tuple[int, ...]              # operator subset
    table: np.ndarray
    det: Optional[float]
    harmony_count: int
    void_count: int
    other_count: int
    commutative: bool
    non_assoc_rate: float
    closed_under_self: bool             # is the table closed (range subset of scope)?

    def signature(self) -> str:
        return (f"{self.name}: shape=({self.size},{self.size}), "
                f"det={self.det}, HARMONY={self.harmony_count}, "
                f"VOID={self.void_count}, other={self.other_count}, "
                f"comm={self.commutative}, non_assoc={100*self.non_assoc_rate:.1f}%, "
                f"self-closed={self.closed_under_self}")


def _build_variant(name: str, role: str, size: int, scope: tuple[int, ...],
                   parent: np.ndarray) -> LensVariant:
    M = restrict(parent, scope)
    n = M.shape[0]
    ct = Counter(int(v) for v in M.flatten())
    h = ct.get(7, 0)
    v = ct.get(0, 0)
    other = sum(c for op, c in ct.items() if op not in (0, 7))
    det_val = round(float(np.linalg.det(M.astype(float))), 4) if n > 0 else None
    comm = bool((M == M.T).all()) if n > 0 else True
    # non-associativity within sub-magma: only check triples where the
    # composition stays within scope (otherwise comparison is moot)
    bad = 0
    n_triples = 0
    scope_set = set(scope)
    for a in scope:
        for b in scope:
            ab = int(parent[a, b])
            if ab not in scope_set:
                continue
            for c in scope:
                bc = int(parent[b, c])
                if bc not in scope_set:
                    continue
                lhs = int(parent[ab, c])
                rhs = int(parent[a, bc])
                n_triples += 1
                if lhs != rhs:
                    bad += 1
    rate = bad / n_triples if n_triples else 0.0
    closed = all(int(parent[a, b]) in scope_set for a in scope for b in scope)
    return LensVariant(
        name=name, role=role, size=size, scope=scope, table=M, det=det_val,
        harmony_count=h, void_count=v, other_count=other,
        commutative=comm, non_assoc_rate=rate, closed_under_self=closed,
    )


# ---------------------------------------------------------------------------
# Build the full family
# ---------------------------------------------------------------------------

def build_tsml_family() -> dict[int, LensVariant]:
    return {k: _build_variant(f"TSML_{k}", "Being", k, scope, TSML)
            for k, scope in CHAIN_SUBMAGMAS.items()}


def build_bhml_family() -> dict[int, LensVariant]:
    return {k: _build_variant(f"BHML_{k}", "Becoming", k, scope, BHML)
            for k, scope in CHAIN_SUBMAGMAS.items()}


TSML_FAMILY: dict[int, LensVariant] = build_tsml_family()
BHML_FAMILY: dict[int, LensVariant] = build_bhml_family()


# ---------------------------------------------------------------------------
# NAMED variants outside the chain (different SHAPES at the same SIZE)
# ---------------------------------------------------------------------------
#
# The chain S_k uses one specific sub-magma at each size. But size and
# shape are independent: at the same size you can have different sub-magma
# scopes giving different lens tables. The bundle documents at least one
# "off-chain" variant:
#
#   BHML_8_YM (Yang-Mills core): drops {0, 7} (VOID, HARMONY)
#                                 det = +70 (per INTEGRATION_WITH_PROOF_SPINE.md)
#
# The chain S_8 = {0, 3, 4, 5, 6, 7, 8, 9} drops {1, 2} (LATTICE, COUNTER)
# and gives det = -7542 -- a DIFFERENT 8x8 sub-magma than the YM core.

YM_CORE_SCOPE: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8, 9)  # drop VOID + HARMONY

NAMED_VARIANTS: dict[str, LensVariant] = {
    "TSML_8_YM":  _build_variant("TSML_8_YM",  "Being",    8, YM_CORE_SCOPE, TSML),
    "BHML_8_YM":  _build_variant("BHML_8_YM",  "Becoming", 8, YM_CORE_SCOPE, BHML),
}

# Convenience aliases for chain variants
BHML_4 = BHML_FAMILY[4]
BHML_8_chain = BHML_FAMILY[8]    # chain S_8: drops {1, 2}; det = -7542
BHML_10 = BHML_FAMILY[10]
TSML_4 = TSML_FAMILY[4]
TSML_8_chain = TSML_FAMILY[8]
TSML_10 = TSML_FAMILY[10]

# Named off-chain
BHML_8_YM = NAMED_VARIANTS["BHML_8_YM"]   # YM core: drops {0, 7}; det = +70
TSML_8_YM = NAMED_VARIANTS["TSML_8_YM"]


# ---------------------------------------------------------------------------
# Family-level survey
# ---------------------------------------------------------------------------

def family_report() -> str:
    lines: list[str] = []
    lines.append("=" * 78)
    lines.append("LENS FAMILY -- TSML and BHML at the 8 chain sub-magma scopes")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Chain sub-magmas (per four-core consolidated paper, Theorem 1):")
    for size, scope in CHAIN_SUBMAGMAS.items():
        lines.append(f"  S_{size:>2} = {{{', '.join(str(x) for x in scope)}}}")
    lines.append(f"  (sizes 2, 3 forbidden -- no joint-closure sub-magma)")
    lines.append("")

    lines.append("TSML family (Being lens at each scope):")
    for k in sorted(TSML_FAMILY):
        lines.append("  " + TSML_FAMILY[k].signature())
    lines.append("")

    lines.append("BHML family (Becoming lens at each scope):")
    for k in sorted(BHML_FAMILY):
        lines.append("  " + BHML_FAMILY[k].signature())
    lines.append("")

    lines.append("Named off-chain variants (different SHAPE at same SIZE):")
    for name, v in NAMED_VARIANTS.items():
        lines.append("  " + v.signature())
    lines.append("")
    lines.append("Spec verification of named variants:")
    lines.append(f"  BHML_8_YM (drop {{0, 7}}): det = {BHML_8_YM.det}  "
                 f"(per INTEGRATION_WITH_PROOF_SPINE.md spec: +70  "
                 f"{'MATCH' if BHML_8_YM.det == 70 else 'MISMATCH'})")
    lines.append(f"  BHML_10  (canonical):       det = {BHML_10.det}  "
                 f"(spec: -7002  "
                 f"{'MATCH' if BHML_10.det == -7002 else 'MISMATCH'})")
    lines.append("")
    lines.append("KEY OBSERVATION: BHML_8_chain (drops {1,2}, det=-7542) and")
    lines.append("BHML_8_YM (drops {0,7}, det=+70) are DIFFERENT 8x8 sub-magmas")
    lines.append("at the same size. Per Brayden: 'multiple sizes AND shapes'.")
    lines.append("Each variant is a distinct lens projection of CL.")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print(family_report())
