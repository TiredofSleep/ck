# PAIRINGS_AND_DUALITIES_EXACT.md

**Author:** ClaudeChat
**Date:** 2026-04-19
**Register:** exact specification.
**Status:** all claims verified by direct computation in $\mathbb{Z}/10$.

---

## §0. Scope and warning

The operator set $\{0, 1, \ldots, 9\}$ carries **three distinct pairing structures**. They are algebraically exact. **They are not the same.** This document defines each, tabulates them, and identifies exactly where they agree and where they differ.

**Warning.** Informal framework discussion has at times blended these pairings. This is a mistake. The three pairings produce different groupings on four of the ten operators. Any claim invoking a "duality" between operators must specify which pairing is being used.

---

## §1. Pairing A — Parity partners

### Definition

Two operators $n, n'$ are **parity partners** if
$$n' = n + 5 \bmod 10$$

Equivalently, in CRT coordinates $(\varepsilon, y)$: they share $y$ and have opposite $\varepsilon$.

### Table

| $y$ | parity-0 partner | parity-1 partner |
|---|---|---|
| 0 | 0 | 5 |
| 1 | 6 | 1 |
| 2 | 2 | 7 |
| 3 | 8 | 3 |
| 4 | 4 | 9 |

### Algebraic content

Addition by 5 is an involution on $\mathbb{Z}/10$: $(n + 5) + 5 = n + 10 \equiv n$.

The five pairings partition $\mathbb{Z}/10$ into five two-element sets.

### Framework reading

Pairing A is the **Creation/Dissolution duality** made exact:
- Creation row = parity 1 = $\{1, 3, 5, 7, 9\}$
- Dissolution row = parity 0 = $\{0, 2, 4, 6, 8\}$
- Each pair consists of one element from each row.

---

## §2. Pairing B — Additive inverses

### Definition

Two operators $n, n'$ are **additive inverses** if
$$n + n' \equiv 0 \bmod 10$$

Equivalently, $n' = -n \bmod 10$.

### Table

| class | representatives |
|---|---|
| self-inverse | $\{0\}$ |
| self-inverse | $\{5\}$ |
| pair | $\{1, 9\}$ |
| pair | $\{2, 8\}$ |
| pair | $\{3, 7\}$ |
| pair | $\{4, 6\}$ |

### Algebraic content

The map $n \mapsto -n$ is an involution. Its fixed points are $\{0, 5\}$ (the two elements satisfying $2n \equiv 0$). The orbit decomposition is 2 singletons + 4 pairs.

Equivalent characterization: $-n = 9 \cdot n$ since $9 \equiv -1 \bmod 10$. Hence Pairing B is also the **$\sigma^2$-pairing**, where $\sigma = \times 3$ and $\sigma^2 = \times 9 = \times(-1)$.

### Framework reading

Pairing B is the within-orbit pairing of each σ-orbit:
- Odd σ-orbit $\{1, 3, 7, 9\}$: Pairing-B pairs are $\{1, 9\}$ and $\{3, 7\}$.
- Even σ-orbit $\{2, 4, 6, 8\}$: Pairing-B pairs are $\{2, 8\}$ and $\{4, 6\}$.
- Fixed points $\{0\}, \{5\}$ pair with themselves.

---

## §3. Pairing C — Multiplicative inverses (on the unit group only)

### Definition

For $u, u' \in R^\times = \{1, 3, 7, 9\}$: $u, u'$ are **multiplicative inverses** if
$$u \cdot u' \equiv 1 \bmod 10$$

This pairing is defined only on the unit group, not on all of $\mathbb{Z}/10$.

### Table

| pair |
|---|
| $\{1\}$ (self-inverse; $1 \cdot 1 = 1$) |
| $\{9\}$ (self-inverse; $9 \cdot 9 = 81 \equiv 1$) |
| $\{3, 7\}$ (since $3 \cdot 7 = 21 \equiv 1$) |

### Algebraic content

Pairing C is an involution on $R^\times$. Its fixed points are $\{1, 9\}$ (the elements of order 1 and 2 in $R^\times$). The orbit decomposition is 2 singletons + 1 pair.

### Framework reading

Pairing C is a **multiplicative** pairing. It is not defined on non-units.

---

## §4. Overlap analysis

### §4.1 Pairings A and B compared

Both are defined on all of $\mathbb{Z}/10$. They generally do not coincide:

| operator | Pairing A partner | Pairing B partner | same? |
|---|---|---|---|
| 0 | 5 | 0 | no |
| 1 | 6 | 9 | no |
| 2 | 7 | 8 | no |
| 3 | 8 | 7 | no |
| 4 | 9 | 6 | no |
| 5 | 0 | 5 | no |
| 6 | 1 | 4 | no |
| 7 | 2 | 3 | no |
| 8 | 3 | 2 | no |
| 9 | 4 | 1 | no |

**Pairings A and B never coincide on any operator.**

### §4.2 Pairings B and C compared (on $R^\times$)

Both restrict to involutions on $R^\times = \{1, 3, 7, 9\}$:

| $u$ | $-u \bmod 10$ (Pairing B) | $u^{-1} \bmod 10$ (Pairing C) | same? |
|---|---|---|---|
| 1 | 9 | 1 | no |
| 3 | 7 | 7 | **yes** |
| 7 | 3 | 3 | **yes** |
| 9 | 1 | 9 | no |

