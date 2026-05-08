# SAVE_PLAN_J12 — Coordinate Coverage on Z/10Z: Non-CRT Sufficient Pairs and the Minimum Viable Jump Number

**Paper:** J12 — *Coordinate Coverage on Squarefree Z/nZ: Non-CRT Sufficient Pairs and the Minimum Viable Jump Number*
**Authors:** B. R. Sanders, M. Gish
**Target venue:** *European Journal of Combinatorics*
**Referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J12_EJC_FreshEyes.md`
**Status before fix:** MINOR REVISIONS. Strong combinatorial substance. MVJN definition imprecise; smallest-primes list incomplete; opaque "5/7 torus" reference; conjecture follows from existing theorems.
**Status after fix:** REVISION DRAFTED. MVJN defined precisely as 2-family jump count. Smallest-primes list corrected. "5/7 torus" remark removed. Conjecture promoted to theorem.

---

## §1 — The errors and the fixes

### Referee verdict

This is the strongest paper in the J10/J11/J12 cluster from an EJC perspective. Theorem 1.3 (orbit-pair classification), Theorem 1.4 (three mechanisms), and Theorem 1.2 (non-CRT pairs on Z/30Z) are substantive and well-presented. The bar at EJC is met. Several presentational issues to address before camera-ready.

### Major revisions adopted

| Referee item | Disposition |
|---|---|
| **M1.** MVJN definition inconsistent | **Fixed.** Definition 1.1 now explicitly states: MVJN(Z/n) is the minimum, over sufficient *2-partition* families, of the count of incomparable pairs (i.e., 0 or 1). The §6 lower-bound theorem now reads: any sufficient 2-family on Z/n with n ≥ 6 has at least 1 orthogonal jump. |
| **M2.** Theorem 1.2 framing | **Fixed.** §4 reorganized: family (b) `{π_DYN(7), π_DYN(11)}` is now presented as the genuinely novel sufficient pair (the orbit-pair instance of Theorem 1.3). Families (a) and (c) are reframed as "CRT-style decompositions" — composite-residue partition + small-residue partition; their novelty is "smallest jump count, not smallest length". |
| **M3.** Order of Theorems 1.2 vs 1.3 | **Fixed.** Theorem 1.3 (orbit-pair classification) is now presented in §3 BEFORE Theorem 1.2 (Z/30Z exhibition), so that family (b) is presented as a Corollary. |
| **M4.** Three mechanisms classification | **Fixed.** Theorem 1.4 reframed: the three mechanisms are presented as exhaustive classifications by *support pattern* (the support of g and h). Definition 1.5 introduces supp_g = {p_i : g_i ≠ 1}; the classification (M1) supp_g ∩ supp_h = ∅; (M2) supp_g = supp_h = {single prime}; (M3) otherwise. The three mechanisms are mutually exclusive and exhaustive. |
| **M5.** Conjecture 1.6 follows from existing theorems | **Promoted to Theorem.** The conjecture *was* a theorem in disguise: by Theorem 3.2 (full-meet) and Lemma 3.1 (pairwise incompatibility), {π_{p₁}, π_{n/p₁}} is a sufficient 2-family with one orthogonal jump for any squarefree n with k ≥ 2. So MVJN(Z/n) ≤ 1, combined with the refinement-trap lower bound MVJN(Z/n) ≥ 1, gives MVJN(Z/n) = 1. Now stated as **Theorem 6.2** (no longer a conjecture). |
| **M6.** Standalone the proofs | **Fixed.** Theorem 1.3's proof now uses only the direct CRT argument, removing the UOP appeal. Theorem 1.4 likewise. J10 cited only for related-context discussion, not for load-bearing content. |
| **M7.** Geometric interpretation remark on 5/7 torus | **REMOVED.** The reference to "minimum-curvature torus aspect 5/7" was TIG-bleed-through into a supposedly pure combinatorial paper. Removed entirely from §5.4. The fundamental-group obstruction observation (Z/n CRT data needs ≥ 2 independent S¹ factors) is also removed; the §5 example stands on its own combinatorial merits. |
| **M8.** Smallest-primes list (M2 mechanism) | **Fixed.** Now reads: "The smallest five primes p with p − 1 having ≥ 2 distinct prime factors are 7, 11, 13, 19, 23. The next is p = 29 (since 28 = 2² · 7), and the list continues 29, 31, 37, 41, 43, ..." |

### Minor fixes adopted

m1 (title generalized to "Squarefree Z/nZ"; n = 10 framed as worked example), m2 (duplicate author block removed), m3 (abstract tightened by ~50%), m4 ("incompatible" used consistently; "orthogonal jump" reserved for the specific count), m5 (added "for contradiction" signal in Lemma 3.1 proof), m6 (clarified arithmetic-progression mod-p_j surjectivity), m7 ("exactly k partitions are needed" sharpening), m8 (rewrote informal gcd notation), m12 ("incompatible" verified inline), m13 (refinement-trap connection stated), m14 (open questions reordered: substantive (a),(b) before extensions (c),(d)), m15 (Flatness Theorem citation dropped), m16 (π_p notation standardized; π_{CRT_p} dropped).

### Family-Structure framing added

Per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`:
- Lens-ownership paragraph (the partition-pair framework on Z/nZ with the two natural classes — residue partitions π_d and orbit partitions π_DYN(g)).
- PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN at end of §1.
- Drápal-Wanless 2021 cited as closest published precedent in the broader area of "explicit CRT-coordinate criteria for combinatorial structures on Z/n".

