# The Analytic Last Lemma
## Appendix E — Halving Lemma Paper

*Status: Open. Everything in this appendix is the proof target.*

---

## What We Need

$$\min_{\sigma \in [0,1]} |\zeta(\sigma + it)| \;\geq\; \exp\!\Bigl(-C\,(\log t)^{2/3}(\log\log t)^{1/3}\Bigr)$$

for ALL $t \geq t_0$, with $C$ explicit and $t_0$ computable.

This is the **uniform gap condition**. It says no vertical line is ever silent — ζ never simultaneously vanishes everywhere across the critical strip at the same height.

---

## What We Already Have

**Numerical:** Gap-positivity holds on all genuine zero-free verticals to t≈1100 (716 zeros, δ=2.0). No failures after accounting for scanner gaps. [Appendix D]

**Algebraic:** Pre-leak corridor min|ζ| ≥ 1.376 · KV(t) for t ∈ [8, 200] (7 genuine heights). Gap is *widening* (slope +1.405 in log t). [Stop 2]

**Phase-drift:** corr(|dθ/dσ|, λ²) = −0.989 at t=100. The drift rate is proportional to corridor depth squared. [Phase-vs-corridor computation]

**TIG constant prediction:** C_TIG = T\*/W_BHML = (5/7)/(3/50) = 250/21 ≈ 11.905.

---

## The Import from Each Team

**From OOL-KND-RH:**
They showed |dθ/dσ| is small at σ=½. If they can bound:
$$|d\theta/d\sigma| \leq C_0 \cdot \lambda^2 \quad \text{uniformly in } t$$
then since $\lambda = 2|\sigma - \tfrac12|$ and $\theta$ integrates to give $\log|\zeta|$, this becomes the uniform gap directly.

**From Guth-Maynard:**
Their matrix bound gives: if $|\zeta(\sigma_0 + it)| = 0$ at some $\sigma_0 \neq \tfrac12$, then a Dirichlet polynomial of length $N \sim t$ takes values $\geq N^{3/4}$ on a set of size $\geq T^{1-\epsilon}$. This contradicts their large-value theorem for $\sigma_0 \geq 0.65$ (BRT corridor or higher). The gap: they can't reach $\sigma_0 \in (0.5, 0.65)$ — the CHA corridor.

**From Connes:**
Weil positivity in the semilocal case gives a lower bound on the kernel trace. The global case would give the uniform gap directly. The TIG sub-magma theorem provides the idempotent that Connes needs: $\Pi_C = $ projection onto corner operators, $\Pi_C^2 = \Pi_C$ (sub-magma closure).

---

## The Three-Line Proof Sketch (What's Missing Analytically)

```
1. |dθ/dσ| ≤ C_TIG · λ²   [need: uniform bound in t]
        ↓
2. Integrate: log|ζ(σ+it)| ≥ log|ζ(½+it)| - C_TIG · |σ-½|²/2
        ↓  
3. |ζ(½+it)| ≥ KV(t)   [Hardy: infinitely many zeros on critical line
                          → |ζ| is not always tiny there, but this needs 
                          quantification away from zeros]
        ↓
4. Combine: min|ζ(σ+it)| ≥ KV(t) · exp(-C_TIG/8)   [uniform gap] ✓
```

**The actual missing piece:** Step 1 needs to be proved with C_TIG explicit and uniform in t. Numerically we have C_TIG ≈ 11.9 (from TIG) and the correlation −0.989 (from computation). The analytic proof that this holds for ALL t is the open lemma.

---

## Concrete Tasks (A, B, C, D from the itinerary)

**A. Kernel bound:** Compute min|ζ(σ+it)|/KV(t) for σ ∈ Pre-leak corridor, first 1000 zeros' midpoints. Fit α(t). If α(t) ≥ 1 and not decreasing, the gap is widening — strong evidence.

**B. Large-sieve splice:** Ask Guth/Maynard: can their singular-value bound for the matrix M_W be rewritten as ||K_corridor||_op ≤ f(σ)? If yes, this closes the gap for σ ≥ 0.65.

**C. Paley-Wiener paragraph:** If |dθ/dσ| ≤ C·λ², then by the PW band-limit theorem applied to log|ζ|, the minimum modulus is bounded below by exp(-C·λ²_max/2). Insert as Appendix E with C = C_TIG = 250/21.

**D. Gram-block scan:** Push corridor scan to t ≈ 10,000 using Odlyzko's zero tables. Every clean pass strengthens the numerical case; every failure narrows the search for a counterexample.

---

## Status Summary

| Step | Status | Owner |
|------|--------|-------|
| Corridor dictionary | ✓ Done | TIG (this work) |
| Sub-magma closure | ✓ Proved | Proc. AMS note |
| Kernel bound (numerical) | ✓ α≥1.376, t≤200 | Stop 2 above |
| Phase-drift correlation | ✓ corr=−0.989 | OOL-KND bridge |
| GM splice (σ≥0.65) | ✓ Implied | Guth-Maynard 2024 |
| GM splice (0.5<σ<0.65) | ✗ Open | Need CHA-corridor bound |
| Uniform |dθ/dσ|≤C·λ² | ✗ Open | The last lemma |
| Weil positivity (global) | ✗ Open | Connes program |
| **RH** | **Conditional** | **All of the above** |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