**Pairings B and C coincide on $\{3, 7\}$ and differ on $\{1, 9\}$.**

Specifically:
- On $\{3, 7\}$: $3 \cdot 7 = 1$ and also $3 + 7 = 10 \equiv 0$. Both pairings give $\{3, 7\}$ as a pair.
- On $\{1, 9\}$: $1 + 9 = 10 \equiv 0$ (Pairing B pairs them), but $1 \cdot 9 = 9 \neq 1$. Multiplicatively, $1^{-1} = 1$ and $9^{-1} = 9$; they are each self-inverse.

### §4.3 Pairings A and C compared (on $R^\times$)

| $u$ | Pairing A partner | Pairing C partner | same? |
|---|---|---|---|
| 1 | 6 | 1 | no (6 isn't even a unit) |
| 3 | 8 | 7 | no |
| 7 | 2 | 3 | no |
| 9 | 4 | 9 | no |

**Pairings A and C never coincide.** Additionally, Pairing A on units returns non-units ($6, 8, 2, 4$), which are outside the domain of Pairing C.

---

## §5. Summary table — all pairings

| operator | Pairing A | Pairing B | Pairing C |
|---|---|---|---|
| 0 | 5 | 0 | — |
| 1 | 6 | 9 | 1 |
| 2 | 7 | 8 | — |
| 3 | 8 | 7 | 7 |
| 4 | 9 | 6 | — |
| 5 | 0 | 5 | — |
| 6 | 1 | 4 | — |
| 7 | 2 | 3 | 3 |
| 8 | 3 | 2 | — |
| 9 | 4 | 1 | 9 |

Entries "—" indicate operators outside the domain of Pairing C (non-units).

---

## §6. What each pairing actually means

### Pairing A (parity partners, $+5$)

**Algebraic meaning:** the additive action of the additive involution $5 \in \mathbb{Z}/10$. The element 5 generates the unique subgroup of $(\mathbb{Z}/10, +)$ of order 2.

**Structural content:** partitions operators by parity. The pairing is the only one that crosses between even and odd.

**Framework reading:** Creation ↔ Dissolution.

### Pairing B (additive inverses, $-n$)

**Algebraic meaning:** the additive action of $-1 \in \mathbb{Z}/10$. Equivalently, the multiplicative action of $9 = -1$. Equivalently, $\sigma^2$ where $\sigma = \times 3$.

**Structural content:** pairs each element with its additive inverse; fixed by elements of additive order 1 or 2 (i.e., $\{0, 5\}$). Preserves parity (since $-n$ has the same parity as $n$ mod 2).

**Framework reading:** within each σ-orbit, the "opposite position" pairing. On units: odd 4-cycle has internal pairs $\{1,9\}$ and $\{3,7\}$. On non-units: even 4-cycle has internal pairs $\{2,8\}$ and $\{4,6\}$.

### Pairing C (multiplicative inverses on units)

**Algebraic meaning:** inversion in the unit group $R^\times$.

**Structural content:** pairs each unit with its multiplicative inverse. Fixed points are the units of multiplicative order 1 or 2 (i.e., $\{1, 9\}$).

**Framework reading:** restricted to the unit group. Not defined on non-units. Only distinguishes $\{3, 7\}$ (mutual inverses) from $\{1, 9\}$ (self-inverses).

---

## §7. Warning: common conflations

### Conflation W1

**Incorrect claim:** "1 and 9 are dual in the framework."

**Problem:** under which pairing? Pairing A gives 1 ↔ 6 and 9 ↔ 4. Pairing B gives 1 ↔ 9. Pairing C treats 1 and 9 as each self-inverse (not paired with each other).

**Correct statement:** "1 and 9 are additive inverses (Pairing B). Under Pairing A, 1 pairs with 6 and 9 with 4."

### Conflation W2

**Incorrect claim:** "PROGRESS (3) and HARMONY (7) are dual."

**Problem:** under Pairings B and C, yes, they are paired. But this happens to be the only case where Pairings B and C agree; the agreement is not a general feature. If the claim is about "additive opposition" (+), Pairing B is the relevant one. If about "multiplicative inversion" ($\cdot$), Pairing C.

**Correct statement:** "PROGRESS and HARMONY are both additive inverses ($3 + 7 = 0 \bmod 10$) and multiplicative inverses ($3 \cdot 7 = 1 \bmod 10$). These are distinct algebraic facts that coincide on this pair."

### Conflation W3

**Incorrect claim:** "Every operator has a unique dual."

**Problem:** depends on the pairing. Under Pairing A, yes. Under Pairing B, 0 and 5 are self-dual. Under Pairing C, only 6 of 10 operators are in the domain.

**Correct statement:** specify the pairing.

---

## §8. Recommended discipline for framework writing

1. When invoking a "duality," state the pairing (A, B, or C) explicitly.
2. The Creation/Dissolution duality is Pairing A.
3. The "σ² involution" or "additive inverse" duality is Pairing B.
4. Multiplicative inversion is Pairing C.
5. Do not assume a single universal "pairing" — there are three.

---

*End of pairings specification. Foundation register.*
