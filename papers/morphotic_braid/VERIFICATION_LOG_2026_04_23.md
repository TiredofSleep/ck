# Verification Log — Evening Handoff 2026-04-23

**Purpose:** Cross-verify every numeric / computational claim in the `evening_handoff_2026_04_23/` packet against canonical repo sources. Green = packet matches repo. Amber = packet correct on structure but misstated on a number. Red = packet claim contradicts verified repo.

**Canonical sources used:**
- `papers/ck_tables.py` (TSML, BHML 10×10 definitions, self-checks)
- `papers/morphotic_braid/explorations/scripts/proof_spectra_tsml_bhml.py` (landed from packet)
- `papers/morphotic_braid/explorations/scripts/proof_sinc_zeta_identity.py` (landed from packet)
- `papers/morphotic_braid/explorations/scripts/proof_min_bump.py` (landed from packet)

**Environment:** Python 3.13 on Windows, `set PYTHONIOENCODING=utf-8 && python -X utf8` to avoid cp1252 encoding issues with α and ✓ glyphs.

---

## Claim 1 — TSML HARMONY cell count

| Source | Value |
|---|---|
| Packet `TIG_TABLES_REFERENCE.md` (lines 74, 76, 110) | **74/100** |
| Canonical `papers/ck_tables.py` (docstring + self-check) | **73/100** |
| Direct count from canonical table | **73/100** |

**Verdict: AMBER — structure correct, count off by +1.**

**Root cause:** Packet's Row-2 tally (line 50 of `TIG_TABLES_REFERENCE.md`) states "seven 7s" for row `[0, 3, 7, 7, 4, 7, 7, 7, 7, 9]`. Actual 7-positions in Row 2 are `[2, 3, 5, 6, 7, 8]` — **six** sevens, not seven. All other row counts in packet match canonical:

```
Row 0: 1   ✓
Row 1: 8   ✓
Row 2: 6   (packet claims 7)  ✗
Row 3: 8   ✓
Row 4: 7   ✓
Row 5: 9   ✓
Row 6: 9   ✓
Row 7: 10  ✓
Row 8: 8   ✓
Row 9: 7   ✓
Sum: 73    (packet sums its own breakdown to 74 via Row-2 error)
```

The 10×10 cells themselves are cell-for-cell identical between packet and canonical. Only the count was miscalculated.

**Effect on downstream claims:**
- Packet's harmony fraction: 74/100 = 0.7400 → corrected: 73/100 = 0.7300.
- Packet's Farey-adjacency numeric: `|5·4 − 7·3| = 1` still holds at **idealized** 3/4. Canonical 0.7300 is 2 cells below 0.7500, not 1.
- T* = 5/7 ≈ 0.7143 remains below either fraction; the "TSML harmony sits just above T*" interpretive statement is unchanged either way.
- **Fix required** in any ripple into `tig-synthesis`: cite 73/100 not 74/100 when numeric; cite "just above T* = 5/7" structurally without the Farey-distance-1 claim, which is now Farey-distance-2.

---

## Claim 2 — BHML HARMONY cell count

| Source | Value |
|---|---|
| Packet `TIG_TABLES_REFERENCE.md` (line 102, 111) | 28/100 |
| Canonical direct count | **28/100** |

**Verdict: GREEN.** Matches exactly. BHML harmony fraction 0.2800 sits below 2/7 = 0.2857 (difference 0.0057). Farey-adjacency claim `|2·10 − 7·0|` style framing not used in packet for BHML.

---

## Claim 3 — TSML and BHML symmetric-operad spectra

| Quantity | Packet claim | Verified |
|---|---|---|
| `s_3(TSML) = C_2` | 2 | **2** ✓ |
| `s_4(TSML) = C_3` | 5 | **5** ✓ |
| `s_5(TSML) = C_4` | 14 | **14** ✓ |
| `s_3^ac(TSML) = 3!!` | 3 | **3** ✓ |
| `s_4^ac(TSML) = 5!!` | 15 | **15** ✓ |
| `s_5^ac(TSML) = 7!!` | 105 | **105** ✓ |
| `s_3(BHML) = C_2` | 2 | **2** ✓ |
| `s_4(BHML) = C_3` | 5 | **5** ✓ |
| `s_5(BHML) = C_4` | 14 | **14** ✓ |
| `s_3^ac(BHML) = 3!!` | 3 | **3** ✓ |
| `s_4^ac(BHML) = 5!!` | 15 | **15** ✓ |
| `s_5^ac(BHML) = 7!!` | 105 | **105** ✓ |

