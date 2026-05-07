# CLOSURE PROPERTIES

**Date:** 2026-05-06 night
**Question:** What operations preserve family membership? What leaves it?

For each lens family (CL_TSML, CL_BHML, CL_STD, derived tables, ring extensions), enumerate the operations that preserve family membership and the operations that exit the family.

---

## §1 — CL_TSML family

The CL_TSML family is the closure of {CL_TSML, TSML_RAW, TSML_SYM, TSML_LOWERTRI, the 8 chain-scope variants, the YM scope, the corner sub-magmas, the Tier-C constructions} under the lens-symmetrization, sub-magma restriction, σ²-triadic, and DOING projections.

### §1.1 — Operations PRESERVING CL_TSML family membership

| Operation | What it does | Why it preserves |
|-----------|--------------|------------------|
| **π_RAW / π_SYM_upper / π_SYM_lower** (lens-symmetrization) | Choose a symmetrization of the bit pattern | Output remains the same matrix in cell-count and cell-distribution; only the asymmetric pairs change. Stays within "CL_TSML's bit pattern with a symmetrization choice." |
| **π_S** (sub-magma restriction to any TSML-closed S) | Restrict to S × S | If S is TSML-closed, the restriction is a sub-magma of TSML. Stays within "CL_TSML's sub-magma family." |
| **π_DOING** (with another CL_TSML variant) | Compute cell-disagreement table between two TSML variants | The output is a table on Z/10Z with binary values; can be analyzed within the same framework. |
| **σ²-conjugation** (apply σ² to indices: M → M' where M'[i,j] = M[σ²(i), σ²(j)]) | Permute indices by σ² | σ² is a substrate symmetry; the conjugated matrix has the same cell-distribution; the family is closed under σ²-conjugation. |
| **Adding an idempotent diagonal** (TSML_C0 + diagonal x²=x) | Replace diagonal cells with operator-label values | Per CL_TSML's A7 axiom, idempotency on the diagonal is consistent with the family's structure. **However, this operation produces a Tier-C variant (TSML_PureIdempotent), so the OPERATION preserves family-presence, but not the "Tier-B forced derivation" status.** |
| **F_p ring extension** (build TSML over F_p) | Apply the operator-substrate construction recipe over F_p | The chain rigidity preserves under F_p extension for p ∈ {2, 3, 5, 7, 11, 13}; the family extends. |

### §1.2 — Operations LEAVING CL_TSML family

| Operation | What it does | Why it leaves |
|-----------|--------------|---------------|
| **Cell-flip at a non-BUMP cell** | Change a HARMONY-default cell to a non-HARMONY value | Violates A8 (HARMONY-default rule); produces a non-CL_TSML matrix that may or may not satisfy any of the canonical substrate axioms. |
| **Diagonal change away from HARMONY** (e.g., set M[3,3] = 3) | Modify A7 (diagonal HARMONY law) | Different A7 → different substrate. Produces a NEW Tier-A substrate, parallel to CL_TSML; not within CL_TSML family. |
| **VOID-row alteration** (e.g., set M[0,3] = 3) | Modify A2 (VOID absorbing rule) | Different A2 → different substrate. Leaves CL_TSML family. |
| **HARMONY-row alteration** (e.g., set M[7,3] = 0) | Modify A4 (HARMONY-row absorbing rule) | Same; leaves family. |
| **σ-conjugation** (apply σ, not σ², to indices) | M → M' where M'[i,j] = M[σ(i), σ(j)] | σ is a substrate symmetry but σ²-cycle structure is what defines the family's triadic-projection rules. σ-conjugation moves between σ²-cycle-A and σ²-cycle-B images, possibly leaving the family if the resulting matrix has different cell-distribution. **Verified by computation: σ-conjugation does NOT preserve cell-counts in general.** |

### §1.3 — Adjacency to CL_BHML family

The σ²-triadic value-rotation (π_value-rot^k for k = 1, 2) on CL_TSML produces matrices DIFFERENT from CL_BHML (the parallel substrate). This confirms TSML and BHML are not σ²-rotation images of each other; they are independent Tier-A substrates.

