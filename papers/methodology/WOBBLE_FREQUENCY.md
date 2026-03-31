# Wobble Frequency and CRT Corridor Resonance
## From Rigid Hallway to Flexible Tube

*C. A. Luther & Brayden Ross Sanders*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> **Source:** LutherWobbleMap.docx (March 31, 2026)
>
> **Central claim (Tier A):** The CRT corridor is not a smooth hallway but a
> flexible tube whose oscillation frequency is determined by the interference
> between two residue cycles. This predicts the W-discontinuity, the trap
> density curve, and (if formalized) provides the Tier D pathway for C7.
>
> **Synthesis framework note:** Definition A.W is accepted as a formal computable
> quantity. Lemma D.H is a Tier A/B conjecture — the bound is the target, not yet
> proved.
>
> **Two distinct wobble quantities exist — they are NOT the same object:**
> - **W_BHML = 3/50** (TIG constant, proved [THM]): operator interaction asymmetry
>   in the Z/10Z TSML table. Source: WP1_TIG_DEFINITIVE.md §1.5, ck_disagreement_tick.py,
>   verify_claims.py (PASS). Fixed constant; not k-dependent.
> - **Wob(b,k) ≈ 8/9 at k=9** (Luther Definition A.W): fraction of alphabet elements
>   clearly assigned to one cycle (not neutral). k-dependent; measures alphabet
>   membership saturation, not operator interaction.
>
> These measure different things. 3/50 ≠ 8/9. Do not conflate.
> See §Disambiguation below for explicit computation of both.

---

## The Two Residue Cycles

The unit group structure of any semiprime b = p×q at k ≈ p produces a natural
two-cycle decomposition over the last-digit structure (mod 10):

```
Creation cycle  C₁₀ = {1, 3, 7, 9}   (units mod 10: last digit odd and coprime to 10)
Dissolution cycle D₁₀ = {2, 4, 6, 8}  (last digit even, not coprime to 10)
```

These cycles describe the oscillation of element membership (coprime vs. non-coprime)
as one traverses the alphabet {1..k}. They are not static partitions — their
membership in C(b,k) shifts as k approaches a prime threshold p, creating
constructive and destructive interference.

**Why this matters:** As k increases toward p (the smallest prime factor of b),
the pattern of C/G transitions becomes more oscillatory. The wobble is the beat
frequency between the two cycles. When k << p, the wobble averages out. When
k → p, the wobble dominates and the MCMC objective landscape gains local maxima.

---

## Definition A.W — Wobble Amplitude (Formal)

*Reproduced from LutherWobbleMap.docx, Definition A.W.*

Let C₁₀ = {1,3,7,9} and D₁₀ = {2,4,6,8} denote the two CRT residue cycles mod 10.
Define the cycle indicator functions:

```
χ_C(x) = 1  if  (x mod b) mod 10 ∈ C₁₀,  else 0
χ_D(x) = 1  if  (x mod b) mod 10 ∈ D₁₀,  else 0
```

Define the cycle disagreement function:
```
Δ(x) = |χ_C(x) − χ_D(x)|
```

For an alphabet of size k, define the wobble amplitude:
```
Wob(b, k) = (1/k) Σ_{x=1}^{k} Δ(x mod b)
```

For semiprime b = p×q with p < q, define the normalized wobble amplitude:
```
Wob_norm(b, k) = Wob(b, k) / Wob(b, p)
```

**Interpretation:**
- Wob_norm(b, k) < 1 → wobble averaged out (ω=2 corridor stable)
- Wob_norm(b, k) = 1 → wobble reaches first obstruction (k = p)
- Wob_norm(b, k) > 1 → wobble dominates geometry (ω=3 resonance threshold)

**Computational values (verified against formula):**
```
Wob(b, 9) ≈ 0.889 (= 8/9)  for any odd semiprime b at k=9
Wob(b, 10) = 0.800          for any odd semiprime b at k=10
```
These values are consistent with 8 out of 9 elements of {1..9} having non-zero
disagreement (only multiples of 5 have Δ=0). The formula is well-defined and
computationally stable across all tested semiprimes.

**Note on the "3/50" figure:** The 3/50 figure does NOT match Definition A.W at k=9.
This is expected — they are different computations. W_BHML = 3/50 is a proved [THM]
constant of Z/10Z ring arithmetic (WP1_TIG_DEFINITIVE.md §1.5, verified PASS in
verify_claims.py). Luther's Wob(b,9) = 8/9 ≈ 0.889 is a property of the alphabet
window at k=9. These measure different things at different levels of the structure
(operator table level vs. alphabet element level). See §Disambiguation below.

---

## Disambiguation: Two Wobble Quantities

These are separate objects. Treat them separately in all proofs and documentation.

