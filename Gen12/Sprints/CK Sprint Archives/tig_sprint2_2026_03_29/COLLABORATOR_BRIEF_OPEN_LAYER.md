# Open Layer: Deployment Faithfulness for a Type-(9, 3, 6, 3/4) Grammar
## One-Page Collaborator Brief

*Brayden Sanders / 7Site LLC | March 2026*
*For: Analytic number theorists, operator theorists, spectral dynamicists*

---

## The Finite Side Is Closed

We have a finite object — a forced integer grammar on 9 states — that has been proved to simultaneously realize four standard structures:

1. **Absorbing sofic shift** with transient class $G=\{2,4,5,6,8\}$, absorbing class $C=\{1,3,7,9\}$, filtration depth 3 (sub-magma closure, proved; *Proc. AMS* note, submitted)

2. **Perron-Frobenius transfer operator** with uniform spectral gap $\gamma(P_\lambda) \geq 1/4$ for all $\lambda \in [0,1]$, and $\gamma(P_0) = 3/4 = 1 - 1/\varphi(10)$ exactly (eigendecomposition, 51 values, machine-verified; Gen10.14 commit d3db298)

3. **Finite-height return tower** with base $\{\mathrm{HAR}\}=\{7\}$, tail rate $\rho(Q) = 1/4 = 1 - \gamma(P_0)$, max expected return $5/3$ steps (exact Markov calculation)

4. **Arithmetic inverse-limit scaffold** with corner set $C = (\mathbb{Z}/10\mathbb{Z})^*$ stable at every level of the base-10 tower; $\gamma$ formula stable under base-change within $\varphi(b)=4$ class ($b \in \{5,8,10,12\}$)

All four are verified by exact computation. SHA-256 of the table is pinned at `7726d8a6...`; 65/65 unit tests pass.

---

## The Open Layer

We propose deploying this finite grammar into the critical strip via $\lambda(\sigma) = 2|\sigma - \tfrac12|$.

**The claim we cannot yet prove:** The continuous deployment $\{K_\lambda\}$ on $L^2(\text{critical strip})$ inherits the spectral gap of the discrete prototype, and the analytic function $\log|\zeta(\sigma+it)|$ satisfies a drift bound consistent with the grammar's gap constant.

Precisely, we need either of:

**(A) Transfer operator condition** (Gouëzel-Liverani 2006 route):
The family $\{K_\lambda\}$ satisfies Lasota-Yorke inequalities $\|K_\lambda f\|_V \leq \alpha\|f\|_V + \beta\|f\|_1$ with $\alpha < 1$ uniform in $\lambda$. If so, gap-positivity follows from their Theorem 1.1.

**(B) Direct analytic condition** (Appendix E route):
$$\left|\frac{d}{d\sigma}\log|\zeta(\sigma+it)|\right| \leq C_\mathrm{TIG}\cdot\lambda(\sigma)^2 \quad \text{in mean-square over } t$$
where $C_\mathrm{TIG} = 250/21 \approx 11.905$. Empirically: $C_\mathrm{emp} \leq 11.023$ on all tested heights to $t \approx 300$; margin 7.4%.

Either condition would close the gap. They are independent routes.

---

## Why This Is Not Circular

The finite side does not assume RH. It proves algebraic properties of a 9-element table.

The deployment into the critical strip is a *proposed* realization — it may or may not be faithful. RH is equivalent to faithful deployment. We are not assuming RH to prove RH; we are asking whether a specific finite grammar has a specific kind of infinite realization.

The gap at $\sigma = \tfrac12$ is large (71 cancellation pairs at $\lambda=0$, only 13 at $\lambda>0$, 82% contraction) because the grammar algebraically distinguishes the critical line. Whether the analytic function $\zeta$ inherits this distinction is the open question.

---

## What We Are Looking For

A collaborator who can:

1. Evaluate whether the Lasota-Yorke conditions for $\{K_\lambda\}$ on $L^2(\text{critical strip})$ are achievable, and identify the appropriate function space (BV, anisotropic Banach, Sobolev)

2. Or alternatively: provide or cite a mean-square upper bound on $\mathrm{Re}(\zeta'/\zeta)(\sigma+it)$ of the form $O(\lambda^2)$ or $O(\lambda^\alpha)$ for $\alpha > 1$, without assuming RH as input

3. Advise on whether the Young tower structure (finite-height, return rate $1/4$) has a natural continuous analog in the critical strip

The discrete algebra is stable and machine-verified. The continuous bridge is the one open question.

---

**Contact / repository:** `github.com/TiredofSleep/ck` (Gen10.14, tag v1.3)
**Papers:** Sub-magma closure → *Proc. AMS* (submitted); Halving Lemma → arXiv math.NT (in preparation)

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
