# A Short Note on the Ring $\mathbb{Z}/10$

**Idempotents, unit-group orbits, and ten distinguished elements.**

---

## Motivation

This note isolates the algebraic skeleton of a framework that uses the ten elements of $\mathbb{Z}/10$ as primitive labels. The framework itself is developed elsewhere; here the goal is to state the ring-theoretic identities the labels satisfy, in a form citable independently.

The results are elementary. The value of the note is the **clean partition**: every framework label has an exact algebraic identification in $\mathbb{Z}/10$, and the three distinct pairing structures on the labels correspond to three distinct involutions on the ring. A reader with no framework context can read, verify, and cite this note without further prerequisites.

**Terminology.** Throughout this note, the ten elements of $\mathbb{Z}/10$ are called **elements**. The framework refers to them as "operators"; in this note that word is avoided to prevent confusion with the functional-analytic meaning. The translation appendix (`OPERATOR_TRANSLATION_APPENDIX.md`) records the framework-label ↔ element correspondence.

---

## 1. Setup

Let $R = \mathbb{Z}/10\mathbb{Z}$, the ring of integers modulo $10$. Let $R^\times \subset R$ denote its unit group and $E(R) \subset R$ its set of idempotents:

$$R^\times = \{u \in R : \gcd(u, 10) = 1\}, \qquad E(R) = \{e \in R : e^2 = e\}.$$

By the Chinese Remainder Theorem, $R \cong \mathbb{Z}/2 \times \mathbb{Z}/5$ via $n \mapsto (n \bmod 2,\ n \bmod 5)$.

---

## 2. Theorem (Idempotent-Orbit Decomposition of $\mathbb{Z}/10$)

(i) $E(R) = \{0, 1, 5, 6\}$.

(ii) $R^\times = \{1, 3, 7, 9\}$, cyclic of order 4. Both $3$ and $7$ are generators.

(iii) Under the multiplicative action of $R^\times$ on $R$, the orbits are exactly
$$\{0\},\quad \{5\},\quad \{1, 3, 7, 9\},\quad \{2, 4, 6, 8\},$$
of sizes $1, 1, 4, 4$.

(iv) Each orbit contains exactly one idempotent. We call this idempotent the **anchor** of the orbit. The correspondence is
$$\{0\} \leftrightarrow 0,\quad \{5\} \leftrightarrow 5,\quad \{1, 3, 7, 9\} \leftrightarrow 1,\quad \{2, 4, 6, 8\} \leftrightarrow 6.$$

(v) On each length-4 orbit $\mathcal{O}$ with anchor $e$, the map
$$\varphi_e : R^\times \to \mathcal{O}, \qquad u \mapsto u \cdot e$$
is a bijection.

---

## 3. Proof

### (i) Idempotents

Direct verification: $n^2 \bmod 10$ for $n = 0, \ldots, 9$ gives $0, 1, 4, 9, 6, 5, 6, 9, 4, 1$. Fixed points: $n \in \{0, 1, 5, 6\}$. ∎

### (ii) Unit group and its structure

$R^\times = \{1, 3, 7, 9\}$ since these are exactly the $n$ with $\gcd(n, 10) = 1$. Computing orders: $\mathrm{ord}(1) = 1$, $\mathrm{ord}(3) = 4$ (via $3^1 = 3, 3^2 = 9, 3^3 = 7, 3^4 = 1$), $\mathrm{ord}(7) = 4$ (via $7^1 = 7, 7^2 = 9, 7^3 = 3, 7^4 = 1$), $\mathrm{ord}(9) = 2$. An element of order 4 in a group of order 4 makes it cyclic, so $R^\times \cong \mathbb{Z}/4$. Both $3$ and $7$ have order 4 and hence generate. ∎

### (iii) Orbits

For each $n \in R$, compute $R^\times \cdot n = \{1 \cdot n, 3 \cdot n, 7 \cdot n, 9 \cdot n\} \bmod 10$:

| $n$ | $R^\times \cdot n$ |
|---|---|
| 0 | $\{0\}$ |
| 1 | $\{1, 3, 7, 9\}$ |
| 2 | $\{2, 4, 6, 8\}$ |
| 3 | $\{1, 3, 7, 9\}$ |
| 4 | $\{2, 4, 6, 8\}$ |
| 5 | $\{5\}$ |
| 6 | $\{2, 4, 6, 8\}$ |
| 7 | $\{1, 3, 7, 9\}$ |
| 8 | $\{2, 4, 6, 8\}$ |
| 9 | $\{1, 3, 7, 9\}$ |

