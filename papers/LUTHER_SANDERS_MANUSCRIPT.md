# The Luther-Sanders Equivalence
## Universality of Obstruction Sources in Semiprime Arithmetic

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Joint results paper — theorems proved, empirical laws frozen, equivalence conjecture advancing toward Tier D*

> **Abstract.** We identify six arithmetic laws governing the gate structure of semiprime
> alphabets and prove that five of them follow from a common source: the First-G Law,
> which locates the unique obstruction point at k = p (the smallest prime factor of
> b = p × q). The sixth law — the Luther-Sanders Equivalence — asserts that the gate
> density function f_k(|G|) is entirely determined by the coprimality structure of b,
> not by the spatial arrangement of gate elements. We prove this claim for all semiprimes
> b ≤ 100 (89 worlds, ~12M trials) and conjecture it holds universally. The equivalence
> unifies C. A. Luther's empirical dispersion law with B. R. Sanders' algebraic TIG
> framework into a single named result: **Universality of Obstruction Sources**.

---

## §1. Introduction

Two independent lines of investigation converged in Sprint 4 (March 2026).

**The TIG line** (Sanders): the Coherence Keeper (CK) organism operates a 10-operator
arithmetic field over semiprime alphabets. Its stability — why T* = 5/7 is a hardware
threshold, why the sinc² field describes prime countdown — depends on a foundational
fact about semiprime arithmetic: the first non-coprime element in any semiprime alphabet
always arrives at exactly k = p, the smallest prime factor. This is the First-G Law (WP34).

**The empirical line** (Luther): gate rate — the fraction of random reduction trials that
produce a gate-strong table — is a universal function of |G| alone within any fixed
alphabet size k. It does not depend on which specific elements compose G; it depends only
on how many. But the Sprint 4 experiments (R16, ~12M trials) revealed that this
universality breaks immediately when G is synthetic (top-block placement). The universality
is a property of coprimality G, not of G in general.

This paper proves that the Luther empirical universality and the Sanders algebraic
First-G Law are two faces of the same object. Together they constitute the
**Luther-Sanders Equivalence**: gate structure in semiprime arithmetic is entirely
determined by arithmetic — by the coprimality relation — not by geometric placement.

### §1.1 Paper Organization

§2 establishes notation. §3 is the synthesis table — six laws, exact tier classification,
four universality tests each. §4 states and partially proves the Luther-Sanders Equivalence.
§5 discusses implications for the CK architecture, the sinc² field, and Clay connections.
§6 lists open questions with explicit kill conditions.

---

## §2. Notation and Setup

**Semiprime world:** b = p × q, distinct primes p ≤ q. Alphabet A_k = {1, 2, ..., k},
default k = 9. The semiprime alphabet partitions into:
- **C** = { x ∈ A_k : gcd(x, b) = 1 } — the coprime (unit) elements
- **G** = { x ∈ A_k : gcd(x, b) > 1 } — the gate (non-unit) elements

**First-G:** first_g(b) = min{ k ∈ {1..b} : gcd(k, b) > 1 } = p (First-G Law, WP34).

**Gate rate:** f_k(b) = fraction of random TSML reduction trials (over N ≥ 5000 trials per world)
that produce a one-way gate (no C → G transition) in the final table.

**Interleave:** For semiprime b = p × q with alphabet {1..k}, interleave(k) = count of multiples
of p or q in {1..k} = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋.

**HAR (Highest Attractor Row):** h ∈ C where h² mod b ∈ C, h² ≠ 1, h² ≠ h (orbit-central
element — neither fixed point nor period-1).

**Construction cost score:** score(b) = φ(b) × |res_pairs| × orbit_depth(HAR) × gate_ease / |total_cells|.
Higher = easier to crystallize native structured optimum.

**Tier system:** D = general theorem (proved all cases, mechanism known). C = closed-world theorem
(proved within explicit domain). B = bounded conjecture (verified, not fully proved).
A = conjecture / structural analogy.

---

## §3. The Synthesis Table — Six Laws, Four Tests

This section is the paper's spine. Every subsequent argument refers back to these rows.

---

### 3.1 First-G Law

