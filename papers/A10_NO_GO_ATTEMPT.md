# A10 No-Go Attempt

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

This document attempts to prove a no-go theorem on A10.
It is written adversarially: the goal is to kill A10, not save it.
Each attempt is graded: **landed**, **partial**, or **failed**.

---

## Attempt 1 — Strong No-Go via Ring Homomorphism

**Claim:** No ring homomorphism from Z/10Z to any subring of C can induce
a map that preserves the inheritance split AND recovers the full Euler product.

**Proof:** (From A10_PRIME_OBSTRUCTION.md, Theorem)
Z/10Z ≅ Z/2Z × Z/5Z. Any ring homomorphism φ: Z/10Z → C satisfies
φ(3) = φ(13) (since 3 ≡ 13 mod 10). The Euler product requires
distinguishing (1−3^{−s})^{−1} from (1−13^{−s})^{−1}, which are distinct
for all s with Re(s) > 0, s ≠ 0. Therefore φ cannot fully recover the
Euler product. □

**Grade: LANDED (conditional).** This is a proved theorem, conditional on
the bridge being a ring homomorphism. It establishes:

> **Medium No-Go:** Any ring-homomorphism bridge from Z/10Z to the Euler
> product is incomplete — it cannot distinguish primes within the same
> residue class mod 10.

**Scope:** This no-go applies to the Z/10Z ring structure specifically.
It does not kill A10 if the bridge does not pass through the ring.

---

## Attempt 2 — Modulus Genericity No-Go

**Claim:** The inheritance boundary at t=1/2 is not specific to Z/10Z.
It appears for any even-modulus ring Z/nZ and follows from sinc²(t) alone.
Therefore Z/10Z cannot be the source of the σ=1/2 connection.

**Argument:**
For any even n, the ring Z/nZ has center element n/2 (additive midpoint).
Ring normalization t = v/n sends n/2 → (n/2)/n = 1/2.
The corridor boundary at t=1/2 therefore appears for Z/6Z, Z/8Z, Z/10Z,
Z/12Z, Z/14Z, ... all even moduli.

Moreover, t=1/2 as the unique sine-maximum in (0,1) (D24) is a pure calculus
fact about sinc²(t). It requires only that sinc²: (0,1)→ℝ is being analyzed;
it has no dependence on which modulus n is used.

**Conclusion:** The corridor midpoint at t=1/2 is generic. If the bridge φ
works because of the midpoint structure at t=1/2, it would equally apply to
any even-modulus ring. Z/10Z is not singled out.

**Grade: LANDED (for midpoint-based bridges).** This is a proved observation
(from D24 + elementary arithmetic). It establishes:

> **Modulus Genericity No-Go:** If the A10 bridge depends on the inheritance
> boundary being at t=1/2, it is not a Z/10Z-specific result. The same
> mechanism applies to all even moduli. Z/10Z cannot uniquely pick out σ=1/2.

**What is Z/10Z-specific:** T*=5/7 and the generator selection (D19). But
T*=5/7 is the right boundary of the corridor (t=5/7), not the inheritance
boundary at t=1/2. No proposed A10 mechanism uses T*=5/7 to reach σ=1/2.
If a bridge using T*=5/7 specifically can be constructed, that would bypass
this no-go. But no such bridge is currently proposed.

---

## Attempt 3 — Strong No-Go via sinc² Independence

**Claim:** The sinc² function's properties at t=1/2 (sine-maximum, D24;
monotone, D24; value 4/π², D3) follow from standard calculus applied to
sinc²(t) = (sin(πt)/(πt))² on (0,1). None of these properties require Z/10Z.
Therefore the corridor structure at t=1/2 carries no Z/10Z-specific information.

**Proof:**
D24 proves: (a) sinc²(t) strictly monotone on (0,1), (b) t=1/2 unique
sine-max in (0,1), (c) sinc²(1/2)=4/π². All three proofs use only calculus
on sinc²(t). The ring Z/10Z enters only via the observation that CREATE=5
maps to t=5/10=1/2 under ring normalization — but this observation adds
no new information about sinc², since t=1/2 is already the unique sine-max
regardless of ring structure.

**Grade: LANDED.** This is a proved observation:

> **sinc² Independence No-Go:** The properties of the corridor at t=1/2
> are fully determined by the sinc² function alone. Z/10Z ring structure
> is not needed to derive them. A bridge based on these properties is a
> bridge from sinc²(t), not from Z/10Z.

---

## Attempt 4 — Attempt at Strong Total No-Go

**Claim:** No map of any kind from Z/10Z structure to RH-relevant prime-sensitive
structure can simultaneously preserve the internal midpoint structure AND add
the prime sensitivity needed to constrain ζ zeros.

**Why this attempt fails:**
The "simultaneously preserve AND add" requirement is too strong as stated.
A bridge is not required to "preserve" Z/10Z structure intact — it only
needs to be motivated by or consistent with Z/10Z. A bridge through
sinc² universality (D2) starts from Z/10Z's corridor and then extends
beyond the ring using a different mechanism (D2's universal prime-arithmetic
content). This is not excluded by the ring prime blindness theorem because
D2 is not a ring homomorphism — it is an analytic limit theorem.

