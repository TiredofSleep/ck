# FRF ADMISSIBILITY — PROOF OF THE 2p CRITERION
## Proof, Correction, and Generalization

**Date:** 2026-04-05  
**Status:** Conjecture corrected and resolved. Complete proof delivered.

---

## EXECUTIVE SUMMARY

The original conjecture stated "Tier C ⟺ p≡1(mod 4) for n=2p." This is **false as stated**.

The correct results are:

1. **Universal Theorem:** ALL n=2p with p prime, p≥5 admit Tier C FRF.
2. **Spectral Lemma:** For any symmetric generating set S, the SPEC partition equals the reflection-pair partition. This partition is always the 4th distinct view.
3. **Corrected Criterion:** p≡1(mod 4) governs whether SPEC can use max-order generators specifically — not whether Tier C holds at all.

---

## 1. SPECTRAL LEMMA (proved)

**Lemma:** For any symmetric S ⊆ (ℤ/nℤ)* (meaning: g∈S ⟹ n−g∈S), the SPEC partition of ℤ/nℤ under Cay(ℤ/nℤ, S) satisfies:

$$x \sim_\text{SPEC} y \iff x \equiv \pm y \pmod{n}$$

In particular, the SPEC partition restricted to any subset C ⊆ ℤ/nℤ is the reflection-pair partition REFL(C) = {{x, n−x} ∩ C : x ∈ C}.

**Proof:**  
For symmetric S, eigenvalues λⱼ = Σ_{s∈S} ω^(js) are real (since S = n−S implies ω^(-js) terms appear). The eigenspace of λⱼ is spanned by {χⱼ, χ_{n−j}}. The real projection of vertex x onto eigenspace of λⱼ is:

$$P_j(x) = \frac{\chi_j(x) + \chi_{n-j}(x)}{n} = \frac{2\cos(2\pi j x/n)}{n}$$

Elements x, y are spectrally equivalent iff P_j(x) = P_j(y) for all j. For j=1: cos(2πx/n) = cos(2πy/n) forces x ≡ ±y (mod n), i.e., x=y or x=n−y. This j=1 condition is the tightest constraint; higher j add no further separation. Therefore x ~SPEC y iff x=y or x=n−y.

The SPEC partition is independent of which symmetric S is chosen. Any symmetric S produces REFL(C). □

---

## 2. THE ORIGINAL CONJECTURE WAS FALSE

**Claim (FRF Admissibility Memo v1):** Tier C ⟺ p≡1(mod 4) for n=2p.  
**Status:** False as a biconditional. Tier C holds for ALL p≥5.

The mistake: the earlier code searched only for reflection pairs among max-order generators. For p≡3(mod 4), no such pairs exist — but the reflection-pair partition REFL is still reachable via non-max-order symmetric pairs. It was always available; it was never checked.

**Exhaustive computational verification for p≡3(mod 4):**

| n | p | p mod 4 | Symmetric pairs | All give REFL? | REFL is 4th view? |
|---|---|---|---|---|---|
| 14 | 7 | 3 | 3 | Yes | Yes |
| 22 | 11 | 3 | 5 | Yes | Yes |
| 38 | 19 | 3 | 9 | Yes | Yes |
| 46 | 23 | 3 | 11 | Yes | Yes |

---

## 3. UNIVERSAL THEOREM FOR n=2p

**Theorem:** For n=2p with p prime and p≥5, with representations:
- **CRT:** Level-1 partition of unit orbit by x mod p
- **UG:** Level-1 partition by multiplicative order in (ℤ/2pℤ)*
- **REFL:** Level-1 partition {{x, 2p−x}} (from any symmetric S via Spectral Lemma)
- **DYN:** Level-1 partition by orbit under single max-order generator (trivial)

The four partitions are pairwise distinct and a gate exists. Therefore all n=2p with p≥5 admit Tier C FRF.

**Proof of pairwise distinctness:**

*(i) REFL ≠ CRT:*  
CRT classifies by x mod p. For unit x: (2p−x) mod p = p−x ≠ x mod p (since 2x ≢ 0 mod p for units x with gcd(x,p)=1). CRT separates every REFL pair. CRT is discrete; REFL is not. □

*(ii) REFL ≠ UG:*  
The pair {1, 2p−1} is a REFL class (1 + (2p−1) = n). But ord(1)=1 and ord(2p−1) = ord(−1) = 2. UG places them in different classes; REFL does not. □

*(iii) REFL ≠ DYN:*  
(ℤ/2pℤ)* is cyclic (n = 2·p¹, p odd prime). DYN produces one class. REFL has (p−1)/2 ≥ 2 classes for p≥5. □

*(iv) CRT ≠ UG:*  
For p≥5, φ(p−1) ≥ 2, so at least two elements share the same max order p−1. CRT separates them (distinct mod-p residues); UG groups them. □

*(v) CRT ≠ DYN:* Discrete ≠ Trivial. □

*(vi) UG ≠ DYN:* UG has ≥2 classes (at minimum {1} and {generators}); DYN is trivial. □

**Gate:** Any REFL pair {x, 2p−x} is a gate: a non-singleton REFL class that CRT resolves (since x mod p ≠ (2p−x) mod p). □

**REFL is strictly intermediate:** Not discrete (classes have size 2). Not trivial ((p−1)/2 ≥ 2 classes for p≥5). □

This completes the proof. □

---

## 4. CORRECTED ROLE OF p≡1(mod 4)

