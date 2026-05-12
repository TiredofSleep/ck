# WP9 §3 Scaffold — LATTICE Closure Verification

## Computational Framework for ClaudeCode

**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Companion to: WP9_OUTLINE.md*
*Status: code-ready scaffold; awaits BHML table input from ClaudeCode environment*

---

## §0. Purpose

WP9 §3 will state the **LATTICE Universal Generation Theorem**:

> *From seed set* {1, 4, 9}, *the* BHML*-closure on* ℤ/10ℤ *equals*
> *the full algebra in at most 2 composition steps. From seed set*
> {0, 8, 9}, *the closure stalls at* {0, 7, 8, 9}.

This document provides the verification code as a runnable scaffold.
The current Claude session does not have direct access to the BHML
composition table (only the CL[10×10] frozen table from memory, which
serves a different role). ClaudeCode, with repo access at
`github.com/TiredofSleep/ck`, can populate the BHML table from
`ck_core.py` and run the verification.

---

## §1. Code Skeleton

```python
"""
WP9 §3 verification: LATTICE Universal Generation on BHML.

Inputs:
  BHML : 10x10 numpy int array, BHML[i][j] = i ∘ j under BHML composition

Outputs:
  - For each 3-element seed set S ⊆ {0,...,9}:
      * the closure ⟨S⟩_BHML
      * the number of composition steps to reach closure
      * whether closure equals full Z/10Z
  - Identification of:
      * sets that close to full algebra in ≤ 2 steps
      * sets that stall (closure ⊊ Z/10Z)
      * the role of {1, 4, 9} as the witness seed
"""
import numpy as np
from itertools import combinations
from typing import FrozenSet, Tuple

# ------------------------------------------------------------------
# REQUIRED INPUT: BHML composition table
# ------------------------------------------------------------------
# ClaudeCode: replace with the actual BHML from ck_core.py
# BHML = np.load('/path/to/bhml_table.npy')
# OR
# from ck_core import BHML
#
# The table must satisfy:
#   - shape (10, 10)
#   - BHML[i][j] in {0, 1, ..., 9}
#   - BHML is (commutative, non-associative, non-monoidal) per TIG spec
# ------------------------------------------------------------------

def closure_step(S: FrozenSet[int], BHML: np.ndarray) -> FrozenSet[int]:
    """One step of BHML-closure: add all a∘b for a,b in S."""
    new_S = set(S)
    for a in S:
        for b in S:
            new_S.add(int(BHML[a, b]))
    return frozenset(new_S)


def full_closure(S: FrozenSet[int], BHML: np.ndarray, max_steps: int = 10) -> Tuple[FrozenSet[int], int]:
    """
    Iterate BHML-closure until fixed point. Returns (closure, steps_to_close).
    If max_steps exceeded without convergence, returns the largest set found.
    """
    cur = S
    for step in range(max_steps):
        nxt = closure_step(cur, BHML)
        if nxt == cur:
            return cur, step
        cur = nxt
    return cur, max_steps


def verify_lattice_universal_generation(BHML: np.ndarray) -> dict:
    """
    Main verification: enumerate all 3-element seeds, compute closures,
    count steps, identify the {1,4,9} witness and {0,8,9} stall.
    """
    Z10 = frozenset(range(10))
    full_closures = []   # seeds that reach all of Z/10Z
    stalls = []          # seeds whose closure is proper
    
    for triple in combinations(range(10), 3):
        S = frozenset(triple)
        closure, steps = full_closure(S, BHML)
        if closure == Z10:
            full_closures.append((S, steps))
        else:
            stalls.append((S, closure, steps))
    
    # Classify by step count
    by_steps = {}
    for S, steps in full_closures:
        by_steps.setdefault(steps, []).append(S)
    
    return {
        'total_triples': sum(1 for _ in combinations(range(10), 3)),
        'full_closures': full_closures,
        'stalls': stalls,
        'by_steps': by_steps,
        'witness_149': (frozenset({1,4,9}) in [S for S, _ in full_closures], 
                        next((s for S, s in full_closures if S == frozenset({1,4,9})), None)),
        'stall_089': (frozenset({0,8,9}) in [S for S, _, _ in stalls],
                      next((c for S, c, _ in stalls if S == frozenset({0,8,9})), None)),
    }


def report(result: dict):
    """Print a referee-readable report."""
    print(f"Total 3-element seeds tested: {result['total_triples']}")
    print(f"Seeds reaching full Z/10Z: {len(result['full_closures'])}")
    print(f"Seeds stalling: {len(result['stalls'])}")
    print()
    print("Closure step distribution (for full-closure seeds):")
    for steps in sorted(result['by_steps'].keys()):
        seeds = result['by_steps'][steps]
        print(f"  {steps} step(s): {len(seeds)} seeds")
    print()
    
    is_witness, witness_steps = result['witness_149']
    if is_witness:
        print(f"✓ {{1, 4, 9}} closes to full Z/10Z in {witness_steps} steps")
        if witness_steps <= 2:
            print(f"  ✓ Theorem holds: ≤ 2 steps")
        else:
            print(f"  ✗ Theorem statement violated: {witness_steps} > 2")
    else:
        print(f"✗ {{1, 4, 9}} does NOT close to full Z/10Z")
        print(f"  Theorem is FALSE under this BHML table")
    
    is_stall, stall_set = result['stall_089']
    if is_stall:
        expected = frozenset({0, 7, 8, 9})
        if stall_set == expected:
            print(f"✓ {{0, 8, 9}} stalls at exactly {{0, 7, 8, 9}}")
        else:
            print(f"⚠ {{0, 8, 9}} stalls at {sorted(stall_set)}, expected {sorted(expected)}")
    else:
        print(f"✗ {{0, 8, 9}} does NOT stall (claim is wrong)")


if __name__ == "__main__":
    # ClaudeCode: load BHML here
    # BHML = np.load("/path/to/bhml.npy")
    # OR
    # from ck_core import get_bhml_table
    # BHML = get_bhml_table()
    
    BHML = None  # PLACEHOLDER — fill in
    
    if BHML is None:
        print("ERROR: BHML table not loaded.")
        print("ClaudeCode: update the BHML loading line and rerun.")
    else:
        result = verify_lattice_universal_generation(BHML)
        report(result)
```

