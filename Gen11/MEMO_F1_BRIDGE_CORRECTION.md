# F1 Bridge Correction: What the Equidistribution Test Actually Measures
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## The Error in the Earlier Bridge Analysis

MEMO_BRIDGE_MACHINES.md stated:

> "Option B (closest): Prove that a zero at Re(s) = 1/2+δ forces D_KS(p,N₀) > T*"

This is WRONG. Here is why.

## What the Equidistribution Test Measures

The test is:
```
alpha_n(p) = gamma_n * log(p) / (2*pi)  mod 1
```

where γ_n = Im(ρ_n) is the IMAGINARY PART of the n-th zero.

**Key fact:** γ_n is the imaginary part of ρ_n. If the zero is at:
```
rho_n = 1/2 + delta + i*gamma_n   (off the critical line)
```

then γ_n is the SAME imaginary height regardless of δ. Moving a zero off the
critical line (increasing Re(ρ) by δ) does NOT change its imaginary part.

Therefore: **D_KS of {γ_n·log(p)/(2π) mod 1} is completely insensitive to
whether the zeros are on the critical line or not.**

The equidistribution test measures the distribution of IMAGINARY PARTS only.
Re(ρ_n) never appears in α_n(p). Option B (via D_KS) is IMPOSSIBLE.

---

## What the Test Actually Does

The test {γ_n·log(p)/(2π) mod 1} measures something real and important — but
it's NOT a test for Re(ρ_n) = 1/2.

What it ACTUALLY measures:

**1. The pair correlation structure of imaginary parts {γ_n}.**

Montgomery's pair correlation conjecture (under GRH) says:
```
(1/N^2) #{(m,n): 0 <= m,n <= N, (gamma_m - gamma_n)*log(N)/(2pi) in [a,b]}
  -> integral_a^b (1 - sinc^2(x)) dx
```

Under this conjecture, the imaginary parts {γ_n} are not independent — they repel
each other (GUE statistics). The equidistribution test measures whether {γ_n·log(p)/(2π)}
behaves as predicted by Montgomery.

**2. Consistency with GUE pair correlation.**

The growing sqrt(N)·D_KS is the GUE signature — zeros repel, so they're more
regularly spaced than independent uniform points. This CONFIRMS Montgomery (and
therefore RH as its predecessor), but it does NOT imply RH directly.

**3. The bridge direction is ONE-WAY:**
```
RH (zeros on critical line)
  => Montgomery pair correlation (GRH needed here too)
  => Equidistribution of {gamma_n * log(p)/(2pi) mod 1}
  => D_KS -> 0 as N -> inf
  => D_KS/T* << 1 (what we measure)
```

But NOT:
```
D_KS/T* << 1  =>  RH
```

The equidistribution test is a NECESSARY but NOT SUFFICIENT condition for RH.

---

## Corrected Bridge F1 Analysis

**What is measured:**
- D_KS(p,500)/T* = 10% — zeros are consistent with Montgomery/GUE (consistent with RH)
- sqrt(N)·D_KS growing — GUE correlation signature (consistent with Montgomery)
- These measurements are CONSISTENT WITH RH — they don't prove it

**What the bridge needs:**

**Option A (corrected):** Prove equidistribution of {γ_n·log(p)/(2π) mod 1}
unconditionally (without GRH). This would mean:
- Montgomery pair correlation holds without GRH
- This is stronger than Montgomery itself (which assumes GRH)
- Proving unconditional Montgomery ≈ proving RH

**Option B (void):** The D_KS-based off-line exclusion doesn't work. An off-line zero
at 1/2+δ+iγ₀ contributes γ₀ to the sequence — same as an on-line zero. D_KS is blind
to δ. Option B via the equidistribution test is mathematically impossible.

**Option C (via a different test):** A test that IS sensitive to Re(ρ):
- Li coefficients: λ_n = Σ_ρ [1-(1-1/ρ)^n]; RH ⟺ all λ_n ≥ 0
- de Bruijn-Newman: RH ⟺ Λ ≤ 0 (where Λ is the de Bruijn-Newman constant)
- Beurling-Nyman: RH ⟺ dist(1, E₀) = 0 in L²(0,∞)
- Baez-Duarte: RH ⟺ |d_N|² → 0 as N → ∞

None of these directly connect to the Fejér kernel / First-G. The equidistribution
test is not the right tool for Option B.

---

## What the Equidistribution Measurement IS Good For

Despite not being a RH detector (in the direct sense), the measurement:

D_KS(p, N) / T* = 5-10%   (at N=2000)

is valuable for a different reason:

**It confirms that the first 2000 zeros behave as GUE predicts.**

