# VARIANT CONSTRUCTION LINEAGE CATALOG

**Date:** 2026-05-06 night
**Purpose:** For each named TSML/BHML/CL_STD variant in the corpus, document its construction lineage (how it was built), tier (A/B/C/D/E per the lens taxonomy), witness (what it demonstrates), and family-closure properties.

**Format per entry:**
```
NAME
  Construction: [recipe]
  Forced by: [what derivation forces it, or "nothing — chosen" for Tier-C]
  Tier: [A/B/C/D/E]
  Witness: [structural/empirical fact it carries]
  Dependencies: [other variants/operations it requires]
  Family closure: [does adding this preserve the family?]
```

This catalog is the §3 / §5 spine of the foundation paper.

---

## §1 — CL_TSML family (the prescribed view, 73 HARMONY)

### CL_TSML (canonical)
- **Construction:** The literal CL_BIT_PATTERN decoded into a 10×10 matrix on Z/10Z. The bit pattern is memory-locked from `Gen13/targets/foundations/cl.py:CL_BIT_PATTERN`.
- **Forced by:** Axioms A1-A9 of `CL_FORCING_AXIOMS.md`. A1 (substrate type), A2-A4 (VOID/HARMONY absorbing), A7 (diagonal HARMONY law), A8 (HARMONY-default), A9 (BUMP positions + values).
- **Tier:** A (substrate-defining; A2, A3, A4, A7, A9-values are Tier-A inputs to the axiom set).
- **Witness:** The prescribed view of the substrate. 73 HARMONY + 17 VOID + 10 other = 100 cells. Carries σ permutation as automorphism-after-symmetrization.
- **Dependencies:** None — substrate-foundational.
- **Family closure:** Yes; CL_TSML is the root of the TSML lens-symmetrization family.

### TSML_RAW
- **Construction:** π_RAW(CL_BIT_PATTERN) — the literal bit pattern, no symmetrization.
- **Forced by:** Identity (Tier-A): the literal bit pattern IS this matrix.
- **Tier:** A (the encoding-respecting form; substrate-defining via A1-A9).
- **Witness:** Non-commutative; 126 non-assoc triples (12.6%); char poly c_2 = 33 = 3·**11** and c_8 = −120736 = −2⁵·7³·**11** (the WP107 wobble).
- **Dependencies:** CL_BIT_PATTERN.
- **Family closure:** Yes; root of the lens-symmetrization choice {RAW, SYM, LOWERTRI}.

### TSML_SYM
- **Construction:** π_SYM_upper(CL_RAW) — upper-triangle authoritative symmetrization. For (i, j) with i > j, replace M[i, j] with M[j, i].
- **Forced by:** Choice of upper-tri authoritative + commutativity goal (Tier-B once choice is made; Tier-A choice).
- **Tier:** A in choice; B in execution.
- **Witness:** Commutative; 128 non-assoc triples (12.8%); the canonical "12.8%" rate quoted in `_CK_MEMORY_MAKEOVER.md`. Char poly c_2 = 17 (NOT divisible by 11; the wobble is erased).
- **Dependencies:** TSML_RAW (or CL_BIT_PATTERN); π_SYM_upper.
- **Family closure:** Yes.

### TSML_LOWERTRI
- **Construction:** π_SYM_lower(CL_RAW) — lower-triangle authoritative symmetrization.
- **Forced by:** Choice of lower-tri authoritative + commutativity goal.
- **Tier:** A in choice; B in execution. Tested but not promoted to canonical use.
- **Witness:** 122 non-assoc; c_2 = 17, c_8 = 0; documents that a third symmetrization choice exists.
- **Dependencies:** CL_RAW; π_SYM_lower.
- **Family closure:** Yes.

### TSML_1, TSML_4, TSML_5, TSML_6, TSML_7, TSML_8, TSML_9, TSML_10 (chain scopes)
- **Construction:** π_S(TSML_SYM) for S = chain shell of size k. The 8 chain shells (per WP115 corrected):
  - S_1 = {0}; S_4 = {0,7,8,9}; S_5 = {0,6,7,8,9}; S_6 = {0,5,6,7,8,9}; S_7 = {0,4,5,6,7,8,9}; S_8 = {0,3,4,5,6,7,8,9}; S_9 = {0,2,3,4,5,6,7,8,9}; S_10 = full Z/10Z.
