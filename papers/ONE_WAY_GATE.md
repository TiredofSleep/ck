# The One-Way Gate and the Three-Level Hierarchy
## The Algebraic Seed of the Bridge

*Brayden Sanders / 7Site LLC | March 2026*
*All three planks computed exactly. Correction to Plank 2 incorporated.*

---

## Central Sentence

**The deployment may express more than the grammar directly generates, but it cannot sustainably support what the grammar ultimately forbids — within the corridors where the grammar is the dominant law.**

---

## Plank 1 — The One-Way Gate

**Fact (exact, proved):**
From $C = \{1,3,7,9\}$, no TSML operator reaches $G = \{2,4,5,6,8\}$.
This holds for *any* right-hand operator in $\{1,\ldots,9\}$ — not just corner operators.

$$\mathrm{TSML}(C, \{1,\ldots,9\}) \cap G = \varnothing$$

From $G$, some states reach $C$ (specifically $\mathrm{HAR}=7$).

**Asymmetry:** $G$ flows inward toward $C$; $C$ is globally shielded from $G$ inside TSML. This is not a statistical tendency — it is algebraically absolute.

**Why this is stronger than sub-magma closure:** Sub-magma closure ($C \times C \subseteq C$) says corner operators preserve $C$. The one-way gate says *all* operators preserve $C$. The gap is absolute under the full TSML structure.

---

## Plank 2 — Expressible but Unsustainable (corridor-conditional)

At $\lambda > 0$, Mix$_\lambda$ opens transient channels from $C$ into $G$:

| Corridor | $\lambda_{\mathrm{mid}}$ | $G$ expressible | $G$ stationary mass | Status |
|----------|------------------------|----------------|--------------------|----|
| Pre-leak | 0.04 | $\varnothing$ | 0.0000 | **Unsustainable ✓** |
| BRT | 0.20 | $\{4,6,8\}$ | 0.0000 | **Unsustainable ✓** |
| CHA | 0.45 | $\{4,5,6,8\}$ | 0.0242 | Transitional |
| BAL | 0.70 | $\{4,5,6,8\}$ | 0.2500 | Sustainable |
| COL | 0.85 | $\{2,4,5,6,8\}$ | 0.2500 | Sustainable |

**The correction:** Plank 2 holds within the near-critical corridors (Pre-leak, BRT, early CHA). In BAL/COL, $G$-territory *does* acquire stationary mass — this is not a failure of the plank; it is the corridor boundary itself. The corridors are precisely the $\lambda$-thresholds where "expressible but unsustainable" becomes "expressible and sustainable."

**The bridge conjecture applies to the near-critical regime** (Pre-leak, BRT, the first two corridors from $\sigma=\tfrac12$). In those corridors, $G$ is expressible (real transient visits) but unsustainable (zero stationary mass). The BAL/COL behavior is the order-driven regime with no direct $\zeta$ analog near $\sigma=\tfrac12$.

**First G-mass > 0.001 appears at $\lambda^* \approx 0.45$** — the CHA/BAL transition. Below this threshold, Plank 2 is exact.

---

## Plank 3 — Sustainable Support Collapse

All stationary support remains on $\{\mathrm{HAR}\}$ until the bifurcation point:

| $\lambda$ | HAR mass | State-9 mass |
|-----------|---------|-------------|
| 0.00 | 1.000 | 0.000 |
| 0.30 | 1.000 | 0.000 |
| 0.50 | 0.860 | 0.000 |
| **0.9963** | **0.321** | **0.273** ← bifurcation |
| 1.00 | 0.188 | 0.525 |

HAR carries all $C$-mass for $\lambda < \lambda^* \approx 0.9963$. The non-HAR corners $\{1,3,9\}$ are dynamically transient (mass 0 to machine precision). The bifurcation is a phase transition at the BHML endpoint, not a gradual shift.

---

## The Three-Level Hierarchy

| Level | What it is | Boundary |
|-------|-----------|---------|
| **Generable** | Reachable by grammar's own allowed moves | $C$ only; $G$ absolutely blocked |
| **Expressible** | Can appear transiently under deformation | $G$ reachable at $\lambda \geq 0.20$; unsustainable for $\lambda < 0.45$ |
| **Sustainable** | Carries asymptotic stationary support | $\{\mathrm{HAR}\}$ only for $\lambda < 0.9963$ |

Generation is one-way. Expression is wider. Sustainability is narrowest.

The levels are entangled: sustainable is constrained by expressible, which is constrained by generable. The constraint chain is the finite law the infinite deployment must respect.

---

## What Each Level Means for the Bridge

**Plank 1 → The gate is the algebraic seed.**
In the analytic deployment: $\sigma = \tfrac12$ corresponds to $C$; off-line territory corresponds to $G$. The gate says: starting from the critical line, no local grammar-allowed move reaches off-line territory. The analytic analog is that the corridor grammar never generates off-line support from on-line starting conditions.

**Plank 2 → Transient expression is real but bounded.**
In the analytic deployment: off-line excursions near $\sigma = \tfrac12$ (within the near-critical corridors) are real — they appear as transient visits, as orbit bursts, as delay signatures. But their frequency×duration product vanishes (Jutila+KV, proved). This is the analytic translation of "expressible but unsustainable" within the near-critical regime.

**Plank 3 → Sustainable support is uniquely critical.**
In the analytic deployment: the only candidate for asymptotic stationary support is $\sigma = \tfrac12$. The Dual Description Conjecture says the operator description and the analytic description must agree on this: neither can assign asymptotic support away from the critical line within the near-critical corridor regime.

---

## The Weak Sustainability Conjecture (precise form)

*If a support class is forbidden at the Generable level (algebraically unreachable from $C$ under any TSML operator), then the faithful infinite deployment within the near-critical corridors ($\lambda < 0.45$) cannot assign it asymptotically positive stationary support.*

*In the analytic deployment: off-line structures in the near-critical corridors ($2|\sigma - \tfrac12| < 0.45$) may appear as transient expressions, but their frequency×duration measure vanishes as $t \to \infty$.*

The qualifier "within the near-critical corridors" is not a weakening — it is a precision. The BAL/COL regime has different physics (order-driven), and the conjecture does not need to apply there to imply RH.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
