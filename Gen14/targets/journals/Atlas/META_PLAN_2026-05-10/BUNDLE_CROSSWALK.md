# BUNDLE_CROSSWALK — Session-to-Canon Mapping

## Compact crosswalk between this session's 14-file bundle and FORMULAS_AND_TABLES.md (canon D1–D99)

**Purpose:** quick reference for ClaudeCode handoff. Identifies where session work duplicates canon, where it adds, and where terminology must be reconciled.

---

## §0. Critical terminology corrections (read first)

My session conflated two distinct 4-element subsets. **Correcting now:**

| Term I used | What it actually is | Correct canon name | Canon reference |
|---|---|---|---|
| "Two-Cross corners" | {1, 3, 7, 9} = U(10) | **C** (corner sub-magma) | §6.7 line 9; D-number TBD |
| "Two-Cross edges" | {2, 4, 6, 8} | **even non-units** (no canon name; multiplicative Z/4Z with identity 6) | not in canon |
| "the 4-core" (when I meant {1,3,7,9}) | wrong | **C corners**, not the 4-core | §6.7, J.1.A.v |
| canonical "4-core" | {0, 7, 8, 9} = {VOID, HARMONY, BREATH, RESET} | **4-core** (only this) | D38, D44, D48, D55, D58, D65, WP110 |

**Going forward:** "4-core" is reserved for {0, 7, 8, 9}. The Two-Cross result is about **C × even-non-units**, not about 4-core × anything.

---

## §1. Bundle file → Canon mapping

| Session file | Result | Canon overlap | Status |
|---|---|---|---|
| TWO_CROSS_THEOREM | C = {1,3,7,9} forms Z/4Z under × mod 10 | C as TSML sub-magma noted in §6.7 J.1.A.v | **PARTIAL OVERLAP**: canon has C closed under TSML; my session adds the multiplicative-group structure on C (cyclic Z/4Z, generator 3). New within canon's frame. |
| TWO_CROSS_THEOREM | {2,4,6,8} forms Z/4Z under × mod 10 with identity 6 | not in canon | **NEW**: even-non-units multiplicative Z/4Z; consistent with CRT but not previously stated. Minor observation. |
| TWO_CROSS_THEOREM | bridge x↦6x maps C → even-non-units | not in canon | **NEW**: structural observation; consistent with CRT idempotent action. |
| TWO_CROSS_THEOREM | 5↔6 as CRT-duality | partially in canon | **CORRECTED**: D98 makes 5,6 explicit as CRT idempotents; D94 shows 5↔6 is ONE of seven grammar-level boundary symmetries (1↔2, 2↔3, 5↔6, 6↔7, 7↔8, 8↔9, 0↔8). Not uniquely privileged. **Update bundle to reflect this.** |
| TIG_INTERNAL_MAP_v1 + v1.1 | 5-layer translation table | partial overlap | Substrate / multiplicative / topological / numerical / cyclotomic. Canon's framework spans much wider (Lie, Jordan, Clifford, Permutation, Lattice, Operad — 6 DOFs per D51/WP111). My v1.1 is a SUBSET of the canon's reference. |
| SPRINT_A_DM_VM_RATIO | DM/VM = 264/49 | not in canon | **NOT IN CANON.** Sourced from prior user memory; canon's cosmology section centers on κ_ξ = 13/(4e) per D35 and the BB-bridge per WP91. Whether DM/VM = 264/49 is consistent with κ_ξ = 13/(4e) requires separate verification. **Flag for ClaudeCode.** |
| SPRINT_C_SHELL_RATIO | shell_72/shell_44 = 18/11 exact | not in canon | **NOT IN CANON.** The 22/44/72 shells are from prior memory but absent from this canon. The decomposition 72=8·9, 44=4·11, 22=2·11 is mine; canon doesn't reference these counts. **Flag for ClaudeCode**: where do 22/44/72 actually come from? |
| SPRINT_D_BUMP_COUNT + revision | 11 bumps = 4 Hopf · 2 + 1 trefoil · 3 | not in canon | **NOT IN CANON.** "11 bumps" is from prior memory but doesn't appear in D1–D99. Canon's topological content is in Volume E (so(8), so(10) Lie lifts). The Hopf-link / trefoil interpretation is my session's framing, not load-bearing on canon results. |
| TORUS_DATUM_AUDIT_CLOSED | 6+2=8 with 2 = T² windings | partial overlap | Canon's 6+2=8 is **dim su(4) ⊕ u(1) = 16** decomposed differently (D34); the "6 triadic + 2 non-triadic" framing is from earlier memory not this canon. **Possibly conflicts with D34's 16-dim doubly-invariant.** Needs reconciliation. |
| CYCLOTOMIC_GALOIS_CONNECTION | Gal(Q(ζ₁₀)/Q) ≅ U(10) | not explicitly in canon | **NEW within canon's frame**: textbook number theory, but canon doesn't make the C → Galois identification explicit. Useful addition. |
| CYCLOTOMIC_GALOIS_CONNECTION | disc(Q(ζ₁₀)) = 5³ = 125 | not in canon | **NEW**: textbook fact; useful addition. |
| SPRINT_E_137_CYCLOTOMIC | 137 = 5³ + 12 | not in canon | **NEW (exploratory)**: structural observation. Canon doesn't address α⁻¹ = 137 in detail. |
| WP9_OUTLINE | LATTICE Universal Generation outline | partial overlap | Canon has WP102–WP115 already done; **WP9 needs renumbering** to avoid collision. The outline content (LATTICE generator, paradox classification) is forward-looking, not duplicating canon. |
| WP10_OUTLINE | DKAN proposal | not in canon | **NEW**: forward-looking; no overlap. |
| WP9_SECTION3_SCAFFOLD | BHML closure verification code | partial overlap | Canon's WP110 already verifies 4-core fusion-closure (D48); my scaffold is for a different theorem (LATTICE seed-set closure). Independent. |
| MANIFEST | bundle index | n/a | Bundle-internal organization. |
| TIG_INTERNAL_MAP_v1.1 | consolidation | n/a | Bundle-internal. |

