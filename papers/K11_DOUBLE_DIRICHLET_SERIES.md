# K11_DOUBLE_DIRICHLET_SERIES.md
## K11: The Double Dirichlet Series Z(s,w) — Last Theoretical Path

**Status**: B-tier conjecture. Functional equation existence is open.
**Follows from**: K10.C1 conjecture, K11.F numerical no-go

---

## 1. Motivation

After K11.F: the Kloosterman sum carries no pointwise signature of ζ-zeros at Re(s)=3/2.
The Eisenstein bridge is global: A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt.

The only surviving non-circular path requires either:
(a) An independent computation of |ζ(1+2it)|^{-2} (K10 showed all routes circular), OR
(b) A **two-variable structure** that encodes ζ-zero information in a second variable w,
    accessible via a functional equation in (s,w)

This document develops (b): the double Dirichlet series for Kloosterman sums.

---

## 2. The Full Kloosterman Zeta Function (Background)

Before the prime-restricted sum A3(s), there is the **full Kloosterman zeta function**:

```
Z_{Kl}(s, m, n) = Σ_{c≥1} (Kl(m,n;c) / c) · c^{-s}
```

This converges absolutely for Re(s) > 3/2 (Weil bound). For (m,n) = (1,1):

```
Z_{Kl}(s) = Σ_{c≥1} Kl(1,1;c) · c^{-s-1}
```

**Kloosterman multiplicativity:** Kl(1,1;mn) satisfies a multiplicativity relation
for gcd(m,n)=1 (not fully multiplicative, but an Euler product mod squares exists).

This gives Z_{Kl}(s) a partial Euler factorization at the square-free level:
```
Z_{Kl}(s) = Π_p (Z_{Kl,p}(s)) · (correction for prime-power contributions)
```

where Z_{Kl,p}(s) is the local factor at prime p.

**Local factor at p (D-tier, Iwaniec):**
```
Z_{Kl,p}(s) = 1 + Kl(1,1;p) p^{-s-1} + (corrections at p², p³, ...)
```

For the prime-square contribution: Kl(1,1;p²) = p · Kl(1,1;p) - p (Ramanujan identity).
For prime cubes: Kl(1,1;p³) = p² Kl(1,1;p) - 2p² (recursive).

---

## 3. The Natural Double Dirichlet Series

Define the **Kloosterman double Dirichlet series** by introducing a second variable
that captures the "depth" of Kloosterman sums:

```
Z(s, w) = Σ_{p prime} Kl(1,1;p) · p^{-s} · Σ_{k≥1} Kl(1,1;p^k) · p^{-kw}
```

This factors as:

```
Z(s, w) = Σ_p Kl(1,1;p) · p^{-s} · L_p(w)
```

where L_p(w) = Σ_{k≥1} Kl(1,1;p^k) p^{-kw} is the local Kloosterman generating series at p.

**Local series L_p(w) using the Ramanujan recursion:**

Kl(1,1;p^k) = p^{k-1} · Kl(1,1;p) - p^{k-1}  for k≥2 (by induction on the recursion)

So:
```
L_p(w) = Kl(1,1;p) · p^{-w} + Σ_{k≥2} (p^{k-1} Kl(1,1;p) - p^{k-1}) p^{-kw}
        = Kl(1,1;p) p^{-w} + p^{-1} Kl(1,1;p) · Σ_{k≥2} p^{k(1-w)}
                            - p^{-1} Σ_{k≥2} p^{k(1-w)}
```

For Re(w) > 1:
```
L_p(w) = Kl(1,1;p) p^{-w} + (Kl(1,1;p) - 1) · p^{-1} · p^{2(1-w)} / (1 - p^{1-w})
```

This is the local factor. Z(s,w) is then:
```
Z(s,w) = Σ_p Kl(1,1;p) p^{-s} · L_p(w)    (Re(s) > 3/2, Re(w) > 1)
```

---

## 4. Connection to Eisenstein L-Functions

The key structural observation: for any prime p, the local factor L_p(w) involves
Kl(1,1;p) and p^{-w}. The Sato-Tate angles θ_p give Kl(1,1;p) = 2√p cos(θ_p).

Therefore:
```
L_p(w) = 2√p cos(θ_p) · p^{-w} + (2√p cos(θ_p) - 1) · (correction)
```

The Eisenstein series on GL(2) has local factors at p given by:
```
L_p(s, E) = (1 - p^{-s})(1 - p^{-(s-1)})^{-1}   [Eisenstein L-function]
```

**Claim K11.2 (B-tier):** Z(s,w) factors (after completing at Archimedean places) as:

```
Z(s, w)  =  L(s + w - 1, E) · R(s, w)
```

where L(·, E) is the Eisenstein L-function (= ζ(s+w-1)/ζ(s+w)) and R(s,w) is a
"remainder" capturing the Kloosterman oscillations (the cos(θ_p) factor).

**Gap:** The Sato-Tate angles θ_p are equidistributed but correlated across primes.
R(s,w) is not a standard L-function; its analytic properties are unknown.

---

