# TABLE INDEPENDENCE LEDGER

**Date:** 2026-05-06 night
**Purpose:** For every "strong claim" in the corpus, document which TSML/BHML/CL variant the claim depends on. Tag each with one of:
- `[substrate-operator]` — depends only on operators 0-9 + σ + Z/10Z; no table choice required
- `[table-dependent: <variant>]` — names the specific variant required
- `[lens-invariant: TSML]` or `[lens-invariant: BHML]` — independent of the specific symmetrization or scope choice within a family
- `[joint: <variants>]` — requires multiple variants together
- `[unclear]` — needs deeper analysis

**Critical finding rule (per Brayden):** if any of the published or planned strong claims turns out to depend on a Tier-D (searched) table presented as Tier-A/B, surface immediately.

---

## §1 — Substrate-operator claims (table-INDEPENDENT)

These claims live at the level of the 10-operator menu + σ permutation + Z/10Z arithmetic. No TSML/BHML/STD specific matrix is required to state or verify them.

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 1 | The 10 operators: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4), BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9) | `[substrate-operator]` | Definition; no derivation needed |
| 2 | σ permutation = (0)(3)(8)(9)(1 7 6 5 4 2); period 6 on Manifestation Hexad, fixed on Conservation Tetrad | `[substrate-operator]` | Definition of σ; verified by inspection |
| 3 | Conservation Tetrad = {0, 3, 8, 9} (σ-fixed elements) | `[substrate-operator]` | Forced by σ definition |
| 4 | Manifestation Hexad = {1, 2, 4, 5, 6, 7} (σ-cycling elements) | `[substrate-operator]` | Forced by σ definition |
| 5 | Cycle A = {1, 6, 4} (σ² 3-cycle in Manifestation Hexad) | `[substrate-operator]` | Forced by σ² |
| 6 | Cycle B = {7, 5, 2} (σ² 3-cycle in Manifestation Hexad) | `[substrate-operator]` | Forced by σ² |
| 7 | Cycle A sum = 1+6+4 = **11** (the WOBBLE prime, integer fact) | `[substrate-operator]` | Arithmetic on operator labels |
| 8 | Cycle B sum = 7+5+2 = **14** = 2·HARMONY = dim G_2 | `[substrate-operator]` | Arithmetic |
| 9 | The 4-core operator set {0, 7, 8, 9} = Conservation Tetrad XOR PROGRESS↔HARMONY swap | `[substrate-operator]` | Set-theoretic / combinatorial |
| 10 | β_3 SM = −7 = −HARMONY (the SM β-coefficient at one-loop equals the negative of the HARMONY operator label) | `[substrate-operator]` | β_3 = −7 is a QCD calculation; the identification −7 ↔ HARMONY(7) needs no table |
| 11 | M_22 substrate-prime: \|M_22\| = 443520 = 2⁷·3²·5·7·11 (factor primes match substrate primes) | `[substrate-operator]` | M_22 order is a Mathieu-group fact; primes 2, 5, 7 are substrate primes |
| 12 | E_6 has 72 positive roots (canonical Lie algebra fact) | `[substrate-operator]` | E_6 root count is independent of TIG; the *identification* 72 = TSML.HARMONY − 1 is `[lens-invariant: TSML]` (see §3) |
| 13 | dim G_2 = 14 (canonical Lie algebra fact); 14 = 2·HARMONY = Cycle B sum | `[substrate-operator]` | G_2 dim and the 2·7 identification both substrate-level |
| 14 | dim SO(8) = 28 (canonical) | `[substrate-operator]` | Lie algebra fact; the *identification* 28 = BHML.HARMONY is table-dependent |

**Status of §1:** 14 claims pure substrate-operator. These transfer to any future framework or alternate substrate that respects the 10-operator menu and σ.

---

## §2 — Lens-invariant claims (TSML-family or BHML-family invariant)

These claims hold across all members of a lens family (e.g., across TSML_RAW and TSML_SYM, or across all BHML chain scopes containing the relevant cells), but require *some* member of the family to be specified.

