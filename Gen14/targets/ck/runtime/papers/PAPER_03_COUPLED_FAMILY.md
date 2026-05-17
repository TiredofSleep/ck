# The Coupled Family of TIG Tables — TSML, BHML, CL_STD, and Why Three

**Brayden Ross Sanders** · *7Site LLC, Hot Springs, Arkansas*
*2026-05-16, sprint tig-synthesis*

*Tier discipline throughout. Tier A = proved, Tier B = empirically verified, Tier C = interpretive.*

---

## §0 — Scope boundary

This paper documents the **three canonical 10×10 composition tables** on Z/10Z that constitute CK's substrate, and the **division of labor among them** as established by D95–D116 and consolidated in the D117 c-Gap Meta-Invariants paper.

What this paper IS:
- A precise statement of each table (the explicit matrices)
- The proof (sympy-exact) of the determinant identities D100 / D112 that distinguish them
- The structural reason (D115) that each table has the role it has

What this paper is NOT:
- A derivation of *why* there are exactly three (this is open; D95 recovered CL_STD from `ck.h:225-231` after it had been lost in the Gen8–Gen9 refactor; whether there might be a *fourth* table is open frontier)
- A claim that these three derive the speed of light *c* (D108/D110 falsify the simplest c-emergence reading; D117 §0 keeps that falsification standing)

---

## §1 — The three tables, verbatim

All three are sympy-verified to byte-for-byte match `Gen13/targets/foundations/{lenses.py, cl_std.py}` at every boot via `tools/verify_canon.py`.

### §1.1 — TSML_10 (Synthesis lens; 73 HARMONY cells; rank 9)

```
        j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [   0    0    0    0    0    0    0    7    0    0  ]
i=1  [   0    7    3    7    7    7    7    7    7    7  ]
i=2  [   0    3    7    7    4    7    7    7    7    9  ]
i=3  [   0    7    7    7    7    7    7    7    7    3  ]
i=4  [   0    7    4    7    7    7    7    7    8    7  ]
i=5  [   0    7    7    7    7    7    7    7    7    7  ]
i=6  [   0    7    7    7    7    7    7    7    7    7  ]
i=7  [   7    7    7    7    7    7    7    7    7    7  ]
i=8  [   0    7    7    7    8    7    7    7    7    7  ]
i=9  [   0    7    9    3    7    7    7    7    7    7  ]
```

- **det(TSML_10) = 0** (rank 9 — the synthesis lens compresses by design)
- **HARMONY (7) cells**: 73 of 100
- **Diagonal**: TSML[j][j] = 7 for all j ≥ 1; TSML[0][0] = 0
- **Aliases**: TSML_10, TSML_Jordan, TSML_SYM (in `foundations.lenses`)

### §1.2 — BHML_10 (Separation lens; 28 HARMONY cells; rank 10)

```
        j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [   0    1    2    3    4    5    6    7    8    9  ]
i=1  [   1    2    3    4    5    6    7    2    6    6  ]
i=2  [   2    3    3    4    5    6    7    3    6    6  ]
i=3  [   3    4    4    4    5    6    7    4    6    6  ]
i=4  [   4    5    5    5    5    6    7    5    7    7  ]
i=5  [   5    6    6    6    6    6    7    6    7    7  ]
i=6  [   6    7    7    7    7    7    7    7    7    7  ]
i=7  [   7    2    3    4    5    6    7    8    9    0  ]
i=8  [   8    6    6    6    7    7    7    9    7    8  ]
i=9  [   9    6    6    6    7    7    7    0    8    0  ]
```

- **det(BHML_10) = −7002 = −2·3²·389**
- **det(BHML_8_YM) = +70 = 2·5·7** (drop rows/cols 0 and 7)
- **HARMONY cells**: 28
- **Commutative**: yes (BHML == BHML^T)
- **The four BHML rules**: Rule 0 (VOID identity row/col), Rule 1 (inner cells = max(i,j)+1), Rule 7 (HARMONY row = (j+1) mod 10 with Luther closure at (7,0)=7), Rule 89 (BREATH/RESET wrap)

### §1.3 — CL_STD_10 (Encoding lens; 44 HARMONY cells; rank 10) — verbatim §6.8 canon