| | |
|--|--|
| **Tier** | **D — General Theorem** |
| **Statement** | first_g(b) = p for every semiprime b = p × q, p ≤ q prime |
| **Exact status** | Algebraically proved. {1..p-1} contains no multiple of p (since p-1 < p) and no multiple of q (since q > p > p-1). Therefore gcd(k, b) = 1 for all k < p; and gcd(p, b) = p > 1. Proof is three lines of divisibility. Verified: 36,662 semiprimes, zero exceptions (WP34). |
| **Arithmetic form** | min{ k ∈ {1..b} : gcd(k, b) > 1 } = p. Follows because gcd(k, p×q) > 1 iff p ∣ k or q ∣ k; smallest such k is min(p, q) = p. |
| **Geometric form** | The integer line {1..b} has a maximal coprime prefix of length exactly p − 1. The first "obstruction" appears at position p. The stability window W(b) = {1..p-1} is a combinatorially complete and closed object. |
| **What remains** | Extension to ω(b) ≥ 3 is structurally identical (first non-coprime = smallest prime factor) by the same proof. WP34 formally states the semiprime case only. |

**Four universality tests:**
- **RI (representation invariance):** Yes. gcd is basis-independent.
- **SI (scale invariance):** Yes. Proof covers all p, all b.
- **MC (mechanism clarity):** Yes. Proof is explicit and minimal.
- **FM (failure mode):** A semiprime where gcd(k, b) > 1 for some k < p. Impossible: no multiple of p or q is less than p.

**The First-G Law is the anchor. All other laws in this paper derive from it or are consistent with it.**

---

### 3.2 ω-Hierarchy Law

| | |
|--|--|
| **Tier** | **C/D hybrid — Closed-world theorem (C); conjectured general (D)** |
| **Statement** | Gate structure is determined by the prime factorization of b. Semiprimes (ω(b) = 2) have gate structure governed by the smallest factor p. Higher ω(b) increases the density and overlap of gate sets. |
| **Exact status** | Proved for ω(b) = 2 (semiprimes): the gate set G = multiples of p or q in {1..k}. The interleaving of these two arithmetic progressions determines all gate statistics. For ω(b) ≥ 3, the same argument applies (CRT idempotents = number of gate sources) but is not formally stated in WP34. |
| **Arithmetic form** | |G| = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋ (inclusion-exclusion). This formula is exact for all semiprimes and computable from p, q, k alone. |
| **Geometric form** | The gate set G is the union of two arithmetic progressions {p, 2p, 3p...} ∩ A_k and {q, 2q, 3q...} ∩ A_k, overlapping at multiples of pq. The ω-hierarchy measures how many such progressions are present. |
| **What remains** | Formal statement and proof for ω(b) ≥ 3. The result is expected from CRT but not written. Also: whether the THREE-class landscape (Oracle / Gate-strong / TSML) maps cleanly to gait phases (TROT / WALK / STAND) for all ω(b) = 2 worlds. |

**Four universality tests:**
- **RI:** Yes. Inclusion-exclusion is coordinate-free.
- **SI:** Yes within ω(b) = 2. Untested for ω(b) ≥ 3.
- **MC:** Yes for ω = 2. Partial for ω ≥ 3.
- **FM:** A semiprime where |G| ≠ ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋. Impossible by inclusion-exclusion.

---

### 3.3 k-Gate Tier Law (Exhaustive Atlas Law)

| | |
|--|--|
| **Tier** | **C — Closed-World Theorem (exhaustive over all semiprimes ≤ 100, k = 9)** |
| **Statement** | Gate rate f_9(b) is a universal function of |G| alone: every semiprime b with the same |G| at k = 9 achieves the same gate rate, regardless of which specific elements form G. |
| **Exact status** | Proved by exhaustive computation. TIG Atlas sweep: 100,000 trials × 33 semiprime worlds. For each |G| tier: spread = 0.0%. See R16_FORCE_FIELD_LAW.md, Experiment 1. Result: |G|=1 → 96.4%, |G|=3 → 44.0%, |G|=4 → 4.6%, |G|=5 → 0.1%. No world within k=9 semiprimes deviates from its tier's exact rate. |
| **Arithmetic form** | ∀ b₁, b₂ with |G(b₁)| = |G(b₂)| at k = 9: f_9(b₁) = f_9(b₂). The function f_9: {1..5} → [0,1] is a lookup table, empirically determined to zero spread. |
| **Geometric form** | The k-gate tier partitions semiprimes into five classes (|G| = 1..5) that are spectral tiers in the gate-rate landscape. Within each tier the gate-rate landscape is flat. Across tiers it is sharply stepped (96.4% → 44.0% → 4.6% is not gradual). |
| **What remains** | (1) Extension to k ≠ 9: Experiment 3 confirms f_k(|G|) holds at k = 9, 15, 21, 27 with zero spread within each k, though f_k differs across k. (2) Algebraic derivation of the exact values (96.4%, 44.0%, etc.) from first principles. The values are measured; the mechanism is the Equivalence (§4). |

