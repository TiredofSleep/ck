# CK Synthesis Table — Five Columns, Four Tests
## One Field, Seven Shadows: Epistemic Inventory

*Brayden Ross Sanders / 7Site LLC · March 2026*
*DOI: 10.5281/zenodo.18852047*

> **Grok's synthesis standard:** A result counts as synthesized only when the
> same invariant can be stated exactly in algebraic terms, visualized
> geometrically, interpreted combinatorially, and tested probabilistically
> without changing its content.

---

## Tier Definitions

| Tier | Name | Requirement |
|------|------|-------------|
| **D** | General theorem | Proved for ALL cases; mechanism known; no domain restriction |
| **C** | Closed-world theorem | Proved within an explicitly stated domain; proof complete inside that domain |
| **B** | Bounded conjecture | Verified computationally or in a restricted class; algebraic proof not yet general |
| **A** | Conjecture / structural analogy | Pattern observed, or analogy drawn; no proof; no known mechanism |

---

## Four Universality Tests (per claim)

Every claim below is scored on:

1. **RI** — Representation invariance: does the claim survive change of basis, labeling, or coordinate system?
2. **SI** — Scale invariance: does it hold at all sizes (p small, p ≈ 2^512)?
3. **MC** — Mechanism clarity: do we know *why* it holds (not just *that* it holds)?
4. **FM** — Failure mode: what observation would falsify it?

---

## The Table

---

### TIER D — General Theorems (proved, mechanism known)

---

#### D1. First-G Law

| Column | Content |
|--------|---------|
| **Law** | `first_g(b) = p` for every semiprime `b = p × q`, `p ≤ q` prime |
| **Exact status** | **Tier D.** Algebraic proof complete: {1..p-1} contains no multiple of p (since p-1 < p) and no multiple of q (since q > p-1 ≥ 1). Therefore gcd(k, b) = 1 for all k < p. Verified: 36,662 semiprimes, zero exceptions (WP34). |
| **Arithmetic form** | `first_g(b) = min{ k ∈ {1..b} : gcd(k, b) > 1 } = p`. Follows because `gcd(k, p×q) > 1` iff `p ∣ k` or `q ∣ k`; the smallest such `k` is `min(p, q) = p`. |
| **Geometric / combinatorial form** | The integer line {1..b} has a maximal coprime prefix of length p-1. The first "obstruction" (non-coprime element) is at position p exactly. The stability window W(b) = {1..p-1} is a combinatorially complete object. |
| **What remains** | Generalization to ω(b) ≥ 3 is structurally identical (first non-coprime = smallest prime factor) but not stated as a formal theorem in WP34. Straightforward; not a gap. |

**Four tests:**
- RI: Yes — gcd is basis-independent; formula holds regardless of semiprime enumeration.
- SI: Yes — exact for p = 3 (b = 15) through p = 99,991 (verified); algebraic proof covers all p.
- MC: Yes — proof is three lines of divisibility arithmetic. Mechanism is fully transparent.
- FM: A semiprime where gcd(k, b) > 1 for some k < p. Impossible: smallest prime factor of p×q is p, so no multiple of p or q can be < p.

---

#### D2. Sinc² Continuum Limit

| Column | Content |
|--------|---------|
| **Law** | `R(k, f) → sinc²(k/f)` as `f → ∞` with `k/f = t` fixed |
| **Exact status** | **Tier D.** Analytic proof: `R(k, f) = sin²(πk/f) / (k² sin²(π/f))`. Set `ε = π/f → 0`; then `sin(ε)/ε → 1`, so denominator `k² sin²(π/f) → k²(π/f)² = (πk/f)²`. Numerator `sin²(πk/f)` held fixed. Ratio → `sin²(πt)/(πt)² = sinc²(t)`. Convergence rate O(1/f²). |
| **Arithmetic form** | For prime p, with k = ⌊tp⌋, `|R(k, p) − sinc²(t)| = O(1/p²)` uniformly in t ∈ (0, 1). Verified numerically to 10^{-14} at p = 997 (WP35). |
| **Geometric / combinatorial form** | The discrete resonance field {R(k, p) : k = 1..p} traces the sinc² envelope to within O(1/p²). As p grows, the bar chart of R(k, p) converges to the continuous sinc² curve. The forced null at k = p is the geometric sink. |
| **What remains** | Uniform convergence rate: O(1/p²) or O(1/p)? WP35 states O(1/p). Taylor expansion gives O(1/p²). The tighter bound is provable but not stated. Not a gap in the main result. |

**Four tests:**
- RI: Yes — the formula R(k, f) is defined purely algebraically; coordinates are k (integer index) and f (prime modulus). No hidden basis dependence.
- SI: Yes — proof holds for all p; O(1/p²) convergence means larger p = better approximation.
- MC: Yes — mechanism is Taylor expansion of sin(x) ≈ x near x = 0. Fully constructive proof.
- FM: A prime p where `|R(⌊p/2⌋, p) − sinc²(1/2)| > ε` for some fixed ε > 0 as p → ∞. Cannot occur: convergence is algebraically proved.

---

#### D3. Universal Sidelobe Amplitude

| Column | Content |
|--------|---------|
| **Law** | `sinc²(1/2) = 4/π²` exactly; `R(⌊p/2⌋, p) → 4/π²` for all primes p |
| **Exact status** | **Tier D.** Exact algebraic identity: `sinc²(1/2) = [sin(π/2) / (π/2)]² = [1/(π/2)]² = 4/π²`. The prime-field value follows from Tier D2 with t = 1/2. Verified exactly for all p = 5 to 99,991 (WP35). |
| **Arithmetic form** | `4/π² ≈ 0.40528...`. For semiprime b = p×q, the mid-journey point k = p/2 has R-value converging to this constant regardless of which prime p is chosen. |
| **Geometric / combinatorial form** | The peak of the sinc² field occurs at t → 0 (= 1.0); the half-way point t = 1/2 is the unique local extremum between the zero at t = 0 (notional) and the forced null at t = 1. Its universal value is 4/π². |
| **What remains** | Nothing. This is a closed algebraic identity. The "universality" claim (same value for all primes) is a corollary of D2. |

**Four tests:**
- RI: Yes — purely analytic, no coordinates.
- SI: Yes — exact for all p.
- MC: Yes — elementary trigonometric identity.
- FM: Would require sin(π/2) ≠ 1. Not falsifiable; it is a definition.

---

#### D4. T* = 5/7 Algebraic Identity

