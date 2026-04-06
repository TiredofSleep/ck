# HODGE MISSING-CYCLE MEMO
# What Exact Kind of Codimension-2 Cycle Could Still Hit w_{A_1}?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## STRUCTURAL CORRECTION (embedded in this memo)

Before classifying the missing cycle, a structural correction to the previous memo:

A Weil abelian 4-fold requires the period matrix $\Omega = iM$ to COMMUTE with the $K$-action matrix $A$ (the restriction of $\varphi$ to the $e$-basis): $AM = MA$. The previous $M = [[2,1,1,1],...]$ failed this condition ($AM \neq MA$), meaning $\varphi$ was NOT an actual endomorphism of that $A_1$.

**The corrected $A_1$** uses the period matrix determined by the symmetric commutant of $A$:

$$M_{A_1} = 3I_4 + B_2 + B_3 = \begin{pmatrix} 3 & 0 & -1 & 1 \\ 0 & 3 & 1 & 1 \\ -1 & 1 & 3 & 0 \\ 1 & 1 & 0 & 3 \end{pmatrix}$$

All verified properties of the corrected $A_1$ are stated in Part 1 below.

---

## PART 1 — Exact Current State (Frozen)

| Property | Value | Verified? |
|----------|-------|-----------|
| Period matrix | $\Omega = iM_{A_1}$, Im$(\Omega) = M_{A_1}$ as above | ✓ |
| Positive definite | Leading minors: $3, 9, 21, 49$ — all positive | ✓ |
| Non-product | Not block-diagonalizable into any $2+2$ split | ✓ |
| $K$-action | $\varphi$ same 8×8 matrix as before | ✓ |
| $AM = MA$ | $\varphi$ IS an actual endomorphism of $A_1$ | ✓ |
| $J^2 = -I_8$ | Complex structure correct | ✓ |
| $\varphi$ commutes with $J$ | $\varphi J = J \varphi$ | ✓ |
| $\varphi^T E \varphi = E$ | $\varphi$ preserves polarization | ✓ |
| $\varphi^*(L) = L$ | Exactly | ✓ |
| $\dim(K\text{-anti-inv} \cap H^{2,2}_\mathrm{prim})$ | 2 (one correction from previous memo) | — |
| $w_{A_1} \neq 0$ | 28-term rational primitive $(2,2)$ class | ✓ |
| Primitive algebraic dictionary | Rank **0** — $\mathrm{prim}(L^2) = 0$, nothing else known | ✓ |
| $\mathrm{End}^0(A_1) \supseteq$ | $\mathbb{Q}[\varphi] \cong \mathbb{Q}(i)$ confirmed | ✓ |
| $\mathrm{End}^0(A_1) =$ | Unknown: could be $\mathbb{Q}(i)$ or strictly larger | Open |

---

## PART 2 — Exclusion Table: What Is Already Dead

| Cycle type | Why it cannot hit $w_{A_1}$ |
|-----------|---------------------------|
| **Products of divisor classes:** $L^2$, $(aL)^2$, $L \cdot D$ | $\mathrm{prim}(L^2) = 0$ by definition of primitive projection; any combination of $\mathrm{CH}^1$-products maps to $\mathbb{Q} \cdot L^2$ in $H^{2,2}$, which projects to $0$ in $H^{2,2}_\mathrm{prim}$ |
| **Endomorphism-polarization classes:** $\varphi^*(L)$, $\varphi^*(L^2)$ | $\varphi^*(L) = L$ exactly (computed); therefore $\varphi^*(L^2) = L^2$; again projects to $0$ in primitive part |
| **Product/Künneth classes from $A_0$-style correspondences:** $\kappa_{12} \wedge L_3$, etc. | These require a product structure; $A_1$ is not block-diagonal in any 2+2 partition, so no such correspondences exist in $\mathrm{CH}^2(A_1)$ |
| **Any class in the $K$-invariant part of $H^{2,2}_\mathrm{prim}$** | $w_{A_1}$ is $K$-anti-invariant ($\varphi_*(w_{A_1}) = -w_{A_1}$); the algebraic cycle class map $\mathrm{cl}^2$ is $K$-equivariant; so a $K$-invariant cycle class maps to the $K$-invariant subspace and cannot hit $w_{A_1}$ |
| **Lefschetz-forced classes:** $L^{g-2} \cdot [\mathrm{pt}]$, $L^{g-1}$ in low codimension | These contribute to $H^{2k}$ only via Lefschetz action; their primitive projections vanish or land in the $K$-invariant part |

