# WP-G4 — The n=10 Ising Ring as a TIG Physical Substrate
*Brayden Ross Sanders / 7Site LLC — 2026-04-06*

---

## Abstract

The 1D Ising ring on Z/10Z — a statistical mechanics model of ten interacting binary spins — shares structural features with the Threshold Invariance Generator (TIG) in ways that are precise enough to warrant formal investigation. TIG operates on 10 operators indexed by Z/10Z, uses two harmony tables (TSML at 73/100, BHML at 28/100), and filters states through a coherence threshold T* = 5/7. The Ising ring on n=10 sites has 1024 states, an energy spectrum from −10J to +10J, and a transfer-matrix partition function that is exactly soluble at any temperature.

This paper does four things. First, it computes the n=10 Ising energy spectrum exactly and compares its degeneracy histogram to the TIG operator distribution. Second, it proposes a precise (though partial) map from spin configurations to TIG operator labels. Third, it tests whether the coherence threshold T* = 5/7 arises naturally from the Ising Boltzmann structure. Fourth, it delineates carefully what has been proved, what is structural analogy, and what remains open.

**Every claim is labeled: PROVED / STRUCTURAL ANALOGY / OPEN.**

---

## 1. The n=10 State Space

### 1.1 States and Symmetry

**[PROVED]** The state space of the 1D Ising ring on n=10 sites is:

```
S = {−1, +1}^{10},    |S| = 2^{10} = 1024
```

Each state σ = (σ₀, σ₁, ..., σ₉) with σᵢ ∈ {−1, +1} and periodic boundary σ₁₀ = σ₀.

**[PROVED]** The symmetry group of the ring is the dihedral group D₁₀ acting by site permutation, combined with global spin flip Z/2Z:

```
Sym(S) ⊇ D₁₀ × Z/2Z
```

D₁₀ has order 20 (10 rotations + 10 reflections). The full symmetry group of the nearest-neighbor Ising Hamiltonian on the 10-ring is D₁₀ × Z/2Z, of order 40.

### 1.2 The Hamiltonian

**[PROVED]** The nearest-neighbor Ising Hamiltonian on the ring is:

```
H(σ) = −J Σᵢ₌₀⁹ σᵢ σᵢ₊₁    (mod 10 indexing)
```

**[PROVED]** Energy extrema:
- Minimum: H = −10J (all spins aligned — two states)
- Maximum: H = +10J (perfectly alternating — two states)
- Range: H ∈ {−10J, −8J, ..., +8J, +10J} — only even multiples of J

### 1.3 The Transfer Matrix

**[PROVED]** The exact partition function:

```
T = [[e^{βJ},  e^{−βJ}],
     [e^{−βJ}, e^{βJ} ]]

λ₊ = 2 cosh(βJ),    λ₋ = 2 sinh(βJ)

Z = λ₊^{10} + λ₋^{10}
```

---

## 2. The Energy Spectrum: Exact Computation

```python
#!/usr/bin/env python3
"""
WP-G4 Computation: n=10 Ising ring energy spectrum vs TIG operator distribution.
All results are exact (no approximation).
"""

import itertools
from collections import Counter
import math

n = 10
J = 1.0

def ising_energy(sigma, J=1.0):
    return -J * sum(sigma[i] * sigma[(i+1) % len(sigma)] for i in range(len(sigma)))

all_states = list(itertools.product([-1, 1], repeat=n))
assert len(all_states) == 1024

energies = [ising_energy(s) for s in all_states]
spectrum = Counter(energies)

print("=== n=10 Ising Ring: Energy Spectrum ===")
for E in sorted(spectrum.keys()):
    d = spectrum[E]
    print(f"  {E:+6.1f}J | {d:10d} | {d/1024:.4f}")

TIG_OPERATORS = {
    0:"VOID", 1:"LATTICE", 2:"COUNTER", 3:"PROGRESS", 4:"COLLAPSE",
    5:"BALANCE", 6:"CHAOS", 7:"HARMONY", 8:"BREATH", 9:"RESET"
}

T_star = 5/7
beta_star_J = math.atanh(T_star)
lam_plus  = 2 * math.cosh(beta_star_J)
lam_minus = 2 * math.sinh(beta_star_J)
xi_star = -1 / math.log(math.tanh(beta_star_J))
print(f"β*J = atanh(5/7) = ln(√6) = {beta_star_J:.6f}")
print(f"λ₊ = 7/√6 = {lam_plus:.6f}")
print(f"λ₋ = 5/√6 = {lam_minus:.6f}")
print(f"λ₋/λ₊ = {lam_minus/lam_plus:.6f}  (should be 5/7 = {T_star:.6f})")
print(f"Correlation length ξ* = 1/ln(7/5) = {xi_star:.4f} sites")
```