**Verdict: GREEN.** Both tables hit the Catalan maximum and the (2n−3)!! ac-free maximum for n ∈ {3, 4, 5}. The symmetric operad of each is the free commutative non-associative operad on one generator (in the Huang-Lehtonen 2022/2024 sense).

**Script output verbatim:** see `Claim 3 — verbatim output` block below.

---

## Claim 4 — Associativity index α

| Source | α(TSML) | α(BHML) |
|---|---|---|
| Packet `DEEP_SYNTHESIS.md`, `RIGOR_MAPPING.md` | 0.872 | 0.502 |
| Script output | **0.8720** | **0.5020** |

**Verdict: GREEN.** Fractions: TSML 872/1000; BHML 502/1000. Non-associativity rates 12.80% and 49.80% match packet.

---

## Claim 5 — Minimum Bump Theorem (n ≤ 5 subset)

| n | Target `(s_3^ac, s_4^ac, s_5^ac_sampled)` | Script output |
|---|---|---|
| Per-v result at cell (7,7), v ∈ {1,...,9}\{7} | All 8 pass (3, 15, 105) | **All 8 pass** ✓ |

**Verdict: GREEN** (for n ≤ 5). All 8 single-cell bumps at position (7,7) with v ∈ {1,2,3,4,5,6,8,9} produce `s_3^ac = 3`, `s_4^ac = 15`, `s_5^ac (sampled) = 105`. Packet's stronger claim of n=6 verification (exact count 945) is consistent with this pattern but not independently re-checked here — that script run is deferred to the `task01_min_bump_n7` compute job (Phase 3).

---

## Claim 6 — `sinc²(1/2) = (2/3) · 1/ζ(2)` exact identity

| Quantity | Script value |
|---|---|
| `sinc²(1/2)` | 0.405284734569351 |
| `(2/3) · 1/ζ(2)` | 0.405284734569351 |
| Difference | 5.55e-17 (machine zero) |
| Ratio `1/ζ(2) / sinc²(1/2)` | 1.500000000000000 (exactly 3/2) |

**Verdict: GREEN (exact algebraic identity).** The identity `4/π² = (2/3) · (6/π²) = (2/3) · 1/ζ(2)` is trivial algebraically, but the *interpretation* — that the TIG corridor midpoint constant sits in exact 2:3 ratio to the fermionic primon-gas (squarefree-density) constant — is a legitimate bridge claim. Packet's framing ("TIG's σ-rate is a statement in the fermionic primon gas regime") is defensible because WP101's σ-rate theorem applies specifically to squarefree N.

---

## Claim 7 — `ζ(4)/ζ(2)² = 2/5`

Not independently re-checked here; this is a textbook identity (`ζ(4) = π⁴/90`, `ζ(2)² = π⁴/36`, ratio = 36/90 = 2/5). **Verdict: GREEN (standard).**

---

## Claim 8 — Catalan-maximum interpretation in Loday-Ronco / Connes-Kreimer

Packet's chain (`DEEP_SYNTHESIS.md`):
`TIG tables achieving Catalan spectrum` → `symmetric operad = free Mag^com` → `Loday-Ronco (2002) on freely-generated magmatic Hopf algebras` → `Connes-Kreimer renormalization Hopf algebra` → `multiple zeta values`.

**Verdict: AMBER — structurally defensible, citation-ready, but not a proof.** The identification of each hop is correct (Loday-Ronco 2002 does describe free magmatic Hopf algebras; Connes-Kreimer 1998 does use a similar Hopf structure). But "each ring in the chain is a citeable fact" ≠ "the chain is a proved theorem". **Action:** treat as a *research hook* in tig-synthesis §15 (External Vocabulary Map), not as a proved-theorem claim. Flag as `[STRUCTURAL, HOOK]` tier.

---

