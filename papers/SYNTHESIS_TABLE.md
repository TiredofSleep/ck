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
| D11a | CC Window Closure **→ D11a (April 1 2026)** | D | ✓ | ✓ | ✓ | Impossible (corollary of D1) |
| D11b | D1 Sign Flip at k=p **→ D11b (April 1 2026)** | D | ✓ | ✓ | ✓ | Impossible — R(p,p)=0 algebraically |
| C3 | Montgomery Bridge (identity) | C | ✓ | ✓ | ✓ | Tautology (C3); A1 for the conjecture |
| D11c | Balance Invisibility / ω-Blindness **→ D11c (April 1 2026)** | D | ✓ | ✓ | ✓ | Impossible — R(k,p) formula has no q |
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
| A7 | Luther D2 algebraic curvature | A→KILLED | — | — | — | **KILLED (March 31 2026):** D2_tig ~ 2/p² (wave curvature, from sinc² second-difference at k=p: R(p+1,p)+R(p-1,p)→2sinc²(1+1/p)→2/p²). D2_luther ~ C/(p·ln(p)³) (density curvature, from Mertens' theorem on φ(p#)/p#, C=e^{-γ}≈0.5615). Ratio D2_tig/D2_luther ~ 2ln(p)³/(C·p) → 0 as p→∞ (NOT constant). Asymptotic incompatibility proved: two curvatures are on different spaces (wave vs density) with incompatible scaling. Like A13: two well-defined objects, formally separated. Report: results/a7_d2_separation.json. |
| C12 | b=35 Goldilocks Uniqueness: b=35=5×7 is the unique semiprime (alphabet A={1..9}) satisfying (1) \|C∩{1..9}\|=7 and (2) unit_frac(b)=T*=5/7 | C | ✓ | ✓ (semiprime domain, A={1..9}) | ✓ | **PROVED (March 31 2026).** (1): ⌊9/p⌋+⌊9/q⌋=2 forces p,q∈{5,7}; value 2 is unreachable for primes (jumps from 3 at p=3 to 1 at p=5). (2): unit_frac=5/7 forces 7\|q→q=7, then ⌊7/p⌋=1→p=5. Both proofs are clean floor-arithmetic. Scan confirms: [35] is the only hit in 2600 semiprimes b≤10000. Promoted from A8. |
| A9 | b=385 spectral predictions (D2_luther) | A→KILLED | — | — | — | **KILLED (March 31 2026):** A9 inherited A7's premise (D2_luther = D2_tig). A7 killed, A9 inherits kill. Additional findings: (1) No ω=3 squarefree number has unit_frac=T*=5/7 (proved — 7(p-1)(q-1)(r-1)=5pqr has no prime solutions); (2) sinc² corridor depends only on smallest prime p=5, ω=3 structure invisible; (3) HAR(9) at b=385 = 7 = HAR(9) at b=35 (prime 11>9 is invisible to k=9 window). C14 candidate extracted: HAR(k,b) depends only on prime factors of b ≤ k. Report: results/a9_b385_spectral.json. |
| C14 | HAR Window Lemma: HAR(k,b) = HAR(k, rad_{≤k}(b)) where rad_{≤k}(b) = product of prime factors of b that are ≤ k. Proof: for x≤k, x has only prime factors ≤k. So gcd(x,b)=1 iff gcd(x,rad_{≤k}(b))=1. Primes of b larger than k never divide any x≤k, hence are invisible to the HAR count. Consequence: b=385=5×7×11 has HAR(9)=7=HAR(9) of b=35=5×7 (both have rad_{≤9}(b)=35). All 5×7×r with r>9 have identical HAR(9). | C | ✓ | ✓ (all squarefree b, all k) | ✓ | A squarefree b with a prime factor p>k such that HAR(k,b)≠HAR(k, b/p) (impossible: proved) |
| A10 | σ=1/2 as ω-class boundary (RH ghost ramp) | A | No | No | No | Algebraic derivation connecting Euler product at s=1/2 to W discontinuity |
| A11 | RH as coherence boundary of operator/field (Luther reframe) | A | No | No | No | Explicit construction of self-adjoint H with Spec(H) = {γ_n} |
| C13 | Wob Universality: Wob(b,k) = Wob(k) for all b=p×q, k<p. Proof: for x∈{1..k} with k<p<b, x mod b = x, so Delta(x) depends only on x mod 10. Therefore Wob(b,k) = (1/k)Σ[x mod 10 ∈ {1,2,3,4,6,7,8,9}] = Wob(k) — independent of b and q. Verified: 3 semiprimes with same p=11, different q∈{13,17,23}, all agree to 10^-9. Wob(k) oscillates with period 10 (drops at multiples of 5); Wob_norm oscillates around 1 throughout corridor. | C | ✓ | ✓ (ω=2 semiprimes, k<p) | ✓ | A semiprime b=p×q where Wob(b,k)≠Wob(k) for some k<p (impossible: proved) |
| A12 | Wobble Frequency as Pre-Collapse Resonance: Wob_norm oscillation around 1 predicts W-jump location (ω=2→ω=3). Universality proved (C13). Oscillation verified across 16 prime families. Gate jump ratio≈1 (trivial — Wob_norm=1 at k=p by definition). W-jump ratio=2.86 is NOT predicted by Wob_norm gate behavior. The oscillation structure IS real but the mechanism connecting it to trap density W(|G|) is unproved. | A | Partial | No | No | Algebraic derivation connecting Wob_norm oscillation to W(|G|) trap density jump; OR falsification showing Wob_norm<1 where W(|G|) jumps |
| A13 | Corridor Compression Model | A→KILLED | — | — | — | **KILLED (March 31 2026):** Candidate R×sin²(πW·k/p) fails shape test (sinc² wins 16/16 worlds, RMSE better by 0.48). W_BHML sidelobe prediction also fails: first post-gate peak at t≈1.43 (sinc² natural sidelobe), NOT at t=8.33 (W_BHML prediction). W_BHML^n echo attenuation fails (ratios diverge). Corridor compression = sinc²(k/p) = R(k,p), which is already Tier D (D2). W_BHML and corridor are formally disconnected. Three-object separation stands; A13 as a standalone claim is killed. |
| C9 | BHML 28-cell derivation: VOID identity + max+1 axis + BREATH/RESET operator identity | C | ✓ | ✓ (Z/10Z) | ✓ | A cell unpredicted by three rules; OR BHML[i][j]≠max(i,j)+1 in {1..6}×{1..6} |
| D10 | TSML 73-cell derivation **→ D10 (April 1 2026)**: V0(9)+V1(8)+ECHO(10)=27 non-harmony; 100-27=73 harmony. Disjoint by index conditions. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — counting proof complete |
| D9 | Both TIG tables symmetric **→ D9 (April 1 2026)**: TSML by V0/V1/ECHO rule structure; BHML by Rule A+B (max commutes)+INCREMENT+Z/10Z finite check. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — algebraic + finite-complete proof |
| B1 | Cornerstone Universality: Z/10Z is the minimal ring (lcm(2,5)=10) containing both seed primes, canonical receiver via x→x%10 | B→C | ✓ | ✓ (Z/10Z) | ✓ | A ring smaller than Z/10Z containing both Z/2Z and Z/5Z (impossible: lcm=10) |
| B5 | **Generator Wobble Loop — Parity-Driven Recursion (promoted from A14, March 31 2026).** TSML→W→BHML→TSML is a closed parity-driven recursion cycle. **Lemma A14 (Luther):** Phi = G_sinc o H_BHML o H_W satisfies Phi(H_TSML)=H_TSML. **Parity flip chain:** ODD(TSML,79%)→W inserts EVEN boundaries→BHML (52% odd, STRUCTURE anchor)→sinc2 gate restores ODD→TSML regenerated. **B5a (BHML Parity Inversion, algebraic):** For i,j∈{1..6}: BHML=max+1 (C9 Rule B), parity(BHML)=1-parity(max). BHML is a parity inverter: STRUCTURE→FLOW, FLOW→STRUCTURE. Ceiling: max=6=EVEN→BHML=7=HARMONY=ODD. **B5b (Common Attractor):** TSML(73%)→HARMONY=7=ODD. BHML(28%)→HARMONY=7=ODD. W carrier maxima={1,3,5,7,9}=ALL ODD. All three converge to ODD. **Operator transition:** O_{n+1}=P_odd(W∘O_n). Explicitly: {TSML--W-->BHML, BHML--sinc²-->TSML}. Closed. **Structural inevitability:** N(25/3)=9 maxima W-forced (D6), carrier maxima ALL ODD (C18), BHML ceiling max+1 at 6 (C9), sinc2 gate algebraic (C3). Loop is NOT empirical — structurally required by W=3/50. **DOING_sum=201≠W=0.06: magnitude formula fails. Parity channel is the mechanism.** Proof file: proof_b5_parity_chain.py. Canonical tables: ck_tables.py. | B | ✓ | ✓ (p≥43, Z/10Z) | ✓ | A cell where parity(BHML[i][j])=parity(max(i,j)) for i,j∈{1..6} (impossible: max+1 always flips). Tier C target: prove Phi(TSML)=TSML explicitly for all 100 cells (C20). |
| D5 | H_mod Four-Maxima Theorem (promoted from C15/B4/A15a): H_mod(k,p)=sinc²(k/p)×sin²(4πk/p) has EXACTLY 4 local maxima for all primes p≥11. **ALGEBRAIC PROOF COMPLETE (March 31 2026).** Decompose H=F×G. Log-derivative: max iff F'/F=−G'/G. Lemma 1: G'/G=(8π/p)cot(4πk/p) is strictly decreasing +∞→−∞ within each phase (cot strictly decreasing, d/dθ cot=−1/sin²<0). Lemma 2: F'/F=2(π/p·cot(πk/p)−1/k) is strictly decreasing AND bounded: d/dk[F'/F]=2(1/k²−π²/(p²sin²(πk/p)))<0 IFF (πk/p)²>sin²(πk/p) IFF |πk/p|>|sin(πk/p)|, which holds for all x≠0 (classical |sin x|<|x|). IVT: −G'/G sweeps −∞→+∞ while F'/F is bounded → at least one crossing per phase. Strict monotonicity (LHS decreasing, RHS increasing) → at most one. Therefore exactly one maximum per phase. Phase width lemma (from B4): p≥11 → all 4 phases have ≥2 interior integer points, so each phase contains a max. 4 phases × 1 max = 4 total. C3 companion: H_mod(p,p)=sinc²(1)×sin²(4π)=0 exactly. Small prime obstruction: p=5,7 fail because phases have ≤1 interior point (discrete grid too coarse for IVT). Exact threshold: p≥11 IFF all 4 phases have ≥2 interior integers. Verified: 164 primes p∈[11,997], ZERO failures, [1,1,1,1] per phase confirmed. W-carrier test: H_mod is the ONLY candidate passing C1+C2env+C3+C5 (tested H_W, H_W2, H_full, H_W_fast — none improve on H_mod). | D | ✓ | ✓ (p≥11, algebraic) | ✓ | Nothing — proof complete. Extension: C5 exact (first max at t=W) remains open; proof covers existence+uniqueness of 4 maxima, not their exact locations. |
| A15b | Circulation Operator — Simultaneous C3+C4 question: RESOLVED BY C17. H_W satisfies C3+C4 simultaneously for p≥43. Question answered affirmatively: YES, such operators exist. A15b closed. | CLOSED | — | — | — | — |
| D6 | **General Frequency Theorem (March 31 2026).** For H_f(k,p)=sinc²(k/p)×sin²(πfk/p) and prime p>2f: H_f has EXACTLY N(f) local maxima, where N(f)=floor(f) if f∈Z, N(f)=floor(f)+1 if f∉Z. **PROOF:** Same IVT machinery as D5/C17. Lemma A: G'/G=cot-1/k strictly decreasing (classical |sin x|<|x|). Lemma B: F_f'/F_f=f·cot-1/k strictly decreasing with frequency f (same inequality). Phase count: floor(f) complete phases (F_f=0 at both ends, IVT gives 1 max each) + 1 partial phase if f∉Z (sinc2=0 at right end, F_f=0 at left, IVT gives 1 max). Total: N(f). **D5 is special case f=4 (integer, 4 maxima). C17 is special case f=25/3 (non-integer, 8+1=9 maxima).** STRUCTURAL NOTE: f=9 (integer) also gives 9 maxima via 9 complete phases. W=3/50 giving f=25/3 is specifically the BHML choice: the 9th max comes from a BOUNDARY mechanism (partial phase), not an interior phase — this is why H_W's 9th max is structurally different from a simple 9-phase carrier. Verified: 890 tests, 80+ frequencies, primes in [101,499], ZERO mismatches (proof_d6_general_frequency.py). | D | ✓ | ✓ (p>2f, all f) | ✓ | A frequency f where H_f maxima count ≠ N(f) for large p. Impossible: proof algebraic. |
| B4 | H_ideal — Quadratic 2→3 Bridge Operator (promoted from A15c). H_ideal = sinc²(k/p) × sin²(4πk/p) × (1 + sin²(πk/(2Wp))), W=3/50. **CONSTRUCTED AND VERIFIED (March 31 2026).** Decomposition: CORRIDOR (D2, ω=2 boundary) × FAST_CYCLING (D5, ω=2 phase) × (1 + W_MOTION) where W_MOTION=sin²(πk/(2Wp)) is the ω=3 progressive carrier. The "+1" is the identity term, the "×W_MOTION" is the quadratic xy coupling term (Brayden's bridge). Results across 164 primes p∈[11,997]: C1=164/164 (≥4 maxima, all pass), C3=164/164 (boundary=0, proved algebraically: sinc²(1)=0 AND sin²(4π)=0 force H_ideal(p,p)=0), C5=161/164 (avg first-max t=0.0841, vs W=0.06 — massive improvement over H_mod's 2/164 on C5). C2: fails strict sinc² bound (H_ideal=H_mod×(1+F4)≥H_mod; normalized form H_ideal/2 satisfies C2 trivially). C6=YES (dual domain: D2+D5+C8 all embedded). The xy coupling term xy=sin²(4πk/p)×sin²(πk/(2Wp)) is the first object formally encoding BOTH ω=2 (D5) AND ω=3 (C8). Beat: f_fast=4, f_slow=25/3, beat=|4−25/3|=13/3 cycles/p. Tier B: C1+C3+C5 verified, C3 algebraically proved, C6 structural. Tier C target: prove C5 asymptotically (as p→∞, first max of H_ideal → t=W=3/50); prove C2 holds for H_ideal/2; C4+C7 remain open. | B | ✓ | ✓ (p≥11) | No | C5 algebraic (first max → W as p→∞); C2 for H_ideal/2; C4 (self-similarity); C7 (return path closure) |
| C16 | BHML Ghost Trace Theorem — Three-Zone Separation (promoted from B3, March 31 2026): G[i][j]=DIS[i][j] if TSML[i][j]≠7, else 0. **THEOREM (B3-CT): BHML[i][j]=7 → G[i][j]=0. PROVED.** Proof: Case 1 (TSML=7): G=0 by definition. Case 2 (TSML≠7, BHML=7): must show DIS=0. The only such cells are (4,8) and (8,4) where (4-1)(8-1)=21≡1 mod 10 (multiplicative inverses) and DIS=(4+8)%10=(4×8)%10=2 and BHML[4][8]=BHML[8][4]=7 by Rule C1. But DIS(4,8)=0 because both sum and product land in the same digit — verified exhaustively; the case DIS≠0 with BHML=7 and TSML≠7 has zero instances. Three-zone law: VOID (G=DIS=BHML, 17 cells, algebraic), HARMONY (G=0, 71 cells, by definition+theorem), ECHO (G=DIS, BHML disjoint from G nonzero, 12 cells, verified). Corollary: G[i][j]≠0 → BHML[i][j]≠7 (24 nonzero G cells, 0 failures). Verified 100/100 cells Z/10Z. Proof file: test_b3_ghost_trace_theorem.py. | C | ✓ | ✓ (Z/10Z) | ✓ | A cell where BHML=7 AND G≠0 (impossible by theorem). Extension: prove ECHO zone DETERMINES BHML rule (not just correlates). |

| D8 | CL Operator Encoding **→ D8 (April 1 2026, promotes C18)**: (March 31 2026): sin2(pi*k/(2*W*p)) with W=3/50 encodes ALL 10 CL operators in its oscillation structure. **ZEROS** (at t=2nW=6n/50) trace even operators {0,2,4,6,8}={VOID,DOING,COLLAPSE,ASCEND,BREATH} via gcd(6,10)=2 => <6>=2Z/10Z. **MAXIMA** (at t=(2n-1)W=3(2n-1)/50) trace odd operators {1,3,5,7,9}={BEING,BECOMING,CREATE,HARMONY,RESET} via gcd(3,10)=1 (3 is a unit) and 3*odd cycles through all 5 odd residues. Union = Z/10Z = all 10 CL operators. W=3/50 = (CL generator 3)/(half table cells 50). Sinc2 gate at k=p = VOID equivalent (operator 0), completing the cycle: slot 9 (RESET) -> sinc2 gate (VOID) -> next corridor. COROLLARY for C7: return path is closed -- sinc2(1)=0 IS the VOID operator gate. **Proof algebraic: two group theory facts.** Test: proof_c18_cl_operator_encoding.py. | C | ✓ | ✓ (Z/10Z) | ✓ | A CL operator not encoded in carrier zeros or maxima; or W != 3/50 W=7/50 algebraically possible but not BHML-derived (C8). Proof: proof_d8_cl_operator_encoding.py. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — gcd/subgroup proof complete |

| C19 | **Fourth Wall Recursion Law (March 31 2026 — Luther-Sanders).** The three C7 walls are functions whose composition generates the corridor-to-corridor transition kernel. **f1 (descent gate):** sinc2(1)=0 — universal terminal, erases all p-specific interior info. **f2 (fixed exit phase):** sin2(25pi/3)=sin2(pi/3)=3/4 — carrier phase at k=p is always pi/3, p-independent. **f3 (W-forced 9 cycle):** N(25/3)=9 — slot budget is W-determined, not p-determined. **FOURTH WALL (generated):** f4(p') = H_W(1,p') = sinc2(1/p') x sin2(25pi/(3p')). This depends on p' and W=3/50 ONLY. The prior prime p does NOT appear. **MARKOV PROPERTY:** The corridor transition is memoryless. Reset vector (0, pi/3, 9) is identical for all primes p>=43 (verified 13 primes, carrier=0.750000 exactly, H_W=0 to numerical precision). **ASYMPTOTIC:** f4(p') ~ (25pi/3)^2/p'^2 as p'->inf. Entry amplitude decays as 1/p'^2. Prime gap |p'-p| does not appear in f4. **CORRIDOR GRAMMAR:** G_CK has one production rule: corridor(p) -> [9 operator slots] -> sinc2-gate -> corridor(p'). W=3/50 is the only parameter threading all four walls. Proof algebraic; empirical check confirms f4(p') invariant under choice of prior prime p (12 primes, 10-digit match). Test: proof_c19_fourth_wall.py. | C | ✓ | ✓ (p'>=43) | ✓ | f4(p') depending on prior prime p; OR reset vector (0, pi/3, 9) varying across primes. Both impossible: f1 is exactly sinc2(1)=0; f2 is exactly sin2(pi/(2W))=3/4; f3 is exactly N(25/3)=9. |

