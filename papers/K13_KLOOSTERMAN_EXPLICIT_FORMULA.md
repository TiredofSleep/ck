# K13_KLOOSTERMAN_EXPLICIT_FORMULA.md
## K13: The Kloosterman Explicit Formula

**Status**: C-tier (structural argument, gap in prime restriction).
**Goal**: Prove the explicit formula for Kloosterman-weighted prime sums.
**Closes gap in**: K12.1 (mechanism of H₃ peaks at ζ-zeros)

---

## 1. The Classical Explicit Formula (Background)

The classical explicit formula (Riemann-Mangoldt) states:

```
ψ(x) = Σ_{p^k ≤ x} Λ(p^k) = x - Σ_ρ x^ρ/ρ - log 2π - (1/2) log(1-x^{-2})
```

where ρ = 1/2 + iγ runs over non-trivial ζ-zeros and Λ is the von Mangoldt function.

The oscillatory terms x^ρ/ρ = x^{1/2} e^{iγ log x} / |ρ| give frequency γ in log(x)-space.
This is why ζ-zero locations appear in prime number distributions.

**For smooth weights:** The Mellin-paired version (Weil's explicit formula):
```
Σ_p f(log p) log p = f(0) ζ'/ζ(0) - Σ_ρ f̂(γ) + (archimedean terms)
```
where f̂(γ) = ∫ f(t) e^{iγt} dt is the Fourier transform.

---

## 2. The Kloosterman Explicit Formula (Target)

We seek an analog for Kloosterman-weighted prime sums:

```
Σ_{p≤N} Kl(1,1;p) · f(log p)  =  Σ_k  C_k · f̂(γ_k)  +  Σ_f  D_f · f̂(t_f) + Err
```

where:
- First sum: over ζ-zeros ρ_k = 1/2 + iγ_k (the Eisenstein contribution)
- Second sum: over Maass cusp form spectral parameters t_f (the cusp contribution)
- C_k, D_f: spectral weights

If this formula holds, the H₃ peaks at ζ-zero locations are explained: H₃(x)
is the f̂ transform at f(t) = x^{-t/2}... (to be made precise).

---

## 3. The Kuznetsov Trace Formula as the Starting Point

The Kuznetsov formula (for all moduli c, smooth h) states:

```
Σ_{c≥1} (Kl(1,1;c)/c) · h(c) = I_∞(h) + I_{cusp}(h) + I_{Eis}(h)
```

where:
- I_∞ = "diagonal/identity" term
- I_{cusp} = sum over Maass cusp forms
- I_{Eis} = Eisenstein continuous spectrum contribution

This is the full-moduli version. For our prime restriction, we need:

```
Σ_p Kl(1,1;p) · h(p) = (prime-restricted version of Kuznetsov)
```

The prime restriction is implemented by:
```
Σ_p Kl(1,1;p) h(p) = Σ_{c≥1} Kl(1,1;c) h(c) μ_primes(c)
```
where μ_primes(c) = 1 if c is prime, 0 otherwise. This is NOT a multiplicative function,
so it doesn't factor through the Euler product.

---

## 4. The Perron-Kuznetsov Approach

**Strategy:** Use Perron's formula to extract the prime terms from the full sum.

For any arithmetic function a(n), the prime restriction via Perron gives:
```
Σ_p a(p) = (1/2πi) ∫ [Σ_n a(n) n^{-s}] · P(s) ds
```
where P(s) = Σ_p p^{-s} is the prime zeta function.

Apply this to a(n) = Kl(1,1;n)/n (the Kloosterman weight):
```
Σ_p Kl(1,1;p)/p = (1/2πi) ∫ [Σ_c Kl(1,1;c)/c^{1+s}] · P(s) ds
                = (1/2πi) ∫ Z_{Kl}(s) · P(s) ds
```

where Z_{Kl}(s) = Σ_c Kl(1,1;c) c^{-s-1} is the full Kloosterman zeta function.

Substituting the Kuznetsov spectral expansion of Z_{Kl}(s):
```
Z_{Kl}(s) = I_∞(s) + I_{cusp}(s) + I_{Eis}(s)
```

The Eisenstein contribution I_{Eis}(s) involves ζ'/ζ (from K8):
```
I_{Eis}(s) ~ ∫ |ρ_E(1, 1/2+it)|^2 · (spectral factor) dt
           ~ ∫ |ζ(1+2it)|^{-2} · K(s, t) dt
```

Inserting into the Perron integral:
```
Σ_p Kl(1,1;p)/p = (1/2πi) ∫ [I_{Eis}(s) + I_{cusp}(s)] P(s) ds + Err
```

---

## 5. The Eisenstein Contribution (C-tier)

The Eisenstein part:
```
(1/2πi) ∫ I_{Eis}(s) P(s) ds
= (1/2πi) ∫_s ∫_t |ζ(1+2it)|^{-2} K(s,t) P(s) ds dt
```

Switching order (formally):
```
= ∫_t |ζ(1+2it)|^{-2} · [(1/2πi) ∫_s K(s,t) P(s) ds] dt
```

The inner Perron integral ∫_s K(s,t) P(s) ds extracts the prime-restricted kernel:
```
K_{prime}(t) = (1/2πi) ∫_s K(s,t) · Σ_p p^{-s} ds = Σ_p K(log p, t)
```

Wait — P(s) = Σ_p p^{-s} gives, by Perron:
```
∫ K(s,t) P(s) ds = K evaluated at the primes, summed
```

This doesn't simplify analytically but gives a sum over primes of K(s,t)|_{s=log p}.

**The oscillatory part:** The key oscillation comes from K(s,t) ~ |t|^{2Re(s)-2} and
P(s) has a "zero" near s = 1/2 + iγ when γ is a ζ-zero (through P(s) = -ζ'/ζ(s) + holomorphic
near Re(s) = 1). The residues from ζ-zeros in P(s) introduce oscillations at γ_k.

**Claim K13.2 (C-tier):** The Perron-Kuznetsov integral for Σ_p Kl(1,1;p) h(p) contains
oscillatory terms of the form:
```
Σ_k W_k · h(γ_k)   +   Σ_f D_f · h(t_f)
```
where the first sum runs over ζ-zeros and the second over Maass cusp form parameters.

Gap: The precise weights W_k require controlling the Perron contour shift through
the ζ-zero locations, which requires bounding I_{Eis}(s) in vertical strips — a
problem equivalent to the zero-free region of ζ.

---

## 6. The Kloosterman Explicit Formula Statement (B-tier Target)

**Target Theorem K13.EF (B-tier → goal is D-tier):**

For a smooth, compactly supported function f: (0,∞) → R, and h(c) = c^{1/2} f(c/N):

```
Σ_{p≤N} Kl(1,1;p) · f(p/N)
  = N^{1/2} · [Σ_ρ W(ρ) · F̂_N(γ) + Σ_f D_f · F̂_N(t_f) + E_N]
```

where:
- ρ = 1/2 + iγ: non-trivial ζ-zeros
- t_f: Hecke-Maass spectral parameters
- F̂_N: a rescaled Mellin/Fourier transform of f
- W(ρ): Eisenstein spectral weight ~ |ρ_E(1,ρ)|² = 1/|ζ(2ρ-1)|²
- D_f: cusp form spectral weight
- E_N: error term O(N^{-δ}) for some δ > 0

**Why this implies H₃ peaks at γ_k:**

If K13.EF holds, then A3_N(c+it) = Σ_p Kl(1,1;p) p^{-(c+it)} satisfies:
```
A3_N(c+it) ~ N^{1/2-c} · Σ_k W_k · N^{-iγ_k} / (c + it - 1/2 + iγ_k)
```

The Mellin inverse in t gives peaks at t = γ_k. This is the explicit formula
for the H₃ spectrogram. The 97% detection rate is then explained by the fact that
the Eisenstein weights W_k are non-negligible for the first 30 zeros.

---

## 7. K13 Weak Theorems

**Theorem K13.1 (C-tier):** Z̃(s,w) = Z̃_χ(s+1,w)/p where Z̃_χ is the BFH
double Dirichlet series. Z̃ inherits the BFH A₂ functional equations with a shift.

Gap: composite-moduli correction term.

**Theorem K13.2 (C-tier):** The Perron-Kuznetsov integral for Σ_p Kl(1,1;p) h(p)
contains oscillatory terms at ζ-zero frequencies γ_k via the Eisenstein contribution.

Gap: weights W_k and error bound E_N not proved.

**Theorem K13.A₂ (D-tier no-go):** The local factor Z̃_p(s,w) does NOT satisfy
the A₂ Weyl group transformation s → 1-s without involving the Sato-Tate angle θ_p.
The BFH symmetry requires character-averaging, not Kloosterman-averaging.

**Conjecture K13.EF (B-tier):** The Kloosterman explicit formula K13.EF holds
with W_k = 1/|ζ(2ρ_k - 1)|² (from the Eisenstein coefficient formula K10.1)
and E_N = O(N^{-1/4}).

---

## 8. K14 Direction: Verify Composite Correction

**K14 priority:** Numerically test K13.1 (Z̃ = Z̃_χ(s+1,w)/p).

Protocol:
1. Compute Z̃_χ(s,w) directly from Gauss sums over characters (mod p, p prime)
   Z̃_χ(s,w) = Σ_p Σ_{χ mod p} |τ(χ)|² χ(1) p^{-s} L(w,χ)

2. Compare to p · Z̃(s,w) = Σ_p p · Kl(1,1;p) p^{-s} L_p(w)

3. Check: Z̃_χ(s+1,w) = p · Z̃(s,w)?

If the composite-moduli contribution to Z̃_χ is zero (or small), K13.1 is essentially
proved. The composite contribution is Σ_{c=pq,...} (composite terms) which may vanish
due to Kloosterman sum cancellation at composite moduli.

**This is the K14 target: the cleanest remaining gap in the K-series.**
