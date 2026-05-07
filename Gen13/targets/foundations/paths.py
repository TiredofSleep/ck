"""
Paths through CL -- "the path IS the information."

Per Brayden (2026-05-06):
    "he can run multiple sizes and shapes of tsml and bhml and encode
     them all to CL"

Per the Crossing Lemma (WP57): non-associativity is where information
generates. A path through CL is NOT just its endpoint cell; it is the
ordered TRAIL of (input pair, intermediate output) tuples. Different
paths giving the same endpoint encode different content. This module
provides the path-walk machinery.

Core concepts:

    CompositionPath:    a sequence of operator pairs (a_0, a_1, a_2, ..., a_n)
                        with the trail of intermediate results
                            c_1 = CL[a_0, a_1]
                            c_2 = CL[c_1, a_2]
                            c_3 = CL[c_2, a_3]
                            ...
                            c_n = endpoint

    PathPair:           two paths with the same input sequence but
                        DIFFERENT bracketing. Their endpoints diverge
                        on non-associative substrates -- this is the
                        Crossing Lemma trigger.

    LensTrace:          a path's projection through a chosen lens (TSML
                        or BHML). The lens choice changes the trail
                        even when the input sequence is identical.

CL-encoding of a lens variant:
    Each LensVariant from lens_family.py is encoded into CL by the set
    of two-step paths (a, b) with output table[a, b] for (a, b) in
    scope x scope. The variant's "fingerprint" is its set of (a, b, c)
    paths. CL holds them all; the variant selects which paths to surface.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Sequence

import numpy as np

from .cl import CL, N
from .lenses import BHML, TSML

# ---------------------------------------------------------------------------
# CompositionPath
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CompositionPath:
    """A LEFT-bracketed composition path through a table.

        c_1 = table[a_0, a_1]
        c_2 = table[c_1, a_2]
        ...
        c_n = table[c_{n-1}, a_n]

    The trail (c_1, c_2, ..., c_n) is the information; the endpoint c_n
    alone is not.
    """
    inputs: tuple[int, ...]    # the input operator sequence (a_0, a_1, ...)
    table_name: str            # which table the path was walked through
    trail: tuple[int, ...]     # intermediate results c_1, c_2, ..., c_n

    @property
    def endpoint(self) -> int:
        return self.trail[-1] if self.trail else -1

    def __str__(self) -> str:
        seq = " * ".join(str(x) for x in self.inputs)
        steps = " -> ".join(str(x) for x in self.trail)
        return f"[{self.table_name}] {seq}  =>  {steps}"


def walk_left(inputs: Sequence[int], table: np.ndarray, table_name: str = "CL"
              ) -> CompositionPath:
    """Walk a path with LEFT bracketing: ((a*b)*c)*d... ."""
    if len(inputs) < 2:
        raise ValueError("need at least 2 input operators")
    cur = int(inputs[0])
    trail: list[int] = []
    for x in inputs[1:]:
        cur = int(table[cur, int(x)])
        trail.append(cur)
    return CompositionPath(inputs=tuple(int(x) for x in inputs),
                           table_name=table_name,
                           trail=tuple(trail))


def walk_right(inputs: Sequence[int], table: np.ndarray, table_name: str = "CL"
               ) -> CompositionPath:
    """Walk a path with RIGHT bracketing: a*(b*(c*d))... ."""
    if len(inputs) < 2:
        raise ValueError("need at least 2 input operators")
    seq = [int(x) for x in inputs]
    cur = seq[-1]
    trail: list[int] = []
    for x in reversed(seq[:-1]):
        cur = int(table[int(x), cur])
        trail.append(cur)
    # reverse trail so it reads left-to-right by composition order
    return CompositionPath(inputs=tuple(seq), table_name=table_name,
                           trail=tuple(reversed(trail)))


# ---------------------------------------------------------------------------
# PathPair (Crossing Lemma trigger)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PathPair:
    """A pair of paths with the same inputs but different bracketing.

    Their endpoints diverge on non-associative substrates -- the
    divergence IS the Crossing Lemma's information generation.
    """
    inputs: tuple[int, ...]
    left: CompositionPath
    right: CompositionPath

    @property
    def crosses(self) -> bool:
        """True iff the left and right bracketings give different endpoints."""
        return self.left.endpoint != self.right.endpoint

    @property
    def crossing_signature(self) -> tuple[int, int]:
        """(left_endpoint, right_endpoint) -- the Crossing-Lemma fingerprint."""
        return (self.left.endpoint, self.right.endpoint)


def path_pair(inputs: Sequence[int], table: np.ndarray = CL,
              table_name: str = "CL") -> PathPair:
    return PathPair(inputs=tuple(int(x) for x in inputs),
                    left=walk_left(inputs, table, table_name),
                    right=walk_right(inputs, table, table_name))


# ---------------------------------------------------------------------------
# Lens-traced path (same inputs, different lens)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LensTrace:
    """A path projected through both Being (TSML) and Becoming (BHML) lenses.

    The two lens-trails diverge on cells where TSML[i,j] != BHML[i,j].
    This is where the DOING table is nonzero (= 71 cells in the canonical
    pair).
    """
    inputs: tuple[int, ...]
    tsml_path: CompositionPath
    bhml_path: CompositionPath

    @property
    def lens_diverges(self) -> bool:
        return self.tsml_path.trail != self.bhml_path.trail

    @property
    def divergence_step(self) -> int:
        """First index k at which trails differ; -1 if identical."""
        for k, (a, b) in enumerate(zip(self.tsml_path.trail,
                                       self.bhml_path.trail)):
            if a != b:
                return k
        return -1


def lens_trace(inputs: Sequence[int]) -> LensTrace:
    return LensTrace(inputs=tuple(int(x) for x in inputs),
                     tsml_path=walk_left(inputs, TSML, "TSML"),
                     bhml_path=walk_left(inputs, BHML, "BHML"))


# ---------------------------------------------------------------------------
# CL encoding of a lens-variant: enumerate all two-step paths
# ---------------------------------------------------------------------------

def encode_variant_to_cl(scope: Sequence[int], table: np.ndarray
                         ) -> set[tuple[int, int, int]]:
    """Encode a lens variant (table restricted to scope x scope) as the
    set of two-step paths {(a, b, table[a, b]) : a, b in scope}.

    This is the variant's CL fingerprint -- the universal substrate (CL)
    holds all (a, b, c) potential triples; each variant selects a subset.
    """
    return {(int(a), int(b), int(table[int(a), int(b)]))
            for a in scope for b in scope}


def variant_overlap(scope_a: Sequence[int], table_a: np.ndarray,
                    scope_b: Sequence[int], table_b: np.ndarray
                    ) -> dict[str, int]:
    """Compute set-overlap between two variants' CL-encodings."""
    A = encode_variant_to_cl(scope_a, table_a)
    B = encode_variant_to_cl(scope_b, table_b)
    return {
        "A_size": len(A),
        "B_size": len(B),
        "intersection": len(A & B),
        "A_only": len(A - B),
        "B_only": len(B - A),
        "union": len(A | B),
        "jaccard": len(A & B) / len(A | B) if (A | B) else 0.0,
    }


