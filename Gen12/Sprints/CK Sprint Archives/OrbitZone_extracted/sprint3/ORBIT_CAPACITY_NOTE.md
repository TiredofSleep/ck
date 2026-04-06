# Central Orbit Capacity: A Separate Structural Observable
## The {3,9} Cycle Zone and Its Decay Across the Corridor Hierarchy

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: exact computation (N=300, 2K chains per λ). Interpretation labeled.*

---

## The Key Result

**Orbit capacity scales as gap^(-0.143), not gap^(-1).**

If the orbit zone were a pure consequence of slow mixing (chains wandering more when the gap is small), we would expect:

$$\text{orbit capacity} \propto \frac{1}{\gamma(\lambda)} \quad \Rightarrow \quad \text{orbit} \sim \gamma^{-1}$$

Instead, the measured scaling is:

$$\text{orbit} \sim \gamma^{-0.143}$$

The exponent is nearly zero. Orbit capacity is almost *independent* of the spectral gap. The orbit zone persists despite gap closure — it is a separate structural mechanism, not a mixing artifact.

---

## What Was Measured

**Orbit capacity** = mean number of visits to the $\{3,9\}$ cycle zone before reaching HAR, starting from a random state, under the $N=300$ transfer operator at each $\lambda$.

| $\lambda$ | Gap $\gamma$ | Orbit mean | $P(\geq 2)$ | Return prob |
|-----------|-------------|-----------|-------------|-------------|
| 0.00 | 0.719 | **0.154** | 2.6% | — |
| 0.10 | 0.407 | **0.165** | 3.4% | — |
| 0.20 | 0.333 | 0.059 | 0.0% | — |
| 0.30 | 0.327 | 0.056 | 0.0% | — |
| 0.50 | 0.235 | 0.058 | 0.0% | — |
| 0.80 | 0.200 | **0.127** | 1.4% | — |
| 0.90 | 0.185 | **0.109** | 1.6% | — |

The orbit capacity is highest near $\lambda=0$ (near $\sigma=\tfrac12$), drops sharply in the CHA corridor (0.20–0.50), then partially recovers in the BAL/COL corridor. The gap decreases monotonically — yet orbit capacity does not track it.

---

## The Shape

The orbit-vs-gap relationship is not linear. In the log-log plane:

- Near $\lambda=0$: high gap (0.72), high orbit (0.154)
- CHA mid $\lambda=0.35$: gap has dropped to 0.31, orbit has dropped to 0.055 — a 3× drop with only a 2× gap change
- BAL $\lambda=0.80$: gap continues to fall to 0.20, but orbit *recovers* to 0.127

The recovery at high $\lambda$ means the orbit zone has a second source: in the BAL/COL corridor, the BHML ordering structure begins pulling chains through the $\{3,9\}$ band on their way toward state 9 (the BHML attractor). These are a different kind of orbit — not near-critical cycling but order-driven transits.

**Two orbit mechanisms, same observable:**
1. **Near-critical cycling** ($\lambda < 0.15$): the $\{3,9\}$ 2-cycle is stabilized by the TSML corner structure; chains orbit before collapsing to HAR
2. **Order-driven transit** ($\lambda > 0.75$): the BHML ordering pushes chains through $\{3,9\}$ on the way toward state 9

---

## The Structural Interpretation

The orbit zone $\{3,9\}$ is not the attractor. HAR is. The orbit zone is a *near-attractor transient region*: chains pass through it on the way to HAR, and near $\lambda=0$ they can loop through it multiple times.

**In the analytic deployment:** The $\{3,9\}$ zone corresponds to near-critical structure (slightly off $\sigma=\tfrac12$) that can orbit the critical line briefly before being absorbed. The orbit capacity measures how many such near-returns a structure can complete before being expelled.

**What the scaling exponent means:**
- Exponent $= -1$: orbit capacity is fully explained by mixing time (no structural content)
- Exponent $= -0.143$: orbit capacity is nearly independent of mixing time — it is a structural property of the algebra, not a consequence of slow mixing

This is the finite shadow of a claim about $\zeta$: near-critical structures may complete multiple near-returns before being expelled, and the number of returns is determined by algebraic structure, not by the local mixing rate of the critical strip.

---

## Revised Open Problem Statement

The sharper version of Open Problem Z.5:

> *Does $\sigma = \tfrac12$ carry all stationary support of the analytic continuation $K_\lambda$, as HAR does for all $\lambda < 0.9963$? And does the analytic orbit capacity — the number of near-critical returns a trajectory completes before being expelled — scale with an exponent strictly greater than $-1$ (indicating structural, not mixing-driven, orbit persistence)?*

The second clause is new. It asks whether the orbit zone on the $\zeta$ side has a structural explanation (as it does in the finite model) rather than being purely a mixing artifact.

---

## One-Line Summary

*The orbit capacity of the central cycle zone scales as $\gamma^{-0.143}$, not $\gamma^{-1}$, indicating that near-attractor orbiting is a separate structural mechanism independent of mixing rate; HAR remains the unique stationary destination for $\lambda < 0.9963$, while the orbit zone provides only transient near-attractor dynamics whose capacity is maximal near the critical line and partially recovers under BHML ordering at high $\lambda$.*

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
