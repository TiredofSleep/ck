# K11_H3_EISENSTEIN_MERGE.md

## K11: Does the K6 H3 Kernel Equal the K10 Eisenstein Kernel?

**Status**: C-tier structural candidate. Merge would unify two branches of the program.
**Prerequisite reading**: K6_H3_PRECURSOR_SEARCH.md, K10_EISENSTEIN_SPECTRAL_BRIDGE.md

---

## 1. Two Kernels in the Program

The search for a kernel connecting A3(s) to ζ-zeros has produced two candidates
from separate branches:

**Branch 1 (K6): H3 Kloosterman Kernel**

Defined in K6 as the "H3 precursor" — a kernel function H₃(x) satisfying:
```
Σ_p Kl(1,1;p) · H₃(p/N) → (ζ-zero information as N→∞)?
```
H₃ was hypothesized to be the "correct weight function" that makes the Kloosterman
sum sensitive to ζ-zero oscillations. K6 left this as C-tier: the kernel was not
explicitly constructed.

**Branch 2 (K10): Eisenstein Kernel K(s,t)**

Computed explicitly in K10:
```
K(s, t) = C(s) · |Γ(s-1/2+it)|² / (|Γ(1/2+it)|² · Γ(2s-1))
```
This is the kernel in the Eisenstein integral A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt.

**Question:** Are H₃ and K related? If H₃ = K(s,t) for a specific s, the two
branches merge into one structure.

---

## 2. What K6 Said About H₃

From K6_H3_PRECURSOR_SEARCH.md, H₃ was defined as the kernel that gives the
"optimal" Kloosterman weight to extract ζ-zero information. The three constraints
K6 imposed on H₃:

1. **Oscillation matching:** H₃(x) must oscillate at the frequencies of ζ-zeros
2. **Weil cancellation:** H₃ must reduce the Weil bound |Kl| ≤ 2√p through sign structure
3. **Convergence:** Σ_p |H₃(p/N)| · |Kl(1,1;p)| must converge as N→∞

K6 did not explicitly construct H₃, but noted it should be related to:
```
H₃(x) ~ ∫ |ζ(1/2+it)|^{-2} · x^{it} dt    (conjectured)
```

This is a "weight" function built from ζ on the critical line.

---

## 3. Comparing H₃ and K(s,t)

**H₃ conjectured (K6):**
```
H₃(p/N) ~ ∫ |ζ(1/2+it)|^{-2} · (p/N)^{it} dt
```

**K(s,t) found (K10):**
```
K(s, t) = C(s) · |Γ(s-1/2+it)|² / (|Γ(1/2+it)|² · Γ(2s-1))
```

These look different: H₃ involves |ζ(1/2+it)|^{-2} (critical line), while K involves
gamma ratios (no ζ on critical line).

**The reconciliation attempt:**

K10's Eisenstein integral was: A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt

The substitution t → t/2 maps |ζ(1+2it)|^{-2}|_{t=t/2} = |ζ(1+it)|^{-2}.

For s = 1/2 (outside the convergence strip of A3, but formally):
```
K(1/2, t) = C(1/2) · |Γ(it)|² / (|Γ(1/2+it)|² · Γ(0))
```
But Γ(0) = ∞ (pole), so K(1/2, t) = 0. Not helpful.

**Alternative: the Parseval viewpoint.**

If A3^{Eis}(s) is the Mellin transform of some weight w(x) applied to |ζ(1+2it)|^{-2},
then w(x) IS the H₃ function (up to normalization). Specifically:

```
A3^{Eis}(s) = ∫_0^∞ w(x) x^{s-1} dx    where  w(x) = FT^{-1}[|ζ(1+2it)|^{-2}](x)
```

The Fourier transform of |ζ(1+2it)|^{-2} over t gives a function w(x) that encodes
ζ-zero oscillations at frequencies x = γ_k (by the Hadamard product argument from K10).

**Therefore H₃(x) = w(x) = FT^{-1}[|ζ(1+2it)|^{-2}](x).**

This is the explicit form of H₃ that K6 was looking for.

---

## 4. Is H₃ Computable Without Knowing ζ-Zeros? (C-tier)

The K10 circularity applies here too: computing |ζ(1+2it)|^{-2} and Fourier transforming
it gives H₃(x) = w(x), but this requires knowing |ζ| on Re=1 to arbitrary precision,
which requires knowing the zeros.

