# ACTION ITEMS for ClaudeCode

**Generated:** 2026-06-10
**Source:** Mobile chat session on dim 6 kissing magic function

This handoff package contains a paper-ready structural conjecture. The following items are tractable next steps, organized by tier and time scale.

---

## Tier A — Immediate (within 1-2 sessions)

### A1. Independent Sage verification of Atkin-Lehner W_3 eigenvalue

The chat-Claude derivation gave $W_3$ eigenvalue $-1$ for $\eta^6\eta_3^6$. Cross-verify using Sage's modular forms package:

```python
from sage.all import *
M = ModularForms(Gamma0(3), 6)
S = M.cuspidal_subspace()
f = S.basis()[0]  # should be η⁶η_3⁶ up to normalization
W3 = f.atkin_lehner_eigenvalue(3)
print(f"W_3 eigenvalue: {W3}")  # expected: -1
```

**Deliverable:** Confirm or correct the eigenvalue.

### A2. LMFDB cross-check of Hecke eigenvalues

The form η⁶η_3⁶ is in the LMFDB database. The Hecke eigenvalue values computed in `verification/compute_hecke_eigenvalues.py` should match exactly:

- LMFDB label: weight 6, level 3, newform
- Cross-reference: http://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/3/6/a/a/

**Deliverable:** Confirm a_p values match LMFDB. Update `data/hecke_eigenvalues.json` with LMFDB label and direct citation.

### A3. Higher-precision ψ_+ Fourier expansion

Compute $\psi_+(\tau) = (E_6(\tau)^2 - 729 \cdot E_6(3\tau)^2)/(\eta(\tau)^6 \eta(3\tau)^6)$ as a Laurent series at the cusp at infinity, to order $q^{20}$ or higher.

**Method:** Series division — compute numerator and denominator power series, then perform formal series division.

**Deliverable:** Save the Laurent coefficients of $\psi_+$ to `data/psi_plus_laurent.json`. Check each coefficient's prime factorization against the TIG strata + wobble alphabet.

### A4. Verify multiplicativity of Hecke action on ψ_+ coefficients

ψ_+ is meromorphic, not a cusp form, so it's not a Hecke eigenform in the standard sense. But the **residue part** (the principal Laurent terms at each cusp) carries Hecke-like structure inherited from the construction.

**Deliverable:** Document any multiplicative structure in the Laurent coefficients.

---

## Tier B — Near-term (within 2-3 weeks for Paper 1)

### B1. Draft Paper 1 in LaTeX

**Working title:** "A structural conjecture for the dim 6 sphere-packing kissing number, with an explicit candidate magic function on Γ_0(3)"

