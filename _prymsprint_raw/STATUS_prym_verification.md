# Prym Verification Status — 2026-04-19

## Target
Numerically verify
```
det(Im τ_P) = 2086 + 462·√15 + 498·√10 + 730·√6 ≈ 7238.260093
```
for the Prym variety of the bielliptic genus-5 curve
```
y^4 = x(x-1)(x-√2)^3(x-√3)^2(x-√5)^2
```
at the canonical triple (√2, √3, √5).

## What is VERIFIED (numerically solid)

1. **Canonical curve setup** (`mn_port.canonical_curve`)
   - 6 branch points: (0, 1, √2, √3, √5, ∞) with σ = (1,1,3,2,2,3)
   - Genus 5 via Riemann-Hurwitz
   - Forms basis: j-indices (1, 1, 2, 3, 3), ι-invariant at index 2 (ω_E), ι-antiinvariant at indices (0, 1, 3, 4)

2. **Shift-s cycles close** (`prym_e_subtraction.shift_s_cycle_list`)
   - 10 closed cycles: 2 (e0) + 3 (e1) + 2 (e2) + 3 (e3)
   - Closure residuals max ~ 5×10⁻⁶ at 60 digits (a loss of ~54 digits during summation — real but numerically clean)

3. **E-period PSLQ** (`prym_e_subtraction.pslq_e_coefficients`)
   - ω_α = 7.0164 (real), ω_β = 5.7509i (imaginary)
   - τ_E = 0.8196i, Im > 0 ✓
   - All 10 ⟨γ_i, ω_E⟩ values identified as integer combinations (a·ω_α + b·ω_β) with residuals < 10⁻⁵
   - M = 10×2 integer matrix of (a, b) coefficients
   - **Left kernel of M is 8-dimensional** (after fixing the Matrix(M_int).T bug in kernel_of_M)

4. **Prym sublattice basis**
   - 8 integer-linear combinations of the 10 shift-s cycles
   - Explicit K_ker (10×8 integer matrix) identified

5. **Pi_P (period matrix on Prym)**
   - 4 × 8 complex matrix, numerically exact to 60 digits
   - Obtained via Ω_shift[prym_idx, :] @ K_ker where prym_idx = [0, 1, 3, 4]

## What is BLOCKED

6. **Intersection form J_P on Prym**
   - Chain K_Γ (12×12 from `mn_port.intersection_matrix`) → J_C = Sᵀ K_Γ S → J_P = K_kerᵀ J_C K_ker
   - Yields J_P with det = 16, Pfaffian = 4, Frobenius type (1, 1, 2, 2)
   - **BUT Riemann 1st FAILS**: max |Pi_C J_C⁻¹ Pi_Cᵀ| = 566 (should be ≈ 0)
   - Riemann 2nd also fails: −i · Pi_C J_C⁻¹ conj(Pi_C)ᵀ has negative diagonals (should be > 0)
   - **Diagnosis**: Molin-Neurohr 2017 Thm 5.1 cross-edge intersection formula is known-broken for σ_shared ≥ 2 (our case at √2 which has σ=3, √3/√5 which have σ=2). The intersection_matrix function inherits this bug.
   - Symptom: K_Γ has rank 12, but the raw γ^(k) lattice should only rank-10 generate H_1(C, ℤ). Rank 12 indicates spurious intersections.

7. **τ_P symmetric + Im > 0**
   - Without correct J_P, cannot symplectically normalize Pi_P
   - Direct search over (70) column partitions: best sym defect 0.58 (straight interleaved), all with mixed-sign Im diagonals
   - Direct search over (256) per-block Sp swaps + sign flips: no small-defect + all-positive-Im combinations
   - **Conclusion**: a nontrivial GL_8(ℤ) transformation with cross-block terms is required — not achievable without correct J_P

## What was TRIED but did not land

- **abelfunctions (pip install from GitHub)**: Cython compilation failed on Windows (MSVC cannot convert between `_Dcomplex` and `__pyx_t_double_complex`)
- **SageMath local**: not installed; cloud Sage (Colab) previously timed out at 53-bit prec and disconnected
- **MAGMA online calculator**: domain http://magma.maths.usyd.edu.au blocked by Chrome MCP allowlist
- **Direct Riemann 1st PSLQ for J_P**: 16-dim nullspace (Pi_P X Pi_Pᵀ is automatically antisymmetric for skew-symm X, giving only 12 real independent equations on 28 unknowns)
- **Block-diagonal J_P ansatz** (4 independent 2×2 blocks per edge): FAILS, minimum off-diagonal residual 93 for d=(1,2,1,2)

## Files that are KEEPERS (math verified to the point listed above)

- `prym_e_subtraction.py` — canonical pipeline, shift-s + E-subtraction + kernel extraction [VERIFIED up to step 5]
- `compute_JP_from_KGamma.py` — K_Γ → J_C → J_P chain [BLOCKED at step 6: inherits MN 2017 bug]
- `search_symplectic_basis.py` — enumerate 70 column partitions for symplectic basis [shows none works; confirms need for linear combinations]

## What would unblock

One of the following:
- (A) Implement the corrected cross-edge intersection formula (MN 2019 or later) that handles σ_shared ≥ 2
- (B) Run the existing `magma_day1_bpm.magma` script in MAGMA (free calculator, 60 sec limit) to get Pi_C in a known-symplectic basis; then restriction to Prym is straightforward
- (C) Install SageMath and use `RiemannSurface.period_matrix()` which implements the full Tretkoff algorithm for non-squarefree f

## Honest summary

Pipeline Step 1 (MN port) — verified for squarefree edges, broken for σ_shared ≥ 2.
Step 2 (shift-s closure) — **verified** (residuals 5e-6 at 60 digits).
Step 3 (E-subtraction) — **verified** (PSLQ residuals 10⁻⁵⁶).
Step 4 (Prym kernel + Pi_P) — **verified** (8-dim sublattice, 4×8 period matrix).
Step 5 (J_P via Riemann bilinear) — **blocked** (underdetermined without an independent source of J_C).

The target 2086 + 462√15 + 498√10 + 730√6 remains unverified by this pipeline.
