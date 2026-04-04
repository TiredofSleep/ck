"""
dbc27.py — DBC27 routing key for CK memory lattice retrieval

DBC27 provides a compact canonical routing key that fractal-indexes
memory without opening all of it at once. The key encodes:

    DBC27_primary :: CL_fused_secondary :: lens_suffix

Format: "{dbc27}::{cl_fused}::{lens}"

Components:
    dbc27         — 27-symbol base encoding of the dominant D2 force vector
    cl_fused      — CL table fusion of (operator, secondary_op) → result
    lens_suffix   — 'S' for STRUCTURE, 'F' for FLOW

The routing key is the index that determines which neighborhood of
the memory lattice to open. Different keys open different sub-lattices.
Retrieval never opens all of memory — only the local neighborhood.

© 2026 Brayden Sanders / 7Site LLC
"""

from __future__ import annotations
import math
from typing import Optional

# DBC27 alphabet — 27 symbols covering the D2 5D force space
# Partitioned into 3 triadic groups (Being × 3, Doing × 3, Becoming × 3) × 3 layers
DBC27_ALPHABET = (
    'A B C D E F G H I '   # aperture-dominant
    'J K L M N O P Q R '   # pressure-dominant
    'S T U V W X Y Z _'    # depth/binding/continuity mixed
).split()

# CL composition table (10×10) — truncated to composition kernel
# Full table lives in ck_sim engine; this is the routing kernel
CL_TABLE = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9,0],
    [2,3,4,5,6,7,8,9,0,1],
    [3,4,5,6,7,8,9,0,1,2],
    [4,5,6,7,8,9,0,1,2,3],
    [5,6,7,8,9,0,1,2,3,4],
    [6,7,8,9,0,1,2,3,4,5],
    [7,8,9,0,1,2,3,4,5,6],
    [8,9,0,1,2,3,4,5,6,7],
    [9,0,1,2,3,4,5,6,7,8],
]


def _force_to_dbc27(force_vector: list[float]) -> str:
    """Map a 5D force vector to a DBC27 symbol.

    Force vector: [aperture, pressure, depth, binding, continuity]
    All values in [0, 1].

    Strategy:
    - Find dominant dimension (argmax of abs values)
    - Within that dimension, quantize to 3 tiers (low/mid/high)
    - Map to one of 27 symbols

    Returns a single character from DBC27_ALPHABET.
    """
    if not force_vector or len(force_vector) != 5:
        return '_'

    # Normalize to [0,1]
    v = [abs(x) for x in force_vector]
    total = sum(v) or 1.0
    v = [x / total for x in v]

    # Dominant dimension
    dom = max(range(5), key=lambda i: v[i])

    # Tier within dominant dimension: low (0-0.33), mid (0.33-0.67), high (0.67-1)
    val = v[dom]
    if val < 0.33:
        tier = 0
    elif val < 0.67:
        tier = 1
    else:
        tier = 2

    # Map to DBC27 index: dim(0..4) × 3 + tier ... but we only have 27 symbols
    # Use (dom × 3 + tier) mod 27
    idx = (dom * 3 + tier) % 27
    return DBC27_ALPHABET[idx]


def _cl_fuse(op: int, secondary_op: int) -> str:
    """Fuse two operators via CL table into a routing suffix."""
    op = max(0, min(9, int(op)))
    secondary_op = max(0, min(9, int(secondary_op)))
    result = CL_TABLE[op][secondary_op]
    return str(result)


def build_key(
    force_vector: list[float],
    operator: int,
    secondary_op: int,
    lens: str,
) -> str:
    """Build a DBC27 routing key.

    Args:
        force_vector:  5D force [aperture, pressure, depth, binding, continuity]
        operator:      dominant CK operator (0-9)
        secondary_op:  secondary operator from CL chain (0-9)
        lens:          'STRUCTURE' or 'FLOW'

    Returns:
        routing key string: "X::n::S" or "X::n::F"
    """
    dbc_sym = _force_to_dbc27(force_vector)
    cl_fused = _cl_fuse(operator, secondary_op)
    lens_suffix = 'S' if lens == 'STRUCTURE' else 'F'
    return f"{dbc_sym}::{cl_fused}::{lens_suffix}"


def key_neighborhood(key: str, radius: int = 1) -> list[str]:
    """Return the local neighborhood of keys within radius steps.

    This determines which sub-lattices to open during retrieval.
    radius=0 → exact key only
    radius=1 → key + adjacent CL compositions
    radius=2 → extends to second-order neighbors (opens wider lattice)

    Retrieval law enforces radius=1 by default; only escalates on miss.
    """
    parts = key.split('::')
    if len(parts) != 3:
        return [key]

    dbc_sym, cl_fused, lens_suffix = parts
    neighbors = [key]

    try:
        cl_val = int(cl_fused)
    except ValueError:
        return [key]

    if radius >= 1:
        # Adjacent CL values (±1 mod 10)
        for delta in [-1, 1]:
            adj_cl = (cl_val + delta) % 10
            neighbors.append(f"{dbc_sym}::{adj_cl}::{lens_suffix}")
        # Cross-lens neighbor (retrieval sometimes needs both lenses)
        alt_lens = 'F' if lens_suffix == 'S' else 'S'
        neighbors.append(f"{dbc_sym}::{cl_fused}::{alt_lens}")

    if radius >= 2:
        # Extend to adjacent DBC27 symbols
        if dbc_sym in DBC27_ALPHABET:
            idx = DBC27_ALPHABET.index(dbc_sym)
            for delta in [-1, 1]:
                adj_idx = (idx + delta) % 27
                adj_sym = DBC27_ALPHABET[adj_idx]
                neighbors.append(f"{adj_sym}::{cl_fused}::{lens_suffix}")

    return list(dict.fromkeys(neighbors))  # deduplicated, ordered


def key_from_atom(atom) -> str:
    """Convenience: build routing key directly from an Atom."""
    from .event_schema import Atom
    secondary_op = (atom.operator + 1) % 10  # simple default
    return build_key(
        force_vector=atom.force_vector,
        operator=atom.operator,
        secondary_op=secondary_op,
        lens=atom.lens,
    )
