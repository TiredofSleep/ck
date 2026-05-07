"""V2 -- Generator-triple closure under BHML's four rules.

Acceptance:
    1. BHML table is constructed from rules (not hardcoded).
    2. BHML[7, 7] = 8 (fuse axiom holds directly on the diagonal).
    3. {1, 4, 9} closes BHML to all of Z/10Z in exactly 2 steps.
       (Trinity = minimum cardinality for algebraic genesis.)

Run: python -m foundations.verifications.v2_bhml_closure
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from foundations.generators import (  # noqa: E402
    BEING, DOING, BECOMING, UNION_BEING_DOING_BECOMING, TRINITY_GENESIS,
    closure,
)
from foundations.lenses import build_BHML, fuse_axiom_holds_on  # noqa: E402
from foundations.substrate import N  # noqa: E402


def main() -> int:
    print("=" * 60)
    print("V2 -- BHML closure under 4 rules (foundations.lenses)")
    print("=" * 60)

    B = build_BHML()

    # Fuse axiom check
    fuse_ok = fuse_axiom_holds_on(B)
    print(f"  fuse axiom (BHML[7, 7] = 8): {fuse_ok}  (expected True)")
    assert fuse_ok, "fuse axiom failed on BHML"

    # Generator triple closures
    seeds = {
        "BEING               {0, 1, 2}":     BEING,
        "DOING               {0, 7, 1}":     DOING,
        "BECOMING            {1, 2, 3}":     BECOMING,
        "UNION  {0, 1, 2, 3, 7}":            UNION_BEING_DOING_BECOMING,
        "TRINITY_GENESIS     {1, 4, 9}":     TRINITY_GENESIS,
    }

    fail = False
    for name, seed in seeds.items():
        closed, steps = closure(seed, B)
        print(f"  {name:35s} -> {sorted(closed)}  ({steps} steps)")

    # Critical claim: {1, 4, 9} closes BHML to all of Z/10Z in 2 steps
    closed, steps = closure(TRINITY_GENESIS, B)
    if closed != set(range(N)):
        print(f"  FAIL: TRINITY_GENESIS did not close to all of Z/10Z: {sorted(closed)}")
        fail = True
    elif steps != 2:
        print(f"  FAIL: TRINITY_GENESIS closed in {steps} steps (expected 2)")
        fail = True
    else:
        print(f"\n  PASS: TRINITY_GENESIS closes BHML to Z/10Z in {steps} steps "
              f"(minimum genesis cardinality)")

    print("=" * 60)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
