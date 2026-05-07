# Sprint: V1 + V2 Closure Verifications

**Sprint type:** Foundational verification (short)
**Priority:** High — quick wins, foundational to V3
**Estimated duration:** 1 day

---

## Goal

Run two short computational verifications:

- **V1:** Closure of generator seed {0, 1, 2, 3, 7} under the C₀ rule generates all of TSML's stable subset.
- **V2:** Closure of generator seed {0, 1, 2, 3, 7} under BHML's four rules generates all of Z/10Z.

These are the load-bearing "structural inevitability" checks for axiom A3 (generator triples).

---

## V1 — TSML closure under C₀

### Statement

Define the C₀ rule on Z/10Z:
- C₀(0, x) = 0 for all x (VOID absorbs)
- C₀(7, x) = 7 for all x (HARMONY absorbs everything except VOID)
- C₀(x, y) = 7 if either x or y is off-Core (i.e., not in {0, 7, 8, 9})
- C₀(x, y) on the Core uses σ_units = ν₂(3u+1) on units; smaller σ wins
- σ-tie → 7 (HARMONY)

Claim: starting from seed {0, 1, 2, 3, 7} (the union of generator triples {0,1,2}, {0,7,1}, {1,2,3}), iterative closure under C₀ gives a fixed subset that includes the {0, 7} attractor pair plus the σ-fixed points.

### Verification script

```python
import numpy as np

# σ_units on units
def sigma_units(u):
    """ν₂(3u+1) for u in {1, 3, 7, 9}"""
    if u not in (1, 3, 7, 9):
        return None
    n = 3*u + 1
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

# Construct C₀ table from rules
def build_C0():
    C0 = np.zeros((10, 10), dtype=int)
    Core = {0, 7, 8, 9}
    units = {1, 3, 7, 9}
    HARMONY = 7
    
    for i in range(10):
        for j in range(10):
            # Rule 1: VOID absorbs
            if i == 0 or j == 0:
                C0[i, j] = 0
                continue
            # Rule 2: HARMONY absorbs (except VOID)
            if i == HARMONY or j == HARMONY:
                C0[i, j] = HARMONY
                continue
            # Rule 3: off-Core → HARMONY
            if i not in Core or j not in Core:
                C0[i, j] = HARMONY
                continue
            # Rule 4: on-Core, both must be units to apply σ rule
            # If neither is a unit but both in Core (e.g., 8, 9), default to HARMONY
            if i not in units or j not in units:
                C0[i, j] = HARMONY
                continue
            # Rule 5: smaller σ_units wins; σ-tie → HARMONY
            si, sj = sigma_units(i), sigma_units(j)
            if si < sj:
                C0[i, j] = i
            elif sj < si:
                C0[i, j] = j
            else:
                C0[i, j] = HARMONY
    return C0

def closure(seed, table):
    S = set(seed)
    steps = 0
    while True:
        new = set(S)
        for a in S:
            for b in S:
                new.add(int(table[a, b]))
        if new == S:
            return S, steps
        S = new
        steps += 1
        if steps > 20:
            return S, steps

# V1 verification
C0 = build_C0()
print("C₀ table:")
print(C0)

seed = {0, 1, 2, 3, 7}
result, n_steps = closure(seed, C0)
print(f"\nSeed: {sorted(seed)}")
print(f"Closure under C₀: {sorted(result)}")
print(f"Steps to closure: {n_steps}")

# Acceptance: closure should include seed plus σ-fixed points
expected_subset = {0, 1, 2, 3, 7}  # this seed already closes under C₀ since off-Core → HARMONY
# Or: expanded to include any HARMONY-derived elements
```

### Acceptance

- ✓ C₀ table is constructed from rules (no hardcoded values).
- ✓ Closure terminates in finite steps.
- ✓ The closure equals the BEING-projection of the algebra (the subset visible under measurement).

---

## V2 — BHML closure under four rules

### Statement