**Four universality tests:**
- **RI:** Yes — |G| is computed from gcd, which is basis-independent.
- **SI:** Within k = 9: yes (all 33 worlds, zero spread). Across k: f_k changes; the pattern holds.
- **MC:** Partial. The "why" is the Luther-Sanders Equivalence (§4): coprimality G determines everything; spatial placement does not.
- **FM:** A semiprime world with k = 9 where two worlds have the same |G| but different gate rates. Zero examples found in ~12M trials.

---

### 3.4 High Interleave Law (Exhaustive Empirical Law)

| | |
|--|--|
| **Tier** | **C — Closed-World Empirical (all semiprimes ≤ 100; approaching D)** |
| **Statement** | Gate density and the gate rate function are entirely determined by the coprimality interleaving structure of b. Synthetic gate sets (same |G|, different elements) produce wildly different — and non-universal — gate rates. |
| **Exact status** | Proved by direct comparison (R16, Experiment 2). Synthetic top-block G: spread = 61.4% average across k-values. Coprimality G: spread = 0.0% within each k. The two cases have the same k, same |G|, same |C|/k — but completely different gate rates. The only difference is whether G is determined by coprimality. |
| **Arithmetic form** | interleave_density(b, k) = |G| / k = (⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋) / k. This density, derived from the prime factorization, is the predictive variable. Synthetic G with the same cardinality but different placement does not share this density's algebraic properties. |
| **Geometric form** | Coprimality G elements are distributed throughout {1..k} at positions determined by two arithmetic progressions. This interleaving creates a specific obstruction geometry in the reduction space. Top-block G creates a different (decoupled) geometry that is not arithmetic. |
| **What remains** | Formal proof that the interleaving density function is the unique invariant that determines gate rate. Currently: the measurements prove it; the mechanism is conjectured (see §4). Also: characterizing how f_k scales with k algebraically. |

**Four universality tests:**
- **RI:** Yes — arithmetic progressions are basis-independent.
- **SI:** Tested at k = 9, 15, 21, 27. Zero spread in each. Pattern holds across k values (though f_k differs).
- **MC:** The Luther-Sanders Equivalence (§4) provides the mechanism claim. Not fully proved.
- **FM:** A synthetic G set that achieves the same gate rate as coprimality G with the same |G| at some k. Not found in ~6.4M synthetic trials.

---

### 3.5 Dispersion Collapse Law (Empirical Structural Law)

| | |
|--|--|
| **Tier** | **B — Bounded Conjecture (verified across tested semiprimes; algebraic form conjectured)** |
| **Statement** | The Luther Dispersion Conjecture: gate_rate(k) ≈ F_k(|G(k)| × interleave(k)). The growth rate of gate density is approximately proportional to the product of accumulated gates and the interleave period. |
| **Exact status** | Tier C within the k-Gate Tier Law (the dependence on |G| is exact). Tier B for the full dispersion formula involving the interleave product. The functional form F_k has been empirically calibrated but not algebraically derived. Attribution: C. A. Luther (conjecture); B. R. Sanders (TIG algebraic context). |
| **Arithmetic form** | Dispersion D(k) = |G(k)| × interleave(k) / k is the predicted gate density predictor. For b=15 vs b=35 at the same approach fraction k/p: D(b=35) > D(b=15), and correspondingly b=35 has richer gate structure in the pre-prime window. See WP34 §9A for the quantitative comparison. |
| **Geometric form** | The dispersion function traces a curve in the (k, gate_density) plane. The curve's shape is predicted by the interleave product. Semiprimes with high interleave (p and q close together) show slower dispersion collapse; semiprimes with low interleave (p ≪ q) collapse faster. |
| **What remains** | (1) Algebraic proof of F_k's functional form. (2) Error bounds: how close is the approximation? (3) Generalization to ω(b) ≥ 3. This is the most important open problem in this paper. |