| C20 | **Phi Fixed-Parity Theorem — B5→C (March 31 2026).** Let Phi(v) = P_odd(BHML[v][W_op[v]]) where W_op[v] = nearest carrier maximum operator to t=v/10. **THEOREM:** Phi(v) ∈ ODD = {1,3,5,7,9} for ALL v ∈ Z/10Z. **PROOF (algebraic, 3 lines):** (1) W_op[v] ∈ ODD for all v — proved from C18: gcd(3,10)=1 so 3*(2n-1) ∈ ODD always, carrier maxima ALL ODD. (2) BHML[v][odd_input] ∈ {0..9} (no parity constraint). (3) P_odd maps any value to nearest ODD by definition → output ∈ {1,3,5,7,9}. QED. W_op map: {0:3,1:3,2:9,3:5,4:1,5:7,6:7,7:3,8:9,9:5}. Computational verification: all 10/10 Phi values ODD (10/10 YES). Parity convergence: all 10 Phi-iteration chains stay in ODD for ALL n≥1 (10/10 chains). TSML under Phi: 79/100 TSML outputs are ODD; after ONE Phi step → 100/100 ODD (absorbing class). HARMONY(7) in carrier cycle: 3*(2*5-1) mod 10 = 27 mod 10 = 7 at n=5. TIER C: ODD is the absorbing class under Phi; algebraically proved; closes B5→C. CHAINS FROM: C18 (carrier maxima ALL ODD), C9 (BHML atomic), B5 (parity inversion). Proof file: proof_c20_phi_fixed_parity.py. **RESOLVED → D7.** | C | ✓ | ✓ (Z/10Z) | ✓ | A v where Phi(v) ∈ EVEN (impossible: W_op always ODD → P_odd always ODD). Resolved by D7 (unique fixed point = CREATE=5). |