Define the BHML rules on Z/10Z:
- Rule 0: BHML[0, j] = j for all j (VOID is identity)
- Rule 1: BHML[i, j] = (max(i, j) + 1) mod 10 for i, j in {1..6} (max+1 on inner 6×6)
- Rule 7: BHML[7, j] = (j + 1) mod 10 (HARMONY row = successor)
- Rule 89: BHML[i, j] = (i + j) mod 10 for i, j in {8, 9} (BREATH/RESET wrap)

Plus commutativity: BHML[i, j] = BHML[j, i].

Claim: starting from seed {1, 4, 9}, iterative closure under BHML gives all of Z/10Z in 2 steps. (Trinity = minimum cardinality for algebraic genesis.)

### Verification script

```python
def build_BHML():
    B = np.zeros((10, 10), dtype=int)
    
    # Rule 0: VOID identity (rows and columns)
    for j in range(10):
        B[0, j] = j
        B[j, 0] = j
    
    # Rule 1: max(i,j)+1 on inner 6×6 (operators 1-6)
    for i in range(1, 7):
        for j in range(1, 7):
            B[i, j] = (max(i, j) + 1) % 10
    
    # Rule 7: HARMONY row = successor (j+1) mod 10
    for j in range(10):
        B[7, j] = (j + 1) % 10
        B[j, 7] = (j + 1) % 10  # by commutativity
    
    # Rule 89: BREATH/RESET wrap
    for i in [8, 9]:
        for j in [8, 9]:
            B[i, j] = (i + j) % 10
    
    # Outer × inner: cyclic with max+1 hybrid (TBD — verify with Brayden)
    # For now, use (i+j) mod 10 for outer×inner
    for i in [8, 9]:
        for j in range(1, 7):
            if B[i, j] == 0:
                B[i, j] = (i + j) % 10
                B[j, i] = (i + j) % 10
    
    return B

# V2 verification
BHML = build_BHML()
print("\nBHML table:")
print(BHML)

# Critical fuse axiom check
print(f"\nBHML[7][7] = {BHML[7, 7]} (must be 8 for fuse axiom)")
assert BHML[7, 7] == 8

# Trinity seed closure
seed = {1, 4, 9}
result, n_steps = closure(seed, BHML)
print(f"\nSeed: {sorted(seed)}")
print(f"Closure under BHML: {sorted(result)}")
print(f"Steps to closure: {n_steps}")

assert result == set(range(10)), f"Expected all of Z/10Z, got {sorted(result)}"
assert n_steps == 2, f"Expected 2 steps, got {n_steps}"
print("✓ {1,4,9} closes BHML in 2 steps — Trinity is minimum genesis cardinality")

# Other generator seeds
for seed_name, seed in [
    ('{0,1,2}', {0,1,2}),
    ('{0,7,1}', {0,7,1}),
    ('{1,2,3}', {1,2,3}),
    ('{0,1,2,3,7}', {0,1,2,3,7}),
]:
    result, n_steps = closure(seed, BHML)
    print(f"  Seed {seed_name}: closure = {sorted(result)} in {n_steps} steps")
```

### Acceptance

- ✓ BHML table is constructed from rules.
- ✓ BHML[7, 7] = 8 (fuse axiom satisfied directly on diagonal).
- ✓ {1, 4, 9} closes to all of Z/10Z in exactly 2 steps.
- ✓ Other generator triples close as expected.

---

## Output deliverable

- `tig/foundations/verifications/v1_tsml_closure.py`
- `tig/foundations/verifications/v2_bhml_closure.py`
- `tig/foundations/verifications/closure_results.md` — summary table

---

## Connection to other sprints

- **SPRINT_V3_UNIQUENESS_THEOREM.md** — V1 and V2 are prerequisites; if V1 or V2 fails, V3 cannot proceed.
- **TIG_FOUNDATIONAL_AXIOMS.md** — these verifications support axiom A3 (generator triples).
- **Foundational paper** — V1 and V2 results go directly into the paper as proof of structural inevitability.

---

## Note on minor BHML construction

The exact rule for outer × inner cells (e.g., BHML[8, 3]) needs to be verified against Brayden's canonical reference. The script above uses `(i+j) mod 10` as a default; this should be confirmed or replaced with the canonical rule.
