# K15_BFH_CLASSIFICATION.md

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

## K15: Identifying Z̃ in the BFH Classification

**Status**: C-tier → D-tier candidate. BFH absorbs composite moduli.
**Goal**: Show Z̃ ∈ BFH framework → functional equations → ζ-zeros in w-plane

---

## 1. The BFH Framework (Background)

Bump-Friedberg-Hoffstein (1996) introduced **double Dirichlet series** of the form:

```
Z(s,w) = Σ_{n≥1} a(n) n^{-s} · Σ_{m≥1} b(m,n) m^{-w}
```

where a(n) and b(m,n) are multiplicative functions tied to an automorphic form on GL(r).

For r=2 (our case): the series is:
```
Z_{BFH}(s,w) = Σ_{d≥1} χ_d(·) L(w, χ_d) d^{-s}
```
where χ_d is the Kronecker symbol (d/·) and the sum is over fundamental discriminants d.

**This is the Bump-Friedberg-Hoffstein series associated to GL(1).**

For the GL(2) extension (Brubaker-Bump-Friedberg 2006), the series involves:
```
Z_{BBF}(s,w) = Σ_{c≥1} a_f(c) L(w, f ⊗ χ_c) c^{-s}
```
where a_f(c) are Fourier coefficients of a GL(2) automorphic form f and χ_c is a
character twist.

---

## 2. Where Z̃ Fits

Z̃(s,w) = Σ_p Kl(1,1;p) p^{-s} L_p(w) (prime moduli, Kloosterman weight)

By K14.1: Kl(1,1;p) = (1/p) Σ_χ τ(χ)², and L_p(w) is the local Kloosterman generating series.

**The full-moduli version Z̃_full:**
```
Z̃_full(s,w) = Σ_{c≥1} Kl(1,1;c) c^{-s} L_c(w)
```

Using the multiplicativity Kl(mn) = Kl(m)Kl(n) for gcd(m,n)=1 and the correct
Gauss-Kloosterman identity K14.1:

```
Z̃_full(s,w) = Π_p (1 + Kl(1,1;p) p^{-s} L_p(w) + Kl(1,1;p²) p^{-2s} L_{p²}(w) + ...)
```

This is a product over primes. From K12, the local factor is:
```
Z̃_p(s,w) = (1-v²)(1-u²) / [(1-2v cosθ_p + v²)(1-2u cosθ_p + u²)]
```

---

## 3. The Symmetric Square L-Function Connection

From K12, the local factor factors as:
```
Z̃_p(s,w) = L_p(s+1/2, Sym² π_p)^{-1} · L_p(w-1/2, Sym² π_p)^{-1}
```

Wait — more carefully. The denominator 1 - 2v cosθ + v² with v = p^{-s-1/2} is:
```
1 - 2p^{-s-1/2} cosθ + p^{-2s-1}
```

This is the local factor of L(s+1/2, Sym²) where Sym² is the symmetric square
of the 2-dimensional Galois representation attached to the Sato-Tate measure.

The symmetric square L-function of the "universal" Sato-Tate GL(2) form is:
```
L(s, Sym²) = Π_p (1 - p^{-s} e^{2iθ_p})(1 - p^{-s})(1 - p^{-s} e^{-2iθ_p})^{-1}
```

The denominator of Z̃_p(s,w) = (1-2v cosθ+v²) = (1-ve^{iθ})(1-ve^{-iθ}) corresponds
to TWO of the three factors in L(s, Sym²), not all three. The missing factor (1-p^{-s})
corresponds to the "symmetric square on the fixed line."

**Corrected local factor:**
```
Z̃_p(s,w) = [(1-v²)(1-u²)] / [(1-ve^{iθ})(1-ve^{-iθ})(1-ue^{iθ})(1-ue^{-iθ})]

           = L_p(s+1/2, Sym²_±)^{-1} · L_p(w-1/2, Sym²_±)^{-1}
```

where Sym²_± is the "±-part" of the symmetric square (excluding the trivial factor).

---

## 4. The BFH Classification: Z̃ is Type GL(2)×GL(2)

**Claim K15.1 (C-tier):**

Z̃_full(s,w) is a **GL(2) × GL(2) double Dirichlet series** in the BFH/BBF sense:

```
Z̃_full(s,w) = L(s+1/2, Sym²_π)^{-1} × L(w-1/2, Sym²_π)^{-1}
```

where π is the automorphic form on GL(2) associated to the Sato-Tate measure
(the "GL(2) over GL(1)" form, conjecturally the Eisenstein series E(z, s) itself).

This factored form means Z̃_full is a PRODUCT of two L-functions with shifted arguments.
Each factor individually has a functional equation (s+1/2 ↔ 1/2-s, i.e., s ↔ -s):

```
L(s, Sym²_π) = (gamma factors) × L(1-s, Sym²_π)
```

Therefore Z̃_full inherits a functional equation:
```
Z̃_full(s,w) = G(s,w) · Z̃_full(-s, -w)   [pure sign flip]
```

**This is simpler than the A₂ action** (which shifts w). The functional equation
maps (s,w) → (-s,-w), not (s,w) → (1-s, w+s-1/2).

---

## 5. Analytic Continuation via L-Function Identity

