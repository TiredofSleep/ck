# SAVE_PLAN_J11 — Corrected Theorem C: M+A Sufficiency on Squarefree Z/nZ

**Paper:** J11 — *Corrected M+A Sufficiency on Squarefree Z/nZ via Zero-Fiber Analysis*
**Authors:** B. R. Sanders, M. Gish
**Target venue:** *Journal of Number Theory* (short note format)
**Referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J11_JNT_FreshEyes.md`
**Status before fix:** MAJOR REVISIONS (close to "Accept with minor"). Math correct; presentational issues.
**Status after fix:** REVISION DRAFTED. Standalone-style; UOP appeal removed; "previously stated condition" reframed as natural conjecture; zero-fiber analysis promoted to structural lemma; J10 dependency removed.

---

## §1 — The errors and the fixes

### Referee verdict

The mathematics is correct. The n=15 counterexample is real and surprising; the corrected theorem is a clean and useful statement. The CRT-coordinate proof is internally complete. The submission is, in the referee's view, a more substantive contribution than its J10 lead companion and could plausibly stand alone in JNT *if* the dependence on J10 is removed, the prior-literature gap is filled, and several exposition issues are addressed.

### Major revisions adopted

| Referee item | Disposition |
|---|---|
| **M1.** "Previously stated condition" needs citation | **Fixed.** Reframed as a *natural conjecture* — the unit-only argument is presented as an honest first-pass derivation that a reader would naturally produce; "previously stated" language dropped. No external citation needed (the condition was a passing remark in earlier internal notes; no published source exists). |
| **M2.** UOP-companion dependence is uneven | **Fixed.** Adopted Option A (independent paper). The proof of Theorem 3.1 now uses only the direct CRT-coordinate argument; the UOP appeal is removed. The J10 paper is cited only for context, not for load-bearing content. |
| **M3.** Theorem C is symmetrized form, not new | **Fixed.** §1 now states explicitly that the corrected condition is the symmetric form of the established A+M classification (which is itself a folkloric CRT-coordinate result, also proved here for self-containment). The theorem is presented as a *corrected statement* of M+A, not as a fundamentally new theorem. Paper condensed to short-note format (~5 pages from ~6). |
| **M4.** Zero-fiber analysis should be promoted | **Fixed.** Proposition 4.1 (action of G on F_d) is now Lemma 1.1 in the introduction, motivating the corrected condition before it is stated. The recursive structure (zero-fiber is a smaller copy of the same problem on n/d) is articulated explicitly. |
| **M5.** §5 should illustrate disagreement parametrically | **Fixed.** Added Example 4.3 — the family n = 3p for primes p ≡ 1 (mod 3), G non-trivial mod 3 but injective into (Z/p)*, d = p — exhibits an infinite family where the prior conjecture and corrected theorem disagree. |
| **M6.** "Established A+M classification" needs citation or proof | **Fixed.** Theorem 3.2 (A+M classification) is now stated and proved inline by a 6-line CRT argument, making the paper self-contained. |
| **M7.** Unit-only argument framed as if complete | **Fixed.** §1.2 heading changed to "The unit-only argument (incomplete)"; opening paragraph signals up-front that this is the first-pass derivation being analyzed. |

### Minor fixes adopted

m1 (title shortened), m2 (duplicate author block removed), m4 (singularize "applications"), m5 (note unit-mod-d via surjection), m7 (rephrase "trivially on every prime" → "trivially at every prime"), m9 (clearer case structure with §3 lemma covering trivial-action degeneracy), m11 (clarify mod-2m arithmetic), m12 (fold §6.1 into intro), m14 (sharpen open question (b)), m15 (drop irrelevant Crossing Lemma citation).

### Family-Structure framing added

Per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`, the paper carries:
- A lens-ownership paragraph (substrate Z/nZ + the partition-pair lens; the choice of partition classes is foundational, not derived).
- The PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN tier discipline at the end of §1.
- Cite Drápal-Wanless 2021 (*JCTA*) as the closest published precedent for finite-CRT-flavored partition-lattice work in the same neighborhood (different specific topic, same intellectual lineage of "small finite combinatorial structure with explicit CRT-coordinate criteria").

---

## §2 — Independent verification of all numerical claims

All claims hand-checkable; ran via numpy:

```
=== J11: n=15, G=<2>, d=5 ===
G = <2> mod 15 = [1, 2, 4, 8]
phi(G mod 5) = [1, 2, 4, 3]    (bijection onto (Z/5)*)
F_5 = [0, 5, 10]
Orbit of 5 under T_2: [5, 10]   (size-2 orbit in F_5, both 0 mod 5)
2 mod 3 = 2                     (G non-trivial on n/d = 3)

=== J11 control: n=30, G=<11>, d=5 ===
G = <11> mod 30 = [1, 11]
phi(G mod 5) = [1, 1]           (NOT injective: phi(11) = 1 = phi(1))
Orbit of 5 under T_11: [5, 25], both 0 mod 5: True
```