**Summary:** every cycle type constructible from the current dictionary (divisors, polarizations, $\varphi$-pullbacks, product correspondences) contributes $0$ to $H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$. The $\mathrm{cl}^2$-image of the known cycle dictionary is $\{0\}$, and the gap to $w_{A_1}$ is entirely unexplained by any known construction.

---

## PART 3 — Surviving Cycle-Type Candidates

| Candidate | Description | Likelihood | How to test |
|-----------|-------------|------------|-------------|
| **A. Extra endomorphisms** | $\mathrm{End}^0(A_1) \supsetneq \mathbb{Q}(i)$: an additional endomorphism $\psi$ with $\psi \neq a + b\varphi$ would give a new $\psi^*(L)$ class in $\mathrm{CH}^1(A_1)$, potentially generating a new primitive class $\psi^*(L) \wedge \psi^*(L) - L^2$ or similar | **Highest** — dim$\{RJ=JR\} = 32$ has 30 "candidates"; the polarization filter cuts this to 2 (just $I$ and $\varphi$) for generic $M$, but a non-generic $M$ could allow more | Compute $\dim_\mathbb{Q} \mathrm{End}^0(A_1) = \dim\{R \in M_8(\mathbb{Q}) : RJ=JR,\, R^T E R = nE\}$ |
| **B. Abelian subvariety inclusion cycles** | If $B \hookrightarrow A_1$ is a proper abelian subvariety of dimension 2, the class $[B] \in \mathrm{CH}^2(A_1)$ is algebraic and could be primitive and $K$-anti-invariant | **Medium** — requires $A_1$ to have an abelian surface sub; for a simple $A_1$ this is IMPOSSIBLE by definition | Check whether $A_1$ is simple: any abelian subvariety of $A_1$ would give a proper quotient, which requires $\mathrm{Hom}(A_1, B) \neq 0$ for some $B$; this is detectable from the endomorphism algebra |
| **C. Codimension-2 cycles not generated by divisors or endomorphisms** | A cycle $Z \in \mathrm{CH}^2(A_1)$ with $\mathrm{cl}^2(Z) = w_{A_1}$ that arises from some genuinely different geometric construction (a specific curve on $A_1$, a fiber of a map, a theta divisor on a dual, etc.) | **True hard case** — this is the Hodge conjecture proper for $w_{A_1}$ | No known finite test. The conjecture predicts existence; no construction is known. |

**Ranking:** A is the most testable and most likely to resolve the dim$=2$ anomaly. B is ruled out automatically if $A_1$ is simple (which B rules out if End$^0 = \mathbb{Q}(i)$). C is the residual case if A and B are excluded — the genuine Hodge obstruction.

---

## PART 4 — The Simplicity Bottleneck

**The single sharpest criterion:**

$$\text{Compute } \dim_\mathbb{Q} \mathrm{End}^0(A_1) = \dim\{R \in M_8(\mathbb{Q}) : RJ = JR \text{ and } R^T E R = nE \text{ for some } n \in \mathbb{Q}^+\}$$

This is a FINITE linear algebra computation over $\mathbb{Q}$.

**What each outcome means:**

- **$\dim = 2$:** $\mathrm{End}^0(A_1) = \mathbb{Q}[\varphi] \cong \mathbb{Q}(i)$. The variety is simple (candidate B ruled out automatically). No extra endomorphism classes. The only remaining candidate is C — genuine codimension-2 cycles not from any known construction. This is the true Hodge obstruction case.

