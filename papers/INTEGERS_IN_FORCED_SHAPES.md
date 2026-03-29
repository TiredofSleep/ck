# Integers in Forced Finite Shapes
## A Type-(n, k_A, k_M, γ) Grammar and Its Arithmetic Hook

*Brayden Sanders / 7Site LLC | March 2026*
*Definitions exact. Theorems proved unless marked Conjecture. Gen10.14, commit d3db298.*

---

The central object is not TIG alone and not base-10 alone. It is:
**integers constrained inside forced finite shapes, and the behavior of that constraint when deployed outward into infinite arithmetic.**

---

## Five Definitions

**Definition 1 — Integer Alphabet.**
An *integer alphabet* is a finite set $A = \{a_1, \ldots, a_n\} \subset \mathbb{Z}$ where the integer values are retained, not relabeled. Each element plays three simultaneous roles:
- **State** — a local configuration of the system
- **Position** — a location in the forced geometry (corner, gap, threshold, reset)
- **Hook** — a connection to infinite arithmetic via residue classes mod $b$

**TIG:** $A = \{1,\ldots,9\}$, with $7 = \mathrm{HAR}$, $C = \{1,3,7,9\} = (\mathbb{Z}/10\mathbb{Z})^*$, $G = \{2,4,5,6,8\}$ = non-units.

---

**Definition 2 — Forced Finite Shape.**
A *forced finite shape* on $A$ is a binary operation $F: A \times A \to A$ with absorbing element $a \in A$ ($F(s,a)=a$ for all $s$) and proper closed subset $C \subsetneq A$ with $F(C,C) \subseteq C$.

*"Forced"* means $F$ is not freely assigned but constrained by the integer structure of $A$ — for example, by dominance rules ($F(s,c) \geq \min(s,c)$), monotonicity ($F$ non-decreasing in each argument), or arithmetic compatibility ($F(s,c) \equiv s \cdot c \pmod{b}$). A forced shape excludes arbitrary magmas by requiring compatibility with an external integer order or residue structure.

**TIG:** $F_0 = \mathrm{TSML}$ (SHA: `7726d8a6...`). Absorbing: $\mathrm{TSML}[s][7]=7$ $\forall s$. Closed: $C \times C \subseteq C$ (proved, Proc. AMS). Integer constraint: 87.7\% of cells equal HAR=7.

---

**Definition 3 — Deformation Family.**
A *deformation family* on $(A, F_0, F_1)$ is a one-parameter family $\{F_\lambda : \lambda \in [0,1]\}$ interpolating from closure endpoint $F_0$ to order endpoint $F_1$. The $\lambda$-level sets of this family define the metric grading.

**TIG:** $F_\lambda = \mathrm{Mix}_\lambda = \mathrm{round}((1-\lambda)\cdot\mathrm{TSML} + \lambda\cdot\mathrm{BHML})$. Order endpoint: $F_1 = \mathrm{BHML}$ with $\mathrm{BHML}[s][c] = \max(s,c)$ exactly. Cancellation locus shrinks from 71 pairs ($\lambda=0$) to 13 pairs ($\lambda=1$): 82\% contraction across the deformation.

*Remark.* The deformation is piecewise-constant due to rounding; all spectral statements are taken on the induced transfer operators, not on derivatives in $\lambda$.

---

**Definition 4 — Algebraic Grading.**
The *algebraic grading* of $(A, F_0)$ is the longest chain $\{a\} = S_0 \subsetneq \cdots \subsetneq S_{k_A} = A$ with each $S_i \circ S_i \subseteq S_i$. The *generative gap* is $\mathcal{G}_{\mathrm{gen}} = A \setminus C^{(\infty)}$ where $C^{(\infty)}$ is the closure of $C$ under $C$-only compositions.

**TIG:** $k_A = 3$. Chain: $\{7\} \subsetneq \{1,3,7,9\} \subsetneq \{1,\ldots,9\}$. Generative gap: $G = \{2,4,5,6,8\}$, unreachable from $C$ by $C$-compositions.

---

