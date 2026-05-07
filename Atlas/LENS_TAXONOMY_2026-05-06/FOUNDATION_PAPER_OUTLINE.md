# FOUNDATION PAPER OUTLINE

**Date:** 2026-05-06 night
**Working title:** *"The Three-Substrate Architecture and Lens Family of the TIG Composition Lattice on Z/10Z"*

This is the **foundation paper** per Brayden's pivot — the paper that documents the substrate's own architecture so that downstream results can cite a clean foundation. NOT the methodology paper (that comes later, year 2-3, when the corpus is mature enough to be a case study). The foundation paper is the ground-truth artifact: when CL is, what its lens family looks like, and which results live at which tier.

**Sept 11 candidacy:** This paper is a STRONG Sept 11 candidate. It is bulletproof (referee-passable), foundation-establishing, and lands the substrate's own architecture honestly. See `SEPT_11_CANDIDATES.md` for the ranking.

---

## §1 — The canonical CL forcing axioms

**Source material:** `CL_FORCING_AXIOMS.md`

Statement: CL_TSML is **uniquely forced** by 9 explicit axioms (A1-A9):
- A1: 10×10 matrix on Z/10Z (substrate type)
- A2-A4: VOID and HARMONY absorbing rules with the (0,7) puncture
- A5-A6: column versions of A2/A4 (forced by commutativity-after-symmetrization)
- A7: diagonal HARMONY law (M[i,i] = 7 for i ∉ {0})
- A8: HARMONY-default (off-special, off-BUMP cells = 7)
- A9: 5 BUMP positions (forced by BDC entropy extremum) + their specific values (substrate-defining)

**Tier classification:** A1, A2-A4, A7, A9-values are Tier-A (substrate-defining); A5, A6, A8, A9-positions are Tier-B (forced).

**Three parallel substrates:** CL_TSML (73 HARMONY), CL_BHML (28 HARMONY), CL_STD (44 HARMONY) share A1-A4 absorbing structure but DIVERGE at A7 + A9-values. They are PARALLEL Tier-A substrates, not projections of each other.

**Honest framing:** CL is not "given" in the sense of "we don't know where it came from." CL is *axiomatically given* in the sense that A2-A4-A7-A9-values are taken as primitive substrate-defining choices. The choice is principled (each axiom captures a substrate-level structural fact) and the resulting matrix is uniquely determined.

---

## §2 — TSML and BHML as projections — but ONLY within their own substrate families

**Source material:** `PROJECTION_DEFINITIONS.md`

**Critical reframing:** TSML and BHML are NOT projections of each other. They are parallel Tier-A substrates. The "Being lens / Becoming lens" pedagogy of Gen 10-12 was useful for teaching but structurally inaccurate.

**The actual projections:**
- **Lens-symmetrization** (within CL_TSML family): π_RAW, π_SYM_upper, π_SYM_lower
- **σ²-triadic value/index rotation** (within any substrate family): π_value-rot^k, π_index-rot^k
- **Sub-magma scope restriction** (within any substrate family): π_S
- **Cell-difference (DOING)** (between two parallel substrates): π_DOING

Each projection is precisely defined. Most are Tier-B (forced once inputs specified). σ²-triadic value/index rotations on BHML are Tier-D (search-found candidates not yet promoted; the choice of canonical "DOING" is open).

---

## §3 — The variant catalog (the lens family)

**Source material:** `VARIANT_CATALOG.md`

For each named variant in the corpus (~50 named + 12 ring-extensions ≈ 62 total), the catalog provides:
- Construction recipe (how it was built)
- Forced-by (what derivation forces it, or "nothing — chosen" for Tier-C)
- Tier (A/B/C/D/E)
- Witness (structural fact it carries)
- Dependencies (other variants/operations it requires)
- Family closure (does adding this preserve family membership?)

**Distribution by tier:**
- Tier A: 5 variants (CL_TSML, TSML_RAW, CL_BHML, CL_STD, F_p choice)
- Tier B: ~21 variants (chain scopes, lens-symmetrizations, sub-magma restrictions, DOING)
- Tier C: ~9 variants (TSML_PureIdempotent, TSML_C0, etc.)
- Tier D: ~7 variants (σ²-triadic candidates, anomaly-flips, Fano subsets)
- Tier E: ~8 variants (Z/n ring extensions)

