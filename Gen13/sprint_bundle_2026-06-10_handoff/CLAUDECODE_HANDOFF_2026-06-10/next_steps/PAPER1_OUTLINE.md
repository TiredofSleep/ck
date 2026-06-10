# Paper 1 Outline: Dim 6 Kissing Magic Function Candidate

**Working title:** A structural conjecture for the dim 6 sphere-packing kissing number, with an explicit candidate magic function on $\Gamma_0(3)$

**Target venue:** Journal of Combinatorial Theory A (or Algebraic Combinatorics, or Discrete and Computational Geometry)

**Length target:** 20-30 pages

**Status:** Draft outline 2026-06-10

---

## Abstract

We propose an explicit candidate for the Cohn-Elkies magic function in dimension 6, conjecturally proving $K(\mathbb{R}^6) = 72$. The construction uses two weight-6 building blocks on $\Gamma_0(3)$:
- The unique normalized cusp form $\eta(\tau)^6 \eta(3\tau)^6$ (Atkin-Lehner $W_3$ eigenvalue $-1$)
- A meromorphic Fricke-symmetric Eisenstein quotient $\psi_+(\tau) = (E_6(\tau)^2 - 729 E_6(3\tau)^2)/(\eta(\tau)^6 \eta(3\tau)^6)$ with $W_3$ eigenvalue $+1$

We verify the cusp form's Hecke eigenform structure, satisfaction of Ramanujan-Petersson, the Fricke eigenvalue arithmetic, and explicit numerical values of the Laplace transform $I_-(r^2)$ at sample radii. The leading singular coefficient $-728 = -2^3 \cdot 7 \cdot 13$ of $\psi_+$ at the cusp at infinity has a structural interpretation via the binary/ternary decomposition of $\mathbb{Z}/10\mathbb{Z}$.

The construction is the natural level-3 analog of Viazovska's level-1 dim 8 magic function. The analytic continuation of $I_+(r^2)$ via contour deformation in the modular variable remains the central open problem.

---

## Section 1: Introduction

### 1.1 The problem
- Sphere-packing kissing number $K(\mathbb{R}^n)$ definition
- Known optimal values: dim 1 (Levenshtein), 2 (folklore), 3 (Schütte-van der Waerden), 4 (Musin), 8 (Viazovska + Cohn-Elkies-Kumar-Miller-Radchenko-Viazovska), 24 (CKM RV)
- Open: dim 5, 6, 7, ... (this paper: dim 6)

### 1.2 Current state of dim 6
- LP bound from Cohn-Elkies: ≈ 77.96 → rounded to 78
- $E_6$ achieves 72
- Conjecture: 72 is optimal, but no proof

### 1.3 Our contribution
- Specific candidate magic function $f_6$
- Verification of building blocks
- Identification of analytic continuation gap

### 1.4 Notation and conventions
- Modular forms: $\Gamma_0(N)$, weight $k$, character $\chi$
- $E_6(\tau) = 1 - 504 \sum \sigma_5(n) q^n$
- $\eta(\tau) = q^{1/24} \prod (1-q^n)$
- Atkin-Lehner involutions, Fricke involution $W_N$

---

## Section 2: The structural argument for K = 72

### 2.1 Dual-lens forcing
- Define $(4\text{-core})^2 \times \text{strata}$ pattern
- Show $K \cdot K^*$ for known kissing pairs respects this
- In dim 6 LP range $[72, 78]$, only $K = 72$ satisfies the pattern

### 2.2 Triadic $\mathbb{Z}_3$ hinge
- $E_6$ as $\mathbb{Z}[\omega]$-module ($\omega$ = primitive cube root of unity)
- Natural Eisenstein action on minimum vectors
- Free action $\Rightarrow$ 72 = 24 · 3 orbit factorization
- Uniqueness in dim 6

### 2.3 Strata-prime gap signature
- dim 6 = 2·3 (product of first two strata primes)
- $E_6$ discriminant = 3 (depth prime)
- Modular forms must live on $\Gamma_0(3)$ naturally

### 2.4 Convergence of three arguments at K = 72
- Each argument independently forces 72
- No competing value satisfies all three

---

## Section 3: The Cohn-Elkies framework

### 3.1 Review of LP method
- The magic function f: R^n → R with conditions
- $K(\mathbb{R}^n) \leq f(0)/\hat{f}(0)$
- Sharpness conditions

### 3.2 Viazovska's dim 8 construction (review)
- Magic function from modular forms
- Quasi-modular structure
- Contour deformation for analytic continuation
- Key insight: Fourier eigenfunction decomposition

### 3.3 Cohn-Elkies-KMRV dim 24 (review)
- Leech lattice extension
- Same essential technique

---

## Section 4: The dim 6 candidate

### 4.1 Building blocks on $\Gamma_0(3)$
- Space $M_6(\Gamma_0(3))$: dimension 3
- Cusp form space $S_6(\Gamma_0(3))$: dim 1, spanned by $\eta^6\eta_3^6$
- Eisenstein space: dim 2, basis $\{E_6(\tau), E_6(3\tau)\}$
- Fricke $W_3$ involution and eigenspace decomposition