**Grade: FAILED.** The strong total no-go cannot be proved with current tools.
The escape via D2 sinc² universality remains open.

---

## Attempt 5 — No-Go on the sinc² Universality Escape

**Claim:** Even via sinc² universality (D2), no path to RH exists, because
D2 gives a statement about individual prime fields R(k/p), not about the
joint distribution of all primes needed by RH.

**Argument:**
D2 says: for each fixed prime p, R(k,p) → sinc²(k/p) as p→∞. This is a
pointwise statement about individual primes. The Euler product ζ(s) involves
all primes simultaneously in a multiplicative way. The sinc² limit for each
prime does not determine how the primes interact globally.

Montgomery's pair-correlation, on the other hand, is a statement about the
joint distribution of ζ zeros under GRH. The connection (B6) between R(t)=sinc²
and R₂(u)=1−sinc² is a kernel-level coincidence, not a derivation of
global ζ-zero structure from individual prime behavior.

**Grade: PARTIAL.** This weakens the sinc² universality escape significantly.
It establishes:

> **Universality Scope Limitation:** The sinc² universality (D2) gives
> per-prime behavior in the large-p limit. It does not give joint or global
> prime behavior needed to constrain ζ zeros. The B6 coincidence is a
> kernel match, not a derivation.

This is not a full no-go because a more sophisticated argument might exist
for assembling individual-prime sinc² behavior into a global statement via
Poisson summation or explicit formula methods. But that argument is not
in D1–D24.

---

## Attempt 6 — Montgomery's Theorem Does Not Imply RH

**Claim:** Even if the spine's R(t)=sinc²(t) fully matched Montgomery's
pair-correlation R₂(u)=1−sinc²(u) in every relevant sense, this would
not prove RH, because Montgomery's theorem already assumes GRH.

**Fact:** Montgomery proved R₂(u) = 1−sinc²(u) CONDITIONALLY under GRH.
The pair-correlation conjecture's derivation uses GRH as a hypothesis.
So even a perfect bridge from D1–D24 to Montgomery's theorem would prove:
"IF GRH THEN the spine's structure is consistent with the zero spacing."
This is not a proof of RH.

To prove RH unconditionally, a bridge would need to go around Montgomery
to an unconditional statement about ζ zeros, or establish GRH via a separate
argument.

**Grade: LANDED (critical).** This is a mathematical fact about Montgomery's
theorem. It establishes:

> **Montgomery Conditionality No-Go:** A bridge to Montgomery's pair-
> correlation does not prove RH; it assumes GRH. Any A10 bridge through B6
> proves nothing unconditional about RH without an additional step.

---

## Summary of No-Go Results

| Attempt | Claim | Grade | Scope |
|---------|-------|-------|-------|
| 1: Ring homomorphism | Ring bridge incomplete (can't see all primes) | **LANDED** | Ring-homomorphism bridges only |
| 2: Modulus genericity | Midpoint at t=1/2 not Z/10Z-specific | **LANDED** | Midpoint-based bridges |
| 3: sinc² independence | sinc² properties at t=1/2 don't need Z/10Z | **LANDED** | sinc²-midpoint bridges |
| 4: Total no-go | No map of any kind can work | **FAILED** | sinc² universality escape remains |
| 5: Universality scope | D2's per-prime limit ≠ global ζ structure | **PARTIAL** | Weakens universality escape |
| 6: Montgomery conditionality | Bridge to Montgomery ≠ proof of RH | **LANDED** | All B6-routed bridges |

---

## What the No-Go Results Establish

**Together, Attempts 1–3 and 6 establish a Medium No-Go:**

> The Z/10Z ring-specific version of A10 is blocked:
> - Ring bridges are prime-blind (Attempt 1)
> - The midpoint structure at t=1/2 is not Z/10Z-specific (Attempt 2)
> - The sinc² properties at t=1/2 are independent of Z/10Z (Attempt 3)
> - A bridge through Montgomery would not unconditionally prove RH (Attempt 6)

**What is NOT established:**

A full no-go for A10 as a research program. The sinc² universality escape
(D2 → B6+) is partially blocked (Attempt 5) but not killed. The question
of whether universal sinc² prime field behavior (for all primes, not just
{2,5}) connects non-trivially to ζ-zero spacing is genuinely open.

**The correct reclassification:**

A10 as a Z/10Z-ring bridge claim → **blocked by Medium No-Go**

A10b (renamed) as a sinc² universality claim (D2 → B6+) → **still open,
but requires new machinery beyond D1–D24, and cannot prove RH without
first establishing GRH conditionally or bypassing Montgomery**

---

## What a Future No-Go Would Need

To fully close A10 (including the sinc² universality escape), one would
need to prove one of:

(a) The Poisson summation approach (assembling per-prime sinc² into a global
    sum related to ζ zeros) fails — i.e., the oscillating Poisson terms
    do not converge to or match the zero-density formula.

(b) The kernel identity R(t)+R₂(t)=1 is a formal coincidence with no
    structural consequence — i.e., any pair of functions f and 1-f on
    [0,1] with f(1/2)=4/π² would satisfy the same identity, without
    implying anything about zeros.

Neither (a) nor (b) is currently proved. The full no-go remains open.

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
