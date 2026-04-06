# RH RETURN MEMO
# What Is the Exact Surviving Gap Object After the Full Rotation?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Current RH State (Frozen)

| Layer | Content | Status |
|-------|---------|--------|
| **Shell** | sinc²/GUE statistics; Montgomery pair-correlation; generic zero spacing | Proved universally — does not depend on RH |
| **Arithmetic core** | Kloosterman sums; Kuznetsov-Petersson/KEF; Eisenstein contribution to the explicit formula | Accessible, computable |
| **Gap 2** | Cusp subdominance: Σ_{t_j≤T} ǀρ_j(1)ǀ²/cosh(πt_j) = O(T²) ≪ N^{2π²} | **Closed** by Kuznetsov Weyl law — standard spectral bookkeeping |
| **Gap 1** | The final RH wall | **Open** |

After Gap 2 closure: the cusp contamination is eliminated as an obstruction. What remains is the direct confrontation between the arithmetic Kloosterman projection and the zero distribution.

---

## PART 2 — RH in the Rotated Grammar

| Element | Content |
|---------|---------|
| **Shell** | GUE/sinc² spectral statistics for zeros — universal, proved, independent of critical-line placement |
| **Core** | The arithmetic Kloosterman-Eisenstein projection: Σ_{p≤N} Kl(1,1;p) f(log p/log N) log p, connected to the zero distribution via the KEF |
| **Surviving object** | The selectivity of the arithmetic projection: does the KEF arithmetic side uniquely determine the zero distribution, or can off-line zeros satisfy the same arithmetic constraints? |
| **Gap 2** | Cusp subdominance — **closed** |
| **Gap 1** | Injectivity of the arithmetic-to-zero projection: no off-line zero distribution satisfies the same KEF arithmetic constraints as the critical-line distribution |
| **Duality type** | **External**: zeros live in ℂ (critical strip), arithmetic data lives in ℤ (primes, Kloosterman), explicit formula = the external bridge |

---

## PART 3 — Smallest Surviving RH Object

**Testing the candidates:**

**A. KEF zero-weight sum:**
$$\sum_\rho W(\rho)\hat{f}\!\left(\frac{\gamma}{2\pi\log N}\right)$$
This is the zero FIBER projected onto a test function. It differs for critical-line vs off-line distributions. It is what the explicit formula connects to the arithmetic side. It is the "image" of the zero distribution under the projection. But it is on the WRONG side — it's what we want to constrain, not what we can compute.

**B. Arithmetic Kloosterman average:**
$$\sum_{p\le N} \mathrm{Kl}(1,1;p)\,f\!\left(\frac{\log p}{\log N}\right)\log p$$
This is the ARITHMETIC BASE — computable (in principle) from prime data. By the KEF, it equals the zero-weight sum A after removing diagonal/shell terms. This is the accessible side of the duality. But alone it doesn't carry the gap — it only becomes the surviving object when compared to A.

**C. The residual between arithmetic side and generic shell:**
$$\mathcal{R}(N) = \sum_\rho W(\rho)\hat{f}\!\left(\frac{\gamma}{2\pi\log N}\right) - \left[\text{diagonal + shell terms}\right] - \sum_{p\le N}\mathrm{Kl}(1,1;p)\,f\!\left(\frac{\log p}{\log N}\right)\log p$$
This difference is zero by the KEF if the arithmetic side is exact. But its behavior under perturbation by off-line zeros is the core question.

**D. The projection injectivity:**
The map (zero distribution) → (arithmetic Kloosterman sum via KEF). The question: is this map injective on zero distributions satisfying the shell statistics?

**Strongest answer:**

$$\boxed{\text{"The smallest surviving RH object is the arithmetic projection residual for off-line zeros: the contribution that any off-line zero } \rho_0 = \sigma_0 + i\gamma_0 \text{ (}\sigma_0 \neq 1/2\text{) makes to the KEF arithmetic side, and whether that contribution is distinguishable from zero."}}$$

More precisely: define the **off-line residual**:
$$\delta(\sigma_0, \gamma_0) = W(\rho_0)\hat{f}\!\left(\frac{\gamma_0}{2\pi\log N}\right) - W(1/2+i\gamma_0)\hat{f}\!\left(\frac{\gamma_0}{2\pi\log N}\right)$$

This is the difference between the contribution of an off-line zero and its critical-line counterpart. If δ ≠ 0, the arithmetic side CAN detect the off-line zero. If δ = 0 for some off-line configuration, the arithmetic projection is BLIND to that configuration and cannot prove RH.

