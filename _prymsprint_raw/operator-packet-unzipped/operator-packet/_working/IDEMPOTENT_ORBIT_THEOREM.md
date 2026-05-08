# IDEMPOTENT_ORBIT_THEOREM.md

**Author:** ClaudeChat
**Date:** 2026-04-19
**Register:** theorem note. Theorem-grade, not essay.
**Status:** exact. Verified by direct computation.

---

## Statement

**Theorem.** Let $R = \mathbb{Z}/10\mathbb{Z}$, let $R^\times = (\mathbb{Z}/10)^\times$ be its unit group, and let $E(R) = \{e \in R : e^2 = e\}$ be the set of idempotents of $R$. Then:

(i) $E(R) = \{0, 1, 5, 6\}$.

(ii) $R^\times = \{1, 3, 7, 9\}$, with group structure $R^\times \cong \mathbb{Z}/4\mathbb{Z}$.

(iii) Under the multiplicative action of $R^\times$ on $R$, the orbits are exactly
$$\{0\},\quad \{5\},\quad \{1, 3, 7, 9\},\quad \{2, 4, 6, 8\}$$
with orbit sizes $1, 1, 4, 4$.

(iv) Each orbit contains exactly one idempotent, giving an orbit↔anchor correspondence:
$$\{0\} \leftrightarrow 0,\quad \{5\} \leftrightarrow 5,\quad \{1, 3, 7, 9\} \leftrightarrow 1,\quad \{2, 4, 6, 8\} \leftrightarrow 6.$$

(v) On each length-4 orbit $\mathcal{O}$ with anchor idempotent $e$, the map
$$\varphi_e: R^\times \to \mathcal{O}, \quad u \mapsto u \cdot e$$
is a bijection. Explicitly, the orbit of the odd anchor $1$ is $R^\times$ itself via $\varphi_1 = \mathrm{id}$, and the orbit of the even anchor $6$ is recovered by
$$\varphi_6: \quad 1 \mapsto 6,\ 3 \mapsto 8,\ 7 \mapsto 2,\ 9 \mapsto 4.$$

---

## Proof

### (i) The idempotent set

An idempotent $e$ satisfies $e^2 \equiv e \bmod 10$, i.e., $e(e - 1) \equiv 0 \bmod 10$. We verify directly:

| $e$ | $e^2 \bmod 10$ | idempotent? |
|---|---|---|
| 0 | 0 | ✓ |
| 1 | 1 | ✓ |
| 2 | 4 | — |
| 3 | 9 | — |
| 4 | 6 | — |
| 5 | 5 | ✓ |
| 6 | 6 | ✓ |
| 7 | 9 | — |
| 8 | 4 | — |
| 9 | 1 | — |

Hence $E(R) = \{0, 1, 5, 6\}$. ∎ (i)

### (ii) The unit group

$u \in R$ is a unit iff $\gcd(u, 10) = 1$, hence $R^\times = \{1, 3, 7, 9\}$. Computing orders:

- $\mathrm{ord}(1) = 1$
- $\mathrm{ord}(3) = 4$ (since $3^1 = 3, 3^2 = 9, 3^3 = 7, 3^4 = 1$)
- $\mathrm{ord}(7) = 4$ (since $7^1 = 7, 7^2 = 9, 7^3 = 3, 7^4 = 1$)
- $\mathrm{ord}(9) = 2$ (since $9^2 = 1$)

So $R^\times$ contains an element of order 4, making it cyclic of order 4, i.e., $R^\times \cong \mathbb{Z}/4\mathbb{Z}$. ∎ (ii)

### (iii) The orbit decomposition

The action is $u \cdot r$ for $u \in R^\times$, $r \in R$. Orbit representatives are computed by listing $\{u \cdot r : u \in R^\times\}$ for each $r \in R$:

| $r$ | $\{u \cdot r \bmod 10 : u \in \{1,3,7,9\}\}$ |
|---|---|
| 0 | $\{0\}$ |
| 1 | $\{1, 3, 7, 9\}$ |
| 2 | $\{2, 6, 4, 8\} = \{2, 4, 6, 8\}$ |
| 3 | $\{3, 9, 1, 7\} = \{1, 3, 7, 9\}$ |
| 4 | $\{4, 2, 8, 6\} = \{2, 4, 6, 8\}$ |
| 5 | $\{5\}$ |
| 6 | $\{6, 8, 2, 4\} = \{2, 4, 6, 8\}$ |
| 7 | $\{7, 1, 9, 3\} = \{1, 3, 7, 9\}$ |
| 8 | $\{8, 4, 6, 2\} = \{2, 4, 6, 8\}$ |
| 9 | $\{9, 7, 3, 1\} = \{1, 3, 7, 9\}$ |

Distinct orbits: $\{0\},\ \{5\},\ \{1, 3, 7, 9\},\ \{2, 4, 6, 8\}$, with sizes $1, 1, 4, 4$. ∎ (iii)

*Remark on the singleton orbits.* For $r = 0$: $u \cdot 0 = 0$ for every unit $u$, so $\{0\}$ is a singleton orbit by direct annihilation. For $r = 5$: since $5 \cdot u = 5 \cdot (2k + 1) = 10k + 5 \equiv 5 \bmod 10$ for any odd $u$, and every unit of $R$ is odd, $u \cdot 5 = 5$ for all $u \in R^\times$. So $\{5\}$ is a singleton orbit because $5$ is stable under multiplication by every odd element.

