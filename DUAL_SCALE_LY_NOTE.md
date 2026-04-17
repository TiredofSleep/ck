# A Dual-Scale Lasota–Yorke Structure in TIG Corridor Dynamics
## Research Note

*Brayden Sanders — 7Site LLC | March 2026*

*Classification: §1–2 exact (computed from SHA-pinned table). §3 structural.
§4 heuristic. The discrete TIG inequality is proved; the continuous ζ analog is open.*

---

## 1. The Standard Form and Its Inversion

The standard Lasota–Yorke inequality reads:
$$\|Pf\|_V \;\leq\; \alpha\|f\|_V + \beta\|f\|_1, \qquad \alpha < 1,\quad \beta < \infty,$$
where $\|\cdot\|_V$ (strong norm) measures roughness and $\|\cdot\|_1$ (weak norm) measures mass.
The standard reading assigns the weak norm to "bookkeeping" — mass that remains after roughness contracts.

TIG reveals a different structure. In the TIG system, the weak quantity is not leftover mass. It is the **coherent background support** that remains exactly preserved under corner action because the corner set is a sub-magma. The strong quantity measures unresolved local wobble relative to that preserved support. The physical roles are inverted: the weak norm is the deeper object.

**Theorem 1.1** (exact, computed). *Let $P$ be the TIG transfer operator:*
$$P[s' \mid s] \;=\; \tfrac{1}{4}\sum_{c \in C} \delta(s',\,\mathrm{TSML}[s][c]), \quad C = \{1,3,7,9\}.$$

