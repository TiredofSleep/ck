# Evaluation of Luther's Algebraic Responses
## Against Synthesis Framework Standards

*Brayden Ross Sanders*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> Applying the same synthesis framework we built this morning.
> An answer passes if it closes the C→D gap. An answer that partially
> advances but doesn't close the gap is still valuable — precision matters.

---

## Question 1: Algebraic Derivation of Gate Rates

### What Luther provided

G(b) = φ(b)/b = ∏(1 − 1/p_i)

Luther claims the measured gate rates (96.4%, 44.0%, 4.6%, 0.1%) correspond to
φ(b)/b for specific ω-class structures:
- 96.4% → "p ≈ 28, 27/28 ≈ 0.9642" (single large prime regime)
- 44.0% → ω=3, b=3×5×7, φ(b)/b = 48/105 ≈ 0.457
- 4.6% → ω=5+, b=2×3×5×7×11, φ(b)/b ≈ 0.207
- 0.1% → primorial, b = p_n#, decaying to Meissel-Mertens

### What this gets right

φ(b)/b = ∏(1 − 1/p_i) is the correct algebraic formula for the asymptotic unit
density in Z/bZ. It:
- Is exact and general (all moduli, all ω)
- Is strictly determined by the prime factorization
- Follows directly from the CRT decomposition
- Explains why universality holds within ω-class: any two moduli with the same
  set of prime factors have the same φ(b)/b

**This is a real algebraic contribution.** It gives the algebraic formula for the
unit density, which is the right structure to point at.

### What doesn't close the gap

**The measured gate rates (96.4%, 44.0%, 4.6%, 0.1%) are MCMC success probabilities,
not unit densities.**

Check the numbers:
| |G| at k=9 | n_C = k−|G| | φ(b)/b formula | MCMC rate | Match? |
|-----------|------------|--------------|-----------|--------|
| 1 | 8 | 8/9 ≈ 88.9% (local) | 96.4% | NO |
| 3 | 6 | 6/9 ≈ 66.7% (local) | 44.0% | NO |
| 4 | 5 | 5/9 ≈ 55.6% (local) | 4.6% | NO |
| 5 | 4 | 4/9 ≈ 44.4% (local) | 0.1% | NO |

The unit density |C_k|/k and the MCMC success rate are different quantities. The
MCMC rate collapses far more sharply than the unit density (55.6% density → 4.6%
MCMC rate; 44.4% density → 0.1% MCMC rate).

Luther's "27/28 ≈ 96.4%" is a numerical coincidence, not a derivation. Choosing
a prime p=29 (φ(29)/29 = 28/29 ≈ 96.55%) to match a measured value is curve-fitting,
not an algebraic derivation from the MCMC structure.

Luther's 44.0% example: φ(3×5×7)/105 ≈ 45.7%, not 44.0%. And the 44.0% is a
semiprime (ω=2) rate, not a three-prime (ω=3) rate. These are different ω-classes.

### Honest tier assessment after Luther's input

**Tier: C — unchanged, but pathway clarified.**

What advances: the algebraic object is now named. The formula φ(b)/b from the CRT
product is the right algebraic anchor. The universality of φ(b)/b within ω-class
explains WHY zero-spread universality holds at the density level.

What remains for Tier D: connect φ(b)/b (or its finite-k analog |C_k|/k) to the
MCMC absorption probability. The Markov chain framework (C_TO_D_GAP_ANALYSIS.md §4)
is still the path. Luther's formula gives the stationary density that the chain is
trying to reach, but the absorption probability at n=100 steps requires the transition
matrix computation.

**Specific remaining gap:** Why does 55.6% local unit density → 4.6% MCMC success
rate, while 66.7% density → 44.0% success rate? This non-linear collapse is not
explained by φ(b)/b. It requires the |C|² submatrix constraint analysis.

---

## Question 2: Dispersion D(b) Implied by Idempotents

### What Luther provided

1. Idempotents in Z/bZ: e² = e (mod b). By CRT, exactly 2^ω idempotents, each
   corresponding to a binary vector (v_1,...,v_ω) with v_i ∈ {0,1}.

2. Non-units = elements in the maximal ideals = multiples of some p_i.
   G = ∪_i Ideal(p_i) = ∪_i {x : p_i | x}