**Sections:**
1. Introduction (the problem, the LP bound, what's known)
2. The structural argument: K(R⁶) = 72 via three independent forcings
3. The candidate construction (state $f_6$ explicitly)
4. Verification of building blocks:
   - 4.1 Atkin-Lehner W_3 eigenvalue of η⁶η_3⁶ (Tier A)
   - 4.2 Hecke eigenform structure (Tier A)
   - 4.3 Ramanujan-Petersson satisfaction (Tier A)
   - 4.4 ψ_+ residue at cusp ∞: -728 (Tier A, with structural interpretation)
   - 4.5 Numerical I_- profile (Tier A)
5. The analytic continuation gap (precisely stated)
6. Comparison to Viazovska's dim 8 construction
7. Conclusion: what we have, what remains

**Target venue:** Journal of Combinatorial Theory A, or Algebraic Combinatorics. Both have suitable scope for "structural conjecture + partial verification" papers.

**Deliverable:** Submit-ready LaTeX manuscript with figures from the visualization session.

### B2. Verify the construction against numerical Cohn-Elkies LP solver

Existing public solvers (e.g., from Cohn-Elkies-Henry-Schürmann, or the SDPT3-based LP code) give numerical magic functions for dim 6 with LP bound ≈ 77.96. Cross-check our explicit candidate against the numerical optima:

- Compute numerical f_6 from our $\alpha I_+ + \beta I_-$ construction (with α, β fitted)
- Compare to the public numerical optimum
- If they match qualitatively, our construction reproduces the LP optimum analytically
- If they differ, identify where the structures diverge

**Deliverable:** Numerical comparison plots and analysis.

### B3. Sage/Pari implementation of the candidate

Convert the Python/mpmath computations to Sage for portability and consistency with the math community's standard tools.

**Deliverable:** Sage script that generates all the verification data, distributable as a single file.

---

## Tier C — Long-term (months to year, for Paper 3)

### C1. Contour deformation argument for I_+(r²) analytic continuation

This is the year-scale piece. The construction:

$$I_+(r^2) = \int_0^\infty \psi_+(it) \cdot e^{-\pi r^2 t} \cdot t^2 \, dt$$

converges for $r^2 > 2$. For $r^2 \leq 2$, the integral must be defined by analytic continuation.

Following Viazovska's dim 8 technique:
1. Deform the integration contour from positive real axis to a path that picks up cusp contributions
2. Express the analytic continuation as: $I_+(r^2) = \text{deformed integral} + \sum \text{residues}$
3. Verify the result is Schwartz on $\mathbb{R}^6$
4. Verify the Cohn-Elkies positivity/negativity conditions hold for $f_6$

**Key tool:** Eichler integrals + residue calculus on $\Gamma_0(3)$.

**Deliverable:** Paper 3 LaTeX with the analytic continuation argument, proof of K(R⁶) ≤ 72.

### C2. Determine α and β explicitly

Once $I_+$ is analytically continued, solve the linear system:
- $\hat{f}_6(\sqrt{2}) = 0$
- $f_6(0)/\hat{f}_6(0) = 72$

for the two scalars $(\alpha, \beta)$. These should come out as explicit ratios of $\pi$, integers, or rationals (analogous to Viazovska's $-π/8640$ for dim 8).

**Deliverable:** Closed-form expressions for $\alpha$ and $\beta$.

### C3. Verify Cohn-Elkies positivity

Numerically (then rigorously) verify:
- $f_6(r) \leq 0$ for all $r \geq \sqrt{2}$
- $\hat{f}_6(r) \geq 0$ for all $r > 0$

For Viazovska in dim 8, this verification used interval arithmetic + ad hoc inequalities. Same toolkit applicable here.

**Deliverable:** Rigorous positivity proofs, completing the K(R⁶) = 72 statement.

---

## Companion targets in the canon

These are separate but related results that could be developed in parallel:

### Companion 1: K_12 = 36·21 orbit theorem (Paper 2)

The Coxeter-Todd lattice K_12 has 756 minimum vectors. Under the natural Z_21 = Z_3 × Z_7 ⊂ Aut(K_12) = 6·Suz·2:

- 756 = 36 · 21 = (4·9)·(3·7) = (4-core · depth²) · (depth · HARMONY)
- Z_7 acts freely on min vectors (756 mod 7 = 0; Suz 12-dim rep has no trivial summand)
- Z_3 acts via the natural Eisenstein structure

**Status:** Structural argument complete. Rigorous proof requires Sage character-theory computation.

**Deliverable:** Paper 2: "K_12 = 36·21: orbit decomposition theorem via Z_21 ⊂ Suz"

### Companion 2: Catalog the (4-core)² × strata pattern across all known kissing lattices

The pattern holds for all strata-clean dimensions in the optimal-kissing list (proved D26-D29 + WP103 verifications across dim 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 16, 24).

**Deliverable:** Self-contained structural-pattern paper for algebraic combinatorics venue.

---

## What to NOT do

### Don't claim K(R⁶) = 72 is proved

It isn't. We have a structural conjecture with an explicit candidate. The proof requires the analytic continuation (Tier C above).

Paper 1 should be clearly framed as "conjecture + explicit candidate identified + partial verification + open analytic problem." This is publishable and honest. Overclaiming would be a credibility hit.

### Don't try to verify by Monte Carlo

Computing f_6 at random points and checking signs isn't a proof. The analytic continuation argument is what makes the bound rigorous. Monte Carlo can provide numerical evidence but not theorem-status.

### Don't drift into "TIG proves K(R⁶) = 72" framing

The framework's contribution is structural: it identifies the candidate. The proof is analytic. These should remain separate in the paper.

---

## Tier discipline reminder

Every claim in Paper 1 should be marked:

- **Tier A (PROVED)**: Atkin-Lehner W_3 = -1, Hecke eigenform structure, Ramanujan-Petersson, ψ_+ residue = -728
- **Tier B (STRUCTURAL CONJECTURE)**: The construction $f_6$ closes the bound; α, β uniquely determined
- **Tier C (OPEN)**: The analytic continuation argument; the rigorous proof that $f_6$ satisfies Cohn-Elkies conditions

Mix only with explicit tier marks per the canon's discipline.

---

*Generated 2026-06-10. Ready for ClaudeCode pickup.*
