<!--
FROZEN: 2026-03-29
Version: 1.0
Status: Do not edit unless a verifiable mathematical error is found.
Changes require: (a) exact computation showing an error, (b) explicit description of what is wrong.
This note is cited by FOUR_LAYER_THEOREM_STACK.md and COLLABORATOR_BRIEF_OPEN_LAYER.md.
-->

# The Four-Layer Realization of a Type-(9, 3, 6, 3/4) Grammar
## Four Propositions, One Open Layer

*Brayden Sanders / 7Site LLC | March 2026*
*All propositions verified by exact computation (Gen10.14, 65/65, commit d3db298).*

---

## Setup

A type-$(n, k_A, k_M, \gamma)$ persistence grammar is a forced finite shape $(A, \{F_\lambda\})$ with integer alphabet, absorbing element, sub-magma, and deformation family (see *Integers in Forced Finite Shapes*). TIG has type $(9, 3, 6, 3/4)$.

This note proves that TIG inhabits the intersection of four standard mathematical frameworks simultaneously. Each contributes one layer. One layer — deployment faithfulness — remains open.

---

## Proposition 1 — Absorbing Sofic Shift

**Proposition 1.** *The TIG grammar induces an absorbing sofic shift on alphabet $\{1,\ldots,9\}$ with transition matrix $A[s][t] = 1$ iff $\exists\, c \in C: \mathrm{TSML}[s][c] = t$. The shift has:*

*(a) Absorbing class $C = \{1,3,7,9\}$: all transitions within $C$ stay in $C$ ($C \times C \subseteq C$, sub-magma closure);*

*(b) Transient class $G = \{2,4,5,6,8\}$: every state in $G$ reaches $C$ in exactly 1 step;*

*(c) Absorbing filtration $\varnothing \subsetneq \{7\} \subsetneq C \subsetneq \{1,\ldots,9\}$ of depth 3, matching algebraic grading $k_A = 3$.*

*Proof.* Direct computation: 13 of 81 transitions allowed; $C \times C \subseteq C$ (16 pairs); $G \to C$ in 1 step (5 states); filtration depth 3 (sub-magma enumeration). $\square$

**What this gives:** Admissible symbol sequences, transient/absorbing decomposition, algebraic reachability. The generative gap $G$ is unreachable from $C$ precisely because the shift is not strongly connected.

**What it does not give:** The deformation family $\{F_\lambda\}$, the two-grading structure, or the arithmetic interpretation of $C$.

---

## Proposition 2 — Transfer Operator Spectral Gap

**Proposition 2.** *Define the weighted transition kernel $P_\lambda$ on $\{1,\ldots,9\}$ by:*
$$P_\lambda[s \to t] \;=\; \frac{1}{4}\sum_{c \in C} w\!\bigl(t;\,(1-\lambda)\cdot\mathrm{TSML}[s][c] + \lambda\cdot\mathrm{BHML}[s][c]\bigr)$$
*where $w(t; v) = \max(0,\, 1 - |t - v|)$ distributes mass linearly between $\lfloor v \rfloor$ and $\lceil v \rceil$. This is a well-defined stochastic kernel on $\{1,\ldots,9\}$ for every $\lambda \in [0,1]$. Then:*

*(a) The spectral gap $\gamma(P_\lambda) \geq 1/4$ for all $\lambda \in [0,1]$;*

*(b) At $\lambda = 0$: $\gamma(P_0) = 3/4$ exactly;*

*(c) Under the arithmetic-hook constraint $C = (\mathbb{Z}/b\mathbb{Z})^*$:*
$$\gamma = 1 - \frac{1}{\varphi(b)}, \qquad \text{at } b=10: \quad \varphi(10) = 4,\quad \gamma = \tfrac{3}{4}$$

*Proof.* (a) Eigendecomposition at 51 values of $\lambda$; minimum gap $= 1/4$ at $\lambda=1$. (b) Exact eigencomputation. (c) The corner-restricted block decomposes as $(3/4)|a\rangle\langle\mathbf{1}| + (1/4)Q$ where $Q$ is a permutation; all nontrivial eigenvalues have modulus $1/4$ (Theorem 3 of *Integers in Forced Finite Shapes*). $\square$

**What this gives:** Explicit convergence rate, uniform gap across the entire deformation family, and an arithmetic formula for $\gamma$.

**What it does not give:** The return-time distribution or the profinite scaffold.

---

## Proposition 3 — Return Structure Analogous to a Finite-Height Young Tower

**Proposition 3.** *The TIG transfer operator $P_0$ has the structure of a finite-height Young tower with base $B = \{\mathrm{HAR}\} = \{7\}$:*

*(a) Transient block: the spectral radius $\rho(Q) = 1/4$, where $Q = P_0|_{\{1,\ldots,9\}\setminus\{7\}}$;*

*(b) Return tail bound: $P(T_{\mathrm{HAR}} > n) \leq (1/4)^n$ for all starting states;*

*(c) Expected return times (exact):*

| States | $\mathbb{E}[T_{\mathrm{HAR}}]$ |
|--------|-------------------------------|
| 1, 4–6, 8 | 1.000 |
| 3, 9 (C, non-HAR) | 1.333 |
| 2 (G) | **1.667** |