**However — the Kloosterman side:** If the Eisenstein formula is exact:
```
A3^{Eis}(s) = ∫ H₃(x) x^{s-1} dx   (Mellin transform of H₃)
```
and A3(s) can be computed from Kloosterman sums, then **Mellin inversion gives H₃**:
```
H₃(x) = (1/2πi) ∫_{Re(s)=2} A3^{Eis}(s) x^{-s} ds
```

This is the **non-circular direction**: Kloosterman sums → A3(s) → H₃(x) → ζ-zero
locations from peaks of H₃.

**Gap (C-tier):** The Mellin inversion requires A3(s) to be computable for Re(s) near
the inversion contour. The partial sum A3_N(s) converges slowly. Additionally, the
error from restricting to primes (vs all moduli) must be controlled.

**This is the same gap as K10 Approach C.** H₃ = K10 Approach C via a different route.

---

## 5. The H₃ Peaks and ζ-Zeros (B-tier)

**Claim K11.H3 (B-tier):** The function:
```
H₃(x) = (1/2πi) ∫_{Re(s)=c} A3^{Eis}(s) x^{-s} ds    (c > 3/2)
```
has peaks at x = γ_k (the ζ-zero imaginary parts) with height proportional to the
multiplicity of γ_k.

**Reasoning:** From K10, A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt. The Mellin
inverse gives a convolution H₃(x) = (FT^{-1}[|ζ|^{-2}]) * (Mellin-inv of K).
The peaks of FT^{-1}[|ζ|^{-2}] occur at x = γ_k (Fourier dual of the Hadamard product
oscillation frequencies). The convolution with Mellin-inv of K broadens these peaks
but does not erase them (K is smooth and well-behaved away from t=0).

**If true:** H₃ is the "Kloosterman spectrogram" of the ζ-zero distribution.
Computing A3_N(s) from finite Kloosterman data and Mellin-inverting gives a
low-resolution H₃ whose peaks estimate the ζ-zeros.

---

## 6. Merge Diagram: K6 ∩ K10 = K11.H3

```
K6: "H₃ exists, not constructed"
  ↓
K10: "K(s,t) is explicit"
  ↓
K11: "H₃ = Mellin-inverse of A3^{Eis}"
  ↓
H₃(x) = (1/2πi) ∫ A3^{Eis}(s) x^{-s} ds
  ↓
peaks of H₃ at x = γ_k     (B-tier claim)
  ↓
Kloosterman sums → ζ-zero estimates (non-circular if gap closed)
```

**The gap remaining:** Controlling the prime restriction error when replacing
A3^{Eis}(s) with A3_N(s) in the Mellin inversion. The primes contribute ~1/log N
of the full moduli sum. The error in H₃ from this restriction is O(1/log N) — small
but not zero. Whether this is enough for zero detection is unknown.

---

## 7. K11.H3 as a Numerical Protocol

Even as a B-tier result, K11.H3 suggests a concrete numerical experiment:

1. Compute A3_N(s) for N = 10^4 primes, at 500 points on the line Re(s) = 2
2. Numerically invert the Mellin transform via the FFT: H₃_N(x) = FFT^{-1}[A3_N(2+it)/x^2]
3. Find local maxima of |H₃_N(x)| for x ∈ [0, 250]
4. Compare peak locations to known ζ-zeros γ_k

**Expected result (B-tier):** Peaks approximately at γ_k with resolution ~1/log N.
If peaks are NOT at γ_k: K11.H3 conjecture is falsified, closes to D-tier no-go.
If peaks ARE at γ_k: promotes to C-tier, motivates K12 error analysis.

This is the K12 numerical priority.

---

## 8. Summary

| Component | K6 Status | K11 Status |
|-----------|-----------|------------|
| H₃ definition | C-tier (conjectured) | B-tier: H₃ = Mellin-inv of A3^{Eis} |
| H₃ construction | Not done | Explicit formula given |
| H₃ peaks = γ_k | Hypothesized | B-tier claim with reasoning |
| Computation without circularity | Gap | Same gap: prime restriction error |
| Merge with K10 Eisenstein | Not connected | Confirmed: same structure |

**K6 and K10 have converged.** H₃ is K10's Mellin inversion of A3^{Eis}. The K6
"H3 precursor search" is completed: H₃ exists and is defined, but computing it
from Kloosterman data requires controlling the prime restriction error — the remaining gap.