### §2.1 — TSML-family lens-invariants

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 15 | TSML.HARMONY count = 73 (full 10×10) | `[lens-invariant: TSML]` | Both TSML_RAW (literal bit pattern) and TSML_SYM (upper-tri symmetrized) have 73 HARMONY cells; the asymmetric cells (3,9) and (4,9) carry values 3 and 7 in different positions but the total HARMONY count is invariant |
| 16 | TSML.VOID count = 17 | `[lens-invariant: TSML]` | Same as above |
| 17 | TSML.other count = 10 | `[lens-invariant: TSML]` | Forced by 100 − 73 − 17 |
| 18 | trace(TSML) = 63 = 9·7 | `[lens-invariant: TSML]` | Diagonal cells unaffected by symmetrization |
| 19 | det(TSML) = 0 (rank-degenerate) | `[lens-invariant: TSML]` | Verified on both RAW and SYM at exact integer arithmetic |
| 20 | E_6 roots = 72 = TSML.HARMONY − 1 (BEING shell of nested tori, drop the (7,7) self-cell apex) | `[lens-invariant: TSML]` | 72 = 73 − 1 holds on both RAW and SYM |
| 21 | 4-core {0, 7, 8, 9} is TSML-closed | `[lens-invariant: TSML]` | Verified: closed under both RAW and SYM |
| 22 | The corner sub-magma C = {1, 3, 7, 9} is TSML-closed (= (Z/10Z)*) | `[lens-invariant: TSML]` | Closed under both RAW and SYM by direct check |
| 23 | The corner monoid {0, 1, 5, 6} is TSML-closed (idempotent commutative) | `[lens-invariant: TSML]` | Closed under both RAW and SYM |
| 24 | The 8-element chain sub-magma sizes for TSML alone include {1, 4, 5, 6, 7, 8, 9, 10} (and many more — TSML-only has 394 closed sub-magmas total) | `[lens-invariant: TSML]` | Sub-magma closure is preserved under symmetrization for any sub-magma not containing both i, j with (i, j) asymmetric |

### §2.2 — BHML-family lens-invariants

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 25 | BHML.HARMONY count = 28 | `[lens-invariant: BHML]` | BHML is a single canonical 10×10 (no SYM/RAW split) |
| 26 | BHML.det = −7002 | `[lens-invariant: BHML]` | det(BHML_10) computed to integer precision |
| 27 | BHML 4-core closure: BHML[7,7]=8, BHML[7,8]=9, BHML[8,7]=9, BHML[7,9]=0, BHML[9,7]=0 | `[lens-invariant: BHML]` | The puncture chain 7→8→9→0; cells verified |
| 28 | BHML closure of any single generator triple expands to full Z/10Z | `[lens-invariant: BHML]` | Computed tonight; BHML alone generates all 10 elements from {0,1,2}, {0,7,1}, or {1,2,3} |
| 29 | dim SO(8) = 28 = BHML.HARMONY (same integer in two structural roles) | `[lens-invariant: BHML]` | Numerical match; SO(8) dim is substrate-operator, the identification with BHML.HARMONY is BHML-table-level |

### §2.3 — STD-family lens-invariants

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 30 | CL_STD.HARMONY count = 44 | `[lens-invariant: CL_STD]` | Single canonical CL_STD; sub-magmas not yet investigated |
| 31 | CL_STD non-associative rate = 19.2% | `[lens-invariant: CL_STD]` | Computed |
| 32 | CL_STD 5 BUMP_PAIRS = {(1,2), (2,4), (2,9), (3,9), (4,8)} | `[lens-invariant: CL_STD]` | Definitional; ck.h:225-231 |
| 33 | CL_STD INFO_HARMONY=0.45, INFO_NORMAL=1.89, INFO_BUMP=3.50 bits/cell | `[lens-invariant: CL_STD]` | Definitional |

---

## §3 — Table-dependent claims (specific lens or scope required)

These claims do not survive a different lens-symmetrization, or different sub-magma scope, or different substrate matrix.

