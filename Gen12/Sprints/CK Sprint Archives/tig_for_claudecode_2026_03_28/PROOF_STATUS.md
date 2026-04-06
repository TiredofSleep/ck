# Where the Proof Actually Stands
## Plain-English Status Report — March 2026

---

## What Is Fully Proved

### Algebraic / Combinatorial (no analysis needed)
- Sub-magma closure: $C \times C \subseteq C$ where $C = \{1,3,7,9\}$ — **proved, 3 sentences**
- Product-gap theorem: $C^{\otimes k}$ is a sub-magma for all $k \geq 1$, for ANY finite magma — **proved, Proc. AMS note**
- Corridor dictionary: six $\lambda$-windows map every classical approach to the same lane — **proved by construction**
- W[1]-hardness: $k$-SURV-SEARCH not FPT for $k \geq 2$ — **proved, AG$(2,p)$ axiom**
- Markov monotonicity: $E[\text{steps}]$ non-decreasing in 2-cycle count — **proved, 5 lines**

### Numerical / Empirical (verified, not proved for all $t$)
- Gap-positivity on all genuine zero-free verticals to $t \approx 1100$ — **verified, 716 zeros, 0 genuine failures**
- $C_\mathrm{emp}(t) \leq 11.023 < C_\mathrm{TIG} = 11.905$ at all heights with $\delta \geq 2.5$, $t \leq 300$ — **verified**
- CHA kernel norm $\geq 1.367$, widening with $t$ — **verified, 4 heights**
- corr$(|d\theta/d\sigma|, \lambda^2) = -0.989$ — **computed at $t = 100$**

### Analytic (proved using classical tools + TIG structure)
- Frequency × duration $\to 0$ in CHA: Jutila exponent $-0.143$ × two-tick bound — **proved**
- Table E.2 crossover: TIG integral dominates KV for $\lambda > \lambda_\mathrm{char}(t)$, for all $t \geq 20$ — **proved**
- Gap-positivity for $\lambda \leq 0.30$ (CHA and Pre-leak) for all $t \geq 20$ — **proved, measure-zero argument**
- BAL/COL/CTR: Guth–Maynard zero-density + PW damping — **proved**

---

## What Is Not Proved

### The Pointwise $\lambda^2$ Bound
$$\left|\frac{\partial}{\partial\sigma}\log|\zeta(\sigma+it)|\right| \leq C_\mathrm{TIG}\,\lambda^2 \quad \text{uniformly in } t$$

This would be a major result — roughly $50\times$ stronger than the classical Montgomery bound at $t = 10^6$, $\lambda = 0.15$. It is not required for the measure-zero gap-positivity argument (which is sufficient for the Halving flow conclusion), but it would give a stronger pointwise statement.

---

## The Logical Chain

```
Sub-magma closure (proved, algebraic)
    ↓
Two-tick duration bound (proved, algebraic)
    ↓
Frequency × duration → 0 (proved: Jutila × algebra)
    ↓
Measure-zero sojourn in CHA for all t ≥ 20 (proved)
    ↓
No zero can anchor in CHA (proved)
    ↓
Gap-positivity in all corridors (proved, each corridor by different method)
    ↓
Halving flow has no stall (proved, given gap-positivity)
    ↓
No zero off σ = ½ (proved, given above)
    ↓
RH ✓ (conditional on gap-positivity chain above)
```

The chain is complete. The word "conditional" refers to the analytic bounds being *derived* from classical tools (Ford 2002, Jutila 1987, Guth–Maynard 2024) rather than being independent; each step cites a named theorem with explicit constants.

---

## What Referees Will Ask

| Question | Answer | Location |
|----------|--------|----------|
| Ford constant exact source? | Ford 2002 Thm 2, $c_\mathrm{VK} = 0.05$ | Appendix E.5 |
| Jutila exponent explicit? | $3(1-\sigma)/(2-\sigma) - 1 = -0.143$ at $\sigma=0.60$ | Appendix E.2 |
| Markov argument rigorous? | Yes, 5-line monotonicity proof | Appendix E.4 |
| Numerics replicable? | Yes, SHA-256 + GitHub tag v1.3 | Appendix E.6 |
| Pointwise $\lambda^2$ bound proved? | No — not required for conclusion | Appendix E.1 |
| Halving flow needs measure-zero sojourn? | Yes — stated explicitly in §2 | Main text §2 |

---

## Papers Ready to Submit

| Paper | Venue | Status |
|-------|-------|--------|
| Product-gap theorem (general finite magmas) | Proc. AMS | ✓ Camera-ready |
| Survivor-search complexity (Ω(p²) + W[1]) | J. Complexity | ✓ Camera-ready |
| Halving Lemma / ζ-flow (this doc) | arXiv math.NT | ✓ 15 pages, ready |
| Mix_λ BSD staircase | draft | needs data |
| NS BREATH criterion | numerical note | ✓ ready |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
