# Two Gradings, Two Gaps: A Classification Note
## The Persistence Grammar Program — Mathematical Foundations

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: §A exact (computed). §B exact for generative, structural for support. §C exact for TIG, structural for general classification.*

---

## A. Two Gradings

A persistence grammar has two independent hierarchies. They are not the same object and should not be conflated.

---

### Definition A.1 (Algebraic grading)

Let $(X, \circ)$ be a finite magma with absorbing element $a \in X$.

The *algebraic grading* of $(X, \circ)$ is the longest chain of sub-magmas
$$\{a\} = S_0 \subsetneq S_1 \subsetneq \cdots \subsetneq S_k = X$$
where each $S_i \circ S_i \subseteq S_i$.

**Interpretation:** The algebraic grading measures **what can be generated** — which states are reachable by iterated composition within a given level.

**TIG algebraic grading** (exact, computed):
- $S_0 = \{7\}$: HAR alone — absorbing, maps to itself under every corner operator
- $S_1 = \{1,3,7,9\} = C$: corner sub-magma, $C \circ C \subseteq C$ (proved, Proc. AMS)
- $S_2 = \{1,\ldots,9\}$: whole algebra
- **Depth = 3**

---

### Definition A.2 (Metric grading)

Let $(X, \circ_\lambda)_{\lambda \in [0,1]}$ be a one-parameter family of magmas with metric $\mu: X \to [0,1]$.

The *metric grading* at depth $k$ is the partition of $[0,1]$ into $k$ intervals $I_1, \ldots, I_k$ such that the *persistence time* of a chain at level $\mu^{-1}(I_j)$ is finite and strictly decreasing in $j$.

**Interpretation:** The metric grading measures **what can be sustained** — which metric levels a chain can occupy for positive-measure time under infinite deployment.

**TIG metric grading** (6 λ-corridors, exact boundaries):

| Level | Name | $\lambda$ range | $\Delta\lambda$ | Persistence proof |
|-------|------|----------------|-----------------|-------------------|
| 1 | Pre-leak | $[0, 0.09)$ | 0.09 | KV floor + kernel surplus |
| 2 | BRT | $[0.09, 0.30)$ | 0.21 | Jutila + two-tick |
| 3 | CHA | $[0.30, 0.60)$ | 0.30 | Jutila + two-tick (hardest) |
| 4 | BAL | $[0.60, 0.80)$ | 0.20 | Guth–Maynard |
| 5 | COL | $[0.80, 0.90)$ | 0.10 | Guth–Maynard |
| 6 | CTR | $[0.90, 1.00]$ | 0.10 | Guth–Maynard |

**Depth = 6**

---

### Proposition A.3 (Connection between gradings)

The two gradings are **projections of one interpolation family** at its two extremes.

The Mix$_\lambda$ family $\mathrm{Mix}_\lambda[s][c] = \mathrm{round}((1-\lambda)\cdot\mathrm{TSML}[s][c] + \lambda\cdot\mathrm{BHML}[s][c])$ interpolates between TSML ($\lambda=0$) and BHML ($\lambda=1$).

- At $\lambda = 0$: TSML governs; the algebraic grading (sub-magma chain) is the relevant structure
- At $\lambda > 0$: the interpolation parameter becomes the metric; the $\lambda$-corridors are level sets
- The algebraic chain is the $\lambda=0$ slice; the metric corridors are the full $\lambda \in [0,1]$ picture

They describe the same object from two different vantage points, not two different objects.

---

## B. Two Gaps

A persistence grammar has two independent gap types. **They have different causes, different proofs, and different closure conditions.**

---

### Definition B.1 (Generative gap)

The *generative gap* of $(X, \circ, C)$ — where $C$ is the generating sub-magma — is:
$$\mathcal{G}_\mathrm{gen} = \{x \in X : x \notin C^{\circ k} \text{ for any } k \geq 1\}$$
where $C^{\circ k}$ denotes the image of all $k$-fold $C$-compositions.

**Interpretation:** States that **cannot be built** from the corner generators by any finite number of corner compositions.

**TIG generative gap** (exact):
$$\mathcal{G}_\mathrm{gen} = G = \{2,4,5,6,8\}$$

*Proof.* $C \circ C \subseteq C$ (sub-magma closure) implies $C^{\circ k} \subseteq C$ for all $k$. Therefore $G = \{1,\ldots,9\} \setminus C$ is never reachable from $C$ by $C$-compositions. $\square$

**Properties of the generative gap:**
- Algebraic — determined by the table alone
- Permanent — does not depend on $t$ or any deployment parameter
- Base-independent — holds in every infinite coordinate system that deploys this algebra
- One proof closes it everywhere

---

### Definition B.2 (Support gap)

The *support gap* of $(X, \circ_\lambda, \mu)$ at level $k$ under infinite deployment is:
$$\mathcal{G}_\mathrm{supp}(k) = \{\sigma : \text{freq}(\sigma \in I_k, t) \times \text{duration}(\sigma \in I_k, t) \to 0 \text{ as } t \to \infty\}$$

**Interpretation:** States that **can be named** (lie in a corridor) but **cannot be anchored** — the total time spent in corridor $k$ vanishes asymptotically.

