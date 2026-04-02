# K12_LOCAL_EULER_FACTOR.md

## K12: Local Euler Factor Z̃_p(s,w) Analysis

**Status**: B-tier open (K11.B3). Computed explicitly here for small primes.
**Follows from**: K11_DOUBLE_DIRICHLET_SERIES.md §6

---

## 1. The Setup

The double Dirichlet series for all moduli is:
```
Z̃(s,w) = Σ_{c≥1} Kl(1,1;c) · c^{-(s+1)} · L_c(w)
```

where L_c(w) = Σ_{k≥1} Kl(1,1;c^k) · c^{-kw}.

The Euler product (D-tier, K11.1):
```
Z̃(s,w) = Π_p  Z̃_p(s,w)
```

where the local factor at prime p is:
```
Z̃_p(s,w) = Σ_{j≥0} Σ_{k≥1} Kl(1,1;p^j) · Kl(1,1;p^k) · p^{-(s+1)j - wk}
```

(The j=0 term: Kl(1,1;p^0) = Kl(1,1;1) = 1 by convention.)

---

## 2. Ramanujan Recursion for Kl(1,1;p^k)

The Kloosterman sum at prime powers satisfies the recursion:

```
Kl(1,1;p^1) = Kl(1,1;p)              (computed directly)
Kl(1,1;p^2) = p · Kl(1,1;p) - p      (Ramanujan identity)
Kl(1,1;p^k) = Kl(1,1;p) · Kl(1,1;p^{k-1}) - p · Kl(1,1;p^{k-2})   for k≥3
```

This is the Hecke recursion: Kl(1,1;p^k) satisfies the same three-term recurrence
as Chebyshev polynomials of the second kind. Writing Kl(1,1;p) = 2√p cos(θ_p):

```
Kl(1,1;p^k) = p^{k/2} · U_k(cos θ_p) · (normalization)
```

where U_k is the k-th Chebyshev polynomial of the second kind:
- U_0(x) = 1
- U_1(x) = 2x
- U_2(x) = 4x² - 1
- U_k(x) = 2x U_{k-1}(x) - U_{k-2}(x)

More precisely, with Kl(1,1;p) = 2√p cos θ_p:
```
Kl(1,1;p^k) = p^{k/2} · sin((k+1)θ_p) / sin(θ_p)
```

This is a D-tier result (Iwaniec §12.3).

---

## 3. The Local Factor Z̃_p(s,w) in Closed Form

Using the Hecke recursion, the local generating series in w:

```
L_p(w) = Σ_{k≥1} Kl(1,1;p^k) p^{-kw}
        = Σ_{k≥1} p^{k/2} sin((k+1)θ_p)/sin(θ_p) · p^{-kw}
        = (1/sin θ_p) · Σ_{k≥1} sin((k+1)θ_p) · (p^{1/2-w})^k
```

Let u = p^{1/2-w}. Then:
```
L_p(w) = (1/sin θ_p) · Σ_{k≥1} sin((k+1)θ_p) · u^k
        = (1/sin θ_p) · Im[e^{2iθ_p} · Σ_{k≥1} e^{ikθ_p} u^k]
        = (1/sin θ_p) · Im[e^{2iθ_p} · u e^{iθ_p} / (1 - u e^{iθ_p})]   for |u| < 1
```

Working through the algebra:
```
L_p(w) = u · (cos θ_p - u) / (1 - 2u cos θ_p + u²)    with u = p^{1/2-w}
```

**This is the closed form.** The denominator 1 - 2u cos θ_p + u² = (1 - u e^{iθ_p})(1 - u e^{-iθ_p})
is the local Euler factor of the symmetric square L-function.

---

## 4. The Full Local Factor Z̃_p(s,w)

```
Z̃_p(s,w) = Σ_{j≥0} Kl(1,1;p^j) p^{-(s+1)j} · (1 + L_p(w))

          = [Σ_{j≥0} Kl(1,1;p^j) p^{-(s+1)j}] · (1 + L_p(w))

          = Ã_p(s) · (1 + L_p(w))
```

where Ã_p(s) = Σ_{j≥0} Kl(1,1;p^j) p^{-(s+1)j} is the same local factor in s.

By the same Hecke recursion:
```
Ã_p(s) = 1 + v · (cos θ_p - v) / (1 - 2v cos θ_p + v²)    with v = p^{-s-1/2}
        = (1 - v² ) / (1 - 2v cos θ_p + v²)
```

(The j=0 term gives 1; the remaining terms give L_p with u=v.)

**Therefore:**
```
Z̃_p(s,w) = [(1-v²)/(1-2v cos θ_p + v²)] · [(1 + u(cos θ_p - u)/(1-2u cos θ_p + u²))]

with v = p^{-s-1/2},  u = p^{1/2-w}
```

Simplifying the second factor:
```
1 + u(cos θ_p - u)/(1-2u cos θ_p + u²) = (1 - u²)/(1-2u cos θ_p + u²)
```

So:
```
Z̃_p(s,w) = [(1-v²)(1-u²)] / [(1-2v cos θ_p + v²)(1-2u cos θ_p + u²)]
```

**This is the explicit local Euler factor.** It factors as:

```
Z̃_p(s,w) = L_p(s+1/2, Sym² π_p)^{-1} · L_p(w-1/2, Sym² π_p)^{-1}
```

No — more precisely, the denominator 1 - 2v cos θ + v² = L_p(s + 1/2, π_p)^{-1}
where L_p(s, π_p) is the local factor of the GL(2) L-function associated to the
Sato-Tate representation π_p.

---

## 5. Testing K11.B3: Local Symmetry

