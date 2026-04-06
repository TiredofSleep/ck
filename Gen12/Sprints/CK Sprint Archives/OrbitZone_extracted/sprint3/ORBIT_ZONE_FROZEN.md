# The Central Orbit Zone: Frozen Vocabulary and Bridge Target
## Version 1.0 — Do Not Expand Until Bridge Is Closed

*Brayden Sanders / 7Site LLC | March 2026*
*Status: FROZEN. All terms defined below are canonical for this program.*

---

## Frozen Vocabulary

**Orbit burst length B(λ)**
The maximum number of consecutive steps the chain spends inside the central cycle zone
{3,9} within a single corridor episode, before exiting to HAR or G-territory.
$$B(\lambda) = \mathbb{E}\!\left[\max_{\text{episode}} \{\text{consecutive steps in } \{3,9\}\}\right]$$

**Transit-through count T(λ)**
The number of distinct entries into the cycle zone {3,9} per chain.
$$T(\lambda) = \mathbb{E}[\#\text{ distinct entries into }\{3,9\}\text{ per chain}]$$

**Do not use:**
- "orbit return" — implies global re-entry after distant wandering (not observed)
- "visit count" — ambiguous between consecutive and non-consecutive entries
- "near-critical orbit" without specifying B or T

---

## Theorem-Style Remark (exact)

**Remark Z.6** *(Finite orbit structure).*
In the refined finite model ($N=300$, unrounded deformation), the central cycle zone
$\{3,9\}$ supports only local burst episodes:
$$T_{\max} = 1 \quad \text{across the sampled deformation range } \lambda \in [0, 0.95]$$
while $B(\lambda)$ varies nontrivially — peaking near $\lambda = 0$ (near-critical, $B_{\max}=6$),
dropping through the CHA corridor, and partially recovering in BAL/COL via the BHML
transit mechanism.

The two mechanisms have opposite gap dependence:
$$B(\lambda) \sim \gamma(\lambda)^{+1.49} \quad (\lambda < 0.50, \text{ cycle-stabilized})$$
$$B(\lambda) \sim \gamma(\lambda)^{-2.84} \quad (\lambda > 0.55, \text{ order-driven transit})$$

The global exponent ($\approx -0.10$) is a cancellation artifact of blending two regimes.

*Proof.* Direct computation: $N=300$ model, 3K chains per $\lambda$, 39 $\lambda$-values.
$T_{\max}=1$ verified at all tested $\lambda$. Exponents from log-log regression, $R^2=0.62$ and $0.75$. $\square$

---

## The Bridge Target (plain statement)

The continuous deployment must preserve exactly three things from the finite model.
In decreasing order of necessity:

**Required (closes the open layer):**
> Unique stationary support: $\sigma = \tfrac12$ carries all stationary support of $K_\lambda$
> for all $\lambda < \lambda^*$, as HAR does in the finite model for $\lambda < 0.9963$.

**Strengthening (not required, but would sharpen the argument):**
> Local burst geometry: the cycle-stabilized burst $B(\lambda)$ has an analytic analog
> — a consecutive near-critical revisit statistic within a single corridor episode of
> length $O(\log t)$ — that is maximal at $\sigma = \tfrac12$ and decays with distance.

**Distinguishing condition (tells the bridge what NOT to inherit):**
> Absence of BHML transit: the analytic deployment has no ordering analog at large $t$
> — there is no "BHML endpoint" in the critical strip that would create spurious
> transit-through orbit signals far from $\sigma = \tfrac12$.

The bridge does not need to recover all three. Item (1) alone closes Open Problem Z.5.
Items (2) and (3) would make the closed argument richer and more precise.

---

## What the ζ-Side Proxy Measures

$$B_\zeta(\sigma, t) = \max\left\{k : \left|\mathrm{Re}\frac{\zeta'}{\zeta}(\sigma+it')\right| < \varepsilon \text{ for } k \text{ consecutive } t' \in [t, t+O(\log t)]\right\}$$

This is a **consecutive near-critical revisit statistic within a single corridor episode**.

It is **not**: the number of times a trajectory returns to a neighborhood of $\sigma=\tfrac12$
after wandering far away. That would be T, and T=1 in the finite model.

It is **not**: the total sojourn time near $\sigma=\tfrac12$. That is the frequency×duration
product, which the Jutila/KV arguments already control.

It is: the length of the longest local burst of near-critical behavior in one height window.

---

## How This Connects to the Existing Appendix E

The existing Appendix E already handles:
- Frequency×duration → 0 (Jutila + two-tick, proved)
- KV floor (Ford 2002, proved)
- Mean-square bound on Re(ζ'/ζ) (open, the drift rate)

The orbit burst $B_\zeta$ is a new observable sitting between these:
- It is finer than the frequency×duration product (which is a global average)
- It is coarser than the drift rate (which is a derivative)
- It measures local burst geometry within one corridor episode

If $B_\zeta(\sigma, t) \to 0$ as $t \to \infty$ for $\sigma \neq \tfrac12$, this would be a
strengthening of the support gap claim — not just that the sojourn frequency vanishes,
but that consecutive near-critical behavior cannot persist locally.

This is currently observable but unproved on the ζ side.

---

## Document Status

This note supersedes any earlier "orbit" language in:
- DELAY_SIGNATURE_NOTE.md (use B/T instead of "delay")
- OFF_LINE_ZERO_SIGNATURES.md (use B/T instead of "wake")
- ORBIT_CAPACITY_NOTE.md (now subsumed here)
- ORBIT_TWO_MECHANISMS.md (now subsumed here)

The four-layer note (FOUR_LAYER_REALIZATION.md) should cite this as Remark Z.6
when next updated.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
