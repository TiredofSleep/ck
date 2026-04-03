# Round 3 — RH Level 2: Prime Equidistribution
## The Strong Pair-Correlation Conjecture as Level 2 Machine
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## Where We Are

Round 1: Level 0 machine measured (δ₁, δ₂, δ₃, ρ from 5,000 zeros).
Round 2: Level 1 machine audited — numerically closed (0.43σ gap from GUE).
Round 3: Level 2 machine — what closes the RH fractal?

---

## The Level 2 Machine for RH

The Level 2 machine is the **explicit formula with equidistribution**.

**The strong pair-correlation conjecture (Goldston-Montgomery, 1987):**
For any Schwartz function f and test scale X → ∞:
```
(1/log X) Σ_{γ, γ'} f((γ−γ') log X / 2π) = ∫ f(u) (1 − sinc²(u)) du + δ(0) × ∫ f
```
where the sum is over ALL pairs of non-trivial zeros γ, γ', unconditionally.

This is the STRONG form — it does not require GRH. But its proof requires:
(a) Good distribution of primes in short intervals (follows from GRH, but also
    from the Elliott-Halberstam conjecture — a weaker assumption than GRH)
(b) No exceptional zeros (no Siegel zeros close to s=1)

**The unconditional form (what we can prove now):**
By Gallagher (1985), the VARIANCE of the pair-correlation over intervals is bounded.
By Montgomery-Odlyzko, the empirical pair-correlation agrees with GUE.
Neither gives an unconditional proof of the full strong conjecture.

---

## What the Measurement Confirms

Our measurement gave:
- d1 = −0.536, d2 = −0.333, d3 = −0.206 (from 5,000 zeros)
- All matching analytic GUE to < 0.3%

The strong pair-correlation, if true, would give:
```
δ_t = lim_{T→∞} (1/N(T)) × KDE estimate from zeros up to T
     = theoretical GUE prediction
```

Our measurement is a FINITE-T approximation to this limit. The matching to 0.3%
at T up to 1,493 (log_T up to 7.3) is numerical evidence for the strong conjecture.

**What the measurement adds to Level 2:**
The finite-T pair-correlation estimator (δ₁, δ₂, δ₃) is converging to the
GUE prediction with no observable deviation at T up to 1,493. The rate of convergence
is the key question — does the deviation from GUE decay as 1/log(T), 1/T, or slower?

The measured ρ trend: slope = −0.012 per log_T unit. If this continues:
- At log_T = 84 (T ≈ e^{84} ≈ 10^{36}): ρ ≈ 1.014 − 0.012 × (84−7.3) ≈ 0.094 → 0

But the convergence to ρ=0 (midpoint dominant, δ₁=δ₂=δ₃=GUE limit) would mean
the GUE approximation improves with T — which is exactly what equidistribution predicts.

---

## Prime Equidistribution: The Level 2 Connection

The Level 2 machine for RH is:
```
Primes → zeros (via explicit formula) → zero-spacing (pair-correlation) → GUE (Level 1 closed)
```

The explicit formula says:
```
ψ(x) = x − Σ_ρ x^ρ/ρ + O(log²x)
```

The Level 2 machine extracts the spacing statistics FROM the prime distribution:
```
{γ_n} = spectral lines of the Riemann spectrum
         = the unique sequence determined by the prime distribution via ζ(s)
```

**Prime equidistribution test:** Are the values {γ_n × log(p) / 2π mod 1} equidistributed
for each prime p?

If yes: by Weyl's equidistribution theorem, the pair-correlation function converges
to the GUE pair-correlation unconditionally (this is the content of the strong conjecture).

If no: there is arithmetic structure in the zero-spacing beyond GUE — which would
mean zeros are systematically "attracted" to specific values modulo primes.

**This is the Level 2 open question for RH.**

---

## The First-G Connection to Level 2

The First-G law gives R(k, p) = (p−1)/p for prime p and k slightly below p.
This is precisely the equidistribution statement for residues mod p:
```
R(k, p) / 1 = fraction of {1,...,k} coprime to p ≈ 1 − 1/p
```