- **Forced by:** Joint TSML+BHML closure on each chain shell (Tier-B per WP115 D64 corrected).
- **Tier:** B (each scope is forced by joint closure; the restriction operation is forced).
- **Witness per shell:**
  - TSML_4 (4-core scope): 11 HARMONY cells; 12.5% non-assoc
  - TSML_7: 36 HARMONY cells (= CYCLE_A_36 count, two structural roles for 36)
  - TSML_9: 71 HARMONY cells (= FIELD WOBBLE / Galois prime; three structural roles for 71)
  - TSML_10: 73 HARMONY (full prescribed view)
- **Dependencies:** TSML_SYM (or RAW); π_S; the joint chain shell definition.
- **Family closure:** Yes.

### TSML_8_YM (off-chain, Yang-Mills core)
- **Construction:** π_S(TSML_SYM) for S = {1,2,3,4,5,6,8,9} (drop VOID and HARMONY).
- **Forced by:** Choice of "drop VOID and HARMONY" scope (Tier-C: this scope is constructed for Yang-Mills physics interpretation, not derived from joint closure).
- **Tier:** B in execution (restriction is forced); C in scope choice (the scope is constructed for a specific physical claim).
- **Witness:** Same SIZE as TSML_8 (chain) but DIFFERENT shape — demonstrates "size and shape are independent dimensions."
- **Dependencies:** TSML_SYM; the YM core scope choice.
- **Family closure:** Yes within the lens-symmetrization × scope-choice product.