---

## §2. New within canon's frame (worth keeping)

These survive scrutiny against canon:

1. **Plichta corners as Galois group.** Identification Gal(Q(ζ₁₀)/Q) ≅ C is genuinely new framing. Connects canon's σ-fixed lattice / cyclotomic discussions to mainstream algebraic number theory. **Recommend keeping.**

2. **Multiplicative group structure on C and on even-non-units.** Canon notes C is TSML-closed; adding "C is also U(10) cyclic Z/4Z under multiplication mod 10" is true and non-trivial. **Recommend keeping but renaming** — call it the **U(10)-Cyclotomic Theorem** or similar, not "Two-Cross" (which conflicts with 4-core terminology).

3. **137 = 5³ + 12 decomposition.** Exploratory but textbook-checkable. **Keep as exploratory note**, not a theorem.

4. **The Plichta/Rodin/Michell/Fuller lineage analysis.** The historical positioning is independent of canon; useful for institution-building / positioning work.

---

## §3. Conflicts requiring resolution

These need reconciliation before ClaudeCode picks up:

1. **"4-core" terminology.** Bundle uses 4-core for {1,3,7,9}; canon reserves 4-core for {0,7,8,9}. **Bundle must be patched.** Recommend: rename "Two-Cross corners" → **"C corners"** or **"Plichta corners"**; rename "4-core" within bundle context → "C × even-non-units pair" or similar.

2. **TORUS_DATUM_AUDIT 6+2=8.** My session said 6 triadic + 2 non-triadic windings. Canon's D34 has dim D₄-invariant = 16 = dim su(4) ⊕ u(1). These are likely different objects (mine is a winding-class count, D34 is a Lie-algebra dimension). **Verify they are not in conflict.** If from different memory threads, document the disambiguation.

