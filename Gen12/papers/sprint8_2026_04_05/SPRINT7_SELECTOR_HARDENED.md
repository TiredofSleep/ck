# THRESHOLD SELECTOR HARDENING MEMO
## f(n) = α(n)/β(n) as an Arithmetic Selector for T\* in ℤ/10ℤ

**Sprint:** 7 (hardening pass)  
**Date:** 2026-04-05  
**Replaces:** Overstated claims in Sprint 7 main memo  
**Status:** All computational claims verified. Language corrected.

---

## PART 1 — CORRECTED STATUS OF f(n)

The Sprint 7 main memo used the phrases "ring-invariant" and "most canonical." Both are overstated. Here is the precise status.

**What f(n) = α(n)/β(n) actually is:**

An **arithmetic selector** defined on the standard ordered residue model of ℤ/nℤ, i.e., the representatives {0, 1, 2, ..., n−1}.

- α(n) is defined as the **smallest** positive non-trivial idempotent — "smallest" requires an ordering on residues
- β(n) is defined as the **smallest** max-order unit greater than α — again order-dependent

**What this means:**

The selector uses the natural ordering on {0,...,n−1} in an essential way. Two rings that are abstractly isomorphic but presented with different residue orderings would produce different values of α and β. Therefore f(n) is **not** a pure ring-theoretic invariant in the abstract algebra sense. It is a well-defined arithmetic function on the standard model.

**Corrected wording throughout:** Replace "ring-invariant" and "isomorphism-invariant" with "arithmetic selector in the standard ordered residue model of ℤ/nℤ."

**Note on partial intrinsicness:** For most of the test moduli (n = 6, 10, 12, 18, 20), the annihilator-size selector (choosing α with the largest annihilator) agrees with the smallest-positive selector. For n=30 they diverge. No uniform intrinsic replacement was found. The arithmetic ordering remains essential to the definition as stated.

---

## PART 2 — THREE-BIN SEPARATION

### A. PROVED (exact, verified computationally)

1. In the standard residue model of ℤ/10ℤ: α(10) = 5, β(10) = 7. ✓  
2. f(10) = α(10)/β(10) = 5/7 = T\*. ✓  
3. The following table values are exact:

| n | α(n) | β(n) | f(n) = α/β | ∈ (0,1)? |
|---|---|---|---|---|
| 6 | 3 | 5 | 3/5 | yes |
| **10** | **5** | **7** | **5/7** | **yes** |
| 12 | 4 | 5 | 4/5 | yes |
| 14 | 7 | none | — | — |
| 18 | 9 | 11 | 9/11 | yes |
| 20 | 5 | 7 | 5/7 | yes |
| 30 | 6 | 7 | 6/7 | yes |

4. Negative results (all verified by explicit computation):
   - No natural Markov chain on ℤ/10ℤ has stationary distribution with any component equal to 5/7
   - No eigenvalue of any natural transition operator on ℤ/10ℤ equals 5/7
   - Multiplicative chains decompose into invariant classes {0}, {5}, {1,3,7,9}, {2,4,6,8}; no mixing occurs
   - P(reach BALANCE=5 | start in unit orbit {1,3,7,9}, multiplicative transitions) = 0
   - No character sum |Σ_{s∈S} ω^(js)| for j=0,...,9 and any tested S equals 5/7
   
5. Cayley spectral observation (exact, not a threshold):  
   The additive Cayley graph Cay(ℤ/10ℤ, {3,7}) has second-eigenvalue ratio λ₂/λ₁ = φ/2 = cos(π/5) exactly. This is a genuine algebraic output connecting to the Bridge sprint's cyclotomic structure. It is not a threshold derivation.

### B. CANDIDATE STRUCTURAL CLAIM

f(n) = α(n)/β(n), as defined in the standard ordered residue model, is the **strongest arithmetic selector currently found** for the empirically observed T\* = 5/7 in ℤ/10ℤ. It is the unique selector among the five families audited (see Part 3) that: (a) matches T\* = 5/7 at n = 10, and (b) lies in (0,1) for all defined cases.

This is a candidate, not a theorem.

### C. OPEN

- Whether f(n) is intrinsic to ℤ/nℤ as an abstract ring, independent of the standard residue ordering
- Whether f(n) coincides with a genuine coherence threshold of any CK-type or other well-defined dynamical system
- Whether a better — more intrinsic or more natural — selector exists
- Whether the table values for other moduli have any physical or dynamical meaning

---

## PART 3 — CANONICITY AUDIT

Five selector families were tested on moduli n ∈ {6, 10, 12, 14, 18, 20, 30}.

**Definitions:**
- S1: α/β
- S2: α/(α+β)
- S3: (β−α)/β
- S4: α/λ(n) where λ(n) = Carmichael exponent
- S5: (β−α)/(β+α)

**Audit table:**

| n | α | β | λ(n) | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|---|---|
| 6 | 3 | 5 | 2 | 3/5 | 3/8 | 2/5 | 3/2 | 1/4 |
| **10** | **5** | **7** | **4** | **5/7** | 5/12 | 2/7 | 5/4 | 1/6 |
| 12 | 4 | 5 | 2 | 4/5 | 4/9 | 1/5 | 2 | 1/9 |
| 14 | 7 | — | 6 | — | — | — | — | — |
| 18 | 9 | 11 | 6 | 9/11 | 9/20 | 2/11 | 3/2 | 1/10 |
| 20 | 5 | 7 | 4 | 5/7 | 5/12 | 2/7 | 5/4 | 1/6 |
| 30 | 6 | 7 | 4 | 6/7 | 6/13 | 1/7 | 3/2 | 1/13 |