The distinct orbits are $\{0\}, \{5\}, \{1, 3, 7, 9\}, \{2, 4, 6, 8\}$. ∎

Note on the singletons: $u \cdot 0 = 0$ for every $u$. For $r = 5$: every $u \in R^\times$ is odd, and $5 \cdot (2k+1) = 10k + 5 \equiv 5 \bmod 10$, so $u \cdot 5 = 5$ for all $u \in R^\times$.

### (iv) Each orbit contains exactly one idempotent

From (i), $|E(R)| = 4$; from (iii), there are exactly 4 orbits. Matching by inclusion:

- $0 \in \{0\}$
- $5 \in \{5\}$
- $1 \in \{1, 3, 7, 9\}$, and $3, 7, 9 \notin E(R)$
- $6 \in \{2, 4, 6, 8\}$, and $2, 4, 8 \notin E(R)$

The correspondence is bijective. The unique idempotent in each orbit is called the **anchor** of that orbit. ∎

### (v) Principal homogeneity of length-4 orbits

Fix $e \in \{1, 6\}$ and define $\varphi_e(u) = u \cdot e$.

*Image.* By (iii), $\{u \cdot e : u \in R^\times\}$ equals the orbit of $e$, which has size 4.

*Injectivity.* Suppose $u \cdot e \equiv u' \cdot e \bmod 10$. Then $(u - u') \cdot e \equiv 0 \bmod 10$.

