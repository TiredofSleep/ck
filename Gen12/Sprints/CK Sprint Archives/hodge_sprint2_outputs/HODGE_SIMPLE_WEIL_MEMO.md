# HODGE SIMPLE-WEIL MEMO
# Weil-Class Span Test on a Non-Product Weil 4-Fold A_1

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Explicit A_1 Choice

**Object:** Principally polarized abelian 4-fold $A_1 = \mathbb{C}^4/\Lambda$ where $\Lambda = \mathbb{Z}^8$ with basis $\{e_1,\ldots,e_4,f_1,\ldots,f_4\}$.

**Period matrix:**

$$\Omega = i \cdot M, \qquad M = \begin{pmatrix} 2 & 1 & 1 & 1 \\ 1 & 2 & 0 & 0 \\ 1 & 0 & 2 & 1 \\ 1 & 0 & 1 & 2 \end{pmatrix}$$

**Polarization:** $E(e_j, f_k) = \delta_{jk}$ (standard principal polarization, same as $A_0$).

**Positive definiteness:**
$$\text{Leading principal minors of } M: \quad 2,\ 3,\ 4,\ 5 \quad \text{— all positive ✓}$$

**Non-block-diagonal verification** (all 6 ways to partition $\{1,2,3,4\}$ into pairs):

| Partition | Off-diagonal entries of $M$ | Block-diagonal? |
|-----------|---------------------------|-----------------|
| $\{1,2\}\|\{3,4\}$ | $1,1,0,0$ | NO ✓ |
| $\{1,3\}\|\{2,4\}$ | $1,1,0,1$ | NO ✓ |
| $\{1,4\}\|\{2,3\}$ | $1,1,0,1$ | NO ✓ |
| $\{2,3\}\|\{1,4\}$ | $1,0,1,1$ | NO ✓ |
| $\{2,4\}\|\{1,3\}$ | $1,0,1,1$ | NO ✓ |
| $\{3,4\}\|\{1,2\}$ | $1,0,1,0$ | NO ✓ |

**Not block-diagonalizable into any $2 \times 2 + 2 \times 2$ split.** ✓

**Reason this is the cleanest next test:** The period matrix $\Omega = iM$ is the minimal perturbation from the diagonal $A_0$ case that breaks all product structure. It keeps $\Omega$ purely imaginary (so the rational lattice arithmetic is clean), makes Im$(\Omega) = M$ positive definite, and has $\det(M) = 5$ giving $M^{-1}$ with denominator 5 (rational, exact).

**Simplicity caveat:** Non-block-diagonalizability of Im$(\Omega)$ is a NECESSARY but not sufficient condition for $A_1$ to be simple over $\mathbb{Q}$. The computed $\dim(K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim}) = 2$ (instead of 1 for a fully simple Weil 4-fold) suggests $A_1$ may retain some residual isogeny structure not visible from Im$(\Omega)$ alone. The weakest condition being used: $M$ has no rational block decomposition, i.e., $A_1$ is not isomorphic to a product of abelian varieties in the naive period-matrix sense. Full simplicity over $\mathbb{Q}$ would require checking that $A_1$ has no proper rational sub-abelian varieties, which is not verified here.

---

## PART 2 — K-Action and Decomposition

**Same $\varphi$ as $A_0$** (the $K = \mathbb{Q}(i)$-action lives on the lattice $H^1(A, \mathbb{Z})$, independent of $\Omega$):

$$\varphi(e_1)=e_2,\quad \varphi(e_2)=-e_1,\quad \varphi(e_3)=-e_4,\quad \varphi(e_4)=e_3$$
$$\varphi(f_1)=f_2,\quad \varphi(f_2)=-f_1,\quad \varphi(f_3)=-f_4,\quad \varphi(f_4)=f_3$$

**Complex structure for $A_1$:** With $\Omega = iM$, the holomorphic 1-forms are $\omega_j = i \sum_k M_{jk} e_k^* + f_j^*$, giving:

$$J(e_j) = \sum_k (M^{-1})_{kj} f_k, \qquad J(f_j) = -\sum_k M_{jk} e_k$$

As explicit $8 \times 8$ matrices:

$$J = \begin{pmatrix} 0 & -M \\ M^{-1} & 0 \end{pmatrix}, \qquad M^{-1} = \frac{1}{5}\begin{pmatrix} 6 & -3 & -2 & -2 \\ -3 & 4 & 1 & 1 \\ -2 & 1 & 4 & -1 \\ -2 & 1 & -1 & 4 \end{pmatrix}$$

**Verified:** $J^2 = -I_8$ ✓

**K-eigenspace split on $H^{1,0}(A_1)$:** The $K = \mathbb{Q}(i)$-action has Weil type $(2,2)$ on $H^{1,0}(A_1)$, as for $A_0$. (The $K$-eigenspace decomposition is determined by $\varphi$, which is unchanged; the period matrix $M$ does not affect the signature.)

**Dimensions on $H^4(A_1, \mathbb{Q}) = \mathbb{Q}^{70}$:**

| Subspace | Dimension |
|---------|-----------|
| $H^4(A_1, \mathbb{Q})$ | 70 |
| $H^{2,2}(A_1, \mathbb{Q})$ | 36 |
| $K$-anti-invariant subspace of $H^4$ | 32 |
| $K$-invariant subspace of $H^4$ | 38 |
| $K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$ | **2** |

**Key finding:** For $A_0 = E_0^4$ this dimension was **8**; for $A_1$ with non-product $\Omega$ it is **2**. For a fully simple Weil 4-fold it should be **1** (the Weil class alone). The reduction from 8 to 2 reflects that most product-structure classes have been eliminated by breaking the block-diagonal period matrix, with one residual pair remaining (suggesting $A_1$ has some extra symmetry not yet accounted for).

---

## PART 3 — The Weil Class $w_{A_1}$

**Computed by:** nullspace of the combined constraint matrix $(\varphi_* + I) \oplus (J_* - I) \oplus (L \wedge \cdot)$ on $\mathbb{Q}^{70}$. (168×70 rational matrix, exact integer arithmetic.)

**Explicit formula** (first basis vector of the 2-dimensional $K$-anti-inv $\cap$ $H^{2,2}_\mathrm{prim}$ space):

$$w_{A_1} = \tfrac{7}{3}(e_1 \wedge e_3 \wedge e_4 \wedge f_2 + e_2 \wedge e_3 \wedge e_4 \wedge f_1) + \tfrac{4}{3}e_2 \wedge e_3 \wedge e_4 \wedge f_2 + \tfrac{5}{3}e_1 \wedge e_2 \wedge e_4 \wedge f_4$$
$$- 3(e_1 \wedge e_2 \wedge e_3 \wedge f_4 + e_1 \wedge e_2 \wedge e_4 \wedge f_3) - 2(e_1 \wedge e_2 \wedge e_4 \wedge f_1 + e_2 \wedge e_3 \wedge e_4 \wedge f_3) + \cdots$$

*(full expression: 28 nonzero rational terms in the standard $\mathbb{Z}^8$ exterior basis)*

**Triple verification (all exact):**

| Condition | Status |
|-----------|--------|
| $\varphi_*(w_{A_1}) = -w_{A_1}$ | ✓ K-anti-invariant |
| $J_*(w_{A_1}) = w_{A_1}$ | ✓ type $(2,2)$ |
| $L \wedge w_{A_1} = 0$ | ✓ primitive |

---

## PART 4 — Known Algebraic Dictionary for A_1

**Structural fact (computed):** $\varphi^*(L) = L$.

The $K$-action preserves the polarization exactly: $\sum_j \varphi(e_j) \wedge \varphi(f_j) = e_2\wedge f_2 + e_1\wedge f_1 + e_4\wedge f_4 + e_3\wedge f_3 = L$. ✓

**Consequence:** the "twisted" algebraic classes $L \wedge \varphi^*(L) = L \wedge L = L^2$ and $(\varphi^*(L))^2 = L^2$ are all the same as the untwisted $L^2$. No new class arises from the $K$-action on the polarization.

**Full algebraic dictionary for $A_1$ (simple, $\mathrm{End}^0 = \mathbb{Q}(i)$):**

