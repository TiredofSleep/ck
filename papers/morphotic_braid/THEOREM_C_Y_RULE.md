# THEOREM C: THE EXACT y' RULE

## Statement

**Theorem C.** The mod-5 component y' of the hidden operator is given exactly
by a piecewise polynomial in y, branching on ε:

```
         ⎧ P₀(y)   if ε = 0
y'(ε,y) = ⎨
         ⎩ P₁(y)   if ε = 1
```

where:

```
P₀(y) = 3y + 2y² + y³ + 4y⁴        (mod 5)
P₁(y) = 4 + 3y + 3y² + y³ + y⁴     (mod 5)
```

---

## Why Piecewise Polynomials Are Exact

Any function Z/5 → Z/5 has a unique polynomial representation of degree ≤ 4 (mod 5).
This follows from the fact that Z/5 is a field with 5 elements.

Since the y-map branches on ε, we have two Z/5 → Z/5 functions,
each with a unique polynomial form. Together they give the exact piecewise representation.

---

## Verification: ε = 0 branch

P₀(y) = 3y + 2y² + y³ + 4y⁴ (mod 5)

| y | y' (required) | P₀(y) (mod 5) | Match |
|---|---------------|---------------|-------|
| 0 | 0             | 0             | ✓     |
| 1 | 0             | 3+2+1+4=10≡0  | ✓     |
| 2 | 1             | 6+8+8+64≡1    | ✓     |
| 3 | 3             | 9+18+27+324≡3 | ✓     |
| 4 | 2             | 12+32+64+1024≡2| ✓    |

**ε=0 branch: all 5 values match. ✓**

---

## Verification: ε = 1 branch

P₁(y) = 4 + 3y + 3y² + y³ + y⁴ (mod 5)

| y | y' (required) | P₁(y) (mod 5) | Match |
|---|---------------|---------------|-------|
| 0 | 4             | 4             | ✓     |
| 1 | 2             | 4+3+3+1+1=12≡2| ✓     |
| 2 | 1             | 4+6+12+8+16≡1 | ✓     |
| 3 | 3             | 4+9+27+27+81≡3| ✓     |
| 4 | 4             | 4+12+48+64+256≡4| ✓   |

**ε=1 branch: all 5 values match. ✓**

---

## Combined Verification

The unified formula:

```
y'(ε, y) = (1-ε)·P₀(y) + ε·P₁(y)  (mod 5)
```

| ε | y | y' (required) | formula | Match |
|---|---|---------------|---------|-------|
| 0 | 0 | 0             | 0       | ✓     |
| 0 | 1 | 0             | 0       | ✓     |
| 0 | 2 | 1             | 1       | ✓     |
| 0 | 3 | 3             | 3       | ✓     |
| 0 | 4 | 2             | 2       | ✓     |
| 1 | 0 | 4             | 4       | ✓     |
| 1 | 1 | 2             | 2       | ✓     |
| 1 | 2 | 1             | 1       | ✓     |
| 1 | 3 | 3             | 3       | ✓     |
| 1 | 4 | 4             | 4       | ✓     |

**All 10 states match exactly. ✓**

---

## Family Analysis

- **Family A** (pure polynomial ay² + by + c + dε): 4 errors — fails
- **Family B** (with mixed terms): not needed — piecewise is exact
- **Family C** (parity-gated): not needed
- **Family D** (piecewise by ε): **EXACT** ← this is the answer

The piecewise polynomial is the minimal exact form.
No simpler unified polynomial exists.

---

## Note on Simplicity

While P₀ and P₁ appear complex as polynomials, by Theorem E they encode
a simple geometric operation: rotation k → k+1 on the 6-cycle, identity on anchors.

The polynomial complexity is the coordinate encoding cost, not the dynamical cost.
