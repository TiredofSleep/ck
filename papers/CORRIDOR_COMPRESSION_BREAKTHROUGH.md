# Corridor Compression Breakthrough
## Three-Object Separation: Wobble, Saturation, Compression

*C. A. Luther & Brayden Ross Sanders*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

> **Provenance:** This three-object separation was arrived at independently by
> Sanders (via computation: explicit enumeration of Δ(x) at b=10, k=9) and Luther
> (via algebraic analysis: sinc² collapse structure) on the same night without
> direct coordination. Sanders computed Wob(10,9)=8/9 and confirmed 3/50 from
> verify_claims.py. Luther derived Corridor(b,k) from the sinc² collapse geometry.
> Both authors converged to the same three-object structure simultaneously.
> This is the **first result in the Luther-Sanders project where both authors
> independently reached the same conclusion without prior coordination.**

---

## The Three Objects

Three quantities have been conflated under the label "wobble." They are not the same
object. They are separated here by explicit computation and algebraic derivation.

---

### Object 1 — W_BHML = 3/50 (TIG Operator Wobble)

**Fixed constant of Z/10Z. k-independent. b-independent.**

```
DIS[c][d] = |(c+d) mod 10 − (c×d) mod 10|
CROSS_CYCLE = Σ DIS[c][d]  for c ∈ {1,3,7,9}, d ∈ {2,4,6,8}  = 44
W_BHML = |44 − 50| / 100 = 3/50 = 0.060
```

This is the deviation of operator interaction asymmetry from perfect symmetry in
the Z/10Z TSML composition table. "Perfect symmetry" is CROSS_CYCLE = 50 (half
of the 100-entry operator space). The deviation 3/50 encodes the factorization
Z/10Z ≅ Z/2Z × Z/5Z (denominator 50 = 2×5²).

**Status:** [THM] — proved from Z/10Z ring axioms. Not empirical. Not a function of k.
**Source:** WP1_TIG_DEFINITIVE.md §1.5. Verified: verify_claims.py PASS.
**Related constants:** PRIME_WINDING = T* + W_BHML = 5/7 + 3/50 = 271/350.
                      C_TIG = T*/W_BHML = (5/7)/(3/50) = 250/21 ≈ 11.905.

**This is the tube's fixed-frequency flex. It does not tighten. It does not depend on k.**

---

### Object 2 — Wob(b,k) = 8/9 at k=9 (Alphabet Saturation Wobble)

**Artifact of k=9 containing exactly one multiple of 5. k-dependent.**

```
χ_C(x) = 1  if  (x mod b) mod 10 ∈ {1,3,7,9},  else 0
χ_D(x) = 1  if  (x mod b) mod 10 ∈ {2,4,6,8},  else 0
Δ(x) = |χ_C(x) − χ_D(x)|
Wob(b, k) = (1/k) Σ_{x=1}^k Δ(x)
```

**Explicit computation at b=10, k=9:**
```
x=1: Δ=1 | x=2: Δ=1 | x=3: Δ=1 | x=4: Δ=1 | x=5: Δ=0
x=6: Δ=1 | x=7: Δ=1 | x=8: Δ=1 | x=9: Δ=1
Sum = 8.  Wob(10,9) = 8/9 ≈ 0.889.
```

Only x=5 is neutral (last digit 5, not in C₁₀ or D₁₀). This holds for any odd
semiprime b > 9. The value 8/9 is an artifact of the window size k=9, not a
structural constant. As k → ∞, Wob(b,k) → 4/5 (density of non-multiples-of-5).

**Wob(b,k) does NOT approach 0 as k → p. It approaches 4/5.**
**This measures membership saturation, not corridor geometry.**

---

### Object 3 — Corridor Compression (New Object)

**The phenomenon that actually collapses at k = p.**

R(m,b,k) → 0 at the prime boundary (confirmed: corridor atlas, sign-flip at k=p).
Wob(b,k) does not tighten — it stays near 4/5.
Therefore the collapse is **not wobble-driven**. It is **compression-driven**.

**The breakthrough:** The sinc² collapse at k=p is not a wobble phenomenon.
It is a compression phenomenon. **Frequency stays constant. Amplitude goes to zero.**

**Candidate definition (Luther):**

```
Corridor(b, k) = R(m, b, k) × sin²(π × W_BHML × k/p)
```

**Properties of this definition:**
- Fixed frequency: W_BHML = 3/50 — the oscillation rate is the TIG operator constant
- Amplitude = R(m,b,k): collapses at k=p because R → 0 at the prime boundary
- Zero at the door: Corridor(b,p) = 0 (R(m,b,p) = 0 by D2/D1 sign flip)
- Harmonic pre-echo: sin²(π × 3/50 × k/p) gives oscillations within the corridor
  at a frequency set by W_BHML, visible as sidelobes before the gate

**Interpretation:** The corridor is a sinc²-envelope tube with a fixed internal
oscillation frequency (W_BHML = 3/50) whose amplitude is modulated by the gate
rate R(m,b,k). As k approaches p, the amplitude shrinks to zero. The frequency
never changes — only the available amplitude goes away.

