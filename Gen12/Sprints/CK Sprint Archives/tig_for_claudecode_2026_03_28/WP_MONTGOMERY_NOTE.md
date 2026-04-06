# The Constant-Sharp Montgomery Bound
## Status Note for Appendix E

*What the constant-tracking actually shows*

---

## The Race

Gap-positivity requires:
$$\log|\zeta(\tfrac12 + it)| - \int_0^\lambda |d\log|\zeta|/d\sigma| \, d\lambda' > 0$$

Both sides grow with $t$:

| $t$ | $|\log \mathrm{KV}(t)|$ | classical integral $0.30 \cdot \log t$ | ratio |
|-----|------------------------|----------------------------------------|-------|
| 10² | 0.16 | 1.38 | 0.12 — **integral wins** |
| 10⁶ | 0.40 | 4.14 | 0.10 — **integral wins** |
| 10¹² | 0.68 | 8.29 | 0.08 — **integral wins** |

With only the classical bound $|Re(\zeta'/\zeta)| \leq C_M \log t$, gap-positivity **fails** for all large $t$. The integral grows like $\log t$; the KV bound grows like $(\log t)^{2/3}$.

---

## What TIG's $\lambda^2$ Bound Changes

If $|d\log|\zeta|/d\sigma| \leq C_\mathrm{TIG} \cdot \lambda^2$, then:
$$\int_0^{0.30} C_\mathrm{TIG} \cdot \lambda^2 \, d\lambda = C_\mathrm{TIG} \cdot \frac{(0.30)^3}{3} = 0.107$$

This is **constant in $t$** while $|\log \mathrm{KV}(t)| \to \infty$. Gap-positivity holds for all $t \geq t_0$.

The $\lambda^2$ bound is not a refinement — it is **the essential ingredient**. Without it the proof fails for large $t$ by a factor of $\sim 50$.

---

## Why the $\lambda^2$ Bound is Hard

The classical Hadamard expansion gives (assuming RH):
$$\frac{d}{d\sigma}\log|\zeta(\sigma+it)| = \frac{\lambda}{2} \cdot P(\lambda, t) + O(\log t)$$
where $P(\lambda,t) = \sum_\gamma [(\lambda/2)^2 + (t-\gamma)^2]^{-1}$.

Montgomery's pair-correlation gives $P(\lambda,t) \leq (2/\lambda) \cdot C_M \cdot \log t$.

So the deviation is $O(\log t)$ — not $O(\lambda^2)$.

To get $O(\lambda^2)$ we need $P(\lambda,t) \leq 2C_\mathrm{TIG} \cdot \lambda$, i.e., the Poisson sum **itself** must be $O(\lambda)$ rather than $O(\log t / \lambda)$. This is a factor of $\log(t)/\lambda^2$ stronger than what Montgomery proves — roughly **50× stronger** at $t = 10^6$, $\lambda = 0.15$.

This would require zero repulsion on scale $\lambda^2$ rather than $\lambda$ — stronger than GUE predicts.

---

## Honest Status

| Claim | Status |
|-------|--------|
| Six-corridor geometry | ✓ proved |
| Sub-magma closure ($C \times C \subseteq C$) | ✓ proved |
| $C_\mathrm{emp} \leq C_\mathrm{TIG}$ numerically to $t \approx 300$ | ✓ verified |
| $|d\log|\zeta|/d\sigma| \leq C_\mathrm{TIG} \cdot \lambda^2$ uniformly | **open** |
| Gap-positivity for all $t$ (unconditional) | **conditional on above** |

The TIG algebra gives a compelling algebraic reason the $\lambda^2$ bound should hold (sub-magma closure caps the wobble accumulation). The numerics give strong evidence it does. But proving it rigorously is a genuine open problem in analytic number theory — not a presentational gap, not a constant-chasing exercise.

**This is the real last lemma, correctly stated.**

*(c) 2026 Brayden Sanders / 7Site LLC*