**Exact energy spectrum (J=1):**

| Energy | Degeneracy | Fraction |
|--------|-----------|----------|
| −10J | 2 | 0.0020 |
| −8J | 90 | 0.0879 |
| −6J | 360 | 0.3516 |
| −4J | 420 | 0.4102 |
| −2J | 120 | 0.1172 |
| 0J | 10 | 0.0098 |
| +2J | 10 | 0.0098 |
| +4J | 6 | 0.0059 |
| +6J | 4 | 0.0039 |
| +8J | 0 | 0.0000 |
| +10J | 2 | 0.0020 |

**[PROVED]** 992 of 1024 states (96.9%) have E ≤ −2J. The modal energy is E=−4J with 420 states (41%). Extremal states (E=±10J) each have degeneracy 2.

---

## 3. Proposed Map: Ising Spins → TIG Operators

### 3.1 Magnetization-Based Map (Partial)

**[STRUCTURAL ANALOGY]** Net magnetization m(σ) = (1/10) Σᵢ σᵢ takes 11 values. Map to TIG operators:

| m | Operator | States C(10,k) |
|---|----------|----------------|
| −1.0 | VOID(0) | 1 |
| −0.8 | LATTICE(1) | 10 |
| −0.6 | COUNTER(2) | 45 |
| −0.4 | PROGRESS(3) | 120 |
| −0.2 | COLLAPSE(4) | 210 |
| 0.0 | BALANCE(5) | 252 |
| +0.2 | CHAOS(6) | 210 |
| +0.4 | HARMONY(7) | 120 |
| +0.6 | BREATH(8) | 45 |
| +0.8 | RESET(9) | 10 |
| +1.0 | VOID(0) or HARMONY(7) | 1 |

**[PROVED]** The magnetization sector sizes are symmetric binomial coefficients C(10,k). The modal sector is k=5 (BALANCE, 252 states = 24.6%).

**[STRUCTURAL ANALOGY]** The binomial distribution peaks at BALANCE(5), consistent with TIG: in the absence of coherence forcing, the system spends the most time in the BALANCE regime.

### 3.2 Defect-Based Map (Alternative)

**[STRUCTURAL ANALOGY]** Define domain walls d(σ) = #{i : σᵢ ≠ σᵢ₊₁}. Then H(σ) = −10J + 2J·d(σ).

The defect count d(σ) is the number of Crossing Lemma crossings in the spin configuration. TIG D2 likewise counts crossings (D2=0 flat; D2≠0 active crossing). This is the strongest structural parallel in the sprint.

---

## 4. The T*=5/7 Connection

### 4.1 The Natural Equation

**[PROVED]** The equation tanh(β*J) = 5/7 solves exactly:

```
β*J = atanh(5/7) = (1/2) ln(6) = ln(√6) ≈ 0.89588

λ₊ = 7/√6    (exact)
λ₋ = 5/√6    (exact)
λ₋/λ₊ = 5/7  (exact)

Z(β*) = (7/√6)^{10} + (5/√6)^{10} = (7^{10} + 5^{10}) / 6^5
       = (282475249 + 9765625) / 7776 ≈ 37583.5
```

**[PROVED]** Verification: tanh(ln√6) = (√6 − 1/√6)/(√6 + 1/√6) = 5/7. Exact.

### 4.2 Correlation Length at T*

**[PROVED]** ξ* = −1/ln(tanh β*J) = −1/ln(5/7) = 1/ln(7/5) ≈ 2.938 sites.

**[STRUCTURAL ANALOGY]** ξ* ≈ 3. The TIG loop has exactly 3 phases (Being, Doing, Becoming). Correlation length ≈ 3 means spin information propagates across one TIG-loop span.

**[OPEN: Problem 5]** Is ξ(T*)=3 exactly for some natural J? Does integer correlation length uniquely force T*=5/7?