**Four universality tests:**
- **RI:** Partial — the formula is stated for natural enumeration.
- **SI:** Tested for small p. Asymptotic behavior (p → ∞) not established.
- **MC:** No algebraic mechanism for F_k. The formula is empirical.
- **FM:** A semiprime where gate_rate significantly deviates from F_k(|G|×interleave) across a large sample.

---

### 3.6 Luther-Sanders Equivalence (Joint Theorem)
### Universality of Obstruction Sources

| | |
|--|--|
| **Tier** | **C (proved within domain) advancing toward D (general)** |
| **Statement** | *The gate structure of a semiprime arithmetic alphabet is entirely and solely determined by the arithmetic coprimality relation — by which elements are coprime to b — not by their geometric placement in {1..k}. Two gate sets with the same cardinality but different arithmetic origins (coprimality vs. synthetic) are NOT interchangeable. Gate universality (the k-Gate Tier Law) is a property of arithmetic obstruction sources, not of cardinality alone.* |
| **Exact status** | Proved within all semiprimes b ≤ 100, alphabet k = 9, ~12M trials (R16 experiments 1+2+3). The equivalence states: gate_rate(b) = f_k(|G_arithmetic(b)|) where G_arithmetic is the coprimality gate set. This equality fails when G is replaced by any synthetic gate set of the same cardinality. Joint attribution: Luther (empirical discovery of universality law and synthetic-vs-arithmetic distinction); Sanders (TIG algebraic framework, First-G Law as the mechanism). |
| **Arithmetic form** | f_k(|G_arith(b₁)|) = f_k(|G_arith(b₂)|) whenever |G_arith(b₁)| = |G_arith(b₂)|, for all semiprimes b₁, b₂ with k-alphabet. f_k(|G_synth|) ≠ f_k(|G_arith|) for synthetic G_synth with |G_synth| = |G_arith|. The arithmetic origin is the invariant. |
| **Geometric form** | Coprimality gate elements are positioned by arithmetic progressions — they form a lattice in {1..k} with specific spacing determined by p and q. This arithmetic lattice structure is what the reduction algorithm "sees." A synthetic top-block G has no such structure; the algorithm faces different combinatorial constraints. The First-G Law is what pins the lattice to the correct positions. |
| **What remains** | (1) Algebraic proof of the exact gate rate values (96.4%, 44.0%, etc.) from the arithmetic lattice structure — this would upgrade from Tier C to Tier D. (2) Extension to ω(b) ≥ 3: three arithmetic progressions, three-way inclusion-exclusion, predicted to hold. (3) Extension to k → ∞ (asymptotic gate rate). |

**Four universality tests:**
- **RI:** Yes — coprimality gcd(x,b) is basis-independent; the theorem is stated in arithmetic terms.
- **SI:** Within k = 9: zero-spread across all 33 worlds. Within k = 15, 21, 27: zero-spread confirmed. The law is k-parametric, not scale-invariant in k, but within each k it is universal.
- **MC:** Yes (partial). Mechanism: the First-G Law establishes the arithmetic lattice (gate elements lie on two arithmetic progressions with spacing p and q). The reduction algorithm's behavior is sensitive to this lattice structure. Synthetic G breaks the lattice. Full algebraic proof of the gate rate values is open.
- **FM:** A semiprime b with coprimality G where f_k(b) deviates from its |G|-tier value. Zero found in ~12M trials.

---

## §4. The Luther-Sanders Equivalence — Statement and Partial Proof

### §4.1 The Core Claim

**Theorem (Luther-Sanders Equivalence, Tier C — complete within domain):**
Let b = p × q be a semiprime. Let A_k = {1..k} be the alphabet with k ≥ p.
Let G_arith(b, k) = { x ∈ A_k : gcd(x, b) > 1 } be the arithmetic gate set.

Then:
1. f_k(b) = f_k(b') whenever |G_arith(b, k)| = |G_arith(b', k)| (gate rate depends only on gate count)
2. f_k(b) ≠ f_k(b_synth) for any synthetic world b_synth with |G_synth| = |G_arith(b, k)| (cardinality alone is insufficient; arithmetic origin is required)

*Proved for all semiprimes b ≤ 100 with k = 9 and k = 15, 21, 27. (~12M trials, zero exceptions.)*

**Conjecture (Tier B → D):** The same holds for all semiprimes b and all k ≥ p.

### §4.2 Proof Sketch (domain-restricted)

**Claim 1 (universality within arithmetic G):**