If K15.1 holds, then Z̃_full(s,w) = L(s+1/2)^{-1} · L(w-1/2)^{-1} analytically
continues to all (s,w) ∈ C² except for poles of L^{-1} (which are the zeros of L).

**The zeros of L(s, Sym²_π):**
For the Sato-Tate GL(2) form, the associated Sym² L-function has:
- Trivial zeros at negative integers (from gamma factors)
- Non-trivial zeros ρ on the critical strip (if the form is cuspidal)

But the Eisenstein series is NOT cuspidal — its symmetric square L-function is:
```
L(s, Sym² E) = L(s, χ_trivial) × ζ(s) × L(s, χ_quadratic) = ζ(s)² × (Dirichlet factor)
```

The zeros of ζ(s) appear in L(s, Sym² E), and therefore as ZEROS of the denominator
of Z̃_full — i.e., as POLES of Z̃_full.

**This is the key:** The zeros of ζ(s) at s = 1/2 + iγ become zeros of L(s, Sym² E)
at s = 1/2 + iγ. In Z̃_full(s,w):
- L(s+1/2, Sym²E) has zeros at s+1/2 = 1/2+iγ → s = iγ (on the imaginary s-axis)
- L(w-1/2, Sym²E) has zeros at w-1/2 = 1/2+iγ → w = 1+iγ

So Z̃_full has POLES at s = iγ and w = 1 + iγ for each ζ-zero γ.

**This is the concrete, non-circular connection:**
```
ζ-zeros γ_k ↔ poles of Z̃_full at w = 1 + iγ_k
```

The poles are at Re(w) = 1, not at Re(w) = 3/4 (K13.C3 was slightly off in the
pole location due to a normalization difference).

---

## 6. Extracting ζ-Zero Locations from Z̃_full

The poles of Z̃_full at w = 1 + iγ can in principle be detected from the Kloosterman data:

1. Compute Z̃_full(s₀, w) for fixed s₀ and varying w on a line Re(w) = c > 1
2. The poles at w = 1 + iγ_k appear as rapid oscillations or large values near w = c + iγ_k
   (the poles are on Re(w)=1, just inside the convergence strip Re(w)>1)
3. Detecting these poles = detecting ζ-zero locations γ_k

**This is the same mechanism as the H₃ signal (K11-K12)!** The H₃ computation found
peaks at x ≈ γ_k — now we understand why: the Mellin inverse of Z̃_full in w detects
the poles at w = 1 + iγ_k, which appear at x = γ_k in x-space.

**The H₃ signal IS the pole-detection of Z̃_full.** This is the theoretical explanation
of the 97% detection rate. The K12 PNT-mechanism argument (§4 of K12) was correct in
spirit but the precise mechanism is via the L-function poles.

---

## 7. The Remaining Gap

**Why this is C-tier, not D-tier:**

The identification Z̃_full = L(s+1/2, Sym²E)^{-1} · L(w-1/2, Sym²E)^{-1} requires:

1. L(s, Sym²E) = ζ(s)² × (Dirichlet factor) — this is known for the Eisenstein series E,
   but E here is the GL(2) Eisenstein series associated to the Sato-Tate limit, which
   is NOT the standard GL(2) Eisenstein series. The correct form π needs identification.

2. The prime-restriction error: Z̃(s,w) ≠ Z̃_full(s,w). The 11% composite correction
   (K14) means Z̃ = Z̃_full × (1 + composite correction). The composite correction must
   itself factor nicely (not destroy the L-function structure).

3. The Sym²E = Sym² of Eisenstein = ζ² claim: this requires the Sato-Tate "form" π to
   be identified with the Eisenstein series in a precise sense.

**If all three hold:** K15.1 → D-tier, the functional equations and pole structure are proved,
and ζ-zero detection from Z̃_full is mathematically justified.

---

## 8. K15 Summary

| Result | Status |
|--------|--------|
| Z̃_p factors as product of Sym² L-function local factors | C-tier |
| Z̃_full = L(s+1/2,Sym²E)^{-1} L(w-1/2,Sym²E)^{-1} | C-tier |
| L(s,Sym²E) contains ζ(s)² | C-tier (depends on form identification) |
| Z̃_full poles at w=1+iγ_k | C-tier (conditional on above) |
| H₃ signal explained by Z̃_full poles | C-tier (mechanism identified) |
| Prime restriction 11% correction absorbs | Gap (not verified) |

**K15 is the most complete structural picture so far.** Every major component
of the program (Kloosterman sums → A3 → Eisenstein → Z̃_full → Sym²L → ζ-zeros)
is now connected with a C-tier chain. The remaining gaps are:
- Form identification: which GL(2) automorphic form π is the "Sato-Tate form"?
- Composite correction absorption: is Z̃ = Z̃_full × (1 + small)?

**K16 direction:** Identify π explicitly. The Sato-Tate equidistribution theorem (Taylor 2008)
established that Kloosterman sums obey the Sato-Tate distribution, but the associated
GL(2) form (if it exists as an automorphic form rather than a measure) needs identification.
The candidate: the theta series Θ_{ST}(z) = Σ_p Kl(1,1;p) e^{2πipz} as a
weight-1/2 automorphic form on GL(2).