The catalog confirms tier-discipline. Each variant has a precise lineage and tier label.

---

## §4 — Closure properties of the families

**Source material:** `CLOSURE_PROPERTIES.md`

Within each substrate family:
- CL_TSML closes under lens-symmetrization, sub-magma restriction, σ²-conjugation, F_p extension. Leaves under axiom modification.
- CL_BHML closes under sub-magma restriction, σ²-triadic rotations, anomaly-flip, F_p extension. Leaves under puncture-chain modification.
- CL_STD has open closure analysis (sub-magma variants not yet enumerated).

**Cross-family:**
- DOING construction LEAVES TSML and BHML families; ENTERS DOING family.
- F_p extensions form their own ring-family indexed by p.
- Tier-C parallel constructions (TSML_PureIdempotent, etc.) are NOT in any substrate's closure; they are independent.

The three substrate families are closed but **disjoint**. The lens family is properly stratified by Origin tier.

---

## §5 — Specific results requiring specific variants

**Source material:** `TABLE_INDEPENDENCE_LEDGER.md` §3 (table-dependent claims)

22 claims that depend on a specific variant, properly scoped:

- **TSML_RAW-specific:** WP107 wobble (c_2 = 33 = 3·11; c_8 = −120736 = −2⁵·7³·11). The wobble theorem holds on TSML_RAW only; symmetrization erases it.
- **TSML_SYM-specific:** the canonical "12.8%" non-associative rate; Sprint 17 tower reconstruction.
- **BHML-specific:** 28 HARMONY count; det = −7002; the puncture chain 7→8→9→0.
- **CL_STD-specific:** 44 HARMONY count; BDC encoding parameters (5 BUMP_PAIRS, INFO constants, GRAVITY).
- **Joint TSML × BHML:** 4-core attractor at α=1/2 with H/Br = 1+√3; the joint 8-shell chain; LMFDB 4.2.10224.1 quartic; FIELD WOBBLE 71 cells.
- **Off-chain scope variants:** BHML_8_YM det = +70 EXACTLY = C(8,4); TSML_8_YM as parallel; the corner sub-magma C = (Z/10Z)*; the corner monoid {0,1,5,6}.

Each claim is honestly scoped to the variant required. **No Tier-D is presented as Tier-A/B in load-bearing claims** (per `TABLE_INDEPENDENCE_LEDGER.md` §5.5).

---

## §6 — Specific results requiring no specific variant (substrate-operator claims)

**Source material:** `TABLE_INDEPENDENCE_LEDGER.md` §1

14 claims that live at the level of operators 0-9 + σ + Z/10Z arithmetic. No TSML/BHML/STD specific matrix is required:

- The 10-operator menu (VOID, LATTICE, COUNTER, ..., RESET)
- σ permutation = (0)(3)(8)(9)(1 7 6 5 4 2)
- Conservation Tetrad {0,3,8,9}, Manifestation Hexad {1,2,4,5,6,7}
- Cycle A {1,6,4} sum 11 (WOBBLE), Cycle B {7,5,2} sum 14 (= 2·HARMONY)
- 4-core operator set {0,7,8,9} = Conservation Tetrad XOR PROGRESS↔HARMONY swap
- β_3 SM = −7 = −HARMONY (SM β-coefficient identity)
- M_22 substrate-prime: \|M_22\| = 2⁷·3²·5·**7**·**11** (factor primes match substrate)
- E_6 has 72 positive roots (canonical Lie algebra; identification with TSML.HARMONY−1 is lens-invariant)
- dim G_2 = 14 = 2·HARMONY; dim SO(8) = 28 = BHML.HARMONY (numerical matches)

These claims survive any lens choice, any table swap, any future framework alteration. They constitute the **strongest spine** of the corpus.

---

## §7 — The σ²-triadic family (open: which DOING is canonical?)

**Source material:** `PROJECTION_DEFINITIONS.md` §2

