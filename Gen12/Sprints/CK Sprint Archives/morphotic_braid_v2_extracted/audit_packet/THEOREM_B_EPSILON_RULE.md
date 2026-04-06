# THEOREM B: THE EXACT ε' RULE

## Statement

**Theorem B.** The parity component ε' of the hidden operator is determined
exactly by the following rule, depending only on y:

| y      | ε' rule              | Plain language              |
|--------|---------------------|-----------------------------|
| y = 0  | ε' = 0             | reset: parity always becomes 0 |
| y = 1  | ε' = 1             | set: parity always becomes 1   |
| y = 2  | ε' = 1 - ε         | flip: parity inverts            |
| y = 3  | ε' = ε             | preserve: parity unchanged      |
| y = 4  | ε' = ε             | preserve: parity unchanged      |

---

## Compact Formula

```
ε'(ε, y) = (1-ε)·𝟙[y ∈ {1,2}] + ε·𝟙[y ∈ {1,3,4}]
```

where 𝟙[P] = 1 if P is true, 0 otherwise.

---

## Verification on All 10 States

| ε | y | ε' (required) | ε' (formula) | Match |
|---|---|---------------|--------------|-------|
| 0 | 0 | 0             | 0            | ✓     |
| 0 | 1 | 1             | 1            | ✓     |
| 0 | 2 | 1             | 1            | ✓     |
| 0 | 3 | 0             | 0            | ✓     |
| 0 | 4 | 0             | 0            | ✓     |
| 1 | 0 | 0             | 0            | ✓     |
| 1 | 1 | 1             | 1            | ✓     |
| 1 | 2 | 0             | 0            | ✓     |
| 1 | 3 | 1             | 1            | ✓     |
| 1 | 4 | 1             | 1            | ✓     |

**All 10 states match exactly. ✓**

---

## Minimality

The formula uses only:
- The current parity ε
- Indicator functions on y ∈ {0,1,2,3,4}

No simpler representation exists because:
- y=0 and y=2 have different rules (reset vs flip) despite both being "even"
- y=1 and y=3 have different rules (set vs preserve) despite both being "odd"
- No single parity function of y captures the pattern

The four-case rule (reset, set, flip, preserve) is the minimal exact description.

---

## Interpretation

The y-coordinate controls what the ε-bit does at each step:

- **y=0** (anchor pre-image): parity is always cleared — this is the void/neutral state
- **y=1** (cycle entry adjacent): parity is always set — entering the active cycle
- **y=2** (cycle state): parity flips — alternating nature of the cycle traversal
- **y∈{3,4}** (fixed-point pre-images): parity is preserved — anchors maintain their parity

This is not an arbitrary rule. The reset/set/flip/preserve pattern
reflects the orbit-sector structure of the operator (Theorem E).
