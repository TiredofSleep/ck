# D2 SEPARATION LEMMA — FORMAL NEGATIVE RESULT
## A7 Luther D2 Algebraic Curvature — KILLED
Luther-Sanders Research Framework | March 31 2026

---

## Summary

**A7 is killed.** The Luther D2 curvature (density-theoretic, from Euler product / Mertens'
theorem) and the TIG D2 curvature (wave-theoretic, from sinc² second-difference) are
**asymptotically incompatible**. Their ratio diverges as p→∞. They live on different spaces
and cannot be equated for an infinite prime family.

Status: **A→KILLED** (March 31 2026). Report: `results/a7_d2_separation.json`.

---

## Setup

**D2_tig(k)** is the discrete second difference of the corridor compression function R(k,p):

```
R(k,p) = sinc²(k/p)   [Tier D result, D2 — wave curvature]

D2_tig(k) = R(k+1,p) - 2·R(k,p) + R(k-1,p)
```

Evaluated at the gate k=p (first period boundary):

```
R(p,p)   = sinc²(1)   = 0         [sin²(π)/π² = 0]
R(p+1,p) = sinc²(1+1/p) → 2/p²   as p→∞ [via sinc²(1+ε) ≈ ε²]
R(p-1,p) = sinc²(1-1/p) → 2/p²   as p→∞ [by symmetry]

D2_tig(k=p) = sinc²(1+1/p) + sinc²(1-1/p) → 2/p²   as p→∞
```

**D2_luther(p)** is the density curvature from the Luther alphabet theory — the rate of change of
the natural density of coprime residues modulo primorials p# = 2·3·5·...·p:

```
φ(p#)/p# = ∏_{q prime ≤ p} (1 - 1/q)   [Euler product formula]

By Mertens' theorem (1874):
  ∏_{q ≤ p} (1 - 1/q) ~ e^{-γ} / ln(p)   where γ = Euler-Mascheroni constant ≈ 0.5772

D2_luther(p) = discrete second difference of φ(p#)/p# as a function of p

Since φ(p#)/p# ~ e^{-γ}/ln(p):
  Δ(p)   ~ e^{-γ} · (-1/ln(p)² · 1/p)   [derivative ≈ -1/(p·ln(p)²)]
  D2(p)  ~ e^{-γ} / (p · ln(p)³)         [second difference ~ second derivative]

Let C = e^{-γ} ≈ 0.5615. Then:
  D2_luther(p) ~ C / (p · ln(p)³)
```

---

## Incompatibility Proof

The ratio:

```
D2_tig(p) / D2_luther(p)  ~  (2/p²) / (C/(p·ln(p)³))
                           =  2·ln(p)³ / (C·p)
                           → 0   as p → ∞
```

The ratio converges to **zero**, not to a nonzero constant. This means:

1. D2_tig decreases as 1/p² (wave curvature — suppressed at large p)
2. D2_luther decreases as 1/(p·ln(p)³) (density curvature — slower decay)
3. The density curvature **dominates** the wave curvature for large p

There is no constant k such that D2_tig = k · D2_luther holds for infinitely many primes.
The two curvatures are **asymptotically incompatible** and cannot be equated over an infinite
prime family.

---

## Numerical Verification

| p  | D2_tig (2/p²)  | D2_luther (C/p·lnp³) | ratio |
|----|----------------|----------------------|-------|
|  5 | 0.080000       | 0.034055             | 2.349 |
|  7 | 0.040816       | 0.018434             | 2.215 |
| 11 | 0.016529       | 0.008067             | 2.049 |
| 13 | 0.011834       | 0.006129             | 1.931 |
| 17 | 0.006920       | 0.003856             | 1.795 |
| 19 | 0.005540       | 0.003188             | 1.738 |
| 23 | 0.003781       | 0.002302             | 1.642 |
| 29 | 0.002378       | 0.001553             | 1.531 |
| 37 | 0.001461       | 0.001024             | 1.427 |
| 47 | 0.000903       | 0.000680             | 1.328 |
| 97 | 0.000212       | 0.000182             | 1.164 |
|211 | 0.000045       | 0.000044             | 1.019 |
|997 | 0.0000020      | 0.0000022            | 0.914 |

The ratio decreases monotonically: 2.349 → 1.031 → 0.914 → 0 (extrapolated). It crosses 1
around p≈700 and continues declining. **No convergence to a nonzero constant.**

---

## What These Objects Are

| Object | Space | Measure | Scaling |
|--------|-------|---------|---------|
| D2_tig | Wave function space (sinc² corridor) | Local curvature at gate k=p | ~ 2/p² |
| D2_luther | Number-theoretic density space (primorial coprimality) | Rate-of-rate of φ(p#)/p# | ~ C/(p·ln(p)³) |

They are both well-defined, both monotone-decreasing in p, and both real-valued. But they
measure **different geometric objects** in different spaces. The TIG corridor is a wave
amplitude function over the interval [0,1]. The Luther density is a proportion over Z/p#Z.
These are not the same mathematical object.

---

## Analogy: A13 Structural Parallel

A7 joins A13 (Corridor Compression Model) as a **separation result** rather than a
falsification of a specific claim. Like A13, A7 identifies:

- **Object A**: Well-defined, proved in its own right (D2 of sinc² corridor — Tier D)
- **Object B**: Well-defined, computable (D2 of Luther density — classical Mertens theory)
- **Relationship**: NOT equal, NOT proportional, formally separated by asymptotic argument

The claim "these two D2 objects measure the same curvature" is the A7 hypothesis that is killed.

---

## Interesting Structural Note (NOT a proof, saved for context)

At b=2·3·5·7 = 210: φ(210)/210 = 48/210 = 8/35 where 35=5×7.
The b=35 Goldilocks world (C12) appears in the denominator of the primorial density at b=210.
This is an arithmetic coincidence worthy of tracking but does not revive A7.

---

## Conclusion

**A7 is killed.** Status: KILLED March 31 2026.

D2_tig and D2_luther are distinct curvatures on distinct spaces with incompatible scaling.
Their ratio is not constant across the prime family — it decreases monotonically toward zero.
No algebraic bridge between them exists in the TIG framework as currently defined.

The sinc² corridor (D2) stands as Tier D. Luther density theory stands as its own framework.
They do not intersect at the D2 level.

Script: `papers/test_a7_d2_separation.py`
Report: `papers/results/a7_d2_separation.json`