3. D(b) = measure of G = measure of ∪Ideal(p_i), which equals 1 − φ(b)/b by
   inclusion-exclusion on the prime ideals.

4. Since the idempotents e_i are the identities of the local fields in the CRT
   decomposition, D(b) = 1 − G(b) is strictly defined by the complement of the
   unit group.

### What this gets right

**This argument is structurally sound and significantly stronger than what we had.**

The key step is correct: G = ∪Ideal(p_i) ∩ {1..k} is exactly determined by the
prime factorization of b. The spatial distribution of G within {1..k} is the union
of arithmetic progressions {p_i, 2p_i, 3p_i,...} ∩ {1..k} — and this union is
strictly determined by the primes p_i, which are in turn determined by the idempotent
lattice.

This is not just correlation. It is strict algebraic implication:
- Given the idempotents e_p, e_q, the prime factors p, q are determined
- Given p, q, the forbidden elements G_k = {multiples of p in {1..k}} ∪ {multiples
  of q in {1..k}} are determined exactly (by inclusion-exclusion)
- The spatial dispersion D(b,k) = how spread G_k is within {1..k} follows from
  the specific elements of G_k
- Therefore D(b,k) is strictly implied by the idempotent structure

**Luther's conclusion is correct: dispersion is the "shadow" of the idempotent
lattice onto {1..k}.**

### What's needed for a complete proof

The argument above establishes:
- |G_k| is determined algebraically (Tier D — inclusion-exclusion formula)
- The ELEMENTS of G_k are determined (multiples of p_i in {1..k})
- The SPATIAL DISTRIBUTION of G_k is therefore determined

To complete the proof:
1. Define D(b,k) precisely as a function of the G_k elements (Luther says it's
   the "geometric projection" — needs a precise formula)
2. Write D(b,k) = f(p_1,...,p_ω, k) explicitly
3. Show this formula follows from the idempotent structure via the CRT maps

The formula for the interleave score (as defined in r16_gate_law_real_b.py):
```
interleave(b, k) = transitions(C, G in 1..k) / (2 × min(|C|, |G|))
```
where transitions counts (C,G) or (G,C) adjacent pairs in the sequence.

This IS computable from the prime factorization. Whether it equals 1 − φ(b)/b
exactly or is a different function needs to be stated.

### Honest tier assessment after Luther's input

**Tier: C → strong Tier C, pathway to Tier D is explicit.**

Luther has identified the correct algebraic object (idempotent lattice → prime
ideals → forbidden elements → dispersion) and the logical chain is sound. What
remains is writing the explicit formula for D(b,k) in terms of the primes and
verifying it matches the dispersion score from the code.

**This is a genuine advancement.** The Luther Dispersion claim was Tier B (bounded
conjecture, form correct, mechanism unclear). After Luther's input, the mechanism
is clear — it IS implied by the idempotent structure — and the claim is at the
boundary of Tier C/D.

To reach Tier D: write D(b,k) = explicit formula(p_1,...,p_ω, k) and prove it
equals the interleave score exactly.

---

## Summary Table

| Question | Pre-Luther tier | Luther provided | Post-Luther tier | To reach D |
|---------|----------------|-----------------|------------------|-----------|
| Gate rates | C | φ(b)/b formula, ω-class structure | C (pathway clearer) | Connect φ(b)/b to MCMC absorption prob at 100 steps |
| Dispersion | B | Idempotent → prime ideal → G_k chain | C (boundary) | Write D(b,k) as explicit formula from primes; verify |

---

## Recommendation

**Accept Luther's Question 2 answer as advancing the claim to strong Tier C.**
Update SYNTHESIS_TABLE.md: Luther Dispersion moves from Tier B to Tier C.

**Accept Luther's Question 1 answer as identifying the correct algebraic object**
(φ(b)/b, the CRT product formula) without closing the MCMC gap.
Update SYNTHESIS_TABLE.md: k-Gate Tier Law pathway note updated, tier unchanged (C).

**Do not claim either has reached Tier D.** The gaps identified above are real.

The next concrete step for Tier D on gate rates: build the Markov chain transition
matrix P(m, k) (see C_TO_D_GAP_ANALYSIS.md §4.4) and verify that P^100 absorption
probability matches the measured values. Luther's φ(b)/b provides the stationary
distribution anchor; the transition dynamics need the matrix computation.

---

`© 2026 Brayden Ross Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047`