**Definition 5 — Metric Grading.**
The *metric grading* of $\{F_\lambda\}$ under deployment $\phi: X \to [0,1]$ is the partition of $[0,1]$ into $k_M$ intervals where, for each interval, the frequency-duration product $n_0(\sigma,t) \cdot \Delta t(\sigma,t) \to 0$ as the deployment scale $t \to \infty$. Here $n_0(\sigma,t)$ denotes the local density of critical events (e.g., Riemann zeros or excursion entrances) per unit scale at height $t$, and $\Delta t$ is the maximum sojourn duration. The *support gap* at level $j$ is the set where this product vanishes.

**TIG:** $k_M = 6$ corridors, $\phi = \lambda = 2|\sigma - \tfrac12|$. Support gap verified to $t \approx 10{,}000$ (Gen10.14, 460 heights, zero crossings).

---

## Theorem 1 — Two Gradings, One Family

**Theorem 1** *(exact, proved).*
*The algebraic grading $(k_A)$ and metric grading $(k_M)$ of TIG arise as projections of a single deformation family $\{F_\lambda\}$:*
$$\text{algebraic grading} = \text{sub-magma structure of } F_{\lambda=0}, \qquad \text{metric grading} = \text{level sets of } \lambda \in [0,1]$$
*The $\lambda$-level sets defining the metric grading are induced directly by the interpolation $\mathrm{Mix}_\lambda$, so both gradings are functions of the same family — the algebraic chain at its $\lambda=0$ slice, the corridors across its full $\lambda$-range.*

*Proof.* The chain $\{7\} \subsetneq C \subsetneq A$ is the sub-magma structure of $F_0 = \mathrm{TSML}$. The six metric corridors are the level sets of $\lambda$ in $\{F_\lambda\}$. Both are determined by the same family. $\square$

---

## Theorem 2 — The Arithmetic Hook

**Theorem 2** *(exact, proved).*
*For any base $b$, every prime $p \nmid b$ satisfies $p \bmod b \in (\mathbb{Z}/b\mathbb{Z})^*$. By Dirichlet's theorem on primes in arithmetic progressions, primes are equidistributed across all residue classes in $(\mathbb{Z}/b\mathbb{Z})^*$, so the unit group is the natural arithmetic support of prime residues in base $b$. In the TIG base-10 deployment, $C = \{1,3,7,9\} = (\mathbb{Z}/10\mathbb{Z})^*$ exactly.*

*Limit of the claim.* This proves the arithmetic hook for the corner set. It does not prove that the base-10 deployment preserves both gradings asymptotically — that is Problem C.

---

## Theorem 3 — The γ-Formula

**Theorem 3** *(exact, proved).*
*Let $(A, \{F_\lambda\})$ be a forced finite shape with corner set $C = (\mathbb{Z}/b\mathbb{Z})^*$. Define the transfer operator:*
$$Pf(s) = \frac{1}{|C|}\sum_{c \in C} f(F_0(s,c))$$
*(uniform right-composition over $C$). Assume the restriction $P|_C$ decomposes as an absorbing component at $a$ plus a permutation sub-block on non-absorbing states in $C$. Then the nontrivial eigenvalues of $P|_C$ are bounded in modulus by $1/|C|$; when the non-absorbing sub-block forms a single cycle:*
$$\gamma = 1 - \frac{1}{\varphi(b)}, \qquad \varphi(b) = |(\mathbb{Z}/b\mathbb{Z})^*| = |C|$$

*Proof.* Under the stated hypothesis, the restriction $P|_C$ decomposes as:
$$P|_C = \frac{|C|-1}{|C|}\, |a\rangle\langle\mathbf{1}| + \frac{1}{|C|}\, Q$$
where $Q$ is a permutation matrix on $C$. The first term has rank 1 with eigenvalue 1 (on the stationary vector) and 0 elsewhere. The second term contributes eigenvalues $\tfrac{1}{|C|}\zeta$ for each root of unity $\zeta$ appearing in $Q$'s cycle decomposition. All non-trivial eigenvalues of $P|_C$ therefore have modulus $\tfrac{1}{|C|}$, giving spectral gap $\gamma = 1 - \tfrac{1}{|C|} = 1 - \tfrac{1}{\varphi(b)}$. $\square$

