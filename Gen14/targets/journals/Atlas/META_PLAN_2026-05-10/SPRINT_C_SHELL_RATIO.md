# Sprint C: The Shell Ratio (Locked)

## shell_72 / shell_44 = 18/11 is exact, not φ

**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Companion to: TIG_INTERNAL_MAP_v1.md (resolves §4.5 floating item #3)*

---

## §0. Result

> **Theorem (Shell Ratio).** *In TIG, with shells*
> *(22, 44, 72) = (Being-skeleton, Becoming-alive, Being-blur),*
>
> $$\frac{\text{shell}_{72}}{\text{shell}_{44}} = \frac{18}{11}$$
>
> *exactly, by TIG-canonical decomposition. The numerical proximity
> to* φ = 1.618 *is coincidental — 18/11 sits between Fibonacci
> convergents and is not asymptotic to any golden-ratio sequence.*

---

## §1. The Decomposition

Each shell count is the product of two TIG-canonical quantities:

| Shell | Decomposition | Reading |
|---|---|---|
| 22 | 2 · 11 | (parity) · (#bumps) |
| 44 | 4 · 11 | (#Hopf links) · (#bumps) = (corner-cycle order) · (#bumps) |
| 72 | 8 · 9 | (#active operators) · (RESET) |

**shell_44 / shell_22:**

$$\frac{4 \cdot 11}{2 \cdot 11} = \frac{4}{2} = 2 \quad\text{(exact doubling, locked)}$$

**shell_72 / shell_44:**

$$\frac{8 \cdot 9}{4 \cdot 11} = \frac{72}{44} = \frac{18}{11} \quad\text{(exact)}$$

The 11 cancels in shell_44/shell_22 (giving the clean doubling)
but does **not** cancel in shell_72/shell_44 (giving the 18/11 that
*looks* like φ). The φ-resemblance is an artifact of where 18/11
falls numerically, not of any golden-ratio recurrence.

---

## §2. Why 8 · 9 for shell_72

The "Being-blur" shell counts the active operators at the level of
RESET-cycle visibility:

- **8 active operators** = corners {1,3,7,9} + edges {2,4,6,8}
  (everything except VOID and BALANCE — i.e. everything that has
  multiplicative content under the Two-Cross structure)
- **9 = RESET** = the operator that closes the BHML cycle

Their product 8·9 = 72 is the count of (operator, RESET) pairs that
participate in the Being-blur shell — the layer where the harmony
attractor is visible but unresolved (not yet 73 = HARMONY one-step-
beyond).

This explains the previously-noted identity **harmony_n / shell_72 = 73/72**
in the Internal Map: HARMONY is one cell beyond the (8·9)-grid of
active-operator × RESET pairs.

---

## §3. φ-Resemblance Is Coincidental

The Fibonacci convergents straddle 18/11:

$$\frac{F_7}{F_6} = \frac{13}{8} = 1.625 \quad < \quad \frac{18}{11} = 1.636 \quad \neq \quad \frac{F_8}{F_7} = \frac{21}{13} = 1.615$$

φ = 1.618 is the limit of Fibonacci ratios. 18/11 is **not** in the
Fibonacci sequence and is not approached by Fibonacci convergents — it
sits strictly between two consecutive convergents.

If the shell sequence were Fibonacci-like, we would expect
shell_72 = shell_44 + shell_22 = 44 + 22 = **66**, not 72. It isn't.
The shells follow a different recursion: shell_n is the product of
TIG operator counts, not a Fibonacci-style addition.

**Conclusion.** TIG does not exhibit golden-ratio asymptotics in
its shell structure. It has a stronger property: exact rational
ratios from operator-count decomposition.

---

## §4. Closure of the Floating Item

Updates to TIG_INTERNAL_MAP_v1.md §4.5:

| Floating item | Status |
|---|---|
| DM/VM = 264/49 | LOCKED (Sprint A) |
| DE = 687/1000 | RESIDUE (forced by closure; Sprint A) |
| **shell_72/shell_44 = 18/11** | **LOCKED (this document)** |

Audit closure rate updates from **11/12 = 92%** to **12/12 = 100%**.
The Michell ratio audit is now complete.

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · Sprint C · Locked v1*