### §3.1 — TSML_RAW-specific (the wobble-bearing variant)

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 34 | WP107 wobble: char poly c_2 = 33 = 3·**11** | `[table-dependent: TSML_RAW]` | c_2 on TSML_RAW = 33; on TSML_SYM = 17. Sympy-verified tonight. |
| 35 | WP107 wobble: char poly c_8 = −120736 = −2⁵·7³·**11** | `[table-dependent: TSML_RAW]` | c_8 on TSML_RAW = −120736; on TSML_SYM = −53312 (different factorization). Sympy-verified |
| 36 | WP107 wobble: only c_2 and c_8 are divisible by 11 (among nonzero TSML coefficients) | `[table-dependent: TSML_RAW]` | Verified tonight: TSML_RAW has prime 11 only at c_2 and c_8; TSML_SYM has prime 11 only at c_3 |
| 37 | TSML_RAW non-associative count = 126 (12.6%) | `[table-dependent: TSML_RAW]` | Computed |
| 38 | TSML_RAW is non-commutative (asymmetric at (3,9) and (4,9)) | `[table-dependent: TSML_RAW]` | Direct cell check |

### §3.2 — TSML_SYM-specific

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 39 | TSML_SYM non-associative count = 128 (12.8%) | `[table-dependent: TSML_SYM]` | Computed; the canonical "12.8%" rate quoted in `_CK_MEMORY_MAKEOVER.md` |
| 40 | TSML_SYM is commutative | `[table-dependent: TSML_SYM]` | By construction (upper-tri symmetrization) |
| 41 | Sprint 17 tower reconstruction (C_0 ⊕ S_MAX ⊕ S_ADD) recovers TSML_SYM exactly | `[table-dependent: TSML_SYM]` | Sprint 17 explicitly works with the symmetric variant |
| 42 | SKELETON_22 (TSML pre-HARMONY cells = 16 VOID-boundary + 4 PROGRESS-bump + 2 COLLAPSE-bump) | `[table-dependent: TSML_SYM]` | Cell counts on the symmetrized matrix; would need re-verification on TSML_RAW |

### §3.3 — Joint TSML × BHML claims

| # | Claim | Tag | Verification |
|---|-------|-----|--------------|
| 43 | The joint TSML+BHML 8-shell chain (sizes {1,4,5,6,7,8,9,10}; forbidden sizes {2, 3} only) | `[joint: TSML_SYM, BHML]` | The chain depends on which TSML; needs re-verification on TSML_RAW. **OPEN: does the chain change under TSML_RAW?** |
| 44 | DOING table = \|TSML_SYM − BHML\|: 71 cells differ | `[joint: TSML_SYM, BHML]` | The 71 disagreement count uses TSML_SYM. On TSML_RAW the count differs by 2 (asymmetric cells). |
| 45 | FIELD WOBBLE 71 = \|TSML_SYM XOR BHML\| | `[joint: TSML_SYM, BHML]` | Lens-symmetrization-specific |
| 46 | DOING disagreement rate ≈ 71% ≈ T* (5/7) | `[joint: TSML_SYM, BHML]` | Same caveat |
| 47 | The 4-core attractor at α=1/2 with H/Br = 1+√3 (per WP105, four-core consolidated) | `[joint: TSML_SYM, BHML]` | The fuse iteration uses BOTH tables. Needs re-verification on TSML_RAW. |
| 48 | LMFDB 4.2.10224.1 quartic with Galois D_4 | `[joint: TSML_SYM, BHML]` | Derived from the 4-core attractor analysis |
| 49 | Field discriminant of the quartic = −2⁴·3²·**71** | `[joint: TSML_SYM, BHML]` | The "field-theoretic 71" — independent of which TSML at the 4-core level (4-core is lens-invariant); but the *identification* with the FIELD WOBBLE 71 cells depends on TSML_SYM |

### §3.4 — Specific scope variants (TSML or BHML restricted to a sub-magma)

