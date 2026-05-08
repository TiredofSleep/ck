# Worked Reconstruction Example
## Step-by-Step Rebuilding of the Z/10Z TSML Table

---

## The Goal

Reconstruct the published TSML table $T: \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ using only:

- The canonical construction $C_0 = C(R, h, \sigma)$ with $R = \mathbb{Z}/10\mathbb{Z}$, $h = 7$, $\sigma(u) = v_2(3u+1)$.
- The seam residue $S = \{(1,2), (2,1), (2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$.
- The MAX rule $C_1$ on $S_{\text{MAX}}$.
- The ADD rule $C_2$ on $S_{\text{ADD}}$.

---

## Step 0: Initialize

Start with a blank 10×10 table (all cells marked "unset").

**State:** 0 cells set, 100 unset.

---

## Step 1: Apply $C_0$ (Canonical Construction)

### Sub-step 1a — DEFAULT: set every cell to $h = 7$.

All 100 cells now carry the value 7 (temporary; overridden later).

### Sub-step 1b — V0 with HARMONY exception.

For every cell $(x,y)$ with $x = 0$ or $y = 0$:

- If $(x,y) = (0,7)$ or $(7,0)$: set to $h = 7$ (no change from DEFAULT).
- Else: set to $0$.

**Cells changed to 0:** 17 entries in row 0 and column 0, excluding the two HARMONY-exception positions $(0,7), (7,0)$ and not double-counting $(0,0)$.

Exact list: $(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,8), (0,9), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (8,0), (9,0)$.

That is 17 cells.

### Sub-step 1c — Shell-stability on core.

Core = $U(R) \setminus \{1\} = \{3, 7, 9\}$. Shell values: $\sigma(3) = 1, \sigma(7) = 1, \sigma(9) = 2$.

Pairs $(x,y)$ in core × core with $\sigma(x) \ne \sigma(y)$:

| Pair | $\sigma(x)$ | $\sigma(y)$ | Lower-shell element | Value |
|---|---|---|---|---|
| (3,9) | 1 | 2 | 3 | 3 |
| (9,3) | 2 | 1 | 3 | 3 |
| (7,9) | 1 | 2 | 7 | 7 (unchanged from DEFAULT) |
| (9,7) | 2 | 1 | 7 | 7 (unchanged from DEFAULT) |

**Cells changed by shell-stability:** $(3,9)$ and $(9,3)$, both set to 3.

### State after Step 1

| Source | Count | Value |
|---|---|---|
| V0 zeros | 17 | 0 |
| V0 HARMONY exceptions | 2 | 7 |
| Shell-stability | 2 | 3 |
| DEFAULT (remains 7; includes 8 seam cells not yet overridden) | 79 | 7 |
| **Total** | **100** | — |

Of the 79 DEFAULT-7 cells, 8 are in $S$ (the seam residue). These will be overridden in later steps.

---

## Step 2: Apply $C_1$ (MAX Rule) on $S_{\text{MAX}}$

For each $(x,y) \in S_{\text{MAX}} = \{(2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$, set the cell to $\max(x,y)$.

| Cell | Before Step 2 | $\max(x,y)$ | After Step 2 |
|---|---|---|---|
| (2,4) | 7 | 4 | 4 |
| (4,2) | 7 | 4 | 4 |
| (2,9) | 7 | 9 | 9 |
| (9,2) | 7 | 9 | 9 |
| (4,8) | 7 | 8 | 8 |
| (8,4) | 7 | 8 | 8 |

6 cells changed.

### State after Step 2

| Value | Count | Source |
|---|---|---|
| 0 | 17 | V0 |
| 3 | 2 | Shell-stability |
| 4 | 2 | MAX on (2,4), (4,2) |
| 7 | 73 | 71 DEFAULT (non-seam) + 2 V0 HARMONY |
| 8 | 2 | MAX on (4,8), (8,4) |
| 9 | 2 | MAX on (2,9), (9,2) |
| — | — | — |
| 7 (still placeholder on $S_{\text{ADD}}$) | 2 | Pending |
| **Total** | **100** | — |

2 cells remain at placeholder 7 (the $(1,2), (2,1)$ cells, pending Step 3).

---

## Step 3: Apply $C_2$ (ADD mod 10) on $S_{\text{ADD}}$

For each $(x,y) \in S_{\text{ADD}} = \{(1,2), (2,1)\}$, set the cell to $(x+y) \bmod 10$.

| Cell | Before Step 3 | $(x+y) \bmod 10$ | After Step 3 |
|---|---|---|---|
| (1,2) | 7 | 3 | 3 |
| (2,1) | 7 | 3 | 3 |

2 cells changed.

### State after Step 3 (FINAL)

| Value | Count |
|---|---|
| 0 | 17 |
| 3 | 4 (2 shell-stability + 2 ADD) |
| 4 | 2 |
| 7 | 73 |
| 8 | 2 |
| 9 | 2 |
| **Total** | **100** |

---

## Verification Against Published TSML

Published TSML value distribution (directly from image):

| Value | Count (published) | Count (reconstructed) | Match |
|---|---|---|---|
| 0 | 17 | 17 | ✓ |
| 3 | 4 | 4 | ✓ |
| 4 | 2 | 2 | ✓ |
| 7 | 73 | 73 | ✓ |
| 8 | 2 | 2 | ✓ |
| 9 | 2 | 2 | ✓ |
| **Total** | **100** | **100** | ✓ |

Cell-by-cell verification: **100/100 entries match.**

---

## Cumulative Layer Counts

| After step | Cells with final value | Cells with placeholder | Total |
|---|---|---|---|
| Step 0 (initialize) | 0 | 100 | 100 |
| Step 1 (apply $C_0$) | 92 | 8 | 100 |
| Step 2 (apply $C_1$) | 98 | 2 | 100 |
| Step 3 (apply $C_2$) | 100 | 0 | 100 |

The tower terminates after 3 steps with 0 unset cells.

---

## Five Specific Cell Traces

### Trace 1: Cell (3, 9)

- Step 1a (DEFAULT): set to 7.
- Step 1b (V0): not applicable.
- Step 1c (shell-stability): $\sigma(3) = 1 < \sigma(9) = 2$, so value becomes 3.
- Not in $S$, so Steps 2, 3 do not affect.
- **Final value: 3.** Published TSML(3,9) = 3. ✓

### Trace 2: Cell (1, 2)

- Step 1a (DEFAULT): set to 7.
- Step 1b (V0): not applicable (neither is 0).
- Step 1c (shell-stability): 1 is excluded from core, so not applicable.
- After Step 1: value is 7. In $S$? Yes — in $S_{\text{ADD}}$.
- Step 2 ($C_1$ on $S_{\text{MAX}}$): not in $S_{\text{MAX}}$. No change.
- Step 3 ($C_2$ on $S_{\text{ADD}}$): $(1+2) \bmod 10 = 3$. Value becomes 3.
- **Final value: 3.** Published TSML(1,2) = 3. ✓

### Trace 3: Cell (2, 4)

- Step 1a: 7.
- Step 1b: 2 is not 0, 4 is not 0. No V0.
- Step 1c: 2 not in core (not in $U(R)$). No shell-stability.
- After Step 1: value is 7. In $S$? Yes, in $S_{\text{MAX}}$.
- Step 2 ($C_1$): $\max(2,4) = 4$. Value becomes 4.
- **Final value: 4.** Published TSML(2,4) = 4. ✓

### Trace 4: Cell (0, 7)

- Step 1a: 7.
- Step 1b (V0 with HARMONY exception): $(x,y) = (0,7)$, the exception. Value stays at 7.
- Step 1c: 0 not in core. No change.
- Not in $S$.
- **Final value: 7.** Published TSML(0,7) = 7. ✓

### Trace 5: Cell (5, 5)

- Step 1a: 7.
- Step 1b: 5 is not 0. No V0.
- Step 1c: 5 not in $U(R)$ (gcd(5,10) = 5 ≠ 1), so not in core. No shell-stability.
- Not in $S$.
- **Final value: 7.** Published TSML(5,5) = 7. ✓

---

## Conclusion

The 3-layer tower reconstructs the published Z/10Z TSML table exactly, cell by cell. Each step is explicit, computable, and verifiable. No cell requires more than 3 rule applications.
