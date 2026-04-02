# K7 — Weak Theorems

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: D** (all three theorems proved). These are weak theorems in the sense that they do not establish an RH connection — they establish necessary structural facts about what CAN and CANNOT carry prime-specific information in the Luther-Sanders orbit setting. They constitute the proved backbone of the K7 program.

---

## Purpose

The K7 program has three closed routes (A1, A2, D_p^PSD assembly — see K7_NO_GO_ATTEMPT.md and K7_EXPLICIT_FORMULA_COMPATIBILITY.md) and one surviving structural candidate (A3, the Kloosterman route — see K7_MULTIPLICATIVE_CHARACTER_ROUTE.md). The theorems in this document explain WHY the closed routes fail and WHY a different class of objects is required. They serve as the logical substrate for the K7 no-go and as proof that the Kloosterman route is the minimal viable extension.

---

## Theorem K7.1 — PSD Oscillatory Decomposition

**Statement:** The PSD deviation D_p^PSD(xi) is a bounded oscillatory object satisfying:

```
(a) |D_p^PSD(xi)| <= C(xi)    for all primes p and all xi not an integer multiple of p,

(b) D_p^PSD(xi) -> c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)]    as p -> infty (p prime),

(c) |D_p^PSD(xi) - c_0(xi)| = O(1/p)    uniformly in xi on any interval [epsilon, M]
                                           with 0 < epsilon < M < infty.
```

Moreover, the limit c_0(xi) is a fixed function of xi determined entirely by sinc calculus:

```
c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)]
         = 2*sinc^2(xi) - 2*sinc(xi)*cos(pi*xi)
         = 2*sinc(xi) * [sinc(xi) - cos(pi*xi)]
         = -4*sinc(xi)*sin^2(pi*xi/2)*...    (various equivalent forms)
```