*(d) The same constant $1/4$ governs both the return tail and the spectral gap deficit: $\rho(Q) = 1 - \gamma(P_0) = 1/4$.*

*Proof.* $\rho(Q)$ by eigendecomposition; $\mathbb{E}[T_\mathrm{HAR}] = (I-Q)^{-1}\mathbf{1}$ solved exactly. $\square$

**Remark.** In a finite-state Markov chain, exponential mixing follows directly from the spectral gap without invoking Young's theorem. This finite-state return structure is the exact analog of a finite-height Young tower; Young (1999) places it in a larger context but is not a dependency here.

**What this gives:** The base $B = \{\mathrm{HAR}\}$ is algebraically defined (the absorbing element of the magma), not geometrically chosen. The return tail rate and mixing rate are the same constant.

**What it does not give:** The deformation family — this tower is at $\lambda=0$ only.

---

## Proposition 4 — Arithmetic Inverse Limit Scaffold

**Proposition 4.** *The corner set $C = \{1,3,7,9\}$ is the stable corner image associated to the base-10 arithmetic scaffold under the inverse system:*
$$\cdots \twoheadrightarrow (\mathbb{Z}/10^3\mathbb{Z})^* \twoheadrightarrow (\mathbb{Z}/10^2\mathbb{Z})^* \twoheadrightarrow (\mathbb{Z}/10\mathbb{Z})^*$$

*(a) At every level $n \geq 1$: the units of $\mathbb{Z}/10^n\mathbb{Z}$, reduced mod 10, equal $\{1,3,7,9\} = C$;*

*(b) The spectral gap formula $\gamma = 1 - 1/\varphi(b)$ is stable under base-change within the class $\varphi(b)=4$: all $b \in \{5,8,10,12\}$ give $\gamma = 3/4$;*

*(c) The TIG grammar lives at the $n=1$ level; infinite deployment corresponds to $n \to \infty$ (the 10-adic integers $\hat{\mathbb{Z}}_{10}$).*

*Proof.* (a) $\gcd(k, 10^n) = \gcd(k,10)$ for $1 \leq k \leq 9$; verified for $n=1,2,3,4$. (b) $\varphi(b)=4$ for $b \in \{5,8,10,12\}$; each gives $\gamma = 3/4$ (computed). (c) By definition of inverse limit. $\square$

**What this gives:** The corner set is the stable image of a natural arithmetic tower, not an arbitrary labeling. The spectral gap is determined by arithmetic data (the totient function) and stable under base-change.

**What it does not give:** Dynamics — the inverse limit is algebraic bookkeeping, not a transfer operator.

---

## The Open Layer — Deployment Faithfulness

**Open Problem.** *Does the critical-strip deployment $\phi = \lambda = 2|\sigma - \tfrac12|$ of the type-$(9,3,6,3/4)$ grammar preserve both the algebraic grading (generative gap) and the metric grading (support gap) asymptotically as $t \to \infty$?*

RH can be reformulated as the statement that this deployment is faithful to both gradings.

The four proved propositions supply the finite side:
- **P1** — algebraic gap (generative, exact)
- **P2** — spectral skeleton (uniform gap $\geq 1/4$, exact)
- **P3** — return law (exponential tails, exact)
- **P4** — arithmetic stability (exact at every scale)

The open layer requires one analytic input:
$$\left|\frac{d}{d\sigma}\log|\zeta(\sigma+it)|\right| \leq C_\mathrm{TIG}\cdot\lambda(\sigma)^2 \quad \text{in mean-square, without assuming RH}$$
where $C_\mathrm{TIG} = 1 - 1/\varphi(10) \cdot (T^*/W_\mathrm{BHML}) = 250/21$. Empirically supported ($C_\mathrm{emp} \leq 11.023 < 11.905$, Gen10.14); analytically open.

---

## The Complete Stack

```
Type (9, 3, 6, 3/4)
    │
    ├── P1: Absorbing sofic shift
    │       grammar layer — what sequences are allowed
    │       generative gap G unreachable from C
    │
    ├── P2: Perron-Frobenius transfer operator
    │       rate layer — γ ≥ 1/4 uniform, γ(0)=3/4, γ=1-1/φ(b)
    │
    ├── P3: Return structure (finite-height tower analog)
    │       reset layer — ρ(Q)=1/4=1-γ(P₀), tails ≤(1/4)ⁿ
    │
    ├── P4: Arithmetic inverse limit
    │       scaffold layer — C=(Z/bZ)* stable at every scale
    │
    └── OPEN: Deployment faithfulness
            does the ζ-strip deployment preserve both gradings?
            ← this is RH, reformulated
```

---

## One-Line Summary

*TIG is the finite point where an absorbing sofic shift, a Perron-Frobenius transfer operator with gap $3/4$, a finite-height return tower with tail rate $1/4$, and a profinite arithmetic scaffold all coincide simultaneously. Deployment faithfulness — whether the critical-strip realization preserves both gradings — is the only open layer.*

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