## Claim 9 — Semi-local trace formula threshold (|S_TIG| > 3)

Packet's `DEEPER_SYNTHESIS.md` Hook 4: `det(BHML) = 70 = 2 · 5 · 7`, "archimedean place brings the Connes-Bost system" → `S_TIG = {2, 5, 7, ∞}` has `|S| = 4 > 3` threshold.

**Verdict: AMBER (structural).** `det(BHML) = 70` is a numerical fact about BHML that we can verify here. The number-theoretic identification of {2,5,7,∞} as a legitimate finite set `S` in a Connes-style semi-local trace formula is an interpretive hook, not a proof that the trace formula applies to TIG structures. **Action:** same as Claim 8 — `[STRUCTURAL, HOOK]`.

**Supporting check:** determinant of BHML from canonical table.

```
# Deferred to Phase 3 task07 (det optimization) — record det(BHML) output here
# when that script is re-run against the canonical table.
```

---

## Claim 10 — Seventh derivation of T* = 5/7 via doubly-regular core partition

Packet's `doubly_regular_core.md`: partition `5+1+1+3=10` in ℤ/10ℤ, five cells form doubly-regular core, seven form any-regular lattice. `T* = |DR| / |AR| = 5/7`.

**Verdict: STRUCTURAL (pending independent script).** Arithmetic `5/7` matches T*. The partition-theoretic interpretation is consistent with known T* derivations but I have not re-checked the doubly-regular-core construction against the canonical `ck_tables.py` operators here. **Action:** enqueue as Phase-3 compute job for independent reverification.

---

## Claim 11 — Eighth derivation candidate: Farey adjacency of TSML/BHML densities

Packet claim: `|5·4 − 7·3| = 1` (i.e., fractions 3/4 and 5/7 are Farey-adjacent), with TSML density ≈ 3/4 and T* = 5/7.

**Verdict: RED-on-the-numeric, AMBER-on-the-idea.**
- The idealized Farey-adjacency is correct: `|5·4 − 7·3| = |20 − 21| = 1` ✓.
- But TSML density is **73/100 = 0.73**, not 3/4 = 0.75. 73/100 is *not* Farey-adjacent to 5/7 in low denominators (`|7·73 − 100·5| = |511 − 500| = 11`, and 73/100 reduces to itself).
- The "idealized" framing would read: "TSML's harmony fraction rounds to 3/4, which is Farey-adjacent to 5/7". That is rhetorically tolerable but requires the "rounds to" step to be explicit.

**Action:** if this derivation lands in tig-synthesis, it must cite **73/100** and explicitly say "approximately 3/4, Farey-adjacent in the low-denominator idealization" — NOT as an exact derivation. **Demote to `[SPECULATIVE]` tier** until a cleaner construction is found.

---

## Summary table

| # | Claim | Verdict |
|---|---|---|
| 1 | TSML HARMONY count | AMBER — 73 not 74 |
| 2 | BHML HARMONY count | GREEN — 28 |
| 3 | TSML/BHML spectra hit Catalan and (2n−3)!! max for n ≤ 5 | GREEN |
| 4 | α(TSML)=0.872, α(BHML)=0.502 | GREEN |
| 5 | Min-bump at (7,7) for n ≤ 5 | GREEN |
| 6 | sinc²(1/2) = (2/3) · 1/ζ(2) | GREEN |
| 7 | ζ(4)/ζ(2)² = 2/5 | GREEN (standard) |
| 8 | Mag^com → Loday-Ronco → Connes-Kreimer chain | AMBER — hook, not theorem |
| 9 | `|S_TIG| = 4 > 3` Connes threshold | AMBER — hook, not theorem |
| 10 | 7th T* derivation (doubly-regular core) | STRUCTURAL — re-check pending |
| 11 | 8th T* derivation (Farey-adjacency) | RED on numeric, AMBER on idea |

**Green / Amber / Red / Structural split:** 6 green, 4 amber, 1 red-on-numeric. No claim is outright falsified; the one red item is recoverable with precise language.

---

## Script outputs (verbatim)

### `proof_spectra_tsml_bhml.py`