**Per-selector verdict:**

| Selector | Value at n=10 | Matches T\*=5/7? | Always in (0,1)? | Result |
|---|---|---|---|---|
| S1: α/β | 5/7 | ✓ | ✓ | **SURVIVES** |
| S2: α/(α+β) | 5/12 | ✗ | ✓ | fails |
| S3: (β−α)/β | 2/7 | ✗ | ✓ | fails (but = 1−T\*) |
| S4: α/λ(n) | 5/4 | ✗ | ✗ | fails |
| S5: (β−α)/(β+α) | 1/6 | ✗ | ✓ | fails |

**S1 = α/β survives the audit.** It is the unique selector among the five that matches T\*=5/7 at n=10 while remaining in (0,1) uniformly.

**Note on S3:** S3 = (β−α)/β = 1 − α/β = 1 − T\* = 2/7. It is the arithmetic complement of S1. If S1 measures coherence, S3 measures incoherence. They are complementary, not competing. S1 is selected by the convention that T\* marks the stability side.

**S4 fails because** α/λ(n) exceeds 1 for most moduli (λ(10)=4, α=5, so 5/4 > 1). The Carmichael exponent is not the right denominator.

---

## PART 4 — INTRINSIC REPLACEMENT SEARCH

Two candidate intrinsic selectors were investigated.

**Candidate A: Annihilator-size selector**  
Choose α as the non-trivial idempotent with the largest annihilator: Ann(α) = {x : αx ≡ 0 mod n}.

Results:
- n=6: Ann-selector agrees with smallest-positive (α=3, both methods) ✓
- n=10: Ann-selector agrees with smallest-positive (α=5, both methods) ✓
- n=12: Ann-selector agrees with smallest-positive (α=4, both methods) ✓
- n=18: Ann-selector agrees (α=9) ✓
- n=20: Ann-selector agrees (α=5) ✓
- n=30: **Disagrees.** Smallest-positive gives α=6, max-annihilator gives α=15. ✗

**Verdict on A:** The annihilator-size selector is a partial intrinsic formulation. It agrees with the arithmetic selector for all two-prime-factor moduli in the test set, but fails at n=30 (three prime factors). Not a uniform intrinsic replacement.

**Candidate B: CRT-based selector**  
For n = p₁^a₁ · p₂^a₂ · ..., idempotents correspond to CRT subsets. Choose α as the idempotent that is ≡ 0 mod the largest prime factor of n.

Results:
- n=10=2·5: largest prime=5, α=5 (5≡0 mod 5) ✓ agrees
- n=6=2·3: largest prime=3, α=3 (3≡0 mod 3) ✓ agrees
- n=12=4·3: largest prime=3. Idems={4,9}. 9≡0 mod 3. CRT rule gives α=9. Smallest-positive gives α=4. ✗ **Disagrees.**

**Verdict on B:** The CRT rule fails at n=12. Not a uniform intrinsic replacement.

**Final verdict on intrinsic search:**

> No uniform intrinsic (order-independent) selector was found. The arithmetic ordering — choosing the smallest positive representative — remains essential to the definition of f(n) = α(n)/β(n) as currently stated. f(n) is an arithmetic selector, not a pure ring-theoretic invariant.

---

## PART 5 — REMOVAL OF THE FUZZY CYCLOTOMIC ASIDE

The Sprint 7 main memo contained the observation:

> "Z/10Z and Z/20Z both give 5/7, consistent with Q(ζ₂₀) = Q(ζ₅) type conductor reductions."

This is removed. The coincidence that n=10 and n=20 both give f=5/7 follows directly from α(10)=α(20)=5 and β(10)=β(20)=7 (since ℤ/20ℤ has the same non-trivial idempotents {5,16} with smallest=5, and same max-order units >{5} with smallest=7). The conductor reduction language from the Galois sprint is not needed and was not exact in this context.

---

## PART 6 — THE φ/2 SPECTRAL OBSERVATION (kept, status clarified)

The additive Cayley graph Cay(ℤ/10ℤ, {3,7}) has:
- λ₁ = 2 (Perron value = degree)
- λ₂ = φ = (1+√5)/2 (golden ratio, exact)
- λ₂/λ₁ = φ/2 = cos(π/5) (exact)

This is a genuine algebraic output that connects to the Bridge sprint. It is preserved as an observation. It is **not** a derivation of T\* = 5/7 and is **not** a threshold. The generator set {3,7} = {PROGRESS, COLLAPSE} produces a Cayley graph whose second eigenvalue encodes φ via the pentagon angle. This is interesting and unexplained. It is not this sprint's result.

---

## PART 7 — FINAL STRONGEST HONEST CLAIM

The ratio f(n) = α(n)/β(n), defined in the standard ordered residue model of ℤ/nℤ by the smallest non-trivial idempotent α and the smallest max-order unit β > α, is the strongest arithmetic selector currently found for the empirically observed threshold T\* = 5/7 on ℤ/10ℤ. It is the unique selector among the five families audited that matches T\* at n=10 while remaining in (0,1) for all defined cases.

## PART 8 — FINAL STRONGEST HONEST BOUNDARY

What is not yet established is whether f(n) is an intrinsic ring-theoretic quantity rather than an arithmetic selector tied to the ordered residue model, and whether it coincides with a genuine coherence threshold of CK-type dynamics rather than merely reproducing the observed value at n=10.