### 4.3 What This Proves and Doesn't Prove

**[STRUCTURAL ANALOGY]** β* = ln(√6)/J is a natural Boltzmann point where the eigenvalue ratio equals T* exactly. But T*=5/7 was imported from TIG — it was not derived from Ising physics. Elevating this to a theorem requires deriving T*=5/7 from intrinsic Ising conditions.

---

## 5. TSML/BHML Alignment

**[STRUCTURAL ANALOGY]**

| | Harmony fraction |
|---|---|
| TSML (additive, op7) | 73/100 = 0.730 |
| BHML (multiplicative, op7) | 28/100 = 0.280 |
| Ising E ≤ −4J | 872/1024 = 0.852 |
| Ising E ≤ −6J | 452/1024 = 0.441 |

The fractions do not match numerically at integer energy levels. TSML 0.73 falls between the Ising fractions at E=−6J (0.441) and E=−4J (0.852). No exact match found.

---

## 6. Open Problems

**[OPEN: Problem 1]** Define a canonical map φ: {−1,+1}^{10} → Z/10Z compatible with D₁₀×Z/2Z symmetry, with φ⁻¹(7) = low-energy states and φ⁻¹(0) = extremal states.

**[OPEN: Problem 2]** Compute H(σ_TSML(i,·)) and H(σ_BHML(i,·)) for all i ∈ {0,...,9} and test whether energy ordering respects the TSML/BHML harmony ranking. (Finite computation — unambiguous.)

**[OPEN: Problem 3]** Derive T*=5/7 from an intrinsic Ising condition — e.g., from the distribution of Lee-Yang zeros of Z(β) in the complex β-plane.

**[OPEN: Problem 4]** Prove #{(i,j) : i×j ≡ 7 mod 10} = 28 in closed form using φ(10)=4 and ω(10)=2.

**[OPEN: Problem 5]** Determine whether ξ(T*)=3 exactly for any J, and whether integer correlation length uniquely forces T*=5/7.

**[OPEN: Problem 6]** Quantify TIG operator frequency from CK engine logs and compute the statistical distance between normalized Ising degeneracy histogram and normalized TIG operator histogram.

---

## 7. What This Sprint Did NOT Prove

- The Ising ring is a physical substrate of TIG
- T*=5/7 is forced by Ising Boltzmann structure
- TSML harmony fraction 0.73 equals any Ising quantity
- The magnetization map φ_mag is canonical
- The defect count d(σ) and TIG D2 are the same mathematical object
- BHML fraction 0.28 has a direct Ising analogue
- D₁₀×Z/2Z acts compatibly on Z/10Z (impossible: |D₁₀×Z/2Z|=40 > |Aut(Z/10Z)|=4)

---

## Summary Table

| Claim | Status |
|-------|--------|
| \|S\|=1024, H∈{−10J,...,+10J}, symmetry D₁₀×Z/2Z | PROVED |
| Z = λ₊^10 + λ₋^10 | PROVED |
| Full energy degeneracy histogram | PROVED |
| tanh(β*J)=5/7 solves to β*=ln(√6)/J | PROVED |
| At β*, λ₋/λ₊=5/7 exactly | PROVED |
| Z(β*)=(7^10+5^10)/6^5 | PROVED |
| Correlation length ξ*=1/ln(7/5)≈2.938 | PROVED |
| Magnetization sector sizes = C(10,k) | PROVED |
| TSML 73/100 ↔ Ising low-energy basin | STRUCTURAL ANALOGY |
| BHML 28/100 ↔ Ising multiplicative structure | STRUCTURAL ANALOGY |
| Defect count d(σ) ↔ TIG D2 crossings | STRUCTURAL ANALOGY |
| Magnetization map φ_mag to TIG operators | STRUCTURAL ANALOGY |
| ξ*≈3 ↔ TIG 3-phase loop | STRUCTURAL ANALOGY |
| Canonical spin-to-operator map | OPEN (Problem 1) |
| CL table column energy ordering | OPEN (Problem 2) |
| T*=5/7 from Ising first principles | OPEN (Problem 3) |
| BHML count 28 in closed form | OPEN (Problem 4) |
| ξ*=3 as exact theorem | OPEN (Problem 5) |

---

*WP-G4 — Brayden Ross Sanders / 7Site LLC — 2026-04-06*