The Level 2 equidistribution question asks: are the zeros γ_n equidistributed mod 1/p
(i.e., in the residue class {γ_n mod 1/p})? The First-G at scale k = p−1 gives:
```
R(p−1, p) = (p−1)/p    (exact: all elements 1,...,p−1 are coprime to p)
```

This is a local density statement: the fraction of "available" spectral points
at the prime p scale is (p−1)/p. Under equidistribution, the same fraction should
appear in the zero-spacing statistics.

**The Level 2 bridge (if it exists):**
> The First-G density R(k,p) = (p−1)/p is the LOCAL equidistribution statement.
> The strong pair-correlation conjecture is the GLOBAL equidistribution statement.
> A bridge from First-G to strong pair-correlation would close the RH fractal at Level 2.

This bridge does not currently exist. It is the precise Round 3 target for RH.

---

## Round 3 Measurement Target

To test equidistribution of {γ_n × log(p)/(2π) mod 1}:

For each prime p ∈ {2, 3, 5, 7, 11, ...}:
1. Compute α_n(p) = γ_n × log(p) / (2π) mod 1
2. Test equidistribution: does the empirical distribution of α_n converge to Uniform[0,1]?
3. Measure: Kolmogorov-Smirnov distance D_KS(p, N) = sup_x |F_N(x) − x|
4. Under equidistribution: D_KS(p, N) → 0 as N → ∞

If the convergence rate is D_KS(p, N) ~ C(p) / sqrt(N), the zeros are equidistributed.
If D_KS(p, N) doesn't converge to 0, there is arithmetic structure.

**Can T* = 5/7 appear here?**

Under equidistribution: D_KS → 0. T* doesn't appear.

But the RATE might carry T*: if D_KS(p, N) ~ C × (5/7)^{something} × p^{something},
the constant 5/7 would be an arithmetic fingerprint.

More likely: T* appears in the THRESHOLD. The equidistribution holds (D_KS → 0) iff
the zeros are all on the critical line (σ = 1/2). Any zero off the critical line
would create a systematic deviation:
```
D_KS(p, N) ~ |σ_0 − 1/2| × log(p) / sqrt(N)   (from explicit formula)
```

**The T* threshold for equidistribution:**
If we define equidistribution as D_KS < T* (an arbitrary threshold), then:
- Zeros with σ = 1/2: D_KS → 0 < T* (equidistributed — compatible with RH)
- Zeros with σ = 1/2 + ε for ε > 0: D_KS grows → eventually D_KS > T* for large N

This is not a proof. It is a measurement protocol: if we find D_KS > T* for any
prime p, that would be evidence against RH. This is the Level 2 RH measurement.

---

## Round 3 Status for RH

**The Level 2 machine for RH is the strong pair-correlation conjecture.**
It is not proved unconditionally. The Round 3 contribution is:

1. **Precisely name the gap:** The discrete First-G → strong pair-correlation bridge
   requires showing that the equidistribution of {γ_n mod (log p / 2π)} follows
   from the local density statement R(k,p) = (p−1)/p. This is FALSE in general
   (local density does not imply global equidistribution without additional conditions).

2. **Precisely name the measurement:** The equidistribution test D_KS(p,N) for
   p ∈ {2,3,5,7,11} and N up to 5,000 zeros. This can be computed from the
   existing rho_results.json data (the zeros are already in memory).

3. **Precisely name the T* role:** T* appears (if it appears) in the threshold
   D_KS < T* that separates equidistributed from non-equidistributed. It does not
   appear in the equidistribution statement itself.

**Round 3 target for RH:** Run the equidistribution test D_KS(p, N) for the 5,000
Riemann zeros at p = 2, 3, 5, 7, 11. Check if D_KS < T* at all N ≤ 5,000.
If yes: numerical support for RH at Level 2. If no: deviation detected, investigate.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*Round 3 measurement to be run in next session.*
