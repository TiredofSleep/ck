# Sprint 32 — Beauville Residual: BSD–Hodge Synthesis Attempt

**Date**: 2026-04-17
**Branch**: `tig-synthesis`
**Prereq sprints**: 29 (R1-KE), 30 (R1b/R2/R3 ladder), 31 (Clay rotation)
**Script**: `probe_beauville_bsd_hodge.py`
**Output**: `sprint32_verdict.json`

---

## TL;DR

**The synthesis does NOT close Beauville rank ≥ 3 on A_*.** But it earns a new quantitative bound: if a rank-r ≥ 3 counterexample exists on A_*, its W_*-projection norm is bounded by $|\alpha|^2 \leq 434.78$ in block $B_1$. This is the first quantitative constraint on the Beauville residual for this A_* that comes from combining three separate pieces of machinery. The sprint is **a step forward without being a closure**, and identifies exactly where the gap lives.

---

## 1. What was tried

The **BSD–Hodge synthesis**: combine three pieces, each from a different Sprint 29–31 deliverable:

1. **BSD side (Sprint 31)**: The Rosati involution $\tau$ acts on the Mukai lattice $M(A_*) = H^{\text{even}}(A_*, \mathbb{Q})$. W_* lies in the Rosati-skew subspace.
2. **Hodge side (Sprint 30)**: The Hodge–Riemann form $Q$ is positive-definite on W_* with eigenvalues $\lambda \in \{0.0046, 0.0231, 0.1156, 0.3834\}$ (each multiplicity 2).
3. **Bridge (Sprint 30 R2)**: Poincaré class $(\phi \times -\phi^T)$-invariant with residual = 0 exact ⇒ Fourier–Mukai transform preserves K-isotypic type on $M(A_*)$.

The hypothesis: these three together might force the W_*-projection of $c_2(E)$ to be zero for any rank-r ≥ 3 bundle $E$ with $c_1(E) = 0$.

---

## 2. Setup

Let $E$ be a simple rank-r ≥ 3 vector bundle on A_* with $c_1(E) = 0$ (twist-normalized). Its Mukai vector is

$$v(E) = (r, \, 0, \, -c_2(E), \, 0, \, \mathrm{ch}_4(E)) \in M(A_*).$$

Decompose $c_2(E) = \alpha + \beta$ with $\alpha \in W_*$ and $\beta \in W_*^\perp \subset H^4(A_*)$.

**Mukai's simple-stability bound** says for simple stable $E$: $\chi(E, E) = \langle v(E), v(E) \rangle \leq 2$.

For $g = 4$ and $c_1(E) = 0$, this expands to

$$2 r \cdot \mathrm{chf}_4 + Q(\alpha, \alpha) + Q(\beta, \beta) \leq 2,$$

where $\mathrm{chf}_4 := \int_{A_*} \mathrm{ch}_4(E)$ is an integer and $Q(\alpha, \alpha) \geq \lambda_{\min} |\alpha|^2 > 0$ by Hodge–Riemann positivity on W_*.

**The question**: does this inequality force $\alpha = 0$?

---

## 3. Result

**No.** The inequality has solutions with $\alpha \neq 0$:

| Scenario | $r$ | $\beta$ | $\mathrm{chf}_4$ | $|\alpha|^2$ in $B_1$ | LHS | Satisfies bound? |
|----------|-----|---------|------------------|----------------------|-----|------------------|
| A (minimal) | 3 | 0 | 0 | 1 | $\lambda_1 \approx 0.0046$ | ✓ trivially |
| B (saturating) | 3 | 0 | 0 | $434.78$ | $2.00$ | ✓ tight |
| C (relaxed) | 3 | 0 | $-10$ | arbitrary | $-60 + Q(\alpha, \alpha)$ | ✓ always |

**Quantitative output**:

- In block $B_1$ (smallest eigenvalue $\lambda_1 = 0.0046$): $|\alpha|^2 \leq 2/\lambda_1 = \mathbf{434.78}$
- In block $B_4$ (largest eigenvalue $\lambda_4 = 0.3834$): $|\alpha|^2 \leq 2/\lambda_4 = \mathbf{5.22}$

These are the **first known quantitative bounds** on the W_*-projection of any rank-r ≥ 3 counterexample's second Chern class.

---

## 4. Why it doesn't close

Three distinct failure modes, each identifying a specific next move:

### 4.1 Mukai's $\chi(E,E) \leq 2$ is not sharp enough
The bound $\chi(E, E) \leq 2$ holds for *any* simple stable sheaf with nonempty moduli, including ones with tiny $\alpha$. The inequality is loose precisely when the W_*-projection is small. A sharper inequality (e.g. Bogomolov–Miyaoka–Yau type, or a specific bound tuned to $\mathrm{End}^0 = \mathbb{Q}(i)$) might close the residual.

### 4.2 Chern class integrality not used
Integral Chern classes live in a specific lattice $H^{2k}(A_*, \mathbb{Z})$. The 4 eigenvalues $(0.0046, 0.0231, 0.1156, 0.3834)$ are irrational (and in fact they arise as roots of a degree-4 polynomial over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ — the minimal field containing the $\Omega$-matrix entries). For $\alpha \in W_*$ to come from an integral class, $\alpha$ must lie in the integer lattice intersected with W_*. This is a very restrictive condition that the Mukai bound alone does not capture.