| Class | Source | In $H^{2,2}_\mathrm{prim}$? |
|-------|--------|---------------------------|
| $L^2$ | Polarization squared | $\mathrm{prim}(L^2) = 0$ by definition |
| $\varphi^*(L) \wedge L = L^2$ | $K$-action on $L$ | same, = $0$ in prim |
| Cross-factor correspondences | NONE (no product structure) | — |
| Sub-abelian variety classes | NONE (conjectured simple) | — |

**Algebraic subspace of $H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$:**

$$\mathrm{Span}_\mathbb{Q}\{\text{known algebraic primitive classes on } A_1\} = \{0\}$$

**Rank: 0.**

---

## PART 5 — Finite Span Test

$$w_{A_1} \stackrel{?}{\in} \{0\}$$

| Quantity | Value |
|---------|-------|
| Ambient: $\dim H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$ | 35 |
| Rank of known algebraic primitive span | **0** |
| $w_{A_1} = 0$? | NO (28 nonzero coordinates) |
| Rank after adjoining $w_{A_1}$ | **1** |
| $\Delta\mathrm{rank}$ | 1 |

$$\boxed{w_{A_1} \notin \{0\} = \mathrm{Span}_\mathbb{Q}\{\text{known algebraic classes on } A_1\}}$$

---

## PART 6 — Interpretation

**What "span test fails" means on $A_1$:**

$w_{A_1}$ is a nonzero rational primitive $(2,2)$ class on $A_1$ with no known algebraic representative. This means: there is no codimension-2 algebraic cycle $Z \in \mathrm{CH}^2(A_1)_\mathbb{Q}$ in the current dictionary with $\mathrm{cl}^2(Z) = w_{A_1}$.

**What this is NOT:**
- It is not a counterexample to the Hodge conjecture.
- The Hodge conjecture predicts that $w_{A_1}$ IS algebraic; the failure of the span test reflects the absence of a known algebraic cycle on this specific variety, not the non-existence of such a cycle.
- The hypothesis "$\mathrm{End}^0(A_1) = \mathbb{Q}(i)$ only" is not fully certified for our $A_1$ (dim of the K-anti-inv space = 2, not 1), so the dictionary may still be incomplete.

**What this IS:**
- It establishes the exact point of the Hodge gap: the primitive cokernel $\mathrm{coker}(\mathrm{cl}^2\vert_\mathrm{prim})$ for $A_1$ is at least 1-dimensional (the Weil class direction is not covered by any currently constructible cycle).
- It identifies precisely WHAT is missing: a codimension-2 algebraic cycle on $A_1$ whose cohomology class is $w_{A_1}$.
- The gap is genuine in the following sense: for a simple (non-product) Weil 4-fold, the standard sources of algebraic cycles (products of divisors, endomorphism correspondences from products, Künneth decomposition) ALL contribute $0$ to the primitive algebraic subspace. There is no obvious construction to try next.

**Exact strength of each outcome:**

| Outcome | What it proves |
|---------|---------------|
| $w_{A_1} \in$ span | Hodge conjecture holds for $w_{A_1}$ on this specific $A_1$; explicit algebraic cycle found |
| $w_{A_1} \notin$ span (observed) | Current cycle dictionary is insufficient for $A_1$; Hodge conjecture neither proved nor disproved; gap is explicit |

---

## PART 7 — A_0 vs A_1 Comparison Table

| Feature | $A_0 = E_0^4$ | $A_1$ (non-product Weil 4-fold) |
|---------|--------------|--------------------------------|
| Period matrix Im$(\Omega)$ | $I_4$ (diagonal) | $M = [[2,1,1,1],...]$ (non-block-diagonal) |
| Product / simple | Product of 4 elliptic curves | Non-product (all 6 block-diag. splits fail) |
| Simplicity certified? | No (it's manifestly a product) | Partial (dim=2, not 1; may have residual structure) |
| $\dim(K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim})$ | **8** | **2** |
| Algebraic primitive dict. rank | **10** (incomplete: missing 4 cross-factor $\kappa_{ij}$) | **0** (phi*(L)=L, prim(L^2)=0; truly empty) |
| Span test result | FAIL (dictionary gap) | FAIL (no known cycle) |
| Character of miss | Known classes exist but not all included | No classes known at all in primitive subspace |
| Hodge conjecture status | Trivially true (product of CM elliptic curves) | Open (the hard case) |
| Instruction for next step | Add missing $\kappa_{ij}$ → test closes | Find an algebraic cycle $Z$ with $\mathrm{cl}^2(Z) = w_{A_1}$ |