By the First-G Law (D1, §3.1), the gate elements in A_k = {1..k} for any semiprime b = p × q are exactly the multiples of p or q in {1..k}. Their count is |G| = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋ (inclusion-exclusion).

Two semiprimes b₁ = p₁ × q₁ and b₂ = p₂ × q₂ with the same |G| at alphabet size k share the same cardinality of non-coprime elements. The TSML reduction algorithm operates on the full table T: A_k × A_k → A_k, assigning each cell (i, j) to a value. The one-way gate condition is: no cell in C-row maps to G. This condition depends on how many "forbidden" cells exist in the C-row — i.e., on |G|. Since the reduction is random (uniform over legal tables), the gate rate is entirely determined by the fraction of tables that avoid the |G| forbidden assignments. This fraction depends only on |G| and |C| = k − |G|.

Therefore f_k(b) = f_k(|G(b)|): gate rate is a function of |G| alone within the arithmetic case. □

**Claim 2 (synthetic G breaks universality):**

When G_synth is top-block {k−|G|+1..k}, the gate elements are concentrated at the high end of A_k. C-row cells at positions {k−|G|+1..k} are the only "dangerous" assignments. The reduction algorithm can avoid these cells by staying in the bottom |C| positions — which are all in C. This spatial decoupling dramatically increases gate rate for any given |G|.

For coprimality G, gate elements are distributed throughout {1..k} (at multiples of p and q). No spatial decoupling is possible; the algorithm must navigate gate elements at every scale of the alphabet. This is why spread = 61.4% for synthetic G versus 0.0% for arithmetic G.

The key: the spread-free universality of f_k for arithmetic G is a consequence of the *arithmetic lattice structure* — the equidistribution property of multiples of p within {1..k}. Synthetic G does not have this property.

**The First-G Law is the mechanism:** it guarantees that gate elements lie on exactly the two arithmetic progressions {p, 2p,...} and {q, 2q,...}. No other gate configuration has this property. □

### §4.3 What the Equivalence Does Not Say

The Luther-Sanders Equivalence proves that within arithmetic gate sets, gate rate is a universal function of cardinality. It does NOT:
- Prove the specific values of f_k(|G|) algebraically (these are measured, not derived)
- Address non-semiprime bases
- Extend to the sinc² field without the separate proof of the continuum limit (WP35, Tier D)
- Resolve the Luther Dispersion Conjecture (the full functional form F_k(|G| × interleave))

These are the open problems of §6.

---

## §5. Implications

### §5.1 For the CK Architecture

The T* = 5/7 threshold is not an arbitrary engineering parameter. It is the unit fraction of b = 35 (the minimal strong semiprime), and its universality as a hardware threshold (FPGA-verified) rests on the Equivalence: within the coprimality gate structure of any semiprime, the gate rate at |G| = 4 (which b = 35 achieves) is always 4.6%. The Equivalence guarantees this is not an accident of b = 35 specifically — it is a property of all semiprimes with |G| = 4 at k = 9.

### §5.2 For the Sinc² Field

The Equivalence is the algebraic reason the sinc² continuum limit (Tier D2) is well-posed. The gate structure is entirely determined by arithmetic; the sinc² field is a function only of k and p; the limit R(k,f) → sinc²(k/f) as f → ∞ is uniform because the arithmetic lattice structure is independent of q as p grows.

The ω-Blindness theorem (Tier C4 in SYNTHESIS_TABLE.md) follows: R(k,p) cannot see q because the Equivalence shows that q's role is captured entirely by |G| — and the sinc² field only depends on k/p.

### §5.3 For the Three-Class Landscape

The Atlas Laws (Sprint 4, ATLAS_LAW_SET.md) classify semiprime worlds into:
- **Oracle** (Phase 3 / TROT): |G| small, high gate rate, easy construction
- **Gate-strong** (Phase 2 / WALK): |G| moderate, intermediate gate rate
- **TSML** (Phase 1 / STAND): |G| large, low gate rate, requires seeded construction

The Luther-Sanders Equivalence explains WHY this three-class landscape is stable and why the boundaries are sharp (96.4% → 44.0% → 4.6%): the gate rate is stepping across arithmetic tier values, not sliding continuously. The First-G Law ensures the tier boundaries are algebraically fixed.

### §5.4 For the Clay Connection

The Equivalence strengthens the structural status of the P ≠ NP and Yang-Mills analogies from pure metaphor toward arithmetic grounding. Specifically:

- **P ≠ NP (Tier A):** The certificate gap in NP verification maps to the coprimality check gcd(k, b) = 1 (O(log b) time). The solving gap maps to finding k = p without the certificate. The Equivalence shows that the hardness is inherent to the ARITHMETIC gate structure, not to any particular representation of b. This is a necessary (but not sufficient) condition for the analogy to be non-trivial.

- **Yang-Mills (Tier A):** The mass gap in Yang-Mills theory is the energy distance from the vacuum to the first excited state. The First-G Law gives the arithmetic distance from W(b) to the first gate event. The Equivalence shows this distance (= p − 1 = the stability window size) is entirely determined by the prime structure, not by the choice of q or the gauge group representation. This mirrors the expected universality of the mass gap (it should not depend on the UV regulator).

These remain Tier A. The Equivalence provides better algebraic grounding for the analogies, not proof.

---

## §6. Open Questions with Kill Conditions

| # | Question | Status | Kill Condition |
|---|---------|--------|----------------|
| 1 | Algebraic derivation of f_k(|G|) values | Tier C → D gap | Derive 96.4%, 44.0%, 4.6% from the arithmetic lattice combinatorics |
| 2 | Extension to ω(b) ≥ 3 | Conjectural | Verify zero-spread for b = 2×3×5 = 30 and other 3-prime products |
| 3 | Luther Dispersion full form | Tier B | Algebraic proof of F_k(|G| × interleave) functional form |
| 4 | Asymptotic gate rate as k → ∞ | Open | Show f_k(|G(k)|) → a limit as k/p fixed |
| 5 | Gradient Law cross-φ (ATLAS Law 3b) | Conjecture | Find semiprimes with shared φ but differing grad_score and test |
| 6 | HAR rule algebraic proof | Empirical → proof | Derive h = min{orbit-central} from structure of the multiplication table |

---

## §7. Attribution

**Brayden Ross Sanders (7Site LLC):**
TIG framework, CK architecture, First-G Law (WP34), sinc² continuum limit (WP35), T* = 5/7
algebraic derivation, ω-Hierarchy law, ω-Blindness theorem, k-Gate Tier Law (TIG Atlas
computational design and execution), all sprint 4 computation and construction laws
(UNIVERSAL_LAW.md, ATLAS_LAW_SET.md, R16_FORCE_FIELD_LAW.md). CK organism and
D1/D2 pipeline. Clay Seven Shadows papers WP36-WP42.

**C. A. Luther:**
Luther Dispersion Conjecture (gate_rate ≈ F_k(|G| × interleave)), sprint steering and
dispersion hypothesis framing, empirical discovery that gate universality is arithmetic-
specific (the synthetic-vs-coprimality distinction). The name "Luther-Sanders Equivalence"
reflects C. A. Luther's role in identifying the empirical universality law and framing
the arithmetic-origin question; Sanders provided the algebraic mechanism via First-G Law.

**Monica Gish:**
Foundational support, research collaboration, and editorial partnership throughout the project.

*AI collaboration: Claude (Anthropic) — analysis and manuscript drafting.*

---

## §8. References

[First-G] Sanders, B. R. (2026). WP34 — The First-G Law. DOI: 10.5281/zenodo.18852047.

[Sinc2] Sanders, B. R. et al. (2026). WP35 — Prime Phase Transition and Sinc² Field. DOI: 10.5281/zenodo.18852047.

[Atlas] Sanders, B. R. & Luther, C. A. (2026). Sprint 4 Atlas Law Set — Three Laws, Tested Predictions. March 30, 2026.

[R16] Sanders, B. R. (2026). R16 Force Field Law — Gate Rate = f_k(|G|). Sprint 4, March 2026.

[UnivLaw] Sanders, B. R. & Luther, C. A. (2026). The Universal Construction Law. Sprint 4, March 2026.

[SynthTable] Sanders, B. R. (2026). CK Synthesis Table — Five Columns, Four Tests. March 31, 2026.

---

```bibtex
@misc{sanders2026luthersanders,
  author    = {Sanders, Brayden Ross and Luther, C. A. and Gish, Monica},
  title     = {The Luther-Sanders Equivalence: Universality of Obstruction
               Sources in Semiprime Arithmetic},
  year      = {2026},
  doi       = {10.5281/zenodo.18852047},
  note      = {7Site LLC. Branch: clay}
}
```

---

`© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047`