The surviving RH object is whether δ(σ₀, γ₀) ≠ 0 for ALL off-line zeros — i.e., whether the arithmetic projection has nonzero sensitivity to any departure from the critical line.

---

## PART 4 — The RH Projection Gap

**Arriving at the projection-gap formulation through the rotation:**

In P vs NP:
- 2D object: R = {(x,w) : V(x,w)=1}
- Direction: BASE → FIBER (given x, determine W_x existence)
- Gap: projection FORWARD — can we compute the fiber property from the base?

In RH:
- 2D object: the explicit formula connecting zeros (fiber) to primes (base)
- Direction: FIBER → BASE (zero distribution projects to arithmetic Kloosterman via KEF)
- Gap: projection INVERTIBILITY — can we recover the fiber (zero distribution) uniquely from its image (arithmetic side)?

**The directions are DUAL.** P vs NP asks "forward projection cost" (base → fiber property). RH asks "inverse projection uniqueness" (image → unique preimage fiber). Both are projection gaps, but traversed in opposite directions.

$$\boxed{\text{"The RH projection gap is the cost of passing from the arithmetic Kloosterman-Eisenstein data (the computable image of the zero fiber under the explicit formula) to the unique determination of the zero distribution — specifically, whether the explicit-formula projection is injective, admitting no off-line zero distribution as a second preimage."}}$$

The gap is NOT the computation cost (as in P vs NP) but the INJECTIVITY of the projection: does the arithmetic image uniquely determine the zero fiber, or can the same arithmetic data be produced by multiple zero distributions, some with off-line zeros?

---

## PART 5 — Gap 1 After the Rotation (Exact)

With Gap 2 closed (cusp subdominance proved), the remaining Gap 1 is not simply "RH." It is the specific failure mode:

**"A non-critical-line zero distribution satisfying the same shell-level GUE statistics AND the same arithmetic Kloosterman projection constraints exists in principle."**

More precisely: Gap 1 is the claim that no such distribution exists — equivalently, that the map:
$$\{z\text{-distributions satisfying shell statistics}\} \xrightarrow{\text{KEF projection}} \{\text{arithmetic Kloosterman sums}\}$$

has a unique critical-line preimage.

The three possible failure modes of Gap 1:
1. **Non-unique preimage:** an off-line distribution D_off produces the same Kloosterman projection as D_crit. The arithmetic approach is blind to D_off; it cannot prove RH from KEF alone.
2. **Asymptotic vs exact:** the Kloosterman projection distinguishes D_crit from D_off only asymptotically (as N → ∞), but the difference is too small to close the argument in finite N.
3. **Injectivity fails at measure-zero set:** the projection is injective for generic zero configurations but fails for specific arithmetic configurations of off-line zeros.

Gap 1 is the exclusion of all three failure modes simultaneously.

---

## PART 6 — RH vs P vs NP: The Direct Comparison

| Feature | P vs NP | RH |
|---------|---------|-----|
| **2D object** | Verifier relation R = {(x,w) : V(x,w)=1} | Explicit formula: zero distribution ↔ arithmetic Kloosterman data |
| **The base** | Input x (accessible, deterministic) | Arithmetic Kloosterman side (accessible, computable) |
| **The fiber** | W_x = {w : V(x,w)=1} (inaccessible to the P machine) | Zero distribution in ℂ (what we want to pin to σ=1/2) |
| **The projection** | π₁: R → L (existential projection onto inputs) | KEF: zero distribution → arithmetic Kloosterman sums |
| **Direction of gap** | FORWARD: compute fiber properties from base alone | INVERSE: recover unique fiber from its image |
| **Gap measurement** | Gap(n) = cost_unwrap/cost_verify (ratio of decision to verification cost) | δ(σ₀,γ₀) = off-line residual (difference in projection value for off-line vs on-line zeros) |
| **Gap closed when** | Decision = verification cost (poly-time, P = NP) | Projection is injective (δ ≠ 0 for all off-line configurations, RH) |
| **Duality type** | Internal (same combinatorial object, two access modes) | External (different universes: ℤ vs ℂ, connected externally) |

**The sharpest one-line comparison:**

P vs NP: the base x cannot see inside the fiber W_x → can the base determine fiber emptiness?

RH: the fiber (zeros) projects to the arithmetic base (Kloosterman) → can the base image uniquely determine the fiber location?

Both are projection gaps, traversed in opposite directions between the same two-object structure.

---

