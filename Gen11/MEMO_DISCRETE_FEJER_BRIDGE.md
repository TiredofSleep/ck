# Discrete Fejér Bridge Memo
## Level 0 → Level 1: Can First-G bypass the GRH step?
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## The Gap in the Chain

The RH bridge chain is:
```
First-G (proved) → Fejér kernel (proved) → sinc² limit (proved)
→ Montgomery R₂(u)=1−sinc²(u)  ← GRH STEP (conditional)
→ GUE β=2 class (numerically confirmed)
→ Locking ρ≈1 (measured, consistent with theoretical GUE)
```

The GRH step is: Montgomery used the Fejér kernel in the CONTINUUM LIMIT
(the function j_F(α) = max{1−|α|, 0}) to prove R₂(u) = 1 − sinc²(u) under GRH.

**The discrete First-G is at finite k.** R(k, f) = F_k(f)/k where F_k is the
discrete Fejér kernel of order k. This is the LEVEL 0 machine. Montgomery's proof
requires the LIMIT k → ∞.

**The question:** Can R(k, f) — the finite-k First-G — appear in a non-GRH proof
of something about the zero-spacing distribution?

---

## What the Discrete Fejér Knows

R(k, f) = F_k(f)/k = sin²(πkf) / (k² sin²(πf))

This function has:
1. **Peak at f=0:** R(k,0) = 1 (all elements coprime at k=0)
2. **Zeroes at f=j/k for j=1,...,k−1:** R(k,j/k) = 0
3. **Decay rate:** R(k,f) ≈ sinc²(kf)/k as f → 0 (local to peak)
4. **Sum formula:** Σ_{f=1}^{b−1} R(k,f) = k−1 (from Fejér kernel sum)

The k-th zero of R(k,f) occurs at f = 1/k. In the RH context:
- f corresponds to the normalized zero spacing u = (γ_{n+1}−γ_n)×log(T)/(2π)
- The first zero of R(k,·) at f=1/k → u=1/k as k grows
- Level repulsion: R₂(u) = 1 − sinc²(u) has a quadratic zero at u=0
  corresponding to GUE level repulsion

**The discrete First-G has zeros at rational f = j/k, not at u=0.**
The GUE level repulsion at u=0 is a different kind of zero — a soft quadratic zero
of the pair-correlation, not a hard zero of the Fejér kernel.

---

## The Pre-Limit Connection Attempt

Can we connect R(k,f) to zero-spacing for FINITE k?

**Explicit formula approach.** The von Mangoldt explicit formula is:
```
ψ(x) = x − Σ_{ρ} x^ρ/ρ − log(2π) − ½log(1−x^{-2})
```
where the sum is over non-trivial zeros ρ = ½ + iγ. The pair-correlation sum is:
```
Σ_{γ, γ'} f(γ−γ') = (two-point explicit formula)
```

Montgomery's proof of R₂(u) = 1 − sinc²(u) uses the Fejér kernel as the TEST FUNCTION
f in this formula. The Fejér kernel is chosen because it is positive (non-negative) and
has a specific Fourier transform (the triangle function) that makes the sum tractable.

**Can the DISCRETE Fejér R(k,f) serve as a test function in the explicit formula?**

R(k,f) is NOT a smooth function — it has discontinuities in derivatives at the
zeros f = j/k. The standard theory requires smooth test functions with rapid decay.
A finite-k discretization of the Fejér kernel would require:
(a) Regularization of the kink singularities at f = j/k
(b) Proof that the regularized version inherits the sum identity Σ F_k = k−1

**Obstruction:** The natural regularization of R(k,f) for the explicit formula is
exactly the limit k→∞ of R(k,f) = sinc²(f) — recovering Montgomery's test function.
There is no finite-k intermediate that improves on the continuum Fejér.

---

## The Spectral Interpretation

There is another angle. The First-G quantity R(k,b) = |C(k,b)|/k measures
*what fraction of the first k integers are coprime to b*.

The Euler product analogy:
```
∏_{p | b} (1 − 1/p) = lim_{k→b} R(k,b)/1
```
(Mertens-type formula)

For b = a prime p: R(k,p)/1 = (k − ⌊k/p⌋) / k ≈ 1 − 1/p for large k.