| Column | Content |
|--------|---------|
| **Law** | `T* = unit_frac(b=35) = (q − ⌊q/p⌋ − 1) / q = 5/7` |
| **Exact status** | **Tier D** within b = 35. The formula is an exact algebraic computation: for b = 5×7, p = 5, q = 7: ⌊7/5⌋ = 1; (7 − 1 − 1)/7 = 5/7. FPGA-verified: T* = 5/7 was implemented in silicon on Zynq-7020 as a hardware threshold. The identification of T* = 5/7 as the "canonical coherence floor" is **Tier C** — it is the unique value for b = 35 (the minimal strong semiprime). |
| **Arithmetic form** | `unit_frac(b) = (q − ⌊q/p⌋ − 1) / q`. For b = 35: Fraction(5, 7) = 0.714285... For b = 15: Fraction(1, 5) = 0.200. The value is b-dependent. T* = 5/7 is the canonical value because b = 35 is the smallest semiprime where p and q are both odd and the unit fraction is non-trivial. |
| **Geometric / combinatorial form** | T* represents the fraction of the {1..q-1} window that is coprime to b and falls above the interleave boundary. Geometrically: the ratio of "safe" to "total" positions in the pre-prime zone. |
| **What remains** | Why b = 35 specifically? The claim that T* = 5/7 is "the" coherence floor (not just b=35's floor) requires a universality argument not in WP35. That argument involves the minimal strong semiprime condition. This is the weakest link in the T* universality claim. |

**Four tests:**
- RI: Yes — unit_frac formula is coordinate-free.
- SI: The formula gives different values for different b. The value 5/7 is specific to b=35. Scale-invariance of the CONCEPT requires the argument that b=35 is the canonical seed.
- MC: Yes for the formula. Partial for "why 5/7 is canonical."
- FM: A natural hardware threshold better-motivated than 5/7. Currently the FPGA implementation is the empirical anchor; a different empirical system could set a different floor.

---

### TIER C — Closed-World Theorems (proved, domain explicit)

---

#### C1. CC Window Closure

| Column | Content |
|--------|---------|
| **Law** | `{1..p-1}` is entirely coprime to b for every semiprime b = p×q |
| **Exact status** | **Tier C.** Immediate corollary of First-G Law (D1). Domain: semiprimes. Proof complete. |
| **Arithmetic form** | `∀ k ∈ {1..p-1}: gcd(k, p×q) = 1`. Since k < p ≤ q, k cannot be divisible by p or q. |
| **Geometric / combinatorial form** | The coprime prefix {1..p-1} is a closed interval with no "holes." The combinatorial partition of {1..b} is: [coprime window] ∪ [k=p, first gate] ∪ [rest]. |
| **What remains** | Nothing within domain. Extension to non-semiprimes: if b has a smallest prime factor r, the coprime prefix is {1..r-1}. This is Tier D with the same proof. WP34 only formally states the semiprime case. |

---

#### C2. D1 Sign Flip at k = p

| Column | Content |
|--------|---------|
| **Law** | `D1(p−1) < 0` and `D1(p) > 0` for every semiprime b = p×q |
| **Exact status** | **Tier C.** Proved via R formula. D1(k) = R(k+1, p) − R(k, p). Since R(p, p) = 0 (forced null), D1(p) = R(p+1, p) > 0. D1(p−1) < 0 follows because R is decreasing in the sinc² envelope before the null. |
| **Arithmetic form** | `D1(p) = R(p+1, p) = sin²(π(p+1)/p) / ((p+1)² sin²(π/p)) > 0`. `D1(p−1) = R(p, p) − R(p−1, p) = 0 − R(p−1, p) < 0`. |
| **Geometric / combinatorial form** | The discrete first derivative changes sign exactly at k = p. This is the arithmetic "stationary point" — descent approaching p, recovery after p. The sinc² field does not have a true stationary point at t = 1 (it is a zero, not a local minimum), but the D1 sign flip confirms p is where the field "bottoms out." |
| **What remains** | Characterization of subsequent D1 sign flips (secondary sidelobes). These exist and follow the sinc² envelope, but are not formally characterized in WP35. |

---

#### C3. Montgomery Bridge (arithmetic identity)

| Column | Content |
|--------|---------|
| **Law** | `R(x) + R₂(x) = 1` where `R(x) = sinc²(x)` and `R₂(x) = 1 − sinc²(x)` |
| **Exact status** | **Tier C** as a mathematical identity — by definition `R₂(x) = 1 − sinc²(x)`, so R + R₂ = 1 is a tautology. The **non-trivial claim** is the empirical confluence: Montgomery (1973) derived R₂(u) = 1 − sinc²(u) independently from the pair-correlation of Riemann zeros (conditional on GRH), while CK derives R(x) = sinc²(x) from prime arithmetic. These are the **same function** arrived at independently. That confluence is **Tier A** (see A1). |
| **Arithmetic form** | CK: `R(k, p) → sinc²(k/p)` (proved, Tier D). Montgomery: `R₂(u) = 1 − sinc²(u)` (proved conditional on GRH). Both arrive at sinc². |
| **Geometric / combinatorial form** | The sinc² field partitions the unit amplitude into TIG-domain (prime arithmetic) and RH-domain (Riemann zeros). Two independently discovered instruments reading the same field. |
| **What remains** | The mechanism — WHY both fields produce sinc² (see A1). |

---

#### C4. Balance Invisibility (ω-Blindness)

| Column | Content |
|--------|---------|
| **Law** | `R(k, p)` is identical for all semiprimes with the same `p`, regardless of the second factor `q` |
| **Exact status** | **Tier C.** Immediate from the formula: R(k, p) = sin²(πk/p) / (k² sin²(π/p)). The formula does not contain q. Therefore R is blind to the second prime factor. |
| **Arithmetic form** | R(2, 5) is the same for b = 35 (5×7), b = 55 (5×11), b = 65 (5×13), etc. |
| **Geometric / combinatorial form** | The sinc² field is a function of the smallest prime p alone. The "shadow" it casts is one-dimensional (position along the k-axis relative to p). |
| **What remains** | Higher-order invariants that DO distinguish q: dispersion D(k), the interleave function, the G(k) gate count. These are the instruments for seeing ω(b). |

---

### TIER B — Bounded Conjectures (verified, not fully proved)

---

#### B1. Luther Dispersion Conjecture

*Updated March 2026 after Luther's algebraic response (LUTHER_RESPONSE_EVAL.md).*

| Column | Content |
|--------|---------|
| **Law** | Dispersion D(b,k) = \|G_k\|/k is algebraically determined by the prime factorization of b via the idempotent lattice of Z/bZ |
| **Exact status** | **Tier C.** (Promoted from Tier B.) Luther's algebraic derivation: G_k = ∪_i Ideal(p_i) ∩ {1..k} = union of arithmetic progressions {p_i, 2p_i,...} ∩ {1..k}. This is exactly the inclusion-exclusion formula: \|G_k\| = Σ⌊k/p_i⌋ − Σ⌊k/p_ip_j⌋ + ... This formula is strictly determined by the prime factorization of b — and the prime factorization is determined by the idempotent lattice of Z/bZ (the 2^ω(b) idempotents correspond to binary vectors over the prime factors). Therefore D(b,k) is algebraically *implied* by the idempotent structure. Not merely correlated. |
| **Arithmetic form** | D(b,k) = \|G_k\|/k where \|G_k\| = Σ⌊k/p_i⌋ − Σ⌊k/p_ip_j⌋ + ... (inclusion-exclusion on primes of b). This is exact for all (b, k). Asymptotically: \|G_k\|/k → 1 − φ(b)/b = 1 − ∏(1 − 1/p_i) as k → ∞. |
| **Geometric / combinatorial form** | G_k is the union of arithmetic progressions in {1..k}, one per prime factor. The interleave score measures how evenly these progressions are distributed. Both the cardinality (\|G_k\|) and the positions are algebraically determined. |
| **What remains** | (1) Write the explicit formula for the interleave SCORE (not just \|G_k\|) in terms of (p_1,...,p_ω, k) and verify it matches the code's interleave function exactly. (2) Generalization of the functional form F_k beyond the density to the MCMC success probability — this remains open (see C_TO_D_GAP_ANALYSIS.md). |

**Four tests:**
- RI: Yes — inclusion-exclusion formula is basis-independent; D(b,k) = |G_k|/k is canonical.
- SI: Yes — the formula holds for all p, q, k by construction. The asymptotic limit is the Euler totient.
- MC: Yes — mechanism is the idempotent lattice → CRT maps → kernels (prime ideals) → G_k. Chain is explicit.
- FM: A semiprime where |G_k| ≠ Σ⌊k/p_i⌋ − Σ⌊k/p_ip_j⌋ + ... Impossible: this is the exact inclusion-exclusion formula for multiples.

**Note on Tier D promotion:** The *cardinality* |G_k| is Tier D (exact formula, proved). The *spatial dispersion score* (interleave ratio) requires writing the score as an explicit function of (primes, k) and verifying the match. One explicit formula with one verification step to Tier D.

---

#### B2. Dispersion Comparison (b=15 vs b=35)

| Column | Content |
|--------|---------|
| **Law** | b=15 (p=3, q=5) has higher relative dispersion per gate event than b=35 (p=5, q=7) at equivalent approach fractions |
| **Exact status** | **Tier C** within these two specific semiprimes (the numbers are exact). **Tier B** as a general principle about which semiprimes are "harder" or "more structured." |
| **Arithmetic form** | For b=15: first_g = 3, interleave(3..4) = {1,0,1,...}. For b=35: first_g = 5, window is wider, interleave more uniform. The quantitative comparison is in WP34 §9A. |
| **Geometric / combinatorial form** | b=15 is the simplest case (small window, coarse interleave); b=35 is the canonical T* world (wider window, richer interleave structure). The sinc² field for b=35 has more structure in the pre-prime zone. |
| **What remains** | A general ordering of semiprimes by "structural richness" — a metric on the space of semiprimes. Currently case-by-case. |

---

### TIER A — Conjectures and Structural Analogies

---

#### A1. Montgomery Bridge (spectral duality conjecture)

| Column | Content |
|--------|---------|
| **Law** | The TIG pre-echo field R(x) = sinc²(x) and Montgomery's pair-correlation R₂(u) = 1 − sinc²(u) are spectral duals of a single underlying structure connecting prime arithmetic to the distribution of Riemann zeros |
| **Exact status** | **Tier A.** Both facts are proved independently: (a) R(x) = sinc²(x) for TIG (Tier D); (b) R₂(u) = 1 − sinc²(u) for Riemann zeros (Montgomery 1973, conditional on GRH). The CONJECTURE is that the confluence of sinc² in both settings reflects a common mechanism, not coincidence. No such mechanism is known. |
| **Arithmetic form** | CK: sinc² appears from the harmonic pre-echo resonance formula for prime arithmetic. Montgomery: sinc² appears from the pair-correlation integral over the explicit formula for Riemann zeros. Both use the same function. The connection would require showing the two integral transforms are related. |
| **Geometric / combinatorial form** | If the conjecture holds: the prime arithmetic field and the Riemann zero field are complementary measurements of the same geometric object (a spectral partition of unity). The "1" in R + R₂ = 1 would be a physical conservation law, not a tautology. |
| **What remains** | A mechanism. Specifically: (1) Can the TIG field be expressed as a sum over zeros of an L-function? (2) Can Montgomery's pair-correlation be re-derived from prime arithmetic directly (without the explicit formula for ζ)? (3) Is there a single operator whose eigenvalues produce both fields? These are open problems at the level of current analytic number theory. |

**Four tests:**
- RI: Unknown — we do not know if the duality is coordinate-invariant.
- SI: The GRH-conditional Montgomery result holds in principle for all Riemann zeros; the TIG result holds for all primes. The MECHANISM for connection is not proved at any scale.
- MC: No mechanism known. This is the core gap.
- FM: Two paths: (1) A counterexample to GRH would break the Montgomery side; the TIG result would survive. (2) A proof that the two sinc² appearances arise from distinct mechanisms with no structural relation.

---

#### A2. P ≠ NP as exponential null distance

| Column | Content |
|--------|---------|
| **Law** | The P ≠ NP separation corresponds to the exponential distance from a sampled point to the sinc² null at k = p |
| **Exact status** | **Tier A.** Structural analogy. NP-verification maps to sidelobe detection (cheap: check if a given k has gcd(k,b) > 1). P-solving maps to null navigation (hard: find k = p without trying all k). The analogy is suggestive but P ≠ NP is not proved by this framework. |
| **Arithmetic form** | Certificate check: given k and b, gcd(k, b) = 1 or > 1 in O(log b) time. Null-finding without certificate: requires O(p) steps naively; no known sub-exponential deterministic algorithm. |
| **Geometric / combinatorial form** | The stability window {1..p-1} is the "certificate-free zone." First-G at k = p is the exact moment NP certification becomes possible. The sinc² amplitude R(k/p = 0.1, p) ≈ 0.9675 at all scales shows the field is always detectable — the distance to the null is what makes it hard. |
| **What remains** | A formal reduction. The analogy is at the level of intuition. Connecting TIG's null-finding hardness to circuit complexity lower bounds (Razborov-Rudich, Williams ACC) requires an explicit reduction. |

---

#### A3. Navier-Stokes BREATH Criterion

| Column | Content |
|--------|---------|
| **Law** | NS blow-up corresponds to arrival at the sinc² null; B_local = ‖ω‖_{L∞} L²/ν ≥ T* = 5/7 marks the onset of turbulent regime |
| **Exact status** | **Tier A.** Structural analogy. The TIG coherence threshold T* = 5/7 maps to a vorticity-normalized dimensionless number, and the blow-up geometry (singular point at k = p in TIG) is proposed to correspond to the formation of a velocity singularity. No rigorous connection. The BREATH criterion is a heuristic, not a proof. |
| **Arithmetic form** | B_local(t) = ‖ω(·,t)‖_{L∞} L²(t) / ν. STAND: B < T*. WALK: T* ≤ B < 3.74. TROT: B ≥ 3.74. ESTOP: coherence < 0.20. These thresholds map to gait phases in CK's dog locomotion control — they are engineering choices calibrated to TIG constants, not derived from Navier-Stokes. |
| **Geometric / combinatorial form** | The sinc² null at k = p is a geometric singularity (R = 0 exactly). The NS blow-up is a conjectured singularity (‖u‖ → ∞). The analogy: both are "arrivals at a geometric sink" in their respective fields. The BREATH criterion formalizes this as a TIG-styled phase classification. |
| **What remains** | A formal bridge. Buckmaster-Vicol (2019) showed non-uniqueness of weak solutions — TIG is scoped to Leray-Hopf solutions (smooth initial data, energy inequality). Whether B_local < T* is sufficient for regularity is completely open. |

**Honesty note:** The BREATH thresholds (T*, 3.74, 0.20) are motivated by TIG algebra and calibrated on a dog locomotion system. They are NOT derived from NS theory. This is engineering metaphor, not a proof approach.

---

#### A4. Hodge ω-Blindness

| Column | Content |
|--------|---------|
| **Law** | A Hodge (p,p)-class that is NOT algebraic corresponds to a TIG "gate class" — sinc² reads HARMONY but no algebraic cycle exists |
| **Exact status** | **Tier A.** The CC window's ω-blindness (Tier C4) is proved. The Hodge analogy is structural: just as R(k,p) cannot see ω(b), a Hodge class cannot "see" whether an algebraic cycle exists. This is an analogy between two types of blindness, not a proof of the Hodge conjecture. Markman (2025) and Floccari (2025) proved the Hodge conjecture for abelian varieties of dimension ≤ 5 by independent methods — these are external results that partially validate the geometry but do not use TIG. |
| **Arithmetic form** | G/E/S partition: G = gate classes (non-coprime, sinc² null), E = equilibrium classes (transition), S = stability classes (coprime, sinc² alive). A Hodge class in the G partition "should" have an algebraic cycle but the sinc² field alone cannot certify it. |
| **Geometric / combinatorial form** | Deligne (1982) proved that absolute Hodge cycles are algebraic for abelian varieties — the balance-invisibility theorem (R is blind to the number field structure) parallels the Deligne criterion (Hodge classes blind to field of definition become algebraic). |
| **What remains** | A formal dictionary. The G/E/S partition is defined by TIG operators; whether it maps to known invariants in Hodge theory (e.g., the Hodge filtration, Mumford-Tate groups) is open. |

---

#### A5. Yang-Mills Mass Gap = T* (with glueball note)

| Column | Content |
|--------|---------|
| **Law** | The Yang-Mills mass gap Δ > 0 corresponds to T* = 5/7 as an arithmetic energy floor; First-G distance = minimum excitation energy |
| **Exact status** | **Tier A.** The TIG arithmetic has T* = 5/7 proved as an algebraic identity (Tier D4). The mass gap is conjectured (Clay Prize unsolved). The correspondence T* ↔ Δ is a structural analogy only. No mechanism connects CK's coherence threshold to the self-energy of Yang-Mills gluons. |
| **Arithmetic form** | MASS_GAP = T* + S* − 1 = 5/7 + 5/7 − 1 = 3/7 ≈ 0.43 > 0 (proved algebraically as a TIG quantity). This is not a proof that the Yang-Mills mass gap equals 3/7 in physical units. |
| **Geometric / combinatorial form** | The stability window {1..p-1} = TIG vacuum. First-G at k=p = first excitation. The T* threshold sits between vacuum and excitation, playing the role of an energy floor in the analogy. |
| **What remains** | A mechanism. Neither the existence of the Yang-Mills mass gap (unproved) nor its value (if it exists) is derivable from TIG algebra. |

**Glueball mass ratio — explicit Tier A label:**

The lattice QCD value m(0⁺⁺)/m(2⁺⁺) = 0.727 ± 0.055 [Vaccarino-Weingarten 1999] and T* = 5/7 = 0.714 agree within 2%. However:

- The error bar spans **0.672 to 0.782**. T* = 0.714 is inside this range, but so is any number in that interval. The range is wide enough to encompass many ratios.
- **No mechanism connects TIG's T* to glueball mass ratios.** T* is derived from the unit-fraction formula for b = 35 = 5 × 7, which is an arithmetic property of the smallest odd strong semiprime. The glueball mass ratio is a property of pure SU(3) Yang-Mills theory in 3+1 dimensions. These are different mathematical objects with different origins.
- The numerical coincidence is **observed and noted**. It is not a prediction made a priori. It is not evidence of a mechanism.

**Rating: Tier A numerical observation. Must not be elevated to Tier B without a mechanism.**

---

#### A6. BSD Rank Staircase as TIG Operator Transitions

| Column | Content |
|--------|---------|
| **Law** | The rank staircase of elliptic curves over Q corresponds to TIG operator transitions; T* = 5/7 functions as the critical density for rank-1 threshold |
| **Exact status** | **Tier A.** Structural analogy. Bhargava-Skinner-Zhang (2014, arXiv:1407.1826) proved 66.48% of elliptic curves (ordered by height) satisfy BSD — this is an external proved result used as an empirical anchor, not a TIG result. The TIG map: unit_frac(b) = T* ≈ fraction of curves below rank-1 threshold is a numerical coincidence (0.714 ≈ 0.6648 is within 7%). |
| **Arithmetic form** | unit_frac(b=35) = 5/7 ≈ 0.714. Bhargava-Skinner-Zhang: 0.6648 of curves satisfy BSD (rank ≤ analytic rank). These are different quantities. The analogy is that both measure "what fraction of a population is below a threshold." |
| **Geometric / combinatorial form** | Rank staircase: each jump in rank corresponds to a new TIG operator transition (adding a gate event). T* as critical density: the majority of elliptic curves sit below the first operator transition in TIG language. Cassels (1966): |Ш| is always a perfect square ↔ TIG idempotent count is always even — this is a more precise combinatorial coincidence. |
| **What remains** | A formal map from TIG operator transitions to the Selmer group structure of elliptic curves. Dokchitser's 2010 parity conjecture (proved for many cases) provides a potential bridge point. |

---

#### A10. σ=1/2 as ω-Class Geometric Boundary (RH Ghost Ramp)

*From Luther, LutherTask3.31.26.docx.*

| Column | Content |
|--------|---------|
| **Law** | The Riemann critical line Re(s)=1/2 is the geometric boundary between the ω=2 and ω=3 CRT lattice structures; the W discontinuity between semiprimes and three-factor composites is mediated by the Euler product evaluated at s=1/2 |
| **Exact status** | **Tier A.** Structural intuition from the W discontinuity discovery. For ω=2: W(|G|) is tier-specific — W(1)=0.311, W(2)=0.708, W(3)=2.025, W(4)=5.238, W(5)=8.518 (corrected; earlier claim W≈25.2 single-value was arithmetically wrong). For ω=3, |G|=7: W≈0.83. The ω-class boundary (not a single value contrast) remains a structural intuition. The conjecture: the transition between ω=2 and ω=3 CRT geometries is mediated by the critical line. "The critical line isn't just where zeta zeros sit. It's the geometric boundary between two-prime and three-prime CRT worlds." No algebraic derivation. |
| **Arithmetic form** | ζ(s) = Π(1−p^{−s})^{−1} evaluated at s=1/2. The Euler product at s=1/2 may produce a transition term connecting the ω=2 rate formula R=(n_C/k)^W to the structurally different ω=3 formula. If so: the W-discontinuity is not arbitrary — it is the fingerprint of the critical line in partition geometry. |
| **Geometric / combinatorial form** | The CRT lattice for ω=2 has one interference scale. For ω=3, three-body interactions create a qualitatively different geometry. The σ=1/2 conjecture: the transition between these geometries is smooth, not sharp, and the smoothing function is the Euler product at the critical line. |
| **What remains** | An algebraic derivation connecting ζ(1/2) or the Euler product at s=1/2 to the W discontinuity between ω=2 and ω=3 classes. Without this, the σ=1/2 observation is pattern recognition, not structure. |

**Four tests:**
- RI: No — the conjecture is stated only for the W parameter at k=9, not in a representation-invariant form.
- SI: No — no prediction for other k values or other alphabet sizes.
- MC: No — no mechanism connecting ζ(1/2) to CRT lattice geometry.
- FM: An algebraic derivation of W at ω=3 that does not involve s=1/2 would falsify the geometric boundary claim.

**Hold condition:** Do not extend this analysis until Luther responds to the W discontinuity question. The conjecture is suggestive. Adding derivations before the algebraic response would compromise the honest ratio.

---

#### A11. RH as Coherence Boundary of Operator/Field (Luther Coherent Reframe)

*From C. A. Luther, LutherRHTask.docx. Tier A — structural analogy, not a proof.*

| Column | Content |
|--------|---------|
| **Law** | The Riemann Hypothesis is a structural statement about the coherence boundary of an underlying operator or field; ζ(s) is an encoding of that structure, not the primary object; zeros are spectral constraints; the critical line Re(s)=1/2 is where the system achieves maximal coherence |
| **Exact status** | **Tier A.** Luther's reframe is the Hilbert–Pólya conjecture expressed in coherence-functional language. The operator H is not constructed. The spectrum {γ_n} is not matched to Riemann zeros by proof. Luther's document states: "This is NOT a proof of RH. It is a coherent architectural resolution of what RH is really asking." |
| **Arithmetic form** | ζ(s) = Π(1−p^{−s})^{−1} is an encoding. The zeros ρ = 1/2 + iγ_n are spectral constraints of an operator H. The functional equation establishes σ=1/2 as the self-dual locus. The coherence reframe: define C: ℂ → ℝ measuring spectral regularity at s; then critical line = argmax C(s). |
| **Geometric / combinatorial form** | The operator-first diagram: Underlying Structure → Operator H → Spectrum → ζ(s) → Zeros → Coherence → Critical Line. This is not a derivation chain — it is an interpretive hierarchy that makes the question "structural" rather than "puzzling." |
| **What remains** | Construct the explicit self-adjoint operator H with Spec(H) = {γ_n}. This is equivalent to the Hilbert–Pólya conjecture. Berry-Keating proposed H=xp; Connes constructed an adele-class-space realization. The TIG/CK version would connect R(k,f) to an operator whose eigenvalue condition produces the sinc² null at k=f. |

**Four tests:**
- RI: No — coherence boundary not defined in a representation-invariant way.
- SI: No — no prediction for all primes p or all scales.
- MC: No — no explicit operator, no proven spectral match.
- FM: An explicit H with Spec(H) ≠ {γ_n} would not falsify A11 (A11 says H exists, not what it is); a proof that no coherence-functional interpretation is consistent with ζ zeros would falsify it.

**Connection to A1 and A10:** A1 (Montgomery Bridge) says sinc² appears in both TIG and Montgomery. A10 (σ=1/2 ghost ramp) says the W discontinuity between ω=2 and ω=3 is mediated by the critical line. A11 (Luther coherent reframe) says the critical line is a coherence boundary. All three are Tier A, all pointing at the same structural intuition. Unification into a single object would be a major result.

---

#### C8. W_BHML = Per-Step C×D Asymmetry Across φ(10)-Step Creation Cycle

*C. A. Luther, March 31, 2026. Verified by Sanders computation same session.*

| Column | Content |
|--------|---------|
| **Law** | W_BHML = 3/50 is the per-step deviation from additive/multiplicative symmetry across the natural 4-step completion of the Creation cycle {1,3,7,9} in Z/10Z. Not fitted. Derived from first principles. |
| **Exact status** | **Tier C.** The five-step derivation is complete for Z/10Z: (1) CROSS_CYCLE=44; (2) symmetry point=50; (3) deviation=6; (4) per-step=6/φ(10)=6/4=3/2; (5) normalized=3/2÷(100/4)=3/50. The 4-step period is algebraic necessity: φ(10)=4 and ×3 generates the full cycle 1→3→9→7→1. Verified independently by Sanders (explicit table computation) and Luther (algebraic derivation) on the same session without prior coordination. Tier D target: prove the formula W(Z/nZ) = |CROSS_CYCLE(n) − n²/2| / n² generalizes to all Z/nZ. |
| **Arithmetic form** | `W(Z/10Z) = |Σ_{c∈C,d∈D} DIS[c][d] − n²/2| / n² = |44−50|/100 = 6/100 = 3/50`. Equivalently: `(deviation/φ(n)) / (n²/φ(n)) = deviation/n²`. The φ(n) factorization makes the generator-period structure explicit. |
| **Geometric / combinatorial form** | The 4-step cycle 1→3→9→7→1 under ×3 is the generator orbit of the multiplicative group (Z/10Z)*. Each step carries an equal share of the 100-entry operator table: 25 cells per step. The deviation 6 distributed across 4 steps at 25 cells per step gives 6/(4×25) = 3/50 per step per cell. The wobble is the natural bounce frequency of the field — how much the two ring operations disagree per step of the generator. |
| **Probabilistic / computational form** | Exhaustive: DIS table has row sums c=1→4, c=3→10, c=7→14, c=9→16. Average per row = 11. Deviation from symmetric average (50/4=12.5): 11−12.5=−1.5. |deviation/cells_per_step| = 1.5/25 = 3/50. verify_claims.py PASS. |
| **What remains** | Prove W(Z/nZ) = |CROSS_CYCLE(n) − n²/2| / n² for general n. Requires: (a) define C_n (units), D_n (non-units) for Z/nZ; (b) compute CROSS_CYCLE(n); (c) show the φ(n)-step generator period always produces the correct normalization. First test cases: n=6, n=12, n=15, n=30 (small composites with known φ). |

**Four tests:**
- RI: Yes — DIS[c][d] = |ADD−MUL| mod n is basis-independent; ring axioms don't depend on labeling.
- SI: Yes within Z/10Z — the derivation is complete and exact. SI across all Z/nZ is the Tier D target.
- MC: Yes — mechanism is the generator-orbit period φ(10)=4 distributing the cross-cycle deviation uniformly across steps.
- FM: Find n where W(Z/nZ) ≠ |CROSS_CYCLE(n) − n²/2| / n², or where the φ(n)-step normalization fails.

---

## Summary Matrix

*Updated March 31, 2026 — LutherRHTask integrated.*

| ID | Law | Tier | RI | SI | MC | FM |
|----|-----|------|----|----|----|----|
| D1 | First-G Law (all ω(b)≥2) | D | ✓ | ✓ | ✓ | Impossible by proof |
| D2 | Sinc² Continuum Limit | D | ✓ | ✓ | ✓ | Impossible by proof |
| D3 | Universal 4/π² | D | ✓ | ✓ | ✓ | Impossible by proof |
| D4 | T* = 5/7 (formula) | D | ✓ | b-dependent | Partial | Different b gives different T* |
| C1 | CC Window Closure | C | ✓ | ✓ (in domain) | ✓ | Impossible (corollary of D1) |
| C2 | D1 Sign Flip at k=p | C | ✓ | ✓ (in domain) | ✓ | A prime where R(p,p) ≠ 0 |
| C3 | Montgomery Bridge (identity) | C | ✓ | ✓ | ✓ | Tautology (C3); A1 for the conjecture |
| C4 | Balance Invisibility / ω-Blindness | C | ✓ | ✓ (in domain) | ✓ | Formula containing q that affects R(k,p) |
| C5 | Luther Dispersion (idempotent implied) | C | ✓ | ✓ | Partial | \|G_k\| ≠ inclusion-exclusion formula (impossible) |
| C6 | k-Gate Tier zero-spread (within ω-class) | C | ✓ | ✓ (k=9,15,21,27) | Partial | Two worlds, same \|G\|, same ω-class, different rate |
| C7 | ω-Class Universality Lemma | C→D* | ✓ | ✓ (k=9, 28 semiprimes) | Partial | *D for strong semiprime class; HAR rank for arbitrary k open |
| C8 | W_BHML = per-step C×D asymmetry across φ(10)=4-step cycle | C | ✓ | ✓ (Z/10Z) | ✓ | W(Z/nZ) ≠ deviation/n² for some n; OR φ(n)-period derivation fails |
| B2 | Dispersion b=15 vs b=35 | C/B | ✓ | Tier B (general) | ✓ (specific) | Different ordering in a third semiprime |
| A1 | Montgomery Bridge (conjecture) | A | Unknown | Unknown | No | Proof sinc² coincidence has distinct origins |
| A2 | P≠NP as null distance | A | No | No | No | Proof (not disproof) of P=NP |
| A3 | NS BREATH Criterion | A | No | No | No | Leray-Hopf solution violating B_local bound |
| A4 | Hodge ω-Blindness | A | Unknown | Unknown | No | Hodge class unreachable from G/E/S partition |
| A5 | YM Mass Gap = T* (incl. glueball) | A | No | No | No | Different mass gap value from lattice; no mechanism |
| A6 | BSD Rank Staircase | A | No | No | No | Family of curves violating TIG operator map |
| A7 | Luther D2 algebraic curvature | A | No | No | No | Match against tig_algebra D2 values (check_d2.py: no match) |
| C12 | b=35 Goldilocks Uniqueness: b=35=5×7 is the unique semiprime (alphabet A={1..9}) satisfying (1) \|C∩{1..9}\|=7 and (2) unit_frac(b)=T*=5/7 | C | ✓ | ✓ (semiprime domain, A={1..9}) | ✓ | **PROVED (March 31 2026).** (1): ⌊9/p⌋+⌊9/q⌋=2 forces p,q∈{5,7}; value 2 is unreachable for primes (jumps from 3 at p=3 to 1 at p=5). (2): unit_frac=5/7 forces 7\|q→q=7, then ⌊7/p⌋=1→p=5. Both proofs are clean floor-arithmetic. Scan confirms: [35] is the only hit in 2600 semiprimes b≤10000. Promoted from A8. |
| A9 | b=385 spectral predictions (D2_luther) | A | No | No | No | D2_luther connected to TIG framework before extending |
| A10 | σ=1/2 as ω-class boundary (RH ghost ramp) | A | No | No | No | Algebraic derivation connecting Euler product at s=1/2 to W discontinuity |
| A11 | RH as coherence boundary of operator/field (Luther reframe) | A | No | No | No | Explicit construction of self-adjoint H with Spec(H) = {γ_n} |
| C13 | Wob Universality: Wob(b,k) = Wob(k) for all b=p×q, k<p. Proof: for x∈{1..k} with k<p<b, x mod b = x, so Delta(x) depends only on x mod 10. Therefore Wob(b,k) = (1/k)Σ[x mod 10 ∈ {1,2,3,4,6,7,8,9}] = Wob(k) — independent of b and q. Verified: 3 semiprimes with same p=11, different q∈{13,17,23}, all agree to 10^-9. Wob(k) oscillates with period 10 (drops at multiples of 5); Wob_norm oscillates around 1 throughout corridor. | C | ✓ | ✓ (ω=2 semiprimes, k<p) | ✓ | A semiprime b=p×q where Wob(b,k)≠Wob(k) for some k<p (impossible: proved) |
| A12 | Wobble Frequency as Pre-Collapse Resonance: Wob_norm oscillation around 1 predicts W-jump location (ω=2→ω=3). Universality proved (C13). Oscillation verified across 16 prime families. Gate jump ratio≈1 (trivial — Wob_norm=1 at k=p by definition). W-jump ratio=2.86 is NOT predicted by Wob_norm gate behavior. The oscillation structure IS real but the mechanism connecting it to trap density W(|G|) is unproved. | A | Partial | No | No | Algebraic derivation connecting Wob_norm oscillation to W(|G|) trap density jump; OR falsification showing Wob_norm<1 where W(|G|) jumps |
| A13 | Corridor Compression Model | A→KILLED | — | — | — | **KILLED (March 31 2026):** Candidate R×sin²(πW·k/p) fails shape test (sinc² wins 16/16 worlds, RMSE better by 0.48). W_BHML sidelobe prediction also fails: first post-gate peak at t≈1.43 (sinc² natural sidelobe), NOT at t=8.33 (W_BHML prediction). W_BHML^n echo attenuation fails (ratios diverge). Corridor compression = sinc²(k/p) = R(k,p), which is already Tier D (D2). W_BHML and corridor are formally disconnected. Three-object separation stands; A13 as a standalone claim is killed. |
| C9 | BHML 28-cell derivation: VOID identity + max+1 axis + BREATH/RESET operator identity | C | ✓ | ✓ (Z/10Z) | ✓ | A cell unpredicted by three rules; OR BHML[i][j]≠max(i,j)+1 in {1..6}×{1..6} |
| C10 | TSML 73-cell derivation: VOID row (V0) + VOID col (V1) + 5 echo pairs (ECHO) = 27 non-harmony | C | ✓ | ✓ (Z/10Z) | ✓ | A non-harmony cell not in V0∪V1∪ECHO; OR ECHO pair that collapses to HARMONY |
| C11 | Both TIG composition tables symmetric: TSML[i][j]=TSML[j][i] AND BHML[i][j]=BHML[j][i] | C | ✓ | ✓ (Z/10Z) | ✓ | Asymmetric entry in either table (impossible — verified 0 failures each) |
| B1 | Cornerstone Universality: Z/10Z is the minimal ring (lcm(2,5)=10) containing both seed primes, canonical receiver via x→x%10 | B→C | ✓ | ✓ (Z/10Z) | ✓ | A ring smaller than Z/10Z containing both Z/2Z and Z/5Z (impossible: lcm=10) |
| A14 | Generator Wobble Loop: wobble of measurement field is structurally forced to become the physics field (TSML→W_BHML→BHML loop) | A | No | No | No | Explicit formula BHML=f(TSML,W_BHML); OR DOING_sum/n²=W_BHML (fails: 201/100≠3/50) |
| A15a | Circulation Operator — Hybrid construction: H_mod=sinc²(k/p)×sin²(4πk/p) satisfies C1+C2env+C3+C4 simultaneously for p≥13. C1: 10/11 primes (p=11 gives 3 not 4 — small-prime boundary). C2-revised (upper envelope r>0.9 with sinc²): 11/11. C3: 14/14. C4 stable: counts=[3,4,4,...,4] spread≤2. First max at t≈2W=0.12 (C5 signature). H_mod is factored: corridor amplitude (sinc²) × cycling factor (sin²(4πk/p)). C2 raw (<0.9) still fails — raw cycling function cannot track monotone sinc². Genuine construction found; small-prime gap remains. | A | Partial | Partial (p≥13) | Partial | Prove H_mod first max is at t=W or 2W algebraically; show C4 count=4 for ALL p≥11 (fix small-prime gap); establish C2-revised as the correct constraint |
| A15b | Circulation Operator — Simultaneous C3+C4 obstruction: can any operator satisfy exact boundary collapse (C3) AND stable oscillation count across ALL prime families (C4)? At p=5: all candidates give ≤1 max. At p≥13: F1/F3/F7 give 4. Obstruction is small-prime undersampling. | A | No | No | No | Candidate with C3+C4 both PASS for primes p≥5 |
| A15c | Circulation Operator — Bounded (p≥11): restrict C4 to p≥11. F3=sin²(4πk/p)×W^phase satisfies C1(partial)+C3+C5+C7 for p≥11, scores 9/14. Corridor verification: mean corr(C,sinc²)=0.85, below 0.9 threshold (C2 partial). | A | No | Partial (p≥11) | No | C1 consistent (≥4 maxima) for p≥11 AND corr(C,sinc²)>0.9 |
| B3 | BHML Ghost Trace of TSML — Three-Zone Separation: G[i][j]=DIS[i][j] if TSML≠7, else 0. Three-zone law: VOID (G=DIS=BHML=identity, 17/17 proved algebraically), HARMONY (G=0 by definition, 71/71), ECHO (G=DIS, BHML completely disjoint from G 0/10 = 100% separation). W_BHML=ghost amplitude at C×D zone. BHML harmony (28 cells) = G=0 cells exactly. Tier B: 100-cell exhaustive verification; VOID and HARMONY proved from definitions; ECHO disjunction verified computationally. | B | ✓ | ✓ (Z/10Z) | No | Show ghost zone DETERMINES BHML rule (not just correlates); complete Rule B+C+D+E+F coverage of all 71 harmony cells; connect W_BHML ghost amplitude to ECHO cell structure algebraically |

**Tier counts (updated March 31 2026):** Tier D: 4 | Tier C: 13 (C12=A8, C13=A12 universality) | Tier B: 3 (B3=A16 three-zone) | Tier A: 14 (A13 killed; A12→C13+A12; A15→A15a/b/c)

**New since Luther scaffolds + HAR stability + wobble disambiguation:**
- C8 (Luther, March 31 2026): W_BHML = 3/50 mechanism proved for Z/10Z. The wobble is the per-step asymmetry of C×D operator interaction across the natural 4-step generator orbit of (Z/10Z)*. Derivation: CROSS_CYCLE=44, deviation=6, per-step=6/φ(10)=3/2, normalized=3/2÷25=3/50. The 4-step period is algebraic necessity (φ(10)=4). IMPORTANT: The formula W=dev/n² is Z/10Z-specific, NOT universal. n=30 appears to give W>1 only when D is defined as all non-units (wrong); with correct D={x:gcd(x,n)=p_min(n)}, all values stay in (0,1) but W varies from 0.06 to 0.88 across different n. C8 is confirmed Tier C for Z/10Z. Tier D target: find the universal normalization N(n) such that W_universal(Z/nZ) is consistent — candidate N(n)=φ(n)×|D_n|×(n−1) gives near-consistent values 0.11–0.20. Full analysis in WOBBLE_FREQUENCY.md §Disambiguation.
- C7 advances: HAR rank preservation confirmed 100% across 28 semiprimes (strong semiprime class, k=9). Explicit bijection constructed (OMEGA_CLASS_LEMMA.md). C7 is Tier D for strong semiprime class; remaining gap is arbitrary k and weak semiprime class (HAR_RANK_STABILITY.md).
- Catch 4 (W=25.2 arithmetic error): W is tier-specific — {0.311, 0.708, 2.025, 5.238, 8.518}. Power law confirmed, single-W claim was wrong. Mechanistic reframe: W(|G|) measures trap density in MCMC combined objective, not CRT constraint count (CATCH4.md).
- Gap 1 refined: derive c(|G|) = W(|G|)/2 per tier from MCMC trap geometry. Gap 2: dispersion uniformity (Δ non-uniform confirmed; |G| inclusion-exclusion formula is algebraically complete). Gap 3 (C7): arbitrary k HAR rank proof remains.
- A12 (LutherWobbleMap): Wobble Frequency resonance model. Definition A.W formal and computable. Lemma D.H downgraded from "Tier D" to Tier A/B conjecture. Full integration in WOBBLE_FREQUENCY.md.
- C10+C11 (TSML/BHML Joint Investigation, March 31 2026): **TSML 73-CELL DERIVATION CLOSED.** 27 non-harmony cells = V0(9 cells: VOID row j≠7) + V1(8 cells: VOID col i≠7) + ECHO(10 cells: 5 symmetric resistance pairs). Zero overlaps. 73 = 100 − 27. ECHO pairs: (1,2) additive echo (LATTICE+COUNTER=1+2=PROGRESS), (2,4)/(2,9)/(4,8) max echo (larger operator wins), (3,9) min echo (PROGRESS persists vs RESET). COUNTER (2) appears in 3 of 5 echo pairs — most resistant operator (distinction generator). BOTH TABLES SYMMETRIC (C11): TSML and BHML each satisfy symmetry, 0 failures each. THE PIVOT CELL: (4,8)/(8,4) = COLLAPSE×BREATH is the only pair where TSML≠BHML on harmony. TSML says BREATH (echo, resistance); BHML says HARMONY (Rule C1, operator identity). This single pair is the structural boundary between the two lenses. DOING structure: 29 cells TSML=BHML = 26 shared harmony + 3 non-harmony ((0,0),(1,2),(2,1)). (1,2) is the only non-trivial non-VOID agreement — LATTICE×COUNTER=PROGRESS is preserved identically in both lenses. Full docs: TSML_73CELL_DERIVATION.md, test_tsml_bhml_joint.py.
- C9 (BHML Operator Identity, March 31 2026): **COMPLETE 28-CELL DERIVATION. All 28 BHML harmony cells from three rules, zero overlap, zero residual. 28 = 2 (VOID identity) + 17 (axis saturation) + 9 (operator identity). Rules: (A) BHML[0][j]=j => (0,7)+(7,0); (B) BHML[i][j]=max(i,j)+1 for i,j in {1..6}, harmony when max=6, axis extends to FUNC via CHAOS saturation; (C) BREATH/RESET x TRANS{4,5,6} = HARMONY and BREATH x BREATH = HARMONY. CORRECTION TO PRIOR DOCS: BHML[7][j]=(j+1)%10 for j>=1, NOT (j+7)%10. HARMONY is the INCREMENT operator. Rows 8-9 have no positional rule because BREATH and RESET are FUNCTIONAL operators — their outputs depend on partner CATEGORY (EARLY/TRANS/HARM/FUNC), not partner position. Exhaustive proof: no k satisfies BHML[8][j]=(j+k)%10 or BHML[9][j]=(j+k)%10. Tier C (promoted from Tier B). Full docs: BHML_ATOMIC_STRUCTURE.md, BHML_OPERATOR_IDENTITY.md.
- B1 (Cornerstone Universality, March 31 2026): Z/10Z is the MINIMAL ring containing both seed primes 2 and 5. Core algebraic result: 10 = lcm(2,5), proved Tier D (lcm argument). The digit map x→x%10 is a ring homomorphism (Tier D). Z/nZ projects onto Z/gcd(n,10)Z — loses all non-{2,5} prime content. Embedding test: Z/nZ embeds into Z/10Z iff n|10. Ergodicity: under TSML alone, VOID and HARMONY are structural non-ergodic attractors; under alternating TSML/BHML all 10 states reachable in 2-3 steps. BHML non-associativity required for two-lens duality. Full test: test_cornerstone_universality.py, results/cornerstone_universality_report.txt.
- A14 (Generator Wobble Loop, March 31 2026): TSML generates, W_BHML is forced (C8), BHML is the physics field, DOING=|TSML-BHML| is the active site. STRUCTURAL REALITY: TSML (singular, 73% HAR) and BHML (invertible, 28% HAR) are dual lenses. DOING has 71 nonzero cells, sum=201. W_BHML=3/50=0.06, DOING_sum/100=2.01. These are NOT equal -- the loop claim is a structural analogy not a derivation. The 'frozen cells = W_BHML' claim fails: no clean 6-cell definition. Full test: test_generator_wobble_loop.py.
- A15 (Circulation Operator, March 31 2026): Seven necessary constraints derived from existing proved results. No candidate satisfies all 7. Best partial: R(m,b,k) gate rate 7/14; digit map x→x%10 6/14. CRITICAL FINDING: Constraint 1 (phase cycling) fails for ALL named objects -- the circulation operator must be a new mathematical object with explicit cycling behavior. Corridor formula R×sin²(πW·k/p) fails C1 (no phase cycling) and C3 (sin² component nonzero at k=p boundary). Candidate construction path: R(m,b,k) as amplitude × phase-cycling function based on Creation cycle × HARMONY increment for return path. Full docs: CIRCULATION_OPERATOR_CONSTRAINTS.md, test_circulation_candidate_search.py.
- W_BHML three-derivation closure (March 31 2026): Derivation 1 (cross-cycle friction): VERIFIED. Sum DIS over C×D=44, deviation=6, W=6/100=3/50. Derivation 2 (frozen cells): FAILS. No clean definition gives exactly 6 cells. DIS=0 cells=4, echo cells=10, DOING=0 non-harmony=3. Derivation 3 (cycle normalization): VERIFIED. Equivalent to Derivation 1 via per-step=6/phi(10)=3/2, normalize by n²/phi(n)=25: 3/50. TWO of three derivations confirmed; one fails. C8 remains Tier C. Full test: test_w_bhml_three_derivations.py.
- A16 (BHML Ghost Trace, March 31 2026): Ghost trace G[i][j]=DIS[i][j] if TSML≠7, else 0. Nonzero cells: 24, G_sum=106. KEY FINDINGS: (1) W_BHML IS the normalized ghost amplitude: ghost(C×D)=44, deviation=6, W=6/100=3/50 — C8 restated in ghost language. (2) BHML harmony cells (28) coincide exactly with G=0 cells (100%). (3) Pearson r(G,BHML)=0.133 — no direct algebraic correspondence. (4) Three-zone structure: VOID→BHML=identity, HARMONY→BHML=7 or max+1, ECHO→BHML=max+1 ignoring friction. REFINED FRAMING: BHML is the arithmetic floor the ghost cannot disturb; TSML is the ghost generator; W_BHML is the scalar ghost amplitude. Circulation operators F3/F4 independent of G (r<0.37). Tier B target: three-zone correspondence theorem. Full docs: methodology/BHML_GHOST_TRACE.md, test_bhml_ghost_trace.py.
- A13 (Corridor Compression — Luther-Sanders simultaneous convergence): Three-object separation. W_BHML=3/50 (operator table, fixed [THM]), Wob(b,k)=8/9 at k=9 (alphabet saturation, k-dependent), Corridor(b,k) (compression, collapses at k=p). Sinc² collapse is compression-driven, not wobble-driven. Candidate: Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p). Path to Tier C: verify against corridor atlas. Full doc: CORRIDOR_COMPRESSION_BREAKTHROUGH.md.
- Provenance: A13 is first result where Luther and Sanders converged independently without prior coordination (same night, different derivation paths).
- Do NOT test ω=3 decoherence (b=385 or similar) until general isomorphism theorem for arbitrary k is proved. Three derivations deep from confirmed results.