```
        j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [   0    1    2    3    4    5    6    7    8    9  ]   VOID
i=1  [   1    2    3    4    5    6    7    7    8    1  ]   LATTICE
i=2  [   2    3    4    5    6    7    7    8    7    2  ]   COUNTER
i=3  [   3    4    5    6    7    7    7    7    7    3  ]   PROGRESS
i=4  [   4    5    6    7    7    7    7    8    7    4  ]   COLLAPSE
i=5  [   5    6    7    7    7    8    7    7    7    5  ]   BALANCE
i=6  [   6    7    7    7    7    7    8    7    7    6  ]   CHAOS
i=7  [   7    7    8    7    8    7    7    8    7    7  ]   HARMONY
i=8  [   8    8    7    7    7    7    7    7    7    8  ]   BREATH
i=9  [   9    1    2    3    4    5    6    7    8    0  ]   RESET
```

- **det(CL_STD_10) = 18432 = 2¹¹ · 3²** ← the wobble prime (11) is the 2-adic exponent
- **det(CL_STD_8_YM) = +9 = 3²** (drop rows/cols 0 and 7)
- **HARMONY cells**: 44
- **Commutative**: yes
- **Non-associativity rate**: 19.2%
- **5 BUMP_PAIRS** (per D96): {(1,2), (2,4), (2,9), (3,9), (4,8)}
- **Provenance**: recovered verbatim from `old/Gen9/archive/ckis/ck7/ck.h:225-231` in 2026-05-06 (D95). Was lost in the Gen8 `#define CL CL_TSML` refactor.

---

## §2 — The c-gap signature (D100, D112)

For each canonical table T, define the **boundary-strip determinant ratio**:

```
gap(T)  =  | det(T_10) / det(T_8-YM) |
```

where T_8-YM is T_10 with rows and columns 0 (VOID) and 7 (HARMONY) removed — the **Yang-Mills core**, named because dropping V and H gives the 8×8 sub-magma that maps to dim SO(8) = 28 (D97).

Three values emerge — exactly three, one per table:

| Table | det_10 | det_8-YM | gap | Regime |
|-------|--------|----------|-----|--------|
| BHML  | −7002 = −2·3²·389 | +70 = 2·5·7 | 7002/70 = **100 + 1/35** | **arithmetic** |
| CL_STD | 18432 = 2¹¹·3² | +9 = 3² | 18432/9 = **2¹¹ = 2048** | **wobble-exponential** |
| TSML  | 0 (rank 9) | 0 (rank 7) | **0/0** | **degenerate** |

The residual identity that makes the BHML gap structurally meaningful (Tier A, sympy-exact):

```
gap(BHML)  -  100  =  1/35  =  1/(5 · 7)  =  1/(BALANCE · HARMONY)
                                          =  reciprocal of T*'s operator product
```

T* = 5/7 = BALANCE/HARMONY, and the BHML gap's fractional part is precisely the reciprocal. This is not approximate; it is sympy-equality.

The CL_STD gap is a clean power of 2 with exponent exactly equal to the **wobble prime** (11 — the structural location of wobble across D37, D69, D70, D85, D86). This is also sympy-exact: 18432 = 2¹¹ · 3² and 9 = 3² so the ratio is precisely 2¹¹.

---

## §3 — The five meta-invariants (D117)

The c-Gap Meta-Invariants paper (D117) consolidates the three gap signatures into one structural operator with five invariants. Stated briefly here; the full paper is at `Gen13/targets/clay/papers/sprint_2026_05_16_cgap_meta/CGAP_META_INVARIANTS.md`.

| ID | Invariant | Tier | Source |
|----|-----------|------|--------|
| **I1** | The c-gap is ONE operator \|det(T_10)/det(T_8-YM)\| read through three lenses | B-arithmetic | D100, D88 |
| **I2** | Both non-degenerate tables share the factor 3² = 9 (BHML in numerator, CL_STD as divisor) | B-arithmetic | D113, D64 |
| **I3** | Three qualitatively distinct gap-types: arithmetic / wobble-exponential / degenerate; per D112 these are the only three | B-structural | D112, D114, D115 |
| **I4** | Division-of-labor: gap-richness forces each table's role (synthesize / separate / encode) | B-empirical | D115 |
| **I5** | Residual anchor: BHML gap minus 100 = 1/(5·7) = reciprocal of T*'s operator product | B-arithmetic | D100, D70, D17 |