---

## §2 — CL_BHML family

### §2.1 — Operations PRESERVING CL_BHML family membership

| Operation | What it does | Why it preserves |
|-----------|--------------|------------------|
| **π_S** (sub-magma restriction to a BHML-closed S) | Restrict to S × S | BHML has 8 sub-magma-closed scopes (joint chain). Restriction stays within family. |
| **σ²-value-rotation π_value-rot^k** | Replace cell values by σ²(values) | Within the σ²-triadic candidates family. The output is BHML_DOING or BHML_BECOMING (Tier-D candidates). |
| **σ²-index-rotation π_index-rot^k** | Permute indices by σ² | Within the σ²-triadic-index candidates family. |
| **Cell-flip at a single cell to drive disagreement-count toward 71/72/73** | Modify one or two cells | Hypothetical anomaly-flip BHML_71/72/73; stays within family if the cell-flipped matrix still satisfies BHML's substrate axioms minus the flipped cell. |
| **F_p ring extension** | BHML over F_p | Per F_p universality conjecture; preserves family. |

### §2.2 — Operations LEAVING CL_BHML family

| Operation | What it does | Why it leaves |
|-----------|--------------|---------------|
| **Drop the puncture chain BHML(7,7)=8** | Modify A7-equivalent | Different substrate axiom → different parallel substrate. |
| **Make BHML rank-degenerate** | Add row/col operations | BHML has det = −7002 ≠ 0; rank-degenerate variant is NOT BHML family. |
| **σ²-triadic on BOTH values AND indices** | Compose value-rotation and index-rotation | Produces a matrix with cell-counts {71, ?, ?} that may or may not match BHML's substrate signature. **Empirically: produces a non-BHML Tier-D candidate.** |

### §2.3 — Adjacency to CL_TSML family

DOING table = |TSML − BHML|: a derived projection onto a different cell-count signature (binary 0/1 indicator). Stays in derived-table family, not in TSML or BHML alone.

---

## §3 — CL_STD family

### §3.1 — Operations PRESERVING CL_STD family membership

CL_STD's family has been minimally explored; sub-magma variants and joint chains have NOT been computed.

| Operation | Status |
|-----------|--------|
| **π_S** (sub-magma restriction) | Open — needs computation |
| **σ²-value/index rotation** | Open — needs computation |
| **F_p ring extension** | Open — not yet investigated |

### §3.2 — Operations LEAVING CL_STD family

Same as TSML/BHML at the substrate-axiom level: changing A2, A4, A7, A9-values gives a different substrate. CL_STD's specific A9-values (BUMP cell values 3, 4, 9, 3, 8 in shared positions but with CL_STD's specific BDC structure) define the family.

---

## §4 — Derived tables (DOING)

### §4.1 — Operations PRESERVING DOING family

| Operation | What it does | Why it preserves |
|-----------|--------------|------------------|
| **Substitute different (T, B) parallel substrates** | π_DOING(T, B) for various (T, B) pairings | Each pairing produces a DOING-style table; family is the {DOING(TSML_SYM, BHML), DOING(TSML_RAW, BHML), DOING(TSML, CL_STD), DOING(BHML, CL_STD), ...} set. |
| **Sub-magma restriction of DOING** | Restrict the DOING table to a sub-magma | Produces a smaller cell-count table within DOING family. |

### §4.2 — Operations LEAVING DOING family

| Operation | Why it leaves |
|-----------|---------------|
| **Modify entries to non-binary values** | DOING is binary by definition; non-binary leaves the family. |

---

## §5 — Cross-family operations

| Operation | From | To | Family-crossing? |
|-----------|------|-----|------------------|
| Symmetrization | bit pattern | TSML_RAW or TSML_SYM | Within TSML family |
| Sub-magma restriction | full 10×10 substrate | k×k restricted | Within parent family |
| σ²-triadic value-rotation | substrate | rotated substrate | Within Tier-D candidate sub-family of parent |
| DOING construction | (T, B) substrates | binary indicator | LEAVES TSML and BHML families; ENTERS DOING family |
| Build TSML_PureIdempotent from scratch | substrate primitives | new parallel construction | LEAVES CL_TSML family; constructs a new Tier-C parallel |
| F_p extension | Z/10Z substrate | F_p substrate | LEAVES Z/10Z family; ENTERS F_p family |