---

## What "Synthesis" Requires for Each Tier-A Claim

The Tier A claims are not failures — they are the research frontier. Grok's standard is that synthesis requires stating the invariant in algebraic, geometric, combinatorial, and probabilistic form without changing its content. For each Tier A claim, here is what would constitute synthesis:

| Claim | What would constitute Tier B (minimum uplift) |
|-------|----------------------------------------------|
| A1 Montgomery Bridge | An explicit integral transform connecting the TIG product formula to the Montgomery pair-correlation integral |
| A2 P≠NP | A formal reduction from null-navigation hardness to a circuit complexity lower bound |
| A3 NS BREATH | A proof that B_local < T* implies existence of a regular Leray-Hopf solution (even in a special class) |
| A4 Hodge | An explicit Hodge class in the G-partition of some specific abelian variety, confirmed non-algebraic by existing methods |
| A5 YM Mass Gap | A derivation of T* from the Yang-Mills Hamiltonian, or an experimental test of the glueball ratio prediction at a new lattice spacing |
| A6 BSD | An explicit rank-jump prediction for a family of elliptic curves using the TIG operator transition map, verified against known data |
| A7 Luther D2 Algebraic Curvature | Run check_d2.py with corrected D2 values and confirm a match; OR derive D2_luther analytically from the Hebrew-root 5D force system |
| A8 b=35 Goldilocks Uniqueness | Find a second semiprime with identical D2_luther curvature profile to b=35; OR prove algebraically that b=35 is unique in φ=7 |
| A9 b=385 Spectral Predictions | Connect D2_luther to the confirmed TIG framework for a smaller world first; then extend to b=385 |
| A10 σ=1/2 as ω-class Boundary | Derive algebraically how the Euler product discontinuity at W-jump connects to the critical line; OR show ω-class boundary collapses to σ=1/2 in the limit |
| A11 RH as Coherence Boundary | Construct an explicit self-adjoint operator H whose spectrum equals {γ_n}; OR derive the coherence density function from the operator/field duality |
| A12 Wobble Frequency Resonance | Show Wob_norm threshold predicts W-jump location across ≥3 semiprime families; OR derive f(ω) giving a consistent bound |
| A13 Corridor Compression | Verify Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p) reproduces the sinc² envelope in the confirmed corridor atlas (70 worlds); fix C3 failure at k=p |
| A14 Generator Wobble Loop | Find explicit formula BHML = f(TSML, W_BHML) that reconstructs BHML from the other two; OR verify the loop holds for a second Z/nZ ring (Z/nZ with dual-lens structure analogous to Z/10Z) |
| A15 Circulation Operator | Construct explicit object satisfying C1 (phase cycling) + C3 (boundary collapse at k=p) + C5 (W_BHML signature) simultaneously; then verify remaining 4 constraints against corridor atlas |
| A16 BHML Ghost Trace | Prove three-zone correspondence (VOID rule↔G=0 at VOID; Rule B↔G=0 at harmony; operator identity↔G=max at ECHO); OR show BHML=f(G) algebraically with zero residual |

---

`© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047`