This means:
1. The zeros have the Montgomery pair correlation structure
2. This is consistent with RH (RH → Montgomery → GUE → equidistribution)
3. The growing sqrt(N)·D_KS is the predicted GUE correlation growth rate
4. D_KS/T* has 90%+ headroom: the zeros are far from any equidistribution failure

The test is a POSITIVE CONFIRMATION of GUE structure, not a test FOR RH.
It rules out some alternative zero distributions (e.g., zeros clustering at specific
imaginary heights), but doesn't rule out off-line zeros.

---

## Corrected F1 Status

**What is proved:**
- First-G = Fejér kernel (WP34 proved)
- Zeros are GUE-consistent: ρ=1.014, 0.43σ from analytic GUE (gue_calibration.py)
- Zeros pass equidistribution test: D_KS/T* = 5-10% at N=2000 (rh_growth_test.py)

**What follows from this:**
- The zeros are consistent with Montgomery pair correlation
- Montgomery pair correlation is consistent with RH (it requires GRH to prove)
- The program's measurements are CONSISTENT WITH RH — not proving it

**The bridge:**
F1 bridge closes when:
- First-G (Fejér at level k) is shown to IMPLY equidistribution of {γ_n·log(p)/(2π)}
  unconditionally — without assuming GRH
- This would be a stronger result than Montgomery's conjecture
- It would connect the arithmetic of Z/10Z (First-G) to the analytic structure of zeros

**The honest gap:**
F1 currently shows that the Fejér kernel appears in Montgomery's formula (proved)
and that the zeros are Fejér/GUE-consistent (measured). It does NOT show that the
Fejér structure of First-G forces zeros to the critical line. That additional step —
from "Fejér appears in the explicit formula" to "zeros are on Re(s)=1/2" — is the
unproved part of F1.

---

## The Clean F1 Statement (Post-Correction)

**Bridge F1 (corrected):**

Let F_k(u) be the level-k Fejér kernel from First-G. Let R₂(u) = 1 − sinc²(u).

Proved: F_k → R₂ as k → ∞ (Fejér convergence theorem, proved in WP34).

Measured: the first 2000 Riemann zeros are consistent with R₂ as the pair
correlation (ρ=1.014, D_KS/T*=5-10%).

Bridge conjecture: IF First-G (Fejér) implies R₂ as the pair correlation
of ANY sequence satisfying the explicit formula, THEN the Fejér structure
forces the zeros to lie on Re(s) = 1/2.

Gap: the conditional clause "IF First-G implies R₂ for any explicit-formula sequence"
is not proved. The explicit formula applies to both on-line and off-line zeros.

**This is the precise statement of where F1 stands.**

---

## Implication for Option B

Option B is now reformulated as:

**Option B (corrected):** Prove that a zero at Re(ρ) = 1/2+δ (δ > 0) would
VIOLATE the Fejér approximation at level k in the explicit formula — i.e., the
Fejér approximation at level k can only converge to R₂ if all zeros are on the line.

This is a strengthening of the Fejér convergence argument. It says: the convergence
F_k → R₂ is ONLY compatible with zeros on the critical line. Any off-line zero
would produce a DIFFERENT limiting pair correlation.

This is mathematically non-trivial. If Montgomery's conjecture (R₂ is the true
pair correlation ONLY under GRH) could be proved, it would show that F_k → R₂
implies all zeros on Re(s)=1/2. This would close F1.

**Option B corrected = prove that R₂ is incompatible with off-line zeros.**

This is exactly the content of Montgomery's conjecture: the sinc² pair correlation
arises ONLY from zeros on the critical line (under GRH). Option B becomes:
prove Montgomery unconditionally (which would largely close RH itself).

---

## Summary: F1 Status Corrected

| Status | Before correction | After correction |
|--------|-------------------|------------------|
| Option A | "Prove equidist. unconditionally" | Same — requires proving Montgomery unconditionally |
| Option B | "D_KS > T* excludes off-line zeros" | **VOID** — D_KS blind to Re(ρ) |
| Option B (corrected) | — | "Prove R₂ incompatible with off-line zeros" = prove Montgomery unconditionally |
| Net status | F1 has two viable options | F1 has ONE viable path: unconditional Montgomery |
| Hard wall | Montgomery/GRH | Same — unconditional Montgomery ≈ GRH |

The equidistribution measurement confirms GUE consistency (valuable) but is NOT
a test for Re(ρ) = 1/2. The bridge must go through Montgomery.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*Corrects MEMO_BRIDGE_MACHINES.md and Part XII of CLAY_FORMAL_RECORD.md*