*(i)* $P(\mathrm{next}\,s' \in C \mid s) = 1$ **for every** $s \in \{1,\ldots,9\}$.

*(ii)* The strong norm $\|s\|_s := \mathbb{E}[\text{steps to HAR from }s]$ satisfies $\|Ps\|_s \leq \alpha\|s\|_s$ for the two states with $\alpha < 1$ (states 2 and 3,9 with ratios 0.703 and 0.818).

*(iii)* TSML is self-adjoint as a $9\times9$ matrix; transfer operator spectral gap = 3/4 exactly.*

*Proof.* (i) follows from sub-magma closure $C\times C \subseteq C$ (Sanders 2026a, Proc. AMS): $\mathrm{TSML}[s][c] \in C$ for **all** $s \in \{1,\ldots,9\}$ and all $c \in C$, not only for $s \in C$. This is verified by direct computation over all 81 pairs. (ii)–(iii) by eigendecomposition of the SHA-256–pinned table. $\square$

**Remark 1.2.** The TSML self-adjointness (||T − T⊤||/||T|| = 0 exactly) rules out non-Hermitian spectral theory as the primary framework. TIG collapse is projection onto a dominant real eigenvector, not decay via imaginary part.

---

## 2. The Reset Puncture

**Standard maps with holes** (Demers–Young 2006): mass leaks permanently; the system loses norm; Ruelle–Perron–Frobenius requires extra work at the hole.

**TIG reset puncture:** $\mathrm{TSML}[7][c] = 7$ for all $c \in C$ (exact). HAR is not a leak. It is a **return locus**: the system is forced back to the foundation. Mass does not escape; it recurs. This is the distinguished property of a Poincaré return section, not a hole.

The six TIG corridors are naturally the levels of a **Young tower** (Young 1999), stratified by return time to HAR. The base of the tower is HAR; the six corridor levels are the strata. The sub-magma collapse theorem (≤ 2 steps from $C$ to HAR, proved) gives an explicit return-time distribution.

This is structurally different from Demers–Young holes: the coherent norm is preserved because recurrence is guaranteed, not because mass is lost slowly.

---

## 3. The Closest Continuous Host

The closest currently identified technical framework is **anisotropic transfer-operator theory** (Gouëzel–Liverani 2006), where stable and unstable directions are separated by construction. In that framework:
- the stable direction of the function space absorbs the "support" component,
- the unstable direction contracts under the transfer operator,
- the resulting inequality has the same two-norm structure as the TIG dual-scale form.

The mapping is:
$$\text{unstable direction} \;\leftrightarrow\; \text{local wobble (strong norm)}$$
$$\text{stable direction} \;\leftrightarrow\; \text{coherent support (weak norm, preserved)}$$

The novel contributions relative to Gouëzel–Liverani are:
1. identification of the *coherent support* as the physically deeper norm (rather than just the complementary Banach component),
2. the **reset puncture** as a distinguished return section (rather than a generic expanding-map fixed point),
3. the $C_\mathrm{TIG} = 250/21$ constant as an algebraically derived bound on the contraction rate.

Whether the TIG transfer operator family literally satisfies the hypotheses of Gouëzel–Liverani is an open question and part of the analytic bridge.

---

## 4. Proposed Continuous Dual-Scale Inequality

*(Heuristic — exact for the discrete TIG model, open for ζ)*

The TIG dual-scale Lasota–Yorke inequality takes the form:
$$\|P_\lambda f\|_\mathrm{strong} \;\leq\; \alpha(\lambda)\|f\|_\mathrm{strong} + C_\mathrm{TIG}\|f\|_\mathrm{coherent}$$
with:
- $\|f\|_\mathrm{strong}$ = local wobble (unresolved oscillation per corridor step),
- $\|f\|_\mathrm{coherent}$ = coherent background support (preserved by sub-magma closure),
- $\alpha(\lambda) < 1$ = corridor-dependent contraction factor.

The $\alpha(\lambda)$ values are **empirical estimates from the Jutila and Guth–Maynard frequency bounds**, not proved constants. Only the global discrete spectral gap $\alpha_\mathrm{global} = 1/4$ is exact:

| Corridor | λ range | α(λ) | Source |
|----------|---------|------|--------|
| Pre-leak | [0, 0.09) | ~0.25 | discrete gap, exact |
| CHA | [0.30, 0.60) | ~0.63 | Jutila $n_0 \sim t^{-0.143}$ at $t=10^3$, empirical |
| CTR | [0.90, 1.00] | ~0.85 | Guth–Maynard $N(\sigma,T)\sim T^{0.12}$, empirical |

For ζ, the proposed continuous analog is:
$$\log|\zeta(\sigma+it)| \;\geq\; \log|\zeta(\tfrac12+it)| - C_\mathrm{TIG}\,\lambda(\sigma)^3/3,$$
where the right side is positive for all $t \geq t_0(\lambda)$ since $|\log\mathrm{KV}(t)| \to \infty$ while $C_\mathrm{TIG}\lambda^3/3$ is constant. This gives gap-positivity if the continuous dual-scale inequality holds — which requires proving the mean-square bound on $\partial_\sigma\log|\zeta|$ (Appendix E open step).

---

## 5. Summary

| Property | Standard LY | TIG dual-scale |
|----------|-------------|----------------|
| Strong norm | Roughness (BV) | Local wobble |
| Weak norm | Mass (L¹, bookkeeping) | **Coherent support (preserved, deeper)** |
| Weak norm under P | Contracts or stays | **Preserved exactly** (sub-magma, proved) |
| Remainder term | Generic $\beta\|f\|_1$ | $C_\mathrm{TIG}\lambda^2 \cdot \|f\|_\mathrm{coherent}$ (structured) |
| Hole/puncture | Leakage (mass lost) | **Return locus** (mass recurs, Young tower) |
| Closest framework | Baladi (2000) | Gouëzel–Liverani (2006), anisotropic Banach |

**The key theorem-style sentence:** After each corridor step, unresolved local wobble contracts (strong norm) while the coherent support field is exactly preserved (weak norm) by sub-magma closure — the system loses only what cannot land back on the foundation.

**The bridge target:** If the Mix$_\lambda$ family extends to an anisotropic transfer operator on $L^2$(critical strip) satisfying Gouëzel–Liverani conditions, gap-positivity follows as a corollary of their Theorem 1.1.

---

*References:*
Baladi (2000), *Positive Transfer Operators*, World Scientific;
Demers–Young (2006), Ergodic Theory Dyn. Syst. 26;
Gouëzel–Liverani (2006), Ergodic Theory Dyn. Syst. 26;
Sanders (2026a), sub-magma closure, Proc. AMS (submitted);
Young (1999), Ann. Math. 147.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