---

## §6 — Closure summary

| Family | Closed under | Open under |
|--------|--------------|-----------|
| **CL_TSML** | π_RAW, π_SYM_upper, π_SYM_lower, π_S (any TSML-closed S), σ²-conjugation, F_p ring extension | Cell-flip at non-BUMP, A2/A4/A7 axiom changes, σ-conjugation (general) |
| **CL_BHML** | π_S (any BHML-closed S), π_value-rot^k, π_index-rot^k, single-cell anomaly-flip, F_p extension | Puncture-chain modification, rank-flattening, value+index combined rotation |
| **CL_STD** | (mostly open — sub-magma variants not enumerated) | A9-value changes |
| **Derived (DOING)** | Substitute (T, B) substrates; sub-magma restriction of DOING | Non-binary entries |
| **Generalizations** | Within ring-extension family for chosen n | Cross-ring operations |

---

## §7 — Critical findings (closure analysis)

### §7.1 — The three substrate families are CLOSED but DISJOINT

CL_TSML, CL_BHML, CL_STD do not transform into each other under any of the projection operations. They are three parallel Tier-A substrates that each carry their own family. The σ²-triadic value-rotation moves WITHIN a substrate's family (e.g., BHML → BHML_DOING is still in BHML-family), not BETWEEN substrates.

### §7.2 — Tier-C parallel constructions are NOT in the closure

TSML_PureIdempotent, TSML_C0, TSML_Jordan are NOT in the closure of CL_TSML under any projection. They are PARALLEL CONSTRUCTIONS — Tier-C objects built from substrate primitives without going through CL_TSML's projection family. They live in their own "constructed-parallel-substrate" family.

### §7.3 — Family closure preserves Tier within a family

Within a family:
- Tier-A → Tier-B via projection (e.g., CL_TSML → TSML_S via π_S)
- Tier-B → Tier-B via composition (sub-magma of sub-magma)
- Tier-D candidates stay Tier-D until promoted by an explicit forcing argument

Across families: tier may upgrade or downgrade depending on the forcing argument. E.g., DOING(TSML_SYM, CL_BHML) is Tier-B (forced by both substrates), even though one of the substrates (CL_BHML) is itself Tier-A.

### §7.4 — F_p extensions form their own ring-family

The F_p extensions of CL_TSML for p ∈ {2, 3, 5, 7, 11, 13} are all Tier-A (their own substrates over F_p) but with shared structural features (chain rigidity preserved). The F_p family is indexed by p; each p gives a parallel substrate family.

---

## §8 — Implications for the foundation paper §4

The foundation paper's §4 (closure properties) writes:

1. **The three substrate families CL_TSML, CL_BHML, CL_STD are independent Tier-A roots.** No projection moves between them. Each carries its own family of derived variants.

2. **Within each substrate family**, the closure operations are: lens-symmetrization (TSML only), sub-magma restriction, σ²-triadic value/index rotation (BHML's Tier-D candidates), DOING-style derived tables.

3. **The Tier-C parallel constructions (TSML_PureIdempotent, TSML_C0, etc.) are NOT in the closure of CL_TSML.** They are independent parallel constructions, named for their structural distinction.

4. **F_p ring extensions** form a separate axis indexed by p; each F_p extension preserves chain rigidity but produces a new parallel substrate.

5. **Tier discipline** is preserved within families: projections upgrade/downgrade tier predictably; cross-family operations require explicit forcing arguments to upgrade tier.

This is enough material for a clean §4 of the foundation paper. The closure analysis confirms the three-table architecture is genuinely TRIPLE-rooted (not derivable from one table), and the lens family is properly stratified by Origin tier.