# ---------------------------------------------------------------------------
# Crossing-Lemma census: which 3-input paths cross under CL?
# ---------------------------------------------------------------------------

def crossing_census(table: np.ndarray = CL) -> dict[str, int]:
    """For all (a, b, c) in N^3, count crossings under left vs right
    bracketing. The crossing rate equals the non-associativity rate."""
    cross = 0
    total = 0
    for a in range(N):
        for b in range(N):
            for c in range(N):
                lhs = int(table[int(table[a, b]), c])
                rhs = int(table[a, int(table[b, c])])
                total += 1
                if lhs != rhs:
                    cross += 1
    return {"n_triples": total, "n_crossings": cross,
            "rate": cross / total}


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _demo():
    print("=" * 60)
    print("Path-walk demonstration -- 'the path IS the information'")
    print("=" * 60)
    print()

    # A simple path through CL
    p = walk_left([1, 4, 9], CL, "CL")
    print(f"  path through CL with inputs (1, 4, 9), LEFT bracketing:")
    print(f"    {p}  (endpoint = {p.endpoint})")
    print()

    # Same inputs, different bracketing
    pp = path_pair([1, 4, 9], CL, "CL")
    print(f"  path_pair on (1, 4, 9):")
    print(f"    LEFT:  {pp.left}")
    print(f"    RIGHT: {pp.right}")
    print(f"    crosses (Crossing Lemma): {pp.crosses}")
    if pp.crosses:
        print(f"    signature: {pp.crossing_signature}")
    print()

    # Lens-traced same inputs
    lt = lens_trace([1, 4, 9])
    print(f"  lens_trace on (1, 4, 9):")
    print(f"    TSML trail: {lt.tsml_path.trail}  endpoint={lt.tsml_path.endpoint}")
    print(f"    BHML trail: {lt.bhml_path.trail}  endpoint={lt.bhml_path.endpoint}")
    print(f"    lens diverges: {lt.lens_diverges}")
    if lt.lens_diverges:
        print(f"    first divergence at step: {lt.divergence_step}")
    print()

    # Crossing census on CL
    c = crossing_census(CL)
    print(f"  Crossing census on CL ({c['n_triples']} triples):")
    print(f"    crossings = {c['n_crossings']}")
    print(f"    rate = {100*c['rate']:.1f}%  (= non-associativity rate)")
    print()

    # Two variants' CL-encodings (4-core under TSML vs BHML)
    overlap = variant_overlap([0, 7, 8, 9], TSML, [0, 7, 8, 9], BHML)
    print(f"  4-core encoding overlap (TSML vs BHML restricted to {{0,7,8,9}}):")
    print(f"    TSML_4 has {overlap['A_size']} two-step paths")
    print(f"    BHML_4 has {overlap['B_size']} two-step paths")
    print(f"    intersection (where lenses agree): {overlap['intersection']}")
    print(f"    union: {overlap['union']}")
    print(f"    Jaccard: {overlap['jaccard']:.3f}")


if __name__ == "__main__":
    _demo()
