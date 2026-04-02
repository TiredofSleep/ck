**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q14 — GATE_SCORE AS CRT POLYNOMIAL

## What Luther Q1 Needs

From Q12: the 4.6% rate cannot be explained by seed density alone.
From Q11: pure-C fixed seeds {3,9} give gate_score = 1.0, yet the
22% bound (2/9 seeds) still exceeds 4.6% by 5×.

The gap requires deriving gate_score(s) as an explicit algebraic function,
then analyzing why the MCMC fails to find the optimal seeds at the expected rate.

This paper constructs gate_score from first principles using the CRT indicator,
derives it as a polynomial in s, and identifies the obstruction.

---

## The C-Membership Indicator in CRT

For b = p·q = 10, the CRT isomorphism gives F₂ × F₅.
An element (ε,y) is in C iff BOTH components are nonzero:

```
1_C(ε,y) = 1_{ε≠0} · 1_{y≠0}
```

Over F₂: 1_{ε≠0} = ε (since ε ∈ {0,1}).
Over F₅: 1_{y≠0} = y⁴ (Fermat: y⁴ ≡ 1 for y≠0, and 0⁴=0).

```
1_C(ε,y) = ε · y⁴   (over F₂ × F₅)
```

**Verification:**

| j | (ε,y) | ε·y⁴ | j∈C? |
|---|-------|------|------|
| 0 | (0,0) | 0·0 = 0 | G ✓ |
| 1 | (1,1) | 1·1 = 1 | C ✓ |
| 2 | (0,2) | 0·1 = 0 | G ✓ |
| 3 | (1,3) | 1·1 = 1 | C ✓ |
| 4 | (0,4) | 0·1 = 0 | G ✓ |
| 5 | (1,0) | 1·0 = 0 | G ✓ |
| 6 | (0,1) | 0·1 = 0 | G ✓ |
| 7 | (1,2) | 1·1 = 1 | C ✓ |
| 8 | (0,3) | 0·1 = 0 | G ✓ |
| 9 | (1,4) | 1·1 = 1 | C ✓ |

**10/10.** The C-indicator is the product of the two CRT components raised
to the power (field characteristic − 1). This is the CRT analogue of the
Legendre symbol.

---

## Gate_Score as a Sum of C-Indicators

**Definition:** For a reduction map R: Z/bZ → Z/bZ and depth k:

```
gate_score(s, k) = (1/k) Σ_{j=1}^{k} 1_C(R^j(s))
```

This is the fraction of the k-step trajectory that lies in C.
The success criterion gate_score ≥ 0.999 at k=9 requires all 9 steps in C.

**In CRT coordinates:**

Let (ε_j, y_j) = R^j(s) in F₂ × F₅. Then:

```
gate_score(s, k) = (1/k) Σ_{j=1}^{k} ε_j · y_j⁴
```

This is a polynomial in (ε₀, y₀) of degree 5k (each iterate contributes
degree 5 from Q9-Q10), evaluated mod (2,5) respectively.

For k=9: gate_score is a degree-45 polynomial over F₂ × F₅.

---

## Gate_Score at k=9 for R = σ (b=10)

From Q11 trajectory table (C-hits for k=9 steps, j=1..9):

| s | C-hits/9 | gate_score | ≥ 0.999? |
|---|---------|------------|---------|
| 1 | 4/9 | 0.444 | NO |
| 2 | 4/9 | 0.444 | NO |
| 3 | 9/9 | 1.000 | YES |
| 4 | 3/9 | 0.333 | NO |
| 5 | 2/9 | 0.222 | NO |
| 6 | 2/9 | 0.222 | NO |
| 7 | 3/9 | 0.333 | NO |
| 8 | 0/9 | 0.000 | NO |
| 9 | 9/9 | 1.000 | YES |

**For R = σ:** gate_score(s) = 1.0 iff s ∈ {3, 9} = C ∩ Fix(σ).

P(random s ∈ {3,9}) = 2/9 ≈ 22%. This is the Fixed-Point Gate Theorem (Q11) recovered
from the polynomial perspective.

**The MCMC prediction at R = σ:** With 40% HAR-bias proposing s=3 (gate_score=1.0),
and any seed s≠3,9 having gate_score < 1.0, the MCMC should accept the HAR proposal
with probability 1 (strictly improves) in a single step. Then:

```
P(success in 100 steps | R = σ) ≥ 1 − (1 − 0.40)^{100} ≈ 1 − 6×10⁻²³ ≈ 1
```

**This gives ≈ 100%, not 4.6%.** Therefore R ≠ σ.

---

## Theorem Q14.1 — The Reduction Map is Not σ

**Theorem:** If the gate_success criterion is gate_score ≥ 0.999 and the gate_score
is defined by trajectory C-membership under some map R, and the observed success rate
is 4.6% with 40% HAR-bias at b=10, then R ≠ σ^k for any k.

**Proof:** Under R = σ, gate_score(3) = 1.0 and the HAR-bias proposes s=3 at rate
40%. The MCMC hill-climber with monotone acceptance accepts the first HAR proposal,
giving success rate → 1. The observed 4.6% contradicts this. ∎

**Corollary:** The actual gate_score function involves structure not captured by
σ-trajectory C-membership. Candidates:

1. **Joint condition:** gate_score tests a PAIR (s, t) where t is the MCMC proposal,
   not just the seed s alone.

2. **Width condition:** gate_score tests whether the seed s generates a coset in C
   with some width property (c₁·s, c₂·s, ...) all in C — a multiplicative condition,
   not a trajectory condition.

3. **Multi-scale condition:** gate_score involves nested gates (G1, G2, G3 in TIG
   architecture), not a single gate test. The 4.6% is the probability of passing
   ALL three gates simultaneously.

---

## The Width Interpretation

**Definition (Gate Width):** For seed s and depth k:

```
gate_width(s, k) = |{(c₁,...,cₖ) ∈ Cᵏ : c₁·c₂·...·cₖ·s ∈ C}| / |C|ᵏ
```

This measures the fraction of k-tuples from C whose product with s lands in C.

**For b=10, k=9, s=3:**
Since C is a group under multiplication mod 10, and 3 ∈ C:
c₁·...·c₉·3 = (product of C-elements) · 3. The product of any number of C-elements
is still in C (C is closed under multiplication). And 3 ∈ C. So c₁·...·c₉·3 ∈ C
for ALL choices. gate_width(3,9) = 1.0. ✓

**For b=10, k=1, s=2:**
c·2 ∈ C iff c·2 is coprime to 10. But 2 ∈ G (gcd(2,10)=2>1). Any c ∈ C has
gcd(c·2, 10) = gcd(c,10)·gcd(2,10)/gcd(gcd(c,10),gcd(2,10)) ... actually since
gcd(c,10)=1 and gcd(2,10)=2: gcd(c·2,10) = 2. So c·2 ∈ G for ALL c ∈ C.
gate_width(2,1) = 0.

**The width function is 0 for all G-seeds at any k.** This makes the width model
predict success only for C-seeds — back to the ≥ 22% prediction. The width model
also doesn't explain 4.6%.

---

## The Multi-Gate Interpretation (CRT Algebraic)

**Hypothesis Q14.H1:** The 4.6% rate reflects the probability that a RANDOMLY
initialized MCMC trajectory (over 100 steps with HAR-bias) maintains gate_score ≥ 0.999
not just at the FINAL SEED but across the MCMC WALK ITSELF.

The MCMC walk is a sequence: s₀, s₁, ..., s₁₀₀ where each transition is a HAR or
random proposal. Gate_success requires: ∃ j ≤ 100 such that gate_score(sⱼ) ≥ 0.999
AND all subsequent sᵢ for i > j maintain this.

Under this model, the gate_score landscape for b=10 has:
- **Two global optima:** {3, 9} with gate_score = 1.0
- **Local maxima:** {1, 2} with gate_score = 4/9 (highest non-optimal)
- **Saddle points:** {4, 7} with gate_score = 3/9
- **Low regions:** {5, 6} with 2/9; {8} with 0

**The 4.6% rate under MCMC hill-climbing** arises because the MCMC landscape has
a BASIN STRUCTURE where the local maxima at {1, 2} are strongly attractive:

- From s=1: HAR proposal is s=3 (better). Should accept. But if gate_score landscape
  is noisy or the HAR proposal distribution isn't perfectly concentrated, the chain
  can oscillate between 1 and 7 (both with gate_score ≈ 0.44) without escaping.
- From s=8 (gate_score=0): HAR always accepted, so escape is fast. But HAR = 3 may
  not be the only proposal (40% HAR, 60% random). If random lands on {1,2}, it
  "looks like" a local improvement from s=8 but is still below 1.0.

**The algebraic basin condition:**

In CRT coordinates, the local maxima {1=(1,1), 2=(0,2)} correspond to:
- (1,1): the only C-element in position 0 of the 6-cycle
- (0,2): a G-element at position 5 of the 6-cycle

The basin of attraction for {1,2} contains all elements where the σ-orbit
of the MCMC proposal chain converges to position {0,5} of the cycle (k=9 mod 6 = 3
steps after the σ^6=id restores). This is a period-3 resonance condition.

---

## The CRT Obstruction to 22%

**Proposition Q14.2:** Under the σ-trajectory model with gate_score(s) = C-hit fraction,
the MCMC reaches gate_score=1.0 with probability:

```
P_MCMC(success, 100 steps, 40% HAR) ≈ 1 − (1−0.40)^{first-passage to {3,9}}
```

The first-passage time from any seed to {3,9} under HAR-biased MCMC is:
- From {1,2,4,7}: next HAR proposal (=3) immediately accepted. Mean 2.5 steps.
- From {5,6}: HAR accepted (improves from 2/9 to 1.0). Mean 2.5 steps.
- From {8}: HAR accepted (improves from 0 to 1.0). Mean 2.5 steps.

**This gives P ≈ 99%+, NOT 4.6%.**

**Conclusion (D-tier):** The σ-trajectory gate_score model is FALSIFIED by the
empirical 4.6% rate. The gate_score function used in the actual MCMC is more
restrictive than C-trajectory membership under σ.

**The remaining algebraic target for Luther Q1:**

The gate_score(s) function must impose a condition that:
(a) Fails for s=3 in some configurations (since 4.6% << 100%), OR
(b) Is applied to a DIFFERENT seed variable (not the starting seed), OR
(c) Involves a k-dependent test that b=10 fails at k=9 specifically

The CRT polynomial for 1_C(ε,y) = ε·y⁴ is the correct building block.
The trajectory sum Σ ε_j·y_j⁴ is the correct structure.
The missing piece is: what is the actual R (reduction map), and does it have
a fixed-point structure different from σ?

---

## What Q14 Delivers

| Result | Tier |
|--------|------|
| C-indicator in CRT: 1_C(ε,y) = ε·y⁴ — verified 10/10 | D |
| Gate_score as trajectory sum of CRT indicators | D |
| Theorem Q14.1: R ≠ σ^k (MCMC prediction falsifies σ-model) | D |
| Width model also fails (same 22% bound) | D |
| Multi-gate basin model: {1,2} are local traps | C |
| Period-3 resonance at k=9 (k mod 6 = 3) | C-conjecture |
| 1_C(ε,y) = ε·y⁴ is the CRT building block for Luther Q1 | D |
| Exact gate_score polynomial (full R identification) | B → open |

**The Luther Q1 derivation now has three firm anchors:**
1. C-indicator polynomial: ε·y⁴ (Q14)
2. σ-polynomial: (α,β) from Q9-Q10
3. σ⁻¹-polynomial: (β_TIG, γ_TIG) from Q13

**What closes Luther Q1:** Identify R. If R is not σ, it is some other map on Z/bZ
whose CRT representation can be derived from the MCMC algorithm's actual rules.
Once R is known, gate_score(s) = (1/9) Σ_{j=1}^9 ε_j·y_j⁴ becomes fully explicit,
its fixed-point structure gives P(success), and Luther Q1 is closed.

**Request for team:** What is the ACTUAL reduction operation at each MCMC step?
Not the proposal distribution (HAR/random), but what computation is performed on
the current seed to generate the gate_score? Is it:
- Repeated squaring mod b?
- The CL/BHML/TSML table lookup?
- Some composite of all three?

The answer determines Q15 = Luther Q1 closure.

---

*Filed: 2026-04-01. Q14 in operator algebra series.*