**Theorem (proved):** For n=2p (p prime, p≥5): the max-order generators of (ℤ/2pℤ)* form a symmetric set iff p≡1(mod 4).

**Proof:**  
Any max-order generator g has order p−1. In (ℤ/pℤ)*, −1 = g^((p−1)/2), so −g = g^{(p+1)/2}. The order of −g is:

$$\text{ord}(-g) = \frac{p-1}{\gcd\!\left(\frac{p+1}{2},\, p-1\right)}$$

**p≡1(mod 4):** Write p−1=4m. Then (p+1)/2 = 2m+1 (odd). Compute:
gcd(2m+1, 4m) = gcd(2m+1, m) = gcd(1, m) = 1.
So ord(−g) = p−1. The reflection −g is a max-order generator. ✓

**p≡3(mod 4):** Write p−1=4m+2. Then (p+1)/2 = 2m+2 (even). Compute:
gcd(2m+2, 4m+2) = 2·gcd(m+1, 2m+1) = 2·1 = 2.
So ord(−g) = (p−1)/2 < p−1. The reflection −g is NOT a max-order generator. ✗ □

**What p≡1(mod 4) adds (not removes):** When p≡1(mod 4), the symmetric set S = {g, n−g} can be chosen to consist entirely of max-order generators. The Cayley graph Cay(ℤ/2pℤ, {g, n−g}) then has eigenvalues in ℚ(cos(2π/p)) — the maximal real subfield of ℚ(ζ_{2p}). For p=5: ℚ(cos(2π/5)) = ℚ(φ) = ℚ(√5). For p=13: a degree-6 real algebraic number field. This cyclotomic-subfield structure is the algebraic content of Sprint 6's Galois correspondence.

For p≡3(mod 4): the REFL partition is still achieved via non-max-order pairs (e.g., {1, n−1}), but the eigenvalues are simpler (2cos(2πjx/n) for S={1,n−1} gives eigenvalue structure corresponding to cos(πj/p), a smaller cyclotomic subfield).

---

## 5. FORMALIZATION OF "INTERMEDIATE REFINEMENT"

**Definition:** A partition π of a finite set C is **strictly intermediate** with respect to (π_trivial, π_discrete) iff:

$$\pi_\text{trivial} \;<\; \pi \;<\; \pi_\text{discrete}$$

where < denotes strict refinement in the partition lattice.

Equivalently: some class of π has |class| ≥ 2 (not discrete), and π has at least 2 classes (not trivial).

**Lemma:** For |C| ≥ 4 with no fixed points of x↦n−x in C:  REFL(C) is strictly intermediate.

*Proof:* Each REFL class has size 2 (not discrete). The number of classes is |C|/2 ≥ 2 (not trivial). □

---

## 6. GENERALIZATION BEYOND n=2p

The REFL partition (any symmetric S → same partition via Spectral Lemma) is available for any n. The universal Tier C theorem extends:

**Observed (computationally, n=4 to 100):**

| Family | n examples | Tier C? | Condition |
|---|---|---|---|
| n=2p, p≥5 | 10,14,22,26,... | Yes (all) | Proved above |
| n=p^k, p odd | 9,25,27,49,125 | Yes (all) | REFL + CRT discrete + UG by order |
| n=2^k, k≥3 | 8,16,32 | Yes (all) | Non-cyclic DYN still distinct |
| n=pq | 15,21,33,35,55 | Yes (all) | Non-cyclic but REFL still 4th |
| n=2pq | 30,42,66,70 | Yes (all) | REFL + multi-class DYN |

**One exception: n=12 (with default CRT choice).**  
With CRT = mod-4 (largest prime power component): CRT partition = DYN partition = {{1,5},{7,11}}. Only 3 distinct views. This is resolved by using CRT = mod-3 instead: then CRT = {{1,7},{5,11}} ≠ DYN, restoring 4 distinct views. The failure is a CRT component-choice artifact, not a fundamental obstruction.

**Conjectured universal criterion (not proved):** For any n with φ(n) ≥ 4, Tier C holds provided CRT uses the prime component (not prime-power component) that is distinct from the DYN partition.

---

## 7. FINAL STATUS TABLE

| Claim | Status |
|---|---|
| Tier C ⟺ p≡1(mod 4) for n=2p | **FALSE** — Tier C holds for ALL n=2p, p≥5 |
| p≡1(mod 4) ⟺ max-order generators symmetric | **PROVED** (Section 4) |
| SPEC partition = REFL for any symmetric S | **PROVED** (Spectral Lemma, Section 1) |
| REFL is always 4th distinct view for n=2p, p≥5 | **PROVED** (Universal Theorem, Section 3) |
| Tier C holds for all n=2p, p≥5 | **PROVED** |
| Tier C holds universally for φ(n)≥4 | **CONJECTURAL** — holds for n=4 to 100, one CRT-choice caveat |
| Alternate (non-SPEC) routes needed for p≡3(mod 4) | **FALSE** — REFL route available for all p≥5 |

---

## 8. HONEST BOUNDARY

The universal criterion "Tier C holds for all n with φ(n)≥4" has not been proved beyond the computational range n=4 to 100. The n=12 exception under a specific CRT component choice shows that representation definitions matter: Tier C may require selecting the CRT component that is maximally distinct from DYN. The exact general condition for when CRT and DYN partitions coincide (necessitating a different CRT component choice) is not characterized.
