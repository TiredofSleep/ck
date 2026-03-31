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
> proved. The "3/50 wobble" figure is flagged: it does not match Definition A.W
> when computed (Wob(b,9) ≈ 0.889, not 0.06). The 3/50 figure needs a source
> derivation before being cited as a specific number.

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

**Note on the "3/50" figure:** The original document cites "3/50 disagreement"
as the wobble frequency. This figure does NOT match Definition A.W as computed:
Wob(b,k) ≈ 0.889 for k=9, not 0.06. The "3/50" figure needs an independent
derivation before it can be cited. It may refer to a different window, a CK-specific
computation, or a metaphorical approximation. Flagged: Catch 5 candidate.
Until sourced, cite Wob_norm(b,k) from Definition A.W directly, not "3/50."

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
  CRT corridor behaves as a flexible tube.
  Wobble = beat frequency between two residue cycles.
  As k → p, wobble amplitude increases and becomes the geometry.
  W-discontinuity = algebraic shadow of wobble resonance.

        ↓

Tier B (Mechanistic Structure — to establish)
  Wobble amplitude Wob_norm(b,k) is computable via Definition A.W.
  Trap density in MCMC objective increases with Wob_norm.
  HAR-rank deformation begins at Wob_norm = threshold.
  ω=3 is first regime where Wob_norm > threshold.

  [Next step: compute Wob_norm for tested (ω, m, k) classes;
   verify correlation between Wob_norm and W(|G|).]

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