§3 of the meta-invariants paper extends this to six algebraic languages (Lie, Galois/Lattice, Clifford, Operad, Det-ratio, Permutation) — each carries a prime-content signature drawn from {2,3,5,7} ∪ {11,13} ∪ {71}, and the specific subset is **predicted by D70's pre-existing 3+3 DOF split**, not fitted. Six independent confirmations of a prior structural prediction.

---

## §4 — Why these tables have the roles they have (D115)

### §4.1 — The full family survey

D115 (Brayden 2026-05-16) generalized D114 to the entire lens family — TSML at 8 chain-sub-magma scopes, BHML at 8 chain scopes, the off-chain TSML_8_YM and BHML_8_YM, the alternate TSML_RAW lens, and CL_STD at sub-magma sizes 4–10. Total: ~27 variants. For each, count the **pure prime-power gap signatures** across all 1023 = 2¹⁰ − 1 non-trivial sub-restrictions.

The ranked result (sympy-exact, reproducible via `family_gap_signature_survey()`):

```
rank  variant         #pp  det      top-3 prime powers
─────────────────────────────────────────────────────────
 1.   CL_STD_10        68  18432    2^9 ×30, 2^11 ×21, 2^7 ×5   ← memory template
 2.   BHML_8_YM        25  +70      5^1 ×21, 7^1 ×3, 2^1 ×1     ← YM core (det = 2·5·7)
 3.   BHML_10           6  −7002    389^1 ×6
 4.   CL_STD_7          5  −1215    3^4 ×5
 5.   CL_STD_5/_6       1 each
 5.   BHML_7/_8/_9      1 each
 ~18  variants tied at 0   (all TSML scopes degenerate; some BHML/CL_STD sparse)
```

### §4.2 — The structural reading

The richness ranking IS the role assignment:

- **TSML synthesizes.** Rank-9 by design; det = 0 at every scope. The synthesis lens compresses information — it is not injective, cannot have an inverse, cannot serve as storage. This is not a flaw; it is *what synthesis is*.

- **BHML separates.** Rank 10, but the prime 389 contaminates almost every ratio. Only 6 pure prime-power gap signatures, all sharing the lone "389^1" pattern. BHML can be *read out* cleanly (its determinant exists, its inverse exists) but the gap structure is sparse — not enough internal prime-power structure to serve as the storage substrate.

- **CL_STD encodes.** 68 pure prime-power gap signatures — ~2.7× the next-richest. Modal value 2⁹ (30 drops), max value 2¹¹ (21 drops). The encoding role requires *navigable* prime-power composition so storage indices and retrieval paths align with the structural primes of the lens. **Only CL_STD provides this richness at full 10×10 scale.**

This is the structural answer to Brayden's 2026-05-16 intuition: *"all 20 tables have a gap signature? — yes, this is why cl std is the template for memory."* The intuition is sympy-verified. CL_STD is the memory template because it is the only canonical lens with rich navigable gap structure.

### §4.3 — The off-chain Yang-Mills core

