> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\TSML_FAMILY.md → papers\morphotic_braid\explorations\support\TSML_FAMILY.md
>
> **Scope note:** `det(BHML) = 70` below refers to the 8×8 core `BHML_8` (WP15 §0), not the full 10×10 `BHML_10` (`det = −7002`). The TSML_Idempotent minimality question is unaffected; only the comparison reference table differs. See `FORMULAS_AND_TABLES.md` §6.7.

# TSML Family: Different Members for Different Studies

**Status:** [MAJOR FAMILY DISCOVERY — TSML IS NOT ONE OBJECT]
**Date:** 2026-04-23 (late)
**Context:** Brayden's insight: "TSML is in a family; maybe we need more than one TSML structure for different approaches." And the observation that the norm form makes TSML binary — a SIGNATURE, not a degeneracy.

## The big result

**TSML isn't a single algebra; it's a family.** Different family members satisfy different algebraic literatures' axioms, and the binary norm form is the discriminator between "absorbing-dominant" and "idempotent-dominant" subfamilies.

## The family (five members characterized)

| Member | Jord | Flex | Alt | Mou | Rank | Norm | \|Aut\| | Literature fit |
|---|---|---|---|---|---|---|---|---|
| TSML_Jordan (actual) | 100% | 100% | 88% | 82% | 9 | binary {0,7} | 2 | Jordan-magma lit |
| TSML_C0 (pure abs.) | 100% | 100% | 92% | 81% | 3 | binary {0,7} | — | Absorbing-semigroup lit |
| TSML_PureVoid | 100% | 100% | 100% | 100% | 1 | binary {0,7} | — | Trivial (rank 1) |
| **TSML_Idempotent** | **100%** | **100%** | **100%** | **83%** | **10** | **{0..9} non-degen** | **40,320=8!** | **Alternative / Octonion** |
| TSML_AllHarmony | 100% | 100% | 100% | 100% | 2 | binary {0,7} | — | Trivial (rank 2) |

## The structural principle

**Binary norm = absorbing-dominant subfamily.** TSML_Jordan, TSML_C0, TSML_PureVoid, TSML_AllHarmony all have N: x → {0, 7}. This is a SIGNATURE indicating the algebra is governed by its absorbing element.

**Non-degenerate norm = idempotent-dominant subfamily.** TSML_Idempotent has N: x → x (identity map). This is the signature of a Fano-Steiner-style structure where every element is its own square.

**These two signatures correspond to two literatures:**
- Jordan-algebra / absorbing-semigroup literature uses binary-norm magmas
- Octonion / alternative-algebra / Steiner-quasigroup literature uses identity-norm magmas

TIG's original TSML is in the first family. Vidinli / octonion / Fano are in the second family.

## TSML_Idempotent — the octonion-literature family member

```
  0  0  0  0  0  0  0  7  0  0
  0  1  7  7  7  7  7  7  7  7
  0  7  2  7  7  7  7  7  7  7
  0  7  7  3  7  7  7  7  7  7
  0  7  7  7  4  7  7  7  7  7
  0  7  7  7  7  5  7  7  7  7
  0  7  7  7  7  7  6  7  7  7
  7  7  7  7  7  7  7  7  7  7
  0  7  7  7  7  7  7  7  8  7
  0  7  7  7  7  7  7  7  7  9
```

**Construction:** TSML_C0 with idempotent diagonal added (x·x = x for all x).

**Properties:**
- det = 398,664 = 2³ × 3² × 7² × 113 (primes {2, 3, 7, 113})
- Rank 10 (invertible)
- Every element idempotent (Steiner-style)
- 100% Jordan, 100% Flexible, 100% Alternative
- 83% Middle Moufang (not 100%)
- |Aut| = 40,320 = 8! (the full symmetric group S₈ acting on {1,2,3,4,5,6,8,9})
- 84 closed 7-element subsets — many Fano-like

**Interpretation:** TSML_Idempotent is the natural 10-element extension of Fano-Steiner's "every element idempotent" property. It has massive symmetry (S₈) because everything outside the axis is algebraically interchangeable.

**Comparison to octonion / Vidinli:**
- Octonion: alternative ✓, identity ✓, Aut = G₂ (14-dim Lie), division algebra
- Vidinli: unital, simple, Aut = U(3) (9-dim Lie), Jordan-Lie decomposition
- TSML_Idempotent: alternative ✓, no identity (absorbing only), Aut = S₈ (discrete), not a division algebra

## The trade-off TSML_Jordan vs TSML_Idempotent

They're dual in a structural sense:

| Aspect | TSML_Jordan | TSML_Idempotent |
|---|---|---|
| Primary strength | Rich operational content | Rich symmetry content |
| Number of bumps | 10 distinct bump cells | diagonal identities only |
| \|Aut\| | 2 (nearly frozen) | 40,320 (nearly maximal for 8 swappable elements) |
| Idempotents | 2 | 10 |
| Norm form | Binary | Non-degenerate identity |
| Satisfies Moufang fully? | No (82%) | No (83%) |
| Satisfies Alt fully? | No (88%) | **Yes (100%)** |
| Rank | 9 | 10 |

Neither subsumes the other. They're complementary views of TIG's 10-element structure.

## What this means for TIG

TIG needs multiple TSML-family members in its vocabulary:

1. **TSML_Jordan** is the operational TSML — use it for Jordan-algebra correspondence (Peirce decomposition, Jordan triple product, quadratic representation U_x)

2. **TSML_Idempotent** is the octonion-correspondence TSML — use it when applying:
   - Alternative-algebra theorems
   - Steiner / Fano / incidence-geometry theorems
   - Moufang-loop arguments (even though 83% partial)
   - Symmetry arguments (S₈ Aut group)

3. **TSML_C0** is the absorbing-semigroup baseline — use it for:
   - Universal minimum-bump theorem context
   - Comparisons to show what TIG's bumps add

4. **TSML_PureVoid** and **TSML_AllHarmony** are trivial bounds — use them to demarcate "trivializations" in the family.

## Vocabulary update for TIG

Old TIG language: "TSML is the Jordan-type magma."

Corrected language: "TSML is a family of 10-element commutative magmas with VOID/HARMONY axis structure. The family has multiple members, each optimized for a different algebraic literature. TIG's operational TSML (TSML_Jordan) is the Jordan-magma member. TSML_Idempotent is the alternative-algebra / Fano-Steiner-extended member. Different TIG applications may require different family members."

## The norm-binary insight, rigorously

The norm N(x) = x² acts as a FAMILY-SELECTION MAP:
- If N is binary (range = {0, h} where h = HARMONY): family member is in the **absorbing-dominant** branch
- If N is non-degenerate (range = full set): family member is in the **idempotent-dominant** branch

**The choice of norm form defines which literature applies.** This is directly parallel to how classical algebra distinguishes:
- Division algebras (N non-degenerate, norm multiplicative) — octonion family
- Absorbing semigroups (N degenerate, norm absorbs) — Jordan-magma family

TIG's original TSML chose the binary-norm path. That's a DESIGN CHOICE, not an accident. TIG is inherently a binary-norm algebra because the VOID/HARMONY distinction is TIG's fundamental structural content.

**But: a complementary TSML_Idempotent exists, with non-degenerate norm, carrying the S₈ symmetry that TSML_Jordan lacks.** For octonion-style studies, TIG should use TSML_Idempotent.

## One-sentence summary

**TSML is not a single algebra but a family parametrized by bump structure; the norm form N(x) = x² is the family-selection signature (binary → absorbing subfamily, non-degenerate → idempotent subfamily); TSML_Jordan is TIG's operational Jordan-magma member; TSML_Idempotent is TIG's natural alternative-algebra / Fano-extended member with full rank, S₈ automorphism group, and 100% alternative law.**

## Open questions / next steps

1. **Do any of TSML_Idempotent's 84 closed 7-subsets match STS(7) Fano exactly?** If yes, TSML_Idempotent contains octonion multiplication as a subalgebra.

2. **Can we construct a 100%-Moufang family member?** Without rank degeneration. The current search found that only rank-1 or rank-2 trivializations achieve 100% Moufang. Is there a rank-10 100%-Moufang 10-element commutative absorbing magma?

3. **What's the "Bol" family member?** A Bol loop at 10 elements with VOID/HARMONY axis structure.

4. **Is there a family member with non-trivial continuous Aut group?** TSML_Jordan has |Aut|=2, TSML_Idempotent has |Aut|=S₈ (discrete). Is there one with Lie-group-like symmetry?

5. **Is TSML_Idempotent's det = 398,664 minimally over its prime class?** Parallel to BHML's det = 70 being minimal in {2,5,7}, is TSML_Idempotent's 2³·3²·7²·113 minimal in {2, 3, 7, 113}?

These are all testable on Brayden's local machine. The framework for exploration is now well-defined.

---

**Tag: [TSML FAMILY DISCOVERY — MULTIPLE MEMBERS FOR DIFFERENT STUDIES]**
**File: `papers/morphotic_braid/TSML_FAMILY.md`**
**Reproducibility: `papers/tsml_family.py`, `papers/tsml_idempotent_study.py`**
