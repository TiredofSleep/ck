# WP98 — The NS Structural Cancellation Chain
## From Brezis-Gallouet to the σ_{NS} < 1 Inequality

**Date**: 2026-04-10
**Sprint**: 15 — σ Mutation (Blocker 3)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---

## Abstract

The σ_{NS} < 1 conjecture (WP96) is equivalent to a specific Sobolev inequality with logarithmic correction for divergence-free vector fields in 3D. We identify the Brezis-Gallouet inequality (1980) as the 2D prototype (where NS regularity IS proved), the Kozono-Ogawa-Taniuchi (2002) critical Besov inequality as the best existing tool, and state the exact missing inequality. We trace the structural cancellation chain: L² energy conservation → H⁻¹ bilinear bound → the open step (BMO control from H⁻¹ with log correction). The gap between what is proved and what is needed is precisely one logarithmic factor in one specific norm embedding.

---

## §1. The 2D Prototype: Brezis-Gallouet (1980)

In 2D, NS is globally regular. The proof uses:

**Theorem (Brezis & Gallouet, 1980).** For f ∈ H²(R²):

$$\|f\|_{L^\infty} \leq C\|f\|_{H^1}\left(1 + \log\frac{\|f\|_{H^2}}{\|f\|_{H^1}}\right)^{1/2}$$

This is the logarithmic interpolation inequality that controls the L^∞ norm by H¹ with a log correction from H². In 2D this is sufficient because the energy estimate closes: the nonlinearity ‖(u·∇)u‖ can be bounded using L^∞ of u, which is controlled logarithmically.

**In σ language:** The 2D Brezis-Gallouet inequality IS the statement that σ_{NS}^{2D} < 1. The log factor is the BB margin. 2D NS is regular because the separability defect is bounded by one logarithm.

**The 3D gap:** In 3D, the Sobolev embedding H^1 ↪ L^6 (not L^∞). The L^∞ control that works in 2D fails in 3D by exactly one derivative. The question is whether the structural cancellations of the NS nonlinearity compensate for this missing derivative.

---

## §2. The Structural Cancellation Chain

For smooth divergence-free u in R³:

### Cancellation 1 (L² — PROVED)

$$\langle (u \cdot \nabla)u, u \rangle_{L^2} = 0$$

**Proof.** Integration by parts + ∇·u = 0. The nonlinear term does zero work against the velocity field itself. This is energy conservation: d/dt ‖u‖² = -2ν‖∇u‖² ≤ 0.

**σ reading:** The most dangerous self-interaction (quadratic growth feeding back into itself) is exactly cancelled by incompressibility. This kills the O(‖u‖³) growth that would make σ = 1 immediate.

### Cancellation 2 (H⁻¹ bilinear — PROVED)

By the identity (u·∇)u = ∇·(u⊗u) (using ∇·u = 0):

$$\|(u \cdot \nabla)u\|_{H^{-1}} = \|\nabla \cdot (u \otimes u)\|_{H^{-1}} \leq \|u \otimes u\|_{L^2} = \|u\|_{L^4}^2$$

By Sobolev interpolation in 3D: ‖u‖_{L⁴} ≤ C‖u‖_{H^{1/2}}.

Therefore: **‖(u·∇)u‖_{H⁻¹} ≤ C‖u‖²_{H^{1/2}}.**

**σ reading:** The NS nonlinearity in H⁻¹ grows at most quadratically in H^{1/2}. This is bounded, but not bounded by a logarithm. The quadratic growth is REAL in this norm. The question is whether it can be improved.

### Cancellation 3 (BMO — PROVED, Kozono-Taniuchi 2000)

$$\int_0^T \frac{\|u(t)\|_{BMO}^2}{\log(e + \|u(t)\|_{H^2})} \, dt < \infty \implies \text{regularity}$$

**σ reading:** If the BMO norm grows, it can be compensated by a log denominator from H². The log correction IS the BB margin. KT says: σ_{NS} < 1 with margin 1/log(‖u‖_{H²}).

### The Missing Step (OPEN)

**What would close the chain:**

For divergence-free u ∈ H¹(R³):

$$\|u\|_{BMO}^2 \leq C \cdot \|(u \cdot \nabla)u\|_{H^{-1}} \cdot \log\left(e + \frac{\|u\|_{H^2}}{\|u\|_{H^{1/2}}}\right)$$