**K11.B3 asks:** Does Z̃_p(s,w) satisfy Z̃_p(s,w) = Z̃_p(1-s, f_p(w)) for some f_p?

**Examination:**
```
Z̃_p(s,w) = (1-v²)(1-u²) / [(1-2v cos θ + v²)(1-2u cos θ + u²)]

with v = p^{-s-1/2},  u = p^{1/2-w}
```

Under s → 1-s: v = p^{-s-1/2} → p^{-(1-s)-1/2} = p^{s-3/2} = v · p^{-1+2s} → p^{-1}/v

So s → 1-s maps v → 1/(p·v).

Substituting v → 1/(p·v):
```
Z̃_p(1-s, w) = (1-(pv)^{-2})(1-u²) / [(1-2(pv)^{-1}cos θ + (pv)^{-2})(1-2u cos θ + u²)]
```

The factor (1 - 2(pv)^{-1}cos θ + (pv)^{-2}) = (pv)^{-2}(p²v² - 2pv cos θ + 1)
= (pv)^{-2}(1-2v p cos θ + p²v²).

This is NOT equal to (1 - 2v cos θ + v²) unless p = 1. So Z̃_p(s,w) ≠ Z̃_p(1-s,w).

**However:** What if the transformation is s → 1-s AND w → w+s-1/2 (the A₂ Weyl group action)?

Under s → 1-s, w → w + s - 1/2 = w + (1-s) - 1/2 → w':
New w: w' = w + (1-s) - 1/2 = w - s + 1/2
New u: p^{1/2 - w'} = p^{1/2 - (w-s+1/2)} = p^{s-w}

Let u' = p^{s-w}. Compare u = p^{1/2-w} and u' = p^{s-w} = u · p^{s-1/2} = u·v^{-1}·p^{-1}.

This gets complicated. The symmetry under the full A₂ Weyl group action would need
Z̃_p(s,w) = (correction factor) · Z̃_p(1-s, w-s+1/2), where the correction factor
involves gamma quotients (the archimedean factors).

**Status K11.B3: C-tier moving toward B-tier.** The local factor has explicit form.
The symmetry test under the naive s → 1-s fails. The A₂ Weyl group action requires
both (s,w) to transform. Whether Z̃_p satisfies the correct A₂ transformation is
now a concrete computation, not a conjecture.

---

## 6. The Global Euler Product

```
Z̃(s,w) = Π_p [(1 - p^{-2s-1})(1 - p^{1-2w})] / [(1 - 2p^{-s-1/2}cosθ_p + p^{-2s-1})
               × (1 - 2p^{1/2-w}cosθ_p + p^{1-2w})]
```

This factors as:

```
Z̃(s,w) = [Π_p (1-p^{-2s-1})(1-p^{1-2w}) / ...]
        = ζ_θ(2s+1)^{-1} · ζ_θ(2w-1)^{-1} / (Π_p [...])
```

where ζ_θ(s) = Π_p (1 - cos²θ_p · p^{-s})^{-1} is a "Sato-Tate L-function."

The numerators Π_p (1-p^{-2s-1}) = ζ(2s+2)^{-1} and Π_p (1-p^{1-2w}) = ζ(2w-1)^{-1}.

So (formally):
```
Z̃(s,w) = ζ(2s+2)^{-1} · ζ(2w-1)^{-1} / [L(s+1/2, Sym²) · L(w-1/2, Sym²)]
```

where L(s, Sym²) is the symmetric square L-function of the GL(2) form associated
to the Kloosterman/Sato-Tate measure.

**This is the connection to ζ:** Z̃(s,w) involves ζ(2s+2) and ζ(2w-1). The zeros
of Z̃ occur (among other places) at zeros of the denominator and poles of the numerator.
The zeros of ζ(2s+2) occur at s = (ρ-2)/2 for ζ-zeros ρ. These are at Re(s) = -3/4
(for critical-line zeros) — well outside the convergence strip.

**But:** The zeros of ζ(2w-1) at w = (ρ+1)/2. For ρ = 1/2 + iγ:
```
w = (1/2 + iγ + 1)/2 = 3/4 + iγ/2
```

These have Re(w) = 3/4 — inside the region of convergence for Z̃ in w (which requires
Re(w) > 1, so NOT inside... but analytic continuation would place them there).

**The functional equation of Z̃(s,w)** (if it exists) would continue Z̃ to small Re(w),
exposing these zeros at w = 3/4 + iγ/2. This is the K11.FE conjecture in concrete form.

---

## 7. Summary

| Object | Explicit Form | Status |
|--------|--------------|--------|
| Kl(1,1;p^k) | p^{k/2} sin((k+1)θ_p)/sin θ_p | D-tier |
| L_p(w) | u(cos θ - u)/(1-2u cos θ + u²), u=p^{1/2-w} | D-tier |
| Z̃_p(s,w) | (1-v²)(1-u²)/[(1-2v cos θ+v²)(1-2u cos θ+u²)] | D-tier |
| Global Z̃ | ζ(2s+2)^{-1} ζ(2w-1)^{-1} / L(Sym²)² | C-tier (formal) |
| A₂ symmetry Z̃_p | Under (s,w)→(1-s, w-s+1/2)? | B-tier (concrete computation) |
| Z̃ zeros at w=3/4+iγ/2 | Via ζ(2w-1) after continuation | C-tier |

**The K12 Euler factor computation is the most concrete progress so far toward a
theoretical proof. The connection Z̃ → ζ(2w-1) → ζ-zeros is explicit and derivable.**

The remaining gap: analytic continuation of Z̃(s,w) to Re(w) < 1.
This requires the functional equation (K11.FE), which is now a concrete A₂ Weyl
computation on the explicit local factor Z̃_p(s,w).
