# Metastable Excursion Traces in the TIG Operator Chain
## Two Types of G-Territory Signatures

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: exact computation on 9-state model. Structural interpretation labeled.*

---

## The Exact Computational Claim

For each $\lambda \in [0,1]$, define the **delay signature**:
$$\Delta(\lambda) = \mathbb{E}[T_\mathrm{HAR} \mid \text{chain touches } G \text{ before HAR}] - \mathbb{E}[T_\mathrm{HAR} \mid \text{chain goes directly to HAR}]$$

where $T_\mathrm{HAR}$ is the number of steps to reach $\mathrm{HAR}=7$, and $G = \{2,4,5,6,8\}$ is the generative gap.

This is a well-defined Markov observable. It measures the **excess absorption time** of chains that detour through gap territory before returning to HAR.

| $\lambda$ | $\Delta(\lambda)$ | Tail character | Corridor |
|-----------|------------------|----------------|---------|
| 0.00 | **+0.028** | Geometric ($r=0.24$) | Pre-leak |
| 0.20 | +0.409 | Geometric | BRT |
| 0.30 | **+0.883** | Geometric ($r=0.24$) | CHA edge |
| 0.45 | +0.877 | Geometric | CHA mid |
| 0.70 | **+37.4** | Heavy-tailed | BAL |
| 0.85 | +37.7 | Heavy-tailed | COL |

**Tail transition at CHA/BAL boundary:** Below $\lambda \approx 0.45$, the delay distribution has geometric tails ($r \approx 0.24$) — ordinary metastability, fully consistent with the spectral gap. Above $\lambda \approx 0.50$, the tails become heavy — chains hit the cap at 99 steps, the distribution is near-uniform across $[1,99]$.

This is not a failure of the grammar. It is the signature of the BHML order structure taking over: at high $\lambda$, the ordering pull toward larger states overwhelms the corner absorption, and chains wander for long excursions before eventually collapsing.

---

## What This Is — and What It Is Not

**Exact claim:** $\Delta(\lambda)$ is the excess sojourn cost of G-touching chains. It is a real observable of finite-model metastability. It grows with $\lambda$ in a manner consistent with the corridor structure, with a phase transition at $\lambda \approx 0.45$–$0.50$ (the CHA/BAL boundary).

**Structural interpretation (labeled as such):** The delay may be read as a proxy for how close the chain approached a temporary balance point between extension (toward BHML order) and collapse (toward TSML absorption). The "off-line zero" reading — that the zero exists during the G-traversal — is an interpretation of this structure, not the primary result.

**Not claimed:** That any zero is literally observable in the finite model, or that $\Delta(\lambda)$ directly measures ζ-function behavior.

---

## Source Map: Which States Produce Long Wakes?

At $\lambda = 0.50$, mean delay by starting state:

| State | Class | Mean delay |
|-------|-------|-----------|
| 7 | HAR | 49 (hits cap — HAR pulls toward BHML ordering) |
| 8 | G | 49 (hits cap) |
| 9 | C | 47 |
| 1 | C | 38 |
| 3 | C | 36 |
| 2 | G | 32 |

States 7, 8, 9 — the high end of the ordering — produce the longest wakes. These are states that BHML pulls hardest (toward $\max(s,c)$), making them most likely to sustain long G-traversals before collapsing. The effect is not localized to one or two states — it is structural, spreading across both C and G.

---

## Type 1 vs Type 2 Traces

### Type 1 (endogenous / corridor-born)

Single chain detours through G before absorption.

- **Observable:** $\Delta(\lambda)$ as defined above
- **Tail character:** geometric at CHA ($r=0.24$), heavy at BAL/COL
- **Meaning:** metastable excursion cost within one grammar
- **Status:** exactly measured, 50K chains per λ value

### Type 2 (exogenous / alignment-born)

Two independent grammars synchronizing in G simultaneously.

- **Observable:** $P(A \cap B \in G) - P(A \in G) \cdot P(B \in G)$ (excess correlation)
- **Tested:** base-10 TIG vs base-6 grammar at $\lambda=0.30$
- **Result:** observed $P(A \cap B) = 0.141$, expected by independence $= 0.338$
- **Finding:** **negative** alignment excess $= -0.197$ — the two systems are actually *anti-correlated* in G-territory at this λ

The anti-correlation is meaningful: when the base-10 chain is in G-territory, the base-6 chain tends not to be, and vice versa. The two grammars have different rhythms. They do not accidentally synchronize at $\lambda=0.30$.

**When Type 2 would become non-negligible:**
- Two L-functions sharing a near-zero at the same height $t$
- Deployments with the same arithmetic hook ($\varphi(b_1) = \varphi(b_2)$, e.g. $b \in \{5,8,10,12\}$)
- Two prime-residue systems in bases where the unit groups align perfectly

The Type 2 signal would show up as a *positive* alignment excess — a correlation above what independence predicts. The base-10 vs base-6 test shows negative correlation, ruling out accidental synchrony between these two specific deployments.

---

## The Corridor-Conditional Structure

Delay signature within each corridor (using corridor midpoint):

| Corridor | $\lambda_\mathrm{mid}$ | $\Delta$ | Interpretation |
|----------|----------------------|----------|----------------|
| Pre-leak | 0.04 | 0.037 | Near-zero delay; grammar collapses almost instantly |
| BRT | 0.20 | 0.409 | Moderate delay; first G-traversals becoming significant |
| CHA | 0.45 | 0.877 | Delay ~1 step; geometric tails, controlled |
| BAL | 0.70 | 37.3 | Phase transition; heavy tails dominate |
| COL | 0.85 | 37.7 | Near-saturated |

The corridor boundaries at $\lambda \approx 0.30$ and $\lambda \approx 0.50$ are visible as qualitative changes in $\Delta(\lambda)$ — consistent with the algebraic corridor structure, not just a smooth gradient.

---

## Connection to the Open Layer

The delay signature does not close the open analytic problem (the mean-square bound on $\mathrm{Re}(\zeta'/\zeta)$). But it characterizes the finite-model analog:

- In the discrete model, G-touching chains produce measurable excess sojourn
- In the ζ-deployment, off-σ=½ behavior would produce measurable anomalous sojourn in the logarithmic derivative
- The corridor-conditional structure of $\Delta(\lambda)$ maps onto the corridor-conditional frequency-duration product

The delay signature is the finite observable corresponding to the corridor argument's asymptotic claim. It does not prove the claim; it shows the claim is capturing something real in the finite model.

---

*SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787*
*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