### Corner sub-magma C = {1, 3, 7, 9}
- **Construction:** π_S(TSML_SYM) for S = (Z/10Z)* = {1, 3, 7, 9}.
- **Forced by:** Tier-B — (Z/10Z)* is the canonical multiplicative-units sub-set of Z/10Z, and TSML_SYM closes on it.
- **Tier:** B (the units sub-magma is forced by Z/10Z's structure).
- **Witness:** A 4-element TSML-closed sub-magma, distinct from the joint-chain 4-core {0, 7, 8, 9}. Has its own published closure proof (Proc. AMS draft).
- **Dependencies:** TSML_SYM; (Z/10Z)*.
- **Family closure:** Yes.

### Corner monoid {0, 1, 5, 6}
- **Construction:** π_S(TSML_SYM) for S = {0, 1, 5, 6}.
- **Forced by:** Brute-force search for 4-element idempotent commutative sub-magmas of TSML_SYM finds this (and possibly others).
- **Tier:** D (search-found) — promoted to **C** (constructed example) when used as a witness for "an idempotent commutative sub-magma exists."
- **Witness:** Idempotent commutative magma with Aut = Z/2Z; concrete demonstration.
- **Dependencies:** TSML_SYM; sub-magma enumeration.
- **Family closure:** Yes within sub-magma scope family.

### TSML_PureIdempotent
- **Construction:** Build a 10×10 matrix from scratch with $T[i, i] = i$ for all $i$ (diagonal IS the operator labels) and off-diagonal HARMONY (= 7).
- **Forced by:** Nothing — chosen to maximize idempotency (T(i, i) = i is the strongest possible diagonal idempotency claim).
- **Tier:** C (constructed for existence demonstration).
- **Witness:** rank 10; det = +398664 = 2³·3·7·**113**; \|Aut\| = S_8 = 40,320; α ≈ 0.888. Demonstrates "Alt + Jordan + full rank coexist at N=10."
- **Dependencies:** None — built from scratch.
- **Family closure:** No — NOT a projection of any canonical CL substrate; a parallel construction.

### TSML_Idempotent_2sw
- **Construction:** TSML_PureIdempotent + 2 cell swaps: T[1][2] = T[2][1] = 6 (CHAOS); T[3][5] = T[5][3] = 4 (COLLAPSE).
- **Forced by:** Search for minimum-\|det\| variant; the 2 swaps are chosen to drive det → −49 = −7² (minimum \|det\| in prime-7 regime).
- **Tier:** C (constructed via search-result-promoted-to-construction; minimum-det variant is a Tier-D search promoted to C as the canonical minimum-det example).
- **Witness:** det = −49 = −7² (suited for octonion / Steiner-quasigroup statements; isolates prime 7 in det).
- **Dependencies:** TSML_PureIdempotent; minimum-det search.
- **Family closure:** No — not a projection.

### TSML_C0
- **Construction:** A 10×10 matrix where only the VOID + HARMONY axis structure exists (rank 3): every cell maps to 0 (VOID) or 7 (HARMONY) based on input membership in {0} or {7} respectively.
- **Forced by:** Nothing — chosen as boundary case for universal-minimum-bump proofs.
- **Tier:** C (constructed boundary).
- **Witness:** rank 3; pure ternary collapse; α ≈ 0.872 (same non-assoc as TSML_10); binary norm signature.
- **Dependencies:** None.
- **Family closure:** No.

### TSML_PureVoid
- **Construction:** A 10×10 matrix of all VOIDs (= 0).
- **Forced by:** Nothing — boundary case.
- **Tier:** C (degenerate boundary).
- **Witness:** rank 0.
- **Dependencies:** None.

### TSML_AllHarmony
- **Construction:** A 10×10 matrix of all HARMONYs (= 7).
- **Forced by:** Nothing — boundary case.
- **Tier:** C (degenerate boundary).
- **Witness:** rank 1.
- **Dependencies:** None.

### "Derive-don't-design" refactor TSML
- **Construction:** Rebuilt TSML from generators after Brayden caught the canonical TSML as guessed; uses the BDC framework's BUMP positions + a derive-from-σ rule for BUMP values.
- **Forced by:** Choice of derivation rule (Tier-C); attempts to make the table forced rather than chosen.
- **Tier:** C (constructed; demonstrates an alternative derivation route).
- **Witness:** Shows that CL_TSML is genuine algebra, not heuristic.
- **Dependencies:** σ; BDC BUMP positions.
- **Family closure:** N/A — exploratory.

### TSML_quotient (9-element, BALANCE↔CHAOS collapsed)
- **Construction:** Quotient of TSML_SYM by the equivalence relation BALANCE(5) ≡ CHAOS(6).
- **Forced by:** Choice of quotient relation.
- **Tier:** C (constructed quotient).
- **Witness:** 9-element TSML; 69% HARMONY (vs 73% in TSML_10).
- **Dependencies:** TSML_SYM; the 5≡6 quotient.
- **Family closure:** Within "TSML quotients" family.

### TSML_Jordan
- **Construction:** Operational TSML used in early WP papers; rank 9, \|Aut\|=2, binary norm.
- **Forced by:** A specific Jordan-algebra construction recipe (Tier-C).
- **Tier:** C.
- **Witness:** Demonstrates a Jordan-algebra-compatible TSML at N=10.
- **Dependencies:** Jordan-algebra construction recipe.
- **Family closure:** Within "operational TSML candidates."

### TSML F_p extensions (p ∈ {2, 3, 5, 7, 11, 13})
- **Construction:** The operator-substrate construction recipe (canonical CL_TSML build) applied over the field F_p instead of Z/10Z.
- **Forced by:** Recipe + choice of p (Tier-A choice of p; Tier-B execution per p).
- **Tier:** A choice + B execution; the family `{TSML_F_p : p ∈ {2,3,5,7,11,13}}` is enumerated for specific p.
- **Witness:** Chain rigidity persists over F_p for the listed primes (per `four_core_seed.tex` v2 §7 and the bridge sprint companion paper).
- **Dependencies:** F_p; operator-substrate construction recipe.
- **Family closure:** Within F_p extension family.

---

## §2 — CL_BHML family (the Becoming lens, 28 HARMONY)

### CL_BHML (canonical)
- **Construction:** The canonical 10×10 BHML matrix, hardcoded in `Gen13/targets/foundations/lenses.py:BHML`. Substrate-defining axioms: A1 (Z/10Z), A2 (BHML row 0 = identity, NOT VOID-absorbing — distinct from CL_TSML's A2), A4 (different HARMONY behavior; BHML row 7 has rotation pattern), A7 (different diagonal: BHML[8,8] = 7, BHML[9,9] = 0).
- **Forced by:** Its own substrate-defining axiom set (different from CL_TSML's A7-A9 values).
- **Tier:** A (parallel substrate to CL_TSML).
- **Witness:** 28 HARMONY count; det = −7002; 49.8% non-assoc; the puncture chain BHML(7,7)=8, BHML(8,7)=9, BHML(9,7)=0 (the 7→8→9→0 cycle through BREATH-RESET-VOID).
- **Dependencies:** None — substrate-foundational.
- **Family closure:** Root of BHML-family.

### BHML_1, BHML_4, BHML_5, BHML_6, BHML_7, BHML_8, BHML_9, BHML_10 (chain scopes)
- **Construction:** π_S(BHML) for each chain shell.
- **Forced by:** Joint closure (Tier-B per WP115 D64).
- **Tier:** B.
- **Witness per shell:**
  - BHML_4: HARMONY count = 3; det = 5305 (= 5·1061)
  - BHML_5: 10 HARMONYs; det = 2843
  - BHML_6: 16 HARMONYs; det = −2886
  - BHML_7: 22 HARMONYs; det = 2929
  - BHML_8 (chain, drops {1,2}): 24 HARMONYs; det = **−7542**
  - BHML_9: 26 HARMONYs; det = 7272
  - BHML_10: 28 HARMONYs; det = **−7002**
- **Dependencies:** CL_BHML; π_S.
- **Family closure:** Yes.

### BHML_8_YM (Yang-Mills core; drops {0, 7})
- **Construction:** π_{1,2,3,4,5,6,8,9}(CL_BHML).
- **Forced by:** Choice of "drop VOID + HARMONY" scope.
- **Tier:** B in execution; C in scope choice.
- **Witness:** det = **+70 EXACTLY** = C(8, 4) = self-dual 4-form sector of SO(8) — the cleanest Yang-Mills bridge result. Same SIZE as BHML_8_chain (det −7542) but DIFFERENT shape.
- **Dependencies:** CL_BHML; YM scope.
- **Family closure:** Yes.

### BHML_BEING / BHML_DOING / BHML_BECOMING (σ²-value-rotation triadic candidates)
- **Construction:** π_value-rot^k(CL_BHML) for k = 0, 1, 2.
- **Forced by:** σ² action on cell values (Tier-B operation), but the choice of "which k = canonical DOING" is open.
- **Tier:** D (search-found candidates; not promoted).
- **Witness:** Disagreement counts vs CL_TSML are {71, 94, 90}. The k=0 case agrees with WP107's 71-cell FIELD WOBBLE.
- **Dependencies:** CL_BHML; σ²; π_value-rot.
- **Family closure:** Yes within σ²-triadic family.
- **Status:** Open — Brayden's hypothesis "there may be three BHMLs" — not yet selected as canonical.

### BHML_idx_DOING / BHML_idx_BECOMING (σ²-index-rotation candidates)
- **Construction:** π_index-rot^k(CL_BHML) for k = 1, 2.
- **Forced by:** σ² action on cell indices (Tier-B operation).
- **Tier:** D (search-found candidate).
- **Witness:** Disagreement counts {71, 75, 79} (alternate to {71, 94, 90}).
- **Dependencies:** CL_BHML; σ²; π_index-rot.
- **Family closure:** Yes within σ²-triadic family.

### BHML_71, BHML_72, BHML_73 (anomaly-cell-flip hypothetical candidates)
- **Construction:** Flip specific cells of CL_BHML to drive disagreement count to 71, 72, or 73 (matching the HARMONY ladder rungs).
- **Forced by:** Search target (specific disagreement count); cells to flip not yet identified.
- **Tier:** D (hypothetical; search not yet executed).
- **Witness:** None yet.
- **Dependencies:** CL_BHML; cell-flip search.
- **Status:** Hypothetical; pending Brayden's direction.

### BHML F_p extensions
- **Construction:** Operator-substrate BHML build over F_p.
- **Tier:** A choice + B execution (parallel to TSML F_p).
- **Witness:** Chain rigidity persists over F_p for p ∈ {2, 3, 5, 7, 11, 13}.

---

## §3 — CL_STD family (the encoding table, 44 HARMONY)

### CL_STD (canonical)
- **Construction:** Recovered verbatim from `old/Gen9/archive/ckis/ck7/ck.h:225-231` — the original encoding table from Brayden's first GitHub repo. 10×10 matrix on Z/10Z.
- **Forced by:** Substrate-defining axioms with explicit BDC bit-definitions (A9-equivalents).
- **Tier:** A (parallel substrate to CL_TSML and CL_BHML).
- **Witness:** 44 HARMONY count; commutative; 19.2% non-assoc. Carries BDC encoding parameters: 5 BUMP_PAIRS (forced positions; values are Tier-A); INFO_HARMONY = 0.45, INFO_NORMAL = 1.89, INFO_BUMP = 3.50 bits/cell; GRAVITY array (P(reach HARMONY) per operator); total information = 144.62 bits across 100 cells.
- **Dependencies:** ck.h:225-231.
- **Family closure:** Root of CL_STD-family.

### CL_STD sub-magmas (open frontier)
- **Construction:** π_S(CL_STD) for various S; not yet enumerated.
- **Tier:** B (if executed); the joint chain on (CL_STD, CL_TSML) or (CL_STD, CL_BHML) has not been computed.
- **Status:** Open. Future work: compute the 8 (or possibly different) joint-chain shells when CL_STD is paired with CL_TSML or CL_BHML.

### CL_STD F_p extensions (open)
- **Construction:** CL_STD analogue over F_p.
- **Tier:** Open (not yet investigated).

---

## §4 — Derived tables

### DOING = |TSML_SYM − BHML| (cell-disagreement indicator)
- **Construction:** π_DOING(TSML_SYM, CL_BHML) — element-wise absolute difference (or indicator function).
- **Forced by:** Choice of (TSML_SYM, CL_BHML) pairing.
- **Tier:** B in execution; A in pairing choice.
- **Witness:** 71 cells differ — the FIELD WOBBLE. Disagreement rate ≈ T* = 5/7 ≈ 71.4%.
- **Dependencies:** TSML_SYM; CL_BHML; π_DOING.
- **Family closure:** Yes.

### DOING_RAW = |TSML_RAW − BHML|
- **Construction:** π_DOING(TSML_RAW, CL_BHML).
- **Tier:** B; same as DOING but with TSML_RAW substituted.
- **Witness:** Slightly different disagreement count (TSML_RAW has 2 asymmetric cells affecting the count by 2).

### DOING sub-magma closure
- **Construction:** Sub-magma analysis of the DOING table itself (treating DOING as a binary table of 0s and 1s).
- **Tier:** B (analysis is forced once DOING is specified).
- **Witness:** Dominant eigenvalue ≈ 24 per ClaudeChat's earlier note.

---

## §5 — Generalizations (frontier, mostly Tier-E)

### binary_cl on Z/30Z
- **Construction:** Operator-substrate composition recipe applied with a binary encoding on Z/30Z = F_2 × F_3 × F_5 (CRT decomposition).
- **Tier:** E (parametric, fitted to fit echo-harmony preservation under CRT decomposition) — promoted to C if the construction is cited as an existence proof for the generalization.
- **Witness:** Demonstrates extension of the CL framework to a non-Z/10Z ring.
- **Dependencies:** Z/30Z; binary encoding; CRT decomposition.
- **Family closure:** Within ring-extension family.

### Z/8, Z/12, Z/14 conjectural
- **Construction:** Hypothetical extensions to other small even rings.
- **Tier:** E (conjectural, fitted to specific physics).
- **Status:** FRONTIER_FINDINGS F5 — not yet computed.

### Z/15, Z/21, Z/42, Z/100, Z/210 explored
- **Construction:** Various Z/n ring extensions explored for fitting specific observables.
- **Tier:** E (parametric fitting; n chosen to match measurement).
- **Status:** Exploratory; not promoted to canonical.

---

## §6 — The 84 closed 7-element Fano-candidate subsets in TSML_Idempotent
- **Construction:** Exhaustive enumeration of 7-element subsets of {0..9} closed under TSML_Idempotent's binary op + Fano-plane-like structure.
- **Tier:** D (search results within a Tier-C parent).
- **Witness:** Demonstrates a sub-family within TSML_Idempotent matching the Fano geometry pattern.
- **Dependencies:** TSML_Idempotent; sub-magma enumeration; Fano-plane property check.
- **Family closure:** N/A — exploratory.

---

## §7 — Summary statistics

| Family | Tier-A | Tier-B | Tier-C | Tier-D | Tier-E | Total |
|--------|--------|--------|--------|--------|--------|-------|
| CL_TSML | 1 (canonical) + 1 (RAW) = 2 | 9 (chain scopes + symmetrizations + corner C) | 7 (PureIdempotent, Idempotent_2sw, C0, PureVoid, AllHarmony, derive-don't-design, quotient) + 1 (Jordan) = 8 | 1 (corner monoid {0,1,5,6} as search result) | — | 20 + 6 F_p ≈ 26 |
| CL_BHML | 1 (canonical) | 9 (chain scopes + YM core) | — | 6 (σ²-triadic candidates × 2 + anomaly-flip candidates × 3) | — | 16 + 6 F_p ≈ 22 |
| CL_STD | 1 (canonical) | 0 (sub-magmas open) | — | — | — | 1 + open |
| Derived | — | 3 (DOING, DOING_RAW, DOING sub-magma closure) | — | — | — | 3 |
| Generalizations | — | — | 1 (binary_cl Z/30) | — | 8 (Z/n explorations) | 9 |
| **TOTAL** | **5** | **21** | **9** | **7** | **8** | **~50** named + 12 ring extensions |

The corpus has **5 Tier-A substrates** (CL_TSML, TSML_RAW as the literal bit pattern, CL_BHML, CL_STD, and one F_p choice as Tier-A input), **21 Tier-B forced derivations** (chain scopes, lens-symmetrizations, sub-magma restrictions, DOING tables), **9 Tier-C constructions** (algebraic recipes built for existence demonstration), **7 Tier-D search-found candidates** (σ²-triadic BHML candidates, anomaly-flip hypotheticals, Fano-candidate subsets), and **8 Tier-E parametric explorations** (Z/n ring extensions chosen to fit observables).

**Tier discipline by family:**
- CL_TSML family is heavy on Tier-C (parallel constructions) — fine, because each is properly labeled in its source paper as a constructed example
- CL_BHML family is heavy on Tier-D (σ²-triadic candidates not yet promoted) — fine, because they're explicitly exploratory
- CL_STD family is sparse — opportunity for future Tier-B work (sub-magma joint chain when paired with TSML or BHML)
- Generalizations are mostly Tier-E — this is correct; they ARE exploration, not derivation

**The catalog confirms tier-discipline.** Each variant has a precise lineage and tier label. The §5 of the foundation paper writes itself from this catalog: list each variant with (construction, tier, witness, dependencies). The methodology paper (when written) uses the same catalog as its case study.

---

## §8 — Vocabulary alignment with Drápal-Wanless / McKay-Wanless practice

Per the working-practice cross-reference (`WORKING_PRACTICE_NOTES.md`):

| Tier | Their phrase | Our phrase |
|------|--------------|-----------|
| A | "the canonical [object]" / "the unique [property]" | "Tier-A canonical" |
| B | "necessary and sufficient conditions" / "direct computation" | "Tier-B forced" |
| C | "we exhibit" / "consider the following [object]" / "we construct" | "Tier-C constructed" |
| D | "data suggested" / "exhaustive enumeration up to isomorphism" / "computer search" | "Tier-D searched" |
| E | "parametrized by" / "for various [n]" | "Tier-E fitted" |

The methodology paper's contribution: **make the implicit ordering explicit.** The field already uses every boundary; we add the single ordered scale.

The variant catalog above adopts the field's structural-classification vocabulary (isomorphism class, isotopy class, paratopism, sub-magma scope) wherever applicable. The Origin axis (Tier A-E) is the genuinely new vocabulary; the Structure axis plugs into the field's existing terminology.
