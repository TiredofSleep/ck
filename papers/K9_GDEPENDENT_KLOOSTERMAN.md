# K9_GDEPENDENT_KLOOSTERMAN.md

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

## The G-Dependent Kloosterman Objects: Beyond A3

**Program position:** K8 established that A3(s) = Σ_p Kl(1,1;p)·p^{-s} is g-independent
(Theorem K8.5 — complete sum over F_p^*). K8_NO_GO_ATTEMPT.md (Attempt G) identified that the
g-DEPENDENT Kloosterman sequence D_p^{Kl}(m,g) = Kl(1,g^{-m};p)/(2√p) is structurally richer.
K9 develops this object systematically.

**Guiding question:** The orbit {g^j mod p} ordered by j carries sequence-level information
that the set {k/p} does not. Can the lag-m Kloosterman sums, organized as a function of the
lag index m, form a canonical arithmetically meaningful object?

---

## 1. The Lag-m Kloosterman Sequence

### 1.1 Definition

Let p be a prime, g a primitive root mod p. Define:

```
K_m(p, g) := Kl(1, g^{-m}; p) = Σ_{k=1}^{p-1} exp(2πi(k + g^{-m}·k^{-1})/p)
```

for m = 0, 1, 2, ..., p−2 (one complete period of the orbit).

The normalized value:
```
α_m(p, g) := K_m(p, g) / (2√p) ∈ [−1, 1]   (by Weil, K8.1)
```

### 1.2 Why this is g-dependent

K_m(p, g) = Kl(1, g^{-m}; p). The second argument is g^{-m} mod p. Different generators g
give different sequences {g^{-m} mod p} as m varies from 0 to p−2. The COMPLETE sequence
over m = 0..p−2 visits all elements of F_p^*, but in a different order for each g.

