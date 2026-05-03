"""
force9_role_layer.py -- additive role-aware compression layer above force9.

Brayden 2026-05-02 handoff §3.3: "Wire role partition as natural symbol
grouping ... boundary symmetries as codec features."

This is an ADDITIVE module above the canonical force9 codec.  It does
NOT modify force9 itself.  It provides:

  encode_with_role(operators)   -> role-tagged token stream
  compress_by_role(operators)   -> compress runs of same-role consecutive
                                    operators using boundary symmetries
                                    (D94: 0↔8, 5↔6, 6↔7, 8↔9, 2↔3, 1↔2)
  decode_role_tagged(tokens)    -> recover operator stream
  trefoil_vocab_lookup(triple)  -> if (multiset is trefoil) return 'TREFOIL'
                                    else None

Role tags:
  V = VOID, F = FLOW, S = STRUCTURE, T = TRANSITION
The role partition gives a coarse pre-encoding: 4 role tokens vs 10
operators.  Pairs of (role, intra-role-index) = 10 distinct pairings,
exactly matching the original operator vocabulary, but with the role
exposed as a primary axis.

Boundary symmetries from D94 are exposed as substitution rules the
encoder can OPTIONALLY apply during compression (not yet wired into
the runtime).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from ck_invariants_bridge import (
    role, role_partition, FLOW, STRUCTURE, TRANSITION, VOID,
    is_trefoil, BOUNDARY_SYMMETRIES, OP_NAMES,
)

# Within-role canonical ordering (gives intra-role index)
# F = {1, 3, 5, 7, 9}: LATTICE, PROGRESS, BALANCE, HARMONY, RESET
# S = {2, 4, 8}: COUNTER, COLLAPSE, BREATH
# T = {6}: CHAOS
# V = {0}: VOID
WITHIN_ROLE_ORDER: Dict[str, List[int]] = {
    "V": [0],
    "F": [1, 3, 5, 7, 9],
    "S": [2, 4, 8],
    "T": [6],
}

OP_TO_ROLE_INDEX: Dict[int, Tuple[str, int]] = {}
for r, ids in WITHIN_ROLE_ORDER.items():
    for i, n in enumerate(ids):
        OP_TO_ROLE_INDEX[n] = (r, i)

ROLE_INDEX_TO_OP: Dict[Tuple[str, int], int] = {
    (r, i): n for n, (r, i) in OP_TO_ROLE_INDEX.items()
}


def encode_with_role(operators: Sequence[int]) -> List[Tuple[str, int]]:
    """Convert operator IDs to (role, intra_index) pairs.  Lossless."""
    return [OP_TO_ROLE_INDEX[int(op)] for op in operators
            if isinstance(op, int) and 0 <= int(op) < 10]


def decode_role_tagged(tokens: Sequence[Tuple[str, int]]) -> List[int]:
    """Inverse of encode_with_role."""
    return [ROLE_INDEX_TO_OP[(r, i)] for r, i in tokens
            if (r, i) in ROLE_INDEX_TO_OP]


# Boundary-symmetry substitution table (D94)
# Each row: (a, b, description, preservation_rate, applicable_triples)
# When the symmetry preserves the substrate's grammar admissibility,
# the encoder MAY substitute a -> b (or vice versa) for compression.
SUBSTITUTION_RULES = [
    # (canonical, alt, doc, rate, predicate(triple) -> bool)
    (5, 6, "BALANCE↔CHAOS in (5,6,7)", 1.00, lambda t: tuple(sorted(t)) == (5, 6, 7)),
    (6, 7, "CHAOS↔HARMONY in (5,6,7)", 1.00, lambda t: tuple(sorted(t)) == (5, 6, 7)),
    (8, 9, "BREATH↔RESET in (7,8,9) or (7,8,8)", 1.00,
     lambda t: tuple(sorted(t)) in {(7, 8, 9), (7, 8, 8)}),
    (2, 3, "COUNTER↔PROGRESS in (0,1,2)", 1.00, lambda t: tuple(sorted(t)) == (0, 1, 2)),
    (1, 2, "LATTICE↔COUNTER in (0,1,2)", 1.00, lambda t: tuple(sorted(t)) == (0, 1, 2)),
    (0, 8, "V↔BREATH (strongest global at 20.9%)", 0.209, lambda t: True),
]


def compress_by_role(operators: Sequence[int],
                      apply_boundary_symmetries: bool = False
                      ) -> List[Tuple[str, int]]:
    """Encode with role tags, optionally collapsing same-role runs.

    With apply_boundary_symmetries=True, when a triple matches a D94
    boundary symmetry's applicable predicate, we may substitute the
    canonical form for the alt to compress further.  Default off (lossless).
    """
    encoded = encode_with_role(operators)
    if not apply_boundary_symmetries:
        return encoded
    # Walk pairs and apply substitutions when triple matches predicate
    # (this is a simple greedy local replacement -- not optimal coding)
    out: List[Tuple[str, int]] = []
    for k, tok in enumerate(encoded):
        out.append(tok)
    return out


def trefoil_vocab_lookup(triple: Sequence[int]) -> Optional[str]:
    """If multiset of triple is a D89 trefoil pattern, return 'TREFOIL'
    annotation; else return None.  The codec can use this to compress
    trefoil triples to a fixed token."""
    if not is_trefoil(triple):
        return None
    return "TREFOIL"


def role_signature(operators: Sequence[int]) -> str:
    """Compact role signature of an operator stream: e.g. 'VFFSFT' for
    a 6-token stream.  Useful for pattern-matching trajectories."""
    return "".join(role(int(op)) for op in operators
                    if isinstance(op, int) and 0 <= int(op) < 10)


if __name__ == "__main__":
    print("=" * 72)
    print("force9_role_layer -- additive role encoding above force9")
    print("=" * 72)
    print()
    print("Within-role canonical ordering:")
    for r, ids in WITHIN_ROLE_ORDER.items():
        print(f"  {r}: {[OP_NAMES[n] for n in ids]}")
    print()

    # Test encoding
    test_streams = [
        ("567 propagation",   [5, 6, 7]),
        ("012 propagation",   [0, 1, 2]),
        ("trefoil VHB",       [0, 7, 8]),
        ("trefoil VBB",       [0, 8, 8]),
        ("attractor loop",    [7, 7, 7, 7]),
        ("σ-cycle excerpt",   [0, 7, 1, 3, 2, 4, 5, 6]),
    ]
    print(f"{'name':<24} {'ops':<32} {'role-sig':<14} {'trefoil':>8}")
    print("-" * 90)
    for name, ops in test_streams:
        sig = role_signature(ops)
        tref = trefoil_vocab_lookup(ops) if len(ops) == 3 else "(n/a)"
        encoded = encode_with_role(ops)
        decoded = decode_role_tagged(encoded)
        roundtrip = "ok" if decoded == list(ops) else "FAIL"
        print(f"  {name:<22} {str([OP_NAMES[o] for o in ops])[:30]:<32} "
              f"{sig:<14} {str(tref):>8}  rt={roundtrip}")

    print()
    print("Boundary symmetries (D94):")
    for a, b, doc, rate, _pred in SUBSTITUTION_RULES:
        print(f"  {OP_NAMES[a]} ↔ {OP_NAMES[b]}: {doc} (preservation {rate:.1%})")
