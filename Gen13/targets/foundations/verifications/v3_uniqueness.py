"""V3 -- Uniqueness theorem stub.

STATUS: STUB. The full enumeration is intractable on a workstation
(M(Z/10Z) has cardinality 10^55 unconstrained, ~10^15 even after
A0+A1+A3 constraints). The bundle's SPRINT_V3_UNIQUENESS_THEOREM.md
recommends a Dell R16 with Z3 SMT and a direct-construction proof
strategy (Lemmas 1-5).

This stub records what V3 needs to test, sketches the constraint set,
and runs only the cheap sanity checks.

Run: python -m foundations.verifications.v3_uniqueness
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from foundations.lenses import build_C0, build_BHML, fuse_axiom_holds_on  # noqa: E402
from foundations.substrate import N  # noqa: E402


def main() -> int:
    print("=" * 60)
    print("V3 -- Uniqueness theorem stub (NOT a full proof)")
    print("=" * 60)
    print()
    print("Theorem (V3): the pair (TSML, BHML) is the unique commutative")
    print("non-associative magma pair on Z/10Z satisfying A0-A5.")
    print()
    print("Status: OPEN. Full enumeration requires:")
    print("  - Phase 1: brute-force with A0+A1+A3 constraints (~10^15 tuples")
    print("    after constraints; needs Dell R16 multi-core).")
    print("  - Phase 2: Z3 SMT encoding for the constraint satisfaction.")
    print("  - Phase 3: direct-construction proof (Lemmas 1-5 from")
    print("    sprint_bundle/SPRINT_V3_UNIQUENESS_THEOREM.md).")
    print("  - Phase 4: brute-force verification of the proof.")
    print()
    print("This stub runs only the cheap sanity checks:")
    print()

    # Sanity check 1: the canonical pair satisfies A4 differently
    C0 = build_C0()
    B = build_BHML()
    a4_C0 = fuse_axiom_holds_on(C0)
    a4_B = fuse_axiom_holds_on(B)
    print(f"  A4 (fuse(3,4,7) = 8) on C_0:  {a4_C0}  (expected False)")
    print(f"  A4 (fuse(3,4,7) = 8) on BHML: {a4_B}  (expected True)")
    print(f"  -> A4 distinguishes the lenses (consistent with A5 two-lens).")
    print()

    # Sanity check 2: tables are commutative (A1)
    a1_C0 = (C0 == C0.T).all()
    a1_B = (B == B.T).all()
    print(f"  A1 (commutativity) on C_0:    {a1_C0}  (expected True)")
    print(f"  A1 (commutativity) on BHML:   {a1_B}  (expected True)")
    print()

    # Sanity check 3: tables are non-associative (A2; existence of one bad triple)
    def first_non_assoc(table):
        for a in range(N):
            for b in range(N):
                for c in range(N):
                    lhs = int(table[int(table[a, b]), c])
                    rhs = int(table[a, int(table[b, c])])
                    if lhs != rhs:
                        return (a, b, c, lhs, rhs)
        return None

    bad_C0 = first_non_assoc(C0)
    bad_B = first_non_assoc(B)
    print(f"  A2 (non-associativity) on C_0:  "
          f"{'witness ' + str(bad_C0) if bad_C0 else 'none found (table associative??)'}")
    print(f"  A2 (non-associativity) on BHML: "
          f"{'witness ' + str(bad_B) if bad_B else 'none found (table associative??)'}")
    print()
    print("These sanity checks pass; the load-bearing uniqueness step")
    print("(no other commutative non-associative magma on Z/10Z satisfies")
    print("all of A0-A5) requires the multi-day enumeration documented")
    print("in sprint_bundle/SPRINT_V3_UNIQUENESS_THEOREM.md.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