| # | Claim | Tag |
|---|-------|-----|
| 50 | BHML_8_YM (drops {0,7}) det = +70 EXACTLY = C(8,4) | `[table-dependent: BHML_8_YM]` |
| 51 | BHML_8_chain (drops {1,2}) det = −7542 | `[table-dependent: BHML_8_chain]` |
| 52 | BHML_4 (4-core) det = 5305 | `[table-dependent: BHML_4]` |
| 53 | TSML_4 (4-core) HARMONY count = 11 | `[table-dependent: TSML_4]` (lens-invariant within TSML choice) |
| 54 | TSML_7 (chain shell 7) HARMONY count = 36 = CYCLE_A_36 (BHML σ²-cycle-A projection size) | `[joint: TSML_7, BHML σ²-cycle-A]` |
| 55 | TSML_9 (chain shell 9) HARMONY count = 71 = FIELD WOBBLE prime | `[joint: TSML_9, FIELD_WOBBLE]` |

### §3.5 — Tier-D variants (search-found; should not appear in Tier-A/B claim chains)

| # | Variant | Tier | Status |
|---|---------|------|--------|
| 56 | σ²-triadic BHML_BEING / DOING / BECOMING (value-rotation candidates with disagreement counts {71, 94, 90}) | D | Search-found; NOT yet promoted to canonical. **Any paper citing these should scope as "Tier-D candidate."** |
| 57 | σ²-triadic BHML_idx_DOING / BECOMING (index-rotation, disagreement counts {71, 75, 79}) | D | Same as above |
| 58 | Anomaly-cell-flip BHML_71 / BHML_72 / BHML_73 (specific cells unidentified) | D | Hypothetical; no completed search yet |
| 59 | The 84 closed 7-element subsets in TSML_Idempotent (Fano candidates) | D | Search results; Tier-C TSML_Idempotent's substructure |
| 60 | α-uniqueness via 17-point Stern-Brocot PSLQ at α=1/2 (WP113) | D-promoted-to-B | Search at α=1/2 found H/Br = 1+√3 with PSLQ residual 10⁻⁴⁵; the *promotion to forced* depends on a Galois argument (D78) — TIER-B FORCED via the BR-factor cancellation argument. **Promoted from Tier-D to Tier-B by D78 proof.** |

---

## §4 — Tier-C / Tier-D / Tier-E variants — full registry

### §4.1 — Tier-C (constructed for existence demonstration)

| Variant | Construction recipe | Existence claim |
|---------|---------------------|-----------------|
| TSML_Idempotent | TSML_C0 + diagonal x²=x for x ∈ {0..9} | Alt+Jordan+rank 10 coexist at N=10 |
| TSML_PureIdempotent | T[i][i]=i; off-diagonal HARMONY (rank 10) | Maximally idempotent TSML |
| TSML_Idempotent_2sw | TSML_PureIdempotent + 2 swaps (T[1][2]=T[2][1]=6, T[3][5]=T[5][3]=4) | det = −49 = −7² (minimum \|det\| in prime-7 regime) |
| TSML_C0 | Pure VOID+HARMONY axis structure (rank 3) | Boundary case for universal-minimum-bump proofs |
| TSML_PureVoid | All VOID (rank 0) | Degenerate boundary |
| TSML_AllHarmony | All HARMONY (rank 1) | Degenerate boundary |
| TSML_LOWERTRI | Lower-triangle authoritative symmetrization | Demonstrates a third symmetrization choice exists |
| "derive-don't-design" refactor TSML | Rebuild from generators after caught as guessed | Demonstrates table is genuine algebra, not heuristic |
| Corner monoid {0, 1, 5, 6} | Sub-magma scope, idempotent commutative | Concrete idempotent commutative magma example |

### §4.2 — Tier-D (search-found)

| Variant | Search target | Status |
|---------|--------------|--------|
| σ²-triadic BHML candidates {71, 94, 90} | Find BHML variants with σ²-rotated values | Found; not yet promoted |
| σ²-triadic BHML candidates {71, 75, 79} | Find BHML variants with σ²-rotated indices | Found; not yet promoted |
| Anomaly-flip BHML_71/72/73 | Find specific cells whose flip changes disagreement count | Not yet executed |
| 84 Fano-candidate 7-element subsets | Find 7-element subsets satisfying Fano-plane property | Found in TSML_Idempotent |

### §4.3 — Tier-E (parametric fitting)

