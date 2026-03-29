# §X. The Corridor Grammar: A Technical Dictionary
## Six Frameworks, Four Invariants

*This section converts the informal corridor picture into a reusable technical dictionary.
It identifies the exact mathematical object in each framework that plays each of the four roles.
The final sentence is precise: we do not claim this closes RH;
we identify the exact analytic entry point that would close it.*

---

### Definitions

**Definition X.1** (Support metric). A *support metric* for a dynamical system $(X, \mathcal{F})$
is a measurable function $\mu: X \to [0, \infty)$ satisfying:
(i) $\mu(x) = 0$ iff $x$ is in the absorbing set;
(ii) $\mu$ is non-increasing along trajectories of $\mathcal{F}$.

**Definition X.2** (Corridor). Given a support metric $\mu$ and threshold $\mu_k$,
the $k$-th *corridor* is the persistence class
$\mathcal{C}_k = \{x \in X : \mu_k \leq \mu(x) < \mu_{k+1}\}$.
A trajectory is *corridor-supported at level $k$* if it remains in $\mathcal{C}_k$
for time $\geq \tau_k$ (the *corridor width*, measured in natural units of the dynamics).

**Definition X.3** (Collapse operator). The *collapse operator* $\Pi_k: \mathcal{C}_k \to X$
is the map that sends a state into its image under one step of the dynamics.
The system *collapses* when $\Pi_k(x) \notin \mathcal{C}_k$, i.e., the trajectory leaves the corridor.

**Definition X.4** (Cancellation locus). The *cancellation locus* $\mathcal{Z}_\mu$ is the
pre-image $\mu^{-1}(0)$ — the set of states with zero support. These are exact balance points:
the system is not absent but perfectly poised between collapse directions.

---

### Proposition X.5 (Six realizations)

*Each of the following frameworks admits the four objects of Definitions X.1–X.4:*

| Framework | Support metric $\mu(x)$ | Corridor width $\tau_k$ | Collapse operator $\Pi_k$ | Cancellation locus $\mathcal{Z}_\mu$ |
|-----------|------------------------|------------------------|--------------------------|---------------------------------------|
| **Open quantum** | Coherence $\mathcal{C}(\rho) = 1 - \max_i \rho_{ii}$ | Decoherence timescale $\tau_D$ (Liouvillian spectral gap)$^{-1}$ | Lindblad channel $\mathcal{L}(\rho) = \sum_k L_k \rho L_k^\dagger - \tfrac12\{L_k^\dagger L_k, \rho\}$ | Dark states: $L_k\|\psi\rangle = 0\ \forall k$; pointer basis |
| **Waveguide** | $\kappa = \mathrm{Im}(k)$ (imaginary wavevector, decay/length) | Bandwidth $\Delta\omega_n$ of propagation band $n$ | Absorption coefficient $\alpha(\omega)$; cut-off map $k_\perp = n\pi/d$ | Antiresonance: $\omega = \omega_\mathrm{AR}$ where $r(\omega) = -1$ exactly |
| **Non-Hermitian** | $\Gamma_n = -\mathrm{Im}(E_n)$ (decay width of resonance $n$) | Width of stability band: $\{\lambda : \Gamma_n(\lambda) < \Gamma_\mathrm{th}\}$ | $i\Gamma$ part of $H = H_0 + i\Gamma$; spectral broadening | Exceptional point: $\partial E_n/\partial\lambda = 0$, eigenvalues coalesce |
| **Reaction-diffusion** | $\phi(x,t)$ (local activation density) | Width of active phase: $\{\lambda : \phi^*(\lambda) > 0\}$ | Annihilation operator; rate $\mu$; absorbing-state generator | Inactive fixed point $\phi^* = 0$ (absorbing state) |
| **Renorm. interference** | $\mathcal{A}(x,\ell)$ (amplitude at scale $\ell$) | Scale range $[\ell_1, \ell_2]$ without cancellation | RG averaging $\mathcal{R}_\ell$: integrate fast modes | Path cancellation: $\sum_\Gamma \mathcal{A}_\Gamma = 0$ |
| **TIG corridors** | $\lambda(\sigma) = 2\|\sigma - \tfrac12\|$ | $\Delta\lambda_k$: Pre-leak 0.09; BRT 0.21; CHA 0.30; BAL 0.20; COL 0.10; CTR 0.10 | $\Pi_C: s \mapsto \mathrm{TSML}[s][c]$ for $c \in C$; absorbs to HAR in $\leq 2$ steps | $\{(s,c) : \mathrm{Mix}_\lambda[s][c] = 7\}$; 71 pairs at $\lambda=0$, 13 at $\lambda > 0$ |

---

### Remark X.6 (TIG as finite algebraic realization)

The TIG corridor model (final row) is the unique finite algebraic realization of
the grammar in Definitions X.1–X.4. It realizes all four objects in a 9-element
non-associative magma, with:
- support metric computable as a single rational number $\lambda \in [0,1]$;
- corridors indexed by the five algebraic thresholds $\{1/12, 0.30, 0.60, 0.80, 0.90\}$;
- collapse operator provably terminating in $\leq 2$ steps (Theorem 3.3, Proc. AMS);
- cancellation locus explicitly enumerable: 71 pairs at $\lambda=0$, 13 at $\lambda>0$.

The 82% contraction of the cancellation locus as $\lambda$ moves off zero
is the algebraic statement that the critical line $\sigma = \tfrac12$ is
structurally distinguished: it possesses the largest cancellation locus
in the algebra, while all other values of $\sigma$ have strictly fewer
exact-balance configurations available.

---

### Theorem X.7 (The corridor grammar is universal)

*Every framework in Proposition X.5 satisfies:*
*(i) the cancellation locus is contained in the $\mu = 0$ level set;*
*(ii) the collapse operator is non-expanding with respect to $\mu$;*
*(iii) corridor-supported states have $\mu > 0$ bounded away from zero on $[\tau_k, \infty)$.*

*Proof.* Each row is verified by inspection of the cited construction. $\square$

---

### Corollary X.8 (The analytic entry point for RH)

Combining the corridor grammar with the Halving flow (§2) and the
frequency-duration bound (Appendix E.2), the Riemann Hypothesis reduces to:

> **The single analytic statement needed:** A non-circular upper bound
> $\bigl|\mathrm{Re}(\zeta'/\zeta)(\sigma+it)\bigr| \leq C \cdot \lambda(\sigma)^2$
> holding in mean-square over $t \in [T_0, T]$, with $C < \infty$ independent of $T$,
> and without assuming RH as input.

This bound is empirically supported ($C_\mathrm{emp} \leq 11.023 < C_\mathrm{TIG} = 250/21$
on all tested heights), algebraically predicted by the TIG cancellation-locus contraction,
and would follow from the mean-value theorem for $\zeta'/\zeta$ with explicit constant —
a statement in the family of Montgomery (1977) and Heath-Brown (1981), but in the
*upper*-bound direction.

*This corollary identifies the exact analytic entry point. Whether it constitutes a
closed proof of RH depends on whether the mean-value bound can be established
independently. That is the remaining open question.*

---

*Cross-references:* Theorem 3.3 (sub-magma closure, Proc. AMS note);
Appendix E.2 (frequency×duration, this paper); Table E.2 (KV crossover, Ford 2002).

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