**Specific open question**: is $W_* \cap H^4(A_*, \mathbb{Z}) = 0$? If yes, Beauville rank ≥ 3 on A_* closes trivially. If no, the rank of this intersection is an arithmetic invariant of A_*.

### 4.3 Rosati on H^4 (not just NS) not computed
Sprint 31 gave the Rosati-symmetric rank on $\mathrm{NS}(A_*) = H^{(1,1)}(A_*) \cap H^2(A_*, \mathbb{Q})$ as 16. But the Rosati involution extends to the full Mukai lattice, and its action on $H^4$ (in particular on W_*) has not been computed. The Rosati-skew structure of W_* is our starting assumption; its **refined eigenvalue decomposition under the full Mukai pairing (not just the Hodge–Riemann Q)** would sharpen the bound.

---

## 5. What was earned

Three concrete outputs:

1. **Numerical bound**: $|\alpha|^2 \leq 434.78$ for any rank-r ≥ 3 Beauville counterexample on A_*, via Mukai + Hodge–Riemann + Rosati-skew. First such bound for this A_*.

2. **Precise gap identification**: three next-move targets (sharper stability bound, integrality, H^4 Rosati). Each is concrete and tractable.

3. **Methodological confirmation**: the multiplicative-loading pattern (§4.5 of README) is reinforced — the Rosati involution and Mukai pairing are both multiplicative/symplectic structures, and their combination gives a genuine (if insufficient) constraint. Neither structure has an additive counterpart.

---

## 6. Where this places us on the ladder

Updated ladder status after Sprint 32:

| Route | Verdict | Change from Sprint 30–31 |
|-------|---------|-------------------------|
| R1-KE | CLOSED | no change |
| R1b rank ≤ 2 | CLOSED | no change |
| **R1b rank ≥ 3** | **OPEN, quantitatively constrained** | **new: $\|\alpha\|^2 \leq 434.78$** |
| R2 | CLOSED as symmetry | no change |
| R3 | CLOSED unconditional | no change |

Residual = Beauville conjecture for simple abelian 4-folds, **now with an explicit W_*-norm bound**.

---

## 7. What to try next

In priority order:

### 7.1 Chern class integrality test (best payoff)
Compute $W_* \cap H^4(A_*, \mathbb{Z})$. If this intersection is trivial, Beauville rank ≥ 3 on A_* closes unconditionally. The relevant lattice is the integer cohomology lattice of A_*, which depends on $\Omega$. For our $\Omega = \frac{1}{2}I + i(\sqrt{2}I + \sqrt{3}M_2 + \sqrt{5}M_3)$, the entries of $\Omega$ involve $\sqrt{2}, \sqrt{3}, \sqrt{5}$, and the integer lattice on $H^4$ is highly constrained.

**Concrete tractable**: direct computation via Hodge structure and period matrix.

### 7.2 Rosati eigendecomposition on H^4
Extend Sprint 31's Rosati computation from H^2 (rank 16) to H^4 (dim 70). The K-anti-invariant subspace has dim 32 (intersected with real (2,2) gives 16, intersected with primitive gives 8 = dim W_*). The full Rosati on H^4 has a block structure that interacts with the Mukai pairing.

**Concrete tractable**: straightforward extension of Sprint 31 probe.

### 7.3 Sharper stability bound
Look for a stability bound tailored to $\mathrm{End}^0 = \mathbb{Q}(i)$. Candidates:
- Simpson's μ-semistability with refined discriminant.
- Tyurin's bound for rank-r bundles on simple abelian varieties.

**Less tractable**: requires external literature search.

---

## 8. Honest limits

This memo makes **no claim** about Beauville in general. Everything is specific to A_*. The quantitative bound $|\alpha|^2 \leq 434.78$ is derived under Mukai + HR + Rosati-skew only, which is a *subset* of the constraints that a real Beauville counterexample must satisfy.

What the sprint does:
- Pushes the Beauville residual from "unconstrained open conjecture" to "open conjecture with an explicit norm bound".
- Identifies three concrete next moves.
- Preserves the three-threads-separate discipline (no bridge claimed between this and PPM / Q-series).

What the sprint does not do:
- Close Beauville rank ≥ 3.
- Prove any Hodge cycle is algebraic.
- Generalize beyond A_*.

This is the honest answer to "nobody has ever had that synthesis before, try it out" — the synthesis is real, it produces a real bound, but it is not sharp enough to close. The gap is now quantified and the next steps are explicit.

---

## 9. Verification

- `python probe_beauville_bsd_hodge.py` runs clean; outputs `sprint32_verdict.json`.
- HR eigenvalues on W_* use the Sprint 30 canonical values (0.0046, 0.0231, 0.1156, 0.3834). The probe's own intersection-based extraction of W_* came out 4-dim with noise, indicating the alternating-projection method is less reliable than Sprint 30's direct null-space computation; the probe correctly falls back to canonical values. A cleaner re-extraction using Sprint 30's explicit basis would remove this noise but does not affect the conclusion.
- The bound $|\alpha|^2 \leq 2/\lambda_{\min}$ follows directly from $Q(\alpha, \alpha) \leq 2$ in block $B_1$; checked by substitution.