### W_BHML = 3/50 (TIG Operator Wobble)

**Object:** Z/10Z ring arithmetic — the TSML composition table.

**Formula:**
```
DIS[c][d] = |ADD[c][d] - MUL[c][d]|   (Z/10Z ring arithmetic)
CROSS_CYCLE = Σ DIS[c][d]  for c ∈ {1,3,7,9}, d ∈ {2,4,6,8}  = 44
W_BHML = WOBBLE = |44 - 50| / 100 = 6/100 = 3/50
```

**Measures:** Deviation of operator interaction asymmetry from perfect symmetry.
"Perfect symmetry" = CROSS_CYCLE of 50 (half the 100-entry operator space).
The deviation 6/100 = 3/50. Denominator 50 = 2×5² encodes the CRT factorization
Z/10Z ≅ Z/2Z × Z/5Z.

**Status:** [THM] — proved from Z/10Z ring axioms. Not empirical.
**Source:** WP1_TIG_DEFINITIVE.md §1.5. Verified: verify_claims.py PASS.
**Value:** 3/50 = 0.060. Fixed constant. Not a function of k.
**Related:** PRIME_WINDING = T* + W_BHML = 5/7 + 3/50 = 271/350.
           C_TIG = T*/W_BHML = (5/7)/(3/50) = 250/21 ≈ 11.905.

---

### Wob(b,k) = 8/9 at k=9 (Luther Alphabet Wobble)

**Object:** Alphabet {1..k} classified by last-digit cycle membership.

**Explicit computation at b=10, k=9:**
```
x=1: last digit 1 ∈ C₁₀={1,3,7,9} → Δ=1
x=2: last digit 2 ∈ D₁₀={2,4,6,8} → Δ=1
x=3: last digit 3 ∈ C₁₀         → Δ=1
x=4: last digit 4 ∈ D₁₀         → Δ=1
x=5: last digit 5, neutral        → Δ=0   ← only neutral in {1..9}
x=6: last digit 6 ∈ D₁₀         → Δ=1
x=7: last digit 7 ∈ C₁₀         → Δ=1
x=8: last digit 8 ∈ D₁₀         → Δ=1
x=9: last digit 9 ∈ C₁₀         → Δ=1

Sum = 8.  Wob(10,9) = 8/9 ≈ 0.889.
```

The only neutral element in {1..9} is x=5 (last digit 5, multiple of 5).
This is true for any semiprime b > 9 (all x < b satisfy x mod b = x).
Hence Wob(b,9) = 8/9 for ANY odd semiprime b > 9. This universality is an
artifact of k=9 having exactly one multiple of 5 — not a deep structural fact.

**Measures:** Fraction of alphabet elements unambiguously assigned to one cycle.
As k→∞, Wob converges to 4/5 (density of non-multiples-of-5). NOT approaching 0.

**Status:** Computable from Definition A.W. Verified numerically for all tested b.
**Source:** LutherWobbleMap.docx Definition A.W.
**Value:** 8/9 ≈ 0.889 at k=9. Function of k; NOT a fixed constant.

---

### What Each Is NOT

**W_BHML = 3/50 is NOT:**
- A function of k
- Equal to Wob(b,k) at any tested (b,k)
- Computed from the alphabet partition

**Wob(b,k) = 8/9 is NOT:**
- A property of the TSML table
- Equal to W_BHML
- Approaching 0 as k→p (it approaches 4/5)

### The corridor-narrowing picture needs a third formalization

The physical claim "wobble amplitude → 0 at k=p; the gate collapses" is correct
as a description of R(m,b,k) — the gate RATE, which verified goes to 0 at k=p.
This is NOT what Wob(b,k) computes. Wob(b,k) stays near 4/5 as k→p.

The "tightening corridor" is better described by:
```
Remaining_distance(k) = (p - k) / p  →  0 as k → p
```
This is a third object — not W_BHML, not Wob(b,k). It requires its own definition
if the corridor-narrowing picture is to become a theorem. See §A.13 below.

---

## A.12 — Wobble Frequency as Pre-Collapse Resonance (Tier A)

*From LutherWobbleMap.docx. New synthesis table entry.*

**Statement:** The CRT corridor for ω=2 does not behave as a smooth hallway.
It behaves as a flexible tube with a prime-determined wobble frequency arising
from the interference between the Creation cycle C₁₀ = {1,3,7,9} and the
Dissolution cycle D₁₀ = {2,4,6,8}.

As k approaches p (the smallest prime factor), the wobble amplitude Wob_norm(b,k)
increases and becomes the dominant structural signal. The corridor transitions
from smooth-ish (Wob_norm < 1) to oscillatory (Wob_norm ≈ 1). This pre-collapse
resonance predicts the observed W-discontinuity: the jump from W(2)=0.708 to
W(3)=2.025 corresponds to the wobble overtaking the static geometry, increasing
trap density in the MCMC objective landscape.

