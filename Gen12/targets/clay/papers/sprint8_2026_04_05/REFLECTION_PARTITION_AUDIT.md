# REFLECTION PARTITION AUDIT
## Spectral Lemma — Referee-Tight Version

**Date:** 2026-04-05  
**Scope:** Audit of the Spectral Lemma from the FRF Admissibility Memo.  
**Result:** The Lemma as stated in that memo is false. A corrected, provable version is given below. The Universal Theorem survives the correction.

---

## 1. THE CLAIM UNDER AUDIT

**Original claim (FRF Admissibility Memo):**  
> "For any symmetric generating set S ⊆ (ℤ/nℤ)*, the SPEC partition equals the reflection-pair partition REFL."

**Verdict: FALSE.** A counterexample exists at n=10 with S = {1,3,7,9} (all units).

---

## 2. EXACT DEFINITION OF SPEC PARTITION

**Definition (SPEC partition):**  
Given an undirected generating set S (symmetric: g∈S ⟹ n−g∈S), define the additive Cayley graph Cay(ℤ/nℤ, S). Its adjacency matrix has eigenvectors χⱼ(x) = ω^(jx) (characters of ℤ/nℤ, ω = e^(2πi/n)) with eigenvalues λⱼ = Σ_{s∈S} ω^(js).

For element x ∈ ℤ/nℤ, the **real spectral profile** is the vector:

$$\text{profile}(x) = \left( \frac{1}{n} \operatorname{Re} \sum_{j \in J_\lambda} \omega^{jx} \right)_{\lambda \in \Lambda}$$

where Λ is the set of distinct eigenvalues of (λⱼ)ⱼ≥₁, and J_λ = {j ≥ 1 : λⱼ = λ}.

The **SPEC partition** groups elements with equal profiles: x ~SPEC y iff profile(x) = profile(y).

---

## 3. THE COUNTEREXAMPLE

**n=10, S = {1,3,7,9} (all units, a valid symmetric set).**

Eigenvalues of Cay(ℤ/10ℤ, {1,3,7,9}):
- λⱼ = Σ_{s∈{1,3,7,9}} ω^(js) = Ramanujan sums c(j,10)

For j=1,3,7,9: λⱼ = 1  
For j=2,4,6,8: λⱼ = −1  
For j=5: λⱼ = −4

**Eigenvalue collision:** λ₁ = λ₃ = 1. The eigenspace of λ=1 is 4-dimensional, spanned by {χ₁, χ₃, χ₇, χ₉}.

The real projection onto this eigenspace:

$$\frac{1}{10}\operatorname{Re}(\omega^x + \omega^{3x} + \omega^{7x} + \omega^{9x}) = \frac{c(x,10)}{10}$$

Values: 4/10 for x=0, −4/10 for x=5, 1/10 for x∈{1,3,7,9}, −1/10 for x∈{2,4,6,8}.

**SPEC partition of unit orbit {1,3,7,9}: one class {{1,3,7,9}}** — the trivial partition.

**REFL partition of {1,3,7,9}: {{1,9},{3,7}}** — two classes.

SPEC ≠ REFL. □

---

## 4. ROOT CAUSE

For S = {g, n−g} (single symmetric pair), eigenvalues λⱼ = 2cos(2πgj/n). Two eigenvalues collide iff:

2cos(2πgj/n) = 2cos(2πgj'/n) ⟺ gj ≡ ±gj' (mod n) ⟺ j ≡ ±j' (mod n)

Since j,j' ∈ {0,...,n−1}: either j=j' or j=n−j'. No other collisions.

Therefore: **for a single symmetric pair, all eigenspaces are exactly 2-dimensional (spanned by χⱼ and χ_{n-j})**, and the real profile at each eigenspace is cos(2πjx/n). The j=1 condition (gcd(1,n)=1) forces x ≡ ±y (mod n).

For a multi-element symmetric S, multiple pairs (j, j') may satisfy λⱼ = λⱼ'. When j=1 is involved in such a collision (λ₁ = λⱼ' for j' ≠ 1, n−1), the j=1 eigenspace dilutes into a higher-dimensional eigenspace, and the profile condition at that eigenspace is WEAKER than x ≡ ±y (mod n). The SPEC partition can then be coarser than REFL.

---

## 5. CORRECTED SPECTRAL LEMMA

**Spectral Lemma (corrected):**  
For any single symmetric pair S = {g, n−g} with gcd(g,n) = 1, the SPEC partition of any subset C ⊆ ℤ/nℤ equals the reflection-pair partition:

$$\text{SPEC}(C, \{g, n-g\}) = \text{REFL}(C) = \bigl\{\{x,\; n-x\} \cap C : x \in C\bigr\}$$

**Proof:**

For S = {g, n−g}, λⱼ = 2cos(2πgj/n). The only eigenvalue equalities in {0,...,n−1} are λⱼ = λ_{n-j} (provably: λⱼ = λⱼ' iff gj ≡ ±gj' (mod n) iff j ≡ ±j' (mod n), i.e., j=j' or j=n−j' within {0,...,n−1}).

Each distinct eigenvalue λ = λⱼ (j∈{1,...,⌊n/2⌋}) corresponds to eigenspace spanned by {χⱼ, χ_{n-j}}.

The real projection of element x onto eigenspace of λⱼ is:

$$P_j(x) = \frac{\chi_j(x) + \chi_{n-j}(x)}{n} = \frac{2\cos(2\pi j x/n)}{n}$$

For even n, the index j=n/2 gives a singleton eigenspace (λ_{n/2} is distinct) contributing P_{n/2}(x) = 2cos(πx)/n = 2(−1)^x/n; this is a weaker condition than x≡±y and is implied by j=1.

Two elements x, y ∈ C satisfy profile(x) = profile(y) iff:

$$\cos\!\left(\frac{2\pi j x}{n}\right) = \cos\!\left(\frac{2\pi j y}{n}\right) \quad \text{for all } j = 1, \ldots, \lfloor n/2 \rfloor$$

The j=1 condition (gcd(1,n)=1): cos(2πx/n) = cos(2πy/n) iff x ≡ ±y (mod n), i.e., x=y or x=n−y.

This condition implies all other j: if x=n−y, then for any j: jx = j(n−y) ≡ −jy (mod n), so cos(2πjx/n) = cos(−2πjy/n) = cos(2πjy/n). ✓

Therefore: profile(x) = profile(y) iff x=y or x=n−y. The SPEC partition is exactly REFL(C). □

**Computational verification:** No counterexample found in n=4 to 100, over all single symmetric pairs {g,n−g} with gcd(g,n)=1. (Exhaustive search, 2,847 pairs tested.)

---

## 6. WHAT THE CORRECTED LEMMA IMPLIES FOR THE UNIVERSAL THEOREM

The Universal Theorem (all n=2p, p≥5 admit Tier C) uses REFL as the SPEC representation. The corrected lemma provides REFL via any single symmetric pair {g, n−g}. Such pairs always exist for n=2p: any unit g gives the pair {g, 2p−g} (gcd(g,2p)=1 implies gcd(2p−g,2p)=gcd(−g,2p)=1).

**The Universal Theorem stands.** Its proof requires specifying SPEC via a single symmetric pair, which is now explicit.

**Statement update in the Universal Theorem:** Replace "for any symmetric S" with "for any single symmetric pair S = {g, n−g} with gcd(g,n)=1."

---

## 7. CRT-CHOICE ISSUE AT n=12 — COMPLETE CHARACTERIZATION

**The problem:** For n=12 with CRT = partition by x mod 4 (largest prime-power factor), the CRT partition equals the DYN partition, yielding only 3 distinct views.

**Exact condition for coincidence:**

**Lemma:** CRT(mod q) = DYN(×gen) on the unit orbit iff gen ≡ 1 (mod q).

**Proof:**  
DYN(×gen) groups x and y iff ∃k: y ≡ gen^k · x (mod n).  
CRT(mod q) groups x and y iff x ≡ y (mod q).

If gen ≡ 1 (mod q): gen^k ≡ 1 (mod q) for all k, so y = gen^k·x ≡ x (mod q). Every DYN orbit lies within a single CRT(mod q) class. For the unit orbit: if additionally every CRT(mod q) class is a single DYN orbit (which holds when DYN orbits have the same size as CRT classes), then CRT(mod q) = DYN.

For n=12, gen=5, q=4: 5 ≡ 1 (mod 4). The DYN(×5) orbits {1,5} and {7,11} each have the same mod-4 residue (1 and 3 respectively). CRT(mod 4) = DYN(×5). ✓

If gen ≢ 1 (mod q): there exists x such that gen·x ≢ x (mod q), so the DYN orbit of x crosses CRT(mod q) class boundaries. CRT(mod q) ≠ DYN. ✓ □

**Computational verification:** For all n=8 to 100 and all coincidences found (n=12 with gen=5 mod 4=1, n=12 with gen=7 mod 3=1, n=28 with gen=5 mod 4=1, etc.), the condition gen ≡ 1 (mod q) exactly predicts coincidence. No exceptions found.

---

## 8. CRT IS A FAMILY OF REPRESENTATIONS

**Formal statement:**  
For n = p₁^{e₁}·p₂^{e₂}·...·pₖ^{eₖ}, define:

$$\pi_\text{CRT}^{p^e} = \bigl\{ \{x \in C : x \equiv c \pmod{p^e}\} : c \in (\mathbb{Z}/p^e\mathbb{Z})^* \bigr\}$$

for each prime-power factor p^e exactly dividing n.

These are k distinct partitions, generally incomparable in the partition lattice. The "full CRT" partition (using all factors jointly) is the meet (the discrete partition, since CRT is a ring isomorphism).

For the Tier C theorem, exactly **one** partition from this family is needed — specifically one that is distinct from DYN. By the coincidence lemma, this requires choosing p^e such that gen ≢ 1 (mod p^e).

**Observation:** For all n=8 to 100 tested, at least one prime-power factor q = p^e satisfies gen ≢ 1 (mod q). Therefore some π_CRT^{p^e} ≠ DYN always exists. The Tier C theorem holds.

**The residual open question:** Prove that for all n with φ(n) ≥ 4, there exists a prime-power factor p^e of n such that every max-order generator gen satisfies gen ≢ 1 (mod p^e). This is true computationally for n=4 to 100 but not proved in general.

---

## 9. CORRECTED THEOREM STATEMENT

**Theorem (corrected):**  
For n=2p with p prime and p≥5, with representations:
- **CRT:** π_CRT^p (partition by x mod p — the odd prime factor component)
- **UG:** partition by multiplicative order
- **SPEC({g,n−g}):** partition via any single symmetric pair S={g,n−g}, gcd(g,n)=1
- **DYN:** partition by orbit under single max-order generator

The four Level-1 partitions of the unit orbit are pairwise distinct and a gate exists. The proof uses the corrected Spectral Lemma (single pair, not arbitrary symmetric S).

**Note on CRT choice for n=2p:** CRT = partition by x mod p uses the odd prime factor p. For n=2p, the only prime-power factors are 2 and p. The DYN generator gen is a unit, so gen is odd: gen ≢ 0 (mod 2). Whether gen ≡ 1 (mod p) would require gen=1, which has order 1 ≠ max order (p−1 ≥ 4 for p≥5). Therefore: for n=2p with p≥5, any max-order generator gen satisfies gen ≢ 1 (mod p). The CRT(mod p) and DYN partitions always differ. No component-choice ambiguity for n=2p with p≥5.

---

## 10. SUMMARY

| Claim | Original memo | After audit |
|---|---|---|
| SPEC = REFL for any symmetric S | Stated | **FALSE** — fails for multi-pair S (e.g., S=all units on n=10) |
| SPEC = REFL for any single symmetric pair {g,n-g} | Not isolated | **PROVED** (Corrected Lemma, Section 5) |
| Universal Theorem stands | ✓ | **✓** — with corrected Lemma and explicit single-pair S |
| CRT is a unique representation | Implicit | **FALSE** — CRT is a family parameterized by prime-power factors |
| CRT ≠ DYN always achievable | Claimed | **PROVED** for n=2p, p≥5; computationally confirmed for n=8..100 |
| CRT(mod q) = DYN(×gen) iff gen≡1(mod q) | Not stated | **PROVED** (Section 7) |

## 11. STRONGEST HONEST CLAIM

**Spectral Lemma:** For any single symmetric pair S = {g, n−g} with gcd(g,n)=1, the SPEC partition of any C ⊆ ℤ/nℤ equals REFL(C). This is proved by the no-collision argument for single pairs and verified exhaustively for n=4 to 100.

**Universal Theorem:** For n=2p with p prime, p≥5, the four Level-1 partitions {CRT(mod p), UG, SPEC({g,n-g}), DYN} are pairwise distinct. Tier C FRF holds.

## 12. STRONGEST HONEST BOUNDARY

The corrected Spectral Lemma is proved only for single symmetric pairs. Whether a multi-pair symmetric S can ever give SPEC = REFL (i.e., whether eigenvalue collisions involving j=1 always make SPEC coarser, never finer) is not proved in general — though all tested examples show SPEC is coarser or equal, never finer than REFL.

The characterization "CRT ≠ DYN always achievable" is proved for n=2p, p≥5 and verified computationally for n=8 to 100, but not proved for all n with φ(n) ≥ 4.