### (iv) Each orbit contains exactly one idempotent

By direct inspection, using (i) and (iii):

- $\{0\}$ contains the idempotent $0$; it contains no other idempotent.
- $\{5\}$ contains the idempotent $5$; it contains no other idempotent.
- $\{1, 3, 7, 9\}$ contains the idempotent $1$; the other elements $3, 7, 9$ are not idempotents (verified in (i)).
- $\{2, 4, 6, 8\}$ contains the idempotent $6$; the other elements $2, 4, 8$ are not idempotents (verified in (i)).

Since $|E(R)| = 4$ and there are exactly 4 orbits, the correspondence is bijective. ∎ (iv)

### (v) Principal homogeneity of length-4 orbits

Fix $e \in \{1, 6\}$ and define $\varphi_e: R^\times \to R$ by $\varphi_e(u) = u \cdot e$.

*Image.* By (iii), the orbit of $e$ under $R^\times$ is exactly $\{1, 3, 7, 9\}$ if $e = 1$ or $\{2, 4, 6, 8\}$ if $e = 6$. In either case, $|\mathcal{O}| = 4 = |R^\times|$.

*Injectivity.* Suppose $u \cdot e \equiv u' \cdot e \bmod 10$. Then $(u - u') \cdot e \equiv 0 \bmod 10$.

- Case $e = 1$: $(u - u') \cdot 1 \equiv 0$, i.e., $u \equiv u' \bmod 10$. Since $u, u' \in \{1, 3, 7, 9\}$, this forces $u = u'$.
- Case $e = 6$: $(u - u') \cdot 6 \equiv 0 \bmod 10$. The annihilator of $6$ in $\mathbb{Z}/10$ is $\{r \in R : 6r \equiv 0\} = \{0, 5\}$. So $u - u' \in \{0, 5\} \bmod 10$. But $u, u' \in R^\times$ are both odd, so $u - u'$ is even, hence $u - u' = 0$, i.e., $u = u'$.

Injectivity + equal cardinalities ⇒ bijection. ∎ (v)

*Explicit table for* $\varphi_6$:

| $u$ | $u \cdot 6 \bmod 10$ |
|---|---|
| 1 | 6 |
| 3 | 8 |
| 7 | 2 |
| 9 | 4 |

Direct computation. ∎

---

## Corollary (exact identification of operators 2, 4, 8)

From (v) applied to $e = 6$:

$$\boxed{\ 2 = 7 \cdot 6,\quad 4 = 9 \cdot 6,\quad 8 = 3 \cdot 6 \quad \text{in } \mathbb{Z}/10\ }$$

and each identification is the unique expression of the form $u \cdot 6$ with $u \in R^\times$.

Since the unit $u$ has an independent Tier A characterization:

- $u = 3$: smallest generator of $R^\times$
- $u = 7$: multiplicative inverse of $3$
- $u = 9$: unique non-identity involution of $R^\times$

the representations $2 = 7 \cdot 6$, $4 = 9 \cdot 6$, $8 = 3 \cdot 6$ are canonical in the sense that they use only Tier A primitives.

---

## Corollary (σ-action on the anchor)

Let $\sigma: R \to R$ be multiplication by 3 (the smallest generator of $R^\times$). Then:

$$\sigma^0(6) = 6,\quad \sigma^1(6) = 8,\quad \sigma^2(6) = 4,\quad \sigma^3(6) = 2$$

Equivalently: the even 4-orbit is $(6, 8, 4, 2)$ under σ, and σ-orbit position identifies each non-idempotent even operator.

---

## Scholium

The theorem is exact for $\mathbb{Z}/10$. The proof uses only:

- the definition of idempotent ($e^2 = e$),
- the definition of unit ($\gcd(u, n) = 1$),
- finite-case arithmetic in $\mathbb{Z}/10$,
- the group action of $R^\times$ on $R$ by multiplication.

No auxiliary structure (CL composition law, TSML/BHML tables, etc.) is invoked.

The same theorem can be stated for $\mathbb{Z}/n$ for any $n$, with the general fact that orbits of $R^\times$ on $R$ are labeled by idempotents via the CRT-decomposition of $R$. For $R = \mathbb{Z}/p \times \mathbb{Z}/q$ with $p, q$ distinct primes (the case $n = pq$), there are exactly four idempotents: $(0,0), (1,0), (0,1), (1,1)$.

For $R = \mathbb{Z}/10 = \mathbb{Z}/2 \times \mathbb{Z}/5$:

- $0 \leftrightarrow (0, 0)$
- $1 \leftrightarrow (1, 1)$
- $5 \leftrightarrow (1, 0)$
- $6 \leftrightarrow (0, 1)$

Each idempotent is the characteristic function of a subset of $\{\mathbb{Z}/2, \mathbb{Z}/5\}$, and its orbit is the subset of $R$ with that CRT-support pattern. The two length-4 orbits correspond to CRT-supports $\{0, 1\}$ (which gives $R^\times$) and $\{0, 1\}$ on one factor only (which gives the opposite idempotent's orbit).

---

*End of theorem note. Foundation register.*