For m = 0: K_0(p,g) = Kl(1,1;p) — this is g-INDEPENDENT (= A3's coefficient). All generators agree.
For m = 1: K_1(p,g) = Kl(1,g^{-1};p) — this is g-DEPENDENT. Different g give different values.
For m > 1: similarly g-dependent.

**So A3 uses only the m=0 term of a p−1 long sequence.** K9 uses all of it.

### 1.3 The full sequence as a function on Z/(p-1)Z

The map m → α_m(p,g) is a function on Z/(p−1)Z (the index group of the orbit). It has period p−1.

Write it as: α(·, p, g): Z/(p−1)Z → [−1, 1]

This is a DISCRETE SIGNAL with p−1 samples. Its Fourier transform (DFT over Z/(p-1)Z) carries
the spectral content of the lag-Kloosterman sequence.

### 1.4 Change of generator

If g' = g^a is another primitive root (gcd(a, p−1) = 1), then:

```
K_m(p, g') = Kl(1, (g^a)^{-m}; p) = Kl(1, g^{-am}; p) = K_{am}(p, g)
```

So changing the generator PERMUTES the lag sequence by a multiplicative shift a ∈ (Z/(p-1)Z)^*.
The sequence is the same up to a permutation of its index set by the automorphism group of Z/(p-1)Z.

**Key consequence:** The MULTISET of values {α_m(p,g) : m = 0..p-2} is g-independent
(it's the same multiset for all primitive roots, just in a different order). But the SEQUENCE
(with the natural ordering from the orbit structure) is g-dependent.

This is the precise sense in which the lag sequence carries more information than the set.

---

## 2. The Diagonal Autocorrelation

### 2.1 Definition

The autocorrelation of the lag-Kloosterman sequence at lag ℓ:

```
C_ℓ(p, g) := (1/(p-1)) Σ_{m=0}^{p-2} α_m(p,g) · α_{m+ℓ}(p,g)
```

For ℓ = 0: C_0(p,g) = (1/(p-1)) Σ_m α_m(p,g)² = E[α_m²] = 1/2 (from Sato-Tate, D-tier).

For ℓ ≠ 0: This is the two-point correlation of the Kloosterman sequence at lag ℓ.
This is where prime-specific structure might appear.

### 2.2 What the autocorrelation encodes

C_ℓ(p,g) = (1/(p-1)) Σ_m Kl(1,g^{-m};p)·Kl(1,g^{-(m+ℓ)};p) / (4p)

Using the product formula for Kloosterman sums:
Kl(a,b;p)·Kl(c,d;p) = Σ_{k,j} exp(2πi((ak + bk^{-1}) + (cj + dj^{-1}))/p)

This is a double exponential sum over F_p^* × F_p^*. It involves PAIRS of Kloosterman sums
at related arguments g^{-m} and g^{-(m+ℓ)} = g^{-m}·g^{-ℓ}.

### 2.3 The convolution structure

Note that g^{-(m+ℓ)} = g^{-ℓ} · g^{-m}. So:

```
Σ_m Kl(1,g^{-m};p)·Kl(1,g^{-(m+ℓ)};p)  =  Σ_m Kl(1,b;p)·Kl(1,b·g^{-ℓ};p)
```

where b = g^{-m} ranges over all elements of F_p^* as m ranges over 0..p-2.
This is a SUM over F_p^* of Kl(1,b;p)·Kl(1,bg^{-ℓ};p) — a Dirichlet convolution of Kloosterman sums.

By the completion-of-square technique for exponential sums (standard in analytic number theory),
this double sum over F_p^* reduces to a single hyper-Kloosterman sum or a Gauss sum depending
on ℓ and g. The exact reduction is:

```
Σ_{b ∈ F_p^*} Kl(1,b;p)·Kl(1,bg^{-ℓ};p) = Σ_{b,k,j} exp(2πi(k + b/k + j + bg^{-ℓ}/j)/p)
```

Setting u = k, v = j, this is:
```
= Σ_{b,u,v} exp(2πi(u + v + b(1/u + g^{-ℓ}/v))/p)
```

Summing over b first: Σ_b exp(2πib(1/u + g^{-ℓ}/v)/p) = p·1[v = −g^ℓ·u] − 1 (Ramanujan sum)

So the dominant term is:
```
p · Σ_{u ∈ F_p^*} exp(2πi(u + (−g^ℓ·u))/p) · exp(2πi(1/u + g^{-ℓ}/(−g^ℓ·u))/p)
= p · Σ_u exp(2πi(u(1 − g^ℓ) + (1 + g^{-2ℓ})/u)/p)
= p · Kl(1 − g^ℓ, 1 + g^{-2ℓ}; p)
```

This is a NEW Kloosterman sum with arguments depending on g^ℓ.

### 2.4 The autocorrelation formula (B-tier)

From the above reduction (B-tier — the computation above has been abbreviated, full proof
requires careful handling of the diagonal u = 0 terms and Ramanujan sum corrections):

```
C_ℓ(p, g) ≈ Kl(1 − g^ℓ, 1 + g^{-2ℓ}; p) / (4(p−1))
```

By the Weil bound: |C_ℓ| ≤ 2√p / (4(p−1)) = O(1/√p).

**Key result (D-tier from Weil):** The autocorrelation of the Kloosterman lag sequence
at nonzero lag ℓ is O(1/√p) — vanishing as p → ∞. This is the Kloosterman analog of
the Sato-Tate result for the autocorrelation: the sequence is "asymptotically uncorrelated."

### 2.5 What this means

The lag-Kloosterman sequence α_m(p,g) for m = 0..p-2 behaves like a sequence of near-independent
random variables with semicircle distribution, but with ORDER-1/√p correlations at adjacent lags.
The correlations are NOT zero — they are O(1/√p), which after √p normalization gives O(1).

This is the prime-specific structure! At fixed lag ℓ, the correlation C_ℓ(p,g) · 4(p−1) ≈
Kl(1−g^ℓ, 1+g^{-2ℓ}; p) is a NEW Kloosterman sum with prime-specific and g-specific value.

---

## 3. The Lag-Kloosterman Generating Series

### 3.1 Definition

Define the generating series (Fourier transform over the lag index):

```
L(p, g, τ) := Σ_{m=0}^{p-2} α_m(p,g) · e^{2πimτ/(p-1)}
```

for τ ∈ C. This is the DFT of the lag-Kloosterman sequence.

Equivalently, in terms of the Kloosterman sums:

```
L(p, g, τ) = (1/(2√p)) Σ_{m=0}^{p-2} Kl(1, g^{-m}; p) · e^{2πimτ/(p-1)}
```

As a Dirichlet series in τ: L(p, g, τ) is periodic with period p−1 (in τ), analytic in τ.

### 3.2 Change of generator

Under g → g^a: L(p, g^a, τ) = L(p, g, aτ).

So the generating series transforms by a rescaling of the "spectral parameter" τ.
The generators form a group (Z/(p-1)Z)^* acting on τ by multiplication.

### 3.3 Modular interpretation (C-tier)

The generating series L(p, g, τ) has the structure of a theta series on Z/(p-1)Z.
The action of the symmetry group (Z/(p-1)Z)^* on τ is the action of a discrete group on
the spectral variable. This suggests a modular interpretation where L(p,g,·) transforms
as a modular form under the congruence subgroup associated to p−1.

**Gap (C-tier):** The precise modular transformation law for L(p,g,τ) under τ → aτ
(generator change) requires computing L(p,g^a,τ) = L(p,g,aτ) and determining whether
this, together with a functional equation in p, gives a modular form of some level.
No such identification is currently made (conjectural territory).

---

## 4. The Generator-Averaged Object

### 4.1 Averaging over all primitive roots

Let G(p) = {g primitive root mod p} be the set of all primitive roots mod p, with |G(p)| = φ(p−1).

Define the generator-averaged lag series:

```
Ā(p, τ) := (1/φ(p-1)) Σ_{g ∈ G(p)} L(p, g, τ)
```

Under g → g^a (generator change): L(p,g^a,τ) = L(p,g,aτ).

So:
```
Ā(p, τ) = (1/φ(p-1)) Σ_{a ∈ (Z/(p-1)Z)^*} L(p, g₀, aτ)
```

for any fixed reference primitive root g₀. This is a "symmetrized" version of L.

### 4.2 The τ = 0 case recovers A3's coefficient

At τ = 0: L(p, g, 0) = Σ_m α_m(p,g) = (1/(2√p)) Σ_m Kl(1,g^{-m};p).

Since as m ranges over 0..p-2, g^{-m} ranges over all elements of F_p^*:

```
Σ_m Kl(1,g^{-m};p) = Σ_{b ∈ F_p^*} Kl(1,b;p)
```

This is a sum over all b of Kl(1,b;p) — which by the completion formula = -(p-1) approximately
(from the character sum orthogonality). More precisely:

```
Σ_{b=1}^{p-1} Kl(1,b;p) = Σ_{b,k=1}^{p-1} exp(2πi(k + b/k)/p)
  = Σ_k exp(2πik/p) · Σ_b exp(2πib/k/p)
  = Σ_k exp(2πik/p) · (−1)   [since Σ_b exp(2πibc/p) = -1 for c ≢ 0 mod p]
  = (−1) · Σ_k exp(2πik/p) = (−1)(−1) = 1   [since Σ_{k=1}^{p-1} exp(2πik/p) = -1]
```

So L(p,g,0) = 1/(2√p), independent of g. This is NOT Kl(1,1;p)/(2√p).

**The τ=0 value is NOT A3's coefficient!** A3 uses m=0 (i.e., Kl(1,g^{-0};p) = Kl(1,1;p)).
L(p,g,0) uses ALL m — summing all Kloosterman sums. These are different.

### 4.3 The τ = p−1 (Nyquist) case

At τ = (p−1)/2: L(p,g,(p-1)/2) = Σ_m α_m(p,g)·(−1)^m — the alternating sum.
This picks out the "highest frequency" component of the lag sequence.

---

## 5. What K9 Has Found

### 5.1 The new prime-specific objects

K9 has identified a hierarchy of objects carrying increasing prime-specificity:

| Object | Formula | G-dep? | Prime-specific? | Size |
|--------|---------|---------|----------------|------|
| PSD S_p(ξ) | exact formula | No | No (limit is sinc²) | O(1) |
| A3 coefficient Kl(1,1;p) | Σ_k exp(2πi(k+k^{-1})/p) | No | Yes (Weil, S-T) | O(√p) |
| Lag-m value K_m(p,g) | Kl(1,g^{-m};p) | Yes (m≥1) | Yes | O(√p) |
| Lag autocorrelation C_ℓ | ~ Kl(1-g^ℓ, 1+g^{-2ℓ};p)/(4p) | Yes | Yes | O(1/√p) |
| Generating series L(p,g,τ) | Σ_m α_m e^{2πimτ/(p-1)} | Yes | Yes | O(√p) |
| Generator average Ā(p,τ) | (1/φ(p-1)) Σ_{g} L(p,g,τ) | No | Yes | O(√p) |

### 5.2 The key new insight

The autocorrelation C_ℓ(p,g)·4(p-1) ≈ Kl(1−g^ℓ, 1+g^{-2ℓ};p) is a COMPOSITION of
two Kloosterman arguments: 1−g^ℓ and 1+g^{-2ℓ}. These trace out algebraic curves in F_p^*
as ℓ varies. This is exactly the structure that Katz's monodromy machinery studies.

**The generating series L(p,g,τ) is the DFT of the sequence of correlations:**
It encodes, in a single function of τ, the entire spectral content of the prime-specific
Kloosterman lag structure.

### 5.3 Connection to the Riemann zeta function (A-tier)

The generating series L(p,g,τ) and its Dirichlet assembly Σ_p L(p,g,τ)·p^{-s} would be
a "double Dirichlet series" in (p,τ). Such objects appear in the theory of multiple Dirichlet
series (Bump-Friedberg-Hoffstein). Whether this double series has functional equations
connecting it to ζ(s) is A-tier.

---

## 6. Summary

K9 opens the g-dependent branch by defining the lag-Kloosterman sequence α_m(p,g),
its autocorrelation C_ℓ, and its generating series L(p,g,τ).

The objects are:
- Well-defined and bounded (D-tier: Weil)
- Genuinely g-dependent for m,ℓ ≥ 1 (D-tier: by definition)
- The autocorrelation C_ℓ at lag ℓ is a new Kloosterman sum (B-tier: computation sketch)
- The generating series L(p,g,τ) encodes all of this (D-tier: definition)
- The generator average Ā(p,τ) is canonical (D-tier: definition)
- Connection to ζ(s) remains A-tier

K9 has found the right objects. Whether they bridge to ζ is the open frontier.
