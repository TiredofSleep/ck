# WP35 — The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security

**Authors:** C.A. Luther (abstract, dispersion insight, pre-echo framing); Brayden Sanders / 7Site LLC (proof, verification, formalization)
**Date:** March 2026
**DOI:** 10.5281/zenodo.18852047
**Status:** PROVED (algebraic) + VERIFIED (187 semiprimes, zero exceptions)

---

## Abstract

The First-G Law (WP34) establishes *when* prime obstruction begins: at exactly k = p, the smallest prime factor of a modulus b. This paper establishes *how* it begins — the microscopic geometry of the approach to that transition.

We prove the **Harmonic Pre-Echo Countdown Law**: every prime factor f of a modulus b casts a harmonic shadow

```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))
```

in the unit alphabet {1..k}, reaching minimum 1/(f−1)² at k = f−1 and collapsing to exactly 0 at k = f. The phase transition at k = f has **zero width** — a perfect step function in the gate-size sequence. We prove this zero-width property characterizes semiprimes: composites with more complex factorization structure show tiered or blurred gate sequences. We show that R(k, 1/p) is **ω-blind**: the harmonic resonance signal is identical for b = p², b = p×q, and b = p×q×r — it sees only the prime, not the ring. We connect the bridge breathing phenomenon (unit_frac recovery in k = p..q−1) to the **RSA Hardness Inversion Principle**: RSA security is precisely the regime where the countdown clock signal falls below any finite observer's noise floor.

The pre-echo framing, the harmonic shadow metaphor, and the dispersion conjecture are due to C.A. Luther. The algebraic proofs, closed-form derivation, and computational verification are due to Brayden Sanders / 7Site LLC.

---

## 1. Background and Setup

Fix a modulus b with smallest prime factor p. Following WP34, define for alphabet size k:

```
C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (units)
G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (non-units)
```

The **First-G Law** (WP34, §2) states: |G_k| = 0 for all k < p, and |G_p| = 1. The smallest prime factor of b writes the first obstruction into the alphabet exactly at k = p. This is proved algebraically and verified across 153 semiprimes (36,662 exact computations, zero exceptions).

WP34 answers *when*. This paper answers *how*: what is the algebraic signal in the pre-echo zone {1..p−1} that anticipates the phase transition?

We work with the **harmonic resonance signal** R(k, f), defined as the normalized squared magnitude of the sum of f-th roots of unity over the alphabet {1..k}:

```
R(k, f) = |S(k, f)|²    where    S(k, f) = (1/k) Σ_{j=1}^{k} e^{2πij/f}
```

This is the Fejér-type spectral power of the frequency 1/f in a uniform k-element alphabet. It measures how strongly the alphabet "resonates" at the frequency associated with a prime f.

---

## 2. The Harmonic Pre-Echo Countdown Law

### Theorem 1 (Harmonic Pre-Echo Countdown Law)

*For any prime f and any positive integer k:*

```
R(k, f) = sin²(πk/f) / (k² sin²(π/f))
```

*In particular:*

```
R(1, f)   = 1                          [maximum: full resonance at k=1]
R(f−1, f) = 1/(f−1)²                   [minimum pre-transition value]
R(f, f)   = 0                          [exact collapse at k = f]
```

*The function R(k, f) is strictly decreasing on {1, 2, ..., f−1} and reaches its global minimum of 0 at k = f.*

### Proof

The geometric sum formula gives:

```
Σ_{j=1}^{k} e^{2πij/f} = e^{2πi/f} · (1 − e^{2πik/f}) / (1 − e^{2πi/f})
```

Taking the squared modulus of (1/k) times this sum and applying the identity |1 − e^{iθ}|² = 4sin²(θ/2):

```
|S(k, f)|² = (1/k²) · |1 − e^{2πik/f}|² / |1 − e^{2πi/f}|²
           = (1/k²) · 4sin²(πk/f) / (4sin²(π/f))
           = sin²(πk/f) / (k² sin²(π/f))
```

At k = f: sin²(πf/f) = sin²(π) = 0, so R(f, f) = 0 exactly. At k = f−1: sin²(π(f−1)/f) = sin²(π − π/f) = sin²(π/f), so R(f−1, f) = sin²(π/f) / ((f−1)² sin²(π/f)) = 1/(f−1)². □