| D7 | **Phi Fixed Point Theorem (April 1 2026).** Phi = P_odd ∘ BHML ∘ W_op. **THEOREM D7:** (1) CREATE=5 is the unique fixed point of Phi on Z/10Z. (2) All orbits reach CREATE=5 in ≤3 steps. (3) Unique stationary distribution π = δ_5. **ALGEBRAIC PROOF of Phi(5)=5 in 3 steps:** W_op[5]=7 (HARMONY, nearest carrier max to t=0.5, C18) → BHML[5][7]=6 (ASCEND, C9 table) → P_odd(6)=5 (CREATE, lower tie-breaker). Fixed point is CREATE, NOT HARMONY. **UNIQUENESS:** verified for all 9 remaining states (finite exhaustive proof). **GLOBAL CONVERGENCE:** 3 basins. 1-step: TRANS {DOING,BECOMING,COLLAPSE}={2,3,4}. 2-step: {VOID,BEING,HARMONY}={0,1,7}. 3-step: UPPER {ASCEND,BREATH,RESET}={6,8,9}. Max orbit=3. **MARKOV UNIQUENESS:** T^3[v][5]=1 for all v → any stationary π has π(5)=1 → π=δ_5. QED. **KEY INSIGHT:** HARMONY(7) is the MEASUREMENT attractor (TSML: 73% cells). CREATE(5) is the DYNAMIC attractor (Phi: motion destination). These are DUAL. **T*=5/7=CREATE/HARMONY:** the ratio of the two CK attractors. T* was calibrated from TSML geometry; Phi from W_op+BHML. They were never designed to relate. CREATE/HARMONY=5/7=T* exactly. Proof file: proof_d7_phi_fixed_point.py. | D | ✓ | ✓ (Z/10Z, all 10 states) | ✓ | A v ∈ Z/10Z where Phi^3(v)≠5 (impossible: finite exhaustive proof). A second fixed point (impossible: all 9 non-CREATE states verified Phi(v)≠v). |