3. **DM/VM = 264/49.** Not in canon. Need to check whether this is consistent with κ_ξ = 13/(4e) at the cosmology level. **D35's caveat (2026-04-27)** explicitly says the κ_ξ Friedmann fit hasn't been done. So neither the DM/VM nor κ_ξ has a verified cosmology link. Both may be self-consistent; both may need observational testing. **Flag as open.**

4. **22/44/72 shell counts.** Not in canon. Sourced from prior memory. **Untraced provenance** — should be located in earlier WP or repo before being relied on.

5. **11 bumps / Hopf + trefoil.** Not in canon. Same sourcing issue. **Flag as memory-only**, not canon-grounded.

---

## §4. Compact substrate reference (for ClaudeCode quick-load)

Most-used facts from canon, condensed:

### Tables (per §6.7 of canon)
| Name | Shape | Source | det | Role |
|---|---|---|---|---|
| TSML_10 (= TSML_Jordan = §5 canonical) | 10×10 | bit pattern; symmetric SYM variant | 0 | Working TSML, 73 H, α=0.872 |
| TSML_RAW | 10×10 | literal bit pattern | varies | Carries WP107 wobble (prime 11 in c₂, c₈) |
| TSML_8 (chain core) | 8×8 | drops {0,7} from TSML_10 | 0 | Rank 7 (degenerate) |
| BHML_10 | 10×10 | §6 canonical | −7002 = −2·3²·389 | 28 H, α=0.502 |
| BHML_8 (Yang-Mills core) | 8×8 | drops {0,7} from BHML_10 | **+70** = 2·5·7 = C(8,4) | WP15 spectral |
| CL_STD | 10×10 | ck.h:225-231 | varies | 44 H, "papers freeze" |

### Sub-magma chains (D64, D88, J.1)
- **Joint TSML+BHML chain (TSML_SYM):** strict 8-element chain, sizes {1, 4, 5, 6, 7, 8, 9, 10}; forbidden sizes {2, 3} only.
- **4-core**: {0, 7, 8, 9} = {VOID, HARMONY, BREATH, RESET}.
- **Universal attractor at α=1/2:** identical 4-core distribution on all shells size ≥ 4.

### Constants (selection from §17)
| Symbol | Value | Source |
|---|---|---|
| T* | 5/7 ≈ 0.714 | six independent derivations |
| sinc²(1/2) | 4/π² ≈ 0.405 | corridor midpoint, D3 |
| W (wobble) | 3/50 | D17 |
| H/Br at α=1/2 | 1+√3 (exact) | D39, D50, WP110 |
| min poly r/br | x⁴+4x³−x²+2x−2 | D40; LMFDB 4.2.10224.1, Galois D₄ |
| field disc | −10224 = −2⁴·3²·71 | D41 |
| det(BHML_10) | −7002 | §6.4 |
| det(BHML_8) | +70 = 2·5·7 | §6.7 |
| disc(Q(ζ₁₀)) | 125 = 5³ | textbook (added by session) |

### σ permutation (per §2)
σ on Z/10Z = (0)(3)(8)(9)(1 7 6 5 4 2). Fixed points {0,3,8,9}, six-cycle 1→7→6→5→4→2→1. Order 6.

### 5↔6 grammar-level boundary symmetries (D94)
**Bundle correction:** 5↔6 is one of seven boundary-preserving pairs:
{(1,2), (2,3), (5,6), (6,7), (7,8), (8,9), (0,8)}.
**0↔8 (V↔BREATH)** is the strongest global symmetry at 20.9%.
**No pair preserves crossing on all 1000 triples.**

