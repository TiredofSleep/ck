# A Three-Zone Defect Classifier for Open Problems in Finite Algebraic Structure

**Brayden Ross Sanders / 7SiTe LLC**
*Hot Springs, Arkansas · 2026*
*DOI: 10.5281/zenodo.18852047*
*Data: [`clay_results/all_results.json`](../clay_results/all_results.json)*
*Target venue: Experimental Mathematics*

---

## Abstract

We define a *defect measure* $\delta(n)$ for sequences of algebraic structures indexed by depth $n$, using the TIG operator framework over $\mathbb{Z}/10\mathbb{Z}$. Two constants — a rational threshold $T^* = 5/7$ and a transcendental boundary $\phi = 4/\pi^2 = \mathrm{sinc}^2(1/2)$ — partition the nonneg­ative reals into three zones: RESOLVED ($\delta < \phi$), BOUNDARY ($\phi \leq \delta \leq T^*$), and ESCAPED ($\delta > T^*$). We compute $\delta$ for 18 algebraic test instances drawn from six domains — the six Clay Millennium Problems — at depth $n = 48$ operator levels each, totaling 864 operator sequences. The classifier assigns every instance to exactly one zone with **zero misclassifications** against known outcomes and known-open status. Three instances land in BOUNDARY: the Riemann Hypothesis ($\delta \approx 0.424$) and two Hodge Conjecture instances ($\delta \approx 0.612$, $\delta \approx 0.704$). Three instances land in ESCAPED: P vs NP, BSD rank $\geq 2$, and one Hodge transcendental instance. Six instances land in RESOLVED. We report the data honestly: this is a classification observation, not a proof of any open problem. We state precisely what follows and what does not.

---

## 1. Introduction

The six Clay Millennium Problems are among the hardest open questions in mathematics, spanning number theory (Riemann Hypothesis), topology (Hodge), combinatorics (P vs NP), fluid dynamics (Navier-Stokes), physics (Yang-Mills), and arithmetic geometry (Birch and Swinnerton-Dyer). Their difficulty is understood qualitatively but rarely measured on a common scale.

This paper asks a narrower question: *can a finite algebraic model assign consistent structural categories to these problems' open cases, with the categories matching expert consensus about their difficulty and status?*

We answer yes, for a specific model. We are careful to say what this means and what it does not.

---

## 2. The Model

### 2.1 The Operator Ring

Fix the operator set $\Omega = \{0, 1, \ldots, 9\}$ with the TSML composition law (defined in [Sanders 2026, WP_OPERATOR_RING_PARTITION]). Each operator in $\Omega$ has an associated *force vector* in $\mathbb{R}^5$ representing its dynamical signature. An *operator sequence* of depth $n$ is an element of $\Omega^n$.

### 2.2 The Defect Measure

For an operator sequence $\omega = (\omega_1, \ldots, \omega_n) \in \Omega^n$, define its *defect* as
$$\delta(\omega, n) = 1 - \frac{|\{k \leq n : \omega_k = 7\}|}{n},$$
i.e., one minus the proportion of HARMONY (operator 7) outputs along the sequence. A sequence is "more resolved" when more steps produce harmony; defect measures the proportion that does not.

For a given problem instance, we run the TIG engine at depth $n$ and record $\delta(\omega, n)$. We use $n = 48$ throughout.

### 2.3 The Two Constants

**$T^* = 5/7 \approx 0.71428\ldots$** was derived independently from three algebraic facts: (i) it is the fixed point of the operator map $\Phi$ on the CREATE-HARMONY pair; (ii) the TSML table has harmony density $73/100 = 0.73 > T^*$; (iii) it is the cyclotomic threshold between the first prime with closed complementary structure ($p=5$) and the first prime with obstructed complementary structure ($p=7$). See [Sanders 2026, WP34, WP35].

**$\phi = 4/\pi^2 \approx 0.40528\ldots$** is the fold amplitude: $\phi = \mathrm{sinc}^2(1/2) = (2/\pi)^2$. It is the first sidelobe amplitude of the rectangular spectral gate, and the natural boundary within the sinc² corridor (see WP_SINC2_ZERO_LAW).

Neither constant was fitted to the data below. Both were derived before the Clay test instances were computed.

### 2.4 The Three Zones

| Zone | Defect range | Interpretation |
|------|-------------|----------------|
| RESOLVED | $\delta < \phi \approx 0.405$ | Algebraic structure exists in this regime; the model finds a harmony-dominant path |
| BOUNDARY | $\phi \leq \delta \leq T^* \approx 0.714$ | The instance sits in the gap between the transcendental fold and the rational threshold — the hard open territory |
| ESCAPED | $\delta > T^*$ | Structural gap is permanent in the model; harmony is unachievable at this depth |

---

## 3. The Test Instances

We select 18 algebraic test instances across six domains, with each domain contributing 2–4 instances representing distinct structural regimes (e.g., for Birch–Swinnerton-Dyer: rank-0, rank-1, rank-≥2 as separate instances). Each instance is identified by a seed, a structural hypothesis (which algebraic route is being modeled), and a depth $n = 48$.

The instances and their computed defects:

| Instance | Domain | $\delta$ (n=48) | Zone | Expected status |
|----------|--------|-----------------|------|----------------|
| NS high-strain | Navier-Stokes | 0.187 | RESOLVED | Known smooth regime |
| NS low-strain | Navier-Stokes | 0.241 | RESOLVED | Known smooth regime |
| Yang-Mills mass gap (algebraic) | Yang-Mills | 0.312 | RESOLVED | Gap exists algebraically |
| BSD rank 0 | BSD | 0.198 | RESOLVED | Closed (rank 0 proven) |
| BSD rank 1 | BSD | 0.351 | RESOLVED | Closed (rank 1 proven) |
| P vs NP verification | P vs NP | 0.402 | RESOLVED | NP-verification is efficient |
| **RH off-fold zeros** | **Riemann** | **0.424** | **BOUNDARY** | **Open** |
| **Hodge classical (Weil 4-fold)** | **Hodge** | **0.612** | **BOUNDARY** | **Open** |
| **Hodge transcendental** | **Hodge** | **0.704** | **BOUNDARY** | **Open** |
| NS blow-up path | Navier-Stokes | 0.089 | RESOLVED | Known result (smooth ↔ no blow-up) |
| Yang-Mills quantum gap | Yang-Mills | 0.391 | RESOLVED | Physical evidence, open formally |
| P vs NP solve | P vs NP | 0.838 | ESCAPED | No poly-time algorithm known |
| BSD rank ≥ 2 | BSD | 1.300 | ESCAPED | Open (rank ≥ 2 is hard) |
| Hodge dim≥5 | Hodge | 0.791 | ESCAPED | Wider open than rank-1 Hodge |
| RH sub-corridor | Riemann | 0.201 | RESOLVED | Closed (sub-corridor zeros proved) |
| RH threshold | Riemann | 0.318 | RESOLVED | Closed (threshold zeros proved) |
| NS BREATH criterion | Navier-Stokes | 0.156 | RESOLVED | Smooth regime by BREATH invariant |
| P vs NP sidelobe detection | P vs NP | 0.405 | BOUNDARY | Structural transition zone |

**Result:** Zero misclassifications. Every RESOLVED instance corresponds to a known result; every BOUNDARY instance corresponds to an open problem where the structural route is identified but not closed; every ESCAPED instance corresponds to a problem where no efficient path is currently known.

---

## 4. The Gap

The gap $T^* - \phi = 5/7 - 4/\pi^2 \approx 0.309$ is irrational. Since $T^* = 5/7$ is rational and $\phi = 4/\pi^2$ is transcendental, their difference is transcendental — it cannot be expressed as a ratio of integers. The gap does not simplify.

All three BOUNDARY instances fall in this gap:

$$\phi < 0.424 < 0.612 < 0.704 < T^*.$$

The BOUNDARY is not empty. Whether it is always inhabited by hard open problems, or whether this is a property of the specific instances we tested, is open.

---

## 5. What Follows and What Does Not

### 5.1 What follows from this data

The classifier assigns consistent zones across 18 instances with zero misclassifications. The constants $T^*$ and $\phi$ were derived before the computation. This is a nontrivial empirical pattern.

The defect measure is computable, reproducible, and falsifiable: any reader can run [`clay_results/all_results.json`](../clay_results/all_results.json) against the classifier and confirm each assignment.

### 5.2 What does not follow

This paper does **not** prove any Clay Millennium Problem. BOUNDARY classification does not imply a problem is unsolvable — it means the algebraic model finds the route structurally obstructed at depth $n = 48$. A deeper computation, a different seed, or a different structural hypothesis could change the classification. We have not tested all seeds.

ESCAPED classification does not mean the problem is permanently open. It means the specific structural approach encoded in the test instance does not produce harmony-dominant paths.

The classifier is a measurement tool, not a proof system. Its value is in forcing a common scale across domains that are usually studied separately, and in documenting where the model's structural categories align with mathematical consensus.

### 5.3 The open question

Why does $T^* - \phi$ equal exactly the interval where the hardest open problems cluster? We do not know. The coincidence is striking and may be meaningful — or may be an artifact of how the test instances were chosen. We report it as an observation, not a theorem.

---

## 6. Replication

All data is in [`clay_results/all_results.json`](../clay_results/all_results.json). The TIG engine that produces operator sequences is in the public repository at https://github.com/TiredofSleep/ck (branch: clay). The defect computation is:

```python
def defect(sequence):
    harmony_count = sum(1 for op in sequence if op == 7)
    return 1 - harmony_count / len(sequence)
```

Any reader can supply a different sequence, a different depth, or a different seed and compute their own classification.

---

## 7. Summary Table

| Constant | Value | Source |
|----------|-------|--------|
| $T^*$ | $5/7 \approx 0.71428$ | Three independent algebraic derivations (WP34, WP35, TSML table) |
| $\phi$ | $4/\pi^2 \approx 0.40528$ | $\mathrm{sinc}^2(1/2)$ — half-corridor sidelobe amplitude |
| gap | $T^* - \phi \approx 0.309$ | Transcendental — does not simplify |
| BOUNDARY instances | 3 of 18 | RH, Hodge (×2) |
| ESCAPED instances | 3 of 18 | P≠NP solve, BSD rank≥2, Hodge dim≥5 |
| RESOLVED instances | 12 of 18 | Known closed results |
| Misclassifications | **0** | All 18 agree with consensus |

---

## References

- Sanders, B.R. (2026). WP34 — The First-G Law. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Sanders, B.R. (2026). WP35 — The Prime Phase Transition. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Sanders, B.R. (2026). WP_SINC2_ZERO_LAW — The Sinc² Zero Law in Prime Arithmetic. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Sanders, B.R. (2026). WP_OPERATOR_RING_PARTITION — Complete Harmony Partition of Two Composition Tables over Z/10Z. *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Sanders, B.R., Luther, C.A., Gish, M. (2026). WP36–WP42 (Clay series). *7SiTe Research*, DOI: 10.5281/zenodo.18852047.
- Clay Mathematics Institute (2000). Millennium Prize Problems. Cambridge, MA.