Three candidate "BHML_DOING" matrices exist (value-rotation, index-rotation, anomaly-flip families), all currently Tier-D (search-found). Per Brayden's hypothesis "there may be three BHMLs," the σ²-triadic structure suggests three canonical BHML matrices, but the choice among the candidates requires:
- An explicit forcing argument (analogous to D78's BR-factor cancellation argument that promoted α-uniqueness from Tier-D to Tier-B), OR
- An empirical disambiguator (a measurement that picks one candidate over the others)

**Open question:** which candidate, if any, is the canonical "BHML_DOING"? Currently undecided.

---

## §8 — F_p ring extensions (open: full enumeration)

The TSML / BHML / STD families extend over F_p for p ∈ {2, 3, 5, 7, 11, 13} (per the bridge sprint companion in preparation). Chain rigidity preserves; structural details (det signatures, char polys) vary by p.

**Open work:** The CL_STD family's F_p extensions have not yet been computed. The four-core consolidated paper notes this as future work.

---

## §9 — Where the foundation paper sends the reader

After §1-§8, the foundation paper concludes by directing readers to:

1. **The σ-rate companion** (Sanders + Gish, in prep. for JCT-A): a Tier-A+B claim about CL_N over Z/NZ, table-independent at the family level (see TABLE_INDEPENDENCE_LEDGER §1).
2. **The four-core consolidated companion** (Sanders + Gish, in prep. for Algebraic Combinatorics): joint TSML+BHML chain + closed-form attractor + LMFDB 4.2.10224.1 quartic. Tier-A+B with explicit scope to TSML_SYM in cell-level results.
3. **The xi cosmology companion** (Sanders + Johnson, in prep. for JCAP): a Phase-2 physics application that uses substrate-operator claims (Tier-A+B) for its derivations.
4. **The methodology paper** (Year 2-3): the deeper synthesis paper (working title *"Finite Algebra Construction: A Taxonomy of Usage Tiers"*) that uses the TIG corpus as its case study. Waits until the corpus is mature enough that the methodology has earned its case study.

---

## §10 — What the foundation paper does NOT do

- Does NOT claim a unifying framework called "TIG" — the framework name is reserved for downstream synthesis papers.
- Does NOT use the threshold T* = 5/7 in the methodology layer (per Popper-Carnap-Lakatos-FAIR consensus that methodology must not depend on substrate-specific constants).
- Does NOT present any Tier-D variant as Tier-B without explicit forcing argument.
- Does NOT claim CL is "given by God" or "given by the universe" — CL is axiomatically given via 9 explicit axioms; the axioms are substrate-defining choices.
- Does NOT use the Universal Operator Paradox (UOP) classifier in the methodology layer (per `UOP_PRIOR_ART.md` recommendation; UOP appears only in the case-study section if at all).

---

## §11 — Length and scope

**Target length:** 25-35 pages.

**Audience:** Working algebraists (Drápal-Wanless / McKay-Wanless tradition), reverse mathematicians (Simpson tradition), universal algebraists (Burris-Sankappanavar / Hobby-McKenzie tradition). Plus physicists and number theorists who want to know what the TIG substrate IS before they engage with TIG-specific results.

**Style:** Cite established literature aggressively. Adopt finite-algebra vocabulary (isomorphism class, isotopy class, paratopism, sub-magma, Mal'cev condition). Add tier vocabulary explicitly (Tier-A canonical, Tier-B forced, Tier-C constructed, Tier-D searched, Tier-E fitted) but introduce it carefully in §1 with reverse-mathematics + Bishop-Bridges-Richman + Alon-Spencer anchoring.

**Tone:** Honest. Each axiom and each claim is labeled with its tier and its scope. The paper avoids both overclaim (presenting Tier-D as Tier-A/B) and underclaim (hiding genuine forcing arguments behind "we exhibit").

---

## §12 — Citations (load-bearing 10-citation set + extensions)

From `EXTERNAL_RIGOR.md`:

1. **Ranganathan 1967** — facet methodology lineage (used in §3 multi-axis intersection)
2. **Hjørland 2013** — modern restatement (used in §3)
3. **Simpson 2009** — tier reasoning is canonical (used in §1, §3, §5)
4. **Bridges-Richman 1987** — tier-classifying constructions (used in §1, §3)
5. **Alon-Spencer 2016** — existence-vs-explicit-construction (used in §1)
6. **Hobby-McKenzie 1988** — structural classification anchor (used in §3, §4)
7. **Drápal-Wanless 2021** — working-practice motivation (used in §3, §11)
8. **McKay-Wanless 2005** — Tier-D as distinct mode (used in §1, §3)
9. **Anderson-Krathwohl 2001** — orthogonality-as-design-intent (used in §3 if 3-axis kept)
10. **Peirce *Collected Papers* via T. L. Short 2007** — triadic precedent (used in §3 if 3-axis kept)

**Extensions for the foundation paper specifically:**
- **Burris-Sankappanavar 1981** — universal algebra textbook (used in §1, §4)
- **CFSG (Gorenstein-Lyons-Solomon)** — gold-standard structural classification (used in §3)
- **LMFDB Collaboration 2024** — number-field 4.2.10224.1 (used in §5)
- **Drápal-Lisoněk 2020** — quadratic orthomorphisms in quasigroup theory (used in §11)

---

## §13 — Section-by-section drafting status (as of 2026-05-06 night)

| § | Topic | Drafting status | Source documents |
|---|-------|----------------|---------------------|
| 1 | CL forcing axioms | DRAFTABLE NOW | `CL_FORCING_AXIOMS.md` |
| 2 | Projection definitions | DRAFTABLE NOW | `PROJECTION_DEFINITIONS.md` |
| 3 | Variant catalog | DRAFTABLE NOW (large; 50+ entries) | `VARIANT_CATALOG.md` |
| 4 | Closure properties | DRAFTABLE NOW | `CLOSURE_PROPERTIES.md` |
| 5 | Table-dependent results | DRAFTABLE NOW | `TABLE_INDEPENDENCE_LEDGER.md` §3 |
| 6 | Substrate-operator results | DRAFTABLE NOW | `TABLE_INDEPENDENCE_LEDGER.md` §1 |
| 7 | σ²-triadic open question | DRAFTABLE NOW (with explicit "open" framing) | `PROJECTION_DEFINITIONS.md` §2 |
| 8 | F_p extensions | DRAFTABLE NOW (cite bridge sprint companion) | `VARIANT_CATALOG.md` §1, §2 |
| 9 | Companion-paper directional | DRAFTABLE NOW | The four Phase-1+ companions |
| 10 | What the paper does NOT do | DRAFTABLE NOW | `EXTERNAL_RIGOR.md` (T* exclusion) + `UOP_PRIOR_ART.md` (UOP exclusion from methodology) |

**All sections are draftable from the documents in `Atlas/LENS_TAXONOMY_2026-05-06/`.** The foundation paper can be assembled from the existing material in 1-2 work-days of careful drafting.

---

## §14 — The Sept 11 question

This foundation paper is a strong Sept 11 candidate because:

1. **Bulletproofness:** It documents the substrate's architecture honestly with explicit tier discipline. A referee can verify each axiom and each claim against the source documents. No overclaim.

2. **Foundation-establishing weight:** It anchors all downstream TIG papers in a precise foundation. After this paper, every other paper can cite §1-§9 for "what the substrate is and which variant is being used."

3. **"All things new" / daughter's birthday register:** The paper's central act is to STATE the substrate honestly. It doesn't claim a new framework or a new physics — it just documents what's been there all along, with the precision that makes it citable. That's the recognition register: the math isn't created on Sept 11; it's revealed.

4. **Independent of methodology paper:** The foundation paper stands without the methodology paper. The methodology paper waits for year 2-3 when the corpus has matured into a case study. Sept 11 doesn't need both papers; it needs the right one.

The foundation paper's central recognition: **CL is forced by 9 axioms; three parallel substrates share A1-A4 and diverge at A7-A9-values; the lens family is the natural enumeration of variants under the projection operators; the 14 substrate-operator claims constitute the framework's strongest spine.** That's a clean Sept 11 statement.

---

## §15 — What this outline does NOT commit to

- Does NOT commit to a specific length (25-35 pages is target; could be longer if §3 catalog needs full table)
- Does NOT commit to a specific venue (Algebraic Combinatorics, J. Algebra, J. Pure Applied Algebra, or expository like Bull AMS / Notices are all candidates; Brayden picks)
- Does NOT commit to a specific co-author byline (Sanders + Gish for the TSML/BHML table-family work, but Brayden picks)
- Does NOT commit to drafting tonight (the outline is documented; drafting is later)

The outline is the spine. The drafting follows when Brayden directs.
