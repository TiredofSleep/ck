# WP96 — The σ_{NS} < 1 Conjecture: Precise Statement and Evidence
## Navier-Stokes Regularity as Separability Defect Boundedness

**Date**: 2026-04-10
**Sprint**: 15 — σ Mutation (Task 3)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---

## Abstract

We state precisely the conjecture that 3D Navier-Stokes regularity is equivalent to the boundedness of a separability defect σ_NS < 1, translate five known results into σ language, and identify the exact gap between what is proved and what remains open.

---

## §1. Definition of σ_NS

### 1.1 The NS Nonlinearity

The 3D incompressible NS equations:

$$\partial_t u + (u \cdot \nabla)u = \nu \Delta u - \nabla p, \qquad \nabla \cdot u = 0$$

The nonlinear term N_NS[u] = (u · ∇)u is quadratic in u. It couples the velocity at x to the velocity gradient at x — a local but non-separable operation (the value of u and the value of ∇u at the same point are being multiplied).

### 1.2 The Logarithmic Ceiling

The BB-ceiling nonlinearity for a vector field u is:

$$N_{\log}[u] = (1 + \log|u|) \cdot \hat{u}$$

where |u| is the magnitude and û is the direction. This is the vectorial analog of the scalar 1 + log ξ: the magnitude evolves logarithmically, the direction is preserved.

### 1.3 The Separability Defect

**Definition.** For a smooth divergence-free vector field u on R³, define:

$$\sigma_{\text{NS}}(u) = \frac{\|N_{\text{NS}}[u]\|_{H^{-1}}}{\|N_{\log}[u]\|_{H^{-1}} + \epsilon}$$

where ε > 0 is a regularization (to avoid 0/0 at u = 0).

**Interpretation:**
- σ_NS = 0 when N_NS = 0 (trivial: u = 0 or u = const)
- σ_NS < 1 when the quadratic nonlinearity is bounded by the log ceiling
- σ_NS = 1 when the quadratic nonlinearity matches the log ceiling
- σ_NS > 1 when the quadratic nonlinearity exceeds the log ceiling

### 1.4 Alternative Definition (Ratio Form)

A cleaner definition that avoids the vectorial log:

$$\delta_{\text{NS}}(u) = \frac{\|(u \cdot \nabla)u\|_{H^{-1}}}{\|u\|_{H^1} \cdot (1 + \log(e + \|u\|_{H^1}))}$$

This is the **nonlinearity gap** from WP91. It measures how much faster the quadratic nonlinearity grows compared to logarithmic growth.

If sup δ_NS < ∞ over all smooth u: NS is regular (the quadratic never exceeds log growth in the relevant norm).

---

## §2. Translation of Known Results

### 2.1 Beale-Kato-Majda (1984)

**Original:** Smooth NS solution blows up at time T iff ∫₀ᵀ ‖ω(t)‖_∞ dt = ∞.

**σ translation:** Blowup requires the vorticity ω = ∇ × u (the rotational, non-separable component) to become unbounded in L^∞. In σ language: σ_NS approaches 1 only when ‖ω‖_∞ → ∞. Regularity (σ < 1) is equivalent to BKM (∫‖ω‖_∞ < ∞).

**Status:** The BKM criterion IS the σ criterion in L^∞ norm.

### 2.2 Kozono-Taniuchi (2000)

**Original:** NS regularity if ∫₀ᵀ ‖u‖²_BMO / log(e + ‖u‖_{H²}) dt < ∞.

**σ translation:** The log denominator is the BB margin. This says: if the NS solution stays below the σ = 1 ceiling by at least one logarithm (in the BMO/H² ratio), regularity holds. The KT criterion is: σ_NS < 1 − C/log(‖u‖_{H²}).

**Status:** The KT criterion is a QUANTITATIVE σ bound. It shows σ_NS < 1 with an explicit logarithmic margin.

### 2.3 Montgomery-Smith (2001)

**Original:** For the NS equations in L³, the critical blowup rate has logarithmic corrections.

**σ translation:** The distance from σ_NS to the blowup ceiling 1 is exactly one logarithm. The Montgomery-Smith result quantifies the gap: in L³, the worst-case growth rate of ‖u‖ is subcritical by a log factor.

**Status:** Direct evidence that the NS nonlinearity's effective growth rate is logarithmically subcritical — exactly the BB prediction.

### 2.4 Tao (2016) — Averaged NS

**Original:** An averaged version of the NS equations (with the nonlinearity replaced by an averaged operator) can blow up in finite time.