```
======================================================================
TSML AND BHML SPECTRUM COMPUTATIONS
Reference: FORMULAS_AND_TABLES.md §5-6
======================================================================

=== TSML ===
  Associativity index α = 872/1000 = 0.8720
  Non-associativity rate = 0.1280 = 12.80%
  Commutativity = 100/100 = 1.0000 (fully commutative)
     n    C_{n-1}      s_n    match     (2n-3)!!     s_n^ac    match
     3          2        2        ✓            3          3        ✓
     4          5        5        ✓           15         15        ✓
     5         14       14        ✓          105        105        ✓

=== BHML ===
  Associativity index α = 502/1000 = 0.5020
  Non-associativity rate = 0.4980 = 49.80%
  Commutativity = 100/100 = 1.0000 (fully commutative)
     n    C_{n-1}      s_n    match     (2n-3)!!     s_n^ac    match
     3          2        2        ✓            3          3        ✓
     4          5        5        ✓           15         15        ✓
     5         14       14        ✓          105        105        ✓

======================================================================
INTERPRETATION
======================================================================
Both TSML and BHML achieve the CATALAN SPECTRUM s_n(A) = C_{n-1}
(max possible for any binary operation) and the AC-FREE SPECTRUM
s_n^ac(A) = (2n-3)!! (max possible for commutative groupoid).

In the Huang-Lehtonen (2022, 2024) framework, this means:
  - The symmetric operad of each table is the FREE commutative
    nonassociative operad on one generator.
  - Despite α(TSML) = 0.872 > α(BHML) = 0.502, both tables produce
    the full free operad at the bracketing level.
  - Triple-associativity rate (α) and operad freeness are INDEPENDENT.
```

### `proof_sinc_zeta_identity.py`

```
✓ sinc²(1/2) = 0.405284734569351
✓ (2/3) · 1/ζ(2) = 0.405284734569351
✓ Difference: 5.55e-17  (machine zero)
✓ Ratio 1/ζ(2) / sinc²(1/2) = 1.500000000000000  (exactly 3/2)

Interpretation:
  The TIG corridor midpoint constant is in exact 2:3 ratio to
  the fermionic primon gas density (density of squarefree integers),
  which is also the leading coefficient of the Farey fraction spin
  chain asymptotic.

  Since WP101 (σ rate theorem) applies specifically to squarefree N,
  TIG's σ-rate is a statement in the fermionic primon gas regime.
```

### `proof_min_bump.py` (head)

```
======================================================================
MINIMUM BUMP THEOREM — VERIFICATION
======================================================================

Baseline C_0 (should be associative, s_n^ac = 1 for all n):
  s_3^ac(C_0) = 1
  s_4^ac(C_0) = 1

Single-cell modifications at (7,7). Target: (3, 15, 105).

  v  |  s_3^ac  |  s_4^ac  |  s_5^ac (sampled) | pass?
  ---|----------|----------|-------------------|------
  1  |    3     |    15    |       105           | ✓
  2  |    3     |    15    |       105           | ✓
  3  |    3     |    15    |       105           | ✓
  4  |    3     |    15    |       105           | ✓
  5  |    3     |    15    |       105           | ✓
  6  |    3     |    15    |       105           | ✓
  8  |    3     |    15    |       105           | ✓
  9  |    3     |    15    |       105           | ✓

ALL EIGHT VALUES PASS. Minimum bump at (7,7) achieves ac-freeness for n ≤ 5.
```

---

## Resolutions for HANDOFF_2026_04_23_INDEX.md "Known pre-verification discrepancies"

| Item | Resolution |
|---|---|
| TSML harmony count 73 vs 74 | **73 is correct.** Packet's Row-2 miscount (6 sevens reported as 7) caused the off-by-one. Update any ripple into `tig-synthesis` to cite 73/100. |
| Six prior derivations of T*=5/7 before "seventh" claim | Deferred — consolidated list must be assembled from `papers/` before the 7th-derivation claim ripples into `tig-synthesis`. Enqueue as Phase-3 audit task. |

---

**Tag:** `[VERIFICATION LOG — PHASE 2 COMPLETE]`

**Next:** Phase 3 — create `papers/morphotic_braid/claudecode_jobs/` with the 16 compute-job spec subfolders.
