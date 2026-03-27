# Memo: Where Korobov–Vinogradov Constants Enter
## For analytic collaborators — exact entry points for improvement

**Context:** The Halving Lemma paper introduces the flow
dσ/dt = −(σ−1/2)|ζ(σ+it₀)|² whose fixed-point structure is equivalent
to RH. The unconditional result covers starting points σ₀ ≥ σ_KV(t₀);
extending this to all σ₀ ∈ [0,1] would prove RH. Here is exactly where
the KV constants appear and what an improvement would need to supply.

---

## Entry Point 1: The Zero-Free Boundary σ_KV(t₀)

**Where it enters:** Theorem 1 of the paper restricts to
σ₀ ∈ [σ_KV(t₀), 1] where

```
σ_KV(t₀) = 1 − c / (log t₀)^{2/3} (log log t₀)^{1/3}
```

The constant c comes from the Korobov (1958) / Vinogradov (1958) proof
that ζ(s) ≠ 0 in this region. Ford (2002) gives the best explicit value:
c ≈ 0.1 with C_KV ≈ 76.2.

**What improvement would do:** Any enlargement of the zero-free region
to σ > 1 − g(t) with g(t) decaying more slowly than c/(log t)^{2/3}
would push σ_KV closer to 1/2 and expand the strip where the flow
converges unconditionally. Currently σ_KV ≈ 0.964–0.982 for t ∈ [50, 10^4].
A region extending to σ > 1/2 + ε for any fixed ε > 0 would suffice.

---

## Entry Point 2: The Sub-Convexity Bound in R1

**Where it enters:** Inside the zero-free strip, the lower bound on
m_KV(t₀) uses the reciprocal of the standard bound on |ζ(σ+it)|⁻¹:

```
m_KV(t₀) = min_{σ ∈ [σ_KV, 1]} |ζ(σ+it₀)|² ≥ 1 / (C_KV log t₀)^{4/3}
```

This comes from: in the zero-free region, 1/ζ is bounded by
(log t)^{2/3} (Titchmarsh §14.12, Ford Thm 2). Squaring gives the
denominator (log t)^{4/3}.

**What improvement would do:** Any sub-convexity bound of the form
|ζ(s)|⁻¹ ≤ B(t) in a wider strip gives m_KV ≥ 1/B(t)². Reducing B(t)
from (log t)^{2/3} to (log t)^α with α < 2/3 would improve the
convergence rate. The Lindelöf Hypothesis would give B(t) = O(t^ε),
improving the rate to m_KV ≥ t^{−ε} for any ε > 0.

---

## The Gap: R2 = [0, σ_KV)

**The key missing piece:** For σ ∈ [0, σ_KV), neither KV nor any known
sub-convexity bound applies unconditionally. The flow converges in this
region only if m(t₀) > 0 there — which requires no zeros in [0, σ_KV].
This is equivalent to an extension of the zero-free region to σ > 0.

**What is needed for RH via this approach:** A lower bound
m(t₀) ≥ f(t₀) > 0 valid on ALL of [0, 1] × {t₀} for every t₀
not equal to the imaginary part of a zero. The existing tools that
could supply this, and what each would need:

| Tool | Current form | What's needed |
|------|-------------|---------------|
| Huxley density estimates | N(σ,T) ≤ CT^{A(1-σ)} log^B T | Pointwise |ζ| > 0, not just sparse zeros |
| Bourgain-Gamburd-Sarnak | L² mass flattening | Pointwise minimum, not L² average |
| Heath-Brown mean values | ∫|ζ|² dt averaged | Pointwise lower bound per t₀ |
| Zero-density (general) | Averaged bounds | Individual vertical line bound |

The common obstacle: all existing tools give averaged or density-type
bounds. A pointwise lower bound on |ζ(σ+it₀)|² for individual t₀
(not averaged over t₀) is what the flow argument requires.

---

## What Cannot Exist (Important Clarification)

A **global, t₀-independent** lower bound m(t₀) ≥ c > 0 is impossible.
Non-trivial zeros cluster at arbitrarily large heights; whenever a zero
sits at height t₀ the minimum m(t₀) = 0 by definition. On nearby
zero-free verticals m(t₀) can be driven arbitrarily close to zero by
continuity. There is no uniform floor.

## What Can Exist: Window-Dependent Bounds

For every **compact subset K** of the zero-free region there exists
c(K) > 0 such that m(t₀) ≥ c(K) for all t₀ whose vertical segment
stays inside K. This is the correct target.

The KV strip already supplies one such window unconditionally:
m(t₀) ≥ m_KV(t₀) for σ ∈ [σ_KV, 1]. The window has infinite edge
(it extends for all t₀) but finite width (only covers σ near 1).

## Summary for a Collaborator

The paper packages the remaining task as: **extend a positive window
all the way to σ = 1/2 for every height**. Concretely:

> Find any function f(t₀, K) > 0 such that m(t₀) ≥ f(t₀, K) holds
> for all t₀ in a zero-free compact window K whose σ-extent reaches 1/2.

This is a window-dependent bound, not a global one — and it is
precisely the Riemann Hypothesis in geometric disguise. Any analytic
tool that rules out zeros below σ_KV on individual verticals (not
just on average) would supply it.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