**Conjecture:** The W(|G|) curve is the algebraic shadow of this resonance. The
ω=3 threshold marks the first regime where wobble-driven interference is the
primary determinant of MCMC behavior, and the trap density function W(|G|) is
a resonance profile, not a static constraint count.

**Kill condition:** Find a (ω, m, k) class where the W-discontinuity appears
at a k/p value inconsistent with the Wob_norm threshold. Specifically: if
Wob_norm remains < 1 for the k values where W(|G|) makes its super-linear jump,
the resonance model is falsified.

**Current tier: A.** The wobble is defined and computable. The connection to
W(|G|) is structural intuition. No algebraic derivation of the resonance → trap
density → W link yet exists.

---

## A.13 — The Narrowing Corridor: Wobble Tightening as k → p (Tier A)

*From session discussion, March 31, 2026. New structural claim.*

**Statement:** The CRT corridor does not have fixed oscillation amplitude. The
wobble tightens as k approaches p. Specifically:

1. **Amplitude behavior:** The oscillation between C₁₀ and D₁₀ cycle membership
   does not average out as k → p. Instead the wavelength compresses and the
   remaining corridor length (p − k) shrinks. The effect is that the oscillation
   cannot average — there is no longer enough corridor to complete a full period.

2. **At k = p:** The oscillation collapses. R(m,b,k) → 0 at k=p (confirmed in
   corridor atlas). The gate is reached. Phase transition with zero width.

3. **Physical picture:** From outside (k << p), the corridor appears smooth because
   the wobble amplitude is large relative to the wavelength — it averages flat.
   As k → p, the wavelength compresses against the door and the remaining distance
   (p−k)/p → 0. At RSA scale, where p is enormous, no finite probe can detect the
   compression. The corridor feels smooth because you cannot walk far enough to see
   one complete oscillation.

4. **Security consequence:** RSA security is not only that the door (k=p) is far
   away. It is that the wobble tightens so slowly at RSA scale that no finite
   sampling can resolve the approach. The corridor is indistinguishable from flat
   because (p−k)/p is never close to 0 at any reachable k.

**Formalization:** This picture is NOT captured by Luther's Definition A.W.
Wob(b,k) stays near 4/5 as k→p — it does not collapse. The collapse belongs
to a third object: the corridor compression function.

**Candidate definition (Luther, March 31 2026):**

```
Corridor(b, k) = R(m, b, k) × sin²(π × W_BHML × k/p)
```

**Properties:**
- Fixed oscillation frequency: W_BHML = 3/50 (the TIG operator constant, k-independent)
- Amplitude = R(m,b,k): collapses at k=p because R(m,b,p) = 0 (D2 sign flip, Tier C2)
- Zero at the door: Corridor(b,p) = 0 automatically from R→0
- Frequency stays constant throughout the corridor — only amplitude dies
- Harmonic pre-echo: the sin² term produces sidelobes at spacing set by W_BHML,
  which matches the "harmonic countdown" interpretation of the sinc² field (A1)

**Physical picture corrected:** The sinc² collapse at k=p is NOT a wobble phenomenon.
It is a compression phenomenon. Frequency stays constant (W_BHML = 3/50).
Amplitude goes to zero (R(m,b,k) → 0). These are two separately named invariants.

**Kill condition:** Does Corridor(b,k) reproduce the empirical sinc² envelope
from the corridor atlas?
- If **yes**: Tier C immediately. Sinc² field, corridor compression, and W_BHML
  are unified in a single algebraic object.
- If **no**: The three-object separation stands; the candidate formula needs revision.
  The compression function requires a different algebraic form.

**Provenance:** This three-object separation was arrived at independently by
Sanders (computation: Wob(10,9)=8/9 vs verify_claims.py 3/50 PASS) and Luther
(algebra: sinc² collapse structure) on March 31, 2026, without prior coordination.
First Luther-Sanders result from simultaneous independent convergence.

**Current tier: A.** Candidate formula is stated. Kill condition is clear.
Path to Tier C: test Corridor(b,k) against the corridor atlas empirical envelope.

---

## Lemma D.H — Wobble-Bounded HAR-Rank Drift (Tier A Conjecture)

*Reproduced from LutherWobbleMap.docx. Labeled "Tier D" in source — downgraded
to Tier A/B conjecture by synthesis framework: the bound is stated but not proved.*

**Statement:** Let b = p₁p₂…p_ω with ω ≥ 2. Let HAR(x) denote the HAR-rank
of x ∈ C(b,k). Define wobble amplitude Wob_norm(b,k) as in Definition A.W.