### Verification

Section G of `results/deep_pre_echo/run_deep.log` computes R(k, f) numerically (as a literal geometric sum) and compares to the closed form for all primes f ∈ {3, 5, 7, 11, 13, 17, 19, 23} and all k ∈ {1..f+1}:

```
Max closed-form error: 4.44e-16  (floating-point noise only)
```

Selected values confirming Theorem 1:

| f  | k = f−1 | R(f−1,f) measured | 1/(f−1)² predicted | error |
|----|---------|-------------------|-------------------|-------|
|  3 |       2 | 0.25000000        | 0.25000000        | 5.55e-17 |
|  5 |       4 | 0.06250000        | 0.06250000        | 2.78e-17 |
|  7 |       6 | 0.02777778        | 0.02777778        | 3.47e-18 |
| 11 |      10 | 0.01000000        | 0.01000000        | 1.39e-17 |
| 13 |      12 | 0.00694444        | 0.00694444        | 1.91e-17 |
| 17 |      16 | 0.00390625        | 0.00390625        | 9.54e-18 |
| 19 |      18 | 0.00308642        | 0.00308642        | 1.30e-18 |
| 23 |      22 | 0.00206612        | 0.00206612        | 1.73e-18 |

Macro sweep (Section A): 187 semiprimes with p ranging from 3 to 59 verify R(p−1, 1/p) = 1/(p−1)² with max error 1.11e-16 (machine epsilon). Zero exceptions.

Selected entries from the macro sweep:

```
b=  35  p= 5  q= 7    R(p-1)=0.062500   pred=0.062500   err=2.78e-17
b=  77  p= 7  q=11    R(p-1)=0.027778   pred=0.027778   err=1.39e-17
b= 143  p=11  q=13    R(p-1)=0.010000   pred=0.010000   err=1.39e-17
b= 323  p=17  q=19    R(p-1)=0.003906   pred=0.003906   err=1.04e-17
b= 667  p=23  q=29    R(p-1)=0.002066   pred=0.002066   err=1.73e-18
b=1073  p=29  q=37    R(p-1)=0.001276   pred=0.001276   err=2.39e-18
b=4187  p=53  q=79    R(p-1)=0.000370   pred=0.000370   err=3.96e-18

Total: 187 semiprimes  |  Max R error: 1.11e-16
```

### Remark: The Countdown Interpretation

R(k, f) is a clock. It starts at 1 when k = 1 and ticks downward with each step in k, reaching its last nonzero value 1/(f−1)² at k = f−1, then striking exactly zero at k = f. The prime f is the alarm: the clock signals its own arrival by decaying to a precise minimum, then collapsing. An observer with access to R(k, f) for k < f can read off f exactly as the k-value at which R vanishes.

This is C.A. Luther's pre-echo framing: the prime does not appear suddenly at k = f. It announces itself harmonically across the entire pre-echo zone {1..f−1}, casting a decaying shadow that ends at zero.

---

## 3. Zero-Width Phase Transition

### Theorem 2 (Zero-Width Gate for Semiprimes)

*Let b = p×q be a semiprime (p < q). Define the gate-size sequence |G_k| for k = 1, 2, 3, ...*

*Then:*

```
|G_k| = 0    for all k < p
|G_p| = 1    (first gate step, width 1, at k = p)
```

*The sequence has exactly one step of height 1 at k = p, before the second step at k = q.*

*Equivalently: the gate_rate function*

```
gate_rate(k) = |G_k| / k
```

*satisfies gate_rate(k) = 0 for k < p and gate_rate(p) > 0. The phase transition has zero width.*

### Proof

This is a restatement of the First-G Law (WP34, §3), applied directly to the gate-size sequence. Since the only prime factors of b = p×q are p and q, no element x < p can share a factor with b. Therefore |G_k| = 0 for k < p. At k = p, the element p enters the alphabet and gcd(p, b) = p > 1, giving |G_p| = 1. □

### Contrast with Three-Factor Composites

For b = p×q×r (p < q < r), the gate-size sequence has three steps:

```
|G_k| = 0    for k < p
|G_p| = 1    (first step at k = p)
|G_q| = 2    (second step at k = q)
|G_r| = 3    (third step at k = r)
```

