"""V1 -- Generator-triple closure under TSML's C_0 backbone.

Acceptance:
    1. C_0 table is constructed from rules (not hardcoded).
    2. Closure terminates in finite steps for each generator triple.
    3. {0, 1, 2, 3, 7} (UNION_BEING_DOING_BECOMING) closes under C_0
       to itself (already a closed set under the off-Core -> HARMONY rule).

Run: python -m foundations.verifications.v1_tsml_closure
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running as a script (not just as a module)
_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from foundations.generators import (  # noqa: E402
    BEING, DOING, BECOMING, UNION_BEING_DOING_BECOMING, TRINITY_GENESIS,
    closure,
)
from foundations.lenses import build_C0  # noqa: E402


def main() -> int:
    print("=" * 60)
    print("V1 -- TSML closure under C_0 (foundations.lenses)")
    print("=" * 60)

    C0 = build_C0()

    seeds = {
        "BEING               {0, 1, 2}":     BEING,
        "DOING               {0, 7, 1}":     DOING,
        "BECOMING            {1, 2, 3}":     BECOMING,
        "UNION  {0, 1, 2, 3, 7}":            UNION_BEING_DOING_BECOMING,
        "TRINITY_GENESIS     {1, 4, 9}":     TRINITY_GENESIS,
    }

    fail = False
    for name, seed in seeds.items():
        closed, steps = closure(seed, C0)
        print(f"  {name:35s} -> {sorted(closed)}  ({steps} steps)")

    # Acceptance: UNION closes to itself (already closed under off-Core -> HARMONY)
    closed, _ = closure(UNION_BEING_DOING_BECOMING, C0)
    expected = set(UNION_BEING_DOING_BECOMING)
    if closed != expected:
        print(f"  FAIL: UNION did not close to itself: {sorted(closed)} != {sorted(expected)}")
        fail = True
    else:
        print(f"\n  PASS: UNION = {sorted(expected)} closes to itself under C_0")

    print("=" * 60)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