The product ∏_{p≤N} (1−1/p) ≈ 1/(e^γ log N) (Mertens' theorem) — this IS the
density of primes up to N. The First-G at many scales simultaneously encodes the
prime density.

**If b = pq (semiprime):** The First-G at scale k tracks which numbers from 1 to k
are coprime to BOTH p and q. This is a joint sieve — the inclusion-exclusion for
two primes.

**Connection to pair-correlation:** The pair-correlation of zeros involves pairs
(γ_n, γ_m) weighted by log(γ/2π). The First-G at (k, pq) involves pairs (k, pq)
weighted by the Legendre symbol structure. This is a structural similarity, not
a formal identity.

---

## What Would Be Needed

For a DISCRETE FIRST-G → ZERO-SPACING bridge without GRH, we would need:

**Step 1.** Identify a quantity in the spectral theory of ζ(s) that is naturally
indexed by finite-k Fejér kernels (not just the k→∞ limit).

Candidate: The DISCRETE TRUNCATION of Montgomery's formula:
```
R₂^{(N)}(u) = (1/N) Σ_{1≤n≤N} (1+cos(2πu_n))  ← u_n = normalized zero spacing
```
This is the empirical pair-correlation. It converges to R₂(u) = 1−sinc²(u) as N→∞
(unconditionally, by equidistribution if zeros are GUE; conditionally by Montgomery).

**Step 2.** Show that R₂^{(N)}(u) is bounded below by R(k, N/k) for some k(N).

This would give: *zero-spacing statistics at finite N are controlled by the
discrete Fejér kernel at scale k(N)*.

No proof of Step 2 exists. It is a conjecture about the finite-N convergence rate
of the empirical pair-correlation to the GUE prediction.

**Step 3.** Show that the bound in Step 2 implies RH or some consequence.

This step is not formulated at all. The connection between pair-correlation bounds
and the location of zeros is indirect (through the explicit formula, which requires
GRH-type input).

---

## Current Status

The discrete Fejér bridge is:
- **Conceptually motivated:** First-G = Fejér kernel is proved; Fejér kernel IS the
  Montgomery test function (confirmed in arXiv:2501.14545). The chain is real.
- **Formally blocked at finite-k:** No finite-k extension of Montgomery's proof
  exists. The continuum limit k→∞ is required by the smoothness requirements of the
  explicit formula.
- **The gap is precisely named:** The gap between Level 0 (discrete First-G at finite k)
  and Level 1 (Montgomery's pair-correlation formula at k=∞) is exactly the question
  of whether the explicit formula can be run with a NON-SMOOTH finite-k test function.

**This is the specific open question for F1(b):**
Does there exist a finite-k version of the Montgomery pair-correlation argument that:
(i) Uses R(k,f) directly (or a regularization of it) as the test function
(ii) Does not require GRH or the narrow-strip condition
(iii) Gives a non-trivial bound on the zero-spacing distribution?

If yes: the First-G law gives a direct arithmetic-to-zero-spacing connection.
If no (as currently suspected): the discrete Fejér bridge dies at the continuum limit,
and the GRH conditionality is unavoidable.

---

## The Next Cycle

The recursive fractal cycle continues:

- Level 0: First-G R(k,b) discrete Fejér ← proved
- Level 1: Montgomery R₂(u) = 1−sinc²(u) ← GRH conditional
- Level 2: GUE β=2 class, locking ρ≈1 ← numerically confirmed
- Level 3: Equidistribution of (γ_n mod 1) ← unknown; would follow from GRH+zero-spacing

Level 3 is: are the fractional parts of γ_n×log(p)/2π equidistributed for each prime p?
This is the prime equidistribution condition, known as the "strong pair-correlation"
conjecture. It is stronger than Montgomery's result and would imply a much tighter
connection between primes and zeros.

If Level 3 is proved, it would give an unconditional statement connecting prime
arithmetic to zero-spacing. The First-G law (Level 0) would then connect to
zero-spacing through the chain: Level 0 → Level 1 (conditional) → Level 2
(numerical) → Level 3 (if proved).

**The full Level 3 bridge is the open question. This is where the work stands.**

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*See CLAY_FORMAL_RECORD.md, F1 open questions.*