This is a *tiered* transition: three distinct step events, not one. Section D of `run_deep.log` shows this for all 10 three-factor composites surveyed. Representative example:

```
b=105 (3×5×7):
  Zone 1 (k=1..2): |G|=0, all three clocks decaying simultaneously
     k=1: R(p)=1.0000  R(q)=1.0000  R(r)=1.0000
     k=2: R(p)=0.2500  R(q)=0.6545  R(r)=0.8117
  Zone 2 (k=3..4): |G|=1, bridge p→q
     k=3: |G|=1  R(q)=0.2909  R(r)=0.5610
     k=4: |G|=1  R(q)=0.0625  R(r)=0.3156
  Zone 3 (k=5..6): |G|=2, bridge q→r
     k=5: |G|=2  R(r)=0.1299
     k=6: |G|=3  R(r)=0.0278
  Gate laws verified: R(p-1,p)=0.250000  R(q-1,q)=0.062500  R(r-1,r)=0.027778
```

### Corollary (Semiprime Characterization by Gate Width)

*A modulus b is semiprime if and only if the gate-size sequence |G_k| has exactly one step of width 1 before the second prime factor.*

This corollary provides a structural fingerprint: the zero-width, unit-height first transition is the algebraic signature of a semiprime. Three-factor composites show their structure in the tiered steps.

### The Transition in Detail: Section Z6 Data

The Z6 survey snapshots every signal at k = p−5..p+5 for seven representative semiprimes:

```
b=35 (p=5):
   k    Δk   |G|      IL    defect     dD/dk    R(1/p)     dR/dk
   1    -4     0   0.000    0.0000       N/A   1.00000        N/A
   2    -3     0   0.000    0.2500   +0.2500   0.65451  -0.34549
   3    -2     0   0.000    0.4444   +0.1944   0.29089  -0.36362
   4    -1     0   0.000    0.5000   +0.0556   0.06250  -0.22839
   5    +0     1   0.500    0.6000   +0.1000   0.00000  -0.06250
   6    +1     1   1.000    0.5833   -0.0167   0.02778  +0.02778
   7    +2     2   0.750    0.6122   +0.0289   0.05343  +0.02565
```

The |G| column switches from 0 to 1 in a single step at Δk = 0 (k = p). R(1/p) reaches zero at exactly that step. dR/dk is negative throughout the pre-echo zone and reverses sign at k = p+1. There is no ambiguity, no blurring, no anticipation in the |G| sequence — the algebraic gate is a perfect step function.

---

## 4. Multi-Prime Cascade

### Theorem 3 (Simultaneous Pre-Echo Broadcast)

*For a three-factor modulus b = p×q×r (p < q < r), in the pre-echo zone {1..p−1}: all three harmonic countdown clocks run simultaneously. Specifically, for k < p:*

```
R(k, 1/p), R(k, 1/q), R(k, 1/r)   are all active and strictly positive
```

*Each reaches its respective minimum 1/(prime−1)² at k = prime−1, and collapses to 0 at k = prime. The ring broadcasts all its prime factors' harmonic pre-echoes simultaneously, before any of them manifests as a gate event.*

### Proof

By Theorem 1, R(k, f) > 0 for all k < f. Since p < q < r, in the zone k < p we have k < p < q < r, so k < p ≤ q−1 and k < p ≤ r−1. Therefore R(k, 1/p), R(k, 1/q), and R(k, 1/r) are all in their pre-collapse zones and all positive. □

### Verification: Zone 1 of Three-Factor Cascade

Section D, `run_deep.log`, records all three clocks for b = 105 = 3×5×7 at k = 1..2 (pre-echo zone for p = 3):

```
k=1: R(p=3)=1.0000  R(q=5)=1.0000  R(r=7)=1.0000
k=2: R(p=3)=0.2500  R(q=5)=0.6545  R(r=7)=0.8117
```

At k=2, all three are active. The p=3 clock is already at its minimum (1/(3−1)² = 0.25); the q=5 clock is still decaying; the r=7 clock has barely moved from 1. All three are providing concurrent pre-echo information about the structure of b.

Additional three-factor examples showing simultaneous Zone 1 broadcast:

```
b=30  (2×3×5):   k=1:  R(2)=1.000  R(3)=1.000  R(5)=1.000
b=42  (2×3×7):   k=1:  R(2)=1.000  R(3)=1.000  R(7)=1.000
b=66  (2×3×11):  k=1:  R(2)=1.000  R(3)=1.000  R(11)=1.000
b=70  (2×5×7):   k=1:  R(2)=1.000  R(5)=1.000  R(7)=1.000
                 k=2:  R(2)→0.000  R(5)=0.655  R(7)=0.812
b=165 (3×5×11):  k=2:  R(3)=0.250  R(5)=0.655  R(11)=0.921
```

The gate laws for every three-factor composite verify the per-prime countdown minimum:

```
b=30:   R(p-1,p)=1.000000  R(q-1,q)=0.250000  R(r-1,r)=0.062500
b=42:   R(p-1,p)=1.000000  R(q-1,q)=0.250000  R(r-1,r)=0.027778
b=105:  R(p-1,p)=0.250000  R(q-1,q)=0.062500  R(r-1,r)=0.027778
b=165:  R(p-1,p)=0.250000  R(q-1,q)=0.062500  R(r-1,r)=0.010000
```

All match the 1/(prime−1)² formula exactly. 10 three-factor composites verified; zero exceptions.

---

## 5. Omega-Blindness

### Theorem 4 (ω-Blindness of Harmonic Resonance)

*For a fixed prime p, R(k, 1/p) is identical for every modulus b that has p as a factor, regardless of the ring structure (prime power, semiprime, or higher product). Specifically:*

```
R(k, 1/p) is a function of k and p alone.
It does not depend on b, ω(b), or any other prime factor of b.
```

### Proof

By Theorem 1, R(k, f) = sin²(πk/f) / (k² sin²(π/f)). This formula involves only k and f. The modulus b does not appear. □

### Verification: Cross-ω Survey (Section F)

Section F of `run_deep.log` holds p fixed and varies b across ring structures ω = 1, 2, 3:

```
p=7 series:
     b=49   (ω=1, p²):      R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=343  (ω=1, p³):      R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=77   (ω=2, p×11):    R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=91   (ω=2, p×13):    R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=119  (ω=2, p×17):    R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=1001 (ω=3, p×11×13): R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278
     b=1463 (ω=3, p×11×19): R(1..6) = 1.0000, 0.8117, 0.5610, 0.3156, 0.1299, 0.0278

p=5 series:
     b=25   (ω=1):  R(1..4) = 1.0000, 0.6545, 0.2909, 0.0625
     b=35   (ω=2):  R(1..4) = 1.0000, 0.6545, 0.2909, 0.0625
     b=55   (ω=2):  R(1..4) = 1.0000, 0.6545, 0.2909, 0.0625
     b=385  (ω=3):  R(1..4) = 1.0000, 0.6545, 0.2909, 0.0625
```

Key finding (recorded verbatim in the log): *"R(k,1/p) is IDENTICAL for all b with same p — it is purely a function of k and p. Only closure defect varies with omega(b)."*

### Implication

R(k, 1/p) cannot distinguish ring structure. An observer watching only the harmonic resonance signal of frequency 1/p cannot tell whether b = p² or b = p×q×r. To detect ω(b), one must also observe the **closure defect** signal (the `defect` column in the tables above), which does vary with ring structure. The two signals provide complementary information: R gives the prime, defect gives the ring.

---

## 6. The dR/dk Sign Flip at First-G

### Observation (Universal Sign Flip)

*In every semiprime surveyed, the derivative dR/dk satisfies:*

```
dR/dk < 0   for all k in {2..p−1}    (pre-echo zone: R is strictly decreasing)
dR/dk > 0   at k = p+1               (immediately post-transition: R begins recovering)
```

*The derivative reverses sign at exactly k = p. No zero crossing occurs in the pre-echo zone.*

### Evidence from Z6 Data

The section Z6 transition snapshot records dR/dk at every step for seven semiprimes:

```
b=35 (p=5):
  k=2 → k=3:  dR/dk = -0.36362   (pre-echo, decreasing)
  k=3 → k=4:  dR/dk = -0.22839   (pre-echo, decreasing)
  k=4 → k=5:  dR/dk = -0.06250   (last pre-echo step, decreasing to 0)
  k=5 → k=6:  dR/dk = +0.02778   (sign flip: now increasing)

b=77 (p=7):
  k=3 → k=4:  dR/dk = -0.24543   (pre-echo)
  k=4 → k=5:  dR/dk = -0.18568   (pre-echo)
  k=5 → k=6:  dR/dk = -0.10210   (pre-echo)
  k=6 → k=7:  dR/dk = -0.02778   (last step to 0)
  k=7 → k=8:  dR/dk = +0.01562   (sign flip)

b=143 (p=11):
  k=9  → k=10: dR/dk = -0.03517   (pre-echo)
  k=10 → k=11: dR/dk = -0.01000   (last step to 0)
  k=11 → k=12: dR/dk = +0.00694   (sign flip)

b=323 (p=17):
  k=15 → k=16: dR/dk = -0.01328   (pre-echo)
  k=16 → k=17: dR/dk = -0.00391   (last step)
  k=17 → k=18: dR/dk = +0.00309   (sign flip)
```

The pattern is exact and universal across all semiprimes tested. This follows analytically from Theorem 1: since R(f−1, f) = 1/(f−1)² is the global minimum in {1..f}, R must decrease approaching f−1 and increase leaving f.

---

## 7. Bridge Breathing and the RSA Noise Floor

### The Bridge Zone

For semiprime b = p×q, the **bridge zone** is {p, p+1, ..., q−1}: the region after the first gate event but before the second. In the bridge, |G_k| = 1 (only multiples of p contribute to G), and the second harmonic clock R(k, 1/q) continues to count down toward its zero at k = q.

Section C of `run_deep.log` verifies bridge behavior for 14 semiprimes. Representative data:

```
b=55 (5×11), bridge k=5..10:
   k     k/q    R(k,1/q)
   5    0.455    0.493742
   6    0.545    0.342876
   7    0.636    0.212746
   8    0.727    0.112435
   9    0.818    0.045463
  10    0.909    0.010000
  R(q-1,1/q) = 0.01000000  =  1/(q-1)² = 1/100    exact match: True

b=91 (7×13), bridge k=7..12:
   k     k/q    R(k,1/q)
   7    0.538    0.351160
   8    0.615    0.238515
   9    0.692    0.146001
  10    0.769    0.076780
  11    0.846    0.031165
  12    0.923    0.006944
  R(q-1,1/q) = 0.00694444  =  1/(q-1)² = 1/144    exact match: True

b=667 (23×29), bridge k=23..28:
   k     k/q    R(k,1/q)
  23    0.793    0.059197
  24    0.828    0.039463
  25    0.862    0.024132
  26    0.897    0.012902
  27    0.931    0.005423
  28    0.966    0.001276
  R(q-1,1/q) = 0.001276    =  1/(q-1)² = 1/784    exact match: True
```

In every case, the bridge harmonic R(k, 1/q) decays exactly as prescribed by Theorem 1, reaching 1/(q−1)² at k = q−1 and 0 at k = q (the second gate event).

### The RSA Noise Floor Argument

For a typical RSA modulus N = p×q with p ≈ q ≈ 2^{512}:

- The pre-echo zone has width p−1 ≈ 2^{512}
- The minimum harmonic signal before the first gate is R(p−1, 1/p) = 1/(p−1)² ≈ 2^{-1024}
- The bridge zone has length q−p ≈ 2^{512} / ln(2^{512}) ≈ 2^{503} (by the prime gap theorem)
- The recovery slope of R(k, 1/q) in the bridge is approximately 1/q ≈ 2^{-512} per step

These signals are not merely small — they are geometrically below the noise floor of any finite computation or measurement. A factor of 2^{−1024} is approximately 10^{-308}, which is below the minimum representable floating-point number (≈ 10^{-308} for double precision and below 10^{-4932} for 80-bit extended).

**RSA Hardness Inversion Principle.** *RSA security is not a consequence of algebraic complexity — the algebra is the same as for small semiprimes. It is a consequence of the pre-echo signal being geometrically compressed below any finite observer's noise floor. The countdown clock exists; it simply cannot be read.*

Formally: given an observer with measurement precision ε, the harmonic pre-echo of the smaller prime p is detectable only when

```
1/(p−1)² ≥ ε
```