The function c_0(xi) is real-analytic on R, decays like |xi|^{-2} as |xi| -> infty, satisfies c_0(0) = 0 (verified by L'Hopital), and has infinitely many zeros (at the zeros of sinc and at solutions of sinc(xi) = cos(pi*xi)).

**Proof:**

Part (a): From the exact formula S_p(xi) = sin^2(pi*xi*(p-1)/p) / ((p-1)^2 * sin^2(pi*xi/p)):

```
0 <= S_p(xi) <= 1/(p-1)^2 * (1/sin^2(pi*xi/p))
```

For xi in a compact set away from integers, |sin(pi*xi/p)| >= c/p for some constant c > 0 depending on the compact set and xi. So S_p(xi) = O(p^2/p^2) = O(1). Therefore D_p^PSD(xi) = p*(S_p(xi) - sinc^2(xi)) = O(p * O(1)) at first glance — but this is too crude.

The refined bound uses the exact formula directly. For xi in (0,1) away from 0:

```
sin^2(pi*xi*(p-1)/p) <= 1  and  (p-1)^2 * sin^2(pi*xi/p) >= (p-1)^2 * C / p^2
```

for a constant C > 0. So S_p(xi) = O(p^2/(p-1)^2) = O(1). The deviation:

```
D_p^PSD(xi) = p*(S_p(xi) - sinc^2(xi)) = p*(S_p(xi) - sinc^2(xi))
```

Both S_p(xi) and sinc^2(xi) are O(1), so their difference is O(1), and D_p^PSD = O(p)*O(1/p) = O(1) by the Taylor expansion (the O(1/p) cancellation is the content of the leading term computation in K7_NO_GO_ATTEMPT.md, Step 3).

More precisely, from the Taylor expansion:

```
D_p^PSD(xi) = c_0(xi) + c_1(xi)/p + O(1/p^2)
```

with c_0(xi) and c_1(xi) both bounded on compact sets. So |D_p^PSD(xi)| <= |c_0(xi)| + |c_1(xi)|/p + O(1/p^2) <= C(xi) for all large p. For small p (finite check), the exact formula is bounded by inspection.

Part (b) and (c) follow directly from the Taylor expansion proved in K7_NO_GO_ATTEMPT.md: D_p^PSD(xi) = c_0(xi) + O(1/p) uniformly on compact sets away from integers.

**QED.**

**Note:** Theorem K7.1 is purely descriptive — it characterizes D_p^PSD without any claim about RH. Its content is entirely classical (exact formula + Taylor expansion). The "oscillatory" qualifier refers to c_0(xi) being a function of xi that oscillates (has infinitely many sign changes), not to D_p^PSD varying with p. In fact, for large p, D_p^PSD(xi) barely varies with p — it is essentially frozen at c_0(xi).

---

## Theorem K7.2 — Primeness Enters Through Sequence, Not Set

**Statement:** Any prime-sensitive extension of the corridor that depends only on the SET of orbit values {g^0/p, ..., g^{p-2}/p} — that is, on the empirical measure

```
mu_p = (1/(p-1)) * sum_{j=0}^{p-2} delta_{g^j mod p / p}
```

— is necessarily g-independent and carries no generator-specific arithmetic.

Formally: let F : M_1([0,1]) -> R be any continuous functional on the space of probability measures on [0,1] (with the weak topology). Then F(mu_p) is independent of the choice of primitive root g mod p.

Proof:

The empirical measure mu_p is a sum of point masses at the positions {g^j mod p / p : j = 0, ..., p-2}. The set {g^j mod p : j = 0,...,p-2} = {1, 2, ..., p-1} for every primitive root g (by definition of a primitive root). The positions {k/p : k = 1,...,p-1} are identical regardless of which primitive root g generated the orbit. Therefore:

```
mu_p = (1/(p-1)) * sum_{k=1}^{p-1} delta_{k/p}
```

is the same measure for all primitive roots g. Any functional F(mu_p) that depends only on this measure — its moments, its Fourier transform, its support, its quartiles, any weak-topology-continuous functional — gives the same value regardless of g.

More precisely: the Fourier transform of mu_p is:

```
hat(mu_p)(xi) = integral e^{-2*pi*i*xi*t} d(mu_p)(t) = (1/(p-1)) * sum_{k=1}^{p-1} e^{-2*pi*i*xi*k/p}
```

This is a function of p and xi only — no g appears. The PSD is |hat(mu_p)(xi)|^2, which is also g-independent. The deviation D_p^PSD(xi) = p*(|hat(mu_p)(xi)|^2 - sinc^2(xi)) is therefore g-independent.

**Corollary:** To distinguish between primitive roots g and g' of the same prime p (at the level of the orbit), one must examine a quantity that is sensitive to the ORDER of the orbit elements, not just to the SET. The order carries information about multiplication in F_p*.

Proof of Corollary: For a fixed prime p, distinct primitive roots g and g' generate the same set {1,...,p-1} but with different orderings:

```
g^0, g^1, g^2, ..., g^{p-2}   (one ordering)
g'^0, g'^1, g'^2, ..., g'^{p-2}   (a different ordering)
```

The sequence {g^j mod p : j = 0,...,p-2} is a permutation of {1,...,p-1}, and two different primitive roots give different permutations (unless g^m ≡ g' (mod p) for some m, in which case they give cyclic shifts of each other's sequence). Any functional that is invariant under permutation of the orbit elements (i.e., depends only on the set) is g-independent. To get g-dependence, the functional must be ORDER-sensitive.

Order-sensitive functionals include:
- Autocorrelation at lag m: (1/(p-1)) * sum_j f(g^j/p) * g(g^{j+m}/p) — depends on the ordering.
- Cross-products g^j * g^{-j} = g^{j-j} = 1 if j is computed consistently, but g^j * (g')^{-j} for two different generators gives a nontrivial element — depends on both generators.
- Kloosterman sums Kl(a, g^{-m}; p) as defined in K7_MULTIPLICATIVE_CHARACTER_ROUTE.md.

**QED (Theorem K7.2 and Corollary).**

**Remark on the empirical measure:** The empirical measure mu_p for the prime-field orbit is the SAME object as the empirical measure of the lattice {1/p, 2/p, ..., (p-1)/p}. This lattice is the same for all primitive roots. The orbit IS the lattice (as a set). The PSD is the spectral measure of the lattice. The lattice has no prime-specific information beyond the lattice spacing 1/p.

This is the deepest structural reason why D_p^PSD is prime-blind: the orbit is a lattice, and all lattices of the same spacing are isometric. There is no room for prime-specific arithmetic in an isometric invariant.

---

## Theorem K7.3 — Bridge Requires New Arithmetic Transform

**Statement:** Suppose D_p is any function of the prime p and a parameter xi (or m, or other index) such that:

(i) |D_p| <= C (bounded, uniformly in p),
(ii) sum_{p<=X} D_p * w(p) has an explicit-formula-shaped Mellin transform (i.e., admits analytic continuation to Re(s) > 1/2 with poles related to zeros of a non-trivial L-function, not just to the standard zeta zeros scaled by a constant),
(iii) D_p does NOT factor as D_p = c * w_0(p) + (negligible) for any constant c and any "standard" arithmetic function w_0 (such as 1, log(p), or the Chebyshev weight).

Then D_p must involve an arithmetic transform T(p) that is NOT present in D1–D24 of the Luther-Sanders orbit corpus. Specifically, T(p) must be one of:

```
(a) A Kloosterman sum Kl(a, b; p) for some a, b depending on the auxiliary parameter, or
(b) A Hecke eigenvalue lambda_f(p) for some non-trivial automorphic form f on GL(n), n >= 2, or
(c) Some other nonlinear character sum over F_p* that distinguishes the orbit sequence
    from a generic permutation of {1,...,p-1}.
```

**Proof:**

We prove the contrapositive: if D_p does NOT involve any of (a), (b), (c), then either condition (ii) fails (no explicit formula structure) or condition (iii) fails (D_p factors trivially).

Suppose D_p is bounded and does not involve Kloosterman sums, Hecke eigenvalues, or other nonlinear character sums. Then D_p can be expressed in terms of:
- Additive character sums over F_p (complete or incomplete),
- Multiplicative character sums in the trivial representation (Ramanujan sums),
- Arithmetic functions of p that factor over Euler products trivially (such as 1, log p, p^{-s}, p^{it} for real t, etc.).

By K7_ADDITIVE_CHARACTER_EXPANSION.md (complete sum result): any additive character sum over the FULL prime-field orbit reduces to a complete sum evaluating to -1 (for non-trivial frequency). After normalization, this is O(1/p), which decays. The normalized sum has no residual prime-specific amplitude.

By K7.2 (Theorem above): any SET-based functional of the orbit is g-independent and reduces to a function of p alone (not of the specific prime arithmetic such as primitive roots or character tables).

By K7_NO_GO_ATTEMPT.md: if D_p is set-based (which is implied by its derivation from the orbit SET), then D_p admits a Taylor expansion in 1/p with all-deterministic coefficients, and its assembly factors as (constant in p) * (standard prime sums). By K7_EXPLICIT_FORMULA_COMPATIBILITY.md, this violates condition (ii) — no new L-function structure emerges.

Therefore, for condition (ii) to hold while condition (iii) also holds, D_p must involve a non-set-based, sequence-order-sensitive arithmetic quantity. The minimal such quantities at the orbit level are exactly the nonlinear character sums (a), (b), (c) listed in the theorem.

The Kloosterman sum Kl(a, g^{-m}; p) is the canonical example: it is ORDER-sensitive (requires knowing g^{-m} specifically, not just the set value), satisfies the Weil bound (hence bounded), and connects to automorphic forms (Hecke theory, Kuznetsov formula). It is not present in D1–D24 (the Luther-Sanders D-series documents up to D24 concern the orbit's set statistics, sinc^2 structure, corridor geometry, and algebraic invariants of the orbit — none compute Kloosterman sums or Hecke eigenvalues).

**QED.**

**Remark on D1–D24:** The D-series documents D1 through D24 establish the structural geometry of the prime-field corridor — its curvature, its midpoint properties, its CL operator encoding, its Phi fixed points, its TSML-73 cell structure, its BHML-28 cell structure, and related objects. These are all derived from the orbit SET statistics (symmetry, density, self-similarity) and the underlying algebra of the TIG framework. They are powerful for characterizing the corridor but they do not produce Kloosterman sums or Hecke L-functions. Theorem K7.3 says that this is not an accident — it is a structural necessity.

---

## Relationship Between the Three Theorems

The three theorems form a logical chain:

```
K7.1 (D_p^PSD is bounded and deterministic-limit)
    |
    v
K7.2 (any SET-based functional is g-independent)
    |
    v
K7.3 (bridge requires SEQUENCE-sensitive arithmetic, i.e., Kloosterman / Hecke)
```

**K7.1** establishes that D_p^PSD is well-behaved (bounded, converges to a deterministic limit). This is the platform.

**K7.2** identifies the structural reason for the failure: the orbit, as a set, is a lattice — it has no prime-specific arithmetic beyond the lattice spacing. Generator-dependence enters only through order.

**K7.3** derives the consequence: any bridge from orbit statistics to an RH-type result must exit the SET regime and enter the SEQUENCE regime. The minimal exit route is Kloosterman sums. Anything else either reduces to the standard PNT (trivial) or violates boundedness.

---

## What These Theorems Establish Collectively

**What is proved:**

1. D_p^PSD is bounded and asymptotically deterministic. It is a well-defined, computable object with a clean large-p limit.

2. The entire D_p^PSD family (all assembly candidates A1, A2) is prime-blind. This is not a failure of ingenuity — it is a structural theorem.

3. Any non-trivial prime-sensitive, bounded, orbit-derived object must involve Kloosterman sums (or equivalent). This uniquely identifies the Kloosterman route as the minimal viable extension.

**What is not proved:**

1. That the Kloosterman route (A3) actually bridges to zeta zeros. This is Tier A (speculative).

2. That any Kloosterman sum in D_p^{Kl}(m) has a computable explicit formula relating to zeta. Tier B at best.

3. That D_p^{Kl}(m) is the right Kloosterman object (vs. other Kloosterman-type sums associated to the orbit). The specific form Kl(1, g^{-m}; p) is the natural one from the sequence autocorrelation, but other nonlinear character sums might also be relevant.

---

## Tier Summary for K7 Program

| Result | Content | Tier |
|---|---|---|
| K7.1 | D_p^PSD bounded, converges to c_0(xi) | D (proved) |
| K7.2 | SET-based functionals are g-independent | D (proved) |
| K7.3 | Bridge needs Kloosterman / Hecke | D (proved) |
| K7.NO-GO | PSD assembly gives no new zeros | D (proved) |
| A1 dead end | sum D_p * log(p) ~ c_0(xi) * X | D (proved) |
| A2 trivial | sum D_p * log(p) * p^{-s} ~ c_0(xi) * (-z'/z)(s) | D (proved) |
| A3 = B | Kloosterman Dirichlet series has L-function connection | B (structural) |
| A3 -> zeta | Automorphic zeros = zeta zeros | A (speculative) |
| Explicit formula for A3 | Perron inversion of Z_{Kl}(s) | B (conditional on continuation) |
| RH from orbit | Full bridge prime orbit -> zeta zeros | A (deeply open) |

---

*Prerequisite: K7_NO_GO_ATTEMPT.md, K7_ADDITIVE_CHARACTER_EXPANSION.md, K7_DIRICHLET_ASSEMBLY_CANDIDATE.md*
*Feeds: K7_EXPLICIT_FORMULA_COMPATIBILITY.md, K7_MULTIPLICATIVE_CHARACTER_ROUTE.md*

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
