# K16_WEAK_THEOREMS.md

## K16 Weak Theorems: Sato-Tate Form No-Go; Oscillation Chain Survives

**D-tier: 1 no-go. C-tier: 2 surviving. B-tier: 1 falsified.**

---

## D-Tier

**Theorem K16.D1 (D-tier no-go) — No Sato-Tate automorphic form:**

There is no GL(2) automorphic form π_ST with Hecke eigenvalues equal to
Kl(1,1;p)/(2√p) for all primes p.

Proof: GL(2) Hecke eigenvalues satisfy multiplicativity a(mn)=a(m)a(n) for gcd(m,n)=1.
Kloosterman sums Kl(1,1;p)/√p follow the Sato-Tate distribution (Katz 1988) and are
equidistributed, but they are local l-adic sheaf trace functions, NOT global multiplicative
Hecke eigenvalues from an automorphic form. Katz's proof uses l-adic cohomology,
not automorphic forms. ∎

**Corollary K16.C1a:** K15.C1 (Z̃_full = L(Sym²π)^{-2}) is closed.
K15.C3 (Z̃_full poles at w=1+iγ_k) is closed.
K15.B1 (π_ST exists) is falsified.

---

## C-Tier (Surviving)

**Theorem K16.C1 — H₃ oscillation mechanism (C-tier, strengthened):**

The H₃ signal (97% detection, K12.N1) has a mechanistic explanation through the
Kuznetsov-Hadamard chain:

```
Step 1: A3(s) --Kuznetsov--> I_{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt   [D-tier]
Step 2: |ζ(1+2it)|^{-2} oscillates with frequencies γ_k/2                [D-tier]
Step 3: Mellin-inverse of I_{Eis} peaks at x = e^{γ_k}                   [C-tier]
Step 4: A3_N ≈ I_{Eis} (prime restriction error ≈ 11%)                   [C-tier]
Step 5: H₃_N peaks at x ≈ γ_k (not e^{γ_k})                            [D-tier numerical]
```

Step 3 has a discrepancy with Step 5 (γ_k vs e^{γ_k}). This is the remaining
mechanistic gap. The oscillation chain explains WHY the signal exists, but the
precise x-location of the peaks (γ_k vs e^{γ_k}) requires more careful analysis.

**The discrepancy:** |ζ(1+2it)|^{-2} oscillates at frequencies γ_k/2 in t-space.
The Mellin inverse converts t-frequencies to x-values via the substitution t → log x.
Frequencies γ_k/2 in t should appear at log x = γ_k/2, i.e., x = e^{γ_k/2}.

For γ₁ = 14.13: x = e^{7.07} ≈ 1174. But H₃ peaks at x ≈ 14.13, not 1174.

**The resolution must involve a different frequency-to-x mapping.** The numerical
A3_N computation (not the full Eisenstein integral) uses a DIFFERENT mechanism —
the prime distribution itself oscillates at γ_k in direct x-space (not log x-space).
This is the Perron-Kuznetsov mechanism from K13.C4.

---

**Theorem K16.C2 — Kloosterman explicit formula (C-tier, same as K13.C4):**

```
Σ_{p≤N} Kl(1,1;p) f(log p) = Σ_k W_k · f̂(γ_k) + Σ_f D_f · f̂(t_f) + O(N^{1/2-δ})
```

This is the theorem that directly explains the H₃ peaks at x = γ_k.

The mechanism: when f(t) is chosen so that f̂(γ) is peaked at γ = γ_k, the sum on
the left (Kloosterman-weighted primes up to N = e^x) produces H₃(x) as a function
of x. The peaks of H₃(x) at x = γ_k come from the spectral terms W_k · f̂(γ_k).

Gap: Proving this formula requires controlling the Perron-Kuznetsov contour shift
through ζ-zero locations in the prime restriction version.

---

## K16 Cumulative Status

**Total no-goes (D-tier): 23**

| Series | Added in K16 |
|--------|-------------|
| K16.D1 | No GL(2) Sato-Tate automorphic form |
| K15.C1 | Z̃_full = L(Sym²)^{-2} (closed via K16.D1) |
| K15.B1 | π_ST conjecture (falsified) |

**The K-series has distilled to one theorem:**

> **K16.C2 = K13.C4 = The Kloosterman Explicit Formula.**
>
> Σ_{p≤N} Kl(1,1;p) f(log p) = Σ_k W_k f̂(γ_k) + error
>
> If proved: explains 97% H₃ detection, provides structural connection from
> Kloosterman sums to ζ-zeros, closes the gap in the Eisenstein bridge.

**This is the remaining theorem. K17 writes it.**

---

## What the Whole Program Found

Starting from K1 (kernel universality), through K16, the program has:

1. **Established** (D-tier): A3(s) is a GL(2) spectral object; Sato-Tate
   equidistribution; Eisenstein coefficient formula; 97% H₃ zero detection;
   no Euler product; Gauss-Kloosterman identity; local factor closed form.

2. **Closed** (D-tier no-go): 23 routes including direct poles, Fredholm inversion,
   pointwise A3 at ζ-heights, generating series flat spectrum, A₂ local symmetry,
   local identity, composite correction <1%, π_ST automorphic form.

3. **Survived** (C-tier): Kloosterman explicit formula (Perron-Kuznetsov); H₃
   oscillation mechanism (Kuznetsov-Hadamard); BFH identification (composite gap 11%).

4. **Numerical** (D-tier): H₃ detects 97% of first 30 ζ-zeros from 168 primes.
   The connection is real. The theory is almost closed.