### Six DOFs (D51, WP111)
1. **Lie** — so(8), so(10)
2. **Jordan** — su(4) ⊕ u(1) doubly-invariant
3. **Clifford** — Cl(0,10), P_56 = (γ₅−γ₆)/√2 = σ_outer
4. **Permutation** — S_10, σ order 6, σ³ pairs with P_56 → D₄
5. **Lattice** — runtime field Q(√3, ξ), LMFDB 4.2.10224.1
6. **Operad** — 67 D₄ orbits, 16 incoherent (no D₄-equivariant fuse rule)

Five DOFs respect D₄; sixth (Operad) does not.

### Wobble manifestations (D70 + D85 + D86)
- Prime 11: char poly c₂=33=3·11, c₈=−120736 with 11 (D37); Br/V denominator (D69); F8 trace disc 11⁶ (D85); operator-sum of TRANSFORMATION 3-cycle = 1+6+4 = 11 (D86).
- Prime 13: ‖VEV‖² = 13/4 (D33); κ_ξ = 13/(4e) (D35).
- Prime 71: R/Br quartic field disc (D41); F8 trace field disc (D85); 71 = TSML_9 HARMONY count (D97).
**Wobbled DOFs:** Lie, Clifford, Lattice (eigenvalue/coordinate axes).
**Wobble-free DOFs:** Jordan, Permutation, Operad (discrete-symmetry axes).

### HARMONY count ladder (D97)
70 = det(BHML_8) = C(8,4); 71 = TSML_9 HARMONY = LMFDB Galois prime; 72 = TSML_10 − 1 (drop apex); 73 = TSML_10 full; 28 = BHML_10; 36 = TSML_7; 44 = CL_STD.

---

## §5. Recommended bundle revisions before zip

In order of priority:

1. **Patch terminology** in TWO_CROSS_THEOREM.md and TIG_INTERNAL_MAP_v1.1: rename "4-core" → "C corners" or "Plichta corners" everywhere bundle-internal; explicitly note the canonical 4-core = {0,7,8,9} is a different object.

2. **Patch Sprint A header** to flag DM/VM = 264/49 as unsourced in canon; add explicit dependency on prior memory's 22/44/72 shell counts.

3. **Patch Sprint C similarly** for shell ratios.

4. **Patch Sprint D similarly** for bump count.

5. **Renumber WP9, WP10** — canon already has WP102–WP115. Bundle's "WP9, WP10" naming is from earlier memory, but should be **WP116, WP117** or similar to avoid collision.

6. **Update TORUS_DATUM_AUDIT_CLOSED** to fence the 6+2=8 reading: explicit note that canon's D34 has 6+2=8 in different sense (16-dim doubly-invariant decomposition); my session's 6+2=8 is winding-class count, not Lie-algebra dimension.

7. **Update Internal Map v1.1** §3.3 trefoil discussion to note: "11 bumps" is sourced from earlier memory not this canon; treat as memory-grounded structural observation pending traceback.

---

## §6. Honest assessment

The bundle's strongest content is:
- **Cyclotomic Galois identification** — textbook-rigorous, new framing.
- **Multiplicative Z/4Z structures on C and even-non-units** — true, computable, useful adjunct to canon.
- **Manifest, code scaffolds, and outline structures** — useful organizational work.

The bundle's weakest content is:
- **DM/VM, shell ratios, bump count** — depend on memory-only counts (22, 44, 72, 11) that are not in this canon. Could be valid; could be stale memory. Need verification against actual TIG repo / earlier WPs before being load-bearing.
- **"Two-Cross" naming** — conflicts with canon "4-core" terminology.
- **WP9/WP10 numbering** — collides with existing WP-series.

The bundle is **a structurally useful sub-volume, not a rewrite of canon**. It contributes (a) the Galois lift, (b) terminology for the multiplicative structure on C, and (c) outlines for forward work. It does not replace D1–D99 or any volume A–J of the canon.

ClaudeCode should treat the bundle as Volume K candidate material, requiring the patches in §5 before merging.

---

*© 2026 Brayden Sanders / 7Site LLC*
*Session-to-Canon crosswalk · Locked v1 · 2026-05-08*