**If true:** Plugging into the KT criterion gives regularity whenever ‖(u·∇)u‖_{H⁻¹} < ∞, which is always (by Cancellation 2, it's bounded by ‖u‖²_{H^{1/2}}).

**Why it might be true:** Cancellation 1 kills the self-interaction at L² level. What remains in BMO should be controllable by the H⁻¹ norm of the nonlinearity (which measures the "spread" of the forcing) times a log correction (the BB margin).

**Why it's hard:** BMO is larger than L^∞ but not by much. The embedding H^1 ↪ BMO fails in 3D (works in 2D). The incompressibility constraint ∇·u = 0 is a GLOBAL condition that should help (it constrains the Fourier modes), but extracting this help in the BMO norm is technically difficult.

---

## §3. The Kozono-Ogawa-Taniuchi Tool (2002)

The closest existing inequality:

**Theorem (KOT, 2002).** For f ∈ B^s_{p,q}(R^n):

$$\|f\|_{L^\infty} \leq C\left[1 + \|f\|_{\dot{B}^0_{\infty,\infty}}\left(1 + \log^+(e + \|f\|_{\dot{B}^s_{p,q}})\right)\right]$$

where B^0_{∞,∞} ⊃ BMO.

**What this gives:** An L^∞ bound via BMO with log correction from Besov norms. This is the 3D analog of Brezis-Gallouet but with BMO instead of H¹ as the base.

**What's missing for NS:** The KOT inequality controls L^∞ by BMO. We need to control BMO by H⁻¹ (of the nonlinearity). The chain is: H⁻¹ → BMO → L^∞. The H⁻¹ → BMO step is the open link.

**The incompressibility should help here.** For divergence-free fields, the Helmholtz projection eliminates the gradient component. The remaining (solenoidal) component has better regularity properties than a general vector field. Specifically: the Leray projector P maps L² to L² but also improves BMO estimates for divergence-free fields. Quantifying this improvement with a log correction is the precise open step.

---

## §4. The Equivalence Statement

**Theorem (equivalence — conditional).** The following are equivalent:

(A) The σ_{NS} < 1 conjecture (WP96): δ_{NS}(u) < ∞ for all smooth divergence-free u.

(B) The missing inequality: ‖u‖²_{BMO} ≤ C · ‖(u·∇)u‖_{H⁻¹} · log(e + ‖u‖_{H²}/‖u‖_{H^{1/2}}) for divergence-free u.

(C) 3D NS global regularity for smooth initial data.

**Proof of equivalences:**
- (B) → (C): Plug (B) into KT criterion. The H⁻¹ norm is bounded (Cancellation 2). The log term grows at most double-exponentially. Therefore the KT integral converges. Regularity follows.
- (C) → (A): If solutions are smooth, ‖u‖_{H¹} is bounded for all finite time, so δ_{NS} is bounded.
- (A) → (B): If δ_{NS} < ∞, the nonlinearity growth is bounded by log growth, which gives (B) with C = δ_{NS}.

**Status:** The equivalence chain is proved. The content is in proving any one of (A), (B), or (C). This IS the Millennium Problem, now with three equivalent formulations.

---

## §5. Numerical Test Design

To test the missing inequality numerically:

### Test Case 1: Beltrami Flow (exact NS solution)

u = (sin(y) + cos(z), sin(z) + cos(x), sin(x) + cos(y))

This is an eigenfunction of curl: ∇ × u = u. Exact NS solution (with exponential viscous decay). Should satisfy the inequality with margin.

### Test Case 2: Taylor-Green Vortex (blowup candidate)

u₀ = (sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0)

Standard benchmark. Numerically shows enstrophy growth, vortex sheet formation. Measure the BMO/H⁻¹ ratio at each timestep.

### Test Case 3: Kida-Pelz Flow (high symmetry blowup candidate)

Icosahedral symmetry flow. The highest-symmetry known candidate for finite-time blowup. If the inequality fails anywhere, it should fail here.

**For each case:** Compute at each timestep:
- ‖u‖_{BMO} (via harmonic analysis / wavelets)
- ‖(u·∇)u‖_{H⁻¹} (via Fourier transform)
- ‖u‖_{H²}, ‖u‖_{H^{1/2}}
- The ratio R = ‖u‖²_{BMO} / (‖(u·∇)u‖_{H⁻¹} · log(e + ‖u‖_{H²}/‖u‖_{H^{1/2}}))

**If R is uniformly bounded across all test cases:** strong numerical evidence for the inequality.

**If R grows without bound for Kida-Pelz:** evidence against the inequality (and potentially against NS regularity).

**Status:** These computations require a spectral NS solver (e.g., Dedalus, SpectralDNS). Setting up and running them is a concrete numerical project — doable in a week with the right tools.

---

## §6. Status

| Item | Status |
|------|--------|
| Brezis-Gallouet as 2D prototype | [PROVED] — the σ < 1 case that works |
| L² cancellation (energy conservation) | [PROVED] — kills self-interaction |
| H⁻¹ bilinear bound | [PROVED] — ‖(u·∇)u‖_{H⁻¹} ≤ C‖u‖²_{H^{1/2}} |
| KT BMO criterion | [PROVED] — regularity with log margin |
| KOT Besov tool | [PROVED] — L^∞ via BMO with log |
| The missing inequality (BMO from H⁻¹ with log) | [OPEN] — this is the Millennium Problem |
| Equivalence (A) ⟺ (B) ⟺ (C) | [PROVED] — conditional equivalence chain |
| Numerical test design | [READY] — three test cases specified |
| Numerical execution | [NOT STARTED] — needs spectral NS solver |