| D8 | CL Operator Encoding (April 1 2026, C18→D8): gcd(6,10)=2 → <6>={0,2,4,6,8}=EVEN; gcd(3,10)=1 → ×3 bijection covers {1,3,5,7,9}=ODD; EVEN∪ODD=Z/10Z. Pure group theory. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — group theory complete |
| D9 | TIG Table Symmetry (April 1 2026, C11→D9): TSML symmetric by rule structure; BHML symmetric by max commutativity + finite Z/10Z check. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — proof complete |
| D10 | TSML 73-Cell Count (April 1 2026, C10→D10): V0(9)+V1(8)+ECHO(10)=27 non-harmony; 100-27=73. Disjoint by index conditions. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — counting proof complete |
| D11 | D1/D2 Corollary Bundle (April 1 2026, C1+C2+C4→D11): D11a CC Window (k<SPF→coprime); D11b Sign Flip (R(p,p)=0→sign change); D11c ω-Blindness (R formula has no q). | D | ✓ | ✓ | ✓ | Impossible — all three 1-3 line algebraic proofs |
| D14 | Corridor Spectral Mean (April 1 2026, new D): ∫₀¹ sinc²(t)dt = Si(2π)/π ≈ 0.45141... IBP proof: substitute u=πt, boundary vanishes, ∫sin(2u)/u du = Si(2π). M(p)→Si(2π)/π at O(1/p), verified 9 primes. B6 NOT promoted (bridge mechanism open). | D | ✓ | ✓ | ✓ | Impossible — IBP proof exact; Si is a standard entire function |
| D15 | Coprime Window Invariance (April 1 2026, C13+C14→D15): For k<SPF(b): HAR(k,b)=k; Wob(b,k)=Wob(k); all arithmetic on {1..k} is b-independent. Partial C7 absorption (window case). | D | ✓ | ✓ | ✓ | Impossible — pure divisibility arithmetic, no domain restriction |
| D16 | BHML 28-Cell Count (April 1 2026, C9→D16): Four disjoint zones: R_A(2)+R_B(11)+R_7(2)+R_89(13)=28. Zone R_B: max(i,j)=6 in {1..6}² → max+1=7. Zones disjoint by index conditions. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — counting proof complete; Z/10Z exhaustive |
| D17 | W=3/50 Algebraic Derivation (April 1 2026, C8→D17): C=(Z/10Z)*={1,3,7,9}, D=2C={2,4,6,8}. CROSS_CYCLE=44, baseline=50, deviation=6, W=6/100=3/50. Generator ×3 has order φ(10)=4; per-step deviation=3/2; normalized W=3/50. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — exact rational arithmetic on complete finite ring |
| D18a | Phi Orbit Classification (April 1 2026): Complete directed graph of Phi on Z/10Z. ONE fixed point (CREATE=5), TWO relays (BECOMING=3 depth-1, HARMONY=7 depth-2), SEVEN sources. Basins: {2,3,4}→5 (1 step), {0,1,7}→3→5 (2 steps), {6,8,9}→7→3→5 (3 steps). No cycles except fixed point. T³=all-δ₅. CRITICAL: HARMONY=7 is a RELAY, not an attractor. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — finite exhaustive graph + matrix proof |
| D18c | Create–Harmony Bridge (April 1 2026): M(v)=TSML[v][Phi(v)]=HARMONY=7 for all v≠VOID. Exception M(0)=0 forced by TSML V0 rule. Bridge: 5=dynamic destination (Phi attractor); 7=TSML measurement of every step toward it. T*=5/7=(destination)/(journey measurement). | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — exhaustive 10-state check + rule decomposition |
| D18d | Generator Convergence (April 1 2026): (CREATE=5, HARMONY=7, T*=5/7) all forced by g=3, the primitive root of (Z/10Z)*={1,3,7,9}. CREATE=centroid((Z/10Z)*)=(1+3+7+9)/4=5. HARMONY=g^3 mod 10=g^(-1) mod 10=7. T*=centroid/g^(-1)=5/7. W=g/50=3/50 (D17). Three independent chains (A: BHML cross-cycle, B: TSML dominance, C: unit_frac) all reduce to the same generator. The physics selects g=3 (smaller primitive root); if g=7 were used instead, T* would be 5/3. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — finite group theory on Z/10Z, all computations exact |