Confirmed:
1. G = ⟨2⟩ in (Z/15)* has order 4; φ is a bijection.
2. Orbit of 5 under T_2 in Z/15 is {5, 10}, both in zero-fiber F_5.
3. The pair {5, 10} is a conflict in U(π_DYN(G)) ∩ U(π_5).
4. CRT decomposition: 5 = (2,0) and 2 = (2,2) give 2·5 = (1,0) = 10. Confirmed.
5. The control example n=30, G=⟨11⟩, d=5 has φ not injective AND fails the corrected condition (both reasons for non-sufficiency align).
6. The corrected condition predicts non-sufficiency at n=15 because 2 ≡ 2 (mod 3), so G acts non-trivially on n/d = 3.

---

## §3 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:**
  - Theorem 3.1 (corrected M+A): For squarefree n = p₁⋯pₖ, G ≤ (Z/n)*, d | n, the pair {π_DYN(G), π_d} is sufficient iff every g ∈ G satisfies g ≡ 1 (mod p_j) for every prime p_j | n/d.
  - Theorem 3.2 (A+M classification, inline proof): same condition characterizes A+M sufficiency. The two are the same condition by the symmetry of joint-map injectivity.
  - Lemma 1.1 (zero-fiber action): G preserves F_d setwise, every G-orbit on F_d lies in the zero block of π_d, and conflicts on F_d exist iff G acts non-trivially on n/d.
- **COMPUTED:**
  - The n = 15 counterexample verified by direct enumeration (orbit of 5 under T_2 in Z/15 gives {5, 10} ⊂ F_5 = {0, 5, 10}).
  - The control n = 30, G = ⟨11⟩ cross-checks both prior and corrected conditions (both fail; consistent).
  - Smallest cases of the parametric disagreement family n = 3p exhibited at p = 7, 13, 19 (p ≡ 1 mod 3 with the specific G of order divisible by 3).
- **STRUCTURAL RHYME:**
  - The recursive structure of the zero-fiber as a smaller copy of the original problem (F_d ≅ Z/(n/d) as G-set) is a structural-rhyme observation; the recursive descent is not unrolled in this paper.
  - The "previously stated unit-only condition" is named as the *natural conjecture* a reader would produce after one careful pass through the unit-fiber argument; this is honest framing, not citation-free reference to an unspecified prior literature.
- **OPEN:**
  - Classification of M+A-sufficient G for fixed d: the corrected theorem says the admissible G are precisely subgroups of ker(Φ: (Z/n)* → ∏_{p_j|n/d} (Z/p_j)*). A finer combinatorial classification of which G are *maximally* non-trivial on d while remaining admissible is open.
  - Extension to non-squarefree n via p-adic components.

---

## §4 — Lens-ownership paragraph (drafted for §0 of manuscript)

> *Lens and substrate.* This paper works on Z/nZ for squarefree n with k ≥ 2 prime factors, with the partition-pair lens consisting of multiplicative orbit partitions π_DYN(G) (G ≤ (Z/n)*) and additive residue partitions π_d (d | n). These choices are not derived from first principles; they are the two natural classes that arise from the multiplicative-additive structure of (Z/n)* acting on Z/n. The theorems below are theorems on this specific structure; analogous theorems would hold for other choices of partition classes (e.g., subset-lattice partitions, equivalence partitions induced by other group actions). The framework's claim is that these two classes admit a clean joint-injectivity criterion, with the corrected M+A condition (Theorem 3.1) as the symmetric form of the established A+M criterion. Whether other partition-class pairs admit similarly clean joint-injectivity criteria is left open.

---

## §5 — Estimated revision time

- **Manuscript rewrite:** **DONE** (this turn). New `manuscript.tex` written. ~3 h equivalent.
- **README + cover letter update:** **DONE** (this turn). README.md §5 + cover_letter.md updated.
- **Final read-through:** ~30 min.

**Total residual to submission-ready:** ~30 min after this turn.

The paper is now a clean ~5-page short note in the form "natural conjecture → counterexample → corrected theorem → structural reason → applications", explicitly self-contained, with the J10 reciprocal-citation removed and the prior-literature gap honestly addressed by reframing as natural conjecture.

This is appropriate for *Journal of Number Theory* short-note format. The referee called it "the strongest" of the J10/J11/J12 cluster and "the most JNT-appropriate"; with these revisions, it should clear the JNT bar.