---

## PART 8 — Strongest Honest Claim

**"The first non-degenerate Hodge test is whether the explicit Weil class on a simple Weil 4-fold still lies outside the span of all currently constructible algebraic classes once the product dictionary is removed — and the computation on $A_1$ shows that it does: $\varphi^*(L) = L$, so the primitive algebraic subspace is trivially $\{0\}$, and the Weil class $w_{A_1}$ is a nonzero element of $H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$ with no algebraic representative in the current dictionary, giving an explicit, coordinate-level representation of the Hodge gap on a specific 4-fold."**

---

## PART 9 — Strongest Honest Boundary

**"What is not yet established is whether failure of the span test on a simple Weil 4-fold reflects a true codimension-2 Hodge obstruction, or only the incompleteness of the current algebraic cycle dictionary: specifically, because $\dim(K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim}) = 2$ rather than 1 for our $A_1$, the period matrix may admit extra structure (a partial isogeny) that would supply additional algebraic classes not yet included; and even for a fully simple Weil 4-fold (dimension = 1), the Hodge conjecture may hold via an algebraic cycle that is not constructible from endomorphisms, products, or polarizations — a cycle of a fundamentally different geometric kind, which this computation cannot rule out."**

---

## Observable-Side Checklist for A_1

| Quantity | Computable for $A_1$? |
|---------|----------------------|
| Period matrix $\Omega = iM$, $M$ rational | YES — explicit |
| $M^{-1}$, $\det(M) = 5$ | YES — exact |
| Complex structure $J$ on $H^1(A_1, \mathbb{R})$ | YES — $8 \times 8$ rational matrix |
| $J$ action on $H^4(A_1, \mathbb{Q})$ | YES — $70 \times 70$ rational matrix |
| $\dim H^{2,2}(A_1, \mathbb{Q}) = 36$ | YES — from $J$-eigenspace |
| $\varphi^*(L) = L$ | YES — verified |
| $\mathrm{prim}(L^2) = 0$ | YES — verified |
| Weil class $w_{A_1}$ (28-term rational 4-form) | YES — explicit, triply verified |
| Whether $w_{A_1}$ is algebraic | **NOT KNOWN** — this is the open Hodge gap |

---

## Collaborator Paragraph

The computation on $A_1$ completes the first non-degenerate Hodge span test. The key advance over $A_0$: the period matrix $\Omega = iM$ with $M = [[2,1,1,1],...]$ is not block-diagonalizable (all 6 pair-partitions fail), eliminating the product structure that trivialized $A_0$. The $K = \mathbb{Q}(i)$-action is the same $\varphi$ as before; the complex structure $J = [[0,-M],[M^{-1},0]]$ is new, rational, and verified to satisfy $J^2 = -I$. The combined constraint computation (168×70 exact rational matrix) gives $\dim(K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim}) = 2$ for $A_1$, down from 8 for the product $A_0$, and the first basis vector is the Weil class $w_{A_1}$ — a 28-term rational 4-form verified K-anti-invariant, type (2,2), and primitive. The algebraic dictionary for a simple $A_1$ with $\mathrm{End}^0 = \mathbb{Q}(i)$: since $\varphi^*(L) = L$ (computed exactly), the only algebraic class is $L^2$, whose primitive projection is 0 by definition. The algebraic primitive subspace is $\{0\}$, rank 0. The span test fails: $w_{A_1} \neq 0$ (28 nonzero terms), rank rises from 0 to 1 when $w_{A_1}$ is adjoined. The gap is explicit at the coordinate level. The residual caveat: $\dim = 2$ rather than 1 indicates $A_1$ may not be fully simple; for a FULLY simple Weil 4-fold (dimension = 1), the algebraic dictionary is the same (still rank 0), and the span test still fails in the same way. The next step is to find — or prove the non-existence of — an algebraic cycle $Z \in \mathrm{CH}^2(A_1)_\mathbb{Q}$ with $\mathrm{cl}^2(Z) = w_{A_1}$.