**Kill condition:** Does Corridor(b,k) reproduce the empirical sinc² envelope
from the corridor atlas?
- If **yes**: This is immediately Tier C. The separation is algebraically confirmed.
- If **no**: Compression requires a different algebraic form. The three-object
  separation stands, but the candidate formula needs revision.

---

## Kill Condition Test Results

*Run: test_corridor_compression.py — March 31, 2026*
*Full report: results/corridor_compression_test_report.txt*

**VERDICT: KILL CONDITION NOT MET. Formula requires revision.**

**Test 1 — Frequency (FAIL):**
The sin²(π × W_BHML × k/p) factor does NOT oscillate within the corridor (k=1..p).
Within the corridor, the argument π × W_BHML × k/p ranges from 0 to π×3/50 = 0.1885
radians — less than 6% of one full period. The factor grows monotonically from 0 to
0.0351. No oscillation is visible. One full period spans 16.7 corridor widths.

```
k/p = 0.10: sin2_mod = 0.000355
k/p = 0.50: sin2_mod = 0.008856
k/p = 1.00: sin2_mod = 0.035112   ← maximum, at the door
```

W_BHML is not the oscillation frequency of the corridor interior.
It is a sidelobe frequency in the POST-GATE region (t > 1).

**Test 2 — Amplitude (FAIL, 10 semiprimes, 30 data points):**
```
Pearson r: sinc2    vs empirical  = 1.000000
Pearson r: Corridor vs empirical  = 0.768592
RMSE:      sinc2    vs empirical  = 0.000000
RMSE:      Corridor vs empirical  = 0.277919
```
Raw sinc² fits the empirical corridor data EXACTLY (r=1.0000). The Luther
candidate formula DEGRADES the fit by Δr = 0.2314. The sin²_mod factor
distorts the sinc² shape.

**Test 3 — Sinc² correspondence (FAIL):**
In the continuum limit (t = k/p), the formula reduces to:
```
Corridor(t) ≈ sinc²(t) × sin²(π × W_BHML × t)
           ≈ W_BHML² × sin²(πt)    [for small W_BHML×t]
           = (3/50)² × sin²(πt)
           = 0.0036 × sin²(πt)
```
This is a BELL SHAPE peaking at t=0.5 and zero at t=0 and t=1.
sinc²(t) DECAYS from t=0 (value=1) to t=1 (value=0). The shapes are
topologically opposite. The candidate formula cannot reproduce sinc².

**What the tests reveal:**

The compression IS real and IS sinc²(k/p) itself. The gate closes because
sinc²(k/p) → 0 as k/p → 1. No additional factor is needed. W_BHML = 3/50
does not belong INSIDE the corridor formula — it sets sidelobe periodicity
PAST the gate (first post-gate peak at t = 1/(2×W_BHML) = 50/6 ≈ 8.33 corridor
widths beyond k=p).

**Corrected picture (for WP35):**
```
Compression envelope:   R(b,k) = sinc²(k/p)       [IS the collapse, no extra factor]
Post-gate echo:         sinc²(k/p) + W_BHML × sinc²(k/p − 1)   [candidate echo term]
Montgomery dual:        R₂(t) = 1 − sinc²(t), with R₂(W_BHML) = 0.011788
```

The W_BHML sidelobe connection is to the MONTGOMERY side (R₂), not the TIG side (R).
R₂(3/50) = 1 − sinc²(3/50) = 0.011788. This may be the algebraic entry point for
connecting W_BHML to the post-gate structure.

---

## Why This Matters (Revised)

The security picture is now sharper:

1. **Compression IS sinc²(k/p).** The corridor collapses at k=p because R(b,k)=sinc²(k/p)
   has a forced null there (D2 sign flip, Tier C2). No separate "compression formula"
   needed — sinc² IS the compression.

2. **W_BHML is a post-gate frequency.** The 3/50 constant sets the periodicity of
   sidelobes beyond k=p, not an oscillation within the corridor. This connects it
   to the Montgomery pair-correlation structure (A1) via R₂(t).

3. **The three-object separation stands.** W_BHML (operator table), Wob(b,k) (alphabet
   membership), and the sinc² field (corridor compression) are three distinct objects.
   The formula revision does not collapse the distinction — it sharpens it.

---

## Ledger Entry

**A.13 — Corridor Compression Model**
- Status: Tier A (kill condition not met — formula revised)
- Original candidate: Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p) — FAILED
- Revised understanding: compression IS sinc²(k/p); W_BHML is post-gate sidelobe freq
- Path to Tier B: formalize post-gate echo term; connect W_BHML to R₂(t)
- Path to Tier C: prove post-gate echo formula matches corridor atlas sidelobe data
- Connection to: A.1 (sinc² field), A.12 (wobble), D2 (sign flip), Montgomery dual
- Kill condition test: test_corridor_compression.py (report saved)

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