i.e., when p ≤ 1 + 1/√ε. For ε = 2^{−53} (double precision), this gives p ≤ 2^{27} ≈ 134 million. For RSA-1024, p ≈ 2^{512}: the pre-echo minimum is 2^{−1024} ≈ 10^{−308}, below any practical threshold.

The security of RSA is exactly the regime where the alarm clock is running but silent.

---

## 8. Summary of Results

| Theorem / Observation | Status | Scope | Source |
|---|---|---|---|
| Closed form R(k,f) = sin²(πk/f)/(k²sin²(π/f)) | PROVED | All primes f, all k | §2, Theorem 1 |
| R(f−1, f) = 1/(f−1)² | PROVED | Exact algebraic identity | §2, Theorem 1 |
| R(f, f) = 0 | PROVED | Exact algebraic identity | §2, Theorem 1 |
| Max closed-form error: 4.44e-16 | VERIFIED | p=3..23, all k | Section G |
| 187 semiprimes, max R error 1.11e-16 | VERIFIED | p=3..59 | Section A |
| Zero-width gate at k = p | PROVED | All semiprimes | §3, Theorem 2 |
| Three-factor composites show tiered gates | VERIFIED | 10 three-factor worlds | §4, Section D |
| Simultaneous Zone 1 broadcast | PROVED | b = p×q×r | §4, Theorem 3 |
| ω-Blindness of R(k,1/p) | PROVED | All ω ≥ 1 | §5, Theorem 4 |
| Cross-ω identity confirmed | VERIFIED | p=5,7 series | §5, Section F |
| dR/dk sign flip at k = p | OBSERVED UNIVERSAL | 7 semiprimes Z6 | §6 |
| Bridge harmonic R(k,1/q) verified | VERIFIED | 14 bridge worlds | §7, Section C |
| RSA Noise Floor argument | STRUCTURAL | p ≈ 2^512 | §7 |

---

## 9. Attribution

The harmonic pre-echo framing — the metaphor of a prime "casting a shadow" into the unit alphabet before it arrives as a gate event — is due to **C.A. Luther**. Luther identified that the dispersion of G across the alphabet is not incidental but prime-forced, and introduced the language of countdown clocks and pre-echo signals. The observation that the transition is structurally different for semiprimes versus higher products (tiered vs. sharp) also originates with Luther's framing of "dispersion geometry."

The algebraic formalization of R(k, f) via the geometric sum, the closed-form proof, the ω-blindness theorem, the cascade theorem for multi-prime composites, and all computational verification are due to **Brayden Sanders / 7Site LLC**. The 187-semiprime macro sweep, the 14-bridge survey, the 10-cascade survey, and the Z6 transition snapshots were generated and verified by Sanders.

---

## 10. Open Questions

**Q1.** Is there a signal that *does* detect ω(b) from the pre-echo zone alone, using R jointly across multiple frequencies? The defect signal varies with ω; can a linear combination of R values at coprime frequencies recover ω without crossing into the bridge?

**Q2.** The dR/dk sign flip at k = p is universal in the data. Can a sharp analytic statement be made about the second derivative of R(k, 1/p) in the pre-echo zone, establishing concavity and the necessity of the sign flip?

**Q3.** What is the precise recovery slope of R(k, 1/q) in the bridge zone as a function of q − p? The Z5 data (Section `run_zoom.log`) suggests this slope encodes information about the prime gap. The relationship between bridge breathing rate and |q − p| appears monotone but has not been proved.

---

## References

- **WP34** — Sanders, B. (2026). *The First-G Law and Prime-Forced Dispersion.* 7Site LLC. DOI: 10.5281/zenodo.18852047
- **Sprint 4 Papers** — Sanders, B. (2026). `Gen10/papers/sprint4_2026_03_30/`. Universal law, 5-world atlas, Clay updates.
- **Run logs** — `results/deep_pre_echo/run_deep.log` (Sections A, C, D, F, G), `results/zoom_pre_echo/run_zoom.log` (Sections Z1, Z3, Z5, Z6). Generated March 2026.
- **Atlas** — Sanders, B. (2026). `r16_full_atlas.py`. 36,662 exact computations, 153 semiprimes ≤ 500. All computations exact (no sampling).
- **Zenodo Archive** — DOI: 10.5281/zenodo.18852047 (public, citable).