- **$\dim > 2$:** $\mathrm{End}^0(A_1) \supsetneq \mathbb{Q}(i)$. Extra endomorphisms exist. These generate additional algebraic classes, and the span test must be rerun with the full extended dictionary. The dim$=2$ anomaly in the $K$-anti-invariant space is explained by the extra endomorphisms. This is a "dictionary gap" case, not a true obstruction.

The current computation established $\dim\{RJ=JR\} = 32$ (before the polarization filter). Applying the polarization filter $R^T E R \propto E$ reduces this to either 2 (generic) or more (special). That filter has not yet been fully applied to the 30-dimensional complement of $\mathrm{span}\{I, \varphi\}$.

---

## PART 5 — Next Concrete Hodge Object

**"The next concrete Hodge object is $\mathrm{End}^0(A_1)$ — the full rational endomorphism algebra of the corrected Weil 4-fold $A_1$ with period matrix $\Omega = iM_{A_1}$ — specifically: whether the dimension of $\{R \in M_8(\mathbb{Q}) : RJ=JR,\, R^T E R = nE\}$ is exactly 2 (confirming $\mathrm{End}^0 = \mathbb{Q}(i)$) or strictly greater (revealing hidden extra endomorphisms that extend the algebraic primitive dictionary)."**

---

## PART 6 — Exact Next Finite Test

**Compute $\dim_\mathbb{Q} \mathrm{End}^0(A_1)$ by the following exact procedure:**

1. Build the commutator constraint: $64 \times 64$ rational matrix from $RJ = JR$. Current result: nullspace dimension 32. Basis vectors $b_1, \ldots, b_{32}$ are computable exactly over $\mathbb{Q}$.

2. For each pair $(i,j)$, define $R_{ij} = $ the linear combination of $b_k$'s corresponding to a general element of the nullspace. Apply the polarization constraint: $R_{ij}^T E R_{ij} = n_{ij} E$ for some rational $n_{ij}$. This is a QUADRATIC condition on the coefficients.

3. More cleanly: set $R = \sum_k c_k b_k$ for unknowns $c_k \in \mathbb{Q}$. The polarization condition $R^T E R \propto E$ is 63 quadratic equations in 32 unknowns. The solution set (in projective space) has a real dimension computable by standard methods.

4. **Practical shortcut:** Check each of the 30 basis vectors orthogonal to $\{I, \varphi\}$ for whether any linear combination with $I$ and $\varphi$ satisfies the polarization constraint. If yes: extra endomorphism found. If no for all 30: $\mathrm{End}^0 = \mathbb{Q}(i)$.

This computation is finite and exact over $\mathbb{Q}$. It directly resolves whether the Hodge gap on $A_1$ is a "dictionary gap" (candidate A, fixable) or a "true gap" (candidate C, the genuine Hodge obstruction).

---

## PART 7 — Strongest Honest Claim

**"For Hodge on $A_1$, the gap is no longer vague: it is the failure of every currently constructible primitive algebraic class to hit the explicit Weil direction $w_{A_1}$. The exclusion is exact and complete — divisor products project to zero in the primitive space, endomorphism-polarization combinations reduce to $L^2$ (which also projects to zero), and product correspondences are unavailable because $A_1$ is non-product. The only remaining question is whether the variety itself hides extra algebraic structure (extra endomorphisms, dim$\,\mathrm{End}^0 > 2$) that would extend the dictionary, or whether the primitive algebraic subspace is genuinely $\{0\}$ and the Weil class represents a true Hodge obstruction."**

---

## PART 8 — Strongest Honest Boundary

