# THEOREM A: THE HIDDEN PERMUTATION STRUCTURE

## The Hidden State Space

The hidden system operates on:

```
Z/2 × Z/5 = {(ε, y) : ε ∈ {0,1}, y ∈ {0,1,2,3,4}}
```

10 states total. Connected to the visible braid via the bijection:

```
x = 5ε + 6y (mod 10)
```

---

## Bijectivity Proof

The map φ: Z/2 × Z/5 → Z/10Z defined by φ(ε, y) = 5ε + 6y (mod 10)
is a bijection.

**Proof.** The image contains all 10 values:

| (ε, y) | x = 5ε + 6y (mod 10) |
|--------|----------------------|
| (0, 0) | 0                    |
| (0, 1) | 6                    |
| (0, 2) | 2                    |
| (0, 3) | 8                    |
| (0, 4) | 4                    |
| (1, 0) | 5                    |
| (1, 1) | 1                    |
| (1, 2) | 7                    |
| (1, 3) | 3                    |
| (1, 4) | 9                    |

All 10 values {0,...,9} appear exactly once. Since |domain| = |codomain| = 10,
the map is a bijection. □

**Consequence.** The hidden operator on (ε, y) and the visible permutation σ on Z/10Z
are exactly the same finite system in different coordinates.

---

## The Permutation Decomposition

**Theorem A.** The hidden operator F: Z/2 × Z/5 → Z/2 × Z/5 is a permutation
with the following cycle structure:

```
σ = (0,0)(0,3)(1,3)(1,4) · (1,1  1,2  0,1  1,0  0,4  0,2)
      ↑ four fixed points ↑     ↑______ one 6-cycle ______↑
```

In visible x-coordinates:
```
σ = (0)(3)(8)(9)(1  7  6  5  4  2)
```

---

## The Four Fixed Points

These states map to themselves under F:

| (ε, y) | x | σ(x) | Confirmed |
|--------|---|------|-----------|
| (0, 0) | 0 | 0    | ✓         |
| (0, 3) | 8 | 8    | ✓         |
| (1, 3) | 3 | 3    | ✓         |
| (1, 4) | 9 | 9    | ✓         |

---

## The 6-Cycle

The cycling states traverse:

```
(1,1) → (1,2) → (0,1) → (1,0) → (0,4) → (0,2) → (1,1)
  x=1     x=7     x=6     x=5     x=4     x=2     x=1
```

Cycle length: 6. Period: 6. ✓

---

## Complete Transition Table

| x | ε | y | x' | ε' | y' | type  |
|---|---|---|----|----|----|-------|
| 0 | 0 | 0 | 0  | 0  | 0  | fixed |
| 1 | 1 | 1 | 7  | 1  | 2  | cycle |
| 2 | 0 | 2 | 1  | 1  | 1  | cycle |
| 3 | 1 | 3 | 3  | 1  | 3  | fixed |
| 4 | 0 | 4 | 2  | 0  | 2  | cycle |
| 5 | 1 | 0 | 4  | 0  | 4  | cycle |
| 6 | 0 | 1 | 5  | 1  | 0  | cycle |
| 7 | 1 | 2 | 6  | 0  | 1  | cycle |
| 8 | 0 | 3 | 8  | 0  | 3  | fixed |
| 9 | 1 | 4 | 9  | 1  | 4  | fixed |

---

## Source of the Braid

The visible braid 0713245689 is the σ⁻¹-traversal of the 6-cycle
starting from entry point x=7, interleaved with the fixed points at their own indices.

See THEOREM_E_CONJUGACY.md for the conjugacy proof.
See THEOREM_D_UNIQUE_SPLIT_OPERATOR.md for the algebraic form.