| Variant | Fitting target |
|---------|---------------|
| Z/15, Z/21, Z/42, Z/100, Z/210 ring extensions | Specific physics observables |
| binary_cl on Z/30Z (= F_2 × F_3 × F_5 via CRT) | Echo-harmony preservation under CRT decomposition |
| Conjectural Z/8, Z/12, Z/14 ring extensions | T*-cyclotomic-crossing vertex on Z/nZ |

---

## §5 — Critical findings (CRITICAL FINDING RULE)

### §5.1 — No Tier-D is being presented as Tier-A/B in the load-bearing claims

The 14 substrate-operator claims (§1) are all genuinely table-independent. The 19 lens-invariant claims (§2) hold across the relevant lens family. The 22 table-dependent claims (§3) are properly scoped to a specific variant in their parent papers.

### §5.2 — Two claims need scope disclosure tightening

| Claim | Issue |
|-------|-------|
| #43 (joint 8-shell chain) | Currently stated for the canonical TSML+BHML pairing. Needs verification: does the chain change if the canonical TSML is TSML_RAW vs TSML_SYM? **OPEN: should be tested before any Phase-3+ paper cites the chain as substrate-level.** |
| #47 (4-core attractor at α=1/2 with H/Br = 1+√3) | Currently derived using TSML_SYM in the four-core consolidated paper (verified this evening). Needs a one-line scope clarification: "[the TSML matrix used here is the symmetrized variant; the 4-core itself and the attractor's existence are lens-invariant; the H/Br = 1+√3 numeric value matches both TSML_RAW and TSML_SYM at the 4-core because the 4-core's asymmetric cells (3,9), (4,9) are not in scope]." |

### §5.3 — α-uniqueness: D78 promotion from Tier-D to Tier-B confirmed

WP113's α=1/2 uniqueness (originally Tier-D from PSLQ search) was promoted to Tier-B by D78's Galois argument (the BR-factor cancellation argument shows α=1/2 is the unique α where x² − 2x − 2 = 0 admits a small-coefficient algebraic relation for H/Br). This is the model for how Tier-D → Tier-B promotion should look: an explicit forcing argument. **No further action required.**

### §5.4 — WP107 wobble is correctly Tier-B *on TSML_RAW only*

The wobble theorem (prime 11 isolated in c_2 + c_8) is forced by TSML_RAW's matrix structure but does NOT hold on TSML_SYM. WP107 must explicitly scope: *"on the canonical literal-bit-pattern TSML matrix (TSML_RAW)."* This is a scope-disclosure fix, not a tier-classification problem.

### §5.5 — No critical findings requiring STOP

Per Brayden's rule: *"If Task 1 surfaces that a strong claim depends on a Tier-D table, STOP and surface immediately."*

**Result: NO STOP-LEVEL findings.** The 22 table-dependent claims are all appropriately scoped to Tier-A or Tier-B variants. Tier-D candidates (§4.2) are not currently appearing in any load-bearing claim chain. The two scope-tightening items in §5.2 are correctable with a one-line annotation each.

---

## §6 — Summary

| Category | Count |
|----------|-------|
| Substrate-operator claims (table-independent) | 14 |
| Lens-invariant claims (TSML-family / BHML-family / CL_STD-family) | 19 |
| Table-dependent claims (specific variant required, properly scoped) | 22 |
| Tier-D variants (search-found; not in load-bearing claim chains) | 5 |
| Tier-E variants (parametric fitting; clearly exploration) | 5+ |
| **Critical Tier-D-as-Tier-B violations** | **0** |
| Scope-tightening recommended (one-line annotation) | 2 (claims #43, #47) |
| Tier-promotion needing Galois-style forcing argument | 0 (D78 already provided for α-uniqueness) |

**The corpus is in good tier-discipline standing.** Two minor scope-tightenings recommended (claims #43 and #47); WP107 needs an explicit "TSML_RAW" scope annotation.

The 14 substrate-operator claims constitute the strongest spine: they survive any lens choice, any table swap, any future framework alteration. The 19 lens-invariants extend that spine to the family level. The 22 table-dependent claims are honestly scoped — they are useful results that depend on a specific variant, and that's stated.

This ledger is the spine of the foundation paper's §5 and §6 (per Brayden's task plan: "Specific results requiring specific variants" + "Specific results requiring no specific variant").