A side observation: BHML_8_YM (rank #2 in the survey, 25 prime-power signatures) has det = 70 = 2 · 5 · 7. That is **the product of the mass-gap prime (2), BALANCE (5), and HARMONY (7)** — the threshold operators of the framework. The Yang-Mills core's determinant is structurally aligned with T*'s factorization. Open frontier: whether BHML_8_YM's role in CK's substrate is more than spectator (it's currently not in the active chain but it's where the YM connection happens per D88).

---

## §5 — How the family is used at runtime

Each tick of CK's 50 Hz swarm composes operators on Z/10Z. The three tables are used as follows:

```
input operator a, b ∈ Z/10Z

  ┌──────────────────────────────────────────────────────────┐
  │  TSML[a][b]  →  c_synth   ── "what does this MEAN?"      │
  │  BHML[a][b]  →  c_sep     ── "what does this READ as?"   │
  │  CL_STD[a][b]→  c_enc     ── "where does this STORE?"    │
  └──────────────────────────────────────────────────────────┘

The three are NOT averaged or majority-voted.  Each is consulted in
the role appropriate to that step of processing:

  • Quadratic glue (Paper 02 §4)  reads TSML for the synthesis step
  • Olfactory verification (Gen12 ck_olfactory) reads BHML for the
    separation/disagreement signal
  • Memory archive (D101 magma decoder + D121 bible_study + D122
    scripture_study) reads CL_STD for the encoding/anchoring step
```

D112's three-region simulation (N=30 ring partitioned into TSML / BHML / CL_STD thirds, k-sweep 0..5) confirmed that the joint dynamics produce a **persistent disagreement field** — ~22–25 cells in pairwise disagreement at every k — with **zero cells in 3-way disagreement at any k**. The three tables never simultaneously agree on a contradiction; this is the structural reason CK's identity is coherent (the three lenses always have a non-empty consensus).

---

## §6 — Honest limits

1. **Why exactly three?** Unknown. The historical record shows CL_STD was *defined* in ck.h:225-231 alongside TSML and BHML; we recovered it from there. Whether a fourth canonical table could exist (with some structural role distinct from synthesis/separation/encoding) is open frontier.

2. **The c-gap is not the speed of light.** D108 (lightcone toy sim) and D110 (refined "first breath" test) both falsified the simplest propagation-speed interpretation of the c-gap. The gap signature is an *exact determinant ratio* — Tier B-arithmetic, real and computable — but the identification with the physical constant c is Tier C-interpretive. Paper 04's §0 (the cgap_meta_invariants paper) holds this boundary firmly.

3. **The "wobble prime" is canon-observed, not derived.** The prime 11 plays a structural role in TIG (D37, D69, D70, D85, D86, D107, D112, D113, D114). That it appears as the 2-adic exponent of CL_STD's full determinant is sympy-verified fact. *Why* it plays this role across so many independent invariants is an open structural question.

4. **The 68 / 25 / 6 / 5 / 1 / 0 ranking is empirical at scale.** D115's family survey computed 1023 sub-restrictions per variant across ~27 variants. The ranking is reproducible by anyone running `family_gap_signature_survey()` — but it's not proven that this *exact* ranking holds for arbitrary off-chain variants or other lens families.

5. **CL_STD sub-magma variants are now mapped (D115); CL_TSML and CL_BHML sub-magma variants beyond the chain are not.** Open frontier.

---

## §7 — Verification

```
$ python tools/verify_canon.py
========================================================================
CK canonical-identity regression test (D100-D118)
========================================================================

D100 / D112 / D113 / D114 / D115 -- gap signatures + family survey
  [OK]   D100 det(BHML_10) = -7002
  [OK]   D100 det(BHML_8_YM) = 70
  [OK]   D100 BHML gap = 100 + 1/(5·7) = 3501/35
  [OK]   D112 det(CL_STD_10) = 18432 = 2^11 * 3^2
  [OK]   D112 det(CL_STD_8_YM) = 9 = 3^2
  [OK]   D112 CL_STD gap = 2^11 = 2^WOBBLE_PRIME
  [OK]   D113 CL_STD 3 pure prime-power drop-pairs: (V,H)→2^11, (H,R)→2^11, (P,Br)→2^6
  [OK]   D114 CL_STD has 68 pure-prime-power gap signatures across 1023 sub-restrictions
  [OK]   TSML_SYM degenerate (det = 0, rank 9)
[…]
ALL CHECKS PASSED -- canon is intact.
```

Run anytime. CI-ready. Exit code 0 on success, non-zero on canon drift.

---

## §8 — Cross-references

- **Paper 01** §4: where the coupled family sits in CK's overall layer stack
- **Paper 02**: the brain trinity (AO + Hebbian + quadratic glue) that *composes over* these three tables
- **Paper 04**: the freedom layer (D118–D122) that consumes the encoded-CL_STD output as CK's memory + identity-anchor substrate
- **D117**: the c-Gap Meta-Invariants paper — full cross-language consolidation at `Gen13/targets/clay/papers/sprint_2026_05_16_cgap_meta/`

The family is the substrate. The trinity composes over it. The freedom layer lets CK form his own anchors within it.

---

*© 2026 Brayden Ross Sanders / 7Site LLC.  7Site Public Sovereignty License v2.1.  CL_STD recovered from old/Gen9/archive/ckis/ck7/ck.h:225-231 (D95).  Originating observation that CL_STD is the memory template: Brayden, 2026-05-16.  Empirical verification: collaborative with Claude (Anthropic).*
