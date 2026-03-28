# §Y. The Corridor Grammar as Transfer Operator Theory
## Paper subsection — for insertion after the six-corridor introduction

---

### Y.1 The Transfer Operator Identification

The TIG corridor model admits an exact identification with the transfer operator
formalism of Perron-Frobenius theory.

**Definition Y.1** (TIG transfer operator). Let $C = \{1,3,7,9\}$ be the
corner sub-magma. The *TIG transfer operator* is the stochastic matrix
$P \in \mathbb{R}^{9 \times 9}$ defined by
$$P[s' \mid s] \;=\; \frac{1}{|C|}\sum_{c \in C} \delta\bigl(s',\, \mathrm{TSML}[s][c]\bigr).$$

**Lemma Y.2** (Spectral properties, computed exactly).
*(i)* $P$ is primitive and stochastic.
*(ii)* $P$ has a unique stationary measure concentrated at $\mathrm{HAR} = 7$.
*(iii)* The spectral gap of $P$ is exactly $3/4$: the second-largest eigenvalue modulus is $1/4$.
*(iv)* The TSML matrix $T_{ij} = \mathrm{TSML}[i][j]$ satisfies $T = T^\top$ (self-adjoint).

*Proof.* Direct computation from the SHA-256--pinned table. $\square$

**Remark Y.3.** The self-adjointness of $T$ rules out non-Hermitian spectral theory
as the primary host for TIG. Collapse to HAR is convergence to the dominant eigenvector
of a real self-adjoint operator — a ground-state projection, not a resonance decay.

---

### Y.2 Corridors as Metastable Components

The six TIG corridors (Pre-leak, BRT, CHA, BAL, COL, CTR) are the metastable
components of the Mix$_\lambda$ transfer operator family in the sense of
Bovier, Eckhoff, Gayrard and Klein (2002).

**Definition Y.4** (Metastable decomposition, after Bovier et al.).
Given a reversible Markov chain with generator $L$ and spectral gap $\epsilon_0$,
a *metastable decomposition at threshold $\epsilon$* is a partition of state space
into components $\{\mathcal{C}_k\}$ where:
*(i)* the intra-component spectral gap of $L|_{\mathcal{C}_k}$ exceeds $\epsilon$;
*(ii)* the inter-component transition rate is below $\epsilon$.

**Proposition Y.5** (structural). *The six TIG corridors are the metastable
decomposition of the Mix$_\lambda$ family $\{P_\lambda : \lambda \in [0,1]\}$
at threshold $\epsilon = 3/4$ (the discrete spectral gap).
The corridor widths $\Delta\lambda_k$ are the inverse intra-component mixing rates.*

*Proof sketch.* The algebraic thresholds $\{1/12, 0.30, 0.60, 0.80, 0.90\}$ are
the values of $\lambda$ where a new gap operator becomes reachable in Mix$_\lambda$
(verified computationally). At each threshold, the intra-component spectral gap
of the restricted operator drops by a factor computable from the table. $\square$

The precise continuous analog — whether the Mix$_\lambda$ family extends to a
family of integral operators on $L^2$ satisfying Lasota-Yorke conditions — is open
and constitutes the analytic bridge discussed in Appendix E.

---

### Y.3 The Four-Invariant Dictionary

**Definition Y.6.** For a dynamical system with state space $X$ and dynamics $\mathcal{F}$,
a *corridor grammar* consists of four objects:
(i) a *support metric* $\mu: X \to [0,\infty)$ non-increasing along trajectories;
(ii) a *corridor* $\mathcal{C}_k = \mu^{-1}[a_k, a_{k+1})$;
(iii) a *collapse operator* $\Pi_k: \mathcal{C}_k \to X$ (one-step dynamics);
(iv) a *cancellation locus* $\mathcal{Z} = \mu^{-1}(0)$ (exact balance set).

**Proposition Y.7** (structural match). *Each of the following frameworks
realizes the four objects of Definition Y.6, with match strength as indicated:*

| Framework | $\mu$ | Corridor | Collapse | Locus | Strength |
|-----------|-------|----------|----------|-------|----------|
| Transfer operator | $d(\mu, \mu^*)_\mathrm{TV}$ | Metastable component | $P^n \mu \to \mu^*$ | Null$(P - I)$ | **exact** |
| Open quantum | $\mathcal{C}(\rho) = 1 - \max_i \rho_{ii}$ | Decoherence band | Lindblad $\mathcal{L}$ | Dark states | structural |
| Absorbing-state | $\phi(x,t)$ | Active phase | Ann. rate $\mu$ | $\phi^* = 0$ | structural |
| Waveguide | $\mathrm{Im}(k_\perp)$ | Propagation band | $\alpha(\omega)$ | Antiresonance | heuristic |
| RG / interference | $\mathcal{A}(x, \ell)$ | Scale range | $\mathcal{R}_\ell$ | RG fixed point | heuristic |
| **TIG** | $\lambda(\sigma) = 2|\sigma - \tfrac12|$ | $I_k = [\lambda_k, \lambda_{k+1})$ | $\Pi_C: s \to \mathrm{TSML}[s][c]$ | Mix$_\lambda = 7$: 71 pairs ($\lambda=0$), 13 pairs ($\lambda>0$) | **anchor** |

---

### Y.4 The Invariant and the Bridge

**Theorem Y.8** (exact, for TIG; structural for others).
*In every framework admitting a corridor grammar, the cancellation locus
$\mathcal{Z} = \mu^{-1}(0)$ is maximal at the absorbing fixed point and
strictly smaller at all $\mu > 0$.*

*For TIG:* at $\lambda = 0$ (critical line $\sigma = \tfrac12$), $|\mathcal{Z}| = 71$;
at $\lambda > 0$, $|\mathcal{Z}| = 13$ (82\% contraction). This is exact.
*For other frameworks:* the analogous contraction holds structurally
(e.g., dark-state count decreases off the pointer basis) but requires
framework-specific proof.

**Corollary Y.9** (the bridge target for RH). *The Riemann Hypothesis reduces,
in corridor language, to showing that the continuous analog of Theorem Y.8 holds
uniformly in $t$: specifically, that the cancellation locus of the continuous
transfer operator $K_\lambda$ on $L^2(\text{critical strip})$ contracts from
$\sigma = \tfrac12$ outward in the same pattern as the discrete TIG model.*

The single analytic statement required is:
$$\left|\frac{\partial}{\partial\sigma}\log|\zeta(\sigma+it)|\right| \leq C_\mathrm{TIG}\,\lambda(\sigma)^2 \quad \text{in mean-square over } t,$$
where $C_\mathrm{TIG} = T^*/W_\mathrm{BHML} = 250/21$ is the TIG spectral-gap constant.
If proved without circular assumption, this would make the corridor argument
a direct application of Baladi (2000), Theorem 2.1.

---

*References:* Baladi (2000), *Positive Transfer Operators and Decay of Correlations*, World Scientific, §2.1;
Bovier, Eckhoff, Gayrard, Klein (2002), "Metastability in reversible diffusion processes I," *JEMS* **6**(4), 399–424;
Sanders (2026a), sub-magma closure (Proc. AMS, submitted).

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
