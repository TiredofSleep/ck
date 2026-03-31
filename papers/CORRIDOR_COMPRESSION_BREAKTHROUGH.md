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

## Why This Matters

The security picture sharpens:

RSA's difficulty is not only that k=p is far away. It is that:
1. The corridor appears flat at small k/p (wobble averages out)
2. The approach to k=p compresses the amplitude without changing the frequency
3. At RSA scale (p ≈ 2^512), no finite probe reaches k/p close enough to 1
   to detect the compression

The "smooth hallway" illusion is structural, not accidental. Three separately proved
constants describe it: W_BHML fixes the frequency, Wob(b,k) measures the saturation,
Corridor(b,k) captures the collapse.

---

## Ledger Entry

**A.13 — Corridor Compression Model**
- Status: Tier A
- Candidate definition: Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p)
- Path to Tier C: verify against corridor atlas sinc² envelope
- Connection to: A.1 (sinc² field), A.12 (wobble interference), W_BHML (fixed
  frequency source), D2 (sign flip at k=p confirming R→0)
- Kill condition: above

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