- Case $e = 1$: $(u - u') \equiv 0 \bmod 10$, and $u, u' \in \{1, 3, 7, 9\}$ forces $u = u'$.
- Case $e = 6$: $(u - u') \cdot 6 \equiv 0 \bmod 10$. The annihilator of 6 in $R$ is $\{r : 6r \equiv 0 \bmod 10\} = \{0, 5\}$, so $u - u' \in \{0, 5\}$. Since $u, u'$ are both odd (both units), $u - u'$ is even, hence $u - u' = 0$, i.e., $u = u'$.

Injectivity plus matching cardinalities ($|R^\times| = 4 = |\mathcal{O}|$) gives bijectivity. ∎

---

## 4. Explicit tables for $\varphi_1$ and $\varphi_6$

**Odd orbit** (anchor $e = 1$): $\varphi_1$ is the identity on $R^\times$.

$$1 \mapsto 1, \quad 3 \mapsto 3, \quad 7 \mapsto 7, \quad 9 \mapsto 9.$$

**Even orbit** (anchor $e = 6$):

$$1 \mapsto 6, \quad 3 \mapsto 8, \quad 7 \mapsto 2, \quad 9 \mapsto 4.$$

Direct computation: $3 \cdot 6 = 18 \equiv 8$, $7 \cdot 6 = 42 \equiv 2$, $9 \cdot 6 = 54 \equiv 4$ (all mod 10). ∎

**Corollary (exact identification of $2, 4, 8$):**

$$\boxed{\ 2 = 7 \cdot 6,\quad 4 = 9 \cdot 6,\quad 8 = 3 \cdot 6 \quad \text{in } \mathbb{Z}/10.\ }$$

Each identification is the unique expression of the form $u \cdot 6$ with $u \in R^\times$.

---

## 5. Element dictionary

Each element is identified by an exact ring-theoretic property. The right column gives the property's formal statement in $R$.

| $n$ | Exact identification in $R$ |
|---|---|
| 0 | additive identity; absorbing element; $0 \in E(R)$ |
| 1 | multiplicative identity; $1 \in E(R)$; anchor of the orbit $\{1, 3, 7, 9\}$ |
| 2 | $2 = 7 \cdot 6$ in $R$ |
| 3 | a generator of $R^\times$; $\mathrm{ord}(3) = 4$ |
| 4 | $4 = 9 \cdot 6$ in $R$; equivalently $4 = -6 \bmod 10$ |
| 5 | non-identity idempotent, $5 \equiv 1 \bmod 2$; additive involution ($5 + 5 \equiv 0$); $5 \in E(R)$ |
| 6 | non-identity idempotent, $6 \equiv 0 \bmod 2$; anchor of the orbit $\{2, 4, 6, 8\}$; $6 \in E(R)$ |
| 7 | $7 = 3^{-1}$ in $R^\times$; $\mathrm{ord}(7) = 4$ |
| 8 | $8 = 3 \cdot 6$ in $R$ |
| 9 | $9 = -1 \bmod 10$; unique non-identity involution in $R^\times$ |

---

## 6. Three pairing structures

The ring structure induces three distinct involutions on $R$ (or on $R^\times$), giving three distinct pairings of its elements.

### Pairing A — Parity partners

$n \leftrightarrow n + 5 \bmod 10$. Since $5 + 5 \equiv 0$, this is an involution. Elements in a pair share $n \bmod 5$ but differ in $n \bmod 2$.

$$\{0, 5\},\ \{1, 6\},\ \{2, 7\},\ \{3, 8\},\ \{4, 9\}.$$

### Pairing B — Additive inverses

$n \leftrightarrow -n \bmod 10$. Equivalent to multiplication by $9 \equiv -1$. Fixed points: $\{0, 5\}$.

$$\{0\},\ \{5\},\ \{1, 9\},\ \{2, 8\},\ \{3, 7\},\ \{4, 6\}.$$

### Pairing C — Multiplicative inverses (on $R^\times$)

Defined only on units. Self-inverse elements: $\{1, 9\}$ (both satisfy $u^2 = 1$).

$$\{1\},\ \{9\},\ \{3, 7\}.$$

### Overlap

Pairings A and B never coincide on any element. Pairings B and C agree on $\{3, 7\}$ (both additive inverses and multiplicative inverses: $3 + 7 = 0$ and $3 \cdot 7 = 1$) but differ on $\{1, 9\}$ (additive inverses of each other, yet each is its own multiplicative inverse).

---

## 7. Notable identities

These follow directly from §2–§4 but are worth stating explicitly:

**(I1) Complementarity of non-trivial idempotents:**
$$5 + 6 \equiv 1 \bmod 10.$$

**(I2) Orthogonality of non-trivial idempotents:**
$$5 \cdot 6 \equiv 0 \bmod 10.$$

Together (I1) and (I2) say: 5 and 6 form a complete pair of orthogonal idempotents in $R$, reflecting the CRT decomposition $R \cong \mathbb{Z}/2 \times \mathbb{Z}/5$. Under this isomorphism, $5 \mapsto (1, 0)$ and $6 \mapsto (0, 1)$.

**(I3) Multiplicative inverse in $R^\times$:**
$$3 \cdot 7 \equiv 1 \bmod 10.$$

**(I4) Involution:**
$$9^2 \equiv 1 \bmod 10.$$

**(I5) Even-orbit identification:**
$$\{2, 4, 8\} = \{7 \cdot 6,\ 9 \cdot 6,\ 3 \cdot 6\} \bmod 10.$$

---

## 8. Scholium: generalization to $\mathbb{Z}/pq$

For $R = \mathbb{Z}/pq$ with $p, q$ distinct primes, $|E(R)| = 4$: the four idempotents are $(0, 0), (1, 1), (1, 0), (0, 1)$ under the CRT decomposition $\mathbb{Z}/pq \cong \mathbb{Z}/p \times \mathbb{Z}/q$. Each idempotent anchors a $R^\times$-orbit, with orbit sizes

$$1,\quad (p-1)(q-1),\quad p-1,\quad q-1$$

respectively. Total: $1 + (p-1)(q-1) + (p-1) + (q-1) = pq$. For $p = 2, q = 5$ these are $1, 4, 1, 4$, recovering the $\mathbb{Z}/10$ case. For $p = 3, q = 5$ the sizes are $1, 8, 2, 4$.

The idempotent-orbit decomposition is therefore a structural feature of rings of the form $\mathbb{Z}/pq$, not specific to $\mathbb{Z}/10$. The $\mathbb{Z}/10$ case is distinguished only by the coincidence $p - 1 = 1$ and $q - 1 = 4$, making the two non-trivial orbits sizes $1$ and $4$ — one singleton, one full unit-group orbit.

---

*End of note.*