## 5. The Functional Equation Question

**Conjecture K11.FE (B-tier):** Z(s,w) satisfies a functional equation of the form:

```
Z(s, w) = G(s, w) · Z(1-s, w')    for some explicit G and transformation w ↦ w'
```

**Evidence for:**
- The Bump-Friedberg-Hoffstein theory of double Dirichlet series (type A₂ Weyl group)
  shows that many double sums built from GL(2) Fourier coefficients DO satisfy
  functional equations in both variables.
- The Kloosterman sum Kl(1,1;p) = a_f(p) for a GL(2) automorphic form f (the
  Kloosterman Maass form, if it exists — this is the K8 spectral interpretation).
  If f is self-dual (f = f̃), then its L-function satisfies s ↔ 1-s.
  Z(s,w) built from a_f would inherit this symmetry.

**Evidence against:**
- A3(s) is not multiplicative (K8.6). Functional equations for double Dirichlet series
  require twisted multiplicativity (the "correction factor" in the Weyl group action).
  Without multiplicativity, the standard machinery doesn't apply.
- The prime restriction in Z(s,w) breaks the structure needed for global functional equations.

---

## 6. Alternative: The Full Moduli Sum Z̃(s,w)

Instead of restricting to primes, define:

```
Z̃(s, w) = Σ_{c≥1} Kl(1,1;c) · c^{-s-1} · Σ_{k≥1} Kl(1,1;c^k) · c^{-kw}
```

This sums over ALL moduli c, not just primes.

**Why Z̃ is better:**
- Kloosterman sums ARE multiplicative over coprime moduli: Kl(mn) = Kl(m)Kl(n) for gcd(m,n)=1
- This gives Z̃ a genuine Euler product structure
- The Euler product structure enables functional equations via the Ramanujan recursion

**Euler product for Z̃:**
```
Z̃(s, w) = Π_p  Z̃_p(s, w)

Z̃_p(s, w) = Σ_{j,k≥0} Kl(1,1;p^j) · Kl(1,1;p^k) · p^{-(s+1)j - wk}
```

This is a double power series in (p^{-(s+1)}, p^{-w}), computable from the Ramanujan recursion.

**Status: B-tier.** The Euler product is well-defined. Whether it satisfies a functional
equation depends on whether the local factors Z̃_p(s,w) are symmetric in some sense.

---

## 7. The Weyl Group Action (B-tier framework)

The Bump-Friedberg-Hoffstein double Dirichlet series of type A₂ Weyl group W = S₃
satisfies functional equations under:
- (s, w) ↦ (1-s, w+s-1/2)    [action of simple reflection σ₁]
- (s, w) ↦ (s+w-1/2, 1-w)    [action of simple reflection σ₂]

These generate a group of 6 functional equations.

**Claim K11.3 (B-tier):** If Z̃(s,w) falls into the Bump-Friedberg-Hoffstein framework,
it satisfies functional equations under the A₂ Weyl group action.

**The connection to ζ-zeros:** Under the functional equation (s,w) ↦ (1-s, w'),
the analytic continuation of Z̃(s,w) to Re(s) < 1/2 would be explicit (given by
G(s,w) · Z̃(1-s,w')). If A3(s) = Z̃(s,0)|_{primes} and Z̃ has such a continuation,
then A3 inherits a continuation past Re(s)=3/2 — without circular dependence on ζ-zeros.

This is the B-tier hope: Z̃ provides the analytic continuation that A3 alone cannot have.

---

## 8. What K12 Must Establish

For the double Dirichlet approach to yield results, K12 must:

1. **Compute Z̃_p(s,w) explicitly** from the Ramanujan recursion to verify its structure.

2. **Test for local symmetry:** Does Z̃_p(s,w) have any symmetry under (s,w) ↦ (1-s,w')?
   If the local factor is symmetric, the global product inherits it.

3. **Compare to Bump-Friedberg-Hoffstein:** Identify which class of BFH double Dirichlet
   series Z̃ belongs to. The key is whether Kl(1,1;p^j)·Kl(1,1;p^k) satisfies the
   "twisted multiplicativity" condition required by BFH.

4. **If functional equation holds:** Use the functional equation to continue Z̃(s,w)
   to Re(s) < 1/2 at fixed w. Then Z̃(s,0)|_{primes} = A3(s) extends past Re(s) = 3/2,
   and the Eisenstein integral becomes analytically tractable without circularity.

---

## 9. Summary

```
K11 double Dirichlet status:

Z(s,w) [prime restricted]     -- B-tier conjecture, functional eq unknown
Z̃(s,w) [all moduli, Euler product]  -- B-tier conjecture, local factors computable
BFH A₂ Weyl group framework   -- B-tier candidate framework
K11.FE functional equation     -- B-tier open

Required for C-tier: explicit computation of Z̃_p(s,w) + test of local symmetry
Required for D-tier: proof that Z̃ satisfies A₂ functional equations
```

The program has converged to a single theoretical frontier: the double Dirichlet
series Z̃(s,w) and its functional equations. Everything else (K1–K11.F) is closed.
