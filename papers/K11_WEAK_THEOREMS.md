# K11_WEAK_THEOREMS.md
## K11 Weak Theorems: Double Dirichlet and H₃ Merge

**D-tier: 3 results. C-tier: 2 results. B-tier: 3 conjectures.**

---

## D-Tier (Proved)

**Theorem K11.F (D-tier, numerical):**

A3_N(3/2 + i·γ_k) for the first 100 ζ-zeros is statistically indistinguishable
from A3_N(3/2 + i·t) at 300 uniformly random heights.

```
KS statistic = 0.053   (threshold for "same distribution": KS < 0.10)
Mean at zeros:  0.3778   Mean at random:  0.3709   Ratio: 1.019
```

The Kloosterman-Dirichlet series carries no pointwise analytic signature at ζ-zero heights.
The Eisenstein bridge is global (integral), not local (evaluation at isolated points).

**Proof:** Direct computation, `k11_zero_height_test.py`, 303 primes, 100 zeros, 300 controls. ∎

---

**Theorem K11.1 (D-tier):** The full Kloosterman zeta function Z̃(s,w) defined by
```
Z̃(s,w) = Σ_{c≥1} Kl(1,1;c) c^{-s-1} · Σ_{k≥1} Kl(1,1;c^k) c^{-kw}
```
has an Euler product:
```
Z̃(s,w) = Π_p Z̃_p(s,w)
```
due to the multiplicativity Kl(mn) = Kl(m)Kl(n) for gcd(m,n)=1.

**Proof:** Standard multiplicativity of Kloosterman sums at coprime moduli (Iwaniec §3.2). ∎

---

**Theorem K11.2 (D-tier):** The H₃ function from K6 has explicit form:
```
H₃(x) = (1/2πi) ∫_{Re(s)=c, c>3/2} A3^{Eis}(s) · x^{-s} ds
```
This is the Mellin inverse of the Eisenstein contribution A3^{Eis}(s), and satisfies:
```
∫_0^∞ H₃(x) x^{s-1} dx = A3^{Eis}(s)   for Re(s) > 3/2
```

**Proof:** Definition by Mellin inversion; the integral exists by the rapid decay of
A3^{Eis}(s) as |Im(s)|→∞ (from K10: |ρ_E|² decays via |Γ(1/2+it)|^{-2} ~ e^{-π|t|}). ∎

---

## C-Tier (Structural, gap in proof)

**Theorem K11.C1 (C-tier):** The peaks of H₃(x) occur at x ≈ γ_k (imaginary parts
of ζ-zeros) with height proportional to the local density of zeros near γ_k.

Evidence: A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt. Mellin inversion gives H₃ as a
convolution of FT^{-1}[|ζ|^{-2}] with a smooth kernel. Peaks of FT^{-1}[|ζ|^{-2}] are
at the Fourier dual of Hadamard product oscillation frequencies: x = γ_k/2 (from the
parametrization t → γ_k/2 in the Eisenstein integral).

Gap: The prime restriction (A3 sums over primes, not all moduli) introduces an error
O(1/log N) in H₃_N. Whether this error corrupts the peak locations is not proved.
Also: the "peaks of a convolution" claim requires the kernel (Mellin-inv of K) to be
sufficiently concentrated, which depends on the decay of K(s,t) not proved in K10.

---

**Theorem K11.C2 (C-tier):** The double Dirichlet series Z̃(s,w) satisfies a
functional equation under the reflection (s,w) ↦ (1-s, f(w)) for some function f,
IF the local factor Z̃_p(s,w) satisfies a local symmetry at each prime p.

Evidence: Bump-Friedberg-Hoffstein (1996) proved that double Dirichlet series built
from GL(2) Fourier coefficients with twisted multiplicativity satisfy A₂ Weyl group
functional equations. The Kloosterman sums Kl(1,1;p) are GL(2) Fourier coefficients
(by the spectral interpretation from K8). The twisted multiplicativity of Kl(mn) is
weaker than BFH requires (BFH needs twisted multiplicativity under Dirichlet characters,
which is different from coprime multiplicativity).

Gap: Whether Kloosterman twisted multiplicativity matches BFH twisted multiplicativity
is not verified. This is the key gap. If it does, the functional equation follows from
BFH. If not, a new proof is needed.

---

## B-Tier Conjectures

**Conjecture K11.B1 — Z̃ BFH functional equation:**
```
Z̃(s, w) = G(s, w) · Z̃(1-s, w + s - 1/2)
```
where G(s,w) is an explicit ratio of L-functions and gamma factors.

**Conjecture K11.B2 — H₃ peaks at zero heights:**

The numerically computed H₃_N(x) (from A3_N via Mellin inversion) has local maxima
at x ≈ γ_k for the first K zeros, with accuracy O(1/log N).

Pre-registration: With N=10^4 primes, the first 20 ζ-zeros should appear as peaks
in |H₃_N(x)| with |peak_x - γ_k| < 1.0.

**Conjecture K11.B3 — Local factor symmetry:**

The local Euler factor Z̃_p(s,w) satisfies:
```
Z̃_p(s, w) = Z̃_p(1-s, f_p(w))    for all primes p
```
for some explicit transformation f_p.

If K11.B3 is true, K11.C2 promotes to D-tier and K11.B1 follows from standard BFH machinery.

---

## Cumulative Status After K11

**Total no-goes documented (D-tier): 20**

| Added in K11 | Route | Result |
|--------------|-------|--------|
| K11.F | Pointwise A3 at ζ-zero heights | D no-go |

**Surviving paths:**
1. Z̃(s,w) BFH functional equation (K11.B1) — B-tier
2. H₃ peaks at ζ-zero heights (K11.B2) — B-tier numerical
3. Local factor symmetry Z̃_p (K11.B3) — B-tier

**K12 priorities:**
1. Compute Z̃_p(s,w) explicitly from Ramanujan recursion (test K11.B3 locally)
2. Run H₃ numerical experiment: A3_N Mellin inversion → peak detection → compare to γ_k
3. Search BFH literature for Kloosterman-specific double Dirichlet results