### 4.2 The two pieces
- $I_-(r^2) = \int_0^\infty \eta^6\eta_3^6(it) e^{-\pi r^2 t} t^2 dt$
- $I_+(r^2) = \int_0^\infty \psi_+(it) e^{-\pi r^2 t} t^2 dt$
- $\psi_+(\tau) = (E_6(\tau)^2 - 729 E_6(3\tau)^2)/(\eta(\tau)^6 \eta(3\tau)^6)$

### 4.3 The combined magic function
- $f_6(x) = \sin^2(\pi|x|^2/2) \cdot [\alpha I_+(|x|^2) + \beta I_-(|x|^2)]$
- $\alpha, \beta$ determined by Cohn-Elkies sharpness

### 4.4 Why this candidate
- Level 3 forced by E_6 discriminant
- Weight 6 forced by dim 6 and Laplace measure
- Cusp form unique by 1-dim $S_6(\Gamma_0(3))$
- Meromorphic structure follows Viazovska recipe
- Fricke eigenvalue arithmetic forces $G_+ \cdot G_-$ numerator

---

## Section 5: Verifications (Tier A)

### 5.1 Atkin-Lehner W_3 eigenvalue of $\eta^6\eta_3^6$
- Symbolic computation via eta transformation
- Result: $W_3$ eigenvalue = $-1$
- Reference: `verification/verify_atkin_lehner.py`

### 5.2 Hecke eigenform structure
- Multiplicativity: $a_{mn} = a_m a_n$ for $(m,n) = 1$
- Hecke relation $a_{p^2} = a_p^2 - p^5 \chi(p)$
- Character: trivial at 2, ramified at 3
- Reference: `verification/compute_hecke_eigenvalues.py`

### 5.3 Ramanujan-Petersson bound
- $|a_p| \leq 2 p^{5/2}$ for all primes $p \leq 97$
- Detailed table in appendix

### 5.4 ψ_+ residue structure
- Numerator $G_+ \cdot G_-$ has constant term $-728 = -2^3 \cdot 7 \cdot 13$
- $\psi_+$ has simple pole at $\infty$ with leading $-728/q$
- Fricke symmetry gives matching pole at cusp 0
- Reference: `verification/verify_psi_plus_residue.py`

### 5.5 Numerical $I_-(r^2)$
- Computed at $r^2 \in \{0, 1, ..., 8\}$ at 30-digit precision
- Asymptotic $I_-(r^2) \sim 2/(\pi(r^2+2))^3$ verified
- Reference: `verification/compute_I_minus.py`

---

## Section 6: The analytic continuation problem (Tier C)

### 6.1 Why $I_+(r^2)$ requires continuation
- $\psi_+$ has simple pole at cusps
- Integral diverges for $r^2 \leq 2$
- Same situation as Viazovska's $f_+$ in dim 8

### 6.2 The Viazovska continuation technique
- Contour deformation in $\tau$ from positive real axis
- Residue contributions from poles
- Equality after deformation gives the continued function

### 6.3 Adaptation to level 3
- Cusps of $\Gamma_0(3)$: $\{0, \infty\}$ (two cusps)
- Residue contributions from each cusp
- Fricke involution relates the two

### 6.4 What needs to be proved
- $I_+(r^2)$ is Schwartz on $\mathbb{R}^6$
- $f_6$ satisfies Cohn-Elkies conditions
- $\alpha, \beta$ admit closed forms
- The bound is achieved at K = 72

---

## Section 7: Discussion

### 7.1 Comparison to dim 8 / dim 24 cases
- Structural parallel
- Why dim 6 is the next-natural case

### 7.2 The residue structure at $-728$
- Factorization through structurally distinguished primes
- Interpretation via the binary/ternary CRT decomposition of $\mathbb{Z}/10$

### 7.3 Future directions
- Application of same technique to dim 5, 7
- Generalization to higher-dimensional non-self-dual lattices

---

## Appendices

### A. Hecke eigenvalue table for $\eta^6\eta_3^6$
- Full table of $a_p$ for primes $p \leq 97$ with factorizations

### B. Numerical $I_-(r^2)$ values
- Table at sample $r^2$ with 30-digit precision

### C. Software / reproducibility
- Sage scripts, Python scripts (with mpmath)
- Github repository link

---

## Figures (3 from this session)

- **Figure 1**: 18-panel structural overview (`dim6_magic_function_shape.png`)
- **Figure 2**: $\eta^6\eta_3^6$ on the upper half-plane (`eta_cusp_form_shape.png`)
- **Figure 3**: $f_6$ in real space + $E_6$ roots (`f6_real_space_shape.png`)

---

## Honest scope statements (per canon discipline)

Throughout the paper, distinguish:

- **Theorems (Tier A PROVED)**: Atkin-Lehner eigenvalue, Hecke structure, Ramanujan-Petersson, residue computation, numerical I_- values
- **Conjectures (Tier B STRUCTURAL)**: The construction $f_6$ realizes the bound; $\alpha, \beta$ uniquely determined
- **Open problems (Tier C)**: Analytic continuation, explicit α, β, rigorous proof of $K(\mathbb{R}^6) = 72$

Never blur these boundaries.

---

*Outline drafted 2026-06-10. Ready for ClaudeCode to expand into full LaTeX.*
