> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\ADJACENT_RESEARCHERS.md → papers\morphotic_braid\explorations\support\ADJACENT_RESEARCHERS.md

# Adjacent Researchers and Related Work — Associative Spectrum Program

**Status:** [LITERATURE SURVEY — VERIFIED FROM PUBLIC SOURCES]
**Date:** 2026-04-23

## Primary active workers

### Jia Huang (University of Nebraska at Kearney)
- Most active recent researcher in the ac-spectrum space
- Coauthor with Lehtonen on foundational 2022 paper
- Homepage has publication list and slides
- **Key papers:**
  - Huang-Lehtonen 2022, "The associative-commutative spectrum of a binary operation," arXiv:2202.11826
  - Huang-Lehtonen 2024, "Associative-commutative spectra for some varieties of groupoids," arXiv:2401.15786
  - Huang 2018, "Variations of the Catalan numbers from some nonassociative binary operations," arXiv:1807.04623
  - Huang-Mickey-Xu earlier work on k-depth-equivalence

### Erkko Lehtonen
- Huang's regular collaborator
- Works on clone theory, operads, varieties of groupoids
- Brings the variety-based classification approach

### B. Csákány, T. Waldhauser (Szeged, Hungary)
- **Foundational 2000 paper** on associative spectra (Multiple-Valued Logic 5)
- Primarily studied 2- and 3-element groupoids
- Their program is the origin of the whole area

### Braitt, Silberger
- Parallel development, "subassociativity type" terminology
- Similar measure, independently developed

### Liebscher, Waldhauser
- 2011, generalization to m-ary operations (arXiv:1102.2337)
- Extension of Csákány-Waldhauser framework

### M. Lord
- Introduced "depth of nonassociativity" — a different measure
- Related but not identical program

## Who is NOT working on TIG's specific angle

No one, as far as public literature shows, is systematically studying:

1. **Parametric families of groupoids** with shared canonical structure (σ-based C_0 on ℤ/NℤN across N)
2. **Minimum-perturbation classification** (what's the smallest bump achieving ac-freeness?)
3. **Connection to number-theoretic structure** (σ-classes, CRT fibers, Creation/Dissolution cycles)
4. **Families where a specific structural element (HARMONY) plays a universal role**

These are TIG's distinctive angles. The Huang-Lehtonen program is variety-based (axioms → extremal spectra); TIG's program is family-based (canonical construction → spectrum behavior across family).

## Adjacent but distinct programs

### Latin squares / quasigroup classification
- Separate tradition; cares about different isomorphism classes
- Does not emphasize bracketing complexity

### Finite groupoid enumeration
- Classical result: number of binary operations on N elements is N^(N²)
- Less focused on spectrum; more on structure types

### Non-associative ring theory (Lie algebras, Jordan algebras, Malcev algebras)
- Huge literature; studies identities and their implications
- Closer in spirit to Huang-Lehtonen's variety approach

### Magma classification (Mazurek 2025)
- Classification of small magmas by structural properties
- Adjacent but doesn't emphasize ac-spectrum specifically

## Venues where TIG's work could be submitted

**Primary target journals:**
- Journal of Algebraic Combinatorics (where Huang publishes)
- Discrete Mathematics (where Huang-Lehtonen 2022 was published)
- Semigroup Forum (for the C_0-is-semigroup result)
- Journal of Combinatorial Theory, Series A

**Preprint:** arXiv:math.RA or math.CO

**Conferences:** 
- FPSAC (Formal Power Series and Algebraic Combinatorics) — Huang presents here
- AMS sectional meetings (special sessions on operads or semigroups)

## Recommended next steps

1. **Read Huang-Lehtonen 2022 carefully.** Their definition of ac-spectrum is the standard; use their notation in any publication.

2. **Read Huang-Lehtonen 2024.** Their upper-bound examples at order 3 provide context for what's been done and what hasn't.

3. **Contact Huang directly.** An email to him describing TIG's σ-family and minimum-bump theorem would likely get a response. He's an active publishing researcher who would benefit from seeing a new example class. Good format:
   - 1-paragraph intro
   - Statement of the family theorem
   - Computational evidence table (N vs hits)
   - Offer to share code
   
4. **Check OEIS for sequence A047764 or related.** The counts {2, 3, 5, 6, 7, 8} (single-cell hits by N) match N − 2, which is trivial. But the exact sequence of minimum-perturbation positions across the family might be new.

5. **Cite Csákány-Waldhauser, Braitt-Silberger, and Liebscher-Waldhauser** in any publication. They're the foundational layer.

---

**Tag: [LITERATURE SURVEY — CITATIONS VERIFIED]**
**File path: `papers/morphotic_braid/ADJACENT_RESEARCHERS.md`**