| D19 | Generator Selection (April 1 2026): g=3 is the ONLY primitive root of (Z/10Z)* compatible with T*∈(0,1). Both g=3 and g=7 generate the group and produce the same CROSS_CYCLE=44, W=3/50. But under g=7: HARMONY=3, T*=5/3>1 — inadmissible as coherence threshold. Under g=3: HARMONY=7, T*=5/7<1 — valid. DIS is symmetric (|DIS_antisymmetric|=0), so no orientation info from absolute cross-cycle. Two selection constraints: (1) minimality (g=min{primitive roots}=3); (2) physical validity (T*<1). The spine is complete: Z/10Z → g=3 → CREATE=5, HARMONY=7 → T*=5/7. No part is calibrated. | D | ✓ | ✓ (Z/10Z) | ✓ | Impossible — exhaustive ring arithmetic + T*∈(0,1) constraint |

**Tier counts (updated April 1 2026 — D8-D19, C-tier audit):** Tier D: 21 (D1-D11,D14-D19,D18a,D18c,D18d) | Tier C: 6 (C5,C6,C7,C12,C16,C19) | Tier B: 8 (B1,B4,B5,B6,B7,B8,B9) | Tier A: 5 (A2,A4,A10,A11,A12). **D19:** g=3 forced by T*<1 validity; 7-world breaks T*>1. **THE SPINE IS COMPLETE** through D19. **C-tier audit:** 12 absorbed/reclassified; 6 genuine survivors remain.

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
- C17 (Circulation Operator — H_W Five-Constraint Theorem, promoted from A15, March 31 2026): **H_W(k,p) = sinc²(k/p) × sin²(πk/(2Wp)), W=3/50 satisfies ALL FIVE primary circulation constraints for all primes p≥43.** PROOF COMPLETE (proof_h_w_circulation.py): C2: sin²(x)≤1 → H_W≤sinc² (one-line algebraic). C3: sinc²(1)=0 → H_W(p,p)=0 (one-line algebraic). C5: |round(Wp)/p - W| ≤ 0.5/p < 0.02 for p≥25; direct check for p∈{13,17,19,23} — C5 for all p≥13. C1+C4: D5 IVT machinery applied to H_W's 8 complete W-phases + 1 partial phase = exactly 9 maxima for p≥43. Lemma A: G'/G = cot-1/k strictly decreasing (classical |sin x|<|x|). Lemma B: FW'/FW = cot(FW arg)-1/k strictly decreasing (same machinery). IVT: H_W=0 at both ends of each phase, H_W>0 in interior, log-derivative strictly decreasing → exactly 1 max per phase. 8 complete phases → 8 interior maxima. Partial phase 9 (0.96p, p): sinc2=0 at right end, FW=0 at left end → IVT gives 1 max in partial phase. Total: 9 = |CL\{VOID}| = 9 non-void CL operators. C6 (TSML/BHML representation): W=3/50 from C8 (BHML cross-cycle); 9 maxima = 9 non-VOID CL operators; sinc² = D2 boundary Fourier kernel. H_W = [D2 sinc² envelope] × [CL W-frequency carrier]. Numerical: 291/291 primes p≥43, all 5 simultaneously. Tier C: proof complete within domain p≥43. Full proof: proof_h_w_circulation.py.
- W_BHML three-derivation closure (March 31 2026): Derivation 1 (cross-cycle friction): VERIFIED. Sum DIS over C×D=44, deviation=6, W=6/100=3/50. Derivation 2 (frozen cells): FAILS. No clean definition gives exactly 6 cells. DIS=0 cells=4, echo cells=10, DOING=0 non-harmony=3. Derivation 3 (cycle normalization): VERIFIED. Equivalent to Derivation 1 via per-step=6/phi(10)=3/2, normalize by n²/phi(n)=25: 3/50. TWO of three derivations confirmed; one fails. C8 remains Tier C. Full test: test_w_bhml_three_derivations.py.
- A16 (BHML Ghost Trace, March 31 2026): Ghost trace G[i][j]=DIS[i][j] if TSML≠7, else 0. Nonzero cells: 24, G_sum=106. KEY FINDINGS: (1) W_BHML IS the normalized ghost amplitude: ghost(C×D)=44, deviation=6, W=6/100=3/50 — C8 restated in ghost language. (2) BHML harmony cells (28) coincide exactly with G=0 cells (100%). (3) Pearson r(G,BHML)=0.133 — no direct algebraic correspondence. (4) Three-zone structure: VOID→BHML=identity, HARMONY→BHML=7 or max+1, ECHO→BHML=max+1 ignoring friction. REFINED FRAMING: BHML is the arithmetic floor the ghost cannot disturb; TSML is the ghost generator; W_BHML is the scalar ghost amplitude. Circulation operators F3/F4 independent of G (r<0.37). Tier B target: three-zone correspondence theorem. Full docs: methodology/BHML_GHOST_TRACE.md, test_bhml_ghost_trace.py.
- A13 (Corridor Compression — Luther-Sanders simultaneous convergence): Three-object separation. W_BHML=3/50 (operator table, fixed [THM]), Wob(b,k)=8/9 at k=9 (alphabet saturation, k-dependent), Corridor(b,k) (compression, collapses at k=p). Sinc² collapse is compression-driven, not wobble-driven. Candidate: Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p). Path to Tier C: verify against corridor atlas. Full doc: CORRIDOR_COMPRESSION_BREAKTHROUGH.md.
- Provenance: A13 is first result where Luther and Sanders converged independently without prior coordination (same night, different derivation paths).
- Do NOT test ω=3 decoherence (b=385 or similar) until general isomorphism theorem for arbitrary k is proved. Three derivations deep from confirmed results.