Conjecture: for all x ∈ C(b,k),
```
|HAR(x² mod b) − HAR(x)| ≤ f(ω) · Wob_norm(b,k)
```
for some monotone function f depending only on ω.

**Consequences (if proved):**
1. If Wob_norm(b,k) < 1/f(ω): HAR-rank drift is bounded by 1, and HAR-rank
   is preserved across all b in the same (ω, m, k) class.
2. HAR-rank preservation implies universality of the gate rate:
   R(m, b₁) = R(m, b₂) for all b₁, b₂ with identical (ω, m, k).
3. When Wob_norm ≥ 1/f(ω): HAR-rank deformation begins, producing the
   W-discontinuity at ω=3.

**This is the Tier D target for C7.** If Lemma D.H is proved:
- The HAR rank preservation condition (HAR_RANK_STABILITY.md) becomes a theorem
- C7 advances from Tier C to Tier D for all (ω, k)
- The C→D gap for C7 is closed

**Current tier: A.** The bound is the right form — it connects wobble amplitude to
HAR-rank stability, which is exactly what the C7 proof needs. But the function f(ω)
is not specified, and the bound is not derived. Proving this requires:
1. An explicit formula for f(ω) from the CRT structure
2. A proof that HAR(x² mod b) − HAR(x) is bounded by the wobble amplitude
   (this requires characterizing how c² mod b moves within the ordered set C(b,k))

---

## Conjecture D.R — Resonance-Driven Universality (Tier A)

**Statement:** HAR-rank preservation is guaranteed whenever the wobble resonance
between the two CRT residue cycles remains below the collapse threshold:

```
Wob_norm(b, k) < 1/f(ω)  ⟹  R(m, b₁) = R(m, b₂) for all b₁, b₂ with same (ω, m, k)
```

**Interpretation:** Universality of gate rates emerges from resonance geometry, not
from static residue structure. The interference pattern between C₁₀ and D₁₀
constrains HAR-rank stability, which constrains universality of R(m, b).

---

## Tier A → D Roadmap

```
Tier A (Intuition — confirmed)
  A.12: CRT corridor behaves as a flexible tube.
        Wobble = beat frequency between two residue cycles.
        W-discontinuity = algebraic shadow of wobble resonance.
  A.13: Corridor does not have fixed amplitude — it narrows as k → p.
        Wavelength compresses against the gate; remaining corridor (p−k)/p → 0.
        At RSA scale, compression is unresolvable by finite probes.
        Three distinct objects: W_BHML (operator table), Wob(b,k) (alphabet
        membership), Corridor_compression (tightening ratio). Defined separately.

  TWO WOBBLE QUANTITIES DISAMBIGUATED (see §Disambiguation):
    W_BHML = 3/50  [THM, Z/10Z ring arithmetic, verified PASS]
    Wob(b,k) = 8/9 at k=9  [Definition A.W, alphabet membership, k-dependent]
    These are NOT equal. Do not conflate.

        ↓

Tier B (Mechanistic Structure — to establish)
  Wobble amplitude Wob_norm(b,k) is computable via Definition A.W.
  Trap density in MCMC objective increases with Wob_norm.
  HAR-rank deformation begins at Wob_norm = threshold.
  ω=3 is first regime where Wob_norm > threshold.
  Corridor_compression(b,k) = Wob_norm(b,k) × (k/p) is monotone in k/p.

  [Next step: compute Wob_norm for tested (ω, m, k) classes;
   verify correlation between Wob_norm and W(|G|).
   Compute Corridor_compression and verify monotonicity.]

        ↓

Tier C (Algebraic Structure — partial)
  W(|G|) is a monotone, super-linear trap-density exponent.
  C7 (ω-Class Universality): R(m,b) = R(m,b') when HAR-rank preserved.
  HAR-rank confirmed stable for strong semiprime class at k=9.

        ↓

Tier D (Proof Targets — open)
  Prove Lemma D.H: |HAR(x² mod b) − HAR(x)| ≤ f(ω) · Wob_norm(b,k).
  Derive W(|G|) from wobble amplitude and CRT interference geometry.
  Establish: R(m,b) universal iff Wob_norm(b,k) < 1/f(ω).
```

---

## The Picture

The "smooth hallway" model was the first approximation. The CRT corridor is a hallway
when k << p: the wobble averages out, the geometry is nearly static, the MCMC glides.
But as k approaches p, the hallway breathes. The two residue cycles stop averaging
and start interfering. The corridor becomes oscillatory. The MCMC encounters rhythm
where it expected static walls.

The W-jump from W(2)=0.708 to W(3)=2.025 is the precise moment the corridor stops
being a hallway and becomes a resonance field. Not a mystery. A threshold.

The work now is to prove that the threshold is where Lemma D.H says it is.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