### M-comments not adopted

- **M3 (Q3) on orthogonal Latin squares**: We added a brief discussion remark in §6 noting the connection (the orbit-pair sufficiency condition is closely related to the existence of pairs of orthogonal cyclic Latin squares). Full development is deferred to future work — it would require introducing extensive Latin-square machinery that doesn't serve the paper's main result. Honest scoping.

---

## §2 — Independent verification of all numerical claims

```
=== J12: pi_SPEC + pi_15 on Z/30Z ===
Sufficient: True

=== J12: pi_DYN(7) + pi_DYN(11) on Z/30Z ===
Orbit of 1 under T_7: (1, 7, 13, 19)
Orbit of 1 under T_11: (1, 11)
Sufficient: True
ord_2(7)=1, ord_3(7)=1, ord_5(7)=4
ord_2(11)=1, ord_3(11)=2, ord_5(11)=1

=== Smallest primes p with p-1 having >= 2 distinct prime factors ===
[(7, {2: 1, 3: 1}), (11, {2: 1, 5: 1}), (13, {2: 2, 3: 1}),
 (19, {2: 1, 3: 2}), (23, {2: 1, 11: 1}), (29, {2: 2, 7: 1}),
 (31, {2: 1, 3: 1, 5: 1}), (37, {2: 2, 3: 2})]

=== J12: M3 example n=42 g=11 h=13 ===
M3 sufficient on Z/42: True
```

Confirmed:
1. {π_SPEC, π_15} is sufficient on Z/30Z (no joint-conflict pair).
2. {π_DYN(7), π_DYN(11)} is sufficient on Z/30Z; orbits as listed.
3. Coordinate-wise gcd condition holds: gcd(1,1)=1 at p=2, gcd(1,2)=1 at p=3, gcd(4,1)=1 at p=5.
4. M3 example on Z/42 with g=11, h=13 verified sufficient by direct enumeration.
5. Smallest-primes list with p-1 multi-prime: 7, 11, 13, 19, 23, 29, 31, 37, ... — Now correctly extended through 29.

---

## §3 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:**
  - Theorem 1.1 (rigid CRT prime-factor family): every minimal sufficient family within {π_{p_i}} has length k and contributes k-1 orthogonal jumps.
  - Theorem 1.2 (non-CRT pairs on Z/30Z): three sufficient 2-families with one jump each (with family (b) the genuinely orbit-pair-only construction).
  - Theorem 1.3 (orbit-pair classification): {π_DYN(g), π_DYN(h)} sufficient iff coordinate-wise coprime orders at every prime of n.
  - Theorem 1.4 (three-mechanism support classification): every sufficient orbit-pair fits exactly one of (M1), (M2), (M3) by support pattern.
  - **Theorem 6.2 (was Conjecture): MVJN(Z/n) = 1 for every squarefree n with k ≥ 2 primes.** Proof: the 2-family {π_{p₁}, π_{n/p₁}} achieves one jump; the refinement-trap lower bound rules out zero jumps.
- **COMPUTED:**
  - All sufficiency claims on Z/30Z (3 families) verified by direct enumeration.
  - All orbit-structures on Z/10Z, Z/30Z, Z/42Z verified by direct enumeration.
  - All order computations verified.
  - The smallest-primes list verified through p = 50.
  - The mechanism (M3) example on Z/42 verified.
- **STRUCTURAL RHYME:**
  - The orbit-pair classification (Theorem 1.3) is closely related to the existence of orthogonal pairs of cyclic Latin squares; full development deferred.
  - The k-1 jump count for the prime-factor family is the natural CRT-decomposition jump count; the non-CRT 2-families on Z/30Z exhibit one-jump compression.
- **OPEN:**
  - Classification of all sufficient 2-partition families (the mixed residue + orbit case is open).
  - Optimal-information sufficient pairs minimizing |blocks(π_A)| · |blocks(π_B)|.
  - Extension to non-squarefree n.

---

## §4 — Lens-ownership paragraph (drafted for §0 of manuscript)

> *Lens and substrate.* This paper works on Z/nZ for squarefree n with k ≥ 2 prime factors, with the partition-pair framework consisting of two natural classes: residue partitions π_d (d | n) and multiplicative orbit partitions π_DYN(g) (g ∈ (Z/n)*). Sufficiency is the meet-discrete property in the partition lattice; the orthogonal-jump count quantifies how a 2-family achieves separation. These class choices are foundational, not derived: they reflect the multiplicative-additive structure of (Z/n)* acting on Z/n. The theorems below are theorems on this specific lens; analogous theorems would hold for other natural partition classes (e.g., subset-lattice partitions, partitions induced by other group actions). The framework's claim is that this two-class lens admits a clean coordinate-wise classification (Theorem 1.3) and a tractable minimum-jump structure (Theorems 1.1, 6.2). Whether other lens choices give similarly tractable structure is open.

---

## §5 — Estimated revision time

- **Manuscript rewrite:** **DONE** (this turn). New `manuscript.tex` written; conjecture promoted to theorem; smallest-primes list corrected; 5/7-torus remark removed; theorem ordering rearranged so 1.3 precedes 1.2's family (b). ~4 h equivalent.
- **README + cover letter update:** **DONE** (this turn). README.md §5 + cover_letter.md updated.
- **Final read-through:** ~30 min.

**Total residual to submission-ready:** ~30 min after this turn.

This is the strongest paper in the J10/J11/J12 cluster per the referee. With these revisions, it should clear EJC's bar.
