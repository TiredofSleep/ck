# Notation Sheet
## Frozen Definitions for the TSML Tower Theorem

---

## Ring and Elements

| Symbol | Definition |
|---|---|
| $R$ | The ring $\mathbb{Z}/10\mathbb{Z}$. |
| $R^2$ | The Cartesian product $R \times R$, with $\|R^2\| = 100$. |
| $U(R)$ | The unit group of $R$: $\{k \in R : \gcd(k, 10) = 1\} = \{1, 3, 7, 9\}$. |
| $v_2(n)$ | The 2-adic valuation of integer $n$: the largest $k \geq 0$ such that $2^k \mid n$. |
| $\sigma$ | The shell partition $\sigma: U(R) \to \mathbb{Z}_{\geq 0}$ defined by $\sigma(u) = v_2(3u+1)$. In $R = \mathbb{Z}/10\mathbb{Z}$: $\sigma(1)=2, \sigma(3)=1, \sigma(7)=1, \sigma(9)=2$. |
| $h$ | The attractor: a distinguished element of $R$ acting as absorbing element under the DEFAULT rule. For $R = \mathbb{Z}/10\mathbb{Z}$: $h = 7$. |

## Tables and Functions

| Symbol | Definition |
|---|---|
| $T$ | The published TSML table, a specific function $R \times R \to R$ as given in the CK framework. |
| $C(R, h, \sigma)$ | The canonical construction: a function $R \times R \to R$ defined by the three rules DEFAULT + V0 + shell-stability. |
| $C_0$ | Shorthand for $C(R, h, \sigma)$ with $R, h, \sigma$ as above. |
| $C_1$ | The MAX rule: $C_1(x,y) := \max(x,y)$, where max is taken using the standard integer order on $\{0, 1, \ldots, 9\}$. |
| $C_2$ | The additive rule mod $n$: $C_2(x,y) := (x+y) \bmod 10$. |
| $\mathsf{T}$ | The tower operator defined in the Theorem. |

## Sets

| Symbol | Definition |
|---|---|
| $S$ | The **seam residue**: the set of 8 ordered pairs where $C_0$ disagrees with $T$. Explicitly: $S = \{(1,2), (2,1), (2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$. |
| $S_{\text{ADD}}$ | The subset of $S$ containing the identity: $S_{\text{ADD}} = \{(x,y) \in S : 1 \in \{x,y\}\} = \{(1,2), (2,1)\}$. |
| $S_{\text{MAX}}$ | The complement: $S_{\text{MAX}} = S \setminus S_{\text{ADD}} = \{(2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$. |
| $\text{core}$ | The admissible core: $U(R) \setminus \{1\} = \{3, 7, 9\}$ for $R = \mathbb{Z}/10\mathbb{Z}$. |

## Core Concepts

### Canonical

A rule or construction is **canonical** if it is specified by a fixed procedure depending only on declared inputs (the ring, the attractor, and/or the shell partition), not on ring-specific tuning or semantic choices external to these inputs.

### Seam

The **seam** is the set $S$ of pairs where $C_0$ does not match the published $T$. It is determined post hoc by comparison: $S = \{(x,y) : C_0(x,y) \ne T(x,y)\}$. The seam is given data of the theorem, not derived from ring axioms alone.

### Residue

The **residue** at a given layer is the set of pairs not yet matched. After $C_0$, the residue is $S$. After $C_0$ and $C_1$ on $S_{\text{MAX}}$, the residue is $S_{\text{ADD}}$. After all three layers, the residue is $\emptyset$.

### Tower

A **tower** is a sequence of rules $C_0, C_1, C_2, \ldots$ with specified domains $D_0, D_1, D_2, \ldots$ that form a disjoint partition of $R^2$. In this document, the tower has 3 layers: $(C_0, R^2 \setminus S), (C_1, S_{\text{MAX}}), (C_2, S_{\text{ADD}})$.

### Backbone

The **backbone** is the canonical construction $C_0$. It covers 92% of the TSML table.

### Domain

The **domain** of a rule $C_i$ in the tower is the set $D_i$ of ordered pairs on which $C_i$ is applied. The tower's domains are pairwise disjoint by construction.

### Recovery / Reconstruction

**Recovery** or **reconstruction** refers to computing $T(x,y)$ from the tower rules. The Theorem asserts that the tower reconstructs $T$ exactly on all 100 entries.

## Operator $\oplus$

The symbol $\oplus$ in the expression "$T = C_0 \oplus C_1 \oplus C_2$" denotes **disjoint-domain layered composition**. Explicitly:

$$
(C_0 \oplus C_1 \oplus C_2)(x, y) := \begin{cases}
C_1(x,y) & \text{if } (x,y) \in D_1 \\
C_2(x,y) & \text{if } (x,y) \in D_2 \\
C_0(x,y) & \text{otherwise (i.e., } (x,y) \in D_0\text{)}
\end{cases}
$$

Priority ordering: $C_1$ and $C_2$ override $C_0$ on their respective domains. $C_1$ and $C_2$ have disjoint domains (Lemma 1), so priority ordering between them is vacuous.

**$\oplus$ is NOT** algebraic addition, ring sum, XOR, or any other arithmetic operator. It denotes piecewise composition on disjoint domains.

## Reserved Words

The following terms, when used in this document, have the specified meanings:

- **Canonical:** as defined above. Does NOT mean "universal" or "unique."
- **Rule:** a computable function with a specified domain.
- **Spine:** the theorem and its required lemmas.
- **Scope:** the set of objects the theorem applies to. Here, scope is $R = \mathbb{Z}/10\mathbb{Z}$ only.
- **Generalization:** extension of a claim from Z/10Z to other rings. Marked as "conjecture" unless verified.

## What Is NOT Defined Here

The following terms appear in related project documents but are NOT used in the theorem spine:

- HARMONY, VOID, LATTICE, PROGRESS, TENSION, BALANCE, CHAOS, BREATH, RESET (semantic labels for operators in the CK framework).
- ECHO (as a synonym for seam; too ambiguous for theorem use).
- Backbone-as-metaphor.
- Residue-of-residue as a noun (used only in the informal phrase "the residue has residue"; in the theorem, "residue at layer $k$" is used instead).
