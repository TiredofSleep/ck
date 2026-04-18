# Decomposition Table
## Full Layered Structure of Z/10Z TSML

---

## Primary Decomposition

| Layer | Rule | Domain | # Entries | Example |
|---|---|---|---|---|
| **C₀** | DEFAULT (→ h=7) + V0 (with HARMONY exception) + shell-stability | Complement of seam residue | **92** | (5,5) → 7, (0,3) → 0, (3,9) → 3 |
| **C₁** | MAX(a,b) | Seam residue edges where 1 ∉ {a,b} | **6** | (2,4) → 4, (2,9) → 9, (4,8) → 8 |
| **C₂** | (a + b) mod 10 | Seam residue edges where 1 ∈ {a,b} | **2** | (1,2) → 3, (2,1) → 3 |
| **Residual** | — | — | **0** | — |

**Total: 100 entries captured by 3 rules.**

---

## Priority Ordering

The rules are applied in order C₀ → C₁ → C₂, with each later rule overriding the earlier where applicable. Explicitly:

```
def T(a, b):
    v0 = C0(a, b)                            # default, V0, shell-stability
    if (a, b) in max_domain:                 # seam residue, 1 ∉ {a,b}
        return max(a, b)
    if (a, b) in add_domain:                 # seam residue, 1 ∈ {a,b}
        return (a + b) % 10
    return v0
```

---

## Domain Specification for Layers 1 and 2

**Seam residue (domain of C₁ ∪ C₂):** the 4 unordered pairs

{1,2}, {2,4}, {2,9}, {4,8}

These correspond to 8 ordered pairs (each unordered pair gives 2 ordered pairs).

**C₁ domain (MAX):** {2,4}, {2,9}, {4,8} → 6 ordered pairs

**C₂ domain (ADD):** {1,2} → 2 ordered pairs

---

## Residue Tree Re-examined

The seam residue edges form a tree on 5 vertices {1, 2, 4, 8, 9}:

```
              1               ← C₂ edge (ADD)
              |
              2 ────── 9      ← C₁ edge (MAX, to shell-2 admissible)
              |
              4               ← C₁ edge (MAX, to doubling chain)
              |
              8               ← C₁ edge (MAX, continuing doubling chain)
```

**Topology:** rooted tree at vertex 2, with 3 branches:
- Identity-branch: 2—1 (length 1)
- Admissible-branch: 2—9 (length 1)
- Doubling-branch: 2—4—8 (length 2)

**C₁ covers the admissible-branch and the doubling-branch (3 edges).**
**C₂ covers the identity-branch (1 edge).**

The type-class distinction from previous sprints maps cleanly to the rule distinction:

| Branch | Rule | Reason |
|---|---|---|
| Identity-branch | C₂ (ADD) | Identity is the additive zero's "companion"; additive structure dominates |
| Admissible-branch | C₁ (MAX) | Admissible element carries more "structural weight" than hub |
| Doubling-branch | C₁ (MAX) | Larger doubling element carries the chain structure |

---

## Values by Layer

**Distribution of values in TSML after decomposition:**

| Value | Entries | Source |
|---|---|---|
| 0 | 17 | C₀ (V0) |
| 3 | 2 + 2 = 4 | C₀ (shell-stability on {3,9}): 2 + C₂ (additive on {1,2}): 2 |
| 4 | 2 | C₁ (MAX on {2,4}) |
| 7 | 73 | C₀ (71 DEFAULT + 2 V0 HARMONY exceptions) |
| 8 | 2 | C₁ (MAX on {4,8}) |
| 9 | 2 | C₁ (MAX on {2,9}) |
| **Total** | **100** | — |

Note: the value 3 appears 4 times. Two instances come from C₀ shell-stability on pair (3,9), and two instances come from C₂ additive on pair (1,2). These are distinct sources of the same value — the value 3 is not a unique signal of any single layer.

---

## Rule Compactness Comparison

| Description | Size |
|---|---|
| **Flat description** (full 10×10 table) | 100 values |
| **Two-component description** (canonical + exception list) | ~35 data items (canonical params + 8 exception entries) |
| **Three-layer canonical tower** | ~15 data items (3 rule specs + 4 domain pairs + 1 attractor) |

The three-layer description is **most compact** — roughly 7× shorter than flat.

---

## Completeness Check

All 100 entries of TSML are accounted for:

- C₀ covers 92 entries (17 V0 zeros, 2 V0 HARMONY exceptions, 71 DEFAULT sevens, 2 shell-stability threes).
- C₁ covers 6 entries (2 each of: 4, 9, 8).
- C₂ covers 2 entries (both of value 3 from the {1,2} edge).

**Sum: 92 + 6 + 2 = 100.** ✓

**No entry is ambiguous.** C₀'s domain is disjoint from C₁'s and C₂'s by construction (the seam residue was defined as the complement of C₀'s matching set). C₁'s and C₂'s domains are disjoint by the identity-condition.

---

## Status

| Claim | Status |
|---|---|
| Decomposition captures 100/100 entries | **Exact** |
| 3 rules + priority ordering | **Exact** |
| Rule domains are disjoint | **Exact** |
| Seam residue tree has 4 edges, 5 vertices | **Exact** |
| Tree topology maps to rule distinction | **Exact** |
| Value 3 comes from two distinct sources | **Observed** |
| Three-layer description is most compact | **Exact** (~15 items vs 100) |