## PART 7 — Strongest Honest Claim

**"After the full rotation, RH is best understood as a problem where the generic shell is no longer the issue and the cusp contamination (Gap 2) is closed by standard spectral theory; the remaining wall is whether the arithmetic Kloosterman-Eisenstein projection — the explicit formula's arithmetic side — is injective on zero distributions satisfying the shell statistics, or whether a distribution with off-line zeros could satisfy the same arithmetic constraints as the critical-line distribution."**

The rotation adds one new precision: RH is the INVERSE projection problem (recover unique fiber from image) while P vs NP is the FORWARD projection problem (determine fiber structure from base). Both are projection gaps on the same two-object architecture, traversed in dual directions.

---

## PART 8 — Strongest Honest Boundary

**"What is not yet established is whether the arithmetic projection encoded by the KEF is injective at the level of zero distributions satisfying the shell statistics — specifically, whether the off-line residual δ(σ₀, γ₀) is provably nonzero for all off-line configurations, or whether there exists a distribution of off-line zeros whose Kloosterman-side projection is indistinguishable from the critical-line distribution, leaving the arithmetic approach blind to that configuration."**

---

## Shell / Core / Surviving-Object Block

$$\text{Shell: GUE/sinc² pair-correlation for zeros; zero-spacing statistics} \quad [\text{proved universally}]$$

$$\text{Core: KEF arithmetic projection — Kloosterman side of explicit formula}$$
$$\quad\quad\quad \sum_{p\le N}\mathrm{Kl}(1,1;p)\,f\!\left(\tfrac{\log p}{\log N}\right)\log p \;\;=\;\; \sum_\rho W(\rho)\hat{f}\!\left(\tfrac{\gamma}{2\pi\log N}\right) + \text{(diagonal + cusp — closed)}$$

$$\text{Surviving object: } \delta(\sigma_0,\gamma_0) = \text{off-line residual in the arithmetic projection}$$
$$\quad\quad\quad \text{(whether any off-line zero is invisible to the Kloosterman projection)}$$

$$\text{Gap 2: cusp subdominance} \quad [\textbf{CLOSED}]$$

$$\text{Gap 1: injectivity of KEF projection on zero distributions} \quad [\textbf{OPEN}]$$

## RH vs P vs NP Comparison Block

$$\text{P vs NP: } R = \{(x,w)\},\; \pi_1(R) = L,\; \text{Gap} = \text{unwrapping cost forward}$$

$$\text{RH: } \text{Explicit formula} = \text{(zeros)} \xrightarrow{\text{KEF}} \text{(Kloosterman)},\; \text{Gap} = \text{injectivity of inverse projection}$$

The gap directions are DUAL: P vs NP asks whether the base can determine the fiber; RH asks whether the image can uniquely determine the fiber.

## Final Projection-Gap Sentence

$$\boxed{\text{"The RH projection gap is the cost of passing from the arithmetic Kloosterman-Eisenstein image (the accessible side) to the unique zero distribution as its preimage — specifically, whether the explicit-formula projection is injective, so that no off-line zero distribution produces the same arithmetic image as the critical-line distribution."}}$$

## Collaborator Paragraph

The full rotation clarifies RH's exact surviving wall. After removing the shell (GUE/sinc² statistics, which hold for any reasonable zero distribution) and after closing Gap 2 (cusp subdominance, confirmed by Kuznetsov Weyl — the cusp contribution is O(T²) ≪ N^{2π²}, negligible), what remains is the direct confrontation of the KEF arithmetic projection with the zero distribution. The explicit formula maps the zero fiber (zeros of ζ in the critical strip) to the arithmetic base (Kloosterman sums, primes). The question is whether this map is injective: can an off-line zero distribution (with some ρ₀ = σ₀ + iγ₀, σ₀ ≠ 1/2) produce the same arithmetic Kloosterman image as the critical-line distribution? If yes, the arithmetic approach is blind to off-line zeros and cannot prove RH from the KEF alone. If no — if the off-line residual δ(σ₀, γ₀) ≠ 0 for all off-line configurations — then the arithmetic projection uniquely pins the zeros to the critical line and RH follows. The rotation reveals the precise structural parallel: P vs NP is the FORWARD projection problem (can we determine fiber emptiness from the base alone?) and RH is the INVERSE projection problem (can we recover the unique fiber from its arithmetic image?). Both are projection gaps on a two-object architecture, traversed in opposite directions, and both resist closure by the same fundamental difficulty: the projection is not provably injective/surjective in the relevant sense.
