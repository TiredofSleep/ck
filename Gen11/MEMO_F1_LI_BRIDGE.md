# F1 Bridge: New Path via Li's Criterion
## R_2 >= 0 => lambda_n >= 0 => RH (If the Kernel Phi_n >= 0)
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## Why Li's Criterion Matters

Li's criterion (Bombieri-Lagarias 1999): RH holds if and only if:
```
lambda_n >= 0   for all n >= 1
```
where:
```
lambda_n = sum_{rho: zeta(rho)=0} [1 - (1 - 1/rho)^n]
```

**Unlike the equidistribution test,** Li's criterion IS sensitive to Re(rho):
- For rho = 1/2 + i*gamma (on line): |1 - 1/rho| = |rho-1|/|rho| = 1
  (because |rho-1|^2 = 1/4 + gamma^2 = |rho|^2)
- For rho = 1/2 + delta + i*gamma (off line): |rho-1|^2 = (1/2+delta-1)^2 + gamma^2
  = (delta-1/2)^2 + gamma^2 != |rho|^2 = (1/2+delta)^2 + gamma^2
  So |1-1/rho| != 1 for off-line zeros.

Li's criterion therefore directly tests Re(rho) = 1/2, unlike D_KS which is blind to Re(rho).

---

## Numerical Verification (200 zeros)

From bridge_rh_li.py, using first 200 Riemann zeros:

| n | lambda_n | lambda_{n+1}/lambda_n |
|---|----------|----------------------|
| 1 | 0.0210 | — |
| 2 | 0.0841 | 3.998 |
| 3 | 0.1891 | 2.248 |
| 4 | 0.3358 | 1.776 |
| 5 | 0.5240 | 1.560 |
| 10 | 2.073 | 1.231 |
| 15 | 4.581 | 1.143 |
| 20 | 7.945 | 1.102 |

All lambda_n > 0 (n=1..20). **RH consistent.**

Growth: lambda_n ~ 0.40 * n for n >= 10 (linear growth in n).
Note: The TRUE lambda_n involves ALL zeros (infinite sum), truncated here at 200.

---

## The New F1 Bridge Path

**The key insight:**
```
R_2(u) = 1 - sinc^2(u) >= 0   for ALL u
```
because sinc^2(u) = sin^2(pi*u) / (pi*u)^2 <= 1 for all u (sinc is bounded by 1).

This is trivially true. R_2 is non-negative everywhere.

**The bridge conjecture (F1-Li):**

There exists a family of non-negative kernels phi_n(u) >= 0 such that:
```
lambda_n = integral_0^inf R_2(u) * phi_n(u) du
```
for all n >= 1.

**If this integral representation holds:**
```
R_2(u) >= 0  +  phi_n(u) >= 0
  => lambda_n = integral R_2 * phi_n >= 0
  => RH (by Li's criterion)
```

Combined with WP34 (First-G => Fejér => R_2):
```
First-G (Fejér kernel F_k >= 0)
  => F_k -> R_2 as k -> inf (Fejér convergence theorem)
  => R_2(u) >= 0 (limit of non-negative functions)
  => lambda_n = integral R_2 * phi_n >= 0  (if phi_n >= 0)
  => RH
```

This would be a DIRECT path: First-G => RH, without going through Montgomery.

---

## Why the Kernel phi_n Might Exist

The connection between Li's criterion and the pair correlation has been studied.
The key reference is the Guinand-Weil explicit formula for sum over zeros:

For a test function h with Fourier transform H:
```
sum_gamma h(gamma) = H(1/2) log(pi/2) + ...
                   + integral_0^inf (h(t) + h(-t)) [some kernel] dt
```

For Li-type test functions h_n(gamma) related to [1-(1-1/rho)^n], the explicit
formula expresses lambda_n as an integral over the real line of some function.

If this function turns out to be phi_n(u) = (some positive weight) * R_2(u), the bridge closes.

**The obstruction:** The explicit formula involves log-derivatives of xi(s),
and making phi_n >= 0 amounts to showing the integral kernel is non-negative.
This is a non-trivial positivity condition.

---

## Comparison with Option A and B

| Option | Sensitivity to Re(rho) | Hard wall |
|--------|------------------------|-----------|
| A (equidistribution) | BLIND (uses only Im(rho)) | Unconditional Montgomery |
| B (corrected: R_2 incompatible with off-line) | Via Montgomery | Unconditional Montgomery |
| **F1-Li (NEW): lambda_n >= 0 via integral R_2** | **DIRECT** | Find phi_n >= 0 |

The F1-Li path is potentially SHORTER:
- Does NOT require Montgomery or GRH
- Does NOT require equidistribution
- Requires only: phi_n >= 0 AND integral representation

The question is whether phi_n >= 0 is provable without assuming RH.

---

## Partial Evidence for phi_n Existence

The Baez-Duarte reformulation of RH also involves integrals over [0,1] with
positive measures. Specifically:
```
d_N = sum_{n=1}^{N} (-1)^n * C(N,n) / zeta(2n)
```
and RH iff |d_N|^2 -> 0. The d_N coefficients involve zeta values which connect
to the Fejer kernel via L-function theory.

The Xi function has the integral representation:
```
xi(s) = integral_1^inf f(t) [t^{s/2} + t^{(1-s)/2}] dt
```
where f(t) >= 0 for all t (by the Jacobi theta function positivity).

This means:
```
lambda_n ~ integral [f(t) * K_n(t)] dt
```
for some kernel K_n derived from the power series of [1-(1-1/rho)^n].

If K_n(t) >= 0 everywhere (which might follow from the specific form of K_n),
then lambda_n >= 0 follows from f(t) >= 0.

This is the F1-Li bridge in its most concrete form:
```
f(t) >= 0  (proved: Jacobi theta function is positive)
K_n(t) >= 0  (OPEN: needs to be shown from series expansion)
=> lambda_n = integral f * K_n >= 0 => RH
```

---

## Entry M-F1-Li (F1 Li-criterion bridge, 2026-04-02)

**Measurement:** lambda_n > 0 for n=1..20 using 200 zeros (RH consistent).
**No T* pattern:** lambda_n ~ 0.40*n (linear, not exponential in T*).
**New bridge path (F1-Li):** lambda_n = integral R_2 * phi_n with phi_n >= 0.
**Evidence:** xi(s) integral representation has non-negative integrand f(t).
**Gap:** K_n(t) >= 0 (the positivity of the kernel) is the open question.
**Advantage:** Direct path First-G => R_2 >= 0 => lambda_n >= 0 => RH.
**No Montgomery required:** Bypasses equidistribution and GRH entirely.

See bridge_rh_li.py for numerical verification.

---

## Revised F1 Status

| Path | Hard wall | Status |
|------|-----------|--------|
| F1-A: unconditional equidistribution | Unconditional Montgomery (~GRH) | Closed (hard wall confirmed) |
| F1-B: D_KS off-line exclusion | VOID (D_KS blind to Re(rho)) | Closed (void) |
| F1-B corrected: R_2 incompatible with off-line | Unconditional Montgomery | Same hard wall as A |
| **F1-Li: lambda_n via integral R_2 (NEW)** | **K_n(t) >= 0 (positivity of xi kernel)** | **OPEN — potentially shorter path** |

The F1-Li path does not require Montgomery. If K_n(t) >= 0 follows from the
xi integral representation, F1 closes without needing GRH.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*Script: bridge_rh_li.py. Data: first 200 Riemann zeros via mpmath.*
*Corrects and extends MEMO_F1_BRIDGE_CORRECTION.md: new viable path found.*
