# The Dual Description Conjecture
## Locating the Missing Compatibility Between Two Infinite Deployments

*Brayden Sanders / 7Site LLC | March 2026*
*Status: CONJECTURE. This document locates the open problem. It does not prove anything.*

---

## The 2×2 Matrix

|  | **Support / Grammar** | **Expression / Rate** |
|--|----------------------|----------------------|
| **Finite (exact)** | **TSML** — closure grammar, sub-magma chain, generative gap G, HAR unique attractor. *FROZEN, proved.* | **BHML** — order/deformation, Mix_λ family, corridor transitions. γ=3/4 exact. *FROZEN, proved.* |
| **Infinite (open)** | **Transfer operator** — stationary support, gap persistence, corridor faithfulness, B(λ). *Route A, open.* | **Analytic number theory** — zero density (Jutila, proved), KV floor (Ford, proved), mean-square Re(ζ'/ζ), drift rate. *Route B, partly open.* |

The missing object is not a fifth cell. It is the **compatibility relation between the two infinite cells** — the theorem that says they cannot disagree about where stationary support lives.

---

## Definition: Faithful Dual Description

Two infinite deployments of a finite grammar are *faithful dual descriptions* if they preserve:
1. The same stationary support set
2. The same deformation ordering
3. Compatible rate and support constraints — neither can hold without the other

---

## The Conjecture

**Conjecture (Dual Description, weak form).**
*In the near-critical regime $\lambda = 2|\sigma - \tfrac12| < 0.45$ (Pre-leak and BRT corridors, where "expressible but unsustainable" holds exactly), at least one of the following holds without assuming RH:*
*(B) ⇒ (A): If the drift rate bound holds in this window, the operator cannot have stationary support off σ=½.*
*(A) ⇒ (B): If the operator has unique stationary support at σ=½ in this window, the drift rate satisfies the mean-square bound.*

**Conjecture (Dual Description, strong form).**
*(A) and (B) are equivalent within $\lambda < 0.45$: each implies the other, and both are equivalent to RH.*

**Domain note:** The conjecture is stated in the near-critical window only. The BAL/COL regime ($\lambda > 0.45$) exhibits order-driven behavior — G-territory becomes genuinely sustainable there — but that regime has no direct $\zeta$ analog near $\sigma=\tfrac12$ and is not required for the RH argument. Restricting to $\lambda < 0.45$ is not a weakening; it is the correct statement of where the bridge operates.

Where:

**(A) Support statement (operator language):**
$K_\lambda$ has unique stationary support at $\sigma=\tfrac12$ for all $\lambda < \lambda^*\approx 0.9963$.

**(B) Rate statement (analytic language):**
$$\frac{1}{T}\int_1^T \left|\mathrm{Re}\frac{\zeta'}{\zeta}(\sigma+it)\right|^2 dt \;\leq\; C_\mathrm{TIG} \cdot \lambda(\sigma)^2 \cdot (\log T)^2 \quad \text{for all }T, \sigma$$
without assuming RH, where $C_\mathrm{TIG} = 250/21$.

**Epistemic note on (B):** The constant $C_\mathrm{TIG} = 250/21$ is predicted by the finite grammar. It is *empirically supported* ($C_\mathrm{emp} \leq 11.023 < 11.905$ at tested heights) but not proved. Classical bounds give only $O(\log t / \lambda)$, which is $\sim$50× too weak.

---

## How Each Clause Gives RH (spelled out)

**(A) gives RH:** If $K_\lambda$ has unique stationary support at $\sigma=\tfrac12$, then by the frequency×duration argument (Jutila + two-tick, proved), no trajectory can accumulate off the critical line asymptotically. The Halving Lemma then excludes zeros off $\sigma=\tfrac12$.

**(B) gives RH:** If Re(ζ'/ζ) cannot drift by more than $C_\mathrm{TIG}\lambda^2$ in mean-square, then the integrated drift across any corridor is bounded. Combined with the KV floor (Ford 2002), no corridor can sustain a zero off $\sigma=\tfrac12$ for all $t$.

Both arguments are conditional — neither (A) nor (B) has been proved. They are the two routes.

---

## The Finite Analogy (with honest labeling)

| Finite | Infinite | Status |
|--------|---------|--------|
| TSML closure → HAR attractor | Transfer operator → σ=½ support | **Open** (Route A) |
| BHML order → γ=3/4 | Drift rate → C_TIG bound | **Open** (Route B); C_TIG empirical |
| Mix_λ deformation | Equivalence (A)↔(B) | **Open** (the Dual Description) |
| γ = 1−1/φ(b) = 3/4 (exact) | C_TIG = 250/21 (predicted, empirical) | Finite exact; infinite conjectural |

The fourth row is the weakest correspondence. The finite constant is proved from the table. The infinite constant is predicted by the grammar and supported empirically, but has no proof. It should not be treated as established.

---

## What Would Falsify the Dual Description

The conjecture fails if either of the following is demonstrated:

**Falsifier 1 (A without B):**
The continuous operator $K_\lambda$ has unique stationary support at $\sigma=\tfrac12$ within $\lambda < 0.45$, yet $C_\mathrm{emp}$ exceeds $C_\mathrm{TIG}$ at some height $t$ in that window.
→ This would mean support is controlled but rate is not — the two descriptions decouple within the near-critical domain.

**Falsifier 2 (B without A):**
The drift rate bound (B) holds for all $t$, yet the operator $K_\lambda$ develops non-trivial stationary support off $\sigma=\tfrac12$ at some scale.
→ This would mean the analytic rate is fine but the support structure is wrong — the grammar fails to deploy faithfully.

**Falsifier 3 (neither direction implies the other):**
Someone proves (A) without being able to derive (B), and separately proves (B) without being able to derive (A), using essentially different techniques.
→ This would mean (A) and (B) are independent true statements, not dual descriptions. RH still follows from either, but the Dual Description framework is wrong — they are not two faces of one object.

None of these falsifiers have been demonstrated. None have been ruled out.

---

## Why One Infinite System Is Not Enough

The operator side alone gives:
- Support structure, attractor geometry, corridor faithfulness
- Does *not* give: frequency, density, how often things happen at large $t$

The analytic side alone gives:
- Density, growth, asymptotic bounds
- Does *not* give: the grammar of why certain supports are forbidden

The Dual Description says these two descriptions cannot disagree about where stationary support lives. If the operator says "only σ=½," the analytic side must produce a drift bound that enforces it. If the drift bound holds, the operator cannot place stationary mass elsewhere.

This is the same reason the finite model needed two tables: one object does not show both what is allowed and how allowance deforms.

---

## Summary

The open problem is not to derive one infinite system from the other. It is to prove that both are faithful dual descriptions of the same finite grammar — that they cannot disagree about stationary support.

The finite model makes this plausible by supplying an exact analogy (TSML/BHML/Mix_λ), exact constants (γ=3/4, C_TIG=250/21), and a four-layer realization. It does not prove the Dual Description. It locates where the proof must go.

---

---

## 4-Lattice Constraint Set (Added March 2026)

The 4-lattice construction provides a concrete finite test for the compatibility theorem.
The compatibility question is now specific:

*Do the operator deployment and the analytic deployment both preserve the four non-trivial 4-lattice nodes?*

**The four nodes:**
1. **Gap floor ≥ ¼** — the order-seeded lower bound on mixing speed, set by the BHML endpoint
2. **BHML residual structure** — 6 cells following the order law, persisting through all corridors
3. **C-dominance** — corner class carries dominant stationary mass
4. **Single dominant state** — one state (or narrow region near σ=½) carries dominant support

**The structural result behind these:** The deformation-wide gap floor is set by the order grammar (BHML gap = ¼ exactly), not the closure grammar (TSML gap = 0.474). The closure grammar generates richer structure above the floor; the order grammar is the stabilizing bound.

**Epistemic status of the constraint set:** The four nodes are computed from the 3-lattice survivors. The claim that the infinite deployments must preserve them is the Dual Description Conjecture in concrete form. This is not proved — it is precisely stated.

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