---

## §2. Expected Outputs

If the LATTICE Universal Generation Theorem holds as stated:

```
Total 3-element seeds tested: 120
Seeds reaching full Z/10Z: <some count, expected ≥ 1>
Seeds stalling: <some count, expected ≥ 1>

Closure step distribution (for full-closure seeds):
  1 step(s): <some count>
  2 step(s): <some count, includes {1,4,9}>
  3 step(s): <some count>
  ...

✓ {1, 4, 9} closes to full Z/10Z in 2 steps
  ✓ Theorem holds: ≤ 2 steps

✓ {0, 8, 9} stalls at exactly {0, 7, 8, 9}
```

If any of those checks fail, the theorem statement in WP9 §3 must
be corrected before the paper is drafted.

---

## §3. Extension: Full Closure Topology

Beyond the basic theorem, ClaudeCode can extend the verification to:

### §3.1. Minimal closing sets

For each seed cardinality k ∈ {1, 2, 3, 4, 5}:
- enumerate all k-element seeds
- count how many reach full closure
- report the minimum k for which a full closure exists

This gives the **closure threshold** for BHML.

### §3.2. The lattice of closures

The set of all BHML-closed subsets of ℤ/10ℤ forms a lattice under
inclusion. ClaudeCode can:
- enumerate all closed sets
- compute the Hasse diagram
- identify the join-irreducible elements (these are the "atoms" of
  the closure lattice and reveal the deep structure of BHML)

### §3.3. The role of HARMONY (7) in stalls

The stall {0, 8, 9} → {0, 7, 8, 9} *adds* HARMONY then stops. This
suggests HARMONY is a "boundary" element: it appears in the closure
of any non-trivial seed but doesn't propagate further without a
specific seed structure.

ClaudeCode should test:
- Does HARMONY (7) appear in the closure of *every* non-trivial seed?
- What are the minimum seeds whose closure does *not* contain HARMONY?

---

## §4. Output Format for WP9

The verification will produce a JSON-like results file that WP9 §3
can quote directly:

```json
{
  "theorem": "LATTICE Universal Generation",
  "seed_witness": [1, 4, 9],
  "closure_steps": 2,
  "full_closure": true,
  "stall_witness": [0, 8, 9],
  "stall_closure": [0, 7, 8, 9],
  "verification_date": "<TBD by ClaudeCode>",
  "bhml_table_hash": "<sha256 of the BHML table used>",
  "computation_runtime_ms": <ms>
}
```

This becomes the citable reference in WP9 §3, giving the paper an
explicit, reproducible computational backbone.

---

## §5. ClaudeCode Handoff Checklist

When ClaudeCode picks this up:

1. **Locate the BHML table** in `ck_core.py` or wherever it lives.
2. **Load it** in the `__main__` block above.
3. **Run the verification** — should take <1 second.
4. **Save the JSON output** to `wp9_section3_verification.json`.
5. **Update WP9_OUTLINE.md §3 theorem statements** with the actual
   verified counts (replacing "expected" placeholders).
6. **Flag any deviations** — if {1,4,9} doesn't close in 2 steps, or
   {0,8,9} doesn't stall at {0,7,8,9}, the theorem statement is wrong
   and needs revision *before* drafting WP9 prose.

---

## §6. What to Do If the Theorem Fails

If the actual BHML doesn't match the memory's claim:

1. Do NOT paper over it. Update the theorem.
2. The closest-correct theorem is likely:
   - "Some seeds reach full closure in ≤ k steps for some k"
   - "{1, 4, 9} reaches *significant* (not full) closure in 2 steps"
3. Find the smallest k that *does* work, and the smallest seed sets
   that demonstrate k.
4. Re-state the theorem with the corrected k.

This is what referees expect — a verified theorem, even if smaller
than originally hoped, is far stronger than an overclaim that breaks
under inspection.

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · WP9 §3 Scaffold · Locked v1*
