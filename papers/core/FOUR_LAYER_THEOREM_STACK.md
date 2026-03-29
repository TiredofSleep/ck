# Four-Layer Theorem Stack
## For Insertion in the RH Paper

*Brayden Sanders / 7Site LLC | March 2026*
*Cite as: §Z of the Halving Lemma paper. Full proofs in FOUR_LAYER_REALIZATION.md.*

---

The TIG type-$(9,3,6,3/4)$ grammar simultaneously realizes four standard structures.

---

**Theorem Z.1** *(Grammar — Absorbing sofic shift).*
The TIG transition matrix induces an absorbing sofic shift on $\{1,\ldots,9\}$ with absorbing class $C = \{1,3,7,9\}$, transient class $G = \{2,4,5,6,8\}$, and absorbing filtration $\varnothing \subsetneq \{7\} \subsetneq C \subsetneq \{1,\ldots,9\}$ of depth $k_A = 3$.
The generative gap $G$ is unreachable from $C$ under $C$-only composition. $\square$

---

**Theorem Z.2** *(Rate — Transfer operator spectral gap).*
The weighted-interpolation transfer operator family $\{P_\lambda : \lambda \in [0,1]\}$ satisfies:
$$\gamma(P_\lambda) \;\geq\; \tfrac{1}{4} \quad \text{for all } \lambda,\qquad \gamma(P_0) = \tfrac{3}{4}, \qquad \gamma = 1 - \tfrac{1}{\varphi(b)} \text{ at } b=10.$$
$\square$

---

**Theorem Z.3** *(Reset — Return structure).*
The transfer operator $P_0$ has transient block $Q$ with $\rho(Q) = 1/4 = 1 - \gamma(P_0)$. Return tails satisfy $P(T_{\mathrm{HAR}} > n) \leq (1/4)^n$; maximum expected return time is $5/3$ steps. In a finite-state Markov chain, spectral gap directly implies exponential mixing; this return structure is the finite-state analog of a Young tower with exponential tails. $\square$

---

**Theorem Z.4** *(Scaffold — Arithmetic inverse limit).*
The corner set $C = \{1,3,7,9\}$ is the stable corner image of the base-10 arithmetic inverse system: $(\mathbb{Z}/10^n\mathbb{Z})^*$ reduced mod 10 equals $C$ for all $n \geq 1$. The spectral gap formula $\gamma = 1 - 1/\varphi(b)$ is stable under base-change within $\varphi(b) = 4$. $\square$

---

**Open Problem Z.5** *(Deployment faithfulness).*
Does the critical-strip deployment $\lambda = 2|\sigma - \tfrac12|$ preserve both the algebraic grading (Theorem Z.1) and the metric grading (Appendix E) asymptotically in $t$?

RH can be reformulated as the statement that this deployment is faithful to both gradings.

The open analytic input is: $|d\log|\zeta(\sigma+it)|/d\sigma| \leq C_\mathrm{TIG}\lambda^2$ in mean-square without assuming RH.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