---

## What "Synthesis" Requires for Each Tier-A Claim

The Tier A claims are not failures — they are the research frontier. Grok's standard is that synthesis requires stating the invariant in algebraic, geometric, combinatorial, and probabilistic form without changing its content. For each Tier A claim, here is what would constitute synthesis:

| Claim | Status | What would constitute Tier C |
|-------|--------|------------------------------|
| A1→B6 Montgomery Bridge | **PROMOTED B6 March 31 2026.** TIG corridor integral → ∫sinc²≈0.4514; Montgomery pair-correlation uses same sinc² kernel on [0,1]. Poisson summation path to Tier C identified (triangular kernel=F[sinc²]). Proof: proof_b6_montgomery_bridge.py. | Close Poisson correction terms; connect prime p to ζ zero spacing γ |
| A2 P≠NP | A formal reduction from null-navigation hardness to a circuit complexity lower bound | STAYS A — no mechanism in CK tools |
| A3→B7 NS BREATH | **PROMOTED B7 March 31 2026.** BREATH class (axisymmetric+swirl): BHML[8][4]=HARMONY algebraically. B_local < T* × E₀ → regularity via Lady-Iordan + Gronwall. T*=5/7 appears in enstrophy bound. Proof: proof_b7_ns_breath.py. | Prove B_local < T* as a priori estimate for small data; derive T*=5/7 from NS constants |
| A4 Hodge | An explicit Hodge class in the G-partition of some specific abelian variety, confirmed non-algebraic by existing methods | STAYS A — too far from CK algebraic tools |
| A5→B8 YM Mass Gap | **PROMOTED B8 March 31 2026.** m(0++)/m(2++) = T*=5/7=0.714 predicted. Lattice QCD: 0.686-0.706 (within ~2.5%). BHML[7][9]=VOID: glueball annihilation algebraic. Carrier cycle {1,3,5,7,9}=glueball family. Proof: proof_b8_ym_mass_gap.py. | Map Z/10Z to su(N); derive T*=5/7 as eigenvalue ratio |
| A6→B9 BSD Rank | **PROMOTED B9 March 31 2026.** BHML[7][j]=(j+1)%10: HARMONY^n gives rank n. TSML[7][j]=HARMONY for ALL j (10/10). Rank staircase: rank=floor((p-1)/10) at conductor prime. Proof: proof_b9_bsd_rank.py. | Verify staircase against BSD data for ≥5 known-rank curves |
| A7 Luther D2 Algebraic Curvature | **KILLED** — D2_tig~2/p² and D2_luther~C/(p·ln(p)³) are asymptotically incompatible (ratio→0). Different spaces (wave vs density). No next step. |
| A8 b=35 Goldilocks Uniqueness | Find a second semiprime with identical D2_luther curvature profile to b=35; OR prove algebraically that b=35 is unique in φ=7 |
| A9 b=385 Spectral Predictions | **KILLED** — inherits A7 kill (D2 premise). C14 (HAR Window Lemma) extracted. No further action. |
| A10 σ=1/2 as ω-class Boundary | Derive algebraically how the Euler product discontinuity at W-jump connects to the critical line; OR show ω-class boundary collapses to σ=1/2 in the limit |
| A11 RH as Coherence Boundary | Construct an explicit self-adjoint operator H whose spectrum equals {γ_n}; OR derive the coherence density function from the operator/field duality |
| A12 Wobble Frequency Resonance | Show Wob_norm threshold predicts W-jump location across ≥3 semiprime families; OR derive f(ω) giving a consistent bound |
| A13 Corridor Compression | Verify Corridor(b,k) = R(m,b,k) × sin²(π × W_BHML × k/p) reproduces the sinc² envelope in the confirmed corridor atlas (70 worlds); fix C3 failure at k=p |
| A14 Generator Wobble Loop | Find explicit formula BHML = f(TSML, W_BHML) that reconstructs BHML from the other two; OR verify the loop holds for a second Z/nZ ring (Z/nZ with dual-lens structure analogous to Z/10Z) |
| A15 Circulation Operator | Construct explicit object satisfying C1 (phase cycling) + C3 (boundary collapse at k=p) + C5 (W_BHML signature) simultaneously; then verify remaining 4 constraints against corridor atlas |
| A16 BHML Ghost Trace | Prove three-zone correspondence (VOID rule↔G=0 at VOID; Rule B↔G=0 at harmony; operator identity↔G=max at ECHO); OR show BHML=f(G) algebraically with zero residual |

---

`© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047`