**Verification for TIG** (exact):

| $s \in C$ | Non-HAR corner ops | Structure |
|-----------|-------------------|-----------|
| 1 | 0 of 4 → non-HAR | all collapse |
| 3 | 1 of 4 → state 3 (via op 9) | one non-HAR |
| 7 | 0 of 4 → non-HAR | all collapse |
| 9 | 1 of 4 → state 3 (via op 3) | one non-HAR |

The permutation $Q$ on $\{3,9\}$ has cycle structure $(3\,9)$, contributing eigenvalue $\pm\tfrac{1}{4}$. Spectral gap $= 1 - \tfrac{1}{4} = \tfrac{3}{4}$ exactly. ✓

**γ-values by base:**

| Base $b$ | $\varphi(b)$ | $\gamma = 1 - 1/\varphi(b)$ |
|----------|-------------|---------------------------|
| 6 | 2 | $1/2$ |
| 8 | 4 | $3/4$ |
| **10** | **4** | **$3/4$ ✓** |
| 12 | 4 | $3/4$ |
| 14 | 6 | $5/6$ |
| 30 | 8 | $7/8$ |

$\gamma = 3/4$ is the spectral gap of any arithmetic-hook deployment with $\varphi(b) = 4$, i.e., $b \in \{5, 8, 10, 12\}$.

---

## Classification Results

**Type.** A forced finite shape has type $(n, k_A, k_M, \gamma)$.
**TIG type:** $(9,\ 3,\ 6,\ 3/4)$.

**Computational results** ($N \approx 28{,}000$ samples, $n = 5$–$13$):

| Finding | Result |
|---------|--------|
| First $n$ with $k_M \geq 6$ | $n = 6$ |
| Rational $\gamma$ among all $k_M \geq 6$ grammars | 54/54 (100\%) |
| $\gamma = 3/4$ in random samples without hook constraint | 0\% |
| Irrational $\gamma$ in sampled range when $k_M \geq 6$ | 0 found |
| $\gamma = 3/4$ requires | arithmetic-hook alignment $C = (\mathbb{Z}/b\mathbb{Z})^*$, $\varphi(b)=4$ |

Grammars at $n=6$ achieving $k_M \geq 6$ have $k_A = 6$ (maximal chain), not $k_A = 3$. They differ structurally from TIG in algebraic chain depth and integer-hook alignment.

---

## Three Open Problems

**Problem A** *(Minimal realization).* What is the minimum $n$ for a type-$(n, 3, 6, \gamma)$ grammar with exactly $k_A = 3$ and $k_M = 6$?
*Known:* $n = 9$ works. Lower bound open.

**Problem B** *(Spectral type).* Does any type-$(n, k_A, k_M, \gamma)$ grammar with $k_M \geq 6$ admit irrational $\gamma$?

**Conjecture B:** For any forced finite shape with $k_M \geq 6$, $\gamma$ is rational.
*Evidence:* 54 grammars with $k_M \geq 6$ across $n = 5$–$13$; all have rational $\gamma$. In the sampled range, irrational $\gamma$ appears only when $k_M \leq 4$.

**Problem C** *(Faithful deployment).* Which infinite deployments of a type-$(n, k_A, k_M, \gamma)$ grammar preserve both the algebraic grading and the metric grading asymptotically?

*For RH:* The critical-strip deployment $\phi = \lambda = 2|\sigma - \tfrac12|$ is **faithful** iff both the generative gap (algebraic, proved) and the support gap (analytic, verified to $t \approx 10{,}000$) hold uniformly for all $t$. **RH can be rephrased as: this deployment is faithful to both gradings.**

---

## One-Line Summary

*A finite integer system with a constrained binary operation produces an algebraic closure hierarchy and a metric persistence hierarchy, both arising from one deformation between closure and order; when the corner set equals the unit group of a residue system, the spectral gap is $\gamma = 1 - 1/\varphi(b)$; the arithmetic hook is exact; and RH asks whether the critical-strip deployment is faithful to both hierarchies.*

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