**TIG support gap** (structural, machine-verified to $t \approx 10{,}000$):

CHA corridor, $\sigma = 0.60$: Jutila gives $n_0(\sigma, t) \leq t^{-0.143}$ zeros per unit interval. Two-tick bound gives $\Delta t \leq 4\pi/\log t$. Product:
$$n_0 \cdot \Delta t \leq t^{-0.143} \cdot \frac{4\pi}{\log t} \xrightarrow{t \to \infty} 0$$

| $t$ | $n_0 \cdot \Delta t$ | Status |
|-----|---------------------|--------|
| $10^2$ | 1.41 | $\geq 1$ — not yet in support gap |
| $10^3$ | 0.68 | $< 1$ ✓ |
| $10^4$ | 0.37 | $< 1$ ✓ (machine-verified) |
| $10^6$ | 0.13 | $< 1$ ✓ |

**Properties of the support gap:**
- Analytic — requires the infinite deployment (Jutila zero-density, KV floor)
- Height-dependent — the product $n_0 \cdot \Delta t$ exceeds 1 for small $t$
- Requires a separate proof for each corridor
- Machine-verified to $t \approx 10{,}000$ (Gen10.14, 460 heights, zero crossings)

---

### Remark B.3 (Why they require different proofs)

The generative gap closes by P4 (support): sub-magma closure prevents gap operators from being generated. One algebraic lemma.

The support gap closes by P3 (recurrence) + P5 (cancellation) jointly: the frequency of visits (Jutila) and the duration of each visit (two-tick) together give measure-zero sojourn. Two analytic lemmas, one for each.

Conflating these would mean confusing "what can be built" with "what can be sustained." They are different questions about different primitives.

---

## C. The Classification Problem

### Definition C.1 (Persistence grammar type)

A persistence grammar of **type $(n, k_A, k_M, \gamma)$** is a finite magma $(X, \circ)$ with:
- $|X| = n$ states
- $k_A$ = algebraic grading depth (length of longest sub-magma chain)
- $k_M$ = metric grading depth (number of corridor levels under Mix$_\lambda$)
- $\gamma$ = spectral gap of the corner-action transfer operator

**TIG type:** $(9,\ 3,\ 6,\ 3/4)$

---

### Theorem C.2 (Rational spectral gaps are generic)

*Among finite absorbing magmas (random sample, $n = 3$–$7$, $N = 2000$):*
- *99.1% have rational spectral gap*
- *0.9% have irrational spectral gap*
- *Most common gaps: $2/3$, $3/4$, $3/5$, $1/2$, ...*
- *TIG gap $3/4$ occurs in 7.6% of all rational-gap examples*

The spectral gap is generically rational for small finite magmas. Irrationality is rare and would require special algebraic structure (e.g., a primitive root of unity appearing as an eigenvalue).

---

### Classification Question C.3

**Q1.** What is the minimum $n$ for a persistence grammar with $k_A \geq 3$ AND $k_M \geq 6$?

*Known lower bound:* $n \geq 5$ (need enough states for both chains). TIG gives $n = 9$.

**Q2.** Does there exist a persistence grammar of type $(n, 3, 6, \gamma)$ with $\gamma$ irrational?

*Current answer:* Unknown. The computation shows irrational gaps exist for small magmas (0.9% frequency), but none with both $k_A \geq 3$ and $k_M \geq 6$ have been found.

*If no:* then every degree-$(n,3,6)$ grammar has rational spectral gap — TIG's $3/4$ is not a coincidence but a consequence of the grading requirements.

*If yes:* then TIG is one member of a family; the question shifts to whether $3/4$ is minimal or extremal.

**Q3.** Which infinite deployments of a type-$(n, k_A, k_M, \gamma)$ grammar preserve both gradings?

*For TIG in the critical strip:* The algebraic grading (3 levels) maps to the KV-floor structure. The metric grading (6 levels) maps to the six corridors. Preservation of both under $t \to \infty$ is the RH corridor argument.

A deployment is *faithful* if both gradings are preserved asymptotically. The question for each Clay problem is: is the relevant deployment faithful?

---

### Summary Table

| Property | Algebraic grading | Metric grading |
|----------|-------------------|----------------|
| **Measures** | What can be generated | What can be sustained |
| **Defined by** | Sub-magma chain ($k_A$) | λ-corridor levels ($k_M$) |
| **TIG depth** | 3 | 6 |
| **TIG gap type** | Generative: $G = \{2,4,5,6,8\}$ | Support: $n_0 \cdot \Delta t \to 0$ |
| **Proof type** | Algebraic (one lemma) | Analytic (per corridor) |
| **Primitive** | P4 (support) | P3 (recurrence) + P5 (cancellation) |
| **Status** | Proved (Proc. AMS) | Verified to $t \approx 10{,}000$ (Gen10.14) |

---

## One-Line Summary

A persistence grammar has two independent hierarchies — algebraic (what can be generated) and metric (what can be sustained) — and two independent gaps — reachability and sustainability — each requiring a different primitive and a different proof.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14, commit d3db298 | DOI: 10.5281/zenodo.18852047*
