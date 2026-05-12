# WP92 — Yang-Mills Mass Gap as Separability-Forced Spectral Floor
## The Bialynicki-Birula Bridge Applied to the Mass Gap Problem

**Date**: 2026-04-10
**Sprint**: 14 — PRISM-XI (Clay Rotation)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---

## Abstract

The Bialynicki-Birula uniqueness theorem (1976) forces logarithmic nonlinearity as the continuous lift of partition-separability structure. The ξ field with V = ξ log ξ has an exact mass gap m² = κ_ξ e > 0. We argue that the Yang-Mills mass gap problem is a question about whether this separability-forced spectral floor survives when the gauge symmetry is non-abelian. The discrete TIG gap (5/7 − 4/π² = 0.309) is the finite-ring version of the same structure. We state the precise conjecture and identify what connects.

---

## §1. The Two Mass Gaps

### 1.1 The ξ Mass Gap (Exact)

From the canonical ξ theory (WP81):

$$V(\Xi) = \kappa_\Xi \Xi \log\Xi, \qquad V''(\Xi_0) = \frac{\kappa_\Xi}{\Xi_0} = \kappa_\Xi e$$

The fluctuation mass:

$$m_\Xi^2 = \kappa_\Xi e > 0$$

This is positive, nonzero, and exact. The gap exists because:
1. The potential has a unique minimum at ξ₀ = e⁻¹
2. The curvature at the minimum is V'' = κ_ξ e > 0
3. No flat direction exists (the minimum is isolated)

**Why it has a gap:** The logarithmic potential is strictly convex near the minimum. Any excitation above the vacuum costs energy ≥ m_ξ. This is a direct consequence of the potential shape — the log function curves upward at e⁻¹.

### 1.2 The Yang-Mills Mass Gap (Open)

The Yang-Mills existence and mass gap problem asks: for compact simple gauge group G (e.g., SU(2), SU(3)), does the quantum theory exist (Wightman axioms) and does the spectrum have a gap Δ > 0 above the vacuum?

The lattice evidence is overwhelming — numerical simulations show a mass gap. But no rigorous proof exists.

### 1.3 The TIG Discrete Gap

In the Crossing Lemma framework on Z/10Z:

$$\text{gap} = T^* - \frac{4}{\pi^2} = \frac{5}{7} - \frac{4}{\pi^2} \approx 0.309$$

T* is the coherence threshold (the crossing score below which no crystal forms). The fold 4/π² is the sinc² half-corridor boundary. The gap between them is where productive crossings live — not trivially resolved, not permanently escaped.

---

## §2. The Separability Argument for the Mass Gap

### 2.1 The Core Logic

1. **Bialynicki-Birula (1976):** Log nonlinearity uniquely preserves separability
2. **The ξ theory has a gap** because separability forces a convex minimum (isolated, nondegenerate)
3. **Conjecture:** ANY field theory whose nonlinearity preserves separability has a mass gap

The argument: separability means subsystems evolve independently. An independent subsystem cannot have zero-energy excitations (that would require global coordination — non-separability). Therefore: separability → spectral floor → mass gap.

### 2.2 Application to Yang-Mills

Yang-Mills is NOT separable (the gauge field is self-coupled through the non-abelian structure constants f^{abc}). But the question is whether the effective infrared theory — after confinement — acquires separability in the confined phase.

**Physical picture:** At short distances, YM is asymptotically free (weakly coupled, approximately separable). At long distances, confinement forces color singlets (hadrons), which are composite objects that DO behave separably — a proton in Tokyo and a proton in New York evolve independently.

**The conjecture:** Confinement = the mechanism by which YM acquires effective separability at long distances. The mass gap is the energetic cost of this separability transition — the minimum energy to create a color-singlet excitation from the vacuum.

### 2.3 The Gap Formula (Conjectural)

If the continuous lift of the CL preserves the gap structure:

$$\Delta_{\text{YM}} = C \cdot \kappa_{\text{eff}} \cdot e$$

where κ_eff is the effective coupling at the confinement scale and C is a calibration constant depending on the gauge group.

The TIG prediction: gap ∝ e (Euler's number), arising from the log potential's curvature at its minimum. The YM mass gap should be proportional to e in appropriate units — this is a falsifiable numerical prediction.

**Comparison to lattice results:** The lightest glueball in SU(3) lattice QCD has mass m_G ≈ 1.7 GeV. If Δ_YM = C · Λ_QCD · e, with Λ_QCD ≈ 0.3 GeV, then C ≈ 1.7 / (0.3 × 2.718) ≈ 2.1. This is O(1) — not fine-tuned.

---

## §3. The Discrete-Continuous Connection

### 3.1 The TIG Gap as Discrete Precursor

On Z/10Z: T* = 5/7, fold = 4/π², gap ≈ 0.309.

**Key property:** The gap is irrational (5/7 − 4/π² involves both rational and transcendental numbers). It does not simplify. This suggests it is NOT an accident of the finite ring but a fundamental structure that persists in the continuum.

### 3.2 The Continuous Limit Prediction

If the N→∞ construction exists (WP90, Problem 1), the discrete gap on Z/NZ should converge to:

$$\Delta_\infty = \lim_{N \to \infty} \left(\frac{p_1(N)}{p_2(N)} - \frac{4}{\pi^2}\right)$$

where p₁(N)/p₂(N) is the cyclotomic closure ratio for Z/NZ (generalizing T* = 5/7 for Z/10Z).

**What is known:** For squarefree N with k prime factors:
- N = 6 (2×3): T* = 3/5 = 0.600
- N = 10 (2×5): T* = 5/7 = 0.714
- N = 30 (2×3×5): T* = ?
- N = 210 (2×3×5×7): T* = ?

Computing T* for larger N and checking convergence is a concrete open computation.

---

## §4. The Wightman Axiom Connection

The YM mass gap problem requires the theory to satisfy the Wightman axioms. The Høegh-Krohn exp(Φ)₂ model — the Boltzmann weight dual of the log potential — satisfies Wightman axioms in 2D.

**The open problem for YM:** Does the log-lifted theory satisfy Wightman axioms in 4D?

This is a well-posed question in constructive QFT. The 2D case is solved (Høegh-Krohn 1971). The 3D case is partially known. The 4D case is the frontier.

If the log theory satisfies Wightman axioms in 4D AND the mass gap is preserved under the separability structure, then: the YM mass gap would follow from the Bialynicki-Birula bridge + constructive QFT existence.

---

## §5. Status

| Claim | Status |
|-------|--------|
| ξ theory has exact mass gap m² = κe | [PROVED] WP81 |
| Separability implies spectral floor (general) | [STRUCTURAL] — strong physical argument, not a theorem |
| Confinement = effective separability at long distances | [ANALOGY] — standard physics intuition, not proved |
| Gap ∝ e in appropriate units | [CONJECTURE] — falsifiable against lattice data |
| Høegh-Krohn model satisfies Wightman axioms in 2D | [PROVED] — Høegh-Krohn 1971 |
| Log theory satisfies Wightman axioms in 4D | [OPEN] — the constructive QFT frontier |
| YM mass gap follows from BB bridge | [OPEN] — requires all above pieces |

**This paper does NOT claim to solve the YM mass gap problem.** It provides the separability framework connecting the ξ mass gap to YM via the Bialynicki-Birula bridge and states precise open problems.