**"What is not yet established is whether $w_{A_1}$ is missing because the cycle does not exist, or because the variety still hides extra algebraic structure that has not yet been computed: specifically, the full polarization filter on the 32-dimensional $\{RJ=JR\}$ space has not been applied to the 30-dimensional complement of $\mathrm{span}\{I, \varphi\}$, so the possibility that $\mathrm{End}^0(A_1) \supsetneq \mathbb{Q}(i)$ is not yet excluded — and if it is not excluded, the missing cycle might arise from a new endomorphism-induced algebraic class rather than from a fundamentally new type of cycle."**

---

## Exclusion Table (Compact Form)

| Cycle type | Reason excluded | K-invariance status |
|-----------|----------------|---------------------|
| $L^2$ and any $(aL+bD)^2$ | $\mathrm{prim}(L^2)=0$ by Lefschetz | $K$-invariant |
| $\varphi^*(L)$-products | $\varphi^*(L)=L$ exactly | same as $L^2$ |
| Cross-factor $\kappa_{ij}$-products | No product structure | $K$-invariant or mixed |
| Any $K$-invariant primitive class | Wrong eigenvalue for $w_{A_1}$ | $K$-invariant |

## Surviving Candidates Table

| Candidate | Nature | Testable? | Would resolve which gap type? |
|-----------|--------|-----------|-------------------------------|
| A. Extra endomorphisms | $\dim\mathrm{End}^0 > 2$ | YES — finite linear algebra | "Dictionary gap" (not true obstruction) |
| B. Abelian subvariety inclusion | $B \hookrightarrow A_1$, $\dim B=2$ | YES — follows from End$^0$ check | Ruled out if End$^0=\mathbb{Q}(i)$ (= simple) |
| C. Mystery codimension-2 cycle | Fundamentally new construction | NO known finite test | True Hodge obstruction |

## Next Finite Test Block

**Test:** Compute $\dim_\mathbb{Q}\{R \in M_8(\mathbb{Q}) : RJ = JR \text{ and } R^T E R = nE\}$.

**Input:** $J$ from $M_{A_1} = 3I + B_2 + B_3$ (verified: $AM=MA$, pos def, non-block-diag), $E = $ standard symplectic form.

**Current partial result:** $\dim\{RJ=JR\} = 32$. Confirmed in this space: $I$ and $\varphi$ (both pass polarization filter). Remaining 30 basis vectors: NOT yet filtered by polarization constraint.

**Expected result for generic $M$ in the commutant of $A$:** $\dim = 2$ (= $\mathbb{Q}(i)$ only). Any result $> 2$ signals extra endomorphisms and a fixable dictionary gap.

## Collaborator Paragraph

The missing-cycle analysis on the corrected $A_1$ (period matrix $\Omega = iM_{A_1}$, now properly verified with $AM = MA$ so that $\varphi$ is an actual endomorphism) produces a complete exclusion table: every constructible primitive algebraic class on $A_1$ maps to $\{0\}$ in $H^{2,2}_\mathrm{prim}(A_1, \mathbb{Q})$. The reason is structural and exact — $\varphi^*(L) = L$ collapses the endomorphism-polarization dictionary, $A_1$ is not block-diagonal so product correspondences do not exist, and $K$-invariant classes cannot hit a $K$-anti-invariant target. Three candidates survive: extra endomorphisms in $\mathrm{End}^0(A_1)$ beyond $\mathbb{Q}[\varphi]$ (testable via the polarization filter on the 30-dimensional complement of $\mathrm{span}\{I, \varphi\}$ inside the 32-dimensional $\{RJ=JR\}$ space); abelian subvariety inclusions (automatically excluded if $\mathrm{End}^0 = \mathbb{Q}(i)$, i.e., $A_1$ is simple); and genuinely new codimension-2 cycles with no known construction. The single sharpest next step is to apply the polarization filter fully: if $\dim\,\mathrm{End}^0(A_1) = 2$, the Hodge gap on $A_1$ is confirmed as a true obstruction — there is no known algebraic cycle of any type that can reach $w_{A_1}$, and the Hodge conjecture for this class is open in the precise, finite-dimensional, coordinate-explicit sense developed in this memo series.