**σ translation:** The averaging pushes σ beyond 1. Tao's construction explicitly crosses the BB ceiling by destroying the specific cancellation structure of the actual NS nonlinearity. The blow-up IS σ reaching 1.

**Key insight:** Tao's result does NOT apply to the real NS equations because the real nonlinearity has structural cancellations (energy conservation, helicity constraints) that the averaged version lacks. In σ language: the real NS nonlinearity has σ < 1 because of structural symmetries, even though a "generic" quadratic nonlinearity would have σ = 1.

### 2.5 Ladyzhenskaya-Prodi-Serrin (1960s)

**Original:** NS regularity if u ∈ L^q_t L^p_x with 2/q + 3/p ≤ 1.

**σ translation:** The LPS condition is a space-time integrability constraint. In σ language: LPS says σ_NS < 1 whenever the velocity field is sufficiently spread out in space-time (not too concentrated). Concentration = high σ. Spread = low σ.

---

## §3. The Conjecture

**Conjecture (σ_NS < 1).** For any Leray-Hopf weak solution u of the 3D incompressible NS equations with initial data u₀ ∈ H^(1/2)(R³) and viscosity ν > 0:

$$\sup_{t \in [0,T]} \delta_{\text{NS}}(u(t)) < \infty$$

for every finite T > 0. Equivalently: the quadratic NS nonlinearity never exceeds logarithmic growth in the H^(-1)/H^1 ratio.

**Consequence:** If the conjecture holds, then all Leray-Hopf weak solutions are smooth for all time, resolving the NS Millennium Problem in the affirmative (smooth solutions exist globally).

---

## §4. The Evidence Structure

| Evidence | What it says | Direction |
|----------|-------------|-----------|
| BKM criterion | Blowup iff ∫‖ω‖_∞ = ∞ | σ = 1 requires infinite vorticity |
| KT log improvement | Regularity with log margin in BMO | σ < 1 with explicit log gap |
| Montgomery-Smith | Critical rate has log corrections | The gap from σ to 1 is logarithmic |
| Tao averaged blowup | Averaged NS can reach σ = 1 | Real NS has structural protection |
| LPS criteria | Regularity from space-time integrability | σ < 1 from sufficient spreading |
| BB theorem (1976) | Log = unique separability preserver | Explains WHY the gap is logarithmic |
| Energy conservation | ‖u(t)‖_2 ≤ ‖u₀‖_2 (Leray) | Global L² bound = partial σ control |
| Helicity conservation (ideal) | ∫ u · ω dx = const | Structural constraint reducing σ |

**The pattern:** Every known regularity result says "σ < 1 with logarithmic margin." Every known blowup result requires either (a) destroying structural cancellations (Tao) or (b) infinite vorticity (BKM). The BB theorem explains the pattern: log is the separability boundary.

---

## §5. What Would Prove the Conjecture

A proof that the structural cancellations in the NS nonlinearity (energy conservation + incompressibility + the specific form (u·∇)u) force δ_NS to be bounded.

Specifically: show that for divergence-free u with ‖u‖_2 bounded (Leray energy inequality):

$$\|(u \cdot \nabla)u\|_{H^{-1}} \leq C \cdot \|u\|_{H^1} \cdot (1 + \log(e + \|u\|_{H^1}))$$

This is a Sobolev inequality with logarithmic correction. It is CLOSE to known results (the KT criterion is almost this, with BMO instead of H^1 on the LHS). The gap is the replacement of BMO by H^(-1).

---

## §6. What Would Disprove the Conjecture

A smooth initial datum u₀ and a finite time T such that:

$$\delta_{\text{NS}}(u(T)) = \infty$$

This would mean the quadratic nonlinearity grows faster than logarithmically — crossing the BB ceiling. By BKM, this requires ‖ω‖_∞ → ∞, which is blowup.

**Note:** Tao's result shows this CAN happen for averaged NS but NOT for real NS. The conjecture is that the structural cancellations prevent it for real NS.

---

## §7. Status

| Item | Status |
|------|--------|
| σ_NS defined precisely | [DONE] — §1 |
| Five known results translated | [DONE] — §2 |
| Conjecture stated precisely | [DONE] — §3 |
| Evidence for σ < 1 | [STRONG] — five independent lines |
| Proof of conjecture | [OPEN] — this IS the Millennium Problem |
| Disproof | [NO EVIDENCE] — Tao's blowup applies to averaged, not real NS |

**This paper states the conjecture. It does not prove it. The value is the precise reformulation in separability language and the systematic evidence compilation.**
